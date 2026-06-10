"""Log a completed benchmark run to Weights & Biases — no model calls.

Reads results/results.jsonl (written by run_eval.py) and creates one W&B run under
entity=tuminha, project=dental-llm-benchmark with: summary metrics, an accuracy-by-model
bar, a results Table, and the two PNG charts. A W&B Report can then be built from it.

    python src/log_to_wandb.py --judge gpt-5.5 --trials 1 --backend openai

Prints the run URL on completion. Requires a W&B login (works via ~/.netrc).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def main() -> None:
    p = argparse.ArgumentParser(description="Log results.jsonl to Weights & Biases.")
    p.add_argument("--judge", default="gpt-5.5")
    p.add_argument("--trials", type=int, default=1)
    p.add_argument("--backend", default="openai")
    p.add_argument("--date", default="2026-06-10")
    p.add_argument("--entity", default="tuminha")
    p.add_argument("--project", default="dental-llm-benchmark")
    args = p.parse_args()

    raw = RESULTS / "results.jsonl"
    if not raw.exists():
        sys.exit(f"{raw} not found — run the benchmark first.")
    rows = [json.loads(line) for line in raw.read_text().splitlines() if line.strip()]
    if not rows:
        sys.exit("results.jsonl is empty.")

    import wandb  # noqa: PLC0415

    by_model: dict[str, list] = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    acc = {m: 100 * sum(x["correct"] for x in rs) / len(rs) for m, rs in by_model.items()}
    lat = {m: round(sum(x["mean_latency_s"] or 0 for x in rs) / len(rs), 2) for m, rs in by_model.items()}
    overall = round(100 * sum(r["correct"] for r in rows) / len(rows), 1)

    run = wandb.init(
        entity=args.entity, project=args.project, job_type="benchmark",
        name=f"dental-qa-{args.backend}-{args.date}",
        config={"backend": args.backend, "judge": args.judge, "trials": args.trials,
                "date": args.date, "n_questions": len({r["qid"] for r in rows}),
                "models": sorted(by_model)},
    )

    table = wandb.Table(columns=["model", "tier", "qid", "domain", "difficulty",
                                 "correct", "mean_latency_s", "judge_explanation"])
    for r in rows:
        table.add_data(r["model"], r.get("tier"), r["qid"], r["domain"], r["difficulty"],
                       r["correct"], r["mean_latency_s"], (r.get("judge_explanation") or "")[:300])

    models = sorted(acc, key=lambda m: acc[m], reverse=True)
    bar = wandb.Table(data=[[m, round(acc[m], 1)] for m in models], columns=["model", "accuracy_pct"])

    log = {
        "overall_accuracy_pct": overall,
        "results": table,
        "accuracy_by_model": wandb.plot.bar(bar, "model", "accuracy_pct", title="Dental accuracy by model"),
    }
    for m in models:
        log[f"accuracy/{m}"] = round(acc[m], 1)
        log[f"latency_s/{m}"] = lat[m]
    for png in ["accuracy_by_model.png", "accuracy_by_domain.png"]:
        f = RESULTS / png
        if f.exists():
            log[png.replace(".png", "")] = wandb.Image(str(f))
    wandb.log(log)
    run.finish()
    print(f"\nW&B run: {run.url}")
    print(f"Project: https://wandb.ai/{args.entity}/{args.project}")


if __name__ == "__main__":
    main()
