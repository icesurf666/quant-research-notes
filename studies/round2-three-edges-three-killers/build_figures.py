"""Render summary figures from the frozen narrative source report, not raw trades."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
BG, INK, MUTED = "#f7f4ed", "#182126", "#647076"


def canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    fig.text(.07, .91, title, fontsize=29, weight="bold", color=INK)
    fig.text(.07, .85, subtitle, fontsize=15, color=MUTED)
    fig.text(.07, .045, "HFM · development backtests · source: frozen capstone report, 2026-09-11",
             fontsize=11, color=MUTED)
    fig.subplots_adjust(left=.10, right=.94, bottom=.19, top=.76)
    return fig, ax


fig, ax = canvas("Three Crypto Edges. Three Different Killers.",
                 "Reported outcomes under the tested assumptions — not live trading")
ax.axis("off")
rows = [
    ["Mean reversion", "Modelled execution costs", "REJECT"],
    ["Funding carry", "Failed held-out year", "REJECT OOS"],
    ["Daily momentum", "Parameter sensitivity", "WEAK"],
]
table = ax.table(cellText=rows, colLabels=["Hypothesis", "Decisive failure", "Verdict"],
                 colWidths=[.30, .44, .26], cellLoc="left", loc="center")
table.auto_set_font_size(False)
table.set_fontsize(19)
table.scale(1, 4)
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor(BG)
    cell.set_facecolor("#e6e0d5" if row == 0 else "#fffdf8")
    cell.set_text_props(color=INK, weight="bold" if row == 0 or col == 2 else "normal")
fig.savefig(ROOT / "figures/research_summary.png", facecolor=BG)
plt.close(fig)

fig, ax = canvas("Momentum: a peak, not a parameter plateau",
                 "Reported net returns at four lookbacks · same development sweep")
values = [33, -23, 97, 35]
bars = ax.bar(range(4), values, color=["#2667a8", "#d65a31", "#2667a8", "#2667a8"], width=.58)
ax.axhline(0, color=INK, linewidth=1)
ax.set_xticks(range(4), ["7 days", "10 days", "14 days", "21 days"], fontsize=14)
ax.set_ylabel("Net return (%)", fontsize=14)
ax.set_ylim(-40, 120)
ax.spines[["top", "right"]].set_visible(False)
for bar, value in zip(bars, values):
    ax.text(bar.get_x()+bar.get_width()/2, value + (4 if value >= 0 else -8),
            f"{value:+d}%", ha="center", fontsize=20, weight="bold", color=INK)
fig.savefig(ROOT / "figures/momentum_sweep.png", facecolor=BG)
plt.close(fig)
