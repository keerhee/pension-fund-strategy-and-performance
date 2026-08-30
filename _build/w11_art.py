# -*- coding: utf-8 -*-
"""W11 프라이머의 그림 — M12 채권 투자."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w11")
EX = "수업용으로 지어낸 예시입니다"


def price(y, c=0.03, T=10, f=1):
    """액면 100, 표면금리 c, 만기 T년 채권의 값."""
    t = np.arange(1, T + 1)
    return (c * 100 / (1 + y) ** t).sum() + 100 / (1 + y) ** T


# ── 왜 금리가 오르면 손해인가 (SVG) ──────────────────────────────
def why():
    b = text(800, 50, "왜 금리가 오르면 이미 산 채권이 손해인가", 30, INK, bold=True)
    b += box(80, 120, 420, 200, "작년에 산 채권", ["해마다 3만원을 준다", "10년 뒤 100만원"], stroke=HAIR)
    b += text(290, 372, "약속은 그대로다", 26, MUTED)
    b += box(560, 120, 420, 200, "오늘 새로 나온 채권", ["해마다 5만원을 준다", "10년 뒤 100만원"],
             stroke=TEAL, tc=TEAL, sc=INK)
    b += text(770, 372, "금리가 올랐으니 더 준다", 26, TEAL)
    b += arrow(500, 220, 548, 220, MUTED, "aM", 5)
    b += limebox(1040, 120, 470, 200, "그럼 내 것은 얼마?",
                 ["3만원짜리를 5만원짜리와", "견주면 값이 내려간다"])
    b += hrule(80, 1520, 430, HAIR, 2)
    b += text(800, 492, "채권은 망해서 값이 내리는 게 아니다", 28, INK, bold=True)
    b += text(800, 546, "더 좋은 조건의 새 채권이 나와서 내린다", 28, RED, bold=True)
    return svg("why.png", b)


# ── 금리와 값 ────────────────────────────────────────────────────
def price_yield():
    ys = np.linspace(.005, .09, 200)
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1.2, 1]})
    ax = axes[0]
    for T, c, lab in [(3, BLUE, "3년 뒤 끝나는 채권"), (10, TEAL, "10년"), (30, RED, "30년")]:
        ax.plot(ys * 100, [price(y, T=T) for y in ys], color=c, lw=3.6, label=lab)
    ax.axvline(3, color=MUTED, lw=1.4, ls=":")
    ax.text(3.3, 132, "표면금리와 같을 때\n값은 100", fontsize=15, color=MUTED)
    ax.set_xlabel("시장 금리(%)", fontsize=15)
    ax.set_ylabel("채권 값", fontsize=15)
    ax.legend(fontsize=15.5, frameon=False, loc="upper right")
    ax.set_title("금리가 오르면 값은 내린다", fontsize=18, color=INK, pad=12)
    clean(ax, grid="both")

    ax = axes[1]
    Ts = [3, 10, 30]
    chg = [(price(.04, T=T) / price(.03, T=T) - 1) * 100 for T in Ts]
    ax.bar(range(3), chg, color=[BLUE, TEAL, RED], width=.56)
    for i, v in enumerate(chg):
        ax.text(i, v - .5, f"{v:.1f}%", ha="center", va="top", fontsize=19,
                color=INK, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"{T}년" for T in Ts], fontsize=17)
    ax.set_ylabel("금리 1%p 오를 때 값 변화(%)", fontsize=15)
    ax.set_ylim(-22, 3)
    ax.set_title("멀리 있는 돈일수록 더 아프다", fontsize=18, color=RED, pad=12)
    clean(ax)
    fig.tight_layout()
    return save(fig, "price_yield.png", "표면금리 3%, 해마다 이자를 주는 채권으로 계산했습니다")


# ── 곡선의 세 얼굴 ───────────────────────────────────────────────
def curves():
    m = np.array([0.25, 1, 2, 3, 5, 7, 10, 20, 30])
    up = 2.0 + 1.8 * (1 - np.exp(-m / 6))
    flat = 3.4 + 0.05 * m / 30
    inv = 4.6 - 1.6 * (1 - np.exp(-m / 5))
    fig, axes = plt.subplots(1, 3, figsize=WIDE, sharey=True)
    specs = [(up, "우상향 — 보통 때", TEAL, "길게 빌려주면 더 받는다"),
             (flat, "평탄 — 갈림길", AMBER, "길게 빌려줘도 더 안 준다"),
             (inv, "역전 — 드문 일", RED, "짧은 쪽이 더 높다")]
    for ax, (y, t0, c, sub) in zip(axes, specs):
        ax.plot(m, y, color=c, lw=4, marker="o", ms=7)
        ax.set_title(t0, fontsize=18, color=c, pad=11)
        ax.set_xlabel(sub, fontsize=15, color=INK)
        ax.set_xscale("log")
        ax.set_xticks([1, 5, 10, 30])
        ax.set_xticklabels(["1년", "5년", "10년", "30년"], fontsize=13)
        ax.set_ylim(1.5, 5.2)
        clean(ax)
    axes[0].set_ylabel("금리(%)", fontsize=15)
    fig.suptitle("가로축은 돈을 빌려주는 기간, 세로축은 그때 받는 금리",
                 fontsize=16, color=MUTED, y=1.02)
    fig.tight_layout()
    return save(fig, "curves.png", EX)


# ── 2022년 ───────────────────────────────────────────────────────
def y2022():
    names = ["짧은 국채", "중간 국채", "긴 국채", "주식"]
    vals = [-3.9, -12.5, -29.3, -18.1]
    cols = [BLUE, TEAL, RED, MUTED]
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(range(4), vals, color=cols, width=.56)
    for i, v in enumerate(vals):
        ax.text(i, v - 1.0, f"{v:.1f}%", ha="center", va="top", fontsize=19,
                color=INK, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=17)
    ax.set_ylabel("그해 수익률(%)", fontsize=15)
    ax.set_ylim(-34, 5)
    ax.text(1.5, 3.4, "“안전 자산”이라던 긴 국채가 주식보다 크게 내린 해",
            ha="center", va="top", fontsize=18, color=RED, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "y2022.png", "2022년의 흐름을 본떠 만든 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$\frac{\Delta P}{P}\;\approx\;-\,D\,\Delta y\;+\;\frac{1}{2}\,C\,(\Delta y)^{2}$",
                  fontsize=42, width=10.0)


if __name__ == "__main__":
    why(); price_yield(); curves(); y2022(); equation()
    print("끝.")
