# -*- coding: utf-8 -*-
"""W10 프라이머의 그림 — M11 주식 퀀트 투자."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w10")
EX = "수업용으로 지어낸 예시입니다"


# ── 네 칸 파이프라인 (SVG) ───────────────────────────────────────
def pipeline():
    b = text(800, 52, "사람이 종목을 고르는 대신, 규칙을 만들어 기계에 맡긴다", 30, INK, bold=True)
    steps = [("① 자료를 모은다", ["값 · 실적 · 거래량"], WHITE, HAIR, INK, MUTED),
             ("② 점수를 매긴다", ["규칙 하나를 정해", "종목마다 점수를"], WHITE, HAIR, INK, MUTED),
             ("③ 담을 것을 정한다", ["점수 높은 쪽을 사고", "낮은 쪽은 던다"], WHITE, HAIR, INK, MUTED)]
    xs = [70, 470, 870]
    for x, (t0, lines, f, st, tc, sc) in zip(xs, steps):
        b += box(x, 150, 350, 200, t0, lines, fill=f, stroke=st, tc=tc, sc=sc, ts=30)
        b += arrow(x + 360, 250, x + 458, 250, MUTED, "aM", 5)
    b += limebox(1270, 150, 260, 200, "④ 사고판다", ["수수료를 줄이며"])
    b += text(800, 430, "사람이 하는 일은 규칙을 정하고 지키는 것이다", 28, TEAL, bold=True)
    b += text(800, 480, "종목 하나하나를 들여다보는 일이 아니다", 26, MUTED)
    b += text(800, 552, "그래서 “왜 이 규칙인가”에 답하지 못하면 그 규칙은 쓸 수 없다",
              27, RED, bold=True)
    return svg("pipeline.png", b)


# ── 점수로 줄 세우면 ─────────────────────────────────────────────
def quantile():
    rng = np.random.default_rng(4)
    n, m = 60, 5
    base = np.linspace(-.010, .012, m)
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1, 1.3]})
    ax = axes[0]
    cols = [RED, AMBER, MUTED, BLUE, TEAL]
    ax.bar(range(m), base * 1200, color=cols, width=.62)
    for i, v in enumerate(base * 1200):
        ax.text(i, v + (.25 if v > 0 else -.25), f"{v:+.1f}%", ha="center",
                va="bottom" if v > 0 else "top", fontsize=15, color=INK)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xticks(range(m))
    ax.set_xticklabels(["1등급\n(낮은 점수)", "2", "3", "4", "5등급\n(높은 점수)"], fontsize=13)
    ax.set_ylabel("해마다 번 몫(%)", fontsize=15)
    ax.set_title("점수 순으로 다섯 무리를 만들면", fontsize=18, color=INK, pad=12)
    clean(ax)

    ax = axes[1]
    t = np.arange(n) / 12
    for k, (c, lab) in enumerate([(TEAL, "높은 점수 무리"), (RED, "낮은 점수 무리")]):
        mu = .012 if k == 0 else -.010
        r = rng.normal(mu / 12, .030, n)
        ax.plot(t, 100 * np.cumprod(1 + r), color=c, lw=3.6, label=lab)
    ax.axhline(100, color=MUTED, lw=1.2, ls=":")
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("100으로 시작한 값", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    ax.set_title("두 무리를 계속 들고 있으면", fontsize=18, color=INK, pad=12)
    clean(ax)
    fig.tight_layout()
    return save(fig, "quantile.png", EX)


# ── 표본 안에서만 좋은 규칙 ──────────────────────────────────────
def overfit():
    rng = np.random.default_rng(11)
    n = 96
    t = np.arange(n) / 12
    inn = np.concatenate([rng.normal(.016, .022, n // 2), rng.normal(.001, .030, n // 2)])
    fig, ax = plt.subplots(figsize=WIDE)
    v = 100 * np.cumprod(1 + inn)
    ax.plot(t[:n // 2], v[:n // 2], color=TEAL, lw=4, label="규칙을 만들 때 쓴 기간")
    ax.plot(t[n // 2 - 1:], v[n // 2 - 1:], color=RED, lw=4, label="그 뒤 실제로 굴린 기간")
    ax.axvline(t[n // 2], color=INK, lw=2, ls="--")
    ax.text(t[n // 2] + .1, v.max() * .98, "여기서부터가 진짜", fontsize=17,
            color=INK, fontweight="bold")
    ax.text(.28, .10, "고르고 고른 규칙이라\n좋아 보인다", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=16, color=TEAL)
    ax.text(.80, .40, "밖에서는 그만큼\n나오지 않는다", transform=ax.transAxes,
            ha="center", va="top", fontsize=16, color=RED, fontweight="bold")
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("100으로 시작한 값", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="lower right")
    clean(ax)
    fig.tight_layout()
    return save(fig, "overfit.png", "과최적화를 보이려고 만든 예시입니다")


# ── 팩터란 무엇인가 (SVG) ────────────────────────────────────────
def what_is_factor():
    """한 종목의 움직임을 세 갈래로 갈라, 가운데 갈래가 팩터임을 보인다."""
    b = text(800, 48, "한 종목이 오르내리는 이유는 세 갈래다", 30, INK, bold=True)
    b += box(60, 190, 330, 150, "어느 회사 주식", ["이번 달 +5.0%"], stroke=HAIR, ts=30)
    rows = [(100, "① 시장 전체가 올라서", "+3.0%", "모든 주식이 함께 움직인 몫", MUTED, WHITE),
            (255, "② 같은 성질끼리 함께 올라서", "+1.5%", "작은 회사들이 다 같이 올랐다", INK, LIME),
            (410, "③ 그 회사만의 일", "+0.5%", "신제품이 잘 팔렸다", MUTED, WHITE)]
    for y, name, val, desc, tc, fill in rows:
        b += arrow(400, 265, 470, y + 60, MUTED, "aM", 4)
        st = INK if fill == LIME else HAIR
        b += (f'<rect x="490" y="{y}" width="700" height="130" rx="10" fill="{fill}" '
              f'stroke="{st}" stroke-width="{3 if fill == LIME else 2}"/>')
        b += text(520, y + 52, name, 29, tc, "start", True)
        b += text(520, y + 96, desc, 24, DARK if fill == LIME else MUTED, "start")
        b += text(1150, y + 74, val, 34, tc, "end", True)
    b += text(1230, 300, "여러 종목을", 26, INK, "start", True)
    b += text(1230, 342, "함께 움직이게 하는", 26, INK, "start", True)
    b += text(1230, 384, "공통 원인", 30, INK, "start", True)
    b += text(1230, 432, "= 팩터", 34, INK, "start", True)
    b += text(800, 590, "①은 누구나 얻고 ③은 흩어져 사라진다 — 골라 담을 수 있는 것은 ②뿐이다",
              27, RED, bold=True)
    return svg("what_is_factor.png", b)


# ── 어떤 팩터가 있나 (SVG) ───────────────────────────────────────
def factor_menu():
    b = text(800, 46, "모형에 흔히 넣는 팩터들", 30, INK, bold=True)
    b += text(800, 86, "모두 “한 묶음에서 다른 묶음을 뺀 수익”으로 만든다", 26, MUTED)
    specs = [("시장", "MKT", "주식 전체 − 국채"),
             ("크기", "SMB", "작은 회사 − 큰 회사"),
             ("가치", "HML", "싼 주식 − 비싼 주식"),
             ("수익성", "RMW", "잘 버는 회사 − 못 버는 회사"),
             ("투자", "CMA", "조심히 늘리는 회사 − 마구 늘리는 회사"),
             ("모멘텀", "UMD", "오르던 것 − 내리던 것")]
    for i, (ko, tag, rule) in enumerate(specs):
        x = 60 + (i % 3) * 500
        y = 130 + (i // 3) * 200
        b += (f'<rect x="{x}" y="{y}" width="460" height="160" rx="10" fill="{WHITE}" '
              f'stroke="{HAIR}" stroke-width="2"/>')
        b += text(x + 30, y + 56, ko, 32, INK, "start", True)
        b += text(x + 430, y + 54, tag, 26, TEAL, "end", True)
        b += hrule(x + 30, x + 430, y + 78, HAIR, 2)
        b += text(x + 230, y + 122, rule, 24, MUTED)
    b += text(800, 578, "앞의 다섯은 파마와 프렌치가, 모멘텀은 카하트가 정리했다",
              26, MUTED)
    return svg("factor_menu.png", b)


# ── 파마-프렌치가 바꾼 것 ────────────────────────────────────────
def ff_lineage():
    names = ["1964  CAPM\n시장 하나만", "1993  파마-프렌치 3팩터\n＋크기 ＋가치",
             "2015  파마-프렌치 5팩터\n＋수익성 ＋투자"]
    r2 = [72, 90, 94]
    cols = [MUTED, TEAL, LIME]
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(range(3), r2, color=cols, width=.56,
           edgecolor=[("none" if c != LIME else INK) for c in cols], linewidth=1.4)
    for i, v in enumerate(r2):
        ax.text(i, v + 1.4, f"{v}%", ha="center", fontsize=23, color=INK, fontweight="bold")
    ax.set_xticks(range(3)); ax.set_xticklabels(names, fontsize=16)
    ax.set_ylabel("종목의 오르내림 중 설명되는 몫(%)", fontsize=15)
    ax.set_ylim(0, 116)
    ax.annotate("", xy=(.70, 79), xytext=(.30, 79),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.4))
    ax.text(.5, 82, "시장 하나로는 부족했다", ha="center", fontsize=17,
            color=RED, fontweight="bold")
    ax.text(1.5, 108, "“설명되지 않던 몫”을 줄여 온 60년",
            ha="center", fontsize=18, color=INK, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "ff_lineage.png",
                "설명되는 몫은 자료와 기간에 따라 달라집니다 · 흐름을 보이려는 예시입니다")


# ── 수익을 조각으로 나눈다 ───────────────────────────────────────
def decompose():
    """한 종목의 한 해 수익을 '어디서 왔는지'로 쪼갠다.
    앞 세 조각은 누구나 살 수 있는 것이고, 마지막 조각만 실력이다."""
    parts = [("시장이 올라서", 8.0, TEAL), ("작은 회사라서", 3.0, BLUE),
             ("싼 주식이라서", 2.0, AMBER), ("설명 안 되는 몫", 1.4, LIME)]
    total = sum(v for _, v, _ in parts)
    known = total - parts[-1][1]
    fig, ax = plt.subplots(figsize=WIDE)
    left = 0.0
    for k, (name, v, c) in enumerate(parts):
        ax.barh([0], [v], left=[left], height=.46, color=c,
                edgecolor=INK if c == LIME else "none", linewidth=1.4)
        ax.text(left + v / 2, 0, f"{v:.1f}%", ha="center", va="center",
                fontsize=19, color=INK if c in (LIME, AMBER) else WHITE,
                fontweight="bold")
        # 이름은 위쪽에 번갈아 놓아 서로 겹치지 않게 한다
        ax.text(left + v / 2, .36 if k % 2 == 0 else .62, name, ha="center",
                fontsize=16.5, color=INK if c == LIME else c, fontweight="bold")
        left += v
    ax.text(total + .25, 0, f"합쳐서 {total:.1f}%", va="center", fontsize=18,
            color=INK, fontweight="bold")

    def bracket(x0, x1, y, lab, c):
        ax.plot([x0, x0, x1, x1], [y + .07, y, y, y + .07], color=c, lw=2)
        ax.text((x0 + x1) / 2, y - .14, lab, ha="center", va="top",
                fontsize=17, color=c, fontweight="bold")
    bracket(0, known, -.34, "여기까지는 누구나 살 수 있다 — 팩터로 설명되는 몫", MUTED)
    bracket(known, total, -.34, "이것만 실력", INK)
    ax.set_xlim(-.3, total + 3.2); ax.set_ylim(-1.05, .92)
    ax.set_xlabel("한 해 수익률(%)", fontsize=15)
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=13)
    fig.tight_layout()
    return save(fig, "decompose.png", EX)


# ── 조각을 늘릴수록 실력은 줄어든다 ──────────────────────────────
def alpha_shrink():
    models = ["시장 하나만\n놓고 볼 때", "크기·가치를\n더하면", "수익성·투자를\n더하면", "오르던 것까지\n더하면"]
    alpha = [4.2, 2.1, 0.9, 0.3]
    cols = [RED, AMBER, BLUE, MUTED]
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(range(4), alpha, color=cols, width=.56)
    for i, v in enumerate(alpha):
        ax.text(i, v + .12, f"{v:.1f}%", ha="center", fontsize=21,
                color=INK, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_xticks(range(4)); ax.set_xticklabels(models, fontsize=15.5)
    ax.set_ylabel("“실력”이라 부를 몫  α(%)", fontsize=15)
    ax.set_ylim(0, 5.2)
    ax.text(1.5, 4.6, "설명하는 조각을 늘릴수록 남는 몫이 줄어든다",
            ha="center", fontsize=18, color=INK, fontweight="bold")
    ax.text(1.5, 4.1, "처음에 실력처럼 보이던 것이 대부분 이미 알려진 조각이었다",
            ha="center", fontsize=15.5, color=MUTED)
    clean(ax)
    fig.tight_layout()
    return save(fig, "alpha_shrink.png",
                "같은 펀드를 서로 다른 모형으로 재봤을 때를 본뜬 예시입니다")


# ── 방향과 크기를 나눈다 (SVG) ───────────────────────────────────
def meta_label():
    b = text(800, 52, "“살까 말까”와 “얼마나 걸까”는 다른 질문이다", 30, INK, bold=True)
    b += box(90, 130, 430, 190, "첫째 모형", ["살까, 팔까", "방향만 정한다"], stroke=HAIR)
    b += arrow(548, 225, 646, 225, TEAL, "aT", 5, "그 답을 받아")
    b += box(676, 130, 430, 190, "둘째 모형", ["이 판단이 맞을 확률은?", "크게 걸까, 작게 걸까"],
             stroke=TEAL, tc=TEAL, sc=INK)
    b += arrow(1134, 225, 1216, 225, TEAL, "aT", 5)
    b += limebox(1246, 130, 280, 190, "최종 크기", ["확신만큼만"])
    b += hrule(90, 1530, 380, HAIR, 2)
    b += text(800, 440, "방향을 맞히는 일과 크기를 정하는 일을 한 모형에 맡기지 않는다",
              28, INK, bold=True)
    b += text(800, 492, "확신이 낮은 판단에 크게 걸면, 맞아도 남는 게 없다", 26, MUTED)
    b += text(800, 556, "이렇게 나눈 것을 메타 레이블링이라 부른다", 27, RED, bold=True)
    return svg("meta_label.png", b)


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$r_i\;=\;\alpha\;+\;\beta_1 f_1\;+\;\beta_2 f_2\;+\;\cdots\;+\;\varepsilon$",
                  fontsize=44, width=9.6)


if __name__ == "__main__":
    pipeline(); quantile(); what_is_factor(); factor_menu(); ff_lineage()
    decompose(); alpha_shrink(); overfit()
    meta_label(); equation()
    print("끝.")
