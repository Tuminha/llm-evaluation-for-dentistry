"""Build the static GitHub Pages report from committed benchmark artifacts.

The interactive report intentionally has no backend and no external JavaScript
dependencies. This script derives the compact browser data bundle from the raw
JSONL files, copies static assets into docs/, and writes a portable SVG
infographic that can be used from GitHub Pages or the repository README.

Run:
    python3 src/build_pages.py
"""
from __future__ import annotations

import base64
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import random
import shutil

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DOCS_ASSETS = DOCS / "assets"
DOCS_LOGOS = DOCS_ASSETS / "logos"
ROOT_ASSETS = ROOT / "assets"
RESULTS = ROOT / "results"
DATA = ROOT / "data" / "dental_qa.json"

DATA_COMMIT = "416104585625b211732bd7355636fda8d625075f"
REPO_URL = "https://github.com/Tuminha/llm-evaluation-for-dentistry"
PAGES_URL = "https://tuminha.github.io/llm-evaluation-for-dentistry/"

MODEL_PROVIDERS = {
    "Claude Fable 5": "Anthropic",
    "Claude Opus 4.8": "Anthropic",
    "GPT-5.5": "OpenAI",
    "GPT-5.2": "OpenAI",
    "Gemini 3.1 Pro": "Google",
    "Qwen3.7 Plus": "Qwen",
    "Llama 4 Maverick": "Meta",
    "DeepSeek V3.2": "DeepSeek",
}

PROVIDER_LOGOS = {
    "Anthropic": "anthropic.png",
    "OpenAI": "openai.png",
    "Google": "gemini.png",
    "Qwen": "qwen.png",
    "Meta": "meta.png",
    "DeepSeek": "deepseek.png",
}

PROVIDER_COLORS = {
    "Anthropic": "#9B6A42",
    "OpenAI": "#10A37F",
    "Google": "#4285F4",
    "Qwen": "#6157D7",
    "Meta": "#1877F2",
    "DeepSeek": "#355CDE",
}

DOMAIN_LABELS = {
    "perio_diagnosis": "Perio diagnosis",
    "perio_treatment": "Perio treatment",
    "implants_periimplantitis": "Implants / peri-implantitis",
    "oral_systemic": "Oral-systemic",
    "pharmacology": "Pharmacology",
    "patient_communication": "Patient communication",
}

ERROR_CATEGORIES = [
    {
        "name": "Periodontal treatment endpoints and protocols",
        "rows": 10,
        "summary": "Missed EFP actionable thresholds, confused stepwise therapy, or gave an overly narrow maintenance interval.",
    },
    {
        "name": "Pharmacology safety and guideline nuance",
        "rows": 8,
        "summary": "Missed safety-critical guidance on AHA prophylaxis alternatives, DOAC handling, MRONJ dose risk, or articaine risk framing.",
    },
    {
        "name": "Peri-implant evidence overstatement or planning omissions",
        "rows": 7,
        "summary": "Overstated keratinized mucosa evidence or omitted peri-implantitis management nuance.",
    },
    {
        "name": "Periodontal diagnostic thresholds",
        "rows": 6,
        "summary": "Misapplied Stage III, grading, or bleeding-on-probing thresholds.",
    },
    {
        "name": "Patient communication omissions",
        "rows": 3,
        "summary": "Omitted that established periodontal bone loss is not naturally reversible while disease can be stabilized.",
    },
]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def bootstrap_ci(values: list[bool], *, resamples: int = 10_000, seed: int = 42) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    draws = []
    for _ in range(resamples):
        correct = sum(values[rng.randrange(n)] for _ in range(n))
        draws.append(100 * correct / n)
    draws.sort()
    return draws[int(0.025 * resamples)], draws[int(0.975 * resamples) - 1]


def pct(numer: int | float, denom: int | float) -> float:
    return 100 * numer / denom if denom else 0.0


