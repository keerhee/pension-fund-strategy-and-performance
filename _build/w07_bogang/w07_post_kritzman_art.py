# -*- coding: utf-8 -*-
"""W07 보강 1 스페셜 II — 국면 기반 TDF 이후 그림.

실행: python w07_post_kritzman_art.py  →  _art/w07pk/
모든 시뮬레이션은 수업용 가상 실험이다(시드 고정). 논문의 실증 수치는 덱 본문에 출처와 함께 적는다.
"""
import math
import numpy as np
from statistics import NormalDist
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, fig, equation, svg, arrow, text,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK, WIDE)

OUT = out_dir("w07pk")
ND = NormalDist()
RES = {}


def bx(x, y, w, h, title, sub=(), kind="white", ts=34, ss=27):
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


# ── 01 · 진화 지도 ────────────────────────────────────────────────
def evo_map():
    b = ""
    b += bx(20, 200, 300, 220, "Kritzman (2017)", ["두 국면 · 임계 z ≥ 1", "기간 말 손실확률"], kind="dark")
    items = [("② 확률 국면", ["HMM 필터", "국면 확률로 가중"]),
             ("③ 연속 변동성", ["비중 ∝ 1/σ²", "변동성 헤징"]),
             ("④ 경로 위험", ["기간 중 손실", "낙폭 제약"]),
             ("⑤ 적응형 경로", ["w(τ, W)", "목표와의 거리"])]
    for k, (t, sub) in enumerate(items):
        y = 20 + k * 145
        b += bx(470, y, 400, 125, t, sub, kind="teal", ts=32, ss=25)
        b += arrow(325, 310, 462, y + 62, color=MUTED, mk="aM", wt=3)
        b += arrow(875, y + 62, 1010, 310, color=MUTED, mk="aM", wt=3)
    b += bx(1020, 190, 560, 240, "3축 글라이드패스", ["남은 기간 × 시장 상태", "× 내 자산 수준", "+ 경로 위험 제약"], kind="lime")
    svg("evo_map.png", b, w=1600, h=600)


# ── 02 · HMM ─────────────────────────────────────────────────────
P_TR = np.array([[0.97, 0.03], [0.10, 0.90]])     # 평상→평상 0.97, 취약→취약 0.90 (월간)
MU = np.array([0.010, -0.010]); SG = np.array([0.035, 0.075])


def hmm_sim(n=240, seed=11):
    rng = np.random.default_rng(seed)
    s = np.zeros(n, int); r = np.zeros(n)
    for t in range(n):
        if t: s[t] = rng.choice(2, p=P_TR[s[t - 1]])
        r[t] = rng.normal(MU[s[t]], SG[s[t]])
    # 해밀턴 필터
    p = np.zeros((n, 2)); prev = np.array([0.77, 0.23])
    for t in range(n):
        pred = prev @ P_TR
        lik = np.array([ND.pdf((r[t] - MU[k]) / SG[k]) / SG[k] for k in range(2)])
        post = pred * lik; post /= post.sum(); p[t] = post; prev = post
    return s, r, p


