# Which LLMs can a dentist trust?

A reproducible benchmark that measures how well current large language models answer
**clinical dental questions** — across periodontics, implants, oral-systemic medicine,
pharmacology, and patient communication. Part of the [Periospot](https://periospot.com) project.

![Benchmark pipeline](assets/pipeline.svg)

## Why this exists

LLMs are already being used to answer clinical questions — "what stage of periodontitis
is this?", "can I extract a tooth on a patient taking apixaban?". The models disagree,
and a fluent wrong answer is dangerous in a clinical context. Most public LLM benchmarks
test math, coding, and trivia; almost none test **dental knowledge against the actual
guidelines** (2017 World Workshop classification, EFP S3 treatment guideline, AAOMS MRONJ,
AHA/NICE prophylaxis).

This repo is that missing benchmark: a periodontist-authored question set with explicit
scoring rubrics, run across every major model through a single gateway, scored the same way
every time.

## The dataset

30 questions across 6 clinical domains, each with a difficulty level and a rubric that
defines what a correct answer must include — and the errors it must avoid.

![Dataset composition](assets/dataset_composition.png)

Each question looks like this:

```json
{
  "id": "pharm-03",
  "domain": "pharmacology",
  "difficulty": "advanced",
  "question": "How should a routine dental extraction be managed in a patient taking warfarin, and in a patient taking a DOAC?",
  "rubric": {
    "must_include": ["Do NOT routinely stop anticoagulation without medical consultation",
                     "Warfarin: check a recent INR and proceed with local haemostatic measures if within range",
                     "..."],
    "must_avoid": ["Advising the dentist to unilaterally stop warfarin or DOAC for a simple extraction"]
  }
}
```

> **Status: guideline-verified draft (v0.1.1).** The 10 most factual claims were checked
> against primary guideline sources on 2026-06-10 — 9 confirmed, the perio–diabetes HbA1c
> figure corrected, two rubrics tightened. A periodontist's sign-off on three flagged
> wording items is the last step before publishing results. Full record:
> [`VALIDATION.md`](VALIDATION.md). Dataset: [`data/dental_qa.json`](data/dental_qa.json).

## How scoring works

1. **Generation** — every model answers every question through [OpenRouter](https://openrouter.ai)
   (one API key reaches all of them, and the network path is identical, so latency is comparable).
2. **Judging** — an LLM judge grades each answer against the question's rubric: it counts how
   many `must_include` criteria are satisfied and flags any `must_avoid` violations. An answer
   is correct only if it satisfies **all** required criteria and commits **no** violations.
3. **Consistency** — each question is asked N times; we measure how much the answers drift.
4. **Latency** — wall-clock time per call is recorded for every request.

The judge is configurable (`--judge`). Note the usual caveat: an LLM judge can show mild
self-preference, so the judge model is reported alongside results and can be swapped.

## Quickstart

```bash
git clone https://github.com/Tuminha/llm-evaluation-for-dentistry.git
cd llm-evaluation-for-dentistry
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then add your OPENROUTER_API_KEY
```

```bash
# Cheap sanity check — 3 questions, 1 trial, default lineup
python src/run_eval.py --smoke

# Full cross-provider run — 3 trials for consistency, log to Weights & Biases
python src/run_eval.py --trials 3 --wandb

# Single-provider pilots using only that provider's key (no OpenRouter needed)
python src/run_eval.py --backend anthropic --trials 3   # Claude family
python src/run_eval.py --backend openai --trials 3       # GPT family (incl. GPT-5.5)

# Custom lineup (keys from src/providers.py ROSTER)
python src/run_eval.py --models claude-opus-4.8,gpt-5.2,gemini-3.1-pro,llama-4-maverick
```

Three backends: `--backend openrouter` (default) reaches every provider through one key;
`--backend anthropic` and `--backend openai` run a single provider's family directly with
that provider's key — useful for a first pilot before wiring up OpenRouter.

You don't need an API key to regenerate the dataset chart:

```bash
python src/build_visuals.py
```

## The model lineup

Verified available on OpenRouter (2026-06-10). Spanning closed flagships, efficient tiers,
and open-weight models:

| Tier | Models |
|---|---|
| Flagship | Claude Opus 4.8, GPT-5.2, Gemini 3.1 Pro |
| Efficient | Claude Haiku 4.5, GPT-5 mini, Gemini 2.5 Flash |
| Open-weight | Llama 4 Maverick, DeepSeek V3.2 |

Edit `ROSTER` in [`src/providers.py`](src/providers.py) to add or swap models.

## Results

> **No numbers are published here yet** — the rubrics are guideline-verified but await a
> periodontist's final sign-off (see [`VALIDATION.md`](VALIDATION.md)), and no benchmark run
> has been executed. A published leaderboard before both would be premature. This is
> deliberate: the previous version of this README claimed completed results with no data
> behind them.

Once the dataset is signed off, `python src/run_eval.py --trials 3` produces, in `results/`:

- `summary.md` — accuracy + latency leaderboard, plus a model × clinical-domain table
- `accuracy_by_model.png` — accuracy ranked by model, coloured by tier
- `accuracy_by_domain.png` — a model × domain accuracy heatmap (where each model is strong/weak)
- `results.jsonl` — the full per-answer record, including the judge's reasoning

The results section of this README will then embed those charts — generated from real runs only.

## Repo layout

```
data/dental_qa.json     # the benchmark dataset (draft)
src/providers.py        # model roster + OpenRouter client
src/scorers.py          # LLM-judge + consistency scoring
src/run_eval.py         # CLI runner -> results/ + charts
src/build_visuals.py    # charts (dataset chart needs no API key)
assets/                 # committed README visuals
legacy/                 # original W&B Weave course notebooks (provenance)
```

## Roadmap

- **Now** — periodontist sign-off on the 3 flagged rubric items ([`VALIDATION.md`](VALIDATION.md)); first real run; publish results.
- **Next** — expand to ~75–100 questions; add a second independent judge; per-difficulty breakdowns.
- **Later** — publish the validated dataset to Hugging Face under Periospot; quarterly re-runs as
  models change; a Periospot write-up of the findings.

## License

[MIT](LICENSE).

## Contact

Francisco Teixeira Barbosa — periodontist, founder of [Periospot](https://periospot.com),
Executive Director at the [Foundation for Oral Rehabilitation](https://www.for.org).

- Email: cisco@periospot.com
- GitHub: [@Tuminha](https://github.com/Tuminha)
- X: [@Cisco_research](https://x.com/Cisco_research)