def cohen_kappa(primary: list[bool], secondary: list[bool]) -> float:
    n = len(primary)
    observed = sum(a == b for a, b in zip(primary, secondary)) / n
    primary_yes = sum(primary) / n
    secondary_yes = sum(secondary) / n
    expected = primary_yes * secondary_yes + (1 - primary_yes) * (1 - secondary_yes)
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0


def copy_assets() -> None:
    DOCS_LOGOS.mkdir(parents=True, exist_ok=True)
    for filename in PROVIDER_LOGOS.values():
        shutil.copy2(ROOT_ASSETS / "brand_logos" / filename, DOCS_LOGOS / filename)
    shutil.copy2(ROOT_ASSETS / "accuracy_by_model.png", DOCS_ASSETS / "accuracy_by_model.png")
    shutil.copy2(ROOT_ASSETS / "accuracy_by_domain.png", DOCS_ASSETS / "accuracy_by_domain.png")
    shutil.copy2(ROOT_ASSETS / "dataset_composition.png", DOCS_ASSETS / "dataset_composition.png")
    shutil.copy2(ROOT / "paper" / "main.pdf", DOCS_ASSETS / "dental-llm-benchmark.pdf")


def model_table(rows: list[dict]) -> list[dict]:
    by_model: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)

    table = []
    for model, model_rows in by_model.items():
        outcomes = [bool(r["correct"]) for r in model_rows]
        answered = [r for r in model_rows if (r.get("answer") or "").strip()]
        ci_low, ci_high = bootstrap_ci(outcomes)
        domains = {}
        for domain in sorted({r["domain"] for r in model_rows}):
            domain_rows = [r for r in model_rows if r["domain"] == domain]
            correct = sum(bool(r["correct"]) for r in domain_rows)
            domains[domain] = {
                "correct": correct,
                "total": len(domain_rows),
                "accuracy": pct(correct, len(domain_rows)),
            }
        refusals = [r["qid"] for r in model_rows if not (r.get("answer") or "").strip()]
        latencies = [
            float(r["mean_latency_s"])
            for r in model_rows
            if r.get("mean_latency_s") is not None
        ]
        table.append({
            "model": model,
            "model_id": model_rows[0]["model_id"],
            "provider": MODEL_PROVIDERS.get(model, "Other"),
            "logo": f"assets/logos/{PROVIDER_LOGOS.get(MODEL_PROVIDERS.get(model, ''), '')}",
            "color": PROVIDER_COLORS.get(MODEL_PROVIDERS.get(model, ""), "#64748B"),
            "tier": model_rows[0].get("tier", "open"),
            "correct": sum(outcomes),
            "total": len(model_rows),
            "accuracy": pct(sum(outcomes), len(model_rows)),
            "ci_low": ci_low,
            "ci_high": ci_high,
            "answer_rate": pct(len(answered), len(model_rows)),
            "answered_accuracy": pct(sum(bool(r["correct"]) for r in answered), len(answered)),
            "latency": sum(latencies) / len(latencies) if latencies else 0.0,
            "refusals": refusals,
            "domains": domains,
        })

    return sorted(table, key=lambda row: (row["accuracy"], row["answered_accuracy"]), reverse=True)


def question_rows(rows: list[dict], questions: list[dict]) -> list[dict]:
    by_qid: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_qid[row["qid"]].append(row)

    out = []
    for q in questions:
        qrows = by_qid[q["id"]]
        correct = sum(bool(r["correct"]) for r in qrows)
        rubric_text = " ".join(q["rubric"].get("must_include", []) + q["rubric"].get("must_avoid", []))
        reference_text = " ".join(q.get("key_references", []))
        out.append({
            "id": q["id"],
            "domain": q["domain"],
            "domain_label": DOMAIN_LABELS.get(q["domain"], q["domain"]),
            "difficulty": q["difficulty"],
            "question": q["question"],
            "search_text": f"{q['id']} {q['domain']} {q['difficulty']} {q['question']} {rubric_text} {reference_text}",
            "must_include_count": len(q["rubric"].get("must_include", [])),
            "must_avoid_count": len(q["rubric"].get("must_avoid", [])),
            "correct": correct,
            "total": len(qrows),
            "accuracy": pct(correct, len(qrows)),
            "outcomes": [
                {
                    "model": r["model"],
                    "correct": bool(r["correct"]),
                    "answered": bool((r.get("answer") or "").strip()),
                    "criteria_met": r.get("criteria_met"),
                    "criteria_total": r.get("criteria_total"),
                    "violations": r.get("violations") or [],
                    "judge_explanation": r.get("judge_explanation", ""),
                }
                for r in sorted(qrows, key=lambda item: item["model"])
            ],
        })
    return out


