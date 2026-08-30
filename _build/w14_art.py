# -*- coding: utf-8 -*-
"""W14 프라이머의 그림 — M15 대체투자와 비유동성 · SS3 세금 효율 투자."""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w14")
EX = "수업용으로 지어낸 예시입니다"


# ── J 커브 ───────────────────────────────────────────────────────
def jcurve():
    yrs = np.arange(0, 13)
    cf = np.array([-18, -26, -22, -12, -2, 8, 18, 26, 30, 26, 18, 10, 4])
    cum = np.cumsum(cf)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(yrs, cf, color=[RED if v < 0 else TEAL for v in cf], width=.58, alpha=.85)
    ax.plot(yrs, cum, color=INK, lw=4, marker="o", ms=7, label="여기까지 쌓인 돈")
    ax.axhline(0, color=INK, lw=1.4)
    ax.annotate("처음 몇 해는 넣기만 한다", (2, cum[2]), xytext=(10, -46),
                textcoords="offset points", fontsize=17, color=RED, fontweight="bold")
    ax.annotate("나중에야 돌려받기 시작한다", (9, cum[9]), xytext=(-16, 18),
                textcoords="offset points", ha="right", fontsize=17,
                color=TEAL, fontweight="bold")
    ax.set_xlabel("펀드에 들어간 뒤 지난 햇수", fontsize=15)
    ax.set_ylabel("그해 오간 돈 · 쌓인 돈", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    clean(ax)
    fig.tight_layout()
    return save(fig, "jcurve.png", EX)


# ── 안 흔들려 보이는 이유 ────────────────────────────────────────
def smoothing():
    rng = np.random.default_rng(15)
    n = 60
    true = 100 * np.cumprod(1 + rng.normal(.008, .052, n))
    rep = true.copy()
    for i in range(1, n):
        rep[i] = .68 * rep[i - 1] + .32 * true[i]     # 천천히 반영한다
    t = np.arange(n) / 4
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1.4, 1]})
    ax = axes[0]
    ax.plot(t, true, color=MUTED, lw=2.2, label="실제로 오간 값")
    ax.plot(t, rep, color=TEAL, lw=4, label="장부에 적힌 값")
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("100으로 시작한 값", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    ax.set_title("값을 자주 안 매기면 매끄러워 보인다", fontsize=18, color=INK, pad=12)
    clean(ax)

    ax = axes[1]
    v = [np.diff(np.log(true)).std() * 200, np.diff(np.log(rep)).std() * 200]
    ax.bar([0, 1], v, color=[MUTED, RED], width=.55)
    for i, x in enumerate(v):
        ax.text(i, x + .3, f"{x:.1f}%", ha="center", fontsize=21,
                color=INK, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["실제", "장부"], fontsize=17)
    ax.set_ylabel("변동성(%)", fontsize=15)
    ax.set_title("절반으로 줄어 보인다", fontsize=18, color=RED, pad=12)
    clean(ax)
    fig.tight_layout()
    return save(fig, "smoothing.png", "값을 천천히 반영할 때 무슨 일이 생기는지를 보이는 예시입니다")


# ── 유동성이란 (SVG) ─────────────────────────────────────────────
def liquidity():
    b = text(800, 48, "“팔고 싶을 때 팔 수 있는가”", 30, INK, bold=True)
    specs = [("예금", "오늘 당장", 100, TEAL),
             ("상장 주식", "이틀이면", 82, TEAL),
             ("회사채", "며칠에서 몇 주", 55, AMBER),
             ("부동산", "몇 달", 26, RED),
             ("사모펀드", "10년 뒤에나", 8, RED)]
    for i, (name, when, w, c) in enumerate(specs):
        y = 118 + i * 92
        b += text(210, y + 34, name, 28, INK, "end", True)
        b += f'<rect x="250" y="{y}" width="{w*10}" height="48" rx="8" fill="{c}"/>'
        b += text(250 + w * 10 + 20, y + 34, when, 26, MUTED, "start")
    b += text(1180, 300, "여기서 더 받는 몫이", 27, INK, "start", True)
    b += text(1180, 344, "“못 파는 값”이다", 27, RED, "start", True)
    b += text(1180, 410, "다만 그 값이 정말", 25, MUTED, "start")
    b += text(1180, 448, "충분한지는 따져야 한다", 25, MUTED, "start")
    return svg("liquidity.png", b)


# ── 세금을 떼면 ──────────────────────────────────────────────────
def after_tax():
    labels = ["그냥 계좌\n해마다 세금", "연금 계좌\n나중에 한 번"]
    yrs = 20
    r = .06
    taxed = 100 * (1 + r * (1 - .154)) ** yrs
    deferred = 100 * (1 + r) ** yrs
    deferred_net = 100 + (deferred - 100) * (1 - .154)
    fig, axes = plt.subplots(1, 2, figsize=WIDE,
                             gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    t = np.arange(yrs + 1)
    ax.plot(t, 100 * (1 + r * (1 - .154)) ** t, color=AMBER, lw=4,
            label="해마다 세금을 떼면")
    ax.plot(t, 100 * (1 + r) ** t, color=TEAL, lw=4, label="나중에 한 번만 떼면")
    ax.set_xlabel("햇수", fontsize=15)
    ax.set_ylabel("100으로 시작한 돈", fontsize=15)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    ax.set_title("같은 수익률인데도 갈라진다", fontsize=18, color=INK, pad=12)
    clean(ax)

    ax = axes[1]
    v = [taxed, deferred_net]
    ax.bar([0, 1], v, color=[AMBER, LIME], width=.55,
           edgecolor=["none", INK], linewidth=1.4)
    for i, x in enumerate(v):
        ax.text(i, x + 4, f"{x:.0f}", ha="center", fontsize=22,
                color=INK, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(labels, fontsize=15.5)
    ax.set_ylabel("세금 떼고 손에 남는 돈", fontsize=15)
    ax.set_ylim(0, max(v) * 1.2)
    ax.set_title(f"20년 뒤 {v[1]-v[0]:.0f}만큼 차이", fontsize=18,
                 color=TEAL, pad=12, fontweight="bold")
    clean(ax)
    fig.tight_layout()
    return save(fig, "after_tax.png",
                "해마다 6%씩 벌고 세율은 15.4%로 놓은 예시입니다")


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$r_{net}\;=\;r\,\times\,(1-\tau)$", fontsize=48, width=6.6)


if __name__ == "__main__":
    jcurve(); smoothing(); liquidity(); after_tax(); equation()
    print("끝.")