def hmm_fig():
    s, r, p = hmm_sim()
    w_star = np.array([0.80, 0.35])
    w_soft = p @ w_star
    hard = np.where(p[:, 1] > 0.5, w_star[1], w_star[0])
    band = [w_soft[0]]
    for x in w_soft[1:]:
        band.append(x if abs(x - band[-1]) > 0.10 else band[-1])
    band = np.array(band)
    to_soft = np.abs(np.diff(w_soft)).sum() / 20
    to_hard = np.abs(np.diff(hard)).sum() / 20
    to_band = np.abs(np.diff(band)).sum() / 20
    RES["hmm_turnover"] = (to_hard, to_soft, to_band)
    t = np.arange(len(r)) / 12
    f, (a1, a2) = plt.subplots(2, 1, figsize=(12.9, 5.4), sharex=True, gridspec_kw={"height_ratios": [1, 1.25]})
    a1.fill_between(t, 0, 1, where=s == 1, color=RED, alpha=0.10, step="mid", transform=a1.get_xaxis_transform())
    a1.plot(t, p[:, 1], color=RED, lw=2.2)
    a1.set_ylabel("취약 국면 확률", fontsize=13); a1.set_ylim(0, 1.05); clean(a1)
    a1.text(0.2, 0.82, "음영 = 실제 취약 국면(가상) · 선 = 필터가 추정한 확률", fontsize=13, color=MUTED)
    a2.step(t, hard * 100, color=MUTED, lw=1.8, where="mid")
    a2.plot(t, w_soft * 100, color=TEAL, lw=1.4, alpha=0.55)
    a2.step(t, band * 100, color=TEAL, lw=2.8, where="mid")
    a2.text(0.2, 24, f"임계값 판정 {to_hard*100:.0f}% · 확률 가중 {to_soft*100:.0f}% · 확률 가중 + 밴드 ±10%p {to_band*100:.0f}%  (연 회전율)",
            fontsize=14, color=INK, fontweight="bold")
    a2.text(0.2, 8, "회색 = 임계값 판정 · 옅은 선 = 확률 가중 · 굵은 선 = 확률 가중 + 밴드", fontsize=13, color=MUTED)
    a2.set_ylabel("위험자산 비중 (%)", fontsize=13); a2.set_ylim(0, 100); clean(a2)
    a2.set_xlabel("연도 (가상 20년, 월간)", fontsize=13)
    f.tight_layout(h_pad=0.8)
    save(f, "hmm.png", note="가상 2국면 HMM · 평상 μ 1%/σ 3.5%, 취약 μ −1%/σ 7.5% (월간) · 국면별 최적 80%/35%")
    print("   회전율 hard/soft", RES["hmm_turnover"])


# ── 03 · 변동성 연동 ──────────────────────────────────────────────
def vol_weight():
    sig = np.linspace(8, 48, 200)
    f, ax = fig()
    base, s0 = 60, 16
    ax.plot(sig, np.minimum(base * (s0 / sig) ** 2, 100), color=INK, lw=3, label="이론 (Merton) ∝ 1/σ²")
    ax.plot(sig, np.minimum(base * (s0 / sig), 100), color=TEAL, lw=3.2, label="실증 권고 ∝ 1/σ (VIX 두 배 → 절반)")
    ax.axhline(base, color=MUTED, ls=":", lw=1.6)
    ax.text(40, 62, "고정 비중 60%", fontsize=14, color=MUTED)
    for x, c_ in ((32, TEAL),):
        ax.plot([x], [base * s0 / x], "o", color=c_, ms=9)
        ax.text(x + 0.8, base * s0 / x + 3, f"σ 32% → {base*s0/x:.0f}%", fontsize=14, color=c_, fontweight="bold")
    ax.plot([32], [base * (s0 / 32) ** 2], "o", color=INK, ms=9)
    ax.text(32.8, base * (s0 / 32) ** 2 - 6, f"→ {base*(s0/32)**2:.0f}%", fontsize=14, color=INK, fontweight="bold")
    ax.axvline(16, color=HAIR, lw=1.2); ax.text(16.4, 95, "평균 σ 16%", fontsize=13, color=MUTED)
    ax.set_xlabel("예상 변동성 σ_t (연율, %)", fontsize=14); ax.set_ylabel("위험자산 비중 (%)", fontsize=14)
    ax.set_ylim(0, 105); ax.legend(fontsize=14, frameon=False, loc="upper right", bbox_to_anchor=(1, 0.9))
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "vol_weight.png", note="평균 σ 16%에서 60%를 들도록 맞춘 예시")


