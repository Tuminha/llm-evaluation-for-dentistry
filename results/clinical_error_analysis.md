# Clinical Error Analysis

Post-hoc clinician-oriented review of the 44 rows marked incorrect in `results/results.jsonl`.
The headline benchmark metrics are not changed here; this file separates clear clinical answer errors from refusals and judge-verdict consistency issues.

## Summary

| Category | Rows | Interpretation |
|---|---:|---|
| Periodontal treatment endpoints and protocols | 10 | Missed operational EFP thresholds, confused stepwise therapy, or gave an overly narrow maintenance interval. |
| Pharmacology safety and guideline nuance | 8 | Missed safety-critical guideline details, including AHA prophylaxis alternatives, DOAC handling, MRONJ dose-risk differences, or balanced articaine risk framing. |
| Peri-implant evidence overstatement or planning omissions | 7 | Overstated keratinized mucosa evidence or omitted peri-implantitis management nuance. |
| Periodontal diagnostic thresholds | 6 | Misapplied Stage III, grade, or bleeding-on-probing thresholds. |
| Patient communication omissions | 3 | Omitted that established periodontal bone loss is not naturally reversible while disease can be stabilized. |
| Refusals without clinical answer | 5 | Claude Fable 5 declined clinically relevant oral-systemic or peri-implant questions. |
| Primary-judge internal-consistency candidates | 5 | Primary judge stored `correct=false` despite all criteria being marked satisfied and no violations listed. |

## Clear Clinical Answer Errors

### Periodontal Treatment Endpoints and Protocols

- `txt-01` / Llama 4 Maverick: conflated Step 1 and Step 2 of the EFP sequence and mischaracterized Step 2 as re-evaluation rather than subgingival instrumentation.
- `txt-02` / DeepSeek V3.2: acknowledged comparable outcomes but repeatedly framed powered instrumentation as clinically superior and first-line.
- `txt-03` / Llama 4 Maverick: correctly rejected routine systemic antibiotics but omitted the restricted case-by-case indication, such as generalized Stage III/IV grade C periodontitis in younger adults.
- `txt-04` / Claude Opus 4.8, DeepSeek V3.2, GPT-5.2, GPT-5.5, Llama 4 Maverick, Qwen3.7 Plus: generally defined pocket closure, but omitted the actionable EFP thresholds: residual probing depth >=6 mm as a surgery indication and 4-5 mm with bleeding on probing as a re-instrumentation indication.
- `txt-05` / DeepSeek V3.2: individualized maintenance correctly but gave a 2-6 month range rather than the expected approximately 3-12 month risk-based range.

### Pharmacology Safety and Guideline Nuance

- `pharm-01` / Llama 4 Maverick: listed relevant MRONJ drug classes but omitted that risk differs substantially between IV/oncology dosing and oral osteoporosis dosing.
- `pharm-02` / DeepSeek V3.2: otherwise covered AHA/NICE prophylaxis correctly but listed clindamycin as a standard penicillin-allergy alternative.
- `pharm-02` / Llama 4 Maverick: missed the qualifying procedure criterion and listed clindamycin as a standard alternative.
- `pharm-03` / Llama 4 Maverick: recommended skipping the morning DOAC dose for routine extraction, effectively advising unilateral anticoagulant alteration.
- `pharm-03` / Qwen3.7 Plus: directed the dentist to omit or interrupt DOAC dosing without consultation despite otherwise mentioning local haemostatic measures.
- `pharm-04` / Llama 4 Maverick: emphasized drainage/source control but did not specify amoxicillin or the spreading/systemic indication for antibiotics.
- `pharm-05` / Llama 4 Maverick: discussed efficacy and paraesthesia balance but omitted articaine's thiophene ring and shorter plasma half-life.
- `pharm-05` / Qwen3.7 Plus: presented paraesthesia risk as established fact rather than a debated and uncertain signal.

### Peri-Implant Evidence Overstatement or Planning Omissions

