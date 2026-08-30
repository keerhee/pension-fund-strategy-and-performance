# -*- coding: utf-8 -*-
"""W09 프라이머의 그림 — M10 위험관리와 성과평가."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w09")
EX = "수업용으로 지어낸 예시입니다"


# ── 같은 수익, 다른 변동성 ───────────────────────────────────────
def two_funds():
    rng = np.random.default_rng(3)
    n = 120
    a = rng.normal(.007, .012, n)
    b = rng.normal(.007, .045, n)
    A, B = 100 * np.cumprod(1 + a), 100 * np.cumprod(1 + b)
    B *= A[-1] / B[-1]                       # 끝값을 같게 맞춘다
    t = np.arange(n) / 12
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1.35, 1]})
    ax = axes[0]
    ax.plot(t, A, color=TEAL, lw=3.6, label="가 펀드")
    ax.plot(t, B, color=AMBER, lw=2.6, label="나 펀드")
    ax.scatter([t[-1]], [A[-1]], s=150, color=INK, zorder=5)
    ax.annotate("끝값이 똑같다", (t[-1], A[-1]), xytext=(-12, 16),
                textcoords="offset points", ha="right", fontsize=17,
                color=INK, fontweight="bold")
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("100으로 시작한 값", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    clean(ax)

    ax = axes[1]
    sr = [(a.mean() * 12 - .02) / (a.std() * np.sqrt(12)),
          (b.mean() * 12 - .02) / (b.std() * np.sqrt(12))]
    ax.bar([0, 1], sr, color=[LIME, AMBER], width=.55,
           edgecolor=[INK, "none"], linewidth=1.4)
    for i, v in enumerate(sr):
        ax.text(i, v + .05, f"{v:.2f}", ha="center", fontsize=22,
                color=INK, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["가 펀드", "나 펀드"], fontsize=17)
    ax.set_ylabel("변동성 한 단위당 번 몫", fontsize=15)
    ax.set_title("같은 결과라도 값은 다르다", fontsize=18, color=INK, pad=12)
    clean(ax)
    fig.tight_layout()
    return save(fig, "two_funds.png", EX)


# ── 왼쪽 꼬리 ────────────────────────────────────────────────────
def var_tail():
    rng = np.random.default_rng(8)
    r = rng.standard_t(4, 40000) * 1.1
    q5 = np.percentile(r, 5)
    tail = r[r <= q5]
    fig, ax = plt.subplots(figsize=WIDE)
    bins = np.linspace(-9, 9, 160)
    ax.hist(r, bins=bins, color=TEAL, alpha=.85)
    ax.hist(tail, bins=bins, color=RED)
    ax.axvline(q5, color=INK, lw=2.4, ls="--")
    top = ax.get_ylim()[1]
    ax.annotate(f"백 번 중 다섯 번은\n{q5:.1f}%보다 나쁘다", (q5, top * .55),
                xytext=(-18, 0), textcoords="offset points", ha="right",
                fontsize=17, color=RED, fontweight="bold")
    ax.text(2.4, top * .78, "여기까지가 흔한 일", fontsize=17, color=TEAL, fontweight="bold")
    ax.annotate("이 빨간 부분의 평균이\n“나쁠 때 얼마나 나쁜가”",
                (q5 - 2.4, top * .16), xytext=(0, 0), textcoords="offset points",
                ha="center", fontsize=15.5, color=INK)
    ax.set_xlabel("한 달 수익률(%)", fontsize=15)
    ax.set_ylabel("그런 달이 나온 횟수", fontsize=15)
    ax.set_xlim(-9, 9)
    clean(ax)
    fig.tight_layout()
    return save(fig, "var_tail.png", EX)


# ── 무엇과 견줄 것인가 (SVG) ─────────────────────────────────────
def benchmark():
    b = text(800, 52, "잘한 건지는 “무엇과 견주느냐”가 정한다", 30, INK, bold=True)
    b += box(90, 130, 420, 150, "우리 성적", ["한 해 +8%"], stroke=HAIR)
    b += text(300, 330, "이것만 보면 알 수 없다", 26, MUTED)
    b += arrow(540, 205, 640, 205, MUTED, "aM", 5)
    b += box(670, 110, 400, 130, "시장이 +12%였다면", ["4%p 뒤졌다"],
             stroke=RED, tc=RED, sc=RED)
    b += box(670, 280, 400, 130, "시장이 +3%였다면", ["5%p 앞섰다"],
             stroke=TEAL, tc=TEAL, sc=TEAL)
    b += limebox(1130, 190, 380, 150, "그래서 먼저 정한다",
                 ["“무엇과 견줄 것인가”"])
    b += text(800, 500, "견줄 잣대를 나중에 고르면, 언제나 이겨 보이게 만들 수 있다",
              27, RED, bold=True)
    b += text(800, 552, "그래서 잣대는 돈을 넣기 전에 정해 문서로 남긴다", 26, MUTED)
    return svg("benchmark.png", b)


# ── 어디서 갈렸나 ────────────────────────────────────────────────
def attribution():
    parts = ["큰 덩어리를\n어떻게 나눴나", "그 안에서\n무엇을 골랐나", "둘이 겹쳐서\n생긴 몫"]
    vals = [1.4, -0.6, 0.2]
    cols = [TEAL, RED, MUTED]
    fig, ax = plt.subplots(figsize=WIDE)
    bottom = 0
    for i, (v, c) in enumerate(zip(vals, cols)):
        ax.bar([i], [v], bottom=[0], width=.55, color=c)
        ax.text(i, v + (.08 if v > 0 else -.08), f"{v:+.1f}%p", ha="center",
                va="bottom" if v > 0 else "top", fontsize=19, color=INK, fontweight="bold")
    tot = sum(vals)
    ax.bar([3], [tot], width=.55, color=LIME, edgecolor=INK, linewidth=1.4)
    ax.text(3, tot + .08, f"{tot:+.1f}%p", ha="center", fontsize=22,
            color=INK, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_xticks(range(4))
    ax.set_xticklabels(parts + ["잣대보다\n앞선 몫"], fontsize=15.5)
    ax.set_ylabel("잣대 대비 더 번 몫(%p)", fontsize=15)
    ax.set_ylim(-1.2, 2.1)
    ax.text(1.5, 1.85, "잘한 곳과 못한 곳을 갈라 놓아야 다음에 고칠 수 있다",
            ha="center", fontsize=17, color=INK)
    clean(ax)
    fig.tight_layout()
    return save(fig, "attribution.png", EX)


# ── 운인가 실력인가 ──────────────────────────────────────────────
def luck():
    yrs = np.arange(1, 21)
    need = 4.0 / np.sqrt(yrs)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(yrs, need, color=TEAL, lw=4)
    ax.fill_between(yrs, 0, need, color=RED, alpha=.10)
    ax.text(9, 2.6, "이 아래는 운으로도 나올 수 있는 범위", fontsize=17,
            color=RED, fontweight="bold")
    for y, c in [(1, RED), (5, AMBER), (16, LIME)]:
        v = 4.0 / np.sqrt(y)
        ax.scatter([y], [v], s=180, color=c, zorder=5,
                   edgecolors=INK if c == LIME else "none", linewidth=1.4)
        ax.annotate(f"{y}년치로 판단하려면\n해마다 {v:.1f}%p는 앞서야", (y, v),
                    xytext=(16, 10), textcoords="offset points",
                    fontsize=15.5, color=INK if c == LIME else c, fontweight="bold")
    ax.set_xlabel("성적을 지켜본 햇수", fontsize=15)
    ax.set_ylabel("실력이라 부르려면 필요한 앞선 폭(%p)", fontsize=15)
    ax.set_xlim(0, 21); ax.set_ylim(0, 4.6)
    clean(ax)
    fig.tight_layout()
    return save(fig, "luck.png", "짧은 기록으로는 실력을 가려내기 어렵다는 것을 보이려는 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$SR\;=\;\frac{r_p\;-\;r_f}{\sigma_p}$", fontsize=48, width=6.0)


if __name__ == "__main__":
    two_funds(); var_tail(); benchmark(); attribution(); luck(); equation()
    print("끝.")
