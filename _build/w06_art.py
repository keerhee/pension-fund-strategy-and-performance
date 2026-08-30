# -*- coding: utf-8 -*-
"""W06 프라이머의 그림 — M7 동적 자산배분 · SS2 재균형 프리미엄."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w06")
EX = "수업용으로 지어낸 예시입니다"


# ── 사람도 자산이다 (SVG) ────────────────────────────────────────
def human_capital():
    b = text(800, 52, "젊을 때는 “앞으로 벌 월급”이 가장 큰 재산이다", 30, INK, bold=True)
    xs, ages = [110, 620, 1130], ["25세", "45세", "65세"]
    hc = [(0.86, "앞으로 벌 월급"), (0.48, "앞으로 벌 월급"), (0.06, "앞으로 벌 월급")]
    for x, age, (h, lab) in zip(xs, ages, hc):
        b += text(x + 180, 128, age, 32, INK, bold=True)
        H = 300
        b += f'<rect x="{x}" y="160" width="360" height="{H}" rx="10" fill="{WHITE}" stroke="{HAIR}" stroke-width="2"/>'
        hh = int(H * h)
        b += f'<rect x="{x}" y="{160+H-hh}" width="360" height="{hh}" rx="10" fill="{TEAL}"/>'
        b += text(x + 180, 160 + H - hh // 2 + 10, f"{int(h*100)}%", 32, WHITE, bold=True)
        b += text(x + 180, 160 + (H - hh) // 2 + 10, "모아 둔 돈", 24, MUTED)
        b += text(x + 180, 500, lab, 24, TEAL)
    b += text(800, 570, "월급은 채권을 닮았다 — 그래서 젊을수록 주식을 더 담아도 된다",
              27, RED, bold=True)
    return svg("human_capital.png", b)


# ── 글라이드패스 ─────────────────────────────────────────────────
def glide():
    age = np.arange(25, 71)
    eq = np.clip(110 - age, 20, 90)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.fill_between(age, 0, eq, color=TEAL, alpha=.85, label="주식")
    ax.fill_between(age, eq, 100, color=BLUE, alpha=.75, label="채권")
    ax.text(31, 42, "젊을 때는 주식을 많이", fontsize=18, color=WHITE, fontweight="bold")
    ax.text(62, 16, "은퇴가 가까우면 줄인다", fontsize=18, color=WHITE,
            fontweight="bold", ha="center")
    ax.text(48, 88, "나머지는 채권", fontsize=18, color=WHITE, fontweight="bold")
    ax.set_xlabel("나이", fontsize=15)
    ax.set_ylabel("담는 비율(%)", fontsize=15)
    ax.set_xlim(25, 70); ax.set_ylim(0, 100)
    ax.legend(fontsize=16, frameon=False, loc="lower left")
    clean(ax, grid=None)
    fig.tight_layout()
    return save(fig, "glide.png", EX)


# ── 오르고 내리면 제자리가 아니다 ────────────────────────────────
def arith_geo():
    labels = ["출발", "+50%", "−50%"]
    vals = [100, 150, 75]
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    ax.bar(range(3), vals, color=[MUTED, TEAL, RED], width=.56)
    for i, v in enumerate(vals):
        ax.text(i, v + 4, f"{v}", ha="center", fontsize=19, color=INK, fontweight="bold")
    ax.axhline(100, color=INK, lw=1.4, ls="--")
    ax.set_xticks(range(3)); ax.set_xticklabels(labels, fontsize=17)
    ax.set_ylim(0, 175)
    ax.set_ylabel("내 돈", fontsize=15)
    ax.set_title("평균은 0%인데 25%가 사라졌다", fontsize=18, color=RED, pad=12)
    clean(ax)

    ax = axes[1]
    sd = np.linspace(0, 40, 200)
    ax.plot(sd, (sd / 100) ** 2 / 2 * 100, color=TEAL, lw=4)
    for s0, c in [(10, BLUE), (20, AMBER), (35, RED)]:
        v = (s0 / 100) ** 2 / 2 * 100
        ax.scatter([s0], [v], s=140, color=c, zorder=5)
        ax.annotate(f"변동성 {s0}% → 매년 {v:.1f}%p 손해", (s0, v),
                    xytext=(-10, 16), textcoords="offset points",
                    ha="right" if s0 > 25 else "left", fontsize=15.5, color=c)
    ax.set_xlabel("변동성(%)", fontsize=15)
    ax.set_ylabel("평균에서 깎이는 몫(%p)", fontsize=15)
    ax.set_title("많이 출렁일수록 더 깎인다", fontsize=18, color=INK, pad=12)
    clean(ax)
    fig.tight_layout()
    return save(fig, "arith_geo.png", EX)


# ── 비중은 저절로 틀어진다 ───────────────────────────────────────
def drift():
    rng = np.random.default_rng(5)
    n = 120
    req = 1 + rng.normal(.0092, .040, n)     # 주식이 길게 보면 더 번다
    rbd = 1 + rng.normal(.0015, .010, n)
    e, b = 60.0, 40.0
    share_drift, share_reb = [], []
    e2, b2 = 60.0, 40.0
    for i in range(n):
        e, b = e * req[i], b * rbd[i]
        share_drift.append(e / (e + b) * 100)
        e2, b2 = e2 * req[i], b2 * rbd[i]
        if (i + 1) % 12 == 0:               # 해마다 되돌린다
            t = e2 + b2
            e2, b2 = t * .6, t * .4
        share_reb.append(e2 / (e2 + b2) * 100)
    t = np.arange(n) / 12
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(t, share_drift, color=RED, lw=3.4, label="그냥 두면 — 정해 둔 60%에서 멀어진다")
    ax.plot(t, share_reb, color=TEAL, lw=3.4, label="해마다 되돌리면 — 60% 근처를 지킨다")
    ax.axhline(60, color=INK, lw=1.6, ls="--")
    ax.set_ylim(49, 67)
    ax.text(.2, 65.4, "정해 둔 비중 60%", fontsize=15.5, color=INK)
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("주식이 차지한 비율(%)", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="lower left")
    clean(ax)
    fig.tight_layout()
    return save(fig, "drift.png", EX)


# ── 되돌리면 무엇이 좋아지나 ─────────────────────────────────────
def rebalance():
    """같은 50 대 50을 놓고 '그냥 둔 것'과 '해마다 되돌린 것'만 견준다.
    다른 자산과 비교하면 되돌리기의 몫이 아니라 자산 고르기의 몫이 섞인다."""
    rng = np.random.default_rng(12)
    n = 240
    z = rng.normal(0, 1, n)
    ra = .004 + .030 * (z + rng.normal(0, .55, n))      # 둘은 반대로 움직인다
    rb = .004 + .030 * (-z + rng.normal(0, .55, n))
    hold_a = hold_b = 50.0
    reb_a = reb_b = 50.0
    HOLD, REB = [], []
    for i in range(n):
        hold_a *= 1 + ra[i]; hold_b *= 1 + rb[i]
        reb_a *= 1 + ra[i]; reb_b *= 1 + rb[i]
        if (i + 1) % 12 == 0:                            # 해마다 반반으로 되돌린다
            t = reb_a + reb_b
            reb_a = reb_b = t / 2
        HOLD.append(hold_a + hold_b); REB.append(reb_a + reb_b)
    t = np.arange(n) / 12
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(t, HOLD, color=MUTED, lw=3.0, label=f"반반 담고 그냥 두면 — 끝값 {HOLD[-1]:.0f}")
    ax.plot(t, REB, color=TEAL, lw=4.2, label=f"반반 담고 해마다 되돌리면 — 끝값 {REB[-1]:.0f}")
    ax.fill_between(t, HOLD, REB, where=np.array(REB) >= np.array(HOLD),
                    color=LIME, alpha=.35)
    ax.annotate(f"되돌리기가 만든 몫  +{REB[-1]-HOLD[-1]:.0f}", (t[-1], REB[-1]),
                xytext=(-18, 18), textcoords="offset points", ha="right",
                fontsize=17, color=INK, fontweight="bold")
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("100으로 시작한 값", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    clean(ax)
    fig.tight_layout()
    return save(fig, "rebalance.png", "되돌리기의 몫만 떼어 보려고 만든 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$g\;\approx\;\mu\;-\;\frac{\sigma^{2}}{2}$", fontsize=48, width=6.4)


if __name__ == "__main__":
    human_capital(); glide(); arith_geo(); drift(); rebalance(); equation()
    print("끝.")
