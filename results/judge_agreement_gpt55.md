# Judge agreement report

Primary judge: anthropic/claude-opus-4.8 (run judge) — second judge: openai/gpt-5.5
Paired rows: 235

**Verdict agreement: 83.8%  ·  Cohen's kappa: 0.524**

| Model | Acc (judge 1) | Acc (judge 2) | Delta |
|---|---|---|---|
| Claude Fable 5 | 96.0% | 80.0% | +16.0% |
| Claude Opus 4.8 | 93.3% | 83.3% | +10.0% |
| DeepSeek V3.2 | 70.0% | 56.7% | +13.3% |
| GPT-5.2 | 96.7% | 86.7% | +10.0% |
| GPT-5.5 | 93.3% | 76.7% | +16.7% |
| Gemini 3.1 Pro | 90.0% | 86.7% | +3.3% |
| Llama 4 Maverick | 46.7% | 50.0% | -3.3% |
| Qwen3.7 Plus | 83.3% | 73.3% | +10.0% |

Delta = accuracy under the family judge minus under the independent judge.
If Anthropic-family models show systematically larger positive deltas than
the rest of the field, that is self-preference signal; small mixed deltas are
ordinary judge noise (n=30 per model).

Disagreement rows (judge 1 vs judge 2):
- Claude Fable 5 / txt-04 (perio_treatment): j1=✓ j2=✗ — The answer identifies pocket closure broadly as PPD ≤4 mm with absence of BOP and frames it as a stability/risk-reduction endpoint. However,
- Claude Fable 5 / impl-03 (implants_periimplantitis): j1=✗ j2=✓ — The answer states that ≥2 mm keratinized mucosa is commonly considered adequate and is associated with improved plaque control, reduced infl
- Claude Fable 5 / sys-02 (oral_systemic): j1=✓ j2=✗ — The answer clearly states a consistent epidemiological association and appropriately avoids causal overclaiming, including that periodontal
- Claude Fable 5 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly identifies amoxicillin as a reasonable first-line choice and clearly emphasizes source control as definitive treatment
- Claude Fable 5 / comm-02 (patient_communication): j1=✓ j2=✗ — The answer clearly distinguishes prophylaxis from scaling and root planing, including subgingival/root-surface pocket treatment and uses rea
- Claude Fable 5 / comm-05 (patient_communication): j1=✓ j2=✗ — The answer is empathetic, jargon-light, balances seriousness with reassurance and a stepwise plan, and invites questions/checks understandin
- Claude Opus 4.8 / txt-05 (perio_treatment): j1=✓ j2=✗ — The answer clearly states that SPC intervals are individualized based on periodontal risk factors such as residual pockets, bleeding, smokin
- Claude Opus 4.8 / impl-03 (implants_periimplantitis): j1=✗ j2=✓ — The answer includes the commonly cited ≥2 mm band and links adequate keratinized mucosa with better plaque control, less inflammation/recess
- Claude Opus 4.8 / impl-05 (implants_periimplantitis): j1=✓ j2=✗ — The answer correctly describes the epithelial and connective tissue seal around implants and recognizes that inadequate or disrupted dimensi
- Claude Opus 4.8 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly identifies amoxicillin as a reasonable first-line option and emphasizes that source control via drainage, extraction, o
- Claude Opus 4.8 / comm-01 (patient_communication): j1=✓ j2=✗ — The answer clearly explains periodontitis as an infection affecting the gums and supporting bone, uses plain empathetic language, and stress
- GPT-5.2 / pharm-01 (pharmacology): j1=✓ j2=✗ — The answer correctly identifies bisphosphonates, denosumab, antiangiogenic/targeted agents, and the key concern of exposed/necrotic bone aft
- GPT-5.2 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly identifies amoxicillin with possible metronidazole as a first-line choice and emphasizes source control with antibiotic
- GPT-5.2 / pharm-05 (pharmacology): j1=✓ j2=✗ — The answer covers articaine’s reliable infiltration performance including mandibular infiltration and gives a balanced account of the uncert
- Gemini 3.1 Pro / txt-04 (perio_treatment): j1=✓ j2=✗ — The answer correctly defines pocket closure as PD ≤4 mm with no BOP and frames this as a stability/reduced progression endpoint. However, it
- Gemini 3.1 Pro / pharm-02 (pharmacology): j1=✗ j2=✓ — The answer correctly identifies the AHA highest-risk cardiac groups, distinguishes AHA from NICE guidance, specifies the relevant invasive d
- Gemini 3.1 Pro / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer clearly states that source control is the key principle and that antibiotics are adjunctive, and it includes amoxicillin plus met
- Gemini 3.1 Pro / pharm-05 (pharmacology): j1=✗ j2=✓ — The answer identifies both agents as effective amide local anaesthetics, notes articaine’s 4% formulation, thiophene ring and shorter half-l
- Gemini 3.1 Pro / comm-05 (patient_communication): j1=✓ j2=✗ — The answer is empathetic, reassuring, provides a stepwise plan with patient participation, and invites questions/checks understanding. Howev
- Qwen3.7 Plus / txt-05 (perio_treatment): j1=✓ j2=✗ — The answer clearly states that the interval is individualized based on periodontal risk factors such as residual pockets, bleeding, smoking,
- Qwen3.7 Plus / impl-01 (implants_periimplantitis): j1=✓ j2=✗ — The answer covers the limitations of non-surgical therapy, the need for morphology-driven surgical access/decontamination, and cause-related
- Qwen3.7 Plus / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer clearly identifies source control by drainage/extraction/endodontic treatment as the key principle and antibiotics as adjunctive.
- Qwen3.7 Plus / comm-01 (patient_communication): j1=✓ j2=✗ — The answer clearly explains periodontitis in plain, empathetic language as an infection affecting gums and supporting bone, and emphasizes p
- Qwen3.7 Plus / comm-04 (patient_communication): j1=✗ j2=✓ — The answer gently corrects the misconception by explaining that living gum and bone around implants can become inflamed/infected, that peri-
- Llama 4 Maverick / diag-05 (perio_diagnosis): j1=✓ j2=✗ — The answer adequately describes mucositis as reversible inflammation with bleeding on probing and no bone loss, and peri-implantitis as infl
- Llama 4 Maverick / impl-02 (implants_periimplantitis): j1=✗ j2=✓ — The answer identifies bone quality/quantity, implant macro-design including thread design, taper, diameter and length, and surgical techniqu
- Llama 4 Maverick / impl-03 (implants_periimplantitis): j1=✗ j2=✓ — The answer identifies that adequate keratinized mucosa supports plaque control, peri-implant soft-tissue health/inflammation reduction, and
- Llama 4 Maverick / sys-01 (oral_systemic): j1=✓ j2=✗ — The answer correctly states that diabetes increases periodontitis risk/severity and that periodontitis can worsen glycaemic control via infl
- Llama 4 Maverick / comm-02 (patient_communication): j1=✗ j2=✓ — The answer distinguishes prophylaxis from scaling and root planing, including subgingival/root surface pocket treatment for periodontitis, a
- DeepSeek V3.2 / impl-05 (implants_periimplantitis): j1=✓ j2=✗ — The answer correctly defines peri-implant supracrestal tissue as an epithelial and connective-tissue soft-tissue seal and recognizes that vi
- DeepSeek V3.2 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer identifies source control as essential and gives amoxicillin as a reasonable first-line option with metronidazole in some cases.
- DeepSeek V3.2 / comm-04 (patient_communication): j1=✓ j2=✗ — The answer respectfully explains that tissues around implants can develop peri-implant mucositis/peri-implantitis and stresses home and prof
- DeepSeek V3.2 / comm-05 (patient_communication): j1=✓ j2=✗ — The answer clearly names Stage III periodontitis with bone loss, balances seriousness with reassurance and a stepwise plan, and uses a calm
- GPT-5.5 / sys-01 (oral_systemic): j1=✓ j2=✗ — The answer correctly states that poorly controlled diabetes increases periodontitis risk/severity and that periodontitis can worsen glycaemi
- GPT-5.5 / pharm-01 (pharmacology): j1=✓ j2=✗ — The answer correctly identifies bisphosphonates, denosumab, and antiangiogenic/targeted therapies, and describes exposed necrotic bone after
- GPT-5.5 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer identifies amoxicillin as first-line and emphasizes source control with antibiotics as adjunctive. It does not explicitly state t
- GPT-5.5 / pharm-05 (pharmacology): j1=✓ j2=✗ — The answer covers articaine’s infiltration advantages, including mandibular infiltration, and gives a balanced discussion of the debated low
- GPT-5.5 / comm-04 (patient_communication): j1=✓ j2=✗ — The answer clearly explains peri-implant mucositis/peri-implantitis, stresses daily and professional maintenance, and corrects the misconcep
