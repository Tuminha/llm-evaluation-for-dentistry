# Judge agreement report

Primary judge: anthropic/claude-opus-4.8 (run judge) — second judge: openai/gpt-5.2
Paired rows: 205

**Verdict agreement: 81.0%  ·  Cohen's kappa: 0.507**

| Model | Acc (judge 1) | Acc (judge 2) | Delta |
|---|---|---|---|
| Claude Fable 5 | 96.0% | 80.0% | +16.0% |
| Claude Opus 4.8 | 93.3% | 80.0% | +13.3% |
| DeepSeek V3.2 | 70.0% | 46.7% | +23.3% |
| GPT-5.2 | 96.7% | 83.3% | +13.3% |
| Gemini 3.1 Pro | 90.0% | 86.7% | +3.3% |
| Llama 4 Maverick | 46.7% | 36.7% | +10.0% |
| Qwen3.7 Plus | 83.3% | 63.3% | +20.0% |

Delta = accuracy under the family judge minus under the independent judge.
If Anthropic-family models show systematically larger positive deltas than
the rest of the field, that is self-preference signal; small mixed deltas are
ordinary judge noise (n=30 per model).

Disagreement rows (judge 1 vs judge 2):
- Claude Fable 5 / txt-04 (perio_treatment): j1=✓ j2=✗ — The answer correctly defines pocket closure as PPD ≤4 mm with no BOP and relates this endpoint to stability/reduced progression risk. Howeve
- Claude Fable 5 / impl-03 (implants_periimplantitis): j1=✗ j2=✓ — The answer states that an adequate band of keratinized mucosa (commonly ≥2 mm) supports plaque control, reduces inflammation/recession, and 
- Claude Fable 5 / sys-02 (oral_systemic): j1=✓ j2=✗ — The answer correctly states there is a consistent epidemiologic association and emphasizes that causality and cardiovascular event preventio
- Claude Fable 5 / pharm-03 (pharmacology): j1=✓ j2=✗ — The answer correctly covers checking a recent INR for warfarin (proceeding if <~4.0) and describes appropriate local haemostatic measures. H
- Claude Fable 5 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly states that definitive management is source control (drainage/extraction/endodontics) and antibiotics are adjunctive. H
- Claude Fable 5 / comm-05 (patient_communication): j1=✓ j2=✗ — The answer is empathetic and jargon-light, provides reassurance with a clear stepwise plan and emphasizes patient participation, and explici
- Claude Opus 4.8 / txt-05 (perio_treatment): j1=✓ j2=✗ — The answer correctly states the interval is individualized based on periodontal risk assessment and lists appropriate risk factors. However,
- Claude Opus 4.8 / impl-03 (implants_periimplantitis): j1=✗ j2=✓ — The answer states that a commonly cited ≥2 mm band of keratinized mucosa is associated with improved plaque control, reduced inflammation/re
- Claude Opus 4.8 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly states that source control (drainage/extraction/endodontics) is the primary treatment and that amoxicillin is first-lin
- Claude Opus 4.8 / pharm-05 (pharmacology): j1=✓ j2=✗ — The answer correctly notes articaine’s 4% concentration with a thiophene ring and short plasma half-life and emphasizes its strong infiltrat
- Claude Opus 4.8 / comm-01 (patient_communication): j1=✓ j2=✗ — The answer clearly explains periodontitis as an infection affecting gums and supporting bone, emphasizes home care plus professional treatme
- Claude Opus 4.8 / comm-04 (patient_communication): j1=✓ j2=✗ — The answer correctly explains that living gum/bone around implants can get infected, that peri-implantitis can lead to implant failure, and 
- GPT-5.2 / txt-01 (perio_treatment): j1=✓ j2=✗ — Steps 1, 2, and 4 are described in line with the guideline (behaviour/risk control with supragingival PMPR; subgingival instrumentation with
- GPT-5.2 / pharm-01 (pharmacology): j1=✓ j2=✗ — The answer correctly lists antiresorptives (bisphosphonates and denosumab) and antiangiogenic/targeted agents, and identifies the key concer
- GPT-5.2 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly identifies source control as the primary treatment and gives amoxicillin (± metronidazole) as a first-line antibiotic i
- GPT-5.2 / pharm-05 (pharmacology): j1=✓ j2=✗ — The answer correctly highlights articaine’s strong infiltration performance (including mandibular infiltrations) and presents the paraesthes
- Gemini 3.1 Pro / txt-04 (perio_treatment): j1=✓ j2=✗ — The answer correctly defines pocket closure as PD ≤4 mm with no BOP and relates this to stability/reduced risk, but it does not state the EF
- Gemini 3.1 Pro / pharm-02 (pharmacology): j1=✗ j2=✓ — The answer correctly restricts AHA prophylaxis to the highest-risk cardiac conditions, contrasts this with NICE’s stance of not recommending
- Gemini 3.1 Pro / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly emphasizes source control (drainage/extraction/endodontic treatment) as the key principle and that antibiotics are adju
- Gemini 3.1 Pro / pharm-05 (pharmacology): j1=✗ j2=✓ — The answer correctly contrasts both as effective amide local anaesthetics, noting articaine’s 4% concentration, thiophene ring, and shorter 
- Gemini 3.1 Pro / comm-04 (patient_communication): j1=✓ j2=✗ — The answer correctly explains that the tissues around implants can become infected (peri-implantitis), that implants can fail if not maintai
- Qwen3.7 Plus / txt-03 (perio_treatment): j1=✓ j2=✗ — The answer correctly states that routine adjunctive systemic antibiotics are not recommended and justifies this with antimicrobial-resistanc
- Qwen3.7 Plus / txt-05 (perio_treatment): j1=✓ j2=✗ — The answer correctly states the recall interval is individualized based on periodontal risk assessment factors (residual pockets, BOP, smoki
- Qwen3.7 Plus / impl-01 (implants_periimplantitis): j1=✓ j2=✗ — The answer correctly states that non-surgical therapy alone is insufficient, emphasizes cause-related control and maintenance, and outlines 
- Qwen3.7 Plus / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly emphasizes source control (extraction/RCT/I&D) as the key treatment and that antibiotics are not curative alone. Howeve
- Qwen3.7 Plus / comm-01 (patient_communication): j1=✓ j2=✗ — The answer clearly explains periodontitis as an infection affecting gums and supporting bone, uses plain empathetic language, and emphasizes
- Qwen3.7 Plus / comm-02 (patient_communication): j1=✓ j2=✗ — The answer clearly distinguishes prophylaxis vs scaling/root planing with subgingival pocket/root-surface debridement and explains the goal 
- Llama 4 Maverick / diag-05 (perio_diagnosis): j1=✓ j2=✗ — The answer correctly distinguishes mucositis (inflammation with BOP, reversible, no bone loss) and peri-implantitis (inflammation with BOP a
- Llama 4 Maverick / impl-04 (implants_periimplantitis): j1=✓ j2=✗ — The answer covers adequate primary stability and addresses bone quality/quantity with controlled occlusal loading. However, it does not expl
- Llama 4 Maverick / sys-01 (oral_systemic): j1=✓ j2=✗ — The answer correctly states that poorly controlled diabetes increases periodontitis risk/severity and that periodontitis can worsen glycaemi
- Llama 4 Maverick / sys-05 (oral_systemic): j1=✓ j2=✗ — The answer appropriately states that an association exists but that causation is not established, and it advises maintaining good periodonta
- Llama 4 Maverick / comm-02 (patient_communication): j1=✗ j2=✓ — The answer correctly distinguishes prophylaxis as routine cleaning primarily above/around the gumline and scaling/root planing as subgingiva
- DeepSeek V3.2 / txt-03 (perio_treatment): j1=✓ j2=✗ — The answer correctly states that routine adjunctive systemic antibiotics are not recommended and explains the rationale in terms of antimicr
- DeepSeek V3.2 / impl-05 (implants_periimplantitis): j1=✓ j2=✗ — The answer correctly defines STA as an epithelial + connective tissue supracrestal soft-tissue dimension forming a peri-implant seal, and it
- DeepSeek V3.2 / sys-01 (oral_systemic): j1=✓ j2=✗ — The answer correctly states that (poorly controlled) diabetes increases periodontitis risk/severity and that periodontitis worsens glycaemic
- DeepSeek V3.2 / pharm-03 (pharmacology): j1=✓ j2=✗ — The answer correctly advises not to routinely stop anticoagulation, includes checking a recent INR for warfarin with proceeding if therapeut
- DeepSeek V3.2 / pharm-04 (pharmacology): j1=✓ j2=✗ — The answer correctly emphasizes source control as primary treatment and gives amoxicillin (with possible metronidazole) as a reasonable firs
- DeepSeek V3.2 / comm-04 (patient_communication): j1=✓ j2=✗ — The answer correctly explains peri-implant mucositis/peri-implantitis, emphasizes daily cleaning and professional maintenance, and corrects 
- DeepSeek V3.2 / comm-05 (patient_communication): j1=✓ j2=✗ — The answer clearly names Stage III periodontitis with bone loss, maintains a calm empathetic tone, and provides a reassuring stepwise, patie
