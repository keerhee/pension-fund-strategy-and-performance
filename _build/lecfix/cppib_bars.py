# -*- coding: utf-8 -*-
"""CPPIB식 막대그래프 — 기준 85/15 → 실제 포트폴리오(자산군) → 위험 환산(주식·채권). 기금 100, 사모 10 · 부동산 10."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_art", "cppib_bars.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
FONT = os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc")
fm.fontManager.addfont(FONT)
plt.rcParams["font.family"] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False
NAVY, GRAY, ORANGE, GREEN = "#1B2C5E", "#9AA3AF", "#E8A04C", "#2E9E6B"

fig, ax = plt.subplots(figsize=(5.6, 2.95), dpi=200)
W = 0.52


def seg(x, bottom, h, color, label, hatch=None, tc="white"):
    ax.bar(x, h, W, bottom=bottom, color=color, edgecolor="white", linewidth=1.2, hatch=hatch)
    if label and abs(h) >= 7:
        ax.text(x, bottom + h / 2, label, ha="center", va="center", fontsize=11, color=tc, fontweight="bold")


# ① 기준
seg(0, 0, 85, NAVY, "주식 85")
seg(0, 85, 15, GRAY, "채권 15")
# ② 실제(자산군)
seg(1, 0, 67, NAVY, "상장주식 67")
seg(1, 67, 13, GRAY, "채권 13")
seg(1, 80, 10, ORANGE, "사모 10")
seg(1, 90, 10, GREEN, "부동산 10")
# ③ 위험 환산
seg(2, 0, 67, NAVY, "상장 67")
seg(2, 67, 13, ORANGE, "사모 13")
seg(2, 80, 5, GREEN, "부동산 5")
seg(2, 85, 13, GRAY, "채권 13")
seg(2, 98, 5, GREEN, "부동산 5")
seg(2, 0, -3, ORANGE, "", hatch="///")
ax.text(1.72, -4.5, "사모 속 빚 −3 →", ha="right", va="center", fontsize=10, color="#B45309")
ax.text(1.5, 106, "초록 = 부동산 10을 주식 5 · 채권 5로 나눈 것", ha="center", va="center", fontsize=10, color=GREEN)
# 괄호 — 주식 85 / 채권 15
for y0, y1, lab in ((0, 85, "주식 환산 85"), (85, 103, "채권 환산 15\n(13 + 5 − 3)")):
    ax.plot([2.31, 2.36, 2.36, 2.31], [y0 + 0.8, y0 + 0.8, y1 - 0.8, y1 - 0.8], color=NAVY, lw=1)
    ax.text(2.4, (y0 + y1) / 2, lab, ha="left", va="center", fontsize=11, color=NAVY, fontweight="bold")
for x0 in (0.3, 1.3):
    ax.annotate("", xy=(x0 + 0.4, 52), xytext=(x0, 52), arrowprops=dict(arrowstyle="->", color="#6B7280", lw=1.4))
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["① 기준 포트폴리오\n(이사회)", "② 실제 포트폴리오\n(자산군)", "③ 위험 환산\n(주식 · 채권)"], fontsize=11)
ax.axhline(0, color="#3b4252", lw=0.8)
ax.set_ylim(-9, 110); ax.set_xlim(-0.45, 3.05)
ax.set_yticks([])
for sp in ("top", "right", "left", "bottom"):
    ax.spines[sp].set_visible(False)
plt.tight_layout()
fig.savefig(OUT, facecolor="white")
print(OUT)
