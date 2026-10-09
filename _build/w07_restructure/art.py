# -*- coding: utf-8 -*-
"""W07 강의본 재구성(2026-10-07) 그림.
  loss_freq      기간별 손실 기간 비율 — 미국 주식 1926~2017 (Morningstar 2018 Fundamentals for Investors 수치)
  sp500_h / kospi_h  투자 기간별 연환산 수익률 최고·평균·최저 (삼성자산운용 Winning Investment 수치)
  rebal_1926 / rebal_1990  60:40 매월 리밸런싱 vs 매수후보유 — Shiller 월별 자료로 재계산
  bands          리밸런싱 밴드 — 단일 밴드 · 이중 밴드 (개념도, 모의 경로)
  binom          이항 예제의 만기 부 — 매수후보유(선형) vs 리밸런싱(오목)
실행: <pandas·xlrd 있는 파이썬> _build/w07_restructure/art.py
"""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "art"); os.makedirs(OUT, exist_ok=True)
FONT = os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc")
fm.fontManager.addfont(FONT)
plt.rcParams["font.family"] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False
NAVY, GRAY, ORANGE, GREEN, RED, BLUE = "#1B2C5E", "#9AA3AF", "#E8A04C", "#2E9E6B", "#C0392B", "#3B6FB6"

def clean(ax, grid="y"):
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_color("#9AA3AF")
    if grid: ax.grid(axis=grid, color="#E5E7EB", lw=0.8); ax.set_axisbelow(True)
    ax.tick_params(colors="#374151", labelsize=11)

def save(fig, name):
    p = os.path.join(OUT, name); fig.savefig(p, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08); plt.close(fig); print(p)