def judge_agreement(primary_rows: list[dict], secondary_rows: list[dict]) -> dict:
    answered_primary = [r for r in primary_rows if (r.get("answer") or "").strip()]
    secondary_by_key = {
        (r["model"], r["qid"]): r
        for r in secondary_rows
        if not r.get("judge_error")
    }
    paired = [
        (row, secondary_by_key[(row["model"], row["qid"])])
        for row in answered_primary
        if (row["model"], row["qid"]) in secondary_by_key
    ]
    primary_verdicts = [bool(p[0]["correct"]) for p in paired]
    secondary_verdicts = [bool(p[1]["correct"]) for p in paired]
    by_model = defaultdict(lambda: {"primary": 0, "secondary": 0, "total": 0})
    for primary, secondary in paired:
        bucket = by_model[primary["model"]]
        bucket["total"] += 1
        bucket["primary"] += int(bool(primary["correct"]))
        bucket["secondary"] += int(bool(secondary["correct"]))
    return {
        "judge": paired[0][1]["judge"] if paired else "unknown",
        "paired": len(paired),
        "agreement": pct(sum(a == b for a, b in zip(primary_verdicts, secondary_verdicts)), len(paired)),
        "kappa": cohen_kappa(primary_verdicts, secondary_verdicts),
        "per_model": [
            {
                "model": model,
                "primary_accuracy": pct(vals["primary"], vals["total"]),
                "secondary_accuracy": pct(vals["secondary"], vals["total"]),
                "delta": pct(vals["primary"], vals["total"]) - pct(vals["secondary"], vals["total"]),
            }
            for model, vals in sorted(by_model.items())
        ],
    }


def error_analysis(rows: list[dict], judge2: list[dict], judge55: list[dict]) -> dict:
    wrong = [r for r in rows if not bool(r["correct"])]
    internal = [
        r for r in wrong
        if r.get("criteria_met") == r.get("criteria_total")
        and r.get("criteria_met") is not None
        and not r.get("violations")
    ]
    refusals = [r for r in wrong if not (r.get("answer") or "").strip()]
    judge2_idx = {(r["model"], r["qid"]): r for r in judge2}
    judge55_idx = {(r["model"], r["qid"]): r for r in judge55}
    flags = []
    for row in internal:
        key = (row["model"], row["qid"])
        flags.append({
            "model": row["model"],
            "qid": row["qid"],
            "domain": row["domain"],
            "primary": "criteria complete, no violations, stored incorrect",
            "gpt52": bool(judge2_idx.get(key, {}).get("correct")),
            "gpt55": bool(judge55_idx.get(key, {}).get("correct")),
        })
    return {
        "total_marked_incorrect": len(wrong),
        "clear_errors": len(wrong) - len(internal) - len(refusals),
        "refusals": [
            {"model": r["model"], "qid": r["qid"], "domain": r["domain"], "explanation": r["judge_explanation"]}
            for r in refusals
        ],
        "internal_candidates": flags,
        "categories": ERROR_CATEGORIES,
    }


