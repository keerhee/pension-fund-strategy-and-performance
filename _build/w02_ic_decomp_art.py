# -*- coding: utf-8 -*-
"""W02 케이스 IC 10쪽 그림 — NBIM 액티브 수익 분해 (Ang-Goetzmann-Schaefer 2009).

수치는 보고서의 정성적 패턴을 옮긴 개념 도해다. 아래첨자는 mathtext로 조판한다.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

KR = "/Users/keerhee/Library/Fonts/NotoSansCJK.ttc"
fm.fontManager.addfont(KR)
KRNAME = fm.FontProperties(fname=KR).get_name()
plt.rcParams.update({"font.family": KRNAME, "axes.unicode_minus": False})

ORANGE, GREEN = "#E29B2E", "#4CB782"
INK, MUTED, HAIR = "#1b2c5e", "#5b6478", "#d7dbe4"
NOTE_BG, NOTE_ED, NOTE_TX = "#FDF6E3", "#E0B15C", "#7a5a1c"
OUT = "/private/tmp/claude-501/-Users-keerhee-Project/e6f6339b-a743-49d4-bfcd-d33ce14011c6/scratchpad/w02/ic_decomp.png"

fig = plt.figure(figsize=(15, 9), dpi=100, facecolor="white")
fig.text(.5, .962, "NBIM 액티브 수익 분해 — Ang-Goetzmann-Schaefer (2009)",
         ha="center", va="center", fontsize=23, fontweight="bold", color="#222")
fig.text(.5, .922, "“명목상 액티브”라고 보고된 수익의 약 70%는 시스템적 팩터 노출로 설명된다",
         ha="center", va="center", fontsize=14, color="#444")

for x0, w in ((.045, .435), (.520, .435)):
    fig.add_artist(Rectangle((x0, .045), w, .845, transform=fig.transFigure,
                             fill=False, edgecolor=HAIR, lw=1.2))

# ── A. 도넛 ─────────────────────────────────────────────────
fig.text(.2625, .855, "A. 액티브 수익 분산의 분해", ha="center", fontsize=17,
         fontweight="bold", color="#222")
ax = fig.add_axes([.09, .435, .345, .410])
ax.pie([70, 30], startangle=90, counterclock=False, radius=.86,
       colors=[ORANGE, GREEN], wedgeprops=dict(width=.35, edgecolor="white", lw=2))
ax.set(aspect="equal")
ax.text(0, .05, "액티브 수익", ha="center", va="center", fontsize=12.5, color=MUTED)
ax.text(0, -.11, "100%", ha="center", va="center", fontsize=13, color=MUTED,
        fontweight="bold")
# 바깥 라벨 — 링 위에 글자를 얹지 않는다
ax.text(.80, -.48, "70%", ha="left", va="center", fontsize=21,
        fontweight="bold", color=ORANGE)
ax.text(.80, -.68, "팩터 노출", ha="left", va="center", fontsize=13, color="#8a6416")
ax.text(-.80, .66, "30%", ha="right", va="center", fontsize=18,
        fontweight="bold", color=GREEN)
ax.text(-.80, .48, "α + 잔차", ha="right", va="center", fontsize=13, color="#2c7a52")

for i, (c, label) in enumerate(((ORANGE, "시스템적 팩터: Value, Size, Mom, Liquidity, Credit"),
                                (GREEN, "진정한 알파 (α) + 잔차 (ε)"))):
    y = .405 - i * .048
    fig.add_artist(Rectangle((.085, y - .012), .022, .026, transform=fig.transFigure,
                             facecolor=c, edgecolor="none"))
    fig.text(.118, y, label, fontsize=13, va="center", color="#222")

fig.add_artist(FancyBboxPatch((.085, .085), .355, .200, transform=fig.transFigure,
                              boxstyle="round,pad=0.006,rounding_size=0.012",
                              facecolor=NOTE_BG, edgecolor=NOTE_ED, lw=1.2))
fig.text(.2625, .252, "핵심 발견", ha="center", fontsize=15, fontweight="bold", color=NOTE_TX)
for i, line in enumerate(("• NBIM이 “알파”로 보고한 수익의 대부분은",
                          "  잘 알려진 팩터 프리미엄의 회수였다.",
                          "• 권고 — 팩터를 자산배분 차원으로 격상하라",
                          "  (factor investing 패러다임의 출발점).")):
    fig.text(.103, .208 - i * .034, line, fontsize=12.5, color=NOTE_TX, va="center")

# ── B. 막대 ─────────────────────────────────────────────────
fig.text(.7375, .855, "B. 팩터별 기여도 (개념 도해)", ha="center", fontsize=17,
         fontweight="bold", color="#222")
fig.text(.7375, .818, "실제 수치는 표본·모형에 따라 변동 — 보고서의 정성적 패턴",
         ha="center", fontsize=12.5, color="#555")
ax = fig.add_axes([.575, .215, .355, .565])
names = ["Value", "Size", "Liquidity", "Credit", "Mom", "α"]
vals = [.88, .62, .78, .85, .45, .07]
ax.bar(range(5), vals[:5], width=.62, color=ORANGE, edgecolor="white")
ax.bar([5.35], [vals[5]], width=.62, color=GREEN, edgecolor="white")
ax.axvline(4.7, ls=(0, (3, 3)), color="#9aa2b1", lw=1.1)
ax.set_xticks(list(range(5)) + [5.35])
ax.set_xticklabels(names, fontsize=13.5, fontweight="bold", color="#222")
ax.set_yticks([]); ax.set_ylim(0, 1.12); ax.set_xlim(-.75, 6.05)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#333"); ax.spines["bottom"].set_color("#333")
ax.tick_params(axis="x", length=0, pad=7)
fig.text(.578, .788, "기여도 (상대)", fontsize=11.5, color="#333", ha="left", va="bottom")
ax.text(2.0, 1.03, r"시스템적 팩터 ($\beta_k \cdot f_k$)", ha="center", fontsize=14.5,
        fontweight="bold", color="#8a6416")
ax.text(5.35, 1.03, r"진정 $\alpha$", ha="center", fontsize=14.5,
        fontweight="bold", color="#2c7a52")
ax.text(5.35, vals[5] + .05, r"$\approx 0$", ha="center", fontsize=13, color="#2c7a52")

fig.text(.7375, .152, r"$r_{\mathrm{active}} \;=\; \alpha \;+\; \sum_k \beta_k f_k \;+\; \varepsilon$",
         ha="center", va="center", fontsize=21, color="#222")
fig.text(.7375, .081, r"α는 통계적으로 0과 구별되지 않음  ·  $\beta_k$는 대부분 양의 부호로 유의",
         ha="center", va="center", fontsize=12.5, color="#444")

fig.savefig(OUT, dpi=100, facecolor="white")
print("saved", OUT)
