# Verified related-work citations

Compiled and URL-verified 2026-06-10 (every entry confirmed by loading the listed
arXiv/DOI/PubMed page that day — nothing cited from memory). Source material for the
preprint's Related Work section. Do not add citations to the paper that are not in
this file without verifying them the same way.

## Bucket 1 — Medical LLM QA benchmarks

1. **MedQA** — Jin et al., "What Disease does this Patient Have? A Large-scale Open
   Domain Question Answering Dataset from Medical Exams," arXiv:2009.13081 (2020).
   MCQ from US/Chinese licensing exams; the standard knowledge-recall medical benchmark.
   verified_at: https://arxiv.org/abs/2009.13081
2. **PubMedQA** — Jin et al., "PubMedQA: A Dataset for Biomedical Research Question
   Answering," EMNLP 2019, arXiv:1909.06146. Yes/no/maybe over PubMed abstracts.
   verified_at: https://arxiv.org/abs/1909.06146
3. **MultiMedQA / Med-PaLM** — Singhal et al., "Large language models encode clinical
   knowledge," Nature 620:172–180 (2023), DOI 10.1038/s41586-023-06291-2. Introduced
   MultiMedQA + physician-rated axes for long-form answers.
   verified_at: https://www.nature.com/articles/s41586-023-06291-2 (arXiv:2212.13138 also verified)
4. **Med-PaLM 2** — Singhal et al., "Towards Expert-Level Medical Question Answering
   with Large Language Models," arXiv:2305.09617 (2023). 86.5% MedQA; physicians
   preferred its long-form answers on most axes. Cite the arXiv version (journal
   version not verified).
   verified_at: https://arxiv.org/abs/2305.09617
5. **HealthBench** — Arora et al. (OpenAI), "HealthBench: Evaluating Large Language
   Models Towards Improved Human Health," arXiv:2505.08775 (2025). 5,000 health
   conversations vs 48,562 physician-written rubric criteria, model-graded — THE
   methodological precedent for rubric-based LLM-judge scoring of open-ended answers.
   verified_at: https://arxiv.org/abs/2505.08775
6. **MedHELM** — Bedi et al., "MedHELM: Holistic Evaluation of Large Language Models
   for Medical Tasks," arXiv:2505.23802 (2025); journal version Nature Medicine (2026),
   DOI 10.1038/s41591-025-04151-2. 121-task clinician-validated taxonomy, LLM-jury method.
   verified_at: https://arxiv.org/abs/2505.23802 and https://www.nature.com/articles/s41591-025-04151-2

## Bucket 2 — LLM-as-judge methodology

7. **MT-Bench / Chatbot Arena** — Zheng et al., "Judging LLM-as-a-Judge with MT-Bench
   and Chatbot Arena," NeurIPS 2023 D&B, arXiv:2306.05685. GPT-4 judge >80% agreement
   with humans; documents position/verbosity/self-enhancement biases.
   verified_at: https://arxiv.org/abs/2306.05685
8. **Self-recognition → self-preference** — Panickssery et al., "LLM Evaluators
   Recognize and Favor Their Own Generations," arXiv:2404.13076 (2024). Causal link
   between self-recognition and self-preference bias. Cite as arXiv.
   verified_at: https://arxiv.org/abs/2404.13076
9. **Self-preference quantified** — Wataoka et al., "Self-Preference Bias in
   LLM-as-a-Judge," arXiv:2410.21819 (2024). Judges favor lower-perplexity (self-like) text.
   verified_at: https://arxiv.org/abs/2410.21819

## Bucket 3 — Dental/perio LLM evaluations 2023–2026

10. **AAP in-service exam** — Danesh et al., "Artificial intelligence in dental
    education: ChatGPT's performance on the periodontic in-service examination,"
    J Periodontol 95(7):682–687 (2024), DOI 10.1002/JPER.23-0514. GPT-3.5/4: 57.9%/73.6% MCQ.
    verified_at: https://pubmed.ncbi.nlm.nih.gov/38197146/
