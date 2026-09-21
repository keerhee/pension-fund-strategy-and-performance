#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M9 IC 케이스 — 판정 조건 계산 (w7m9_build.py 의 CSV → w7m9_results.json · compute_log.txt)

케이스 1 (K퇴직연금 사업자 상품심의위원회) Flexicure형 디폴트옵션 — Floor x · 승수 m · 수수료 c
  조건 ① 목표 미달 확률   P(W_T < G_S) ≤ 5%  (Safety 버킷 — 강의 1교시)
  조건 ② Cash Trap        PSP 비중 < 5% 로 락인된 채 만기 도달할 확률 ≤ 10% (m 이 클수록 커진다 — 강의 2교시)
  조건 ③ 수수료 잠식      수수료 차감 후 P(W_T ≥ G_M) ≥ 70%, G_M = 원리금보장 3.09% 10년 복리 (Market 버킷)
  조건 ④ 2022형 충격      주식 −20% · 금리 +300bp 에서 Floor 위반율 ≤ 1% — Floor 를 GHP 가격으로 정의할 때와 고정 원금으로 정의할 때
  조건 ⑤ 거버넌스         "보장" 표현 금지 · 설명 3문장 · 재심 트리거 — 표결 조건(계산 대상 아님)
케이스 2 (H대학교 발전기금 투자위원회) Yale 모델 — 비유동 대체 상한 x · 안전 유동자산 하한 y · 지출률 z
  조건 ① 실질 지평         2022형 충격 + 목돈 인출 + 캐피탈콜 아래 비유동 자산을 팔지 않고 버티는 연수 ≥ 락업 7년
  조건 ② 지출 Floor        현행 지출 4.0% ≤ z ≤ 실질 기대수익 − 0.5%p (교육용 CMA)
  조건 ③ 접근권            직접 PE·VC = 전담 인력 ≥ 3 · 매니저 15개 분산(최소 출자 100억 × 15) — 미충족이면 펀드오브펀드·세컨더리
  조건 ④ 충격 후 지출 유지  충격 후 3년간 매도 없이 고정 지출·목돈을 안전 유동자산으로 대는 확률 ≥ 95% → y
  조건 ⑤ 거버넌스           분모 효과 시 신규 약정 중단 · 연 1회 재계산 — 표결 조건
