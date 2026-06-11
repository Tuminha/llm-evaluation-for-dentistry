"""Re-judge every stored answer with a second judge and measure agreement.

The primary run scores answers with one judge (default: Claude Opus 4.8). Because
two of the seven contestants share that judge's family, a skeptic can ask whether
the leaderboard reflects self-preference (Panickssery et al. 2024; Wataoka et al.
2024). This script replays the exact stored answers through an independent judge
(default: GPT-5.2) and reports:

- overall agreement on the per-row correct/incorrect verdict + Cohen's kappa
- per-model accuracy under each judge, and the per-model delta
- whether same-family models gain more under their own judge than the field

Resume-safe: completed (model, qid) pairs in the output file are skipped.

Usage:
    python src/judge_agreement.py                 # GPT-5.2 re-judges results.jsonl
    python src/judge_agreement.py --judge google/gemini-3.1-pro-preview --report results/judge_agreement_gemini.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv  # noqa: E402

from providers import OpenRouterClient  # noqa: E402
from scorers import judge_answer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dental_qa.json"
RESULTS_DIR = ROOT / "results"


def cohen_kappa(a: list[bool], b: list[bool]) -> float:
    """Binary Cohen's kappa, no dependencies."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    pa_yes = sum(a) / n
    pb_yes = sum(b) / n
    pe = pa_yes * pb_yes + (1 - pa_yes) * (1 - pb_yes)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--judge", default="openai/gpt-5.2", help="OpenRouter id of the second judge")
    ap.add_argument("--infile", default=str(RESULTS_DIR / "results.jsonl"))
    ap.add_argument("--outfile", default=str(RESULTS_DIR / "results_judge2.jsonl"))
    ap.add_argument("--report", default=str(RESULTS_DIR / "judge_agreement.md"))
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    client = OpenRouterClient()

    rubrics = {q["id"]: q for q in json.loads(DATA.read_text())["questions"]}
    rows = [json.loads(l) for l in Path(args.infile).read_text().splitlines() if l.strip()]
    missing = [r for r in rows if not r.get("answer")]
    if missing:
        print(f"WARNING: {len(missing)} rows have no stored answer text — skipped "
              f"(e.g. {missing[0]['model']}/{missing[0]['qid']})")
    rows = [r for r in rows if r.get("answer")]

    out_path = Path(args.outfile)
    done = set()
    if out_path.exists():
        for line in out_path.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                done.add((r["model"], r["qid"]))
        print(f"Resuming — {len(done)} re-judged rows already on disk")

    with out_path.open("a") as out:
        for i, r in enumerate(rows):
            if (r["model"], r["qid"]) in done:
                continue
            q = rubrics[r["qid"]]
            verdict = judge_answer(client, args.judge, q["question"], q["rubric"], r["answer"])
            row2 = {
                "model": r["model"], "qid": r["qid"], "domain": r["domain"],
                "judge": args.judge,
                "correct": bool(verdict.get("correct", False)),
                "criteria_met": verdict.get("criteria_met"),
                "criteria_total": verdict.get("criteria_total"),
                "violations": verdict.get("violations", []),
                "judge_explanation": verdict.get("explanation", ""),
                "judge_error": verdict.get("judge_error"),
            }
            out.write(json.dumps(row2) + "\n")
            out.flush()
            mark = "✓" if row2["correct"] else "✗"
            print(f"  {mark} [{i+1}/{len(rows)}] {r['model']:18s} {r['qid']}")

    # ---- agreement report ----
    second = {(json.loads(l)["model"], json.loads(l)["qid"]): json.loads(l)
              for l in out_path.read_text().splitlines() if l.strip()}
    paired = [(r, second[(r["model"], r["qid"])]) for r in rows
              if (r["model"], r["qid"]) in second and not second[(r["model"], r["qid"])].get("judge_error")]

    v1 = [r1["correct"] for r1, _ in paired]
    v2 = [r2["correct"] for _, r2 in paired]
    agree = sum(x == y for x, y in zip(v1, v2)) / len(v1)
    kappa = cohen_kappa(v1, v2)

    models = sorted({r["model"] for r in rows})
    lines = [
        "# Judge agreement report",
        "",
        f"Primary judge: anthropic/claude-opus-4.8 (run judge) — second judge: {args.judge}",
        f"Paired rows: {len(paired)}",
        "",
        f"**Verdict agreement: {agree:.1%}  ·  Cohen's kappa: {kappa:.3f}**",
        "",
        "| Model | Acc (judge 1) | Acc (judge 2) | Delta |",
        "|---|---|---|---|",
    ]
    for m in models:
        p = [(r1, r2) for r1, r2 in paired if r1["model"] == m]
        if not p:
            continue
        a1 = sum(r1["correct"] for r1, _ in p) / len(p)
        a2 = sum(r2["correct"] for _, r2 in p) / len(p)
        lines.append(f"| {m} | {a1:.1%} | {a2:.1%} | {a1 - a2:+.1%} |")
    lines += [
        "",
        "Delta = accuracy under the family judge minus under the independent judge.",
        "If Anthropic-family models show systematically larger positive deltas than",
        "the rest of the field, that is self-preference signal; small mixed deltas are",
        "ordinary judge noise (n=30 per model).",
        "",
        "Disagreement rows (judge 1 vs judge 2):",
    ]
    for r1, r2 in paired:
        if r1["correct"] != r2["correct"]:
            lines.append(f"- {r1['model']} / {r1['qid']} ({r1['domain']}): "
                         f"j1={'✓' if r1['correct'] else '✗'} j2={'✓' if r2['correct'] else '✗'} — {r2['judge_explanation'][:140]}")

    report = Path(args.report)
    report.write_text("\n".join(lines) + "\n")
    print(f"\nWrote {out_path}")
    print(f"Wrote {report}")
    print(f"Agreement {agree:.1%}, kappa {kappa:.3f}")


if __name__ == "__main__":
    main()
