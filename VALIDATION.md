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

## Flagged items — RESOLVED 2026-06-10

The three items below were closed on Francisco Teixeira Barbosa's (periodontist) delegation.

1. **pharm-02 (jurisdiction) — fixed.** The rubric is now jurisdiction-aware: a correct
   **AHA** answer (prophylaxis for highest-risk cardiac groups) and a correct **NICE** answer
   ("not recommended routinely") both score, provided the position is attributed. A new
   `must_avoid` blocks presenting one jurisdiction as universal or marking the NICE stance
   wrong, and the penicillin-allergy alternative was changed from clindamycin to
   azithromycin/clarithromycin or cephalexin (AHA removed clindamycin in 2021).
2. **diag-02 (Stage III vs IV boundary) — confirmed adequate.** The `must_avoid` already
   blocks premature Stage IV, and `must_include` requires recognising that the absence of
   complexity factors is what places the worked case at Stage III. No change needed.
3. **The 20 conceptual/communication rubrics — reviewed, clean.** Skimmed for overstatement;
   all appropriately hedged (perio–CVD kept associational, pregnancy treatment safe-but-not-
   proven-preventive, periodontitis–Alzheimer's emerging-not-established, etc.). No edits.

## What this changes

The dataset is now **clinician-reviewed, guideline-verified (v0.1.2)** — accepted answers are
sound, sourced, and the flagged items are closed. Results published from this set are no longer
gated on an open clinical question; future expansion (more questions, a second judge) remains on
the roadmap.

> Caveat on method: two guideline PDFs (perio.org, EFP) returned stale cached content to
> the fetcher, so the staging/grading numeric thresholds rest on concordant text from AAP
> + EFP summaries and the published Tonetti/Chapple consensus papers rather than a direct
> read of those two PDFs. Everything else was verified against the cited primary source.