# 1 ── 기간별 손실 기간 비율 ─────────────────────────────────────────
def loss_freq():
    hz = ["1년", "5년(연환산)", "15년(연환산)"]; loss = [26, 14, 0]
    fig, ax = plt.subplots(figsize=(8.6, 3.3))
    y = np.arange(3)[::-1]
    ax.barh(y, [100 - l for l in loss], color=GREEN, height=.55, label="이익 난 기간")
    ax.barh(y, loss, left=[100 - l for l in loss], color=RED, height=.55, label="손실 난 기간")
    for yi, l in zip(y, loss):
        ax.text(50 - l / 2, yi, f"이익 {100-l}%", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
        if l: ax.text(100 - l / 2, yi, f"손실 {l}%", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
        else: ax.text(101.5, yi, "손실 0%", ha="left", va="center", color=RED, fontsize=13, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(hz, fontsize=13)
    ax.set_xlim(0, 112); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    clean(ax, grid="x")
    ax.set_title("미국 주식 1926~2017 — 보유 기간이 길수록 손실 난 기간의 비율이 줄어든다", fontsize=13, color=NAVY, loc="left")
    save(fig, "loss_freq.png")

# 2 ── 기간별 수익률 범위 ───────────────────────────────────────────
def horizon(name, title, mx, av, mn, ylim, col):
    hz = ["1년", "5년", "10년", "15년", "20년", "25년"]; x = np.arange(6)
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    ax.bar(x, np.array(mx) - np.array(mn), bottom=mn, width=.55, color=col, alpha=.85, label="최고~최저 범위")
    ax.scatter(x, av, marker="D", s=46, color="white", edgecolor=NAVY, zorder=3, label="평균")
    for xi, a, b, c in zip(x, mx, av, mn):
        ax.text(xi, a + ylim[1] * .02, f"{a:.1f}", ha="center", va="bottom", fontsize=11, color=NAVY)
        ax.text(xi, c - ylim[1] * .02, f"{c:.1f}", ha="center", va="top", fontsize=11, color=RED if c < 0 else GREEN)
        ax.text(xi + .32, b, f"{b:.1f}", ha="left", va="center", fontsize=10, color="#374151")
    ax.axhline(0, color="#374151", lw=.9)
    ax.set_xticks(x); ax.set_xticklabels(hz, fontsize=12); ax.set_ylim(*ylim); ax.set_ylabel("연환산 수익률(%)", fontsize=11)
    ax.legend(frameon=False, fontsize=11, loc="upper right")
    clean(ax); ax.set_title(title, fontsize=13, color=NAVY, loc="left")
    save(fig, name)

# 3 ── 60:40 리밸런싱 vs 매수후보유 (Shiller) ─────────────────────────
def shiller():
    x = pd.read_excel(os.path.join(HERE, "shiller_ie_data_2023-09.xls"), sheet_name="Data", header=None, skiprows=8)
    x = x.iloc[:, [0, 4, 9, 18]]; x.columns = ["date", "cpi", "stk_real_tr", "bnd_real_tr"]
    x = x[pd.to_numeric(x["date"], errors="coerce").notna()].astype(float)
    x["stk"] = x["stk_real_tr"] * x["cpi"]; x["bnd"] = x["bnd_real_tr"] * x["cpi"]   # 명목 총수익 지수
    x["ym"] = (x["date"] * 100).round().astype(int)
    return x.set_index("ym")

def rebal(df, a, b, name, title, xt):
    d = df.loc[a:b]; rs = d["stk"].pct_change().fillna(0).values; rb = d["bnd"].pct_change().fillna(0).values
    n = len(d); w0 = .6
    S = np.cumprod(1 + rs); B = np.cumprod(1 + rb)
    R = np.ones(n)
    for t in range(1, n): R[t] = R[t - 1] * (1 + w0 * rs[t] + (1 - w0) * rb[t])
    BH = w0 * S + (1 - w0) * B; wBH = w0 * S / BH
    t = np.arange(n)
    fig, axs = plt.subplots(1, 2, figsize=(11.6, 3.7), gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axs[0]
    ax.plot(t, S, color=ORANGE, lw=1.4, label="주식 100%"); ax.plot(t, B, color=GRAY, lw=1.4, label="국채 100%")
    ax.plot(t, R, color=NAVY, lw=2.2, label="60:40 매월 리밸런싱"); ax.plot(t, BH, color=BLUE, lw=1.4, ls="--", label="60:40 매수후보유")
    ax.set_xticks([i for i, ym in enumerate(d.index) if ym % 100 == 1 and (ym // 100) % xt == 0])
    ax.set_xticklabels([str(ym // 100) for ym in d.index if ym % 100 == 1 and (ym // 100) % xt == 0])
    ax.legend(frameon=False, fontsize=10, loc="upper left"); clean(ax); ax.set_title("A. 1달러의 성장(명목 총수익)", fontsize=12, color=NAVY, loc="left")
    ax = axs[1]
    ax.plot(t, wBH * 100, color=BLUE, lw=1.6, ls="--", label="매수후보유 — 비중이 표류"); ax.plot(t, np.full(n, 60), color=NAVY, lw=2.2, label="리밸런싱 — 60% 유지")
    ax.set_ylim(0, 100); ax.set_ylabel("주식 비중(%)", fontsize=11)
    ax.set_xticks(axs[0].get_xticks()); ax.set_xticklabels([l.get_text() for l in axs[0].get_xticklabels()])
    ax.legend(frameon=False, fontsize=10, loc="lower left"); clean(ax); ax.set_title("B. 주식 비중", fontsize=12, color=NAVY, loc="left")
    fig.suptitle(title, fontsize=13, color=NAVY, x=0.01, ha="left", y=1.02)
    fig.tight_layout(); save(fig, name)
    yrs = (n - 1) / 12
    ann = lambda v: (v[-1] ** (1 / yrs) - 1) * 100
    vol = lambda r: r[1:].std() * np.sqrt(12) * 100
    rR = np.diff(R) / R[:-1]; rBH = np.diff(BH) / BH[:-1]
    return dict(period=f"{a}-{b}", R_ann=ann(R), BH_ann=ann(BH), S_ann=ann(S), B_ann=ann(B),
                R_vol=rR.std() * np.sqrt(12) * 100, BH_vol=rBH.std() * np.sqrt(12) * 100,
                w_min=wBH.min() * 100, w_max=wBH.max() * 100, w_end=wBH[-1] * 100,
                R_end=R[-1], BH_end=BH[-1])

# 4 ── 밴드 개념도 ──────────────────────────────────────────────────
def bands():
    rng = np.random.default_rng(7); n = 60
    fig, axs = plt.subplots(1, 2, figsize=(11.2, 3.3))
    for k, ax in enumerate(axs):
        w = [60.0]; trades = []
        for t in range(1, n):
            v = w[-1] + rng.normal(0, 1.9)
            if k == 0 and abs(v - 60) > 5: trades.append((t, v)); v = 60.0
            if k == 1 and abs(v - 60) > 6: trades.append((t, v)); v = 60 + np.sign(v - 60) * 3
            w.append(v)
        ax.plot(range(n), w, color=NAVY, lw=1.6)
        for t, v in trades: ax.plot([t, t], [v, w[t]], color=RED, lw=1.4); ax.scatter([t], [v], color=RED, s=18, zorder=3)
        ax.axhline(60, color=GREEN, lw=1.4)
        if k == 0:
            for b in (55, 65): ax.axhline(b, color=GRAY, lw=1.2, ls="--")
            ax.text(n - .5, 65.4, "밴드 65%", fontsize=10, color="#374151", ha="right"); ax.text(n - .5, 60.4, "목표 60%", fontsize=10, color=GREEN, ha="right")
            ax.set_title("A. 단일 밴드 — 밴드를 벗어나면 목표로 되돌린다", fontsize=12, color=NAVY, loc="left")
        else:
            for b in (54, 66): ax.axhline(b, color=GRAY, lw=1.2, ls="--")
            for b in (57, 63): ax.axhline(b, color=ORANGE, lw=1.1, ls=":")
            ax.text(n - .5, 66.4, "바깥 밴드 66%", fontsize=10, color="#374151", ha="right"); ax.text(n - .5, 63.4, "안쪽 밴드 63%", fontsize=10, color="#B45309", ha="right")
            ax.set_title("B. 이중 밴드 — 바깥 밴드를 벗어나면 안쪽 밴드까지만", fontsize=12, color=NAVY, loc="left")
        ax.set_ylim(48, 72); ax.set_xticks([]); ax.set_ylabel("주식 비중(%)", fontsize=10); clean(ax)
    fig.tight_layout(); save(fig, "bands.png")

# 5 ── 이항 예제 만기 부 ─────────────────────────────────────────────
def binom():
    S = [0.25, 1, 4]; BH = [0.6340, 1.0840, 2.8840]; RB = [0.5476, 1.2136, 2.6896]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(S, BH, color=BLUE, lw=1.8, ls="--", marker="o", label="매수후보유 — 주가에 선형")
    ax.plot(S, RB, color=NAVY, lw=2.4, marker="s", label="리밸런싱 — 오목(변동성 매도)")
    pos = {0.25: ((.12, .02), (.12, -.17)), 1: ((.12, -.2), (-.12, .12)), 4: ((-.12, .1), (-.12, -.25))}
    for s, a, b in zip(S, BH, RB):
        (dxa, dya), (dxb, dyb) = pos[s]
        ax.text(s + dxa, a + dya, f"{a:.4f}", fontsize=10, color=BLUE, ha="left" if dxa > 0 else "right")
        ax.text(s + dxb, b + dyb, f"{b:.4f}", fontsize=10, color=NAVY, ha="left" if dxb > 0 else "right")
    ax.set_xlabel("2기 말 주가", fontsize=11); ax.set_ylabel("2기 말 부", fontsize=11)
    ax.set_xticks(S); ax.legend(frameon=False, fontsize=10, loc="upper left"); clean(ax)
    save(fig, "binom.png")

if __name__ == "__main__":
    loss_freq()
    horizon("sp500_h.png", "S&P 500 (1950.1~2020.12) — 평균은 10%대 그대로, 범위는 기간이 길수록 좁아진다",
            [72.1, 31.9, 20.0, 20.0, 18.6, 17.4], [12.5, 11.1, 10.6, 10.4, 10.5, 10.8], [-47.5, -8.2, -4.5, 3.4, 3.9, 7.2], (-68, 85), BLUE)
    horizon("kospi_h.png", "KOSPI (1980.1~2020.12) — 15년이면 최저 −0.9%, 20년이면 최저도 플러스",
            [236.2, 51.5, 25.0, 16.6, 13.0, 12.9], [13.6, 10.5, 7.2, 8.3, 7.8, 8.0], [-64.5, -17.8, -8.6, -0.9, 1.6, 3.3], (-100, 270), ORANGE)
    df = shiller()
    print(rebal(df, 192512, 194012, "rebal_1926.png", "1926~1940 — 대공황을 지나며 리밸런싱은 하락한 주식을 사들였다", 2))
    print(rebal(df, 198912, 201112, "rebal_1990.png", "1990~2011 — 닷컴 붕괴와 금융위기에도 60:40을 지켰다", 3))
    bands(); binom()

# 6 ── 장기 주식 저성과 보험 (Bodie 1995 식으로 다시 그림) ─────────────
def bodie():
    from math import erf, sqrt
    N = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
    sig = 0.1908                       # 30년 보험료 0.399가 되는 σ (원문 정상 상태 19%)
    m = 0.2019 * sig                   # 1년 승률 58% → z = 0.2019
    T = np.linspace(0.25, 100, 400)
    P = [N(m * sqrt(t) / sig) for t in T]; C = [2 * N(sig * sqrt(t) / 2) - 1 for t in T]
    fig, axs = plt.subplots(1, 2, figsize=(11.2, 3.2))
    axs[0].plot(T, P, color=NAVY, lw=2.2); axs[0].scatter([1, 30], [N(m / sig), N(m * sqrt(30) / sig)], color=RED, zorder=3)
    axs[0].text(3, N(m / sig) - .03, "1년 58%", fontsize=11, color=RED)
    axs[0].text(31, N(m * sqrt(30) / sig) - .05, "30년 86%", fontsize=11, color=RED)
    axs[0].set_ylim(.5, 1); axs[0].set_title("A. 주식이 채권을 이길 확률", fontsize=12, color=NAVY, loc="left")
    axs[1].plot(T, C, color=ORANGE, lw=2.2); axs[1].scatter([30], [2 * N(sig * sqrt(30) / 2) - 1], color=RED, zorder=3)
    axs[1].text(32, 2 * N(sig * sqrt(30) / 2) - 1 - .05, f"30년 {2*N(sig*sqrt(30)/2)-1:.3f}", fontsize=11, color=RED)
    axs[1].set_ylim(0, .7); axs[1].set_title("B. 1달러를 보장하는 풋옵션 값", fontsize=12, color=NAVY, loc="left")
    for ax in axs: ax.set_xlabel("투자 기간(년)", fontsize=11); clean(ax)
    fig.tight_layout(); save(fig, "bodie.png")

if __name__ == "__main__":
    bodie()

# 7 ── 강화학습 도입: 에이전트–환경 루프 · RL 대 IRL (보강 3-2 4~6쪽을 강의본 색으로) ──
def _box(ax, x, y, w, h, fc, title, sub, tc="white", fs=17):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec="none"))
    ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold")
    if sub: ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=11.5, color=tc)

def _arrow(ax, x0, y0, x1, y1, c, lab, dy=0.12):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2, mutation_scale=18))
    ax.text((x0 + x1) / 2, y0 + dy, lab, ha="center", va="bottom", fontsize=13, color=c, fontweight="bold")

def rl_loop():
    fig, ax = plt.subplots(figsize=(11.6, 3.4)); ax.set_xlim(0, 11.6); ax.set_ylim(0, 3.4); ax.axis("off")
    _box(ax, 0.2, 0.45, 2.8, 2.5, NAVY, "에이전트", "정책 π(a | s)\n트레이더 · 운용역 · 기금")
    _box(ax, 6.6, 0.45, 2.8, 2.5, GREEN, "환경", "시장 + 포트폴리오\n관측 · 부분 관측")
    _box(ax, 9.7, 0.95, 1.7, 1.5, "#EAF1FB", "오프라인", "과거 데이터가\n환경을 대신", tc=NAVY, fs=13)
    _arrow(ax, 3.1, 2.55, 6.5, 2.55, NAVY, r"행동 $a_t$ : 목표 비중 · 주문")
    _arrow(ax, 6.5, 1.7, 3.1, 1.7, GREEN, r"다음 상태 $s_{t+1}$")
    _arrow(ax, 6.5, 0.85, 3.1, 0.85, RED, r"보상 $r_{t+1}$ = 피드백")
    ax.annotate("", xy=(9.45, 1.7), xytext=(9.7, 1.7), arrowprops=dict(arrowstyle="-|>", color="#6B7280", lw=1.6))
    ax.text(5.8, 0.12, "목표: 누적 보상의 기대값을 최대화 — 지도 · 비지도학습에는 없는 피드백 루프", ha="center", fontsize=11.5, color="#374151")
    save(fig, "rl_loop.png")

def rl_irl():
    fig, ax = plt.subplots(figsize=(11.6, 3.2)); ax.set_xlim(0, 11.6); ax.set_ylim(0, 3.2); ax.axis("off")
    for y, lab, c, items in ((1.85, "RL", NAVY, [("보상 함수 + 환경", "무엇을 원하는지 안다"), ("최적화", "벨만 · Q-learning"), ("최적 정책 · 행동", "어떻게 행동할지")]),
                             (0.45, "IRL", RED, [("상태 · 행동 기록", "시연 · 거래 이력"), ("추론", "MaxEnt · T-REX · GIRL"), ("보상 함수 (효용)", "왜 그렇게 행동했나")])):
        ax.text(0.45, y + 0.5, lab, ha="center", va="center", fontsize=20, color=c, fontweight="bold")
        for k, (t, sub) in enumerate(items):
            x = 1.1 + k * 3.55
            _box(ax, x, y, 2.9, 1.0, [GREEN, NAVY, "#B7D7F0"][k], t, sub, tc=("white" if k < 2 else NAVY), fs=15)
            if k < 2: ax.annotate("", xy=(x + 3.5, y + 0.5), xytext=(x + 2.95, y + 0.5), arrowprops=dict(arrowstyle="-|>", color="#374151", lw=1.8))
    ax.text(5.8, 0.05, "같은 MDP를 놓고 질문의 방향만 뒤집는다 — IRL의 보상은 일반적으로 유일하지 않다", ha="center", fontsize=11.5, color="#374151")
    save(fig, "rl_irl.png")

if __name__ == "__main__":
    rl_loop(); rl_irl()
