# Results

This directory is populated by a real benchmark run:

```bash
python src/run_eval.py --trials 3        # full run
python src/run_eval.py --smoke           # cheap 3-question sanity check
```

A run writes:
- `results.jsonl` — one row per model × question (verdict, latency, consistency, judge notes)
- `summary.md` — accuracy + latency leaderboard and a model × domain table
- `accuracy_by_model.png`, `accuracy_by_domain.png` — charts for the README

**Nothing here is committed until a real run produces it.** No placeholder numbers.
