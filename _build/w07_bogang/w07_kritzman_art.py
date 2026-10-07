# -*- coding: utf-8 -*-
"""W07 보강 1 스페셜 — 국면 기반 TDF (Kritzman, 2017) 그림.

실행: python w07_kritzman_art.py  →  _art/w07kr/
원문 Exhibit 1·3·5는 식 (1)·(3)으로 다시 계산해 일치를 확인했다.
Exhibit 8·11은 원문 표의 값을 옮겨 그린다. 터뷸런스·흡수비율 도해는 수업용 가상 자료다.
"""
import math
import numpy as np
from statistics import NormalDist
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from primer_lib import (out_dir, save, clean, fig, equation, svg, arrow, text,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK, WIDE)

OUT = out_dir("w07kr")
ND = NormalDist()
Z05 = ND.inv_cdf(0.05)


def bx(x, y, w, h, title, sub=(), kind="white", ts=36, ss=28):
    fill, stroke, tc, sc = {"white": (WHITE, HAIR, INK, MUTED), "teal": (WHITE, TEAL, INK, MUTED),
                            "lime": (LIME, INK, DARK, DARK), "dark": (DARK, DARK, LIME, "#9FB0B2")}[kind]
    n = len(sub)
    top = y + (h - (ts + 14 + n * (ss + 12))) / 2 + ts
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="{3 if kind != "white" else 2}"/>'
         f'<text x="{x+w/2}" y="{top}" font-size="{ts}" font-weight="700" fill="{tc}" '
         f'text-anchor="middle">{title}</text>')
    for i, ln in enumerate(sub):
        s += (f'<text x="{x+w/2}" y="{top + 14 + (i+1)*(ss+12) - 4}" font-size="{ss}" fill="{sc}" '
              f'text-anchor="middle">{ln}</text>')
    return s


def ploss(mu, sig, T, L=0.0):
    return ND.cdf((math.log(1 + L) * T - mu * T) / (sig * math.sqrt(T)))


def wmax(muR, muS, sig, T, p=0.05):
    """손실확률 p 이하를 지키는 최대 위험자산 비중 — 식 (3), [0, 1]로 자른다."""
    best = 0.0
    for w in np.linspace(0, 1, 1001):
        m = w * muR + (1 - w) * muS
        s = w * sig
        pr = 0.0 if s == 0 else ND.cdf((-m * T) / (s * math.sqrt(T)))
        if pr <= p:
            best = w
    return best


# ── 손실확률과 연환산 변동성 (Exhibit 1) ─────────────────────────
def loss_curve():
    T = np.linspace(1, 30, 300)
    p = [ploss(0.075, 0.21, t) * 100 for t in T]
    sd = 21 / np.sqrt(T)
    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE)
    a1.plot(T, sd, color=INK, lw=3)
    a1.set_title("연환산 변동성 σ/√T (%)", fontsize=16, loc="left")
    a2.plot(T, p, color=RED, lw=3.2)
    a2.set_title("기간 말 손실확률 (%)", fontsize=16, loc="left")
    for t, ax, fn in ((1, a1, lambda t: 21 / math.sqrt(t)), (5, a1, lambda t: 21 / math.sqrt(t)),
                      (20, a1, lambda t: 21 / math.sqrt(t))):
        ax.plot([t], [fn(t)], "o", color=INK, ms=8)
        ax.text(t + 0.8, fn(t) + 0.6, f"{t}년 {fn(t):.1f}%", fontsize=14, color=INK)
    for t in (1, 5, 20):
        v = ploss(0.075, 0.21, t) * 100
        a2.plot([t], [v], "o", color=RED, ms=8)
        a2.text(t + 0.8, v + 1.0, f"{t}년 {v:.1f}%", fontsize=14, color=RED)
    for ax in (a1, a2):
        ax.set_xlabel("남은 투자기간 T (년)", fontsize=14); clean(ax); ax.set_xlim(0, 31)
    a1.set_ylim(0, 25); a2.set_ylim(0, 42)
    f.tight_layout(w_pad=4)
    save(f, "loss_curve.png", note="위험자산 μ 7.5%(연속) · σ 21% — 원문 Exhibit 1 재계산")