def logo_data_uri(provider: str) -> str:
    path = ROOT_ASSETS / "brand_logos" / PROVIDER_LOGOS[provider]
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def build_infographic(models: list[dict], errors: dict) -> str:
    width, height = 1600, 900
    max_acc = 100
    bar_top = 220
    bar_base = 690
    chart_left = 90
    chart_width = 920
    gap = 16
    bar_w = (chart_width - gap * (len(models) - 1)) / len(models)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Dental LLM benchmark visual summary</title>',
        '<desc id="desc">Leaderboard, clinical error analysis, and judge agreement summary from a 30-question dental LLM benchmark.</desc>',
        '<rect width="1600" height="900" fill="#F6F8F7"/>',
        '<text x="90" y="88" fill="#17202A" font-family="Inter, Arial, sans-serif" font-size="52" font-weight="800">Which LLMs can a dentist trust?</text>',
        '<text x="90" y="132" fill="#566070" font-family="Inter, Arial, sans-serif" font-size="24">30 clinician-reviewed dental questions - 8 frontier models - rubric-based judging</text>',
        '<text x="90" y="172" fill="#6B7280" font-family="Inter, Arial, sans-serif" font-size="18">Deployment accuracy; refusals count as incorrect. Top-model intervals overlap, so small ranking gaps should be treated cautiously.</text>',
    ]

    for idx, model in enumerate(models):
        x = chart_left + idx * (bar_w + gap)
        bar_h = (model["accuracy"] / max_acc) * (bar_base - bar_top)
        y = bar_base - bar_h
        color = model["color"]
        if idx == 0:
            parts.append(f'<rect x="{x - 8:.1f}" y="{y - 16:.1f}" width="{bar_w + 16:.1f}" height="{bar_h + 32:.1f}" fill="none" stroke="#E05A5A" stroke-width="5"/>')
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="12" fill="{color}" opacity="0.84"/>')
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y + 42:.1f}" fill="#17202A" font-family="Inter, Arial, sans-serif" font-size="26" font-weight="800" text-anchor="middle">{model["accuracy"]:.1f}</text>')
        logo = logo_data_uri(model["provider"])
        parts.append(f'<circle cx="{x + bar_w / 2:.1f}" cy="{bar_base - 30}" r="26" fill="#FFFFFF" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<image href="{logo}" x="{x + bar_w / 2 - 17:.1f}" y="{bar_base - 47}" width="34" height="34" preserveAspectRatio="xMidYMid meet"/>')
        label_lines = model["model"].replace("Claude ", "Claude|").replace("Gemini ", "Gemini|").replace("Llama 4 ", "Llama 4|").replace("DeepSeek ", "DeepSeek|").replace("Qwen3.7 ", "Qwen3.7|").split("|")
        for line_idx, line in enumerate(label_lines[:2]):
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{bar_base + 36 + line_idx * 24}" fill="#1F2937" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="700" text-anchor="middle">{line}</text>')
        if model["answer_rate"] < 100:
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{bar_base - 72}" fill="#8A4B00" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" text-anchor="middle">{model["answer_rate"]:.0f}% answered</text>')

    card_x = 1080
    parts.extend([
        f'<rect x="{card_x}" y="220" width="420" height="210" rx="18" fill="#FFFFFF" stroke="#DCE4DF"/>',
        f'<text x="{card_x + 28}" y="266" fill="#17202A" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="800">Clinical error audit</text>',
        f'<text x="{card_x + 28}" y="305" fill="#1F2937" font-family="Inter, Arial, sans-serif" font-size="46" font-weight="900">{errors["clear_errors"]}</text>',
        f'<text x="{card_x + 105}" y="302" fill="#566070" font-family="Inter, Arial, sans-serif" font-size="20">clear clinical answer errors</text>',
        f'<text x="{card_x + 28}" y="348" fill="#566070" font-family="Inter, Arial, sans-serif" font-size="18">plus {len(errors["refusals"])} refusals and {len(errors["internal_candidates"])} judge-consistency flags</text>',
        f'<text x="{card_x + 28}" y="388" fill="#566070" font-family="Inter, Arial, sans-serif" font-size="18">Most common: treatment thresholds, pharmacology nuance, peri-implant evidence overstatement.</text>',
        f'<rect x="{card_x}" y="460" width="420" height="170" rx="18" fill="#FFFFFF" stroke="#DCE4DF"/>',
        f'<text x="{card_x + 28}" y="506" fill="#17202A" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="800">Judge dependence</text>',
        f'<text x="{card_x + 28}" y="548" fill="#1F2937" font-family="Inter, Arial, sans-serif" font-size="22" font-weight="800">81.7-83.8% verdict agreement</text>',
        f'<text x="{card_x + 28}" y="586" fill="#566070" font-family="Inter, Arial, sans-serif" font-size="18">GPT-5.2 and GPT-5.5 second-judge passes showed moderate agreement with Claude Opus 4.8.</text>',
        f'<rect x="{card_x}" y="660" width="420" height="110" rx="18" fill="#17202A"/>',
        f'<text x="{card_x + 28}" y="704" fill="#FFFFFF" font-family="Inter, Arial, sans-serif" font-size="24" font-weight="800">Reproducible release</text>',
        f'<text x="{card_x + 28}" y="740" fill="#C9D1D9" font-family="Inter, Arial, sans-serif" font-size="18">Raw answers, rubrics, judge verdicts, scripts, paper, and this report are public.</text>',
        '<text x="90" y="842" fill="#566070" font-family="Inter, Arial, sans-serif" font-size="18">Source: github.com/Tuminha/llm-evaluation-for-dentistry - Data commit 4161045 - June 2026</text>',
    ])
    parts.append("</svg>")
    return "\n".join(parts)


