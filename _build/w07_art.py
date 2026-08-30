# -*- coding: utf-8 -*-
"""W07 프라이머의 그림 — M8 부채연계투자(LDI) · M9 목표기반투자(GBI)."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w07")
EX = "수업용으로 지어낸 예시입니다"


# ── 저울 — 자산만 보면 안 된다 (SVG) ─────────────────────────────
def funding():
    b = text(800, 52, "연기금의 성적표는 “얼마 벌었나”가 아니다", 30, INK, bold=True)
    b += text(800, 96, "“부채를 갚을 수 있나”이다", 28, MUTED)
    # 왼쪽 — 자산만 본다
    b += text(400, 168, "자산만 볼 때", 30, MUTED, bold=True)
    b += f'<rect x="270" y="200" width="260" height="200" rx="10" fill="{TEAL}"/>'
    b += text(400, 290, "모아 둔 돈", 28, WHITE)
    b += text(400, 330, "100", 40, WHITE, bold=True)
    b += text(400, 470, "“작년보다 5% 늘었다”", 27, MUTED)
    b += text(400, 512, "좋은 소식처럼 들린다", 27, MUTED)
    b += vrule(800, 140, 570, HAIR, 2)
    # 오른쪽 — 부채까지 본다
    b += text(1200, 168, "부채까지 볼 때", 30, INK, bold=True)
    b += f'<rect x="1000" y="200" width="180" height="200" rx="10" fill="{TEAL}"/>'
    b += text(1090, 290, "모아 둔 돈", 22, WHITE)
    b += text(1090, 330, "100", 34, WHITE, bold=True)
    b += f'<rect x="1220" y="180" width="180" height="240" rx="10" fill="{RED}"/>'
    b += text(1310, 280, "부채", 22, WHITE)
    b += text(1310, 322, "115", 34, WHITE, bold=True)
    b += text(1200, 470, "“5% 늘었지만 부채은 9% 늘었다”", 27, RED, bold=True)
    b += text(1200, 512, "= 작년보다 나빠졌다", 27, RED, bold=True)
    return svg("funding.png", b)


# ── 금리가 오르면 둘 다 움직인다 ─────────────────────────────────
def duration():
    dy = np.linspace(-2, 2, 200)
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axes[0]
    ax.plot(dy, -6 * dy, color=TEAL, lw=4, label="모아 둔 돈 (듀레이션 6년)")
    ax.plot(dy, -18 * dy, color=RED, lw=4, label="부채 (듀레이션 18년)")
    ax.axhline(0, color=INK, lw=1.2); ax.axvline(0, color=INK, lw=1.2)
    ax.set_xlabel("금리가 몇 %p 움직였나", fontsize=15)
    ax.set_ylabel("값이 몇 % 변하나", fontsize=15)
    ax.legend(fontsize=15, frameon=False, loc="lower left")
    ax.set_title("듀레이션이 길수록 크게 움직인다", fontsize=18, color=INK, pad=12)
    clean(ax, grid="both")

    ax = axes[1]
    x = np.arange(2)
    before = [100, 115]
    after = [100 * (1 + 6 * 0.01), 115 * (1 + 18 * 0.01)]   # 금리 1%p 하락
    ax.bar(x - .19, before, .38, color=MUTED, label="금리가 내리기 전")
    ax.bar(x + .19, after, .38, color=[TEAL, RED], label="금리 1%p 내린 뒤")
    for i in x:
        ax.text(i - .19, before[i] + 2, f"{before[i]:.0f}", ha="center", fontsize=15, color=INK)
        ax.text(i + .19, after[i] + 2, f"{after[i]:.0f}", ha="center", fontsize=15,
                color=INK, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(["모아 둔 돈", "부채"], fontsize=17)
    ax.set_ylim(0, 156)
    ax.set_title(f"부채를 갚을 수 있는 비율  {100/115*100:.0f}% → {after[0]/after[1]*100:.0f}%",
                 fontsize=18, color=RED, pad=12, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "duration.png", EX)


# ── 2022 영국 ────────────────────────────────────────────────────
def uk2022():
    d = np.arange(0, 26)
    y = 3.6 + 1.2 * (1 - np.exp(-d / 4.5)) * (d > 3)
    y[d > 12] = y[12] - 0.35 * (d[d > 12] - 12) / 13
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(d, y, color=RED, lw=4)
    ax.axvspan(4, 12, color=RED, alpha=.08)
    ax.annotate("작은 예산안 발표", (4, y[4]), xytext=(-8, 54),
                textcoords="offset points", ha="right", fontsize=16, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.text(8.4, 5.16, "닷새 만에 30년 금리 +1.2%p", fontsize=17, color=RED,
            fontweight="bold", ha="center")
    ax.annotate("중앙은행이 사들이기 시작", (14, y[14]), xytext=(16, -64),
                textcoords="offset points", fontsize=16, color=TEAL,
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.6))
    ax.set_xlabel("2022년 9월 이후 지난 날수", fontsize=15)
    ax.set_ylabel("30년 국채 금리(%)", fontsize=15)
    ax.set_ylim(3.2, 5.4)
    clean(ax)
    fig.tight_layout()
    return save(fig, "uk2022.png", "2022년 영국의 흐름을 본떠 만든 예시입니다")


# ── 세 개의 통 (SVG) ─────────────────────────────────────────────
def buckets():
    b = text(800, 52, "목표마다 다른 통에 담는다", 30, INK, bold=True)
    b += text(800, 94, "“얼마 벌까”가 아니라 “무엇을 위해 모으나”에서 시작한다", 26, MUTED)
    specs = [(90, "반드시 써야 할 돈", ["매달 나갈 생활비", "실패하면 안 된다"],
              "안전하게", RED),
             (570, "되도록 이루고 싶은 것", ["여행 · 자녀 지원", "못 하면 아쉽다"],
              "적당히", AMBER),
             (1050, "되면 좋은 것", ["기부 · 물려주기", "못 해도 괜찮다"],
              "공격적으로", TEAL)]
    for x, name, lines, how, c in specs:
        b += (f'<rect x="{x}" y="140" width="460" height="290" rx="12" fill="{WHITE}" '
              f'stroke="{c}" stroke-width="3"/>')
        b += text(x + 230, 196, name, 32, c, bold=True)
        b += hrule(x + 60, x + 400, 218, HAIR, 2)
        for i, ln in enumerate(lines):
            b += text(x + 230, 266 + i * 42, ln, 26, INK)
        b += text(x + 230, 386, f"→ {how} 굴린다", 27, c, bold=True)
    b += limebox(400, 468, 800, 118, "통마다 목표가 다르니 굴리는 법도 다르다",
                 ["하나의 큰 통으로 보면 이 차이가 사라진다"])
    return svg("buckets.png", b)


# ── 목표를 이룰 확률 ─────────────────────────────────────────────
def goal_prob():
    save_rate = np.linspace(4, 20, 200)
    p = 100 / (1 + np.exp(-(save_rate - 11) / 2.2))
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(save_rate, p, color=TEAL, lw=4)
    ax.axhline(90, color=MUTED, lw=1.4, ls=":")
    for r, c, lab, off in [(8, RED, "월급의 8%를 모으면\n목표 달성 확률 21%", (-16, 8)),
                           (14, LIME, "14%로 올리면\n확률 80%", (16, -12))]:
        v = 100 / (1 + np.exp(-(r - 11) / 2.2))
        ax.scatter([r], [v], s=190, color=c, zorder=5, edgecolors=INK, linewidth=1.4)
        ax.annotate(lab, (r, v), xytext=off, textcoords="offset points",
                    ha="left" if off[0] > 0 else "right", fontsize=16,
                    color=INK if c == LIME else c, fontweight="bold")
    ax.set_xlabel("월급에서 떼어 모으는 비율(%)", fontsize=15)
    ax.set_ylabel("목표를 이룰 확률(%)", fontsize=15)
    ax.set_ylim(0, 105)
    clean(ax)
    fig.tight_layout()
    return save(fig, "goal_prob.png", EX)


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$\frac{\Delta P}{P}\;\approx\;-\,D\,\times\,\Delta y$",
                  fontsize=46, width=7.0)


if __name__ == "__main__":
    funding(); duration(); uk2022(); buckets(); goal_prob(); equation()
    print("끝.")
