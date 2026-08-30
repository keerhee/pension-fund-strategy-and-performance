# -*- coding: utf-8 -*-
"""W12 프라이머의 그림 — M13 팩터 투자."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w12")
EX = "수업용으로 지어낸 예시입니다"


# ── 여섯 가지 규칙 (SVG) ─────────────────────────────────────────
def factors6():
    b = text(800, 48, "오래 살아남은 규칙 여섯 가지", 30, INK, bold=True)
    b += text(800, 88, "“이런 종목이 더 오르더라”를 규칙으로 적은 것", 26, MUTED)
    specs = [("싼 것", "값에 비해 버는 게 많은 회사"),
             ("오르던 것", "최근 잘 오른 종목이 더 오른다"),
             ("튼튼한 것", "빚 적고 꾸준히 버는 회사"),
             ("덜 흔들리는 것", "조용한 종목이 뜻밖에 낫다"),
             ("작은 것", "큰 회사보다 작은 회사가"),
             ("이자를 주는 것", "들고만 있어도 나오는 몫")]
    for i, (name, desc) in enumerate(specs):
        x = 70 + (i % 3) * 500
        y = 130 + (i // 3) * 210
        b += box(x, y, 460, 170, name, [desc], stroke=HAIR, ts=32, ss=24)
    b += text(800, 590, "여섯 다 “왜 그런가”에 답이 있어야 살아남는다", 27, RED, bold=True)
    return svg("factors6.png", b)


# ── 주식에서 자산군 전체로 (SVG) ────────────────────────────────
def widen():
    b = text(800, 46, "주식에서 배운 나누기를 자산군 전체로 넓힌다", 30, INK, bold=True)
    b += text(395, 116, "W10 — 주식 안에서", 28, MUTED, bold=True)
    b += box(90, 150, 610, 150, "종목을 팩터로 나눴다",
             ["싼 주식 − 비싼 주식", "작은 회사 − 큰 회사"], stroke=HAIR, ts=30)
    b += text(395, 356, "여기까지가 지난 주차", 26, MUTED)
    b += arrow(720, 225, 880, 225, TEAL, "aT", 6)
    b += text(800, 292, "같은 생각을", 26, TEAL, bold=True)
    b += text(1210, 116, "W12 — 자산군을 넘어", 28, TEAL, bold=True)
    b += limebox(900, 150, 620, 150, "자산군도 팩터로 나눈다",
                 ["채권·통화·원자재에서도", "같은 규칙이 통한다"])
    b += text(1210, 356, "이번 주차가 넓히는 곳", 26, TEAL)
    b += hrule(90, 1520, 410, HAIR, 2)
    b += text(800, 476, "“싼 것을 사고 비싼 것을 판다”는 주식만의 이야기가 아니다", 28, INK, bold=True)
    b += text(800, 526, "값이 붙는 것이면 무엇이든 싸고 비쌈이 있다", 27, MUTED)
    b += text(800, 588, "그래서 자산군이 아니라 팩터로 나누는 길이 열린다", 27, RED, bold=True)
    return svg("widen.png", b)


# ── 같은 팩터가 어디에나 ─────────────────────────────────────────
def everywhere():
    assets = ["주식", "채권", "통화", "원자재"]
    facs = ["가치 — 싼 것을 산다", "모멘텀 — 오르던 것을 산다", "캐리 — 이자를 더 주는 것"]
    vals = np.array([[0.34, 0.28, 0.22, 0.31],
                     [0.51, 0.43, 0.47, 0.55],
                     [0.29, 0.46, 0.58, 0.37]])
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=WIDE)
    cols = [BLUE, TEAL, AMBER]
    for j, (f, c) in enumerate(zip(facs, cols)):
        ax.bar(x + (j - 1) * .26, vals[j], .25, color=c, label=f)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xticks(x); ax.set_xticklabels(assets, fontsize=19)
    ax.set_ylabel("변동성 한 단위당 번 몫", fontsize=15)
    ax.set_ylim(0, .80)
    ax.legend(fontsize=16, frameon=False, ncol=3, loc="upper center",
              bbox_to_anchor=(.5, -.13))
    ax.text(1.5, .74, "네 자산군 어디에서도 세 규칙이 모두 살아 있다",
            ha="center", fontsize=18, color=INK, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "everywhere.png",
                "여러 자산군에서 같은 규칙이 나타난다는 연구 흐름을 본뜬 예시입니다")


# ── 나누는 축을 바꾼다 (SVG) ────────────────────────────────────
def two_axes():
    b = text(800, 46, "같은 포트폴리오를 두 가지로 나눌 수 있다", 30, INK, bold=True)
    b += text(430, 116, "자산군으로 나누면", 29, MUTED, bold=True)
    for i, (n, w, c) in enumerate([("주식", "45%", MUTED), ("채권", "35%", MUTED),
                                   ("원자재", "20%", MUTED)]):
        y = 160 + i * 120
        b += box(120, y, 620, 100, f"{n}   {w}", (), stroke=HAIR, ts=30)
    b += text(430, 570, "무엇을 샀는지만 보인다", 26, RED, bold=True)
    b += vrule(800, 100, 600, HAIR, 2)
    b += text(1180, 116, "팩터로 나누면", 29, TEAL, bold=True)
    for i, (n, w, c) in enumerate([("가치", "30%", WHITE), ("모멘텀", "40%", WHITE),
                                   ("캐리", "30%", LIME)]):
        y = 160 + i * 120
        if c == LIME:
            b += limebox(870, y, 620, 100, f"{n}   {w}")
        else:
            b += box(870, y, 620, 100, f"{n}   {w}", (), stroke=TEAL, tc=TEAL, ts=30)
    b += text(1180, 570, "어떤 위험을 졌는지가 보인다", 26, TEAL, bold=True)
    return svg("two_axes.png", b)


# ── 우연히 맞을 확률 ─────────────────────────────────────────────
def tstat():
    x = np.linspace(-5, 5, 500)
    y = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(x, y, color=INK, lw=2.6)
    ax.fill_between(x, 0, y, where=np.abs(x) >= 2, color=AMBER, alpha=.55)
    ax.fill_between(x, 0, y, where=np.abs(x) >= 3, color=RED, alpha=.85)
    ax.axvline(2, color=AMBER, lw=2.4, ls="--")
    ax.axvline(3, color=RED, lw=2.6, ls="--")
    ax.annotate("2.0 — 예전의 문턱\n우연히 넘을 확률 5%", (2, .055),
                xytext=(3.45, .355), ha="left", fontsize=16, color=AMBER,
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.6))
    ax.annotate("3.0 — 요즘 요구하는 문턱\n우연히 넘을 확률 0.3%", (3, .015),
                xytext=(3.45, .225), ha="left", fontsize=16, color=RED,
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    ax.text(-4.6, .32, "규칙이 아무 쓸모 없을 때\n나올 법한 결과의 분포",
            fontsize=16, color=MUTED)
    ax.set_xlabel("검정통계량  t", fontsize=15)
    ax.set_ylabel("그런 값이 나올 법한 정도", fontsize=15)
    ax.set_ylim(0, .46)
    clean(ax, grid=None)
    fig.tight_layout()
    return save(fig, "tstat.png", "쓸모없는 규칙도 우연히 좋아 보일 수 있다는 것을 보이는 그림입니다")


# ── 팩터 동물원 ──────────────────────────────────────────────────
def zoo():
    yrs = np.arange(1970, 2026)
    cnt = np.round(2 * np.exp((yrs - 1970) / 11.5)).astype(int)
    cnt = np.clip(cnt, 1, 420)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.fill_between(yrs, 0, cnt, color=TEAL, alpha=.25)
    ax.plot(yrs, cnt, color=TEAL, lw=4)
    for yr, lab, c in [(1993, "3개로 시작", BLUE), (2010, "수십 개", AMBER),
                       (2024, "400개 넘음", RED)]:
        i = yr - 1970
        ax.scatter([yr], [cnt[i]], s=170, color=c, zorder=5)
        ax.annotate(lab, (yr, cnt[i]), xytext=(-14, 22), textcoords="offset points",
                    ha="right", fontsize=17, color=c, fontweight="bold")
    ax.set_xlabel("발표된 해", fontsize=15)
    ax.set_ylabel("학술지에 실린 규칙의 수", fontsize=15)
    ax.text(1974, 330, "이렇게 많으면 그중 상당수는\n우연히 좋아 보였을 뿐이다",
            fontsize=17, color=RED, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "zoo.png", "규칙의 수가 늘어난 흐름을 본떠 만든 그림입니다")


# ── 발표되면 줄어든다 ────────────────────────────────────────────
def decay():
    t = np.arange(-10, 11)
    r = np.where(t < 0, 6.2, 6.2 * np.exp(-(t) / 6.0) * 0.55 + 1.2)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(t[t <= 0], r[t <= 0], color=TEAL, lw=4.4, label="논문에 실리기 전")
    ax.plot(t[t >= 0], r[t >= 0], color=RED, lw=4.4, label="논문이 나온 뒤")
    ax.axvline(0, color=INK, lw=2, ls="--")
    ax.text(.4, 6.4, "여기서 세상에 알려진다", fontsize=17, color=INK, fontweight="bold")
    ax.annotate("절반 넘게 사라진다", (7, r[17]), xytext=(0, 40),
                textcoords="offset points", ha="center", fontsize=18,
                color=RED, fontweight="bold")
    ax.set_xlabel("논문이 나온 해로부터 지난 햇수", fontsize=15)
    ax.set_ylabel("그 규칙이 해마다 벌어 준 몫(%)", fontsize=15)
    ax.set_ylim(0, 7.6)
    ax.legend(fontsize=16, frameon=False, loc="lower left")
    clean(ax)
    fig.tight_layout()
    return save(fig, "decay.png", "발표 뒤 성과가 줄어드는 흐름을 본떠 만든 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$t\;=\;\frac{\bar{r}}{s\,/\,\sqrt{n}}$", fontsize=48, width=5.6)


if __name__ == "__main__":
    widen(); everywhere(); two_axes(); factors6(); tstat(); zoo()
    decay(); equation()
    print("끝.")
