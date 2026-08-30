# -*- coding: utf-8 -*-
"""W03 프라이머의 그림 — M3 연기금 3대 모델과 CMA."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w03")
EX = "수업용으로 지어낸 예시입니다"


# ── 세 가지 길 (SVG) ─────────────────────────────────────────────
def models():
    b = text(800, 52, "같은 질문에 세 기관이 다른 답을 냈다", 30, INK, bold=True)
    b += text(800, 92, "“우리 돈을 누가, 어떻게 굴릴 것인가”", 26, MUTED)
    xs = [90, 570, 1050]
    specs = [("노르웨이 GPFG", ["거의 다 지수를 산다", "값싸고 투명하게", "사람은 적게"], BLUE),
             ("캐나다 CPPIB", ["직접 사서 직접 굴린다", "사람을 많이 뽑는다", "비싸지만 통제된다"], TEAL),
             ("예일 기금", ["남에게 맡긴다", "잘 고르는 데 집중", "비유동 자산을 많이"], AMBER)]
    for x, (name, lines, c) in zip(xs, specs):
        b += (f'<rect x="{x}" y="140" width="460" height="300" rx="12" fill="{WHITE}" '
              f'stroke="{c}" stroke-width="3"/>')
        b += text(x + 230, 196, name, 34, c, bold=True)
        b += hrule(x + 60, x + 400, 218, HAIR, 2)
        for i, ln in enumerate(lines):
            b += text(x + 230, 268 + i * 44, ln, 26, INK)
    b += limebox(400, 480, 800, 110, "셋 다 성공했다", ["길이 하나가 아니라는 뜻이다"])
    return svg("models.png", b)


# ── 기대수익을 쌓아 만든다 ───────────────────────────────────────
def blocks():
    parts = [("배당으로 받는 몫", 2.2, BLUE),
             ("기업이 더 벌어서 오르는 몫", 4.1, TEAL),
             ("사람들이 더 쳐줘서 오르는 몫", -0.6, AMBER)]
    fig, ax = plt.subplots(figsize=WIDE)
    bottom = 0.0
    for name, v, c in parts:
        ax.bar([0], [v], bottom=[bottom], width=.5, color=c,
               label=f"{name}  {v:+.1f}%")
        ax.text(0, bottom + v / 2, f"{v:+.1f}%", ha="center", va="center",
                fontsize=17, color=WHITE if c != AMBER else INK, fontweight="bold")
        bottom += v
    ax.bar([1], [bottom], width=.5, color=LIME, edgecolor=INK, linewidth=1.4)
    ax.text(1, bottom / 2, f"{bottom:.1f}%", ha="center", va="center",
            fontsize=26, color=INK, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["조각을 쌓으면", "10년 기대수익"], fontsize=17)
    ax.set_ylabel("연 수익률(%)", fontsize=15)
    ax.set_xlim(-.6, 1.7); ax.set_ylim(-1.2, 7.5)
    ax.axhline(0, color=INK, lw=1.2)
    ax.legend(fontsize=15, frameon=False, loc="upper right")
    clean(ax)
    fig.tight_layout()
    return save(fig, "blocks.png", EX)


# ── 기관마다 가정이 다르다 ───────────────────────────────────────
def cma_spread():
    names = ["가 기관", "나 기관", "다 기관", "라 기관", "마 기관", "바 기관"]
    eq = np.array([5.2, 6.4, 4.8, 7.1, 5.9, 6.8])
    bd = np.array([2.4, 2.0, 2.9, 1.8, 2.6, 2.2])
    x = np.arange(6)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(x - .19, eq, .38, color=TEAL, label="주식에 기대하는 수익")
    ax.bar(x + .19, bd, .38, color=BLUE, label="채권에 기대하는 수익")
    for i in x:
        ax.text(i - .19, eq[i] + .16, f"{eq[i]:.1f}", ha="center", fontsize=14, color=INK)
        ax.text(i + .19, bd[i] + .16, f"{bd[i]:.1f}", ha="center", fontsize=14, color=INK)
    ax.annotate("", xy=(3, 7.1), xytext=(2, 4.8),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.2))
    ax.text(2.5, 8.0, "같은 자산인데 2.3%p 차이", ha="center", fontsize=17,
            color=RED, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=16)
    ax.set_ylabel("앞으로 10년 연 수익률 가정(%)", fontsize=15)
    ax.set_ylim(0, 9.2)
    ax.legend(fontsize=15, frameon=False, loc="upper left")
    clean(ax)
    fig.tight_layout()
    return save(fig, "cma_spread.png", EX)


# ── 가정 하나가 결과를 크게 흔든다 ───────────────────────────────
def sensitivity():
    yrs = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=WIDE)
    for r, c, lab in [(0.048, BLUE, "4.8%로 가정하면"),
                      (0.059, TEAL, "5.9%로 가정하면"),
                      (0.071, RED, "7.1%로 가정하면")]:
        v = 100 * (1 + r) ** yrs
        ax.plot(yrs, v, color=c, lw=3.4, label=f"{lab}  →  30년 뒤 {v[-1]:.0f}")
    ax.set_xlabel("지금부터 몇 해 뒤인가", fontsize=15)
    ax.set_ylabel("100으로 시작한 기금(배수 아님, 지수)", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    ax.set_xlim(0, 30)
    clean(ax)
    fig.tight_layout()
    return save(fig, "sensitivity.png", "가정만 바꾸고 나머지는 같게 둔 계산입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$E[r]\;\approx\;\frac{D}{P}\;+\;g\;+\;\Delta\!\left(\frac{P}{E}\right)$",
                  fontsize=44, width=9.0)


if __name__ == "__main__":
    models(); blocks(); cma_spread(); sensitivity(); equation()
    print("끝.")