def vol_sim():
    rng = np.random.default_rng(5)
    n = 12 * 30
    s = np.zeros(n, int)
    for t in range(1, n):
        s[t] = rng.choice(2, p=P_TR[s[t - 1]])
    sig_m = np.where(s == 0, 0.035, 0.075)
    r_eq = rng.normal(0.006, sig_m)               # 국면별 기대수익은 같게 — 변동성만 바뀜
    rf = 0.0025
    sig_hat = np.zeros(n); sig_hat[0] = 0.045
    for t in range(1, n):                          # EWMA 변동성 추정(전월까지)
        sig_hat[t] = math.sqrt(0.7 * sig_hat[t - 1] ** 2 + 0.3 * r_eq[t - 1] ** 2)
    w_const = np.full(n, 0.6)
    w_vol = 0.045 / sig_hat; w_vol = np.minimum(w_vol / w_vol.mean() * 0.6, 1.0)   # 평균 비중을 60%로 맞춤
    out = {}
    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE)
    for w, c_, lab in ((w_const, MUTED, "고정 60%"), (w_vol, TEAL, "변동성 연동 (∝ 1/σ)")):
        rp = w * r_eq + (1 - w) * rf
        W = np.cumprod(1 + rp)
        dd = W / np.maximum.accumulate(W) - 1
        ann = W[-1] ** (12 / n) - 1; vol = rp.std() * math.sqrt(12)
        out[lab] = (ann, vol, dd.min(), (rp.mean() - rf) / rp.std() * math.sqrt(12), w.mean())
        a1.plot(np.arange(n) / 12, W, color=c_, lw=2.6, label=lab)
        a2.plot(np.arange(n) / 12, dd * 100, color=c_, lw=2.2)
    a1.set_title("누적 자산 (시작 1)", fontsize=15, loc="left"); a1.legend(fontsize=13, frameon=False)
    a2.set_title("낙폭 (%)", fontsize=15, loc="left")
    for ax in (a1, a2):
        ax.set_xlabel("연도 (가상 30년)", fontsize=13); clean(ax)
    f.tight_layout(w_pad=4)
    save(f, "vol_sim.png", note="가상 2국면 · 국면별 기대수익 동일, 변동성만 3.5%/7.5%(월간) · EWMA λ 0.7 · 평균 비중 60%로 맞춤")
    RES["vol_sim"] = out
    # 20개 시드 평균
    acc = []
    for seed in range(20):
        g = np.random.default_rng(seed); st = np.zeros(n, int)
        for t in range(1, n): st[t] = g.choice(2, p=P_TR[st[t - 1]])
        req = g.normal(0.006, np.where(st == 0, 0.035, 0.075)); sh = np.zeros(n); sh[0] = 0.045
        for t in range(1, n): sh[t] = math.sqrt(0.7 * sh[t - 1] ** 2 + 0.3 * req[t - 1] ** 2)
        wv = 0.045 / sh; wv = np.minimum(wv / wv.mean() * 0.6, 1.0); row = []
        for w in (np.full(n, 0.6), wv):
            rp = w * req + (1 - w) * rf; Wx = np.cumprod(1 + rp)
            row += [(rp.mean() - rf) / rp.std() * math.sqrt(12), (Wx / np.maximum.accumulate(Wx) - 1).min()]
        acc.append(row)
    acc = np.array(acc).mean(0); RES["vol_avg"] = acc
    print("   20시드 평균 샤프 고정/연동", acc[0].round(3), acc[2].round(3), "MDD", acc[1].round(3), acc[3].round(3))
    for k, v in out.items():
        print(f"   {k}: 연 {v[0]*100:.2f}% · 변동성 {v[1]*100:.1f}% · MDD {v[2]*100:.1f}% · 샤프 {v[3]:.2f} · 평균비중 {v[4]*100:.0f}%")


# ── 04 · 경로 위험 ────────────────────────────────────────────────
def p_end(mu, s, T, L=0.0):
    return ND.cdf((math.log(1 + L) - mu * T) / (s * math.sqrt(T)))


def p_within(mu, s, T, L=0.0):
    a = math.log(1 + L)
    return ND.cdf((a - mu * T) / (s * math.sqrt(T))) + ND.cdf((a + mu * T) / (s * math.sqrt(T))) * math.exp(2 * mu * a / s ** 2)


