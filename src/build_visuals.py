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

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dental_qa.json"
ASSETS = ROOT / "assets"

# Periospot-leaning dark palette.
INK = "#0E1116"
PANEL = "#161B22"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
ACCENT = "#3FB6B2"   # teal
DIFF_COLORS = {"basic": "#3FB6B2", "intermediate": "#E0A458", "advanced": "#E05A5A"}
TIER_COLORS = {"flagship": "#3FB6B2", "efficient": "#E0A458", "open": "#9A7DDE"}

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

    # 1) Accuracy by model.
    by_model: dict[str, list] = defaultdict(list)
    tier_of = {}
    for r in rows:
        by_model[r["model"]].append(r["correct"])
        tier_of[r["model"]] = r.get("tier", "open")
    models = sorted(by_model, key=lambda m: sum(by_model[m]) / len(by_model[m]), reverse=True)
    accs = [100 * sum(by_model[m]) / len(by_model[m]) for m in models]

    fig, ax = plt.subplots(figsize=(9, 5), dpi=160)
    _style(ax, fig)
    bars = ax.barh(list(reversed(models)), list(reversed(accs)),
                   color=[TIER_COLORS.get(tier_of[m], ACCENT) for m in reversed(models)],
                   height=0.6, edgecolor=INK, linewidth=1.5)
    ax.set_xlabel("Accuracy (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Dental knowledge accuracy by model", fontsize=13, pad=12, loc="left", color=TEXT)
    for bar, acc in zip(bars, reversed(accs)):
        ax.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height() / 2,
                f"{acc:.0f}%", va="center", color=TEXT, fontsize=10)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in TIER_COLORS.values()]
    leg = ax.legend(handles, list(TIER_COLORS.keys()), loc="lower right", frameon=False, fontsize=9)
    for t in leg.get_texts():
        t.set_color(TEXT)
    fig.tight_layout()
    p1 = out_dir / "accuracy_by_model.png"
    fig.savefig(p1, facecolor=INK, bbox_inches="tight")
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
