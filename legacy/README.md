# Legacy — original W&B Weave course material

These files are the repo's starting point: adapted from the Weights & Biases
Weave course (Oct 2024). They are kept for provenance and are **not** part of the
dental benchmark.

- `run_evals_wandb_course.ipynb` — original `run_evals.ipynb`. Evaluates 8 generic
  logic-puzzle prompts across LLaMA hosts with a `has_response` scorer (checks the
  model replied, not whether it was correct). No dental content.
- `rag_evaluation_finance_demo.ipynb` — original `rag_evaluation_test.ipynb`. RAG
  demo whose corpus and system prompt are about **finance** ("expert in finance").
  Its `RAGCorrectnessLLMJudge` class is the one genuinely reusable piece — the new
  harness in `src/` borrows that LLM-judge pattern.
- `articles_finance_sample.json` / `article_index_finance.faiss` — the finance news
  corpus (Novo Nordisk, Berkshire) and its FAISS index. Replaced by a dental corpus
  in the real pipeline.

The active project lives at the repo root: `data/`, `src/`, and the rewritten README.