def within_fig():
    T = np.linspace(0.25, 20, 200)
    L = -0.10
    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE)
    for ax, LL, ttl in ((a1, -0.10, "10% 이상 손실 (L = −10%)"), (a2, -0.20, "20% 이상 손실 (L = −20%)")):
        e = [p_end(0.075, 0.21, t, LL) * 100 for t in T]
        w = [p_within(0.075, 0.21, t, LL) * 100 for t in T]
        ax.plot(T, e, color=INK, lw=2.6, label="기간 말 (Kritzman 식 1)")
        ax.plot(T, w, color=RED, lw=3, label="기간 중 한 번이라도")
        ax.set_title(ttl, fontsize=15, loc="left"); ax.set_ylim(0, 105); clean(ax)
        ax.set_xlabel("투자기간 T (년)", fontsize=13)
        for t in (5, 20):
            ax.plot([t], [p_within(0.075, 0.21, t, LL) * 100], "o", color=RED, ms=7)
            ax.text(t + 0.3, p_within(0.075, 0.21, t, LL) * 100 + 3, f"{p_within(0.075, 0.21, t, LL)*100:.0f}%", fontsize=13, color=RED)
            ax.plot([t], [p_end(0.075, 0.21, t, LL) * 100], "o", color=INK, ms=7)
            ax.text(t + 0.3, p_end(0.075, 0.21, t, LL) * 100 - 7, f"{p_end(0.075, 0.21, t, LL)*100:.0f}%", fontsize=13, color=INK)
    a1.legend(fontsize=13, frameon=False, loc="upper right"); a1.set_ylabel("확률 (%)", fontsize=13)
    f.tight_layout(w_pad=4)
    save(f, "within.png", note="위험자산 μ 7.5%(연속) · σ 21% · 기하 브라운 운동의 첫 도달 확률")
    for LL in (-0.10, -0.20):
        print("   L", LL, [(t, round(p_end(0.075, 0.21, t, LL) * 100, 1), round(p_within(0.075, 0.21, t, LL) * 100, 1)) for t in (1, 5, 10, 20)])