# ── 손실확률 5%를 지키는 글라이드패스와 국면 ──────────────────────
def regime_gp():
    T = np.arange(1, 31)
    f, ax = fig()
    for sig, c_, lab, lw in ((0.14, TEAL, "평온 국면 σ 14%", 2.6), (0.21, INK, "평균 σ 21% (원문)", 3.4),
                             (0.28, RED, "취약 국면 σ 28%", 2.6)):
        w = [wmax(0.075, 0.025, sig, t) * 100 for t in T]
        ax.plot(T, w, color=c_, lw=lw)
    ax.text(9.5, 90, "평온 국면 σ 14%", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(17.5, 60, "평균 σ 21% (원문)", fontsize=15, color=INK, fontweight="bold")
    ax.text(27, 40, "취약 국면 σ 28%", fontsize=15, color=RED, fontweight="bold")
    for t, v in ((20, 91.8), (10, 42.2), (1, 8.5)):
        ax.plot([t], [v], "o", color=INK, ms=8)
        ax.text(t + 0.4, v - 6, f"{v}%", fontsize=14, color=INK)
    ax.invert_xaxis(); ax.set_xlim(31, 0); ax.set_ylim(0, 105)
    ax.set_xlabel("남은 투자기간 T (년) — 오른쪽으로 갈수록 목표일", fontsize=14)
    ax.set_ylabel("위험자산 비중 W_R (%)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    ax.text(30, 4, "", fontsize=1)
    save(f, "regime_gp.png", note="손실확률 ≤ 5% · 위험자산 μ 7.5% · 안전자산 2.5% — 점은 원문 Exhibit 3")


# ── 60/40의 손실확률은 국면에 달려 있다 (Exhibit 5) ────────────────
def regime_loss():
    T = [1, 5, 10, 15, 20]
    f, ax = fig()
    xs = np.arange(len(T))
    for k, (sig, c_, lab) in enumerate(((0.033, TEAL, "저위험 국면 σ 3.3% (2007.5)"),
                                        (0.08, MUTED, "전체 평균 σ 8.0%"),
                                        (0.186, RED, "고위험 국면 σ 18.6% (2009.8)"))):
        v = [ploss(0.0794, sig, t) * 100 for t in T]
        bars = ax.bar(xs + (k - 1) * 0.27, v, width=0.26, color=c_, label=lab)
        for b, x in zip(bars, v):
            if x >= 0.05:
                ax.text(b.get_x() + b.get_width() / 2, x + 0.6, f"{x:.1f}", ha="center", fontsize=12)
    ax.set_xticks(xs); ax.set_xticklabels([f"{t}년" for t in T], fontsize=15)
    ax.set_ylabel("60/40의 기간 말 손실확률 (%)", fontsize=14)
    ax.legend(fontsize=13, frameon=False, loc="upper right")
    clean(ax); ax.set_ylim(0, 38)
    save(f, "regime_loss.png", note="기대수익 7.94% · 원문 Exhibit 5를 식 (1)로 재계산")


# ── 터뷸런스 — 마할라노비스 거리 ─────────────────────────────────
def turbulence_demo():
    rng = np.random.default_rng(3)
    S = np.array([[16, 6.4], [6.4, 4]])
    X = rng.multivariate_normal([0, 0], S, 600)
    f, ax = fig(size=(12.9, 5.0))
    ax.scatter(X[:, 0], X[:, 1], s=10, color=MUTED, alpha=0.35)
    vals, vecs = np.linalg.eigh(S)
    ang = math.degrees(math.atan2(vecs[1, 1], vecs[0, 1]))
    for k, a in ((1, 0.9), (2, 0.6), (3, 0.35)):
        ax.add_patch(Ellipse((0, 0), 2 * k * math.sqrt(vals[1]), 2 * k * math.sqrt(vals[0]), angle=ang,
                             fill=False, ec=TEAL, lw=2, alpha=a))
    ax.plot([4], [2], "o", color=TEAL, ms=14)
    ax.plot([4], [-2], "o", color=RED, ms=14)
    ax.text(4.5, 2.3, "A (+4%, +2%) → 터뷸런스 0.56", fontsize=16, color=TEAL, fontweight="bold")
    ax.text(4.5, -2.6, "B (+4%, −2%) → 터뷸런스 5.0", fontsize=16, color=RED, fontweight="bold")
    ax.axhline(0, color=HAIR, lw=1); ax.axvline(0, color=HAIR, lw=1)
    ax.set_xlim(-14, 16); ax.set_ylim(-7, 7)
    ax.set_xlabel("자산 1 월간 초과수익 (%) · σ 4%", fontsize=14)
    ax.set_ylabel("자산 2 (%) · σ 2%", fontsize=14)
    clean(ax, grid=None); ax.tick_params(labelsize=13)
    ax.text(-13.5, 5.8, "상관 0.8 — 두 자산은 보통 같은 방향으로 움직인다", fontsize=15, color=MUTED)
    save(f, "turbulence_demo.png", note="수업용 가상 자료 — 타원은 마할라노비스 거리 1·2·3")


# ── 흡수비율 — 고유값 막대 ────────────────────────────────────────
def absorption_demo():
    N, n = 10, 2
    f, axes = plt.subplots(1, 2, figsize=WIDE, sharey=True)
    for ax, rho, c_, lab in ((axes[0], 0.2, TEAL, "느슨한 시장 — 평균 상관 0.2"),
                             (axes[1], 0.7, RED, "결합된 시장 — 평균 상관 0.7")):
        C = np.full((N, N), rho); np.fill_diagonal(C, 1.0)
        ev = np.sort(np.linalg.eigvalsh(C))[::-1]
        ar = ev[:n].sum() / ev.sum()
        cols = [c_] * n + [HAIR] * (N - n)
        ax.bar(np.arange(1, N + 1), ev / ev.sum() * 100, color=cols)
        ax.set_title(f"{lab}", fontsize=15, loc="left")
        ax.text(5.2, 60, f"AR (상위 {n}개) = {ar*100:.0f}%", fontsize=17, color=c_, fontweight="bold")
        ax.set_xlabel("고유벡터 순위", fontsize=13); clean(ax); ax.set_xticks(range(1, N + 1))
    axes[0].set_ylabel("전체 분산 중 비중 (%)", fontsize=14); axes[0].set_ylim(0, 80)
    f.tight_layout(w_pad=3)
    save(f, "absorption_demo.png", note="수업용 가상 자료 — 자산 10개, 같은 상관")


# ── 국면 민감 TDF의 판단 흐름 ─────────────────────────────────────
def flow():
    b = ""
    b += bx(10, 70, 330, 200, "① 터뷸런스", ["10개 지수 · EWMA 0.97", "252일 z-점수"])
    b += bx(10, 300, 330, 200, "② 흡수비율", ["GICS 3 업종 · 500일", "(15일 − 252일) z"])
    b += arrow(345, 170, 420, 270); b += arrow(345, 400, 420, 300)
    b += bx(430, 180, 330, 220, "③ 국면 판정", ["둘 다 z ≥ 1", "→ 취약, 아니면 평상"], kind="teal")
    b += arrow(765, 290, 830, 290)
    b += bx(840, 180, 330, 220, "④ 공분산 선택", ["과거 취약기 Σ_F", "또는 평상기 Σ_N"], kind="teal")
    b += arrow(1175, 290, 1240, 290)
    b += bx(1250, 160, 340, 260, "⑤ 비중 결정", ["손실확률 ≤ 5%에서", "기대수익 최대", "남은 기간 T 반영"], kind="lime")
    b += text(800, 560, "국면이 바뀔 때와 매년 초에 재배분 · 재배분 뒤 10거래일 거래 금지(회전율 관리)", 28, MUTED)
    svg("flow.png", b, w=1600, h=600)


# ── 재배분 이력 (Exhibit 8) ───────────────────────────────────────
EX8 = [("2003-01-02", 82.00, 82.00), ("2004-01-02", 82.00, 82.00), ("2005-01-03", 82.00, 82.00),
       ("2006-01-03", 82.00, 82.00), ("2007-01-03", 82.00, 82.00), ("2007-08-21", 82.00, 42.47),
       ("2007-10-18", 82.00, 82.00), ("2007-11-13", 82.00, 41.86), ("2008-01-02", 81.87, 40.46),
       ("2008-05-13", 81.87, 81.87), ("2008-07-18", 82.00, 41.68), ("2008-08-08", 82.00, 82.00),
       ("2008-09-09", 82.00, 42.31), ("2009-01-02", 80.70, 21.24), ("2009-02-12", 80.79, 80.79),
       ("2010-01-04", 50.24, 50.24), ("2011-01-03", 28.81, 28.81), ("2011-08-29", 28.48, 21.57),
       ("2011-11-14", 28.39, 28.39), ("2012-01-03", 27.98, 27.98), ("2013-01-02", 26.87, 26.87),
       ("2014-01-02", 26.86, 26.86), ("2014-12-29", 27.12, 19.43), ("2015-01-02", 27.12, 19.59),
       ("2015-04-21", 27.11, 27.11)]


def realloc():
    import datetime as dt
    d = [dt.date.fromisoformat(r[0]) for r in EX8] + [dt.date(2016, 12, 31)]
    conv = [r[1] for r in EX8] + [EX8[-1][1]]
    rs = [r[2] for r in EX8] + [EX8[-1][2]]
    f, ax = fig()
    ax.axvspan(dt.date(2007, 12, 1), dt.date(2009, 6, 30), color=RED, alpha=0.06)
    ax.text(dt.date(2008, 1, 15), 95, "미국 경기침체 (NBER)", fontsize=13, color=RED)
    ax.step(d, conv, where="post", color=MUTED, lw=3, label="전통형 TDF")
    ax.step(d, rs, where="post", color=TEAL, lw=2.4, label="국면 민감 TDF")
    ax.annotate("2007.8.21 — 위기 전 42%로 축소", xy=(dt.date(2007, 8, 21), 42.47),
                xytext=(dt.date(2003, 6, 1), 30), fontsize=14, color=TEAL, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.annotate("2009.1.2 — 21% (전통형 81%)", xy=(dt.date(2009, 1, 2), 21.24),
                xytext=(dt.date(2010, 3, 1), 10), fontsize=14, color=TEAL, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.text(dt.date(2010, 6, 1), 55, "2010년 이후 두 전략 모두 공분산 변화로 크게 축소", fontsize=13, color=MUTED)
    ax.set_ylim(0, 100); ax.set_ylabel("위험자산 비중 (%)", fontsize=14)
    ax.legend(fontsize=14, frameon=False, loc="lower left")
    clean(ax); ax.tick_params(labelsize=13)
    save(f, "realloc.png", note="원문 Exhibit 8의 재배분 일자와 비중을 계단 그래프로 옮김")


# ── 회전율 제약별 최대낙폭 (Exhibit 11) ───────────────────────────
def turnover_mdd():
    lim = ["5%", "10%", "15%", "20%", "제약 없음"]
    conv = [49.88, 49.90, 49.90, 49.90, 50.0]
    rs = [45.17, 41.10, 36.09, 31.29, 37.0]
    shc = [0.50, 0.49, 0.50, 0.51, 0.52]
    shr = [0.56, 0.64, 0.72, 0.80, 0.79]
    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE)
    x = np.arange(len(lim))
    for ax, c, r, t, fmt, top in ((a1, conv, rs, "최대낙폭 (%)", "{:.0f}", 60), (a2, shc, shr, "수익/위험", "{:.2f}", 1.0)):
        b1 = ax.bar(x - 0.2, c, 0.38, color=MUTED, label="전통형")
        b2 = ax.bar(x + 0.2, r, 0.38, color=TEAL, label="국면 민감")
        for bb, vv in ((b1, c), (b2, r)):
            for b, v in zip(bb, vv):
                ax.text(b.get_x() + b.get_width() / 2, v + top * 0.015, fmt.format(v), ha="center", fontsize=11)
        ax.set_xticks(x); ax.set_xticklabels(lim, fontsize=12)
        ax.set_title(t, fontsize=16, loc="left"); ax.set_ylim(0, top * 1.25); clean(ax)
        ax.set_xlabel("연간 회전율 제약", fontsize=13)
    a1.legend(fontsize=13, frameon=False, loc="upper center", ncol=2)
    f.tight_layout(w_pad=4)
    save(f, "turnover_mdd.png", note="원문 Exhibit 10·11 · 2003.1~2016.12")


def equations():
    equation(r"$P=N\left[\dfrac{\ln(1+L)\,T-\mu T}{\sigma\sqrt{T}}\right]$", "eq1.png", fontsize=44)
    equation(r"$P=N\left[\dfrac{\ln(1+L)\,T-\left(\mu_R W_R+\mu_S(1-W_R)\right)T}{\sigma_R W_R\sqrt{T}}\right]$",
             "eq2.png", fontsize=38)
    equation(r"$W_R=\dfrac{\ln(1+L)\,T-\mu_S T}{Z\,\sigma_R\sqrt{T}+\mu_R T-\mu_S T}$", "eq3.png", fontsize=42)
    equation(r"$d_t=\dfrac{1}{N}\,(x_t-\mu)^{\prime}\,\Sigma^{-1}(x_t-\mu)$", "eq4.png", fontsize=44)
    equation(r"$AR=\dfrac{\sum_{i=1}^{n}\sigma_{E_i}^{2}}{\sum_{j=1}^{N}\sigma_{A_j}^{2}},\qquad \Delta AR=\dfrac{\overline{AR}_{15}-\overline{AR}_{252}}{\sigma_{252}(AR)}$",
             "eq5.png", fontsize=38)
    equation(r"$\max_{w}\;\mu_p(w)\quad \mathrm{s.t.}\quad P\left(R_T<0\mid\Sigma_{k},\,T\right)\leq 5\%$",
             "eq6.png", fontsize=40)
    equation(r"$k=F\ \ \mathrm{if}\ \ z_{d}\geq 1\ \mathrm{and}\ z_{\Delta AR}\geq 1,\qquad k=N\ \ \mathrm{otherwise}$",
             "eq7.png", fontsize=38)


if __name__ == "__main__":
    loss_curve(); regime_gp(); regime_loss(); turbulence_demo(); absorption_demo()
    flow(); realloc(); turnover_mdd(); equations()
