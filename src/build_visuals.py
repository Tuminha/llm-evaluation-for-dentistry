"""Generate charts for the README.

Two kinds:
1. dataset_composition() — needs NO API key. Reads data/dental_qa.json and plots
   the question mix by domain and difficulty. Honest visual value you can commit
   today, before any model has been run.
2. charts_from_results() — called by run_eval.py after a real run; plots accuracy
   by model and a model×domain accuracy heatmap from actual results.

Run directly to (re)build the dataset chart:
    python src/build_visuals.py
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.offsetbox import AnnotationBbox, OffsetImage  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dental_qa.json"
ASSETS = ROOT / "assets"
BRAND_LOGOS = ASSETS / "brand_logos"

# Periospot-leaning dark palette.
INK = "#0E1116"
PANEL = "#161B22"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
ACCENT = "#3FB6B2"   # teal
DIFF_COLORS = {"basic": "#3FB6B2", "intermediate": "#E0A458", "advanced": "#E05A5A"}
TIER_COLORS = {"flagship": "#3FB6B2", "efficient": "#E0A458", "open": "#9A7DDE"}
PROVIDER_COLORS = {
    "Anthropic": "#B88A5A",
    "OpenAI": "#10A37F",
    "Google": "#4285F4",
    "Qwen": "#6B5CFF",
    "Meta": "#1877F2",
    "DeepSeek": "#355CDE",
}
PROVIDER_BADGES = {
    "Anthropic": "A",
    "OpenAI": "O",
    "Google": "G",
    "Qwen": "Q",
    "Meta": "M",
    "DeepSeek": "D",
}
PROVIDER_LOGOS = {
    "Anthropic": BRAND_LOGOS / "anthropic.png",
    "OpenAI": BRAND_LOGOS / "openai.png",
    "Google": BRAND_LOGOS / "gemini.png",
    "Qwen": BRAND_LOGOS / "qwen.png",
    "Meta": BRAND_LOGOS / "meta.png",
    "DeepSeek": BRAND_LOGOS / "deepseek.png",
}
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

_LOGO_CACHE: dict[str, object] = {}

DOMAIN_LABELS = {
    "perio_diagnosis": "Perio\ndiagnosis",
    "perio_treatment": "Perio\ntreatment",
    "implants_periimplantitis": "Implants /\nperi-implantitis",
    "oral_systemic": "Oral-\nsystemic",
    "pharmacology": "Pharma-\ncology",
    "patient_communication": "Patient\ncommunication",
}


def _style(ax, fig):
    fig.patch.set_facecolor(INK)
    ax.set_facecolor(PANEL)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=TEXT, labelsize=10)
    ax.title.set_color(TEXT)
    ax.yaxis.label.set_color(MUTED)
    ax.xaxis.label.set_color(MUTED)


def _provider_logo(provider: str):
    if provider not in _LOGO_CACHE:
        logo_path = PROVIDER_LOGOS.get(provider)
        _LOGO_CACHE[provider] = plt.imread(logo_path) if logo_path and logo_path.exists() else None
    return _LOGO_CACHE[provider]


def dataset_composition(out: Path | None = None) -> Path:
    payload = json.loads(DATA.read_text())
    qs = payload["questions"]
    domains = payload["metadata"]["domains"]

    stacks: dict[str, Counter] = {d: Counter() for d in domains}
    for q in qs:
        stacks[q["domain"]][q["difficulty"]] += 1

    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=160)
    _style(ax, fig)
    x = range(len(domains))
    bottoms = [0] * len(domains)
    for diff in ["basic", "intermediate", "advanced"]:
        vals = [stacks[d].get(diff, 0) for d in domains]
        ax.bar(x, vals, bottom=bottoms, color=DIFF_COLORS[diff], label=diff,
               width=0.62, edgecolor=INK, linewidth=1.5)
        bottoms = [b + v for b, v in zip(bottoms, vals)]

    ax.set_xticks(list(x))
    ax.set_xticklabels([DOMAIN_LABELS.get(d, d) for d in domains], fontsize=9.5)
    ax.set_ylabel("Questions")
    ax.set_title(f"Dental QA benchmark — {len(qs)} questions across {len(domains)} clinical domains",
                 fontsize=13, pad=14, loc="left", color=TEXT)
    ax.set_ylim(0, max(bottoms) + 1)
    leg = ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=10)
    for t in leg.get_texts():
        t.set_color(TEXT)
    for xi, total in zip(x, bottoms):
        ax.text(xi, total + 0.12, str(total), ha="center", color=MUTED, fontsize=10)

    fig.text(0.012, 0.02, "v0.1.0-draft · Periospot Dental LLM Benchmark",
             color=MUTED, fontsize=8)
    fig.tight_layout()
    out = out or (ASSETS / "dataset_composition.png")
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, facecolor=INK, bbox_inches="tight")
    plt.close(fig)
    return out


def charts_from_results(rows: list[dict], out_dir: Path) -> list[Path]:
    out_dir.mkdir(exist_ok=True)
    written = []

    # 1) Editorial leaderboard by model.
    by_model: dict[str, list] = defaultdict(list)
    tier_of = {}
    for r in rows:
        by_model[r["model"]].append(r["correct"])
        tier_of[r["model"]] = r.get("tier", "open")
    models = sorted(by_model, key=lambda m: sum(by_model[m]) / len(by_model[m]), reverse=True)
    accs = [100 * sum(by_model[m]) / len(by_model[m]) for m in models]
    answer_rates = {
        m: 100 * sum(bool(r.get("answer")) for r in rows if r["model"] == m) / len(by_model[m])
        for m in models
    }

    fig, ax = plt.subplots(figsize=(12.8, 6.8), dpi=180)
    fig.patch.set_facecolor("#F7F4EF")
    ax.set_facecolor("#F7F4EF")
    x = list(range(len(models)))
    colors = [PROVIDER_COLORS.get(MODEL_PROVIDERS.get(m, ""), ACCENT) for m in models]
    bars = ax.bar(x, accs, color=colors, width=0.64, edgecolor="#F7F4EF", linewidth=2.4, zorder=2)

    # Highlight the leader without implying statistical separation from the top cluster.
    leader = bars[0]
    ax.add_patch(plt.Rectangle((leader.get_x() - 0.08, -2.3), leader.get_width() + 0.16,
                               leader.get_height() + 4.8, fill=False, linewidth=2.4,
                               edgecolor="#E05A5A", clip_on=False, zorder=5))

    for bar, model, acc in zip(bars, models, accs):
        ax.text(bar.get_x() + bar.get_width() / 2, acc - 4.8, f"{acc:.1f}",
                ha="center", va="top", color="#19202A", fontsize=10.5, fontweight="bold")
        provider = MODEL_PROVIDERS.get(model, "")
        badge_color = PROVIDER_COLORS.get(provider, ACCENT)
        badge_text = PROVIDER_BADGES.get(provider, "?")
        center = bar.get_x() + bar.get_width() / 2
        ax.scatter(center, 4.1, s=470, color="#FFFFFF", edgecolor=badge_color,
                   linewidth=1.65, zorder=6)
        logo = _provider_logo(provider)
        if logo is not None:
            imagebox = OffsetImage(logo, zoom=0.052, interpolation="lanczos")
            ab = AnnotationBbox(imagebox, (center, 4.1), frameon=False,
                                box_alignment=(0.5, 0.5), zorder=7)
            ax.add_artist(ab)
        else:
            ax.text(center, 4.1, badge_text, ha="center", va="center",
                    color="#FFFFFF", fontsize=9.5, fontweight="bold", zorder=7)
        if answer_rates[model] < 100:
            ax.text(center, 10.3, f"{answer_rates[model]:.0f}% answered",
                    ha="center", va="bottom", color="#9A5B00", fontsize=8.3, fontweight="bold")

    def model_label(name: str) -> str:
        parts = name.split()
        if name.startswith("Claude "):
            return f"Claude\n{' '.join(parts[1:])}"
        if name.startswith("Gemini "):
            return "Gemini\n3.1 Pro"
        if name.startswith("Qwen"):
            return "Qwen\n3.7 Plus"
        if name.startswith("Llama"):
            return "Llama 4\nMaverick"
        if name.startswith("DeepSeek"):
            return "DeepSeek\nV3.2"
        return name.replace(" ", "\n", 1)

    ax.set_xticks(x)
    ax.set_xticklabels([model_label(m) for m in models], fontsize=9.5, color="#19202A")
    ax.set_ylim(-7, 104)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0", "25", "50", "75", "100"], color="#6B7280", fontsize=8.5)
    ax.grid(axis="y", color="#E6E0D8", linewidth=1, zorder=1)
    ax.tick_params(axis="x", length=0, pad=12)
    ax.tick_params(axis="y", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_ylabel("Accuracy (%)", color="#6B7280", fontsize=9)
    ax.set_title("Which LLMs can a dentist trust?", fontsize=17, pad=18,
                 loc="left", color="#19202A", fontweight="bold")
    ax.text(0, 1.015,
            "Deployment accuracy on 30 clinician-verified dental questions; refusals count as incorrect",
            transform=ax.transAxes, color="#6B7280", fontsize=10, ha="left", va="bottom")

    legend_items = []
    for provider in ["OpenAI", "Anthropic", "Google", "Qwen", "Meta", "DeepSeek"]:
        if provider in [MODEL_PROVIDERS.get(m) for m in models]:
            legend_items.append(plt.Line2D([0], [0], marker="o", color="none",
                                           markerfacecolor=PROVIDER_COLORS[provider],
                                           markeredgecolor="#FFFFFF", markeredgewidth=1.5,
                                           markersize=8, label=provider))
    leg = ax.legend(handles=legend_items, loc="upper right", bbox_to_anchor=(1.0, 1.12),
                    ncol=3, frameon=False, fontsize=8.5)
    for t in leg.get_texts():
        t.set_color("#3B4350")
    fig.tight_layout()
    p1 = out_dir / "accuracy_by_model.png"
    fig.savefig(p1, facecolor="#F7F4EF", bbox_inches="tight")
    plt.close(fig)
    written.append(p1)

    # 2) Model x domain accuracy heatmap.
    domains = sorted({r["domain"] for r in rows})
    grid = []
    for m in models:
        row_vals = []
        for d in domains:
            cell = [r["correct"] for r in rows if r["model"] == m and r["domain"] == d]
            row_vals.append(100 * sum(cell) / len(cell) if cell else float("nan"))
        grid.append(row_vals)

    fig, ax = plt.subplots(figsize=(10, 0.7 * len(models) + 2.5), dpi=160)
    _style(ax, fig)
    im = ax.imshow(grid, cmap="BuGn", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(domains)))
    ax.set_xticklabels([DOMAIN_LABELS.get(d, d).replace("\n", " ") for d in domains],
                       rotation=30, ha="right", fontsize=9)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models, fontsize=10)
    ax.set_title("Accuracy by model and clinical domain", fontsize=13, pad=12, loc="left", color=TEXT)
    for i in range(len(models)):
        for j in range(len(domains)):
            v = grid[i][j]
            if v == v:  # not NaN
                ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                        color=TEXT if v > 55 else INK, fontsize=9)
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.ax.tick_params(colors=TEXT)
    fig.tight_layout()
    p2 = out_dir / "accuracy_by_domain.png"
    fig.savefig(p2, facecolor=INK, bbox_inches="tight")
    plt.close(fig)
    written.append(p2)
    return written


if __name__ == "__main__":
    path = dataset_composition()
    print(f"Wrote {path}")
