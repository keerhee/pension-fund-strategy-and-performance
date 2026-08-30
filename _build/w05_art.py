# -*- coding: utf-8 -*-
"""W05 프라이머의 그림 — M6 리스크 패리티와 HRP."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w05")
EX = "주식 18% · 채권 5% · 상관 0.2 로 놓고 계산한 예시입니다"

# 예시 자산 — 주식과 채권
SD = np.array([0.18, 0.05])
RHO = 0.2
COV = np.array([[SD[0]**2, RHO * SD[0] * SD[1]],
                [RHO * SD[0] * SD[1], SD[1]**2]])


def rc(w):
    """자산별 위험기여도(합이 포트폴리오 변동성)."""
    w = np.asarray(w, float)
    s = np.sqrt(w @ COV @ w)
    return w * (COV @ w) / s, s


# ── 자본으로 반, 위험으로는 반이 아니다 ──────────────────────────
def capital_vs_risk():
    w = np.array([0.6, 0.4])
    contrib, s = rc(w)
    share = contrib / contrib.sum() * 100
    fig, axes = plt.subplots(1, 2, figsize=WIDE)
    for ax, vals, title, note in [
            (axes[0], w * 100, "돈을 나눈 비율", "겉으로 보이는 모습"),
            (axes[1], share, "위험을 나눈 비율", "실제로 짊어진 모습")]:
        cols = [RED if vals is not w * 100 else TEAL, BLUE]
        cols = [TEAL, BLUE] if title.startswith("돈") else [RED, BLUE]
        ax.pie(vals, colors=cols, startangle=90, counterclock=False,
               autopct=lambda p: f"{p:.0f}%", textprops=dict(fontsize=20, color=WHITE,
                                                             fontweight="bold"),
               wedgeprops=dict(edgecolor=PAPER, linewidth=3))
        ax.set_title(f"{title}\n{note}", fontsize=18, color=INK, pad=14)
    fig.legend(["주식", "채권"], fontsize=16, frameon=False,
               loc="lower center", ncol=2, bbox_to_anchor=(.5, -.02))
    fig.suptitle(f"60 대 40으로 나눴는데, 위험은 {share[0]:.0f} 대 {share[1]:.0f}로 쏠려 있다",
                 fontsize=19, color=RED, y=1.02, fontweight="bold")
    fig.tight_layout()
    return save(fig, "capital_vs_risk.png", EX)


# ── 시소 (SVG) ───────────────────────────────────────────────────
def seesaw():
    SHARE_EQ = rc([0.6, 0.4])[0][0] / rc([0.6, 0.4])[0].sum() * 100
    b = text(800, 50, "무게가 같아도 앉는 자리가 다르면 균형이 아니다", 30, INK, bold=True)
    # 왼쪽 — 자본 균형
    b += text(400, 118, "돈으로는 60 대 40", 28, MUTED)
    b += f'<polygon points="400,330 360,400 440,400" fill="{MUTED}"/>'
    b += f'<line x1="140" y1="318" x2="660" y2="342" stroke="{INK}" stroke-width="8"/>'
    b += f'<circle cx="180" cy="288" r="52" fill="{TEAL}"/>' + text(180, 300, "주식", 26, WHITE)
    b += f'<circle cx="620" cy="312" r="42" fill="{BLUE}"/>' + text(620, 322, "채권", 24, WHITE)
    b += text(400, 470, "주식이 훨씬 멀리 앉아 있다", 26, RED, bold=True)
    b += text(400, 512, f"= 위험의 {SHARE_EQ:.0f}%를 주식이 진다", 26, RED, bold=True)
    b += vrule(800, 90, 570, HAIR, 2)
    # 오른쪽 — 위험 균형
    b += text(1200, 118, "위험으로 맞추면", 28, MUTED)
    b += f'<polygon points="1200,330 1160,400 1240,400" fill="{MUTED}"/>'
    b += f'<line x1="960" y1="330" x2="1440" y2="330" stroke="{INK}" stroke-width="8"/>'
    b += f'<circle cx="1000" cy="298" r="30" fill="{TEAL}"/>' + text(1000, 306, "주식", 20, WHITE)
    b += f'<circle cx="1400" cy="288" r="52" fill="{LIME}" stroke="{INK}" stroke-width="3"/>'
    b += text(1400, 300, "채권", 26, DARK)
    b += text(1200, 470, "주식을 줄이고 채권을 늘리면", 26, TEAL, bold=True)
    b += text(1200, 512, "= 둘이 위험을 반씩 진다", 26, TEAL, bold=True)
    return svg("seesaw.png", b)


# ── 위험을 같게 만들면 비중은 이렇게 된다 ────────────────────────
def equalize():
    ws = np.linspace(0.02, 0.98, 400)
    gap = []
    for wq in ws:
        c, _ = rc([wq, 1 - wq])
        gap.append(c[0] / c.sum())
    gap = np.array(gap)
    k = np.abs(gap - 0.5).argmin()
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(ws * 100, gap * 100, color=TEAL, lw=4)
    ax.axhline(50, color=MUTED, lw=1.4, ls=":")
    for wq, c, lab, off in [(0.60, RED, f"돈 60% 담으면\n위험은 {gap[np.abs(ws-.6).argmin()]*100:.0f}%", (14, -54)),
                            (ws[k], LIME, f"돈 {ws[k]*100:.0f}%만 담아야\n위험이 반반", (18, -58))]:
        i = np.abs(ws - wq).argmin()
        ax.scatter([wq * 100], [gap[i] * 100], s=190, color=c, zorder=5,
                   edgecolors=INK, linewidth=1.4)
        ax.annotate(lab, (wq * 100, gap[i] * 100), xytext=off,
                    textcoords="offset points", fontsize=16,
                    color=INK if c == LIME else c, fontweight="bold")
    ax.set_xlabel("주식에 넣은 돈의 비율(%)", fontsize=15)
    ax.set_ylabel("주식이 지는 위험의 비율(%)", fontsize=15)
    ax.set_ylim(0, 105)
    clean(ax)
    fig.tight_layout()
    return save(fig, "equalize.png", EX)


# ── 2022년에 드러난 한계 ─────────────────────────────────────────
def y2022():
    labels = ["주식", "채권", "60/40", "위험을 반반 나눈 것"]
    vals = [-18.1, -13.0, -16.1, -19.4]
    cols = [TEAL, BLUE, MUTED, RED]
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(range(4), vals, color=cols, width=.56)
    for i, v in enumerate(vals):
        ax.text(i, v - 1.1, f"{v:.1f}%", ha="center", va="top",
                fontsize=18, color=INK, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=17)
    ax.set_ylabel("그해 수익률(%)", fontsize=15)
    ax.set_ylim(-24, 3)
    ax.text(1.5, -2.0, "주식과 채권이 함께 내리면 나눠 담기가 통하지 않는다",
            ha="center", va="top", fontsize=17, color=RED, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "y2022.png", "2022년의 흐름을 본떠 만든 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$RC_i\;=\;w_i\;\times\;\frac{\left(\Sigma w\right)_i}{\sigma_p}$",
                  fontsize=44, width=8.0)


if __name__ == "__main__":
    capital_vs_risk(); seesaw(); equalize(); y2022(); equation()
    print("끝.")