11. **Turkish DUS perio MCQs, multi-model** — Kandemir & Sarıbaş, BMC Oral Health
    (2025), DOI 10.1186/s12903-025-07241-2. GPT-4 73.3% > DeepSeek-R1 > Gemini > Claude;
    all weaker on clinical vs knowledge items.
    verified_at: https://link.springer.com/article/10.1186/s12903-025-07241-2
12. **Open-ended perio exam (closest precedent)** — Ramlogan et al., "A pilot study of
    the performance of Chat GPT and other large language models on a written final year
    periodontology exam," BMC Med Educ (2025), DOI 10.1186/s12909-025-07195-7. 12 LLMs,
    20 short-answer perio questions, two human examiners (kappa 0.71); best LLMs 78% vs
    students 60%. Open-ended perio but human-graded, single school.
    verified_at: https://link.springer.com/article/10.1186/s12909-025-07195-7
13. **INBDE/ADAT/DAT** — Dashti et al., Imaging Science in Dentistry (2024),
    DOI 10.5624/isd.20240037. ~80% INBDE knowledge, 66–69% case-history.
    verified_at: https://isdent.org/DOIx.php?id=10.5624/isd.20240037
14. **Japanese national dental exam** — Uehara et al., J Dent Educ 89(4):459–466 (2025),
    DOI 10.1002/jdd.13766. GPT-4o 84.6% vs GPT-3.5 45.5%. (Verified via NCBI eutils,
    PMID 39538434 — PubMed page was captcha-blocked.)
    verified_at: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=39538434&retmode=json

Note: no Korean- or German-licensing-exam LLM paper was verified — do not cite one
without checking.

## Bucket 4 — Existing dedicated dental benchmarks (position against these)

15. **DentalBench / DentalQA** — Zhu et al., "DentalBench: Benchmarking and Advancing
    LLMs Capability for Bilingual Dentistry Understanding," arXiv:2508.20416 (2025).
    36,597-question bilingual DentalQA + 337M-token DentalCorpus. "DentalQA" exists only
    as this component.
    verified_at: https://arxiv.org/abs/2508.20416
16. **GlobalDentBench — CRITICAL, concurrent work** — Zhao et al., "GlobalDentBench:
    A Multinational Benchmark for Evaluating LLM Clinical Reasoning in Dentistry with
    Expert Calibration," arXiv:2605.24636 (submitted 2026-05-23). 8,978 expert-validated
    questions (MCQ/short-answer/case) across 14 specialties incl. periodontal &
    peri-implant diseases; expert-calibrated LLM judge (key-point rubrics, Gemini-3-Flash,
    98.15% expert acceptance); 12 frontier models. Dataset request-only; pipeline public.
    ⇒ Any "first in dentistry" claim is FALSE. Cite as concurrent work.
    verified_at: https://arxiv.org/abs/2605.24636
17. **OralMLLM-Bench** — Wang et al., arXiv:2605.01333 (May 2026). Multimodal (dental
    radiographs), 27 tasks — complementary, imaging not text QA.
    verified_at: https://arxiv.org/abs/2605.01333
18. (Optional) **SCMPE** — Ma et al., "Bridging the Knowledge-Action Gap by Evaluating
    LLMs in Dynamic Dental Clinical Scenarios," arXiv:2601.12974 (Jan 2026). Static
    knowledge vs dynamic clinical dialogues.
    verified_at: https://arxiv.org/abs/2601.12974

## Novelty assessment (honest)

The exact niche — periodontology-only, open-ended, expert-validated questions scored by
rubric-based LLM-judge across 7 frontier models — appears unoccupied as of 2026-06-10.
But GlobalDentBench (May 2026, concurrent) already does expert-validated short-answer +
case-based dental questions with key-point-rubric LLM-judge scoring across 12 models,
with periodontics among 14 specialties. DentalBench (2025) and Ramlogan et al. (2025)
occupy adjacent ground.

**Defensible positioning:** a small, specialty-deep, periodontology-focused open-ended
benchmark — fully public questions and rubrics (vs GlobalDentBench's request-only
dataset), guideline-cited validation log, plus judge self-preference analysis
(dual-judge agreement per Panickssery/Wataoka). Frame as a focused expert probe, not a
comprehensive benchmark. Cite GlobalDentBench explicitly as concurrent work.