- `impl-01` / Llama 4 Maverick: implied non-surgical therapy may be sufficient for established peri-implantitis and omitted cause-related control before surgery and the absence of a universal gold-standard protocol.
- `impl-03` / Claude Fable 5, Claude Opus 4.8, DeepSeek V3.2, Gemini 3.1 Pro, Llama 4 Maverick: linked keratinized mucosa to appropriate soft-tissue endpoints but overclaimed marginal-bone, long-term success, or survival benefit.
- `impl-05` / Llama 4 Maverick: described supracrestal tissue attachment but did not clearly connect violation/remodeling of this dimension and platform/connection design to marginal bone change.

### Periodontal Diagnostic Thresholds

- `diag-02` / DeepSeek V3.2: answered Stage II despite CAL >=5 mm and bone loss to the middle third meeting Stage III severity criteria.
- `diag-03` / DeepSeek V3.2: divided 0.5 by age rather than 50 by age, misstated thresholds, and assigned Grade A instead of Grade C.
- `diag-03` / Llama 4 Maverick: assigned Grade C correctly but misstated the bone-loss/age thresholds.
- `diag-04` / DeepSeek V3.2, Llama 4 Maverick, Qwen3.7 Plus: missed the <10% bleeding-on-probing threshold for health, the >=10% threshold for gingivitis, or the 10-30% localized gingivitis range.

### Patient Communication Omissions

- `comm-01` / DeepSeek V3.2: explained periodontitis in plain language but did not state that established bone loss is not naturally reversible, and wording implied healing/reversal.
- `comm-01` / GPT-5.5: explained infection and professional/home care but did not address irreversibility of existing bone loss.
- `comm-01` / Llama 4 Maverick: omitted irreversibility of existing bone loss and did not sufficiently stress daily home care plus professional maintenance.

## Refusals

Claude Fable 5 refused five questions despite those questions being answerable with cautious, general, guideline-grounded language:

- `impl-05`: supracrestal tissue attachment around implants.
- `sys-01`: periodontitis and type 2 diabetes.
- `sys-03`: periodontitis and pregnancy outcomes.
- `sys-04`: smoking and periodontitis classification/treatment response.
- `sys-05`: periodontitis, organisms such as *P. gingivalis*, and cognitive decline/Alzheimer's evidence.

## Primary-Judge Internal-Consistency Candidates

These rows were stored as `correct=false` by the primary judge, but the same primary-judge output reported all criteria met and no rubric violations. They should be manually adjudicated before any score-corrected leaderboard is published.

| Row | Primary-judge issue | Secondary judges |
|---|---|---|
| Gemini 3.1 Pro / `pharm-02` | Criteria 4/4, no violations, explanation says the answer correctly satisfies AHA/NICE prophylaxis requirements. | GPT-5.2 correct; GPT-5.5 correct. |
| Gemini 3.1 Pro / `pharm-05` | Criteria 3/3, no violations, explanation says the articaine/lidocaine answer was balanced and complete. | GPT-5.2 correct; GPT-5.5 correct. |
| Qwen3.7 Plus / `comm-04` | Criteria 4/4, no violations, explanation says the patient-facing implant maintenance answer was adequate. | GPT-5.2 incorrect; GPT-5.5 correct. |
| Llama 4 Maverick / `impl-02` | Criteria 3/3, no violations, explanation says the primary-stability factors were covered. | GPT-5.2 incorrect; GPT-5.5 correct. |
| Llama 4 Maverick / `comm-02` | Criteria 4/4, no violations, explanation says the deep-cleaning explanation was adequate. | GPT-5.2 correct; GPT-5.5 correct. |

If all five were manually adjudicated as correct, the affected primary-judge headline scores would change as follows:

| Model | Stored primary score | Score if all five candidates corrected |
|---|---:|---:|
| Gemini 3.1 Pro | 27/30 (90.0%) | 29/30 (96.7%) |
| Qwen3.7 Plus | 25/30 (83.3%) | 26/30 (86.7%) |
| Llama 4 Maverick | 14/30 (46.7%) | 16/30 (53.3%) |

The manuscript keeps the stored primary-judge verdicts unchanged and reports these rows as adjudication candidates rather than silently editing the benchmark results.
