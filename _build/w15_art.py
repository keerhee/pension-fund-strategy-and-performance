# -*- coding: utf-8 -*-
"""W15 프라이머의 그림 — M16 총자산 접근(TPA)."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w15")
EX = "수업용으로 지어낸 예시입니다"


# ── 사일로와 통합 (SVG) ──────────────────────────────────────────
def silo():
    b = text(430, 48, "지금까지 — 부서마다 자기 몫", 29, RED, bold=True)
    for i, (n, w) in enumerate([("주식팀", "40%"), ("채권팀", "35%"), ("대체팀", "25%")]):
        y = 110 + i * 150
        b += box(90, y, 620, 120, f"{n}  —  {w}", ["이 안에서만 최고를 노린다"],
                 stroke=HAIR, ts=30, ss=24)
    b += text(400, 600, "칸막이 안에서 각자 이긴다", 26, RED)
    b += vrule(790, 40, 620, HAIR, 2)
    b += text(1180, 48, "총자산 접근 — 한 통에서 겨룬다", 29, TEAL, bold=True)
    b += limebox(880, 110, 600, 190, "하나의 위험 예산",
                 ["부서가 아니라 아이디어끼리", "같은 저울에 올린다"])
    b += box(880, 330, 600, 120, "무엇을 사느냐가 아니라", ["어떤 위험을 지느냐로 나눈다"],
             stroke=TEAL, tc=TEAL, sc=INK, ts=28, ss=24)
    b += text(1180, 520, "좋은 아이디어면 어느 팀 것이든", 26, TEAL)
    b += text(1180, 560, "예산을 가져간다", 26, TEAL)
    b += text(1180, 600, "비어 있는 칸이 없다", 26, MUTED)
    return svg("silo.png", b)


# ── 축구팀 비유 (SVG) ────────────────────────────────────────────
def soccer():
    b = text(800, 50, "포지션별 최고를 모은다고 최강팀이 되지는 않는다", 30, INK, bold=True)
    b += text(800, 96, "각자 자기 자리에서 최고여도, 함께 뛰면 겹치거나 빈다", 26, MUTED)
    b += box(90, 150, 640, 230, "부서별로 최고를 뽑으면",
             ["주식팀도 “경기가 좋다”에 걸고", "대체팀도 같은 데 건다",
              "결국 한 곳에 몰린다"], stroke=RED, tc=RED, sc=INK, ts=30, ss=25)
    b += arrow(748, 265, 848, 265, MUTED, "aM", 5)
    b += limebox(880, 150, 640, 230, "한 통에서 보면",
                 ["같은 베팅이 겹친 걸 알아채고", "빈 곳에 예산을 옮긴다"])
    b += hrule(90, 1520, 440, HAIR, 2)
    b += text(800, 512, "부서를 없애자는 말이 아니다", 28, INK, bold=True)
    b += text(800, 562, "예산을 부서가 아니라 아이디어에 준다는 말이다", 28, TEAL, bold=True)
    return svg("soccer.png", b)


# ── 겹친 베팅 ────────────────────────────────────────────────────
def overlap():
    teams = ["주식팀", "채권팀", "대체팀", "매크로팀"]
    exposures = np.array([[.55, .10, .20, .15],
                          [.15, .50, .20, .15],
                          [.50, .05, .30, .15],
                          [.45, .15, .25, .15]])
    risks = ["경기가 좋다", "금리가 내린다", "물가가 오른다", "그 밖"]
    fig, ax = plt.subplots(figsize=WIDE)
    bottom = np.zeros(4)
    cols = [RED, BLUE, AMBER, HAIR]
    for j, (rk, c) in enumerate(zip(risks, cols)):
        ax.bar(range(4), exposures[:, j] * 100, bottom=bottom * 100, width=.6,
               color=c, label=rk)
        for i in range(4):
            if exposures[i, j] > .12:
                ax.text(i, (bottom[i] + exposures[i, j] / 2) * 100,
                        f"{exposures[i,j]*100:.0f}%", ha="center", va="center",
                        fontsize=15, color=WHITE if c != HAIR else INK,
                        fontweight="bold")
        bottom += exposures[:, j]
    ax.set_xticks(range(4)); ax.set_xticklabels(teams, fontsize=17)
    ax.set_ylabel("그 팀이 진 위험의 구성(%)", fontsize=15)
    ax.set_ylim(0, 128)
    ax.legend(fontsize=15, frameon=False, ncol=4, loc="upper center")
    ax.text(1.5, 108, "네 팀 중 셋이 “경기가 좋다”에 절반 가까이 걸었다",
            ha="center", fontsize=17, color=RED, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "overlap.png", EX)


# ── 예산을 아이디어에 준다 ───────────────────────────────────────
def budget():
    ideas = ["아이디어 A", "아이디어 B", "아이디어 C", "아이디어 D", "아이디어 E"]
    quality = np.array([2.4, 1.9, 1.6, 0.9, 0.4])
    silo_w = np.array([1.2, 1.8, 1.0, 1.6, 1.4])
    x = np.arange(5)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(x - .19, silo_w, .38, color=MUTED, label="부서별로 나눴을 때")
    ax.bar(x + .19, quality, .38, color=[LIME if q >= 1.6 else HAIR for q in quality],
           edgecolor=[INK if q >= 1.6 else "none" for q in quality], linewidth=1.2,
           label="아이디어의 값어치대로 줬을 때")
    ax.set_xticks(x); ax.set_xticklabels(ideas, fontsize=16)
    ax.set_ylabel("받아 간 위험 예산", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper right")
    ax.set_ylim(0, 3.2)
    ax.text(2, 2.86, "좋은 아이디어에 더 주고, 약한 것은 줄인다",
            ha="center", fontsize=17, color=INK)
    clean(ax)
    fig.tight_layout()
    return save(fig, "budget.png", EX)


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$\sigma_{active}\;=\;\sqrt{\sum_i \sigma_i^{2}\;+\;2\sum_{i<j}\rho_{ij}\,\sigma_i\sigma_j}$",
                  fontsize=40, width=10.0)


if __name__ == "__main__":
    silo(); soccer(); overlap(); budget(); equation()
    print("끝.")