def build_report_data() -> dict:
    rows = read_jsonl(RESULTS / "results.jsonl")
    judge2 = read_jsonl(RESULTS / "results_judge2.jsonl")
    judge55 = read_jsonl(RESULTS / "results_judge_gpt55.jsonl")
    questions_payload = json.loads(DATA.read_text())
    questions = questions_payload["questions"]
    domains = questions_payload["metadata"]["domains"]
    models = model_table(rows)
    overall_correct = sum(bool(r["correct"]) for r in rows)
    data = {
        "meta": {
            "title": "Evaluating Frontier Language Models on Clinician-Reviewed Dental Questions",
            "subtitle": "A reproducible specialty benchmark for dental LLM evaluation",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repo_url": REPO_URL,
            "pages_url": PAGES_URL,
            "data_commit": DATA_COMMIT,
            "paper_pdf": "assets/dental-llm-benchmark.pdf",
            "infographic": "assets/visual-summary.svg",
        },
        "domains": [{"id": d, "label": DOMAIN_LABELS.get(d, d)} for d in domains],
        "models": models,
        "questions": question_rows(rows, questions),
        "overall": {
            "models": len(models),
            "questions": len(questions),
            "rows": len(rows),
            "accuracy": pct(overall_correct, len(rows)),
            "correct": overall_correct,
            "refusals": sum(1 for r in rows if not (r.get("answer") or "").strip()),
        },
        "error_analysis": error_analysis(rows, judge2, judge55),
        "judge_agreement": [
            judge_agreement(rows, judge2),
            judge_agreement(rows, judge55),
        ],
    }
    return data


def main() -> None:
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    copy_assets()
    data = build_report_data()

    report_js = "window.REPORT_DATA = "
    report_js += json.dumps(data, ensure_ascii=False, indent=2)
    report_js += ";\n"
    (DOCS / "report-data.js").write_text(report_js)

    svg = build_infographic(data["models"], data["error_analysis"])
    (DOCS_ASSETS / "visual-summary.svg").write_text(svg)
    (ROOT_ASSETS / "visual-summary.svg").write_text(svg)
    print(f"Wrote {DOCS / 'report-data.js'}")
    print(f"Wrote {DOCS_ASSETS / 'visual-summary.svg'}")


if __name__ == "__main__":
    main()
