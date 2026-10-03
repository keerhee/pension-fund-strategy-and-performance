"""W07 M9 정본 시뮬레이션 — 이순자 씨(가상, 65세·금융자산 5억·NPS 월 150만·생활비 월 300만)
단위 억 원(2026 실질). 가정: 주식(PSP) 연 로그수익 m 6%·σ 20%(강의 K 예제와 같은 자본시장 가정),
GHP(물가연동국채) 실질 1.5% = Floor 할인율, 월간 리밸런싱, 레버리지 금지(위험자산 ≤ 100%), 1,000 경로, seed 2026.
Floor = 남은 생활비 부족분(연 1,800만, 88세까지)의 현재가치. 기간 65→75세(10년)."""
import json, numpy as np
R, MU, SIG, N, SEED, T, LIFE = 0.015, 0.06, 0.20, 1000, 2026, 10, 23
C = 0.18                       # (300 − 150)만 × 12 = 1,800만 = 0.18억
A0, MKT, ASP = 5.0, 1.0, 0.5
def floor(k_months):           # 잔여 연금 현가 (월 단위 근사: 연금 연간지급을 월로 나눔)
    n = LIFE*12 - k_months
    if n <= 0: return 0.0
    rm = (1+R)**(1/12)-1
    return C/12 * (1-(1+rm)**-n)/rm
rm = (1+R)**(1/12)-1
F0 = floor(0)
rng = np.random.default_rng(SEED)
Z = rng.standard_normal((N, T*12))
def run(rule, m=3, shock=False):
    A = np.full(N, A0); trap = np.zeros(N, bool); breach = np.zeros(N, bool); F_reset = None
    for k in range(T*12):
        F = floor(k)
        if rule == "cppi": w = np.clip(m*(A-F)/A, 0, 1)
        elif rule == "fixed": w = np.full(N, 0.4)
        elif rule == "flex":            # Flexicure: 매년 초 F_t = max(0.8A, 필수 Floor), m = TDF 주식비중(65세 20%)/0.2 = 1
            if k % 12 == 0:
                F_reset = np.maximum(0.8*A, F); mm = 0.20/0.2
            w = np.clip(mm*(A-F_reset)/A, 0, 1)
        lr = (MU - SIG**2/2*0)/12 + SIG/np.sqrt(12)*Z[:, k]    # MU는 로그 중앙값 성장률
        if shock and k < 12: lr = np.full(N, np.log(0.8)/12)
        A = A*(w*np.exp(lr) + (1-w)*(1+rm)) - C/12
        A = np.maximum(A, 0)
        cush = (A - floor(k+1))/np.maximum(A, 1e-9)
        breach |= A < floor(k+1) - 1e-9
        trap |= (rule == "cppi") & (cush < 0.01)
    FT = floor(T*12); S = A - FT
    w10 = np.sort(A)[:N//10].mean()
    return dict(median=float(np.median(A)), worst10=float(w10), breach=float(breach.mean()), trap=float(trap.mean()),
                p_market=float((S >= MKT).mean()), p_asp=float((S >= MKT+ASP).mean()), FT=FT)
out = dict(F0=F0, cushion0=A0-F0, FT=floor(T*12), assumptions=dict(R=R, MU=MU, SIG=SIG, N=N, SEED=SEED, T=T, C=C))
out["cppi"] = {m: run("cppi", m) for m in range(1, 7)}
out["fixed40"] = run("fixed"); out["flex"] = run("flex")
out["shock2022"] = {m: run("cppi", m, shock=True) for m in [2, 3, 6]}
out["shock2022"]["fixed40"] = run("fixed", shock=True)
# 이순자 Safety 미달(정적 GHP 전액이면 0) · 필요 자본 K(10년 뒤 의료 1억 70% · 손주 0.5억 30%, 주식 m6% σ20%)
from math import exp, sqrt
z = {0.7: 0.524, 0.3: -0.524}
def K(G, p, m, s, T=10): return G*exp(-m*T + z[p]*s*sqrt(T))
out["K"] = dict(market_bal=K(1.0, 0.7, 0.045, 0.09), market_eq=K(1.0, 0.7, 0.06, 0.2), market_ghp=1.0/(1+R)**10,
                asp_eq=K(0.5, 0.3, 0.06, 0.2), asp_bal=K(0.5, 0.3, 0.045, 0.09))
json.dump(out, open("w9_sim_results.json", "w"), indent=1, ensure_ascii=False)
print(f"F0 {F0:.3f} cushion {A0-F0:.3f} FT {floor(120):.3f}")
for m, r in out["cppi"].items(): print("m", m, {k: round(v, 3) for k, v in r.items()})
print("fixed40", {k: round(v, 3) for k, v in out["fixed40"].items()})
print("flex", {k: round(v, 3) for k, v in out["flex"].items()})
for k, r in out["shock2022"].items(): print("shock", k, {kk: round(v, 3) for kk, v in r.items()})
print({k: round(v, 3) for k, v in out["K"].items()})
