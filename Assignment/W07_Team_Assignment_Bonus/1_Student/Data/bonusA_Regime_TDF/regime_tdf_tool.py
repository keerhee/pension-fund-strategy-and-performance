#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""국면전환(regime-switching) TDF 계산 도구 — W07 보너스 과제 A

시장: 주식시장은 '강세'와 '약세' 두 국면을 오간다(마르코프 국면전환 모형). 국면은 직접 보이지 않는다.
  강세: 연 기대수익 9% · 변동성 14%   약세: 연 기대수익 −8% · 변동성 24%   안전자산 3% (교육용 가정)
  매달 강세가 계속될 확률 98%(평균 4년 2개월 지속) · 약세가 계속될 확률 85%(평균 7개월 지속)
가입자: 30세 · 연봉 4,500만 원(2% 성장) · 계좌 2,000만 원 · 매년 연봉의 1/12 적립 · 65세 은퇴 · 위험회피 γ = 4
세 안
  A 표준 TDF          주식 80%(30세) → 30%(64세) 직선
  B 완전 국면 TDF      A의 비중 + (이번 달 국면 확률로 계산한 최적 비중 − 그 장기 평균), 0~100%
  C 제한 국면 TDF      B와 같되 조정 폭을 ±5%p로 제한(--cap으로 변경)
국면 확률은 지난 수익률만 보고 베이즈 규칙(해밀턴 필터)으로 매달 갱신한다. 미래는 보지 않는다.

사용법
  python3 regime_tdf_tool.py                      # 기본
  python3 regime_tdf_tool.py --cap 10             # 안 C의 조정 폭을 ±10%p로
  python3 regime_tdf_tool.py --cost 30            # 매매 비용(편도, bp)
  python3 regime_tdf_tool.py --train-years 15     # 모형 추정에 쓰는 과거 자료 기간(년)
  python3 regime_tdf_tool.py --ce-tol 0 --win-min 70 --iid-loss-max 1 --to-max 60   # 판정 기준 변경
판정 기준(교육용 가정 · 바꿔 볼 수 있음)
  ① 잠재력: 모형을 정확히 알 때 A 대비 CE 개선 > 0
  ② 추정 오차: 과거 자료로 모형을 추정해 쓸 때 A 대비 평균 CE 개선 ≥ −ce_tol%, 그리고 개선되는 경우가 win_min% 이상
  ③ 오진 비용: 실제로는 국면이 없는 시장에서 A 대비 CE 손실 ≤ iid_loss_max%
  ④ 운영: 연 회전율 ≤ to_max%
