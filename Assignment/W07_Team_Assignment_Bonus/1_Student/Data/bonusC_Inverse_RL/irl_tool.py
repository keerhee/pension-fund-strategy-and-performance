#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""역강화학습(Inverse RL) — 투자위원회의 결정에서 '숨은 보상함수'를 추정한다 · W07 보너스 과제 C

강화학습(RL)은 보상이 주어졌을 때 최적 행동을 찾는다. 역강화학습(IRL)은 거꾸로, 관찰된 행동을 보고
그 행동을 가장 잘 설명하는 보상을 찾는다. 이 도구는 최대 엔트로피 IRL을 한 단계(근시안) 문제로 단순화해 쓴다.
그러면 IRL은 '조건부 로짓 최우추정'과 같아진다.

위원회의 보상(이 구조는 가정 · 계수는 추정 대상)
  u(a | 상태) = a·μ_t − (γ/2)·σ²·a² − κ·(a − a_전월)² − δ·[손실 국면]·a
    a 주식 비중(20~70%, 5%p 간격) · μ_t 이번 달 기대초과수익(밸류에이션 신호로 계산, 연율) · σ 주식 변동성 16%
    γ 위험회피 · κ 관성(바꾸기 싫어함) · δ 손실 국면(시장이 고점 대비 −15% 이하)에서 주식을 더 싫어하는 정도
  위원회는 u가 큰 비중을 '대체로' 고른다: P(a) ∝ exp(u(a)/τ). τ가 클수록 결정이 들쭉날쭉하다.
  IPS(투자정책서)에 적힌 위험회피는 γ = 4다.

데이터: committee_decisions.csv — 15년(180개월) 동안의 신호 · 손실 국면 여부 · 전월 비중 · 결정한 비중
  (교육용 모의 자료다. 생성 과정은 이 파일 맨 아래 make_data()에 공개되어 있다.)

사용법
  python3 irl_tool.py                         # 기본
  python3 irl_tool.py --years 5               # 최근 5년 자료만으로 추정
  python3 irl_tool.py --t-min 2 --regret-max 15   # 판정 기준 변경
판정 기준(교육용 가정 · 바꿔 볼 수 있음)
  ① 식별: 드러난 γ와 IPS γ = 4의 차이가 통계적으로 유의(|t| ≥ t_min)
  ② 개선: 두 관점(IPS γ = 4 · 드러난 γ) 모두에서 현행 대비 확실성등가 개선 ≥ 0
  ③ 후회: 두 관점 가운데 불리한 쪽에서도, 그 관점의 최고 안 대비 손실 ≤ regret_max bp/년
