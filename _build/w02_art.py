# -*- coding: utf-8 -*-
"""W02 프라이머의 그림 — M2 자산배분과 CAPM.

숫자는 모두 수업용 예시이며 각 그림에 그렇게 적어 둔다.
"""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w02")
EX = "수업용으로 지어낸 예시입니다"


# ── 무엇이 수익을 정하나 — BHB ───────────────────────────────────
def bhb():
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axes[0]
    vals = [91.5, 4.6, 1.8, 2.1]
    labs = ["큰 덩어리를\n나눈 비율", "언제 사고 팔지", "무엇을 고를지", "그 밖"]
    cols = [LIME, BLUE, AMBER, HAIR]
    ax.pie(vals, colors=cols, startangle=90, counterclock=False,
           wedgeprops=dict(width=.46, edgecolor=PAPER, linewidth=3))
    ax.text(0, .06, "91.5%", ha="center", va="center", fontsize=34,
            color=INK, fontweight="bold")
    ax.text(0, -.24, "큰 덩어리 나누기", ha="center", va="center", fontsize=15, color=MUTED)
    ax.set_title("수익이 오르내린 이유를 뜯어보면", fontsize=17, color=INK, pad=14)

    ax = axes[1]
    ypos = np.arange(4)[::-1]
    ax.barh(ypos, vals, color=cols, height=.62,
            edgecolor=[INK if c == LIME else "none" for c in cols], linewidth=1.2)
    for y, v, l in zip(ypos, vals, labs):
        ax.text(v + 1.6, y, f"{v}%", va="center", fontsize=16, color=INK, fontweight="bold")
    ax.set_yticks(ypos)
    ax.set_yticklabels([l.replace("\n", " ") for l in labs], fontsize=16)
    ax.set_xlim(0, 108)
    ax.set_xlabel("수익의 오르내림을 설명하는 몫(%)", fontsize=15)
    clean(ax, grid="x")
    fig.tight_layout()
    return save(fig, "bhb.png", "Brinson·Hood·Beebower(1986)가 미국 연기금 91곳에서 얻은 값")


# ── 종목을 늘려도 남는 위험 ──────────────────────────────────────
def diversify():
    n = np.arange(1, 51)
    own, mkt = 26.0, 12.5
    tot = np.sqrt(mkt**2 + (own**2 - mkt**2) / n)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(n, tot, color=TEAL, lw=4, zorder=3)
    ax.axhline(mkt, color=RED, lw=2.4, ls="--")
    ax.fill_between(n, mkt, tot, color=BLUE, alpha=.16)
    ax.fill_between(n, 0, mkt, color=RED, alpha=.09)
    ax.text(26, 20.0, "종목을 늘리면 사라지는 위험", fontsize=17, color=BLUE)
    ax.text(26, 8.4, "아무리 늘려도 남는 위험", fontsize=17, color=RED, fontweight="bold")
    ax.annotate("한 종목만 가졌을 때", (1, own), xytext=(16, -6),
                textcoords="offset points", fontsize=16, color=INK)
    ax.scatter([1], [own], s=140, color=INK, zorder=5)
    ax.scatter([50], [tot[-1]], s=200, color=LIME, marker="*", zorder=5,
               edgecolors=INK, linewidth=1.2)
    ax.set_xlabel("담은 종목 수", fontsize=15)
    ax.set_ylabel("변동성(%)", fontsize=15)
    ax.set_ylim(0, 30); ax.set_xlim(0, 51)
    clean(ax)
    fig.tight_layout()
    return save(fig, "diversify.png", EX)


