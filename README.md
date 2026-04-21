# LLM Evaluation for Dentistry

A benchmarking harness for comparing Large Language Model providers on dental knowledge tasks. Part of the [Periospot AI](https://periospot.com) project.

## Why this exists

When an LLM is used to answer clinical questions — "what's the evidence for immediate loading of single implants in the posterior maxilla?" — provider choice matters. Same model name (e.g. LLaMA 3.1 70B), same prompt, different host, different latency, different factual consistency. This repo is the harness for measuring those differences on dental content instead of guessing.

## What's in the repo

| File | Purpose |
|---|---|
| `run_evals.ipynb` | Runs dental-domain prompts across multiple LLaMA 3.1 70B hosts (OpenRouter, Groq, Together, OctoAI, Novita, DeepInfra, Fireworks) and logs results to Weights & Biases. |
| `rag_evaluation_test.ipynb` | Small RAG evaluation over a curated set of dental articles (`articles.json` + `article_index.faiss`) using OpenAI embeddings and Groq generation. |
| `articles.json` / `article_index.faiss` | Curated dental article corpus and its FAISS index, used as the RAG retrieval source. |

## Getting started

```bash
git clone https://github.com/Tuminha/llm-evaluation-for-dentistry.git
cd llm-evaluation-for-dentistry
pip install -r requirements.txt
cp .env.example .env
```

Then add the API keys you actually want to benchmark (you don't need all of them):

- `WANDB_API_KEY` — experiment tracking
- `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `TOGETHER_API_KEY` — provider access
- `OPENAI_API_KEY` — embeddings for the RAG notebook

Open the notebooks in Jupyter or VS Code and run top-to-bottom.

## What's being measured

The evaluation focuses on three axes that matter clinically:

1. **Factual accuracy on dental terminology** — does the model get the anatomy, diagnoses, and treatment steps right, or does it hallucinate plausibly.
2. **Output consistency** — identical prompt, same model, different host or different run: how much does the answer drift.
3. **Latency** — time-to-first-token and total completion time per provider, logged per call.

## Evaluation Results

This is an ongoing exploration rather than a finished benchmark. Current status:

- **Providers compared:** OpenRouter, Groq, Together, OctoAI, Novita, DeepInfra, Fireworks — all running LLaMA 3.1 70B.
- **What's been tested:** baseline dental Q&A prompts and a small RAG evaluation notebook (`rag_evaluation_test.ipynb`) against a curated dental article set (`articles.json` / `article_index.faiss`).
- **What's tracked:** per-provider latency, output consistency for identical prompts, and qualitative accuracy on dental terminology — all logged via Weights & Biases.
- **What's still missing:** a formal scoring rubric validated by clinicians, a larger dental QA test set, and side-by-side comparison with GPT-4-class models.

Findings will be written up once the rubric and test set are in place. If you're working on dental LLM evaluation and want to compare notes, open an issue or get in touch.

## Tools used

- **Weights & Biases** — experiment tracking, per-run metrics, side-by-side comparisons
- **FAISS** — vector index for the RAG corpus
- **OpenAI API** — embeddings + baseline completions
- **Groq / Together / OpenRouter** — LLaMA 3.1 70B provider access
- **Python + Jupyter** — notebook-driven experimentation

## License

[MIT](LICENSE).

## Contact

Francisco Teixeira Barbosa — periodontist, founder of [Periospot](https://periospot.com), Executive Director at the [Foundation for Oral Rehabilitation](https://www.for.org).

- Email: cisco@periospot.com
- GitHub: [@Tuminha](https://github.com/Tuminha)
- X: [@Cisco_research](https://x.com/Cisco_research)