"""
import argparse, os
import numpy as np, pandas as pd
from scipy.optimize import minimize

D = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--data", default=f"{D}/committee_decisions.csv"); ap.add_argument("--years", type=int, default=15)
ap.add_argument("--t-min", type=float, default=2.0); ap.add_argument("--regret-max", type=float, default=15.0)
ap.add_argument("--cost", type=float, default=10.0, help="편도 매매 비용 bp"); ap.add_argument("--make-data", action="store_true")
a = ap.parse_args()
ACT = np.round(np.arange(0.20, 0.701, 0.05), 2); SIG2 = 0.16 ** 2; MUBAR, BSIG = 0.05, 0.03; PHI = 0.95; G_IPS = 4.0
TRUE = dict(g=6.0, k=0.12, d=0.03, tau=0.0004)     # 생성에 쓴 '정답' — 학생에게는 알려 주지 않는 값(답안지 참고)


def market(n, rng):
    """신호 z(AR(1), 표준편차 1) · 월 초과수익 · 손실 국면 여부"""
    z = np.zeros(n + 1); e = rng.standard_normal(n + 1); u = rng.standard_normal(n)
    for t in range(1, n + 1): z[t] = PHI * z[t - 1] + np.sqrt(1 - PHI ** 2) * e[t]
    mu = MUBAR + BSIG * z[:n]                                                 # 결정 시점의 연율 기대초과수익
    r = mu / 12 + 0.16 / np.sqrt(12) * (-0.5 * e[1:] + np.sqrt(0.75) * u)     # 이번 달 수익 — 주가가 떨어지면 다음 신호는 대개 오른다
    lvl = np.cumprod(1 + r); dd = lvl / np.maximum.accumulate(lvl) - 1
    loss = np.r_[0, (dd[:-1] <= -0.15)].astype(float)                         # 결정 시점에 아는 손실 국면
    return mu, r, loss


def feats(mu, loss, prev):
    """행동별 특성 (n, 행동 수, 4): [a·μ, −σ²a²/2, −(a−prev)², −손실·a]"""
    A = np.broadcast_to(ACT[None, :], (len(mu), len(ACT)))
    return np.stack([A * mu[:, None], -0.5 * SIG2 * A ** 2, -(A - prev[:, None]) ** 2, -loss[:, None] * A], -1)


def make_data(path):
    rng = np.random.default_rng(4242); n = 180
    mu, r, loss = market(n, rng); prev = 0.45; rows = []
    th = np.array([1, TRUE["g"], TRUE["k"], TRUE["d"]]) / TRUE["tau"]
    for t in range(n):
        f = feats(mu[t:t + 1], loss[t:t + 1], np.array([prev]))[0] @ th
        p = np.exp(f - f.max()); p /= p.sum(); act = rng.choice(ACT, p=p)
        rows.append(dict(month=t + 1, exp_excess_ret=round(mu[t], 5), drawdown_state=int(loss[t]), prev_weight=prev,
                         weight=act, realized_excess_ret=round(r[t], 5)))
        prev = act
    pd.DataFrame(rows).to_csv(path, index=False)


if a.make_data or not os.path.exists(a.data):
    make_data(a.data)
df = pd.read_csv(a.data).tail(12 * a.years).reset_index(drop=True)
X = feats(df.exp_excess_ret.values, df.drawdown_state.values.astype(float), df.prev_weight.values)
y = np.searchsorted(ACT, df.weight.values - 1e-9)


def nll(b, cols):
    v = X[:, :, cols] @ b; v = v - v.max(1, keepdims=True)
    return -(v[np.arange(len(y)), y] - np.log(np.exp(v).sum(1))).sum()


def fit(cols):
    b0 = np.array([2500.0, 10000.0, 300.0, 50.0])[cols]
    r = minimize(nll, b0, args=(cols,), method="BFGS", options=dict(gtol=1e-6, maxiter=2000))
    # 수치 헤시안으로 표준오차
    k = len(cols); H = np.zeros((k, k)); h = np.maximum(np.abs(r.x) * 1e-4, 1e-3)
    for i in range(k):
        for j in range(k):
            ei = np.eye(k)[i] * h[i]; ej = np.eye(k)[j] * h[j]
            H[i, j] = (nll(r.x + ei + ej, cols) - nll(r.x + ei - ej, cols) - nll(r.x - ei + ej, cols) + nll(r.x - ei - ej, cols)) / (4 * h[i] * h[j])
    V = np.linalg.inv(H); return r.x, V, -r.fun


def ratio(b, V, i):
    """θ_i = b_i / b_0 와 델타법 표준오차"""
    g = np.zeros(len(b)); g[0] = -b[i] / b[0] ** 2; g[i] = 1 / b[0]
    return b[i] / b[0], float(np.sqrt(g @ V @ g))


print(f"=== 역강화학습 — 투자위원회의 숨은 보상 추정 · 자료 {len(df)}개월 · IPS 위험회피 γ = {G_IPS:g} ===")
print(f"    판정 기준(교육용 가정 · 바꿔 볼 수 있음): ① |t| ≥ {a.t_min:g} · ② 두 관점 모두 현행 대비 개선 · ③ 불리한 관점의 후회 ≤ {a.regret_max:g}bp/년")
print("[1] 관찰된 행동 — 평균 비중과 상황별 평균")
print(f"    전체 평균 {df.weight.mean():.1%} · 손실 국면 {df.weight[df.drawdown_state == 1].mean():.1%}({int(df.drawdown_state.sum())}개월)"
      f" · 평시 {df.weight[df.drawdown_state == 0].mean():.1%} · 비중을 바꾼 달 {np.mean(df.weight != df.prev_weight):.0%}")
hi = df.exp_excess_ret > df.exp_excess_ret.median()
print(f"    기대초과수익이 높은 달 평균 비중 {df.weight[hi].mean():.1%} · 낮은 달 {df.weight[~hi].mean():.1%}"
      f" · IPS(γ = 4)대로라면 평균 {np.clip(df.exp_excess_ret / (G_IPS * SIG2), 0.2, 0.7).mean():.1%}")

b, V, ll = fit([0, 1, 2, 3]); gh, gse = ratio(b, V, 1); kh, kse = ratio(b, V, 2); dh, dse = ratio(b, V, 3)
tau, tse = 1 / b[0], np.sqrt(V[0, 0]) / b[0] ** 2
print("[2] 역강화학습 추정 (최대 엔트로피 · 조건부 로짓) — 보상의 '척도'는 식별되지 않으므로 a·μ의 계수를 1로 고정한 비율을 읽는다")
print(f"    위험회피 γ̂ = {gh:5.2f} (표준오차 {gse:.2f}) · IPS γ = 4와의 차이 t = {(gh - G_IPS) / gse:+.2f}")
print(f"    관성 κ̂ = {kh:6.3f} ({kse:.3f}) · 손실 국면 회피 δ̂ = {dh:6.3f} ({dse:.3f}, t = {dh / dse:+.2f}) · 결정 잡음 τ̂ = {tau:.5f} ({tse:.5f})")
print(f"    해석: 손실 국면에서 주식 비중을 δ̂ ÷ (γ̂σ²) ≈ {dh / (gh * SIG2):.1%}p 더 줄인다 · 로그우도 {ll:.1f}")
b3, V3, ll3 = fit([0, 1, 2]); g3, g3se = ratio(b3, V3, 1)
print(f"[3] 특성을 빼면 — 손실 국면 항을 빼고 추정: γ̂ = {g3:5.2f} ({g3se:.2f}) · 로그우도 {ll3:.1f} (우도비 검정 통계량 {2 * (ll - ll3):.1f}, 5% 임계값 3.84)")
b2, V2, ll2 = fit([0, 1]); g2, g2se = ratio(b2, V2, 1)
print(f"    관성 항까지 빼면: γ̂ = {g2:5.2f} ({g2se:.2f}) · 로그우도 {ll2:.1f}")

# [4] 세 안의 미래 성과 — 10년 × 2,000개 경로
rng = np.random.default_rng(77); P, n = 2000, 120; C = a.cost / 1e4
th_hat = np.array([1, gh, kh, dh]) / tau


def policy(kind, mu, loss, prev, rng):
    if kind == "A":                      # 현행: 위원회 재량 = 추정된 보상 · 잡음 그대로
        f = feats(mu, loss, prev) @ th_hat; p = np.exp(f - f.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
        u = rng.random(len(mu))[:, None]; return ACT[(p.cumsum(1) < u).sum(1).clip(0, len(ACT) - 1)]
    g = G_IPS if kind == "C" else gh     # 규칙: 잡음과 손실 국면 항을 빼고 결정적으로 집행
    dd = dh if kind == "R" else 0.0      # 참고 R: B와 같되 손실 국면 회피를 그대로 둔 규칙
    f = feats(mu, loss, prev) @ np.array([1, g, kh, dd]); return ACT[f.argmax(1)]


out = {}
for kind in "ABCR":
    R = np.zeros((P, n)); prev = np.full(P, 0.45); TO = np.zeros(P); r2 = np.random.default_rng(5)
    mus, rs, ls = zip(*[market(n, np.random.default_rng(1000 + i)) for i in range(P)])
    mus, rs, ls = np.array(mus), np.array(rs), np.array(ls)
    for t in range(n):
        w = policy(kind, mus[:, t], ls[:, t], prev, r2)
        R[:, t] = w * rs[:, t] - C * np.abs(w - prev); TO += np.abs(w - prev); prev = w
    out[kind] = dict(R=R, to=TO.mean() / 10 * 100, w=None)


def ce(R, g):
    m = R.mean() * 12
    return (m - 0.5 * g * (R.reshape(-1).var() * 12)) * 1e4


NAMES = {"A": "A 현행 유지(위원회 재량)", "B": "B 드러난 선호로 규칙화", "C": "C IPS 명목 γ로 규칙화", "R": "참고: B + 손실 국면 회피 유지"}
print(f"[4] 세 안의 미래 10년 성과 (2,000개 경로 · 매매 비용 {a.cost:g}bp) — 확실성등가 = 연 초과수익 − (γ/2)·연 분산, bp/년")
print(f"    B: γ̂ = {gh:.2f}·관성 κ̂로 정한 규칙(손실 국면 항 · 잡음 제거) · C: γ = 4·관성 κ̂로 정한 규칙")
lens = {"IPS γ = 4": G_IPS, f"드러난 γ̂ = {gh:.2f}": gh}
tab = {k: {ln: ce(out[k]["R"], g) for ln, g in lens.items()} for k in "ABCR"}
for k in "ABCR":
    R = out[k]["R"]
    print(f"    {NAMES[k]:<18} 연 초과수익 {R.mean()*1200:5.2f}% · 연 변동성 {R.reshape(-1).std()*np.sqrt(12)*100:5.2f}% · 연 회전율 {out[k]['to']:4.0f}%"
          + "".join(f" · CE[{ln}] {tab[k][ln]:6.1f}" for ln in lens))
print("[5] 판정표")
okid = abs((gh - G_IPS) / gse) >= a.t_min
for k in "BC":
    imp = all(tab[k][ln] >= tab["A"][ln] for ln in lens)
    regret = max(max(tab[j][ln] for j in "ABC") - tab[k][ln] for ln in lens)
    m = lambda x: "통과" if x else "탈락"
    print(f"    {NAMES[k]:<18} ① {m(okid)} · ② {m(imp)} · ③ {m(regret <= a.regret_max)} (불리한 관점의 후회 {regret:.1f}bp/년)")
regA = max(max(tab[j][ln] for j in "ABC") - tab["A"][ln] for ln in lens)
print(f"    {NAMES['A']:<18} 기준 안 · 불리한 관점의 후회 {regA:.1f}bp/년")