"""
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--gamma", type=float, default=4.0); ap.add_argument("--cap", type=float, default=5.0)
ap.add_argument("--cost", type=float, default=20.0, help="편도 매매 비용 bp"); ap.add_argument("--paths", type=int, default=4000)
ap.add_argument("--train-years", type=int, default=30); ap.add_argument("--histories", type=int, default=12)
ap.add_argument("--ce-tol", type=float, default=0.0); ap.add_argument("--win-min", type=float, default=70.0)
ap.add_argument("--iid-loss-max", type=float, default=1.0); ap.add_argument("--to-max", type=float, default=60.0)
a = ap.parse_args()
G, CAP, C = a.gamma, a.cap / 100, a.cost / 1e4
R = 0.03 / 12
TRUE = dict(mu=np.array([0.09, -0.08]) / 12, sd=np.array([0.14, 0.24]) / np.sqrt(12), p=np.array([[0.98, 0.02], [0.15, 0.85]]))
A0, A1 = 30, 65; NM = (A1 - A0) * 12; Y0, F0, CONTRIB, GY = 0.45, 0.20, 1 / 12, 0.02


def stationary(P):
    return np.array([P[1, 0], P[0, 1]]) / (P[0, 1] + P[1, 0])


def sim_regime(P, n, m, rng, start=None):
    """m개 경로 × n개월의 국면(0 강세 · 1 약세)"""
    s = np.zeros((m, n), dtype=int)
    cur = (rng.random(m) < stationary(P)[1]).astype(int) if start is None else np.full(m, start)
    u = rng.random((m, n))
    for t in range(n):
        s[:, t] = cur
        stay = np.where(cur == 0, P[0, 0], P[1, 1])
        cur = np.where(u[:, t] < stay, cur, 1 - cur)
    return s


def sim_returns(prm, n, m, rng, iid=False):
    if iid:   # 국면 없는 시장 — 같은 장기 평균 · 변동성을 갖는 정규분포
        pi = stationary(prm["p"]); mu = pi @ prm["mu"]
        var = pi @ (prm["sd"] ** 2 + prm["mu"] ** 2) - mu ** 2
        return mu + np.sqrt(var) * rng.standard_normal((m, n)), None
    s = sim_regime(prm["p"], n, m, rng)
    return prm["mu"][s] + prm["sd"][s] * rng.standard_normal((m, n)), s


def w_opt(pb, prm):
    """다음 달 약세 확률 pb에서 한 달 최적 주식 비중 (혼합분포의 평균 · 분산)"""
    mu, sd = prm["mu"], prm["sd"]
    m = (1 - pb) * mu[0] + pb * mu[1]
    v = (1 - pb) * (sd[0] ** 2 + mu[0] ** 2) + pb * (sd[1] ** 2 + mu[1] ** 2) - m ** 2
    return (m - R) / (G * v)


def npdf(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / sd


def neutral(prm, n=6000):
    """믿는 모형에서 필터가 내놓는 최적 비중의 장기 평균 — 조정 폭의 평균이 0이 되도록 하는 기준점"""
    x, _ = sim_returns(prm, n, 1, np.random.default_rng(9)); x = x[0]; P = prm["p"]
    pb = stationary(P)[1]; ws = np.zeros(n)
    for t in range(n):
        ws[t] = np.clip(w_opt(pb, prm), -1, 2)
        lb, lB = npdf(x[t], prm["mu"][0], prm["sd"][0]), npdf(x[t], prm["mu"][1], prm["sd"][1])
        post = pb * lB / (pb * lB + (1 - pb) * lb); pb = post * P[1, 1] + (1 - post) * P[0, 1]
    return ws.mean()


def run(strategy, ret, prm):
    """ret: (경로, 개월) 실제 수익률 · prm: 투자자가 '믿는' 모형 모수"""
    m = ret.shape[0]; F = np.full(m, F0); Y = Y0
    P = prm["p"]; pb_pred = np.full(m, stationary(P)[1]); wbar = neutral(prm)
    wprev = np.zeros(m); turn = np.zeros(m); wsum = 0.0; pbs = np.zeros((m, NM))
    for t in range(NM):
        age = A0 + t / 12
        glide = 0.80 - 0.50 * min((age - A0) / (A1 - 1 - A0), 1.0)
        tilt = np.clip(w_opt(pb_pred, prm), -1, 2) - wbar
        if strategy == "A": w = np.full(m, glide)
        elif strategy == "B": w = np.clip(glide + tilt, 0, 1)
        else: w = np.clip(glide + np.clip(tilt, -CAP, CAP), 0, 1)
        if t > 0:
            dw = np.abs(w - wprev); turn += dw; F = F * (1 - C * dw)
        x = ret[:, t]
        F = F * (1 + w * x + (1 - w) * R)
        wprev = w * (1 + x) / (1 + w * x + (1 - w) * R)       # 수익률 반영 후 비중이 흘러간다
        if t % 12 == 11:
            F = F + CONTRIB * Y; Y *= 1 + GY
        # 해밀턴 필터: 이번 달 수익률을 보고 약세 확률을 갱신 → 다음 달 예측
        lb, lB = npdf(x, prm["mu"][0], prm["sd"][0]), npdf(x, prm["mu"][1], prm["sd"][1])
        post = pb_pred * lB / (pb_pred * lB + (1 - pb_pred) * lb)
        pbs[:, t] = post
        pb_pred = post * P[1, 1] + (1 - post) * P[0, 1]
        wsum += w.mean()
    ce = np.mean(F ** (1 - G)) ** (1 / (1 - G))
    return dict(ce=ce, med=float(np.median(F)), q5=float(np.quantile(F, 0.05)), to=float(turn.mean() / (NM / 12) * 100),
                wavg=wsum / NM, pbs=pbs)


def fit_hmm(x, iters=150):
    """2국면 정규 HMM을 EM(Baum–Welch)으로 추정. 국면 0을 평균이 높은 쪽으로 정렬한다."""
    n = len(x); med = np.median(np.abs(x - x.mean()))
    mu = np.array([x.mean() + 0.005, x.mean() - 0.01]); sd = np.array([x.std() * 0.8, x.std() * 1.6])
    P = np.array([[0.95, 0.05], [0.10, 0.90]]); pi0 = np.array([0.8, 0.2])
    for _ in range(iters):
        B = np.c_[npdf(x, mu[0], sd[0]), npdf(x, mu[1], sd[1])] + 1e-300
        al = np.zeros((n, 2)); c = np.zeros(n)
        al[0] = pi0 * B[0]; c[0] = al[0].sum(); al[0] /= c[0]
        for t in range(1, n):
            al[t] = (al[t - 1] @ P) * B[t]; c[t] = al[t].sum(); al[t] /= c[t]
        be = np.ones((n, 2))
        for t in range(n - 2, -1, -1):
            be[t] = (P @ (B[t + 1] * be[t + 1])) / c[t + 1]
        gm = al * be; gm /= gm.sum(1, keepdims=True)
        xi = (al[:-1, :, None] * P[None] * (B[1:] * be[1:])[:, None, :]) / c[1:, None, None]
        P = xi.sum(0) / gm[:-1].sum(0)[:, None]; P /= P.sum(1, keepdims=True)
        mu = (gm * x[:, None]).sum(0) / gm.sum(0)
        sd = np.sqrt((gm * (x[:, None] - mu) ** 2).sum(0) / gm.sum(0)); sd = np.maximum(sd, 0.2 * x.std())
        pi0 = gm[0]
    if mu[0] < mu[1]:
        mu, sd, P = mu[::-1], sd[::-1], P[::-1, ::-1]
    return dict(mu=mu, sd=sd, p=P)


def desc(prm):
    return (f"강세 {prm['mu'][0]*1200:+5.1f}%/{prm['sd'][0]*np.sqrt(12)*100:4.1f}% · 약세 {prm['mu'][1]*1200:+5.1f}%/{prm['sd'][1]*np.sqrt(12)*100:4.1f}%"
            f" · 지속확률 {prm['p'][0,0]:.3f}/{prm['p'][1,1]:.3f}")


rng = np.random.default_rng(2026)
NAMES = {"A": "A 표준 TDF", "B": "B 완전 국면 TDF", "C": f"C 제한 국면 TDF(±{a.cap:g}%p)"}
print(f"=== 국면전환 TDF — γ = {G:g} · 매매 비용 {a.cost:g}bp · {a.paths:,}개 경로 · 30→65세 ===")
print(f"    판정 기준(교육용 가정 · 바꿔 볼 수 있음): ① 정답 모형에서 개선 > 0 · ② 추정 모형 평균 개선 ≥ −{a.ce_tol:g}% · 개선 비율 ≥ {a.win_min:g}%"
      f" · ③ 국면 없는 시장 손실 ≤ {a.iid_loss_max:g}% · ④ 연 회전율 ≤ {a.to_max:g}%")
pi = stationary(TRUE["p"])
print(f"[1] 정답 모형: {desc(TRUE)} · 장기적으로 약세인 기간 {pi[1]:.0%}")
for pb in (0.0, pi[1], 0.5, 1.0):
    print(f"    다음 달 약세 확률 {pb:4.0%} → 한 달 최적 주식 비중 {w_opt(pb, TRUE):+7.1%}")
print(f"    조정 폭 = 이번 달 최적 비중 − 장기 평균 최적 비중({neutral(TRUE):.1%}). 조정 폭은 평균적으로 0 — 주식을 '더 많이'가 아니라 '때에 맞게' 들기 위한 것")

# [2] 필터가 국면을 얼마나 빨리 알아채는가
ret, s = sim_returns(TRUE, NM, a.paths, rng)
res = {k: run(k, ret, TRUE) for k in "ABC"}
pbs = res["A"]["pbs"]; bear = s == 1
hit = ((pbs > 0.5) == bear).mean(); onset = np.argwhere((s[:, 1:] == 1) & (s[:, :-1] == 0))
lags = []
for i, t in onset[:3000]:
    k = np.argmax(pbs[i, t + 1:t + 25] > 0.5) if (pbs[i, t + 1:t + 25] > 0.5).any() else 24
    lags.append(k + 1)
print(f"[2] 국면 탐지(정답 모형) — 국면을 맞힌 달 {hit:.0%} · 약세 시작 후 확률 50%를 넘기까지 중앙값 {np.median(lags):.0f}개월"
      f" · 24개월 안에 못 알아챈 비율 {np.mean(np.array(lags) >= 24):.0%}")
print(f"[3] 정답 모형을 알 때 — 65세 은퇴자산(억 원)")
for k in "ABC":
    r = res[k]; d = (r["ce"] / res["A"]["ce"] - 1) * 100
    print(f"    {NAMES[k]:<20} CE {r['ce']:.2f} (A 대비 {d:+5.1f}%) · 중앙값 {r['med']:.2f} · 하위 5% {r['q5']:.2f} · 평균 주식 {r['wavg']:.0%} · 연 회전율 {r['to']:4.0f}%")

# [4] 추정 오차 — 과거 자료로 모형을 추정해 쓴다
print(f"[4] 추정 오차 — 과거 {a.train_years}년 자료로 모형을 추정해 쓰면 (과거 자료 {a.histories}가지, 같은 미래 경로)")
gains = {"B": [], "C": []}
for h in range(a.histories):
    hr = np.random.default_rng(100 + h)
    x, _ = sim_returns(TRUE, a.train_years * 12, 1, hr); est = fit_hmm(x[0])
    rr = {k: run(k, ret, est) for k in "ABC"}
    for k in "BC": gains[k].append((rr[k]["ce"] / rr["A"]["ce"] - 1) * 100)
    if h < 4: print(f"    과거 자료 {h+1:>2}: 추정 {desc(est)} → B {gains['B'][-1]:+5.1f}% · C {gains['C'][-1]:+5.1f}%")
for k in "BC":
    g = np.array(gains[k]); print(f"    {NAMES[k]:<20} A 대비 CE 개선 평균 {g.mean():+5.1f}% · 최저 {g.min():+5.1f}% · 개선된 경우 {np.mean(g > 0):.0%}")

# [5] 오진 비용 — 실제로는 국면이 없는 시장
print("[5] 오진 비용 — 시장에 국면이 없는데(장기 평균 · 변동성은 같음) 과거 자료로 국면 모형을 추정해 쓰면")
ret0, _ = sim_returns(TRUE, NM, a.paths, rng, iid=True); iidg = {"B": [], "C": []}
for h in range(min(a.histories, 6)):
    hr = np.random.default_rng(500 + h)
    x, _ = sim_returns(TRUE, a.train_years * 12, 1, hr, iid=True); est = fit_hmm(x[0])
    rr = {k: run(k, ret0, est) for k in "ABC"}
    for k in "BC": iidg[k].append((rr[k]["ce"] / rr["A"]["ce"] - 1) * 100)
    if h < 2: print(f"    과거 자료 {h+1}: 추정 {desc(est)} (실제로는 국면 없음)")
for k in "BC":
    g = np.array(iidg[k]); print(f"    {NAMES[k]:<20} A 대비 CE 개선 평균 {g.mean():+5.1f}% · 최저 {g.min():+5.1f}%")

print("[6] 판정표")
for k in "BC":
    ok1 = res[k]["ce"] > res["A"]["ce"]; g = np.array(gains[k]); ok2 = g.mean() >= -a.ce_tol and np.mean(g > 0) * 100 >= a.win_min
    ok3 = -np.mean(iidg[k]) <= a.iid_loss_max; ok4 = res[k]["to"] <= a.to_max
    m = lambda b: "통과" if b else "탈락"
    print(f"    {NAMES[k]:<20} ① {m(ok1)} · ② {m(ok2)} · ③ {m(ok3)} · ④ {m(ok4)}")
print(f"    {NAMES['A']:<20} 기준 안(비교 대상) · 연 회전율 {res['A']['to']:.0f}%")