def dd_fig():
    rng = np.random.default_rng(21)
    n = 12 * 15
    alpha, wm = 0.80, 0.60
    r = rng.normal(0.006, 0.05, n); r[40:58] = rng.normal(-0.03, 0.06, 18)
    rf = 0.002
    W = [1.0]; M = 1.0; ws = []; Wc = [1.0]
    for t in range(n):
        w = max(0.0, min(1.0, wm / 0.6 * 0.6 * (1 - alpha * M / W[-1]) / (1 - alpha)))
        ws.append(w)
        W.append(W[-1] * (1 + w * r[t] + (1 - w) * rf)); M = max(M, W[-1])
        Wc.append(Wc[-1] * (1 + 0.6 * r[t] + 0.4 * rf))
    W = np.array(W); Wc = np.array(Wc); tt = np.arange(n + 1) / 12
    floor = alpha * np.maximum.accumulate(W)
    f, (a1, a2) = plt.subplots(2, 1, figsize=(12.9, 5.4), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
    a1.plot(tt, Wc, color=MUTED, lw=2, label="고정 60%")
    a1.plot(tt, W, color=TEAL, lw=2.8, label="낙폭 제약 (α = 0.8)")
    a1.plot(tt, floor, color=RED, lw=1.6, ls="--", label="바닥 = 0.8 × 최고점")
    a1.legend(fontsize=12, frameon=False, loc="lower right", ncol=3); clean(a1); a1.set_ylabel("자산", fontsize=13)
    a2.plot(np.arange(n) / 12, np.array(ws) * 100, color=TEAL, lw=2.4)
    a2.set_ylabel("위험자산 (%)", fontsize=13); a2.set_ylim(0, 105); clean(a2)
    a2.set_xlabel("연도 (가상 15년)", fontsize=13)
    mdd_c = (Wc / np.maximum.accumulate(Wc) - 1).min(); mdd_d = (W / np.maximum.accumulate(W) - 1).min()
    a1.text(5.2, 1.36, f"최대낙폭: 고정 {mdd_c*100:.0f}% · 제약 {mdd_d*100:.0f}%", fontsize=14, color=INK, fontweight="bold")
    f.tight_layout(h_pad=0.8)
    save(f, "drawdown.png", note="가상 경로 · 바닥에서 쿠션 비율만큼만 위험자산 — 바닥에 닿으면 0%")
    RES["dd"] = (mdd_c, mdd_d)
    print("   MDD 고정/제약", RES["dd"])


# ── 05 · 적응형 글라이드패스 ──────────────────────────────────────
def adaptive_sim():
    rng = np.random.default_rng(8)
    nP, T = 20000, 30
    mu_s, sg, rb = 0.075, 0.18, 0.025
    c = 1.0                                         # 매년 1(단위) 적립
    det = np.interp(np.arange(T), [0, 10, 30], [0.9, 0.9, 0.4])
    target = 70.0
    Wd = np.zeros(nP); Wa = np.zeros(nP)
    wa_hist = np.zeros((nP, T))
    for t in range(T):
        Z = rng.standard_normal(nP)
        rs = np.exp(mu_s - sg ** 2 / 2 + sg * Z) - 1
        Wd = (Wd + c) * (1 + det[t] * rs + (1 - det[t]) * rb)
        tau = T - t
        pv_c = sum(c / (1 + rb) ** k for k in range(0, tau)) if tau > 0 else 0
        gap = target / (1 + rb) ** tau - (Wa + c) - (pv_c - c)
        lam = (mu_s - rb) / sg ** 2
        wa = np.clip(lam * gap / np.maximum(Wa + c, 1e-6), 0.0, 1.0)
        wa_hist[:, t] = wa
        Wa = (Wa + c) * (1 + wa * rs + (1 - wa) * rb)
    def st(W):
        return (np.median(W), np.percentile(W, 5), np.mean(W < 0.8 * target) * 100, np.mean(W))
    RES["adapt"] = {"고정 경로": st(Wd), "적응형": st(Wa)}
    for k, v in RES["adapt"].items():
        print(f"   {k}: 중앙 {v[0]:.1f} · 하위5% {v[1]:.1f} · 목표80%미달 {v[2]:.1f}% · 평균 {v[3]:.1f}")
    note = "가상 2만 경로 · 주식 μ 7.5% σ 18% · 채권 2.5% · 매년 1씩 30년 적립 · 목표 70"
    f, a1 = fig()
    bins = np.linspace(0, 200, 60)
    a1.hist(Wd, bins=bins, color=MUTED, alpha=0.6, label="고정 경로 90 → 40%")
    a1.hist(Wa, bins=bins, color=TEAL, alpha=0.6, label="적응형 (목표와의 거리)")
    a1.axvline(target, color=RED, ls="--", lw=1.8)
    a1.text(target + 2, 3650, "목표 70 — 적응형 막대는 위로 잘림(약 1만 1천)", fontsize=13, color=RED)
    a1.axvline(0.8 * target, color=RED, ls=":", lw=1.4)
    a1.text(0.8 * target - 2, 2600, "목표의 80% = 56", fontsize=13, color=RED, ha="right")
    a1.set_ylim(0, 4000); a1.legend(fontsize=13, frameon=False, loc="upper right")
    a1.set_xlabel("은퇴 시 자산 (매년 적립액 1 = 단위)", fontsize=14); a1.set_ylabel("경로 수", fontsize=14)
    clean(a1); a1.tick_params(labelsize=13)
    save(f, "adaptive_dist.png", note=note)

    f, a2 = fig()
    yrs = np.arange(T)
    a2.plot(yrs, det * 100, color=MUTED, lw=3.2)
    a2.text(0.4, 84, "고정 경로\n(모두 같은 비중)", va="top", bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5), fontsize=14, color=MUTED, fontweight="bold")
    q10, q50, q90 = (np.percentile(wa_hist, q, axis=0) * 100 for q in (10, 50, 90))
    a2.plot(yrs, q90, color=TEAL, lw=1.8, alpha=0.6)
    a2.plot(yrs, q50, color=TEAL, lw=3.2)
    a2.plot(yrs, q10, color=TEAL, lw=1.8, alpha=0.6)
    a2.text(21.6, 86, "뒤처진 경로\n(비중 상위 10%)", va="center", bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5), fontsize=13, color=TEAL)
    a2.text(16.6, 50, "중간 경로 (중앙값)", bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5), fontsize=14, color=TEAL, fontweight="bold")
    a2.text(6.6, 14, "앞선 경로\n(비중 하위 10%)", fontsize=13, color=TEAL)
    a2.set_ylim(0, 105); a2.set_xlim(0, 29)
    a2.set_xlabel("가입 후 연수 (30년 뒤 은퇴)", fontsize=14); a2.set_ylabel("위험자산 비중 (%)", fontsize=14)
    clean(a2); a2.tick_params(labelsize=13)
    save(f, "adaptive_weight.png", note=note)