# ── 보상받는 위험은 하나뿐 ───────────────────────────────────────
def sml():
    beta = np.linspace(0, 2.0, 100)
    rf, mrp = 3.0, 5.0
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(beta, rf + beta * mrp, color=TEAL, lw=4, zorder=3)
    pts = [(0.0, rf, "국채 — 시장과 같이 안 움직인다", BLUE, (20, 12), "left"),
           (1.0, rf + mrp, "시장 전체 — 딱 시장만큼", INK, (-16, 10), "right"),
           (1.7, rf + 1.7 * mrp, "시장보다 더 출렁이는 것", RED, (-16, 8), "right")]
    for b, r, lab, c, off, ha in pts:
        ax.scatter([b], [r], s=150, color=c, zorder=5)
        ax.annotate(lab, (b, r), xytext=off, textcoords="offset points",
                    fontsize=16, color=c, ha=ha)
    ax.scatter([1.35], [7.4], s=190, color=AMBER, zorder=5)
    ax.annotate("선 아래 — 위험에 비해 덜 준다", (1.35, 7.4), xytext=(14, -30),
                textcoords="offset points", fontsize=15.5, color=AMBER)
    ax.set_xlabel("시장을 얼마나 따라 움직이나  β", fontsize=15)
    ax.set_ylabel("기대하는 수익(%)", fontsize=15)
    ax.set_xlim(-0.05, 2.05); ax.set_ylim(0, 14)
    clean(ax, grid="both")
    fig.tight_layout()
    return save(fig, "sml.png", EX)


# ── 베타를 눈으로 ────────────────────────────────────────────────
def beta_scatter():
    rng = np.random.default_rng(9)
    m = rng.normal(0, 3.4, 160)
    fig, axes = plt.subplots(1, 3, figsize=WIDE, sharex=True, sharey=True)
    for ax, (b, name, c) in zip(axes, [(0.35, "β = 0.35  전기·가스", BLUE),
                                       (1.00, "β = 1.00  시장 그 자체", TEAL),
                                       (1.75, "β = 1.75  반도체", RED)]):
        y = b * m + rng.normal(0, 2.2, 160)
        ax.scatter(m, y, s=20, color=c, alpha=.6, edgecolors="none")
        xs = np.linspace(-9, 9, 10)
        ax.plot(xs, b * xs, color=INK, lw=2.2)
        ax.set_title(name, fontsize=17, color=c, pad=11)
        ax.set_xlabel("시장이 오르내린 폭(%)", fontsize=14)
        ax.axhline(0, color=HAIR, lw=1); ax.axvline(0, color=HAIR, lw=1)
        ax.set_xlim(-11, 11); ax.set_ylim(-16, 16)
        ax.tick_params(labelsize=12)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("그 종목이 오르내린 폭(%)", fontsize=14)
    fig.suptitle("기울기가 곧 β — 시장이 1% 움직일 때 이 종목은 몇 % 움직이나",
                 fontsize=16, color=MUTED, y=1.02)
    fig.tight_layout()
    return save(fig, "beta_scatter.png", EX)


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$E[r_i]\;=\;r_f\;+\;\beta_i\,\left(E[r_m]-r_f\right)$",
                  fontsize=46, width=10.0)


# ── 큰 덩어리부터 정한다 (SVG) ───────────────────────────────────
def order():
    W, H = 1600, 620
    b = text(800, 56, "결정의 순서 — 위에서부터 아래로", 30, INK, bold=True)
    b += limebox(120, 110, 500, 150, "① 큰 덩어리를 나눈다",
                 ["주식 60 · 채권 40 처럼"])
    b += box(120, 300, 500, 130, "② 언제 사고 팔지", ["비중을 잠깐 바꾼다"])
    b += box(120, 460, 500, 130, "③ 무엇을 고를지", ["어떤 종목을 담을까"])
    b += arrow(370, 268, 370, 292, MUTED, "aM", 4)
    b += arrow(370, 438, 370, 452, MUTED, "aM", 4)
    b += vrule(700, 110, 590, HAIR, 2)
    b += text(760, 170, "수익 오르내림의 91.5%", 30, INK, "start", True)
    b += text(760, 212, "여기서 갈린다", 30, INK, "start", True)
    b += text(760, 352, "합쳐서 8.5%", 27, MUTED, "start")
    b += text(760, 392, "언론이 가장 많이 다루는 곳이지만", 25, MUTED, "start")
    b += text(760, 428, "결과를 가르는 힘은 훨씬 작다", 25, MUTED, "start")
    b += text(760, 520, "그래서 연기금은 ①에 가장 많은 시간을 쓴다", 27, TEAL, "start", True)
    return svg("order.png", b, W, H)


if __name__ == "__main__":
    bhb(); diversify(); sml(); beta_scatter(); equation(); order()
    print("끝.")
