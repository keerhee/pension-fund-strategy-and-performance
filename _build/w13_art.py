# -*- coding: utf-8 -*-
"""W13 프라이머의 그림 — M14 글로벌 매크로와 CTA · SS1 최적 통화 헤지."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w13")
EX = "수업용으로 지어낸 예시입니다"


# ── 네 계절 (SVG) ────────────────────────────────────────────────
def quadrant():
    b = text(800, 46, "경기와 물가로 네 계절을 나눈다", 30, INK, bold=True)
    b += text(800, 84, "계절마다 잘 되는 자산이 다르다", 26, MUTED)
    cx, cy, w, h = 430, 130, 470, 210
    cells = [(0, 0, "경기 좋고 물가 오름", ["원자재 · 신흥국"], AMBER),
             (1, 0, "경기 좋고 물가 안정", ["주식이 가장 좋다"], TEAL),
             (0, 1, "경기 나쁘고 물가 오름", ["가장 어려운 계절"], RED),
             (1, 1, "경기 나쁘고 물가 내림", ["긴 국채가 버틴다"], BLUE)]
    for i, j, name, lines, c in cells:
        x, y = cx + i * (w + 24), cy + j * (h + 24)
        b += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{WHITE}" '
              f'stroke="{c}" stroke-width="3"/>')
        b += text(x + w / 2, y + 74, name, 29, c, bold=True)
        b += text(x + w / 2, y + 130, lines[0], 27, INK)
    b += text(180, 250, "물가가", 26, MUTED)
    b += text(180, 288, "오른다", 28, INK, bold=True)
    b += text(180, 490, "물가가", 26, MUTED)
    b += text(180, 528, "내린다", 28, INK, bold=True)
    b += text(665, 594, "경기가 좋다", 27, INK, bold=True)
    b += text(1160, 594, "경기가 나쁘다", 27, INK, bold=True)
    return svg("quadrant.png", b)


# ── 무상관 베팅의 힘 ─────────────────────────────────────────────
def sqrtn():
    n = np.arange(1, 41)
    sr = 0.30 * np.sqrt(n)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(n, sr, color=TEAL, lw=4)
    for k, c, lab in [(1, BLUE, "한 곳에만 걸면 0.30"),
                      (9, AMBER, "아홉 곳이면 0.90"),
                      (25, LIME, "스물다섯 곳이면 1.50")]:
        ax.scatter([k], [0.30 * np.sqrt(k)], s=190, color=c, zorder=5,
                   edgecolors=INK if c == LIME else "none", linewidth=1.4)
        ax.annotate(lab, (k, 0.30 * np.sqrt(k)), xytext=(16, -6),
                    textcoords="offset points", fontsize=17,
                    color=INK if c == LIME else c, fontweight="bold")
    ax.set_xlabel("서로 무관한 베팅의 수", fontsize=15)
    ax.set_ylabel("변동성 한 단위당 번 몫", fontsize=15)
    ax.text(2, 1.72, "베팅 하나하나의 실력은 그대로인데\n수를 늘리는 것만으로 성적이 올라간다",
            fontsize=17, color=INK)
    ax.set_ylim(0, 2.1)
    clean(ax)
    fig.tight_layout()
    return save(fig, "sqrtn.png", "베팅 하나의 실력을 0.30으로 놓고 그린 그림입니다")


# ── 성적을 올리는 두 길 (SVG) ───────────────────────────────────
def two_ways():
    """'맞히기'와 '나누기'가 각각 무엇인지 정확히 갈라 놓는다.
    두 낱말을 뭉뚱그리면 이 주차의 논지가 통째로 흐려진다."""
    b = text(800, 46, "성적을 올리는 길은 둘뿐이다", 30, INK, bold=True)
    b += text(800, 86, "매크로 운용은 둘 중 어느 쪽에 기대는가", 26, MUTED)

    b += (f'<rect x="60" y="118" width="720" height="252" rx="12" fill="{WHITE}" '
          f'stroke="{HAIR}" stroke-width="2"/>')
    b += text(420, 172, "① 더 잘 맞힌다", 34, INK, bold=True)
    b += text(420, 208, "= 적중률을 올린다", 26, MUTED)
    b += hrule(110, 730, 232, HAIR, 2)
    b += text(420, 274, "한 판단이 맞을 확률을 높이는 일", 26, INK)
    b += text(420, 312, "예 — 금리 방향을 남보다 정확히 본다", 25, MUTED)
    b += text(420, 350, "어렵다 · 남들도 같은 자료를 본다", 25, RED)

    b += (f'<rect x="820" y="118" width="720" height="252" rx="12" fill="{LIME}" '
          f'stroke="{INK}" stroke-width="3"/>')
    b += text(1180, 172, "② 나눠서 여러 번 건다", 34, DARK, bold=True)
    b += text(1180, 208, "= 서로 무관한 판단의 수를 늘린다", 26, DARK)
    b += hrule(870, 1490, 232, DARK, 2)
    b += text(1180, 274, "서로 영향을 주지 않는 판단을 더 만드는 일", 26, DARK)
    b += text(1180, 312, "예 — 금리 · 통화 · 원자재 · 주가지수에 따로", 25, DARK)
    b += text(1180, 350, "해볼 만하다 · 실력이 같아도 성적이 오른다", 25, DARK)

    b += (f'<rect x="240" y="410" width="1120" height="80" rx="10" fill="{DARK}"/>')
    b += text(800, 462, "성적  =  한 판단의 적중률  ×  √( 서로 무관한 판단의 수 )",
              32, LIME, bold=True)
    b += text(800, 546, "“서로 무관한”이 빠지면 아무리 늘려도 수가 늘지 않는다", 27, RED, bold=True)
    b += text(800, 588, "같은 방향에 건 베팅 스무 개는 세어 보면 하나다", 26, MUTED)
    return svg("two_ways.png", b)


# ── 추세를 따라간다 ──────────────────────────────────────────────
def tsmom():
    rng = np.random.default_rng(6)
    n = 180
    trend = np.concatenate([np.linspace(0, 26, 70), np.linspace(26, 4, 60),
                            np.linspace(4, 22, 50)])
    p = 100 + trend + np.cumsum(rng.normal(0, .9, n))
    ma = np.convolve(p, np.ones(24) / 24, mode="same")
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(p, color=INK, lw=2.2, label="값의 움직임")
    ax.plot(ma, color=AMBER, lw=3.0, label="최근 평균")
    up = p > ma
    ax.fill_between(np.arange(n), p.min() - 4, p.max() + 4, where=up,
                    color=TEAL, alpha=.13)
    ax.fill_between(np.arange(n), p.min() - 4, p.max() + 4, where=~up,
                    color=RED, alpha=.10)
    ax.text(16, p.max() + 1, "평균 위 → 산다", fontsize=17, color=TEAL, fontweight="bold")
    ax.text(88, p.max() + 1, "평균 아래 → 던다", fontsize=17, color=RED, fontweight="bold")
    ax.set_xlabel("시간(일)", fontsize=15)
    ax.set_ylabel("값", fontsize=15)
    ax.set_ylim(p.min() - 4, p.max() + 6)
    ax.legend(fontsize=16, frameon=False, loc="lower right")
    clean(ax, grid=None)
    fig.tight_layout()
    return save(fig, "tsmom.png", "규칙의 모양을 보이려고 만든 예시입니다")


# ── 환헤지 비율 ──────────────────────────────────────────────────
def hedge_u():
    h = np.linspace(0, 1, 200)
    sa, sf, rho = .15, .09, -.25
    vol = np.sqrt(sa**2 + (1 - h)**2 * sf**2 + 2 * (1 - h) * rho * sa * sf) * 100
    k = vol.argmin()
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(h * 100, vol, color=TEAL, lw=4)
    ax.scatter([h[k] * 100], [vol[k]], s=340, color=LIME, marker="*", zorder=5,
               edgecolors=INK, linewidth=1.2)
    ax.annotate(f"가장 덜 흔들리는 지점 — {h[k]*100:.0f}%", (h[k] * 100, vol[k]),
                xytext=(0, 34), textcoords="offset points", ha="center",
                fontsize=17, color=INK, fontweight="bold")
    for x0, c, lab, off in [(0, RED, "하나도 안 막으면", (16, 8)),
                            (100, BLUE, "전부 막으면", (-16, 8))]:
        i = np.abs(h * 100 - x0).argmin()
        ax.scatter([x0], [vol[i]], s=150, color=c, zorder=5)
        ax.annotate(lab, (x0, vol[i]), xytext=off, textcoords="offset points",
                    ha="left" if off[0] > 0 else "right", fontsize=16, color=c,
                    fontweight="bold")
    ax.set_xlabel("환율 위험을 막은 비율(%)", fontsize=15)
    ax.set_ylabel("전체 변동성(%)", fontsize=15)
    clean(ax)
    fig.tight_layout()
    return save(fig, "hedge_u.png",
                "해외 주식 15% · 환율 9% · 상관 −0.25 로 놓고 계산한 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$SR_N\;=\;SR_1\,\times\,\sqrt{N}$", fontsize=48, width=7.0)


if __name__ == "__main__":
    quadrant(); sqrtn(); two_ways(); tsmom(); hedge_u(); equation()
    print("끝.")
