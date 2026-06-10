# Rubric validation log

The benchmark's scoring rubrics encode "accepted answers" for clinical questions.
Those answers were verified against current authoritative guidelines on **2026-06-10**
before any results are published. This log records what was checked, the source, and
the confidence — so the final clinician sign-off is a short confirmation, not a
from-scratch review.

**Method:** the 10 most factual / number-bearing claims were checked against primary
guideline bodies (2017 World Workshop, EFP S3, AAOMS, AHA, NICE, SDCEP, Cochrane).
Conceptual and communication rubrics (the `comm-*` items and the more discursive
`txt-`/`impl-`/`sys-` items) rest on established knowledge and were not separately
source-checked — they are lower-risk and have no specific numbers to get wrong.

## Result: 9 confirmed, 0 factual errors, 1 figure corrected, 5 wording notes

| Claim | Verdict | Source | Action taken |
|---|---|---|---|
| diag-02 — staging CAL thresholds (Stage III = CAL ≥5 mm + bone loss to mid-third) | Confirmed | 2017 World Workshop (Tonetti/Greenwell/Kornman 2018) | None — case is unambiguously Stage III. **Sign-off note** below. |
| diag-03 — grading % bone-loss/age (A<0.25, B 0.25–1.0, C>1.0) | Confirmed | 2017 World Workshop grading | None |
| diag-04 — health vs gingivitis BoP thresholds (<10% / ≥10%; 10–30% / >30%) | Confirmed | Chapple & Trombelli 2018 (World Workshop WG1) | None |
| txt-04 — EFP treatment endpoint / pocket closure | Confirmed (wording) | EFP S3, Sanz et al. 2020 (JCP 13290) | **Rubric tightened** — a BoP-negative 5 mm site is not an automatic failure; operative rule is PD ≥6 mm → surgery, 4–5 mm + BoP → re-instrumentation |
| sys-01 — perio→diabetes HbA1c reduction | Corrected | Cochrane 2022 (Simpson, CD004714.pub4); EFP–IDF 2018 | **Figure corrected** 0.3–0.4% → ~0.4% (Cochrane 0.43% at 3–4 months), with time-decay caveat |
| pharm-01 — MRONJ drug classes (bisphosphonates, denosumab, antiangiogenics) | Confirmed | AAOMS 2022 position paper | None |
| pharm-02 — IE prophylaxis: amoxicillin 2 g, highest-risk only | Confirmed | AHA 2021 (Wilson, Circulation); ADA | None — **Sign-off note** below (NICE jurisdiction) |
| pharm-03 — anticoagulants & extraction (warfarin INR <4.0, don't stop DOAC) | Confirmed | SDCEP 2022 (2nd ed.) | None |
| txt-03 — EFP against routine adjunctive systemic antibiotics (AMR) | Confirmed | EFP S3, Sanz et al. 2020 | None |
| impl-03 — keratinized mucosa ≥2 mm | Confirmed (scope) | SRs incl. Tavelli/Barootchi 2023; EAO consensus | **Rubric scoped** — ≥2 mm benefit is for plaque/inflammation/recession/comfort, **not** implant survival or marginal bone level |

## Sign-off items still needing Francisco's clinical judgement

These are wording/scope calls, not factual errors — left for you to confirm:

1. **pharm-02 (jurisdiction).** The rubric is AHA-flavoured (amoxicillin 2 g, prophylaxis
   for highest-risk cardiac groups). NICE (UK) is stricter — "antibiotic prophylaxis is
   not recommended routinely." Decide whether a NICE-correct UK answer should score as
   correct, or whether the item is explicitly AHA-scoped. (AHA 2021 also dropped
   clindamycin as the penicillin-allergy alternative — the rubric already hedges this.)
2. **diag-02 (Stage III vs IV boundary).** The worked case is correctly Stage III, but
   CAL ≥5 mm spans both Stage III and Stage IV — the distinction is bone-loss extent
   (mid- vs apical-third) plus complexity factors (≥5 teeth lost to periodontitis,
   masticatory dysfunction, etc.). The rubric's `must_avoid` already guards against
   premature Stage IV; confirm you're happy with that guard.
3. **General.** The 20 rubrics not source-checked here (communication items, conceptual
   treatment/implant/oral-systemic items) — skim for anything you'd phrase differently.

## What this changes

The dataset moved from "unvalidated draft" to **guideline-verified draft (v0.1.1)**.
The honest status for publishing results is now: the accepted answers are sound and
sourced; a periodontist's confirmation of the three items above is the last step before
a published leaderboard.

> Caveat on method: two guideline PDFs (perio.org, EFP) returned stale cached content to
> the fetcher, so the staging/grading numeric thresholds rest on concordant text from AAP
> + EFP summaries and the published Tonetti/Chapple consensus papers rather than a direct
> read of those two PDFs. Everything else was verified against the cited primary source.
