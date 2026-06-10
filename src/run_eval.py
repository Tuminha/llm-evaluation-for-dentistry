"""Run the dental LLM benchmark.

Pipeline: load dataset -> query each model on each question (N trials) ->
LLM-judge the answers against rubrics -> aggregate accuracy / latency /
consistency -> write raw JSONL, a markdown summary table, and charts.

Examples
--------
Cheap sanity check (3 questions, default lineup, 1 trial):
    python src/run_eval.py --smoke

Full run, custom lineup, 3 trials, log to Weights & Biases:
    python src/run_eval.py --models claude-opus-4.8,gpt-5.2,gemini-3.1-pro --trials 3 --wandb

No API key is needed to build the README visuals — see build_visuals.py for that.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import dotenv_values, load_dotenv  # noqa: E402

from providers import (  # noqa: E402
    CLAUDE_LINEUP,
    CLAUDE_ROSTER,
    DEFAULT_LINEUP,
    OPENAI_LINEUP,
    OPENAI_ROSTER,
    ROSTER,
    AnthropicClient,
    OpenAIClient,
    OpenRouterClient,
)
from scorers import consistency_score, judge_answer  # noqa: E402

# Per-backend: (roster, default lineup, key env var, client class, default judge key)
BACKENDS = {
    "openrouter": (ROSTER, DEFAULT_LINEUP, "OPENROUTER_API_KEY", OpenRouterClient, "claude-opus-4.8"),
    "anthropic": (CLAUDE_ROSTER, CLAUDE_LINEUP, "ANTHROPIC_API_KEY", AnthropicClient, "opus-4.8"),
    "openai": (OPENAI_ROSTER, OPENAI_LINEUP, "OPENAI_API_KEY", OpenAIClient, "gpt-5.5"),
}

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dental_qa.json"
RESULTS_DIR = ROOT / "results"


def load_dataset(limit: int | None = None) -> tuple[dict, list[dict]]:
    payload = json.loads(DATA.read_text())
    questions = payload["questions"]
    if limit:
        # Keep domain spread when limiting: take round-robin across domains.
        by_domain: dict[str, list[dict]] = defaultdict(list)
        for q in questions:
            by_domain[q["domain"]].append(q)
        picked, pools = [], list(by_domain.values())
        while len(picked) < limit and any(pools):
            for pool in pools:
                if pool and len(picked) < limit:
                    picked.append(pool.pop(0))
        questions = picked
    return payload["metadata"], questions


def _ensure_key(var: str) -> str | None:
    """Resolve an API key without ever printing it. Returns the source name.

    Order: existing env -> repo .env -> ~/.env.periospot (Francisco's local store,
    used here only to pick up the key he authorized for this run)."""
    if os.environ.get(var):
        return "environment"
    load_dotenv(ROOT / ".env")
    if os.environ.get(var):
        return "repo .env"
    home_env = Path.home() / ".env.periospot"
    if home_env.exists():
        val = dotenv_values(home_env).get(var)
        if val:
            os.environ[var] = val
            return str(home_env)
    return None


def run(args) -> None:
    roster, default_lineup, key_var, client_cls, default_judge = BACKENDS[args.backend]
    src = _ensure_key(key_var)
    if not src:
        sys.exit(f"No {key_var} found (checked env, repo .env, ~/.env.periospot). "
                 "Add it to .env and retry.")
    print(f"Backend: {args.backend} (key from {src})")
    client = client_cls()

    lineup_keys = args.models.split(",") if args.models else default_lineup
    unknown = [k for k in lineup_keys if k not in roster]
    if unknown:
        sys.exit(f"Unknown model keys: {unknown}. Known for {args.backend}: {list(roster)}")
    models = [roster[k] for k in lineup_keys]
    judge_key = args.judge or default_judge
    judge_id = roster[judge_key].id if judge_key in roster else judge_key

    _, questions = load_dataset(limit=3 if args.smoke else args.limit)
    trials = 1 if args.smoke else args.trials

    print(f"Models: {[m.label for m in models]}")
    print(f"Judge:  {judge_id}")
    print(f"Questions: {len(questions)} | trials: {trials} | "
          f"calls ≈ {len(models) * len(questions) * trials} + {len(models) * len(questions)} judge")

    run = None
    if args.wandb:
        import wandb  # noqa: PLC0415
        run = wandb.init(entity="tuminha", project="dental-llm-benchmark",
                         config={"backend": args.backend, "models": lineup_keys,
                                 "judge": judge_id, "trials": trials})

    RESULTS_DIR.mkdir(exist_ok=True)
    raw_path = RESULTS_DIR / "results.jsonl"
    rows: list[dict] = []
    done: set[tuple[str, str]] = set()
    if raw_path.exists():  # resume: keep already-finished (model, question) results
        for line in raw_path.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                rows.append(r)
                done.add((r["model"], r["qid"]))
        if done:
            print(f"Resuming — {len(done)} model-question results already on disk")

    with raw_path.open("a") as raw:  # append so an interrupted run preserves progress
        for model in models:
            print(f"\n=== {model.label} ({model.id}) ===")
            for q in questions:
                if (model.label, q["id"]) in done:
                    continue
                answers, latencies = [], []
                for t in range(trials):
                    out = client.complete(model.id, q["question"])
                    if out["ok"]:
                        answers.append(out["text"])
                        latencies.append(out["latency_s"])
                    else:
                        print(f"  ! {q['id']} trial {t}: {out['error'][:80]}")
                first = answers[0] if answers else ""
                verdict = (judge_answer(client, judge_id, q["question"], q["rubric"], first)
                           if first else {"correct": False, "explanation": "no answer"})
                row = {
                    "model": model.label, "model_id": model.id, "tier": model.tier,
                    "qid": q["id"], "domain": q["domain"], "difficulty": q["difficulty"],
                    "correct": bool(verdict.get("correct", False)),
                    "criteria_met": verdict.get("criteria_met"),
                    "criteria_total": verdict.get("criteria_total"),
                    "violations": verdict.get("violations", []),
                    "mean_latency_s": round(sum(latencies) / len(latencies), 3) if latencies else None,
                    "consistency": consistency_score(answers) if trials > 1 else None,
                    "judge_explanation": verdict.get("explanation", ""),
                }
                rows.append(row)
                raw.write(json.dumps(row) + "\n")
                raw.flush()  # durable per result — survives a laptop sleep / kill
                mark = "✓" if row["correct"] else "✗"
                print(f"  {mark} {q['id']:9s} {row['mean_latency_s']}s  {q['domain']}")

    summary = aggregate(rows)
    write_summary(summary, rows)
    try:
        from build_visuals import charts_from_results  # noqa: PLC0415
        charts_from_results(rows, RESULTS_DIR)
    except Exception as e:  # noqa: BLE001
        print(f"(charts skipped: {e})")

    if run:
        import wandb  # noqa: PLC0415
        wandb.log({"accuracy_by_model": summary["accuracy_pct"]})
        wandb.summary.update({"overall_accuracy": summary["overall_pct"]})
        run.finish()

    print(f"\nWrote {raw_path}")
    print(f"Wrote {RESULTS_DIR / 'summary.md'}")


def aggregate(rows: list[dict]) -> dict:
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    acc_pct, lat = {}, {}
    for model, rs in by_model.items():
        acc_pct[model] = round(100 * sum(r["correct"] for r in rs) / len(rs), 1)
        lats = [r["mean_latency_s"] for r in rs if r["mean_latency_s"] is not None]
        lat[model] = round(sum(lats) / len(lats), 2) if lats else None
    overall = round(100 * sum(r["correct"] for r in rows) / len(rows), 1) if rows else 0.0
    return {"accuracy_pct": acc_pct, "latency_s": lat, "overall_pct": overall}


def write_summary(summary: dict, rows: list[dict]) -> None:
    domains = sorted({r["domain"] for r in rows})
    models = list(summary["accuracy_pct"].keys())
    by_md: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        by_md[(r["model"], r["domain"])].append(r)

    lines = ["# Benchmark results", "",
             f"Overall accuracy across all models and questions: **{summary['overall_pct']}%**", "",
             "## Accuracy and latency by model", "",
             "| Model | Accuracy | Mean latency (s) |", "|---|---|---|"]
    for m in sorted(models, key=lambda x: summary["accuracy_pct"][x], reverse=True):
        lines.append(f"| {m} | {summary['accuracy_pct'][m]}% | {summary['latency_s'][m]} |")

    lines += ["", "## Accuracy by domain", "", "| Model | " + " | ".join(domains) + " |",
              "|---|" + "|".join(["---"] * len(domains)) + "|"]
    for m in models:
        cells = []
        for d in domains:
            rs = by_md[(m, d)]
            cells.append(f"{round(100 * sum(r['correct'] for r in rs) / len(rs))}%" if rs else "—")
        lines.append(f"| {m} | " + " | ".join(cells) + " |")

    lines += ["", f"_Generated by src/run_eval.py over {len(rows)} model-question results._"]
    (RESULTS_DIR / "summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    p = argparse.ArgumentParser(description="Run the Periospot dental LLM benchmark.")
    p.add_argument("--backend", choices=list(BACKENDS), default="openrouter",
                   help="openrouter = all providers (one key); anthropic = Claude family; openai = GPT family")
    p.add_argument("--models", help="comma-separated roster keys (default: backend's default lineup)")
    p.add_argument("--judge", help="roster key or raw model id for the judge (default: a flagship)")
    p.add_argument("--trials", type=int, default=3, help="trials per question (consistency)")
    p.add_argument("--limit", type=int, help="cap number of questions (keeps domain spread)")
    p.add_argument("--smoke", action="store_true", help="3 questions, 1 trial — cheap sanity check")
    p.add_argument("--wandb", action="store_true", help="log to Weights & Biases")
    run(p.parse_args())


if __name__ == "__main__":
    main()
