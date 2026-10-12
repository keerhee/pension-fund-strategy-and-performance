"""M8 GBI 에피소드별 화면 숫자 계산 — 강의본과 같은 가정(gbi_mc.py와 같은 seed·식).
사용: python3 tools/numbers_m8.py  (gbi_mc.py가 같은 폴더에 있으면 경로 표본을 그 함수로 만든다)"""
import json, math, pathlib
import numpy as np
root = pathlib.Path(__file__).resolve().parents[1] / "src/data"
def save(ep, d):
    (root / f"{ep}.numbers.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(ep, "ok")

r, lam, sig, T = 0.02, 0.06, 0.20, 10
Z = {0.95: 1.645, 0.70: 0.524, 0.30: -0.524}
GOALS = [("Safety", 6.0, 0.95), ("Market", 3.0, 0.70), ("Aspirational", 5.0, 0.30)]
def mix(w): return r + w * lam - 0.5 * w * w * sig * sig, w * sig
def K(G, z, m, s): return G * math.exp(-T * (m - z * s / math.sqrt(T)))
def wstar(z): return min(1, max(0, lam / sig**2 - z / (sig * math.sqrt(T))))

# ── E03a 필요 자본 (방법 1) ──
goals = []
for g, G, p in GOALS:
    z = Z[p]; w = wstar(z); m, s = mix(w)
    goals.append(dict(goal=g, G=G, p=p, z=z, w_raw=lam / sig**2 - z / (sig * math.sqrt(T)), w=w, m=m, s=s,
                      g=m - z * s / math.sqrt(T), K=K(G, z, m, s)))
port = {"GHP": (r, 0.0), "균형형": (0.045, 0.09), "주식": mix(1.0)}
nine = [[K(G, Z[p], *port[k]) for k in port] for _, G, p in GOALS]
tot = sum(x["K"] for x in goals); left = 10 - tot
# Market 계좌: K를 키우면 미달 꼬리가 줄어든다 — W_T 로그정규 밀도
gm = goals[1]; mu_l = gm["m"] * T; sd_l = gm["s"] * math.sqrt(T)
def dens(Kv, xs): return [math.exp(-(math.log(x / Kv) - mu_l) ** 2 / (2 * sd_l**2)) / (x * sd_l * math.sqrt(2 * math.pi)) for x in xs]
xs = [0.2 + i * 0.05 for i in range(140)]
from statistics import NormalDist
def p_hit(Kv): return 1 - NormalDist().cdf((math.log(gm["G"] / Kv) - mu_l) / sd_l)
Ks = [1.6, 1.9, gm["K"]]
save("M8E03a", dict(goals=goals, nine=nine, ports=list(port), total=tot, left=left,
     alloc=[goals[0]["K"], goals[1]["K"], goals[2]["K"] + left],
     xs=xs, dens=[dens(k, xs) for k in Ks], Ks=Ks, phit=[p_hit(k) for k in Ks],
     drift=math.exp(0.02 * T), sqrtT=math.sqrt(T)))

# ── E03b Das–Markowitz (원 논문 가상 자산) ──
mu = np.array([0.05, 0.10, 0.25]); sd = np.array([0.05, 0.20, 0.50])
C = np.diag(sd**2); C[1, 2] = C[2, 1] = 0.02
Ci = np.linalg.inv(C); one = np.ones(3)
gmv = Ci @ one / (one @ Ci @ one); v = Ci @ (mu - (one @ Ci @ mu) / (one @ Ci @ one) * one)
def wg(gm_): return gmv + v / gm_
def stats(w): return float(w @ mu), float(math.sqrt(w @ C @ w))
fr = []
for k in range(200):
    gm_ = 0.6 + k * 0.06
    m_, s_ = stats(wg(gm_)); fr.append(dict(s=s_, m=m_))
fr = sorted(fr, key=lambda x: x["s"])
accs = [("은퇴", -0.10, 0.05, 1.645), ("교육", -0.05, 0.15, 1.0364), ("상속", -0.15, 0.20, 0.8416)]
acc = []
for name, H, a, z in accs:
    lo, hi = 0.3, 50.0
    for _ in range(200):           # m − zσ = H 를 만족하는 γ (γ 작을수록 위험↑)
        mid = (lo + hi) / 2; m_, s_ = stats(wg(mid))
        if m_ - z * s_ >= H: hi = mid
        else: lo = mid
    w = wg(hi); m_, s_ = stats(w)
    acc.append(dict(name=name, H=H, alpha=a, z=z, gamma=hi, w=[float(x) for x in w], m=m_, s=s_))
agg_w = 0.6 * wg(acc[0]["gamma"]) + 0.2 * wg(acc[1]["gamma"]) + 0.2 * wg(acc[2]["gamma"])
agg_gamma = 1 / (0.6 / acc[0]["gamma"] + 0.2 / acc[1]["gamma"] + 0.2 / acc[2]["gamma"])
am, as_ = stats(agg_w)
save("M8E03b", dict(assets=[dict(k="채권형", m=0.05, s=0.05), dict(k="저위험 주식형", m=0.10, s=0.20), dict(k="고위험 주식형", m=0.25, s=0.50)],
     frontier=fr, accounts=acc, agg=dict(w=[float(x) for x in agg_w], gamma=agg_gamma, m=am, s=as_),
     check=dict(w=[0.6, 0.3, 0.1], m=float(np.array([0.6, 0.3, 0.1]) @ mu), s=float(math.sqrt(np.array([0.6, 0.3, 0.1]) @ C @ np.array([0.6, 0.3, 0.1]))))))

# ── E03c 몬테카를로 — 경로 표본 (gbi_mc.py와 같은 식 · seed 2026) ──
rng = np.random.default_rng(2026)
e = rng.standard_normal((100_000, T))
R = np.exp(r + lam - 0.5 * sig * sig + sig * e) - 1
RG = math.exp(r) - 1; w = 0.6708
Wp = np.empty((100_000, T + 1)); Wp[:, 0] = 1.0
for t in range(T): Wp[:, t + 1] = Wp[:, t] * (w * (1 + R[:, t]) + (1 - w) * (1 + RG))
growth = Wp[:, -1]
def kmin(G, p):
    lo, hi = 0.0, G * 10
    for _ in range(60):
        mid = (lo + hi) / 2
        if np.mean(mid * growth >= G) >= p: hi = mid
        else: lo = mid
    return hi
Kmc = kmin(3.0, 0.70)
sample = (Wp[:240] * Kmc).round(3).tolist()
hit = float(np.mean(Kmc * growth >= 3.0))
save("M8E03c", dict(K_mc=Kmc, hit=hit, paths=sample, se=math.sqrt(0.7 * 0.3 / 10000),
     toy=[1.4005, 1.4723, 2.1306, 2.2818, 5.7166, 2.4915, 0.8016, 1.9634, 1.5233, 0.9240],
     table=[dict(goal="Safety 6억 · 95%", Kc=4.91, Km=4.91, pk="100.0%", Kt=4.91),
            dict(goal="Market 3억 · 70%", Kc=2.24, Km=2.26, pk="69.5%", Kt=2.24),
            dict(goal="Aspirational 5억 · 30%", Kc=1.97, Km=1.97, pk="30.0%", Kt=1.99)],
     cppi=dict(breach_n=0.019, breach_t=0.033, p6=0.981, p9=0.832, p14=0.645, med=18.0),
     grid=dict(K=7.1, w=0.60, pS=0.958, pM=0.741, pA=0.309, left=2.9)))

# ── E04 Floor 만들기 ──
def ann(c, n, rr): return c * (1 - (1 + rr) ** -n) / rr
rb65 = ann(0.24, 20, 0.02); rb45 = rb65 / 1.02**20
floor_curve = [dict(r=x / 1000, F=ann(0.24, 25, x / 1000)) for x in range(10, 41)]
save("M8E04", dict(rb65=rb65, rb45=rb45, disc=1.02**20, floor_curve=floor_curve,
     F15=ann(0.24, 25, 0.015), F25=ann(0.24, 25, 0.025), F35=ann(0.24, 25, 0.035), lee_floor=3.50, lee_cushion=1.50))

# ── E05 쿠션과 승수 ──
As = [x / 10 for x in range(40, 121)]
wcur = lambda m: [dict(A=a, w=min(1.0, max(0.0, m * (a - 5) / a))) for a in As]
save("M8E05", dict(F=5, m4=wcur(4), m2=wcur(2),
     demo=[dict(y=1, R=-0.094, W0=10.0, F=7.37, C=2.63, E=7.89, W1=9.30), dict(y=2, R=0.114, W0=9.30, F=7.52, C=1.78, E=5.35, W1=9.99),
           dict(y=3, R=-0.273, W0=9.99, F=7.67, C=2.32, E=6.97, W1=8.15)],
     var=[dict(x=0.10, m=10), dict(x=0.20, m=5), dict(x=0.33, m=3), dict(x=0.50, m=2)],
     trap=[dict(m=3, med=6.10, worst=2.24, breach=0.0, trap=0.014), dict(m=6, med=6.45, worst=2.12, breach=0.019, trap=0.207)]))

# ── E06 운용 규칙 ──
save("M8E06", dict(reset=[dict(k="벌었을 때", A=11.5, F=9.2, psp_reset=0.60, psp_no=min(1, 3 * (11.5 - 8) / 11.5)),
                          dict(k="잃었을 때", A=8.5, F=6.8, psp_reset=0.60, psp_no=3 * (8.5 - 8) / 8.5)],
     var=[dict(k="평상시", vol=0.18, two=0.104, E=4.8), dict(k="불안기", vol=0.36, two=0.208, E=2.4)]))

# ── E07 한국 제도 (금감원 2025 말 공시) ──
save("M8E07", dict(pension=[dict(k="DB 확정급여", v=228.9, sh=0.457, ret=3.53), dict(k="DC 확정기여", v=141.6, sh=0.282, ret=8.47),
                            dict(k="IRP 개인형", v=130.9, sh=0.261, ret=9.44)],
     total=501.4, guar_share=0.754, guar_ret=3.09, perf_ret=16.80, default_stable=0.854, default_aum=53.3,
     tdf2025=-14.0, tdf2045=-16.8, tdf_fee=0.59, robo=1.276))

# ── E08 H대 ──
save("M8E08", dict(fund=5000, x=20, y=30, z=4.5, floor_B=1536, floor_C=1736,
     B=dict(liq=3108, cushion=1572, m=1.53, pe_share=22.5), C=dict(liq=2448, cushion=712, m=4.2, pe_share=35.5),
     survive=dict(x20=13, x60=2)))