def reflection_fig():
    rng = np.random.default_rng(42)
    n = 500; T = 5.0; dt = T / n; sig = 0.21; a = math.log(0.9)
    for seed in range(200):
        g = np.random.default_rng(seed)
        X = np.concatenate([[0], np.cumsum(sig * math.sqrt(dt) * g.standard_normal(n))])
        hit = np.argmax(X <= a) if (X <= a).any() else None
        if hit and 120 < hit < 260 and X[-1] > 0.05:
            break
    t = np.linspace(0, T, n + 1)
    R = X.copy(); R[hit:] = 2 * a - X[hit:]
    f, ax = fig()
    ax.axhline(a, color=RED, lw=2, ls="--")
    ax.text(3.2, a - 0.025, "손실선 a = ln 0.9 (−10%)", va="top", fontsize=14, color=RED)
    ax.plot(t, X, color=INK, lw=2.4)
    ax.plot(t[hit:], R[hit:], color=TEAL, lw=2.4, ls="--")
    ax.plot([t[hit]], [a], "o", color=RED, ms=11)
    ax.annotate("처음 닿는 시점 τ_a", xy=(t[hit], a), xytext=(t[hit] - 1.3, a - 0.20), fontsize=14, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    ax.text(T + 0.05, X[-1], "원래 경로\n끝이 손실선 위", fontsize=13, color=INK, va="center")
    ax.text(T + 0.05, R[-1], "뒤집은 경로\n끝 = 2a − X_T\n(손실선 아래)", fontsize=13, color=TEAL, va="center")
    ax.axhline(0, color=HAIR, lw=1)
    ax.set_xlim(0, T + 1.1); ax.set_xlabel("시간 (년)", fontsize=14); ax.set_ylabel("로그 수익률 X_t", fontsize=14)
    clean(ax); ax.tick_params(labelsize=13)
    save(f, "reflection.png", note="가상 경로 · 추세 0 · σ 21% — 손실선에 닿은 뒤의 움직임을 손실선에 대해 뒤집었다")


def compare_table():
    rows = [("② 확률 국면", r"$\pi_t(k)$", r"$w_t=\sum_k \pi_t(k)\,w_k^{*}$", "모형 오설정 · 회전율"),
            ("③ 연속 변동성", r"$\hat{\sigma}_t^{2}$", r"$w_t \propto 1/\hat{\sigma}_t$", "추정 지연 · 급반등 놓침"),
            ("④ 경로 위험", r"$M_t,\ L$", r"$w_t=m\,(1-\alpha M_t/W_t)$", "회복 속도 저하"),
            ("⑤ 적응형 경로", r"$W_t,\ W^{*}$", r"$w_tW_t \propto W^{*}e^{-r\tau}-W_t-\mathrm{PV}_t$", "상방 포기 · 목표 설정 의존")]
    head = ("갈래", "더하는 정보", "핵심 식", "대가 · 위험")
    xs = [0.01, 0.20, 0.38, 0.75]
    f = plt.figure(figsize=(12.9, 4.4)); ax = f.add_axes([0, 0, 1, 1]); ax.axis("off")
    for x, h in zip(xs, head):
        ax.text(x, 0.93, h, fontsize=15, color=MUTED, va="center")
    ax.plot([0, 1], [0.86, 0.86], color=INK, lw=1.2)
    for i, (g, info, eq, cost) in enumerate(rows):
        y = 0.74 - i * 0.19
        c_ = TEAL if i == 3 else INK
        ax.text(xs[0], y, g, fontsize=19, color=c_, fontweight="bold", va="center")
        ax.text(xs[1], y, info, fontsize=22, color=c_, va="center")
        ax.text(xs[2], y, eq, fontsize=22, color=c_, va="center")
        ax.text(xs[3], y, cost, fontsize=18, color=c_, va="center")
        ax.plot([0, 1], [y - 0.095, y - 0.095], color=HAIR, lw=1)
    save(f, "compare_table.png")


def reflection_equations():
    equation(r"$P\left(\min_{t\leq T}X_t\leq a\right)=2\,N\!\left[\dfrac{a}{\sigma\sqrt{T}}\right]\qquad (\mu=0,\ a<0)$", "eq_reflect0.png", fontsize=38)
    equation(r"$\mu\neq 0:\quad 2N[\cdot]\ \longrightarrow\ N\!\left[\dfrac{a-\mu T}{\sigma\sqrt{T}}\right]+e^{2\mu a/\sigma^{2}}\,N\!\left[\dfrac{a+\mu T}{\sigma\sqrt{T}}\right]$", "eq_reflect1.png", fontsize=36)
    # 두 줄을 한 장으로 쌓는다(eq 장표는 그림 하나만 받는다)
    import os
    from PIL import Image
    from primer_lib import _OUT
    i0, i1 = (Image.open(os.path.join(_OUT, n)).convert("RGB") for n in ("eq_reflect0.png", "eq_reflect1.png"))
    W = max(i0.width, i1.width); gap = int(0.25 * i0.height)
    bg = i0.getpixel((2, 2))
    c = Image.new("RGB", (W, i0.height + gap + i1.height), bg)
    c.paste(i0, ((W - i0.width) // 2, 0)); c.paste(i1, ((W - i1.width) // 2, i0.height + gap))
    c.save(os.path.join(_OUT, "eq_reflect.png"))


def equations():
    equation(r"$\pi_t(k)=\dfrac{f_k(r_t)\sum_{j}p_{jk}\,\pi_{t-1}(j)}{\sum_{m} f_m(r_t)\sum_{j}p_{jm}\,\pi_{t-1}(j)}$", "eq_filter.png", fontsize=38)
    equation(r"$w_t=\sum_{k}\pi_t(k)\,w_k^{*},\qquad w_k^{*}=\arg\max_w\ \mu_p(w)\ \ \mathrm{s.t.}\ \ P(R_T<0\mid\Sigma_k,T)\leq 5\%$", "eq_blend.png", fontsize=34)
    equation(r"$w_t=\dfrac{c}{\hat{\sigma}_t^{2}}\,\bar{w}(\tau),\qquad \hat{\sigma}_t^{2}=\lambda\,\hat{\sigma}_{t-1}^{2}+(1-\lambda)\,r_{t-1}^{2}$", "eq_volman.png", fontsize=38)
    equation(r"$w_t^{*}=\dfrac{\mu-r}{\gamma\,v_t}\;+\;\left(1-\dfrac{1}{\gamma}\right)\dfrac{\rho\,\sigma_v}{\sqrt{v_t}}\,B(\tau)$", "eq_cv.png", fontsize=38)
    equation(r"$P_{\mathrm{within}}=N\!\left[\dfrac{\ln(1+L)-\mu T}{\sigma\sqrt{T}}\right]+N\!\left[\dfrac{\ln(1+L)+\mu T}{\sigma\sqrt{T}}\right](1+L)^{2\mu/\sigma^{2}}$", "eq_within.png", fontsize=34)
    equation(r"$w_t=m\left(1-\dfrac{\alpha\,M_t}{W_t}\right),\qquad M_t=\max_{s\leq t}W_s,\qquad m=\dfrac{\mu-r}{\gamma\,\sigma^{2}}$", "eq_gz.png", fontsize=38)
    equation(r"$w_t\,W_t=\dfrac{\mu-r}{\sigma^{2}}\left(W^{*}e^{-r\tau}-W_t-\mathrm{PV}_t(c)\right)$", "eq_target.png", fontsize=40)
    equation(r"$w_t=\mathcal{N}_{\theta}(\tau,\,W_t),\qquad \theta^{*}=\arg\min_{\theta}\ \frac{1}{M}\sum_{m=1}^{M}\ell\!\left(W_T^{(m)}(\theta)\right)$", "eq_nn.png", fontsize=36)


if __name__ == "__main__":
    evo_map(); hmm_fig(); vol_weight(); vol_sim(); within_fig(); dd_fig(); adaptive_sim(); equations()
    reflection_fig(); compare_table(); reflection_equations()
