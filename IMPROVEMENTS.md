# Improvement Plan & Status

Audit + pivot: 2026-06-10. Everything below was verified against the code, git
history, and the W&B API — not assumed.

## The pivot (decided)

The benchmark was reframed from "the same Llama model across 7 hosting providers"
(an infrastructure/latency question) to **"which current LLMs can a dentist trust
on clinical knowledge"** — a clinically useful comparison across Claude, GPT,
Gemini, Llama, and DeepSeek. This collapses the old Phase 3 (compare against
GPT/Claude-class models) into the core benchmark.

## Where the repo started

- `run_evals.ipynb` tested 8 generic logic prompts (not dental) with a
  `has_response` scorer. `rag_evaluation_test.ipynb` was a **finance** RAG demo.
  Both were W&B Weave course material (Oct 2024). → moved to `legacy/`.
- W&B projects `compare-llamas` / `rag-qa` have **0 runs** — the old README's
  "Phase 1 complete" had no data behind it.
- The committed `wandb/` directory was a stray **virtualenv** (cause of the
  PowerShell/Roff language stats), not run data. → removed.

## Done (2026-06-10)

- [x] **Phase 0 hygiene** — removed `wandb/` venv, archived course material to
      `legacy/`, fixed `.gitignore`, added `.env.example`, rebuilt `requirements.txt`.
- [x] **Dental dataset (draft)** — `data/dental_qa.json`: 30 questions, 6 domains,
      clinician-style rubrics (`must_include` / `must_avoid`). Marked DRAFT.
- [x] **Eval harness** — `src/`: OpenRouter client (`providers.py`), LLM-judge +
      consistency scorers (`scorers.py`), CLI runner (`run_eval.py`), charts
      (`build_visuals.py`). Verified end-to-end on synthetic data (no API key used).
- [x] **README** — honest reframe, embedded pipeline diagram + dataset chart,
      methodology, no fabricated results.

## Needs Francisco (blocks publishing real results)

1. **Clinical sign-off on the 30 rubrics.** I drafted them from mainstream
   guidelines, but a periodontist must validate each before any leaderboard is
   published. This is the one thing I cannot do for you. Review
   `data/dental_qa.json` and correct/confirm each rubric.
2. **An `OPENROUTER_API_KEY` in `.env`.** Needed to actually run the matrix. With
   it, `python src/run_eval.py --smoke` is a ~$0.10 sanity check; a full 3-trial
   run across 8 models is a few dollars.
3. **W&B entity** — runs default to project `dental-llm-benchmark` under your
   default entity; confirm if you want `tuminha` vs `periospot`.

## Next (after sign-off)

- First real run → publish `results/` charts + leaderboard into the README.
- Expand to ~75–100 questions; add a second independent judge to cross-check.
- Publish the validated dataset to Hugging Face under Periospot (citable artifact).
- Periospot write-up: "Which LLM should a dentist trust in 2026?" — content from
  the results at no extra research cost.
- GitHub Actions smoke test with mocked providers so the harness can't silently rot.

## Explicitly not doing

- No results tables/charts before a real run (would fabricate data).
- No 7-host latency race as the headline — clinical accuracy per model is the
  differentiator in 2026, not commodity host latency.
