# Improvement Plan

Audit date: 2026-06-10. Everything below was verified directly against the code,
the git history, and the W&B API — not assumed.

## Where the repo actually stands

The README describes a dental LLM benchmark. The code does not contain one yet:

- `run_evals.ipynb` evaluates **8 generic logic-trick prompts** ("sentences ending
  in apple", "9.11 vs 9.9") — zero dental content. It defines 6 provider models
  (OctoAI, Novita, DeepInfra, Fireworks, Groq, Together), and the committed run
  evaluated only 3. The single scorer is `has_response` (checks the model said
  *anything*), not factual accuracy.
- `rag_evaluation_test.ipynb` is a RAG demo over **finance news** (`articles.json`
  is Novo Nordisk / Berkshire / CNBC content). Its system prompt literally says
  "You are an expert in finance." The good news: it already contains an
  `RAGCorrectnessLLMJudge` LLM-judge scorer worth reusing.
- Both notebooks derive from the W&B Weave course materials (Oct 2024).
- W&B reality check (queried 2026-06-10): `tuminha/compare-llamas` and
  `tuminha/rag-qa` have **0 runs**, last activity Oct 2024. The README's
  "Phase 1 — complete … every run logged to W&B" has no data behind it; the
  April 2026 commits only rewrote the README.

**Consequence:** the externally-suggested fix "add a results table + W&B chart to
the README" cannot be done honestly yet — there are no results to publish. The
matrix has to be (re)run first.

## Phase 0 — Hygiene (≤1 hour, mechanical)

- [x] `.env.example` added (README's `cp .env.example .env` was broken on first clone).
- [x] `requirements.txt` completed (was missing `faiss-cpu`, `numpy`, `nest_asyncio`,
      `tqdm`, `ipywidgets`, `jupyter`, and the `set_env` helper package).
- [ ] **Delete the committed `wandb/` directory.** It is not W&B run data — it is a
      Python *virtualenv named `wandb`* (`pyvenv.cfg`, `bin/activate`, `Activate.ps1`,
      man pages). That's why GitHub shows PowerShell and Roff in language stats.
      `git rm -r --cached wandb && echo "wandb/" >> .gitignore`, commit.
- [ ] **Make the README status block honest** until Phase 1 below is re-run:
      "scaffold derived from W&B Weave course; dental dataset and scoring in
      progress" — or just execute Phase 1 and skip the interim edit.
- [ ] Fix the connection-test cell: Groq's `mixtral-8x7b-32768` is deprecated and
      will fail; use a current Groq model ID.

## Phase 1 — Make it actually dental (the core value, ~1–2 days)

This is the unfair advantage: a periodontist-authored eval set. Nobody else's
harness has clinician-written rubrics.

1. **Dental QA dataset** — replace `quirky_prompts` with 30–50 questions in a
   versioned `data/dental_qa.json`, spanning: perio diagnosis (2018 AAP/EFP
   classification), implant treatment planning, oral-systemic evidence, pharmacology
   (antibiotics/anticoagulants), patient communication. Each item: question,
   clinician-written rubric, domain tag, difficulty. Author the rubrics yourself —
   that's the publishable asset.
2. **Real scorers** — replace `has_response` with: (a) LLM-judge correctness
   against the rubric (adapt `RAGCorrectnessLLMJudge` from the RAG notebook),
   (b) latency per call (Weave already captures it; surface it), (c) consistency =
   same prompt × N trials, response divergence.
3. **Refresh the model lineup** — verified 2026-06-10 on OpenRouter:
   `llama-3.1-70b-instruct` still served, but `llama-3.3-70b-instruct` and
   `llama-4-maverick`/`scout` are current. OctoAI shut down after the NVIDIA
   acquisition — drop it. Decide the benchmark question: "same open model across
   hosts" (infra comparison) vs "best models on dental knowledge" (clinical
   comparison). The second is more useful to your audience; it can include
   GPT/Claude/Gemini and collapses the old Phase 3 into Phase 1.
4. **Dental RAG corpus** — replace the finance `articles.json` with open-access
   perio/implant abstracts or Periospot articles; rebuild `article_index.faiss`
   with a script (`scripts/build_index.py`) so the index is reproducible, and stop
   committing the binary `.faiss` file.
5. **Run the matrix, publish honestly** — results land in W&B; only then add the
   README results table + one chart/report link (the original Cowork suggestion).

## Phase 2 — From notebooks to a small package (~1 day)

- `src/` with `providers.py` (one client class, provider config dict — the three
  near-identical Weave model classes collapse into one), `scorers.py`,
  `run_eval.py` (CLI: `python -m run_eval --providers groq,openrouter --trials 3`).
- Keep ONE demo notebook that imports from `src/`; delete the duplicated
  install/import boilerplate cells (cells 0–5 of each notebook are pip installs).
- Strip saved outputs from committed notebooks (`nbstripout` or pre-commit hook).
- Pin `requirements.txt` versions once the refactor settles.

## Phase 3 — Make it public-worthy (when Phase 1 data exists)

- Publish the dental QA dataset to Hugging Face under Periospot — citable artifact,
  links back to periospot.com.
- W&B public report + README badge; blog post / newsletter issue walking through
  the results ("which LLM should a dentist trust in 2026?") — strong Periospot
  content with zero extra research cost.
- GitHub Actions smoke test with mocked providers (no API spend) so the harness
  never silently rots again.
- Quarterly re-run cadence: models churn fast; a dated, versioned leaderboard is
  the thing people come back for.

## Explicitly not worth doing

- Don't add results tables/charts before re-running (would fabricate Phase 1).
- Don't benchmark 7 LLaMA hosts for latency as the headline — host latency is a
  commodity question in 2026; clinical accuracy per model is the differentiator.
- Don't keep `set-env-colab-kaggle-dotenv` — plain `python-dotenv` everywhere.
