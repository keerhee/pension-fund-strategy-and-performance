# -*- coding: utf-8 -*-
"""RB 현금흐름 타임라인 그림 — 45세에 2.63억으로 RB vs 같은 돈의 20년 일반 국채 (r = 2%, 실질)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_art", "rb_timeline.png")
FONT = os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc")
fm.fontManager.addfont(FONT)
plt.rcParams["font.family"] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False
NAVY, GREEN, RED, GRAY = "#1B2C5E", "#2E9E6B", "#C0392B", "#9AA3AF"

price = 2400 * (1 - 1.02 ** -20) / 0.02 / 1.02 ** 20 / 1e4      # 억 원 (2.64)
fig, axes = plt.subplots(2, 1, figsize=(11.6, 3.0), dpi=200, sharex=True)
# 막대 높이는 도식(금액은 글자로) — 실제 비율이면 연 526만 원 쿠폰이 보이지 않는다
P, PAY, CPN, PRIN = -1.6, 0.55, 0.3, 1.6
for ax, kind in zip(axes, ("RB", "BOND")):
    ax.axhline(0, color=NAVY, lw=1)
    ax.axvspan(64.5, 84.5, color="#E6F5F0", zorder=0)
    ax.bar(45, P, width=0.7, color=RED)
    ax.text(45.7, P * 0.55, f"45세에 {price:.2f}억으로 매수", ha="left", va="center", fontsize=13, color=RED)
    if kind == "RB":
        ax.axvspan(45.5, 64.5, color="#F3F4F8", zorder=0)
        ax.bar(range(65, 85), [PAY] * 20, width=0.7, color=GREEN)
        ax.text(55, 1.0, "이연기 20년 — 쿠폰 없음", ha="center", va="center", fontsize=14, color="#3b4252")
        ax.text(74.5, 1.0, "65세부터 20년 — 실질 연 2,400만 원", ha="center", va="center", fontsize=14, color=GREEN, fontweight="bold")
        ax.text(85.2, 0.3, "원금\n상환 없음", ha="left", va="center", fontsize=12, color="#3b4252")
        ax.set_ylabel("Retirement\nBond", fontsize=14, color=NAVY, rotation=0, ha="right", va="center", fontweight="bold")
        ax.set_ylim(-1.8, 1.3)
    else:
        ax.bar(range(46, 66), [CPN] * 20, width=0.7, color=NAVY)
        ax.bar(65, PRIN, width=0.7, color=NAVY, alpha=0.55)
        ax.text(55, 0.75, "쿠폰 연 526만 원 — 은퇴 전에 들어온다", ha="center", va="center", fontsize=14, color="#3b4252")
        ax.text(66, 1.35, f"만기 원금 {price:.2f}억 — 어디에 다시 넣나?", ha="left", va="center", fontsize=13, color=NAVY)
        ax.text(76, 0.6, "은퇴 후 소득은 없다", ha="center", va="center", fontsize=14, color=RED, fontweight="bold")
        ax.set_ylabel("같은 돈의\n20년 국채", fontsize=14, color=NAVY, rotation=0, ha="right", va="center", fontweight="bold")
        ax.set_ylim(-1.8, 1.8)
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
axes[1].set_xticks([45, 50, 55, 60, 65, 70, 75, 80, 85])
axes[1].set_xticklabels([f"{a}세" for a in [45, 50, 55, 60, 65, 70, 75, 80, 85]], fontsize=13)
axes[1].set_xlim(44, 88)
plt.tight_layout(h_pad=0.3)
fig.savefig(OUT, facecolor="white")
print(OUT, round(price, 2))