"""
import json, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/fml_w7m9_params.csv").set_index("key").value
f = lambda k: float(P[k])
panel = pd.read_csv(f"{D}/fml_w7m9_panel_sim.csv")
grid = pd.read_csv(f"{D}/fml_w7m9_cppi_grid.csv")
cma = pd.read_csv(f"{D}/fml_w7m9_cma.csv").set_index("asset")
alloc = pd.read_csv(f"{D}/fml_w7m9_endow_alloc.csv").set_index("illiq_cap_pct")
cfl = pd.read_csv(f"{D}/fml_w7m9_endow_cashflow.csv")
sc = pd.read_csv(f"{D}/fml_w7m9_scenarios.csv").set_index("scenario")
log = []
def L(s): log.append(s); print(s)
res = {"asof": P["asof"], "case1": {}, "case2": {}}
rng = np.random.default_rng(int(f("panel_seed")))

# ═════════════════════════════════════════════════════════════════════════════
# 케이스 1 — Flexicure형 디폴트옵션 (월간 CPPI, 12개월 블록 부트스트랩)
# ═════════════════════════════════════════════════════════════════════════════
T = int(12 * (f("retire_age") - f("age0")))
NP = int(f("n_path_cppi"))
A0, GS = f("a0"), f("a0") * f("g_s_mult")
GM = f("a0") * (1 + f("market_alt_ret_pct") / 100) ** (T / 12)
Y0 = f("ghp_y0")
eq_m = panel.eq_ret.values; dy_m = np.r_[0, np.diff(panel.yield10.values)]
nb = len(eq_m) // 12
eq_blocks = eq_m[: nb * 12].reshape(nb, 12); dy_blocks = dy_m[: nb * 12].reshape(nb, 12)


def draw_paths(n, shock=False):
    """(n, T) 주식 수익률과 금리 변화. shock=True 면 첫 12개월을 2022형(주식 −20% · 금리 +300bp)으로 고정"""
    idx = rng.integers(0, nb, size=(n, T // 12))
    eq = eq_blocks[idx].reshape(n, T); dy = dy_blocks[idx].reshape(n, T)
    if shock:
        eq[:, :12] = np.array([-0.03, -0.02, -0.08, -0.04, 0.02, -0.06, 0.01, -0.03, 0.03, -0.02, 0.02, 0.005])
        dy[:, :12] = f("shock_2022_dy_bp") / 100
    return eq, dy


def ghp_prices(dy):
    """무이표채(만기 T) 가격 경로 P_0..P_T — 금리 경로 y_t = y0 + Σdy"""
    y = np.zeros((dy.shape[0], T + 1)); y[:, 0] = Y0
    for t in range(T):
        y[:, t + 1] = np.clip(y[:, t] + dy[:, t] + 0.012 * (Y0 - y[:, t]), 0.3, None)   # 패널과 같은 평균회귀(반감기 약 5년)
    tau = (T - np.arange(T + 1)) / 12
    return np.exp(-y / 100 * tau)


def cppi(eq, dy, x, m, fee, fixed_floor=False):
    """월간 수익률 · REBAL 개월마다 w = m(W−F)/W 로 재조정(그 사이는 보유). Cash Trap = 쿠션/W < 임계가 한 번이라도 발생"""
    n = eq.shape[0]; Pz = ghp_prices(dy); RB = int(f("rebal_months")); ct = f("cash_trap_cushion")
    W = np.full(n, A0); breach = np.zeros(n, bool); trapped = np.zeros(n, bool); w0 = None
    Hp = np.zeros(n); Gp = np.zeros(n)
    fg = (1 - fee / 100 / 12) ** (-(T - np.arange(T + 1)))     # 수수료 그로스업 — 만기에 수수료 차감 후 x·G_S 가 남으려면 지금 GHP 에 이만큼 있어야 한다
    for t in range(T):
        F = x * GS * (Pz[:, 0] if fixed_floor else Pz[:, t]) * fg[t]
        if t % RB == 0:
            w = np.clip(m * (W - F) / W, 0, 1); Hp = w * W; Gp = W - Hp
            if t == 0: w0 = w.copy()
        r_g = Pz[:, t + 1] / Pz[:, t] - 1
        Hp = Hp * (1 + eq[:, t]) * (1 - fee / 100 / 12); Gp = Gp * (1 + r_g) * (1 - fee / 100 / 12); W = Hp + Gp
        Ft = x * GS * (Pz[:, 0] if fixed_floor else Pz[:, t + 1]) * fg[t + 1]
        breach |= W < Ft * 0.999
        trapped |= (W - Ft) / W < ct
    return W, trapped, breach, w0


L("=== 케이스 1 — Flexicure형 디폴트옵션: Floor x · 승수 m · 수수료 c ===")
L(f"프로필(교육용) — {int(f('age0'))}세 → {int(f('retire_age'))}세, 지평 {T//12}년 · 초기 자산 1.00 · Safety 목표 G_S = {GS:.2f} · Market 목표 G_M = 1.0309^10 = {GM:.3f} (원리금보장 3.09%, 공시)")
L(f"Floor_0 = x × G_S × P(0,10) — x 0.80/0.90/1.00 → {0.8*GS*np.exp(-Y0/100*10):.3f} / {0.9*GS*np.exp(-Y0/100*10):.3f} / {1.0*GS*np.exp(-Y0/100*10):.3f} (금리 {Y0}%) → 초기 쿠션 {1-0.8*GS*np.exp(-Y0/100*10):.1%} / {1-0.9*GS*np.exp(-Y0/100*10):.1%} / {1-1.0*GS*np.exp(-Y0/100*10):.1%}")
eqN, dyN = draw_paths(NP)
eqS, dyS = draw_paths(NP, shock=True)
def buyhold(eq, dy, w, fee):
    Pz = ghp_prices(dy); W = np.full(eq.shape[0], A0)
    for t in range(T):
        W = W * (1 + w * eq[:, t] + (1 - w) * (Pz[:, t + 1] / Pz[:, t] - 1)) * (1 - fee / 100 / 12)
    return W
bh = []
for w, fee in [(1.0, 0.0), (0.6, 0.5), (0.6, 0.8), (0.4, 0.5), (0.0, 0.0)]:
    W = buyhold(eqN, dyN, w, fee); Ws = buyhold(eqS, dyS, w, fee)
    bh.append({"w_eq": w, "fee_pct": fee, "median_W": float(np.median(W)), "p10_W": float(np.quantile(W, .1)), "p_safety_fail": float((W < GS).mean()), "p_market": float((W >= GM).mean()), "shock_p_safety_fail": float((Ws < GS).mean())})
    L(f"[참고 — 고정 배분(TDF형) 주식 {w:.0%} · 수수료 {fee}%] 중위 {bh[-1]['median_W']:.2f} · 하위10% {bh[-1]['p10_W']:.2f} · Safety 미달 {bh[-1]['p_safety_fail']:.1%} (2022형 시 {bh[-1]['shock_p_safety_fail']:.1%}) · Market {bh[-1]['p_market']:.0%}")
res["case1"]["buyhold"] = bh
rows = []
for x in sorted(grid.floor_x.unique()):
    for m in sorted(grid.m.unique()):
        for fee in sorted(grid.fee_pct.unique()):
            W, trap, br, w0 = cppi(eqN, dyN, x, m, fee)
            Ws, traps, brs, _ = cppi(eqS, dyS, x, m, fee)
            _, _, brf, _ = cppi(eqS, dyS, x, m, fee, fixed_floor=True)
            r = dict(floor_x=float(x), m=int(m), fee_pct=float(fee),
                     p_safety_fail=float((W < GS).mean()), p_cash_trap=float(trap.mean()), p_market=float((W >= GM).mean()),
                     median_W=float(np.median(W)), p10_W=float(np.quantile(W, 0.10)), p90_W=float(np.quantile(W, 0.90)),
                     w0=float(w0.mean()), breach_normal=float(br.mean()),
                     shock_breach_ghp=float(brs.mean()), shock_breach_fixed=float(brf.mean()), shock_cash_trap=float(traps.mean()),
                     shock_median_W=float(np.median(Ws)))
            r["c1"] = r["p_safety_fail"] <= f("safety_fail_max"); r["c2"] = r["p_cash_trap"] <= f("cash_trap_max")
            r["c3"] = r["p_market"] >= f("market_min"); r["c4"] = r["shock_breach_ghp"] <= f("breach_max")
            r["pass_all"] = bool(r["c1"] and r["c2"] and r["c3"] and r["c4"])
            rows.append(r)
G = pd.DataFrame(rows)
for x in sorted(G.floor_x.unique()):
    L(f"[Floor x = {x:.2f}] 초기 PSP 비중(m=1..6, 수수료 0.5%): " + " · ".join(f"{G[(G.floor_x==x)&(G.fee_pct==0.5)&(G.m==m)].w0.iloc[0]*100:.0f}%" for m in range(1, 7)))
    for m in range(1, 7):
        g = G[(G.floor_x == x) & (G.m == m)]
        b = g[g.fee_pct == 0.5].iloc[0]
        L(f"   m={m}: ① 미달 {b.p_safety_fail:.1%} · ② Cash Trap {b.p_cash_trap:.1%} · ③ Market(수수료 0.5/0.8/1.0/1.2/1.5) " + "/".join(f"{v:.0%}" for v in g.sort_values('fee_pct').p_market) + f" · ④ 충격 위반(GHP/고정) {b.shock_breach_ghp:.1%}/{b.shock_breach_fixed:.0%} · 중위 {b.median_W:.2f} 하위10% {b.p10_W:.2f}")
gap = []
for m in sorted(grid.m.unique()):
    eqG = eqN.copy(); eqG[:, 0] = f("gap_shock")
    Wg, tg, bg, _ = cppi(eqG, dyN, 1.0, m, 0.8)
    gap.append({"m": int(m), "floor_x": 1.0, "fee_pct": 0.8, "breach": float(bg.mean()), "cash_trap": float(tg.mean()), "loss_to_breach_pct": 100.0 / m})
    L(f"[참고 — 갭 스트레스 한 달 {f('gap_shock'):.0%}, x=1.0] m={m}: Floor 위반 {gap[-1]['breach']:.0%} · Cash Trap {gap[-1]['cash_trap']:.0%} (한 번에 깨지는 손실 = 1/m = {100/m:.0f}%)")
res["case1"]["gap_stress"] = gap
ok = G[G.pass_all]
L(f"[통과 조합] {len(ok)}개 — Floor {sorted(ok.floor_x.unique())} · m {sorted(ok.m.unique())} · 수수료 {sorted(ok.fee_pct.unique())}")
# 기본 답 — 통과 조합 중 x 는 Safety 를 지키는 최소 Floor 가 아니라 '통과하는 x 중 쿠션이 가장 큰 것'이 아니라: 통과하는 조합의 (x, m 상한, 수수료 상한)
if len(ok):
    x_star = sorted(ok.floor_x.unique())
    dflt = {}
    for x in x_star:
        o = ok[ok.floor_x == x]
        dflt[str(x)] = {"m_max": int(o.m.max()), "fee_max": float(o[o.m == o.m.max()].fee_pct.max()) if len(o) else None,
                        "fee_max_any_m": float(o.fee_pct.max())}
    res["case1"]["passing_by_floor"] = dflt
    L("[통과 조합 요약] " + " · ".join(f"x={k}: m ≤ {v['m_max']}, 수수료 ≤ {v['fee_max_any_m']}%" for k, v in dflt.items()))
    # 판정 순서(사전 규칙): Safety 우선 — 통과하는 x 중 가장 높은 Floor → 그 x 에서 통과하는 최대 m → 그 (x, m) 에서 통과하는 최대 수수료
    xd = max(ok.floor_x); od = ok[ok.floor_x == xd]; md = int(od.m.max()); cd = float(od[od.m == md].fee_pct.max())
    res["case1"]["default"] = {"floor_x": xd, "m_max": md, "fee_max": cd}
    L(f"[기본 답] Floor x = {xd:.2f}(Safety 목표의 {xd:.0%}) · 승수 m ≤ {md} · 연 총보수 ≤ {cd}% — 조건부 승인. x=1.00 은 쿠션이 얇아 ③ Market 미달, x=0.80 은 m ≥ 2 에서 ① 미달 초과, m ≥ 3 은 x=0.9 에서 ① 초과, 수수료 0.8% 이상은 ③ 미달")
else:
    L("[기본 답] 통과 조합 없음 — 부결(재상정 조건: 수수료·승수 재설계)")
# 수수료 잠식 참고 — 30년 복리
fe = [{"fee_pct": c, "erosion_30y": 1 - (1 - c / 100) ** 30, "erosion_10y": 1 - (1 - c / 100) ** 10} for c in [0.3, 0.5, 0.8, 1.0, 1.2, 1.5]]
L("[참고 — 수수료 잠식] " + " · ".join(f"{e['fee_pct']}% → 10년 {e['erosion_10y']:.0%} · 30년 {e['erosion_30y']:.0%}" for e in fe))
res["case1"].update({"T_months": T, "G_S": GS, "G_M": GM, "y0": Y0, "grid": G.to_dict("records"), "fee_erosion": fe,
                     "thresholds": {k: f(k) for k in ["safety_fail_max", "cash_trap_max", "market_min", "breach_max"]}})

# ═════════════════════════════════════════════════════════════════════════════
# 케이스 2 — H대학교 발전기금 (연간, 30년, 연 수익률 부트스트랩)
# ═════════════════════════════════════════════════════════════════════════════
L("\n=== 케이스 2 — H대학교 발전기금 5,000억: 비유동 대체 상한 x · 안전 유동자산 하한 y · 지출률 z ===")
W0 = f("endow_bn_krw"); INF = f("infl_pct") / 100
ZL = [float(z) for z in str(P["z_list"]).split("|")]; YL = [int(float(y)) for y in str(P["y_list"]).split("|")]
ann = lambda s: (1 + s.values[: nb * 12].reshape(nb, 12)).prod(1) - 1
A_eq, A_bd, A_cs, A_pe, A_pr, A_pi = ann(panel.eq_ret), ann(panel.bond_gov_ret), ann(panel.rf), ann(panel.alt_pe_ret), ann(panel.alt_pe_rep_ret), ann(panel.cpi)
L(f"패널 연 수익률(40년) — 주식 {A_eq.mean():.1%}/{A_eq.std():.1%} · 국채 {A_bd.mean():.1%} · 현금 {A_cs.mean():.1%} · 비유동 대체(실제) {A_pe.mean():.1%}/{A_pe.std():.1%} · 보고 기준 σ {A_pr.std():.1%}")
XS = sorted(alloc.index)
mu = {"eq": cma.mu_pct["eq"], "bond_gov": cma.mu_pct["bond_gov"], "cash": cma.mu_pct["cash"], "alt_pe": cma.mu_pct["alt_pe"], "alt_pe_direct": cma.mu_pct["alt_pe_direct"]}

# ── 조건 ③ 접근권 ──────────────────────────────────────────────────────────
acc = []
for x in XS:
    alt_bn = x / 100 * W0
    ok3 = (f("staff_h") >= f("staff_min")) and (alt_bn >= f("mgr_min") * f("min_commit_bn"))
    acc.append({"illiq_cap_pct": int(x), "alt_bn": alt_bn, "managers_affordable": int(alt_bn // f("min_commit_bn")), "staff": int(f("staff_h")),
                "direct_ok": bool(ok3), "vehicle": "직접 PE·VC" if ok3 else ("펀드오브펀드 · 세컨더리" if x > 0 else "—")})
L(f"[조건 ③ 접근권] 전담 인력 {int(f('staff_h'))}명 < {int(f('staff_min'))} → 직접 PE·VC 불가(전 구간). 매니저 15개 분산에 필요한 배분 = {f('mgr_min')*f('min_commit_bn'):,.0f}억 = 기금의 {f('mgr_min')*f('min_commit_bn')/W0:.0%} → x ≥ 30 이어야 규모 요건만 충족")
res["case2"]["access"] = acc

# ── 조건 ② 지출 Floor(결정론) ────────────────────────────────────────────────
sp = []
for x in XS:
    a = alloc.loc[x]
    mu_nom = (a.w_eq * mu["eq"] + a.w_bond_gov * mu["bond_gov"] + a.w_cash * mu["cash"] + a.w_alt_pe * mu["alt_pe"]) / 100
    mu_nom_direct = (a.w_eq * mu["eq"] + a.w_bond_gov * mu["bond_gov"] + a.w_cash * mu["cash"] + a.w_alt_pe * mu["alt_pe_direct"]) / 100
    z_max = mu_nom - f("infl_pct") - f("spend_margin_pp"); z_min = f("current_spend_bn") / W0 * 100
    feas = [z for z in ZL if z_min <= z <= z_max]
    sp.append({"illiq_cap_pct": int(x), "mu_nominal": mu_nom, "mu_real": mu_nom - f("infl_pct"), "mu_real_direct": mu_nom_direct - f("infl_pct"),
               "z_max": z_max, "z_min": z_min, "z_feasible": feas, "c2": len(feas) > 0})
    L(f"[조건 ② 지출] x={x:>2}%: μ 명목 {mu_nom:.2f}% · 실질 {mu_nom-f('infl_pct'):.2f}% → z ≤ {z_max:.2f}% (직접 PE 접근 시 실질 {mu_nom_direct-f('infl_pct'):.2f}%) · 현행 지출 4.0% 이상 가능한 z = {feas}")
res["case2"]["spend_rule"] = sp

# ── 조건 ① 실질 지평(락업 생존 연수, 결정론 스트레스) ─────────────────────────
s22 = sc.loc["2022형"]
lk = []
for x in XS:
    a = alloc.loc[x]
    liq = W0 * (a.w_eq / 100 * (1 + s22.eq_ret_pct / 100) + a.w_bond_gov / 100 * (1 + s22.bond_gov_ret_pct / 100) + a.w_cash / 100 * (1 + s22.cash_ret_pct / 100))
    alt_target = x / 100 * W0
    calls = f("unfunded_share") * alt_target / f("call_years")
    years = 0; path = []
    for t in range(1, 31):
        out = f("current_spend_bn") + (f("lump_bn") if t == int(f("lump_year")) else 0) + (calls if t <= f("call_years") else 0)
        liq = liq * (1 + INF) - out          # 스트레스: 유동자산은 실질 0% (명목 = 물가)
        path.append(liq)
        if liq <= 0: break
        years = t
    lk.append({"illiq_cap_pct": int(x), "liquid_after_shock_bn": float(path[0] + f("current_spend_bn") + calls) if path else None,
               "annual_outflow_bn": float(f("current_spend_bn") + calls), "calls_bn_per_year": calls, "survival_years": years, "c1": years >= f("lockup_years")})
    L(f"[조건 ① 실질 지평] x={x:>2}%: 충격 후 유동자산 {lk[-1]['liquid_after_shock_bn']:,.0f}억 · 연 유출 {f('current_spend_bn'):.0f}+캐피탈콜 {calls:.0f}(+3년차 목돈 {f('lump_bn'):.0f}) → 매도 없이 {years}년 {'≥' if years>=f('lockup_years') else '<'} 락업 {int(f('lockup_years'))}년 → {'통과' if years>=f('lockup_years') else '탈락'}")
res["case2"]["lockup"] = lk

# ── 조건 ④ 안전 유동자산 하한 y — 충격 후 3년 매도 없이 고정 지출·목돈 ───────────
need = sum(cfl.fixed_spend_bn_krw[: int(f("no_sell_years"))]) + f("lump_bn")
y_req = need / W0 * 100
L(f"[조건 ④ 안전 유동자산 — 산수] 충격 후 {int(f('no_sell_years'))}년 확정 유출 = 고정 지출 {sum(cfl.fixed_spend_bn_krw[:3]):,.0f} + 목돈 {f('lump_bn'):.0f} = {need:,.0f}억 = 기금의 {y_req:.1f}%")
NPE = int(f("n_path_endow")); H = int(f("horizon_endow"))
rng2 = np.random.default_rng(int(f("panel_seed")) + 1)      # 케이스 2 는 별도 난수열(케이스 1 의 경로 수와 무관하게 재현)
idx = rng2.integers(0, nb, size=(NPE, H))

def mc(x, z, y_floor=None, shock=True):
    a = alloc.loc[x]; w = np.array([a.w_eq, a.w_bond_gov, a.w_cash, a.w_alt_pe]) / 100
    R = np.stack([A_eq[idx], A_bd[idx], A_cs[idx], A_pe[idx]], -1)      # (NPE, H, 4)
    PI = A_pi[idx]
    if shock:
        R[:, 0, :] = np.array([s22.eq_ret_pct, s22.bond_gov_ret_pct, s22.cash_ret_pct, s22.alt_pe_true_ret_pct]) / 100; PI[:, 0] = INF
    W = np.full(NPE, W0); S = np.full(NPE, f("current_spend_bn")); Wr = np.zeros((NPE, H)); Sk = np.ones(NPE, bool); Sk3 = np.ones(NPE, bool)
    safe = np.full(NPE, (y_floor / 100 * W0) if y_floor is not None else 0.0); forced = np.zeros(NPE, bool)
    defl = np.ones(NPE)
    for t in range(H):
        rp = (R[:, t, :] * w).sum(1)
        S = f("smooth_w") * S * (1 + PI[:, t]) + (1 - f("smooth_w")) * z / 100 * W
        lump = f("lump_bn") if t + 1 == int(f("lump_year")) else 0.0
        W = W * (1 + rp) - S - lump
        defl *= (1 + PI[:, t]); Wr[:, t] = W / defl
        fixed_t = cfl.fixed_spend_bn_krw[t]
        Sk &= S >= fixed_t * 0.999
        if t < int(f("no_sell_years")): Sk3 &= S >= fixed_t * 0.999
        if y_floor is not None and t < int(f("no_sell_years")):
            r_safe = (a.w_bond_gov * R[:, t, 1] + a.w_cash * R[:, t, 2]) / (a.w_bond_gov + a.w_cash)
            safe = safe * (1 + r_safe) - S - lump
            forced |= safe < 0
    return {"p_real_keep": float((Wr[:, -1] >= W0).mean()), "p_spend_keep": float(Sk.mean()), "median_real_W30": float(np.median(Wr[:, -1])),
            "p10_real_W30": float(np.quantile(Wr[:, -1], 0.1)), "p_forced_sale": float(forced.mean()) if y_floor is not None else None,
            "p_spend_keep_3y": float(Sk3.mean()), "p_no_forced_and_spend": float((~forced & Sk3).mean()) if y_floor is not None else None}

mcs = []
for x in XS:
    for z in ZL:
        r = mc(x, z, shock=False); rs = mc(x, z, shock=True)
        r.update({"illiq_cap_pct": int(x), "z_pct": z, "p_real_keep_shock": rs["p_real_keep"], "p_spend_keep_shock": rs["p_spend_keep"],
                  "c2": bool(r["p_real_keep"] >= f("real_keep_min") and z >= f("current_spend_bn") / W0 * 100)}); mcs.append(r)
res["case2"]["mc"] = mcs
for x in XS:
    L(f"[조건 ② MC 30년] x={x:>2}%: z={'/'.join(str(z) for z in ZL)} → 실질가치 유지 확률 " + "/".join(f"{m['p_real_keep']:.0%}" for m in mcs if m['illiq_cap_pct']==x) + " (2022형 1년차 시 " + "/".join(f"{m['p_real_keep_shock']:.0%}" for m in mcs if m['illiq_cap_pct']==x) + ") · 30년 고정 지출 유지 " + "/".join(f"{m['p_spend_keep']:.0%}" for m in mcs if m['illiq_cap_pct']==x))
buf = []
for y in YL:
    r = mc(20, 4.5, y_floor=y); r.update({"y_pct": y}); buf.append(r)
    L(f"[조건 ④ y={y}%] x=20 · z=4.5: 충격 후 3년 강제매도 없음 & 고정 지출 유지 확률 {r['p_no_forced_and_spend']:.1%} (강제매도 {r['p_forced_sale']:.1%})")
res["case2"]["buffer"] = buf
y_ok = [b["y_pct"] for b in buf if b["p_no_forced_and_spend"] >= f("spend_keep_min")]
y_star = min(y_ok) if y_ok else None
L(f"[조건 ④] 확률 ≥ {f('spend_keep_min'):.0%} 인 최소 y = {y_star}% (산수 {y_req:.1f}% 는 국채 −15% 충격을 빼고 센 값)")
res["case2"]["y_required_pct"] = y_req; res["case2"]["y_star"] = y_star
# ── 종합 ─────────────────────────────────────────────────────────────────────
summ = []
for x in XS:
    c1 = [l for l in lk if l["illiq_cap_pct"] == x][0]["c1"]; s2 = [s for s in sp if s["illiq_cap_pct"] == x][0]
    a3 = [a for a in acc if a["illiq_cap_pct"] == x][0]
    zf = [m["z_pct"] for m in mcs if m["illiq_cap_pct"] == x and m["c2"]]
    summ.append({"illiq_cap_pct": int(x), "c1": bool(c1), "c2": len(zf) > 0, "z_feasible": zf, "z_feasible_cma": s2["z_feasible"], "direct_ok": a3["direct_ok"], "vehicle": a3["vehicle"],
                 "pass": bool(c1 and len(zf) > 0)})
res["case2"]["summary"] = summ
ok2 = [s for s in summ if s["pass"]]
L("[종합] " + " · ".join(f"x={s['illiq_cap_pct']}: ①{'통과' if s['c1'] else '탈락'} ②{'통과' if s['c2'] else '탈락'}(z {s['z_feasible']}) ③{s['vehicle']}" for s in summ))
if ok2:
    x2 = max(s["illiq_cap_pct"] for s in ok2); z2 = max([s for s in ok2 if s["illiq_cap_pct"] == x2][0]["z_feasible"])
    res["case2"]["default"] = {"x": x2, "y": y_star, "z": z2}
    L(f"[기본 답] 비유동 대체 상한 {x2}%(펀드오브펀드·세컨더리) · 안전 유동자산 하한 {y_star}% · 지출률 {z2}%(80/20 평활, 고정 지출 3.5% Floor) — 조건부 승인")
json.dump(res, open(f"{D}/w7m9_results.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(f"{D}/compute_log.txt", "w").write("\n".join(log) + "\n")
print("→ w7m9_results.json · compute_log.txt")
