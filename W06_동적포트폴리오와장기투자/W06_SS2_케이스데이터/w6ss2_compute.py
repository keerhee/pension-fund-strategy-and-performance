#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 SS2 IC 케이스 — 판정 조건 계산 (w6ss2_build.py 의 CSV → w6ss2_results.json · compute_log.txt)

제1호 (기금운용위) 국민연금 기금의 리밸런싱 규칙 — 안 A 캘린더 분기 전량 복원(현물) · 안 B 지침 밴드(국내주식 ±3) 월 점검 +
       총 위험자산 밴드 ±2 선물 오버레이 · 안 C 한시 밴드(±6) 상시화 · 분기 점검 · 현물 월 25bp 한도
  조건 ① 평균회귀      자산군별 월간 수익률 AR(1) φ 의 t — t ≤ −2 평균회귀(좁은 밴드 근거) · |t| < 2 랜덤워크(DR만) · t ≥ 2 추세(넓은 밴드)
  조건 ② 순 프리미엄   규칙별 분산수익 DR = g_port − Σ w·g_i 에서 거래비용(스프레드 + 시장충격)을 뺀 값 > 0, 최적 규칙과 5bp 이내
  조건 ③ 시장충격      복원 거래를 20 거래일 안에 끝낼 수 있는가 — 현물은 일평균 거래대금의 5%, 선물은 선물 거래대금의 20% 참여
  조건 ④ 위험 이탈     드리프트 뒤 위험자산 비중의 CVaR95 ≥ −15%(지침 제6조의2) — 총 위험자산 비중 상한 w_max
  조건 ⑤ 거버넌스      지침 별표 1 과 정합(밴드 · 복원 방식 · 오버레이 한도 · 기금위 보고) — 의결문 조건(계산 대상 아님)
제2호 (4기관) 같은 규칙을 쓸 것인가 — 기관별 지표: 실행일수(1%p · 3%p) · 현금흐름 용량 · 비유동 비중 · 위험한도 · 자산군 φ → 규칙표 도출
"""
import json, math, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(f"{D}/fml_w6ss2_params.csv").set_index("key").value
f = lambda k: float(P[k])
A = pd.read_csv(f"{D}/fml_w6ss2_assets.csv").set_index("code")
PN = pd.read_csv(f"{D}/fml_w6ss2_panel_daily_sim.csv")
SNAP = pd.read_csv(f"{D}/fml_w6ss2_nps_snapshot.csv").set_index("nps_class")
INST = pd.read_csv(f"{D}/fml_w6ss2_institutions.csv").set_index("code")
codes = A.index.tolist(); RET = PN[[f"{c}_ret" for c in codes]].values; T, NA = RET.shape
W = A.w_nps.values; RISK = A.is_risk.values.astype(bool)
AUM = f("fund_2026h1_trn"); ETA = f("impact_eta"); PART_CASH = f("part_cash"); PART_FUT = f("part_fut")
ADV_FUT = f("adv_k200_fut_total"); MAX_DAYS = f("max_days"); CVAR_LIM = f("cvar_limit_pct")
MU_R, MU_S, SG_R, SG_S, RHO = f("mu_risk"), f("mu_safe"), f("sig_risk"), f("sig_safe"), f("rho")
CLASS = A.nps_class.values
BAND_PATTERN = {"eq_kr": 3.0, "eq_fx": 4.0, "bond_kr": 7.0, "bond_fx": 0.5, "alt": 3.0}    # 지침 별표 1 의 모양(대체는 교육용 3)
ES_Z = 2.0627   # 정규분포 5% 기대손실 계수 φ(z)/0.05
log = []
def L(s): log.append(s); print(s)


# ── 두 자산 CMA — 위험자산 비중 w 의 μ·σ·CVaR95 ─────────────────────────────
def mu_sig(w):
    mu = w * MU_R + (1 - w) * MU_S
    var = (w * SG_R) ** 2 + ((1 - w) * SG_S) ** 2 + 2 * w * (1 - w) * SG_R * SG_S * RHO
    return mu, math.sqrt(var)
def cvar(w):
    mu, sg = mu_sig(w); return mu - ES_Z * sg
w_max = 0.5
for w in np.arange(0.50, 0.95, 0.0005):
    if cvar(w) >= CVAR_LIM: w_max = w
RISK_TARGET = float(W[RISK].sum())          # 교육용 정의: 목표 비중에서의 위험자산 합(69.5%) ↔ 기준포트폴리오 65% 에 대응
def risk_share_ref(w_risk_actual):          # 실제 위험자산 합 → 기준포트폴리오 척도(65 + 드리프트)
    return f("ref_risk_share") + (w_risk_actual - RISK_TARGET)


# ── 조건 ① AR(1) ──────────────────────────────────────────────────────────
def ar1(x):
    y, x1 = x[1:], x[:-1]; X = np.c_[np.ones(len(x1)), x1]
    b, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ b; s2 = e @ e / (len(y) - 2)
    V = s2 * np.linalg.inv(X.T @ X); return float(b[1]), float(b[1] / math.sqrt(V[1, 1]))
def vr(x, q=12):
    """분산비 VR(q) = Var(q개월 합)/(q·Var(1개월)) — 1 미만이면 평균회귀"""
    xs = pd.Series(x); s = xs.rolling(q).sum().dropna(); return float(s.var() / (q * xs.var()))
mon = pd.DataFrame(RET, columns=codes).groupby(PN.month_id).sum()   # 일간 합 = 월간 단순수익(근사)
cond1 = []
for c in codes:
    phi, t = ar1(mon[c].values); v = vr(mon[c].values)
    kind = "평균회귀" if t <= -f("t_min") else ("추세" if t >= f("t_min") else "랜덤워크")
    cond1.append({"code": c, "name": A.name[c], "phi": round(phi, 3), "t": round(t, 2), "vr12": round(v, 2), "kind": kind,
                  "band_hint": {"평균회귀": "좁게(지침 값 이하)", "랜덤워크": "지침 값 유지", "추세": "넓게(지침 값 이상)"}[kind],
                  "saa_band_pp": BAND_PATTERN[A.nps_class[c]]})
L("=== 제1호 — 국민연금 기금의 리밸런싱 규칙 ===")
L("[조건 ①] 월간 AR(1) φ · t (240개월) · VR(12): " + " · ".join(f"{r['name'].split('(')[0]} φ {r['phi']:+.2f} t {r['t']:+.2f} VR {r['vr12']:.2f} → {r['kind']}" for r in cond1))


# ── 규칙 엔진 ───────────────────────────────────────────────────────────────
def impact_bp(code, q_trn, part, adv=None, dvol=None):
    """주문 q(조원)을 참여율 part 로 나눠 집행할 때 일 참여율 p 의 시장충격(bp) = η·일변동성·sqrt(p); 집행일수도 반환"""
    adv = A.adv_trn_krw[code] if adv is None else adv; dvol = A.dvol_bp[code] if dvol is None else dvol
    if adv <= 0: return float("inf"), float("inf")
    days = max(1, math.ceil(q_trn / (part * adv))); p = q_trn / (days * adv)
    return ETA * dvol * math.sqrt(p), days


def run(mode, k=None, band_scale=None, restore="edge", check=1, cap_bp=None, total_band=None, aum=AUM, scale="nps", W=W, fut_adv=None):
    """mode: 'bh' | 'cal' (k일마다 전량 복원) | 'band' (자산군 밴드, check일마다 점검).
    restore: 'edge' 밴드 경계까지(지침) | 'target' 목표까지. cap_bp: 월 매매 한도(bp of AUM, 현물). total_band: 총 위험자산 ±%p 오버레이(선물)."""
    RT = float(W[RISK].sum()); FADV = ADV_FUT if fut_adv is None else fut_adv
    h = W.copy(); V = np.zeros(T); turn = 0.0; cost_trn = 0.0; cost_fut_trn = 0.0; max_trade = np.zeros(NA); n_reb = 0
    risk_path = np.zeros(T); month_used = 0.0; cur_month = -1; backlog = np.zeros(NA)
    def trade_cash(delta):   # delta: 자산별 비중 변화(합 0) → 비용·회전 기록, 보유 갱신
        nonlocal h, turn, cost_trn, max_trade, month_used
        tot = h.sum(); q = np.abs(delta) * tot
        turn += q.sum() / 2 / tot
        for i, c in enumerate(codes):
            if q[i] <= 0: continue
            q_trn = q[i] / tot * aum; max_trade[i] = max(max_trade[i], q_trn)
            imp = impact_bp(c, q_trn, PART_CASH)[0] if scale == "nps" else 0.0
            cost_trn += q_trn * (A.spread_bp[c] + imp) / 1e4
        h = h + delta * tot; month_used += (q.sum() / 2 / tot) * 1e4
    def trade_fut(dw):       # 총 위험자산을 dw(양수면 축소)만큼 선물로 조정 — 위험자산끼리 비례, 상대는 안전자산
        nonlocal h, cost_fut_trn
        tot = h.sum(); q_trn = abs(dw) * aum
        imp, _ = impact_bp("eq_kr", q_trn, PART_FUT, adv=FADV, dvol=150)
        cost_fut_trn += q_trn * (2 + imp) / 1e4
        delta = np.zeros(NA); wr = h[RISK] / h[RISK].sum(); ws = h[~RISK] / h[~RISK].sum()
        delta[RISK] = -dw * wr; delta[~RISK] = dw * ws; h = h + delta * tot
    for t in range(T):
        h = h * (1 + RET[t]); tot = h.sum(); V[t] = tot; w = h / tot
        risk_path[t] = w[RISK].sum()
        m = PN.month_id.iat[t]
        if m != cur_month: cur_month = m; month_used = 0.0
        if mode == "bh": continue
        if total_band is not None:   # 오버레이 — 매일 점검, 총 위험자산이 목표 ± total_band 를 넘으면 경계까지
            dev = (w[RISK].sum() - RT) * 100
            if abs(dev) > total_band:
                trade_fut(np.sign(dev) * (abs(dev) - total_band) / 100); tot = h.sum(); w = h / tot
        if mode == "cal" and (t + 1) % k == 0:
            trade_cash(W - w); n_reb += 1; continue
        if mode == "band" and (t + 1) % check == 0:
            want = np.zeros(NA)
            for cls in set(CLASS):
                idx = CLASS == cls; b = BAND_PATTERN[cls] * band_scale / 3.0
                if W[idx].sum() <= 0: continue
                dev = (w[idx].sum() - W[idx].sum()) * 100
                if abs(dev) > b:
                    move = (abs(dev) - b) if restore == "edge" else abs(dev)
                    want[idx] -= np.sign(dev) * move / 100 * (W[idx] / W[idx].sum())
            if np.any(want != 0):
                # 상대 매매: 목표 대비 부족한 자산군에 비례해 배분
                short = np.clip(W - w, 0, None); short[want != 0] = 0
                if short.sum() <= 0: short = W.copy(); short[want != 0] = 0
                if short.sum() <= 0: want *= 0
                else: need = -want.sum(); want += need * short / short.sum()
                if cap_bp is not None:   # 월 매매 한도 — 초과분은 다음 달로 이월(백로그)
                    room = max(0.0, cap_bp - month_used) / 1e4
                    size = np.abs(want).sum() / 2
                    if size > room: want = want * (room / size) if room > 0 else want * 0
                if np.any(want != 0): trade_cash(want); n_reb += 1
    lr = np.log(V[1:] / V[:-1]); years = T / 252
    g_port = (math.log(V[-1] / 1.0)) / years * 100
    g_assets = np.array([math.log(np.prod(1 + RET[:, i])) / years * 100 for i in range(NA)])
    DR = g_port - float(W @ g_assets)
    sig = float(np.std(lr) * math.sqrt(252) * 100)
    ref = f("ref_risk_share") + (risk_path - RT)
    return {"g_port": round(g_port, 3), "DR_bp": round(DR * 100, 1), "sigma": round(sig, 2), "sharpe": round((g_port - 2.5) / sig, 3),
            "turnover_pct": round(turn / years * 100, 1), "cost_bp": round(cost_trn / aum / years * 1e4, 1), "cost_fut_bp": round(cost_fut_trn / aum / years * 1e4, 1),
            "net_bp": round(DR * 100 - (cost_trn + cost_fut_trn) / aum / years * 1e4, 1), "n_rebal_per_yr": round(n_reb / years, 1),
            "max_trade_trn": round(float(max_trade.max()), 1), "max_trade_asset": codes[int(max_trade.argmax())],
            "risk_dev_max_pp": round(float((risk_path - RT).max() * 100), 1), "risk_dev_min_pp": round(float((risk_path - RT).min() * 100), 1),
            "pct_days_over_cvar": round(float((ref > w_max).mean() * 100), 1), "final_risk_share": round(float(risk_path[-1]) * 100, 1)}


L(f"[조건 ④] 두 자산 CMA(위험 {MU_R}/{SG_R} · 안전 {MU_S}/{SG_S} · ρ {RHO}) — CVaR95(65%) = {cvar(0.65):.1f}% · 위험자산 상한 w_max = {w_max*100:.1f}% (CVaR ≥ {CVAR_LIM}%) · 총 밴드 ±{w_max*100-65:.1f}%p 까지 허용")
rules = {}
rules["bh"] = run("bh")
for name, k in [("cal_d", 1), ("cal_w", 5), ("cal_m", 21), ("cal_q", 63), ("cal_s", 126), ("cal_a", 252)]:
    rules[name] = run("cal", k=k)
    rules[name + "_small"] = run("cal", k=k, scale="small", aum=0.5)
for b in [2, 3, 5, 6]:
    rules[f"band{b}"] = run("band", band_scale=b)
    rules[f"band{b}_small"] = run("band", band_scale=b, scale="small", aum=0.5)
rules["band3_target"] = run("band", band_scale=3, restore="target")
rules["A"] = rules["cal_q"]
rules["B"] = run("band", band_scale=3, check=21, cap_bp=25, total_band=f("risk_band_total"))
rules["B_nocap"] = run("band", band_scale=3, check=21, total_band=f("risk_band_total"))
rules["C"] = run("band", band_scale=6, check=63, cap_bp=25)
rules["C_nocap"] = run("band", band_scale=6, check=63)
L("[조건 ②] 규칙별 DR · 비용 · 순 프리미엄 (bp/년, NPS 규모 = 스프레드 + 시장충격 · 소형 = 스프레드만)")
for k in ["bh", "cal_d", "cal_w", "cal_m", "cal_q", "cal_s", "cal_a", "band2", "band3", "band5", "band6", "band3_target", "A", "B", "B_nocap", "C", "C_nocap"]:
    r = rules[k]; s = rules.get(k + "_small")
    L(f"   {k:13s} g {r['g_port']:.2f}% σ {r['sigma']:.1f} DR {r['DR_bp']:+6.1f} 회전 {r['turnover_pct']:5.1f}%/년 비용 {r['cost_bp']:5.1f}(+선물 {r['cost_fut_bp']:.1f}) 순 {r['net_bp']:+6.1f}"
      + (f" | 소형 비용 {s['cost_bp']:.1f} 순 {s['net_bp']:+.1f}" if s else "") + f" | 위험 드리프트 {r['risk_dev_min_pp']:+.1f}~{r['risk_dev_max_pp']:+.1f}%p · CVaR 초과일 {r['pct_days_over_cvar']}% · 최대 단일거래 {r['max_trade_trn']}조({r['max_trade_asset']})")
best_nps = max((rules[k]["net_bp"], k) for k in ["cal_d", "cal_w", "cal_m", "cal_q", "cal_s", "cal_a", "band2", "band3", "band5", "band6"])
best_small = max((rules[k + "_small"]["net_bp"], k) for k in ["cal_d", "cal_w", "cal_m", "cal_q", "cal_s", "cal_a", "band2", "band3", "band5", "band6"])
L(f"[조건 ②] 최적 — NPS 규모 {best_nps[1]} {best_nps[0]:+.1f}bp · 소형 {best_small[1]} {best_small[0]:+.1f}bp")

# ── 조건 ③ 시장충격 — 2026.6 공시 갭 시나리오 ──────────────────────────────────
kr = SNAP.loc["eq_kr"]; gap_target = kr.actual_2026_06_pct - kr.target_2026_pct
scen = [("목표(20.8%)까지 복원", gap_target), (f"지침 밴드 ±{kr.saa_band_pp:.0f} 경계(23.8%)까지", gap_target - kr.saa_band_pp),
        (f"한시 밴드 ±{kr.saa_band_temp_pp:.0f} 경계(26.8%)까지", gap_target - kr.saa_band_temp_pp), ("2026 2분기형 월 드리프트 3%p", 3.0),
        (f"총 위험자산 밴드 ±{f('risk_band_total'):.0f} 복원(2%p)", f("risk_band_total"))]
adv_now, adv_2025 = f("adv_kospi_2026_05"), f("adv_kospi_2025")
cap_per_day = f("rebal_cap_new_bp") / 1e4 * AUM / f("rebal_cap_new_days")
cond3 = []
for name, pp in scen:
    q = pp / 100 * AUM
    d_cap = q / cap_per_day; d_cash = q / (PART_CASH * adv_now); d_cash25 = q / (PART_CASH * adv_2025); d_fut = q / (PART_FUT * ADV_FUT)
    imp_cash = impact_bp("eq_kr", q, PART_CASH, adv=adv_now)[0]
    cond3.append({"scenario": name, "pp": round(pp, 1), "amount_trn": round(q, 1), "days_cap25bp": round(d_cap), "days_cash5pct_2026": round(d_cash, 1),
                  "days_cash5pct_2025adv": round(d_cash25, 1), "days_fut20pct": round(d_fut, 1), "impact_cash_bp": round(imp_cash, 1),
                  "ok_cap": d_cap <= MAX_DAYS, "ok_cash": d_cash <= MAX_DAYS, "ok_fut": d_fut <= MAX_DAYS})
L(f"[조건 ③] 2026.6 말 국내주식 {kr.actual_2026_06_pct}% vs 목표 {kr.target_2026_pct}% (갭 {gap_target:.1f}%p = {gap_target/100*AUM:.0f}조) · 코스피 일평균 {adv_now}조(2026.5) / {adv_2025}조(2025) · 월 25bp 한도 = 일 {cap_per_day:.2f}조 · 선물 {ADV_FUT}조×{PART_FUT:.0%}")
for r in cond3:
    L(f"   {r['scenario']:28s} {r['amount_trn']:6.1f}조 → 25bp 한도 {r['days_cap25bp']:4d}일 · 현물 5% {r['days_cash5pct_2026']:5.1f}일(2025 거래대금이면 {r['days_cash5pct_2025adv']:.0f}일) · 선물 20% {r['days_fut20pct']:4.1f}일 · 현물 충격 {r['impact_cash_bp']:.0f}bp")

# ── 조건 ④ — 2026.6 실제 드리프트를 기준포트폴리오 척도로 ─────────────────────
fx = SNAP.loc["eq_fx"]; alt = SNAP.loc["alt"]
drift_2026 = (kr.actual_2026_06_pct - kr.target_2026_pct) + (fx.actual_2026_06_pct - fx.target_2026_pct) + (alt.actual_2026_06_pct - alt.target_2026_pct)
w_2026 = f("ref_risk_share") + drift_2026 / 100
cond4 = {"w_max_pct": round(w_max * 100, 1), "band_max_pp": round(w_max * 100 - 65, 1), "cvar_65": round(cvar(0.65), 1), "cvar_67": round(cvar(0.67), 1), "cvar_68": round(cvar(0.68), 1),
         "drift_2026_06_pp": round(drift_2026, 1), "w_2026_06_pct": round(w_2026 * 100, 1), "cvar_2026_06": round(cvar(w_2026), 1),
         "table": [{"w": w, "mu": round(mu_sig(w / 100)[0], 2), "sigma": round(mu_sig(w / 100)[1], 2), "cvar": round(cvar(w / 100), 1), "ok": cvar(w / 100) >= CVAR_LIM} for w in [60, 63, 65, 67, 68, 70, 74, 78]]}
L(f"[조건 ④] 2026.6 드리프트 {drift_2026:+.1f}%p → 위험자산 {w_2026*100:.1f}% → CVaR95 {cvar(w_2026):.1f}% (한도 {CVAR_LIM}%) · 65% {cvar(0.65):.1f} · 67% {cvar(0.67):.1f} · 68% {cvar(0.68):.1f}")
# 패널에서의 드리프트 통계(B&H)
rp = pd.Series(np.zeros(T)); h = W.copy(); rs = []
for t in range(T):
    h = h * (1 + RET[t]); rs.append(h[RISK].sum() / h.sum())
rs = pd.Series(rs); d3 = (rs.shift(-63) - rs).dropna() * 100; d12 = (rs.shift(-252) - rs).dropna() * 100
cond4["drift_3m"] = {"std": round(float(d3.std()), 2), "p95": round(float(d3.quantile(0.95)), 2), "max": round(float(d3.max()), 2)}
cond4["drift_12m"] = {"std": round(float(d12.std()), 2), "p95": round(float(d12.quantile(0.95)), 2), "max": round(float(d12.max()), 2)}
L(f"[조건 ④] 패널 B&H 드리프트 — 3개월 σ {d3.std():.2f}%p · 95% {d3.quantile(0.95):.2f} · 최대 {d3.max():.2f} / 12개월 σ {d12.std():.2f} · 95% {d12.quantile(0.95):.2f} · 최대 {d12.max():.2f}")

# ── 안 B 민감도 — 밴드 폭(월 점검 · 한도 25bp · 오버레이 ±2) ────────────────────
sens = []
for b in [0, 2, 3, 5, 6]:
    r = run("band", band_scale=b, check=21, cap_bp=25, total_band=f("risk_band_total")) if b > 0 else run("cal", k=21, cap_bp=None, total_band=f("risk_band_total"))
    sens.append({"band": b, "DR_bp": r["DR_bp"], "cost_bp": round(r["cost_bp"] + r["cost_fut_bp"], 1), "net_bp": r["net_bp"], "turnover_pct": r["turnover_pct"], "risk_dev_max_pp": r["risk_dev_max_pp"], "max_trade_trn": r["max_trade_trn"]})
L("[민감도 B] 밴드 폭(월 점검 · 오버레이 ±2): " + " · ".join(f"±{s['band']} 순 {s['net_bp']:+.1f}(DR {s['DR_bp']:.0f} 비용 {s['cost_bp']:.1f} 최대거래 {s['max_trade_trn']}조)" for s in sens))

# ── 안 A·B·C 판정 ────────────────────────────────────────────────────────────
opts = {}
for k, name in [("A", "캘린더 — 분기 말 목표까지 전량 복원(현물)"), ("B", "지침 밴드(국내주식 ±3) 월 점검 · 경계 복원 + 총 위험자산 ±2 선물 오버레이 · 현물 월 25bp 한도"),
                ("C", "한시 밴드 ±6 상시화 · 분기 점검 · 현물 월 25bp 한도")]:
    r = rules[k]
    if k == "A": c3 = cond3[0]["ok_cash"] and cond3[3]["ok_cash"]; c3_note = f"2026.6 형 목표 복원 {cond3[0]['amount_trn']}조 → 현물 5% 참여 {cond3[0]['days_cash5pct_2026']:.0f}일 · 월 3%p 드리프트도 {cond3[3]['days_cash5pct_2026']:.0f}일"
    elif k == "B": c3 = cond3[4]["ok_fut"] and cond3[3]["ok_fut"]; c3_note = f"총 밴드 복원 {cond3[4]['amount_trn']}조 선물 {cond3[4]['days_fut20pct']:.0f}일 · 월 3%p 드리프트도 {cond3[3]['days_fut20pct']:.0f}일"
    else: c3 = cond3[2]["ok_cap"]; c3_note = f"±6 경계 복원 {cond3[2]['amount_trn']}조 → 25bp 한도로 {cond3[2]['days_cap25bp']}일"
    c2 = r["net_bp"] > f("net_min_bp")
    c4 = r["pct_days_over_cvar"] <= 0.5 and r["risk_dev_max_pp"] <= (w_max * 100 - 65) + 0.5
    if k == "C": c4 = c4 and cvar(w_2026) >= CVAR_LIM   # 2026 형 드리프트를 허용하는 밴드는 한도를 넘긴다
    if k == "A": c4 = c4 and cond4["drift_3m"]["max"] <= (w_max * 100 - 65)
    opts[k] = {"name": name, "net_bp": r["net_bp"], "cost_bp": round(r["cost_bp"] + r["cost_fut_bp"], 1), "DR_bp": r["DR_bp"], "turnover_pct": r["turnover_pct"], "risk_dev_max_pp": r["risk_dev_max_pp"], "pct_days_over_cvar": r["pct_days_over_cvar"],
               "max_trade_trn": r["max_trade_trn"], "cond1_ok": True, "cond2_ok": bool(c2), "cond3_ok": bool(c3), "cond3_note": c3_note, "cond4_ok": bool(c4)}
    L(f"[안 {k}] {name} → DR {r['DR_bp']:+.1f} 비용 {r['cost_bp']+r['cost_fut_bp']:.1f} 순 {r['net_bp']:+.1f}bp · 위험 드리프트 최대 {r['risk_dev_max_pp']:+.1f}%p · CVaR 초과일 {r['pct_days_over_cvar']}% · ③ {c3_note}")
    L(f"       조건 ② {'통과' if c2 else '탈락'} · ③ {'통과' if c3 else '탈락'} · ④ {'통과' if c4 else '탈락'}")
feasible = [k for k in opts if opts[k]["cond2_ok"] and opts[k]["cond3_ok"] and opts[k]["cond4_ok"]]
answer = max(feasible, key=lambda k: opts[k]["net_bp"]) if feasible else None
opts["answer"] = answer
opts["B"]["cond5"] = "지침 별표 1 에 총 위험자산 밴드 ±2 와 오버레이 한도(순 익스포저 ±3%p · 기금위 사후 보고)를 명시 — 조건부 승인의 조건"
L(f"[기본 답] ③④ 를 통과한 안 = {feasible} → 순 프리미엄 최대 = 안 {answer} ({opts[answer]['net_bp']:+.1f}bp) · 안 A 와의 격차 {opts['A']['net_bp']-opts[answer]['net_bp']:.1f}bp 는 실행 가능성의 값")

# ── 제2호 — 4기관: 자기 규모 · 자기 배분으로 후보 규칙을 돌린다 ───────────────────
L("\n=== 제2호 — 4기관 차등 ===")
drift_sd = cond4["drift_12m"]["std"]
INST_W = {"NPS": W,
          "KIC": np.array([0.0, 0.40, 0.05, 0.0, 0.33, 0.11, 0.11]),      # 주식 45(선진 40 · 신흥 5) · 글로벌채권 33 · 대체 22(REIT · 원자재 프록시)
          "UNIV": np.array([0.0, 0.55, 0.05, 0.0, 0.30, 0.05, 0.05])}    # 주식 60 · 채권 30 · 대체 10
inst_rows = []
for code, r in INST.iterrows():
    aum = r.aum_trn_krw; adv = r.adv_trn_krw
    d1 = (0.01 * aum) / (PART_CASH * adv) if adv > 0 else float("inf"); d3 = 3 * d1
    flow_ok = abs(r.net_flow_pct) >= 0.5 * drift_sd
    illiq = r.illiquid_share >= 0.8
    row = {"code": code, "name": r["name"], "aum_trn_krw": round(aum, 1), "adv_trn_krw": adv, "days_1pp": (round(d1, 2) if math.isfinite(d1) else None), "days_3pp": (round(d3, 1) if math.isfinite(d3) else None),
           "net_flow_pct": r.net_flow_pct, "flow_ok": bool(flow_ok), "illiquid_share": r.illiquid_share, "risk_limit": r.risk_limit, "deriv_access": int(r.deriv_access)}
    if illiq:
        row.update({"rule_nps_net": None, "rule_best": "부적용", "rule_best_net": None, "band": "부적용 — 집중 한도 · 유동성 계정 하한", "check": "연 1회 평가", "exec": "해당 없음(비상장 지분)", "optA_ok": False,
                    "optA_note": "비상장 정책지분 · 첨단산업 장기 지분 — 팔아서 비중을 맞추는 자산이 아니다", "cands": []})
    else:
        Wi = INST_W[code]; cands = {}
        cands["nps_rule"] = run("band", band_scale=3, check=21, cap_bp=25, total_band=f("risk_band_total"), aum=aum, W=Wi) if r.deriv_access else run("band", band_scale=3, check=21, cap_bp=25, aum=aum, W=Wi)
        cands["cal_m"] = run("cal", k=21, aum=aum, W=Wi); cands["cal_q"] = run("cal", k=63, aum=aum, W=Wi)
        cands["band3_m"] = run("band", band_scale=3, check=21, aum=aum, W=Wi); cands["band5_q"] = run("band", band_scale=5, check=63, aum=aum, W=Wi)
        # 실행 가능성: 최대 단일거래를 20일 안에(현물 5%) 끝내는가 · 위험 드리프트가 총 밴드 안인가
        feas = {}
        for kk, rr in cands.items():
            adv_i = adv if code != "NPS" else A.adv_trn_krw["eq_kr"]
            days = rr["max_trade_trn"] / (PART_CASH * adv_i) if adv_i > 0 else float("inf")
            feas[kk] = (days <= MAX_DAYS or kk == "nps_rule") and rr["pct_days_over_cvar"] <= 0.5
            rr["feasible"] = bool(feas[kk]); rr["max_trade_days"] = round(days, 1)
        if code == "NPS": feas = {k: (k == "nps_rule") for k in cands}   # 제1호 결과 — 2026 형 충격은 패널 밖이라 조건 ③ 을 공시 갭으로 판정했다
        for kk in cands: cands[kk]["feasible"] = bool(feas[kk])
        best = max((cands[k]["net_bp"], k) for k in cands if feas[k]) if any(feas.values()) else (None, None)
        nps_net = cands["nps_rule"]["net_bp"]
        if code == "NPS": band, check, exec_ = "자산군 ±3(지침) + 총 위험 ±2 오버레이", "월", "선물 오버레이 + 현물 분할(월 25bp)"
        elif flow_ok: band, check, exec_ = "밴드 없음 — 월 점검 · 현금흐름으로 먼저 복원", "월", "지출·기부 현금흐름 → 잔여 현물(시장충격 0)"
        else: band, check, exec_ = "밴드 없음 — 월말 목표 복원", "월", "현물 즉시(시장충격 0)"
        a_ok = code == "NPS"
        a_note = ("NPS 규칙 그대로" if code == "NPS" else
                  (f"오버레이 접근 없음 · 월 25bp 한도 = {0.0025*aum*1e4:.0f}억 — 한도가 드리프트를 못 따라가 CVaR 초과일 {cands['nps_rule']['pct_days_over_cvar']}%" if not r.deriv_access else
                   f"시장충격이 없는데 밴드·한도로 DR 을 버린다 — 순 {nps_net:+.1f} vs 최적 {best[1]} {best[0]:+.1f}bp (격차 {best[0]-nps_net:.1f}bp ≈ 연 {(best[0]-nps_net)/1e4*aum*1e4:,.0f}억)"))
        row.update({"rule_nps_net": nps_net, "rule_best": best[1], "rule_best_net": best[0], "band": band, "check": check, "exec": exec_, "optA_ok": a_ok, "optA_note": a_note,
                    "cands": [{"rule": k, **{kk: v for kk, v in cands[k].items() if kk in ("DR_bp", "cost_bp", "cost_fut_bp", "net_bp", "turnover_pct", "risk_dev_max_pp", "pct_days_over_cvar", "max_trade_trn", "max_trade_days", "feasible")}} for k in cands]})
    inst_rows.append(row)
    L(f"[{code}] {r['name']} AUM {aum:,.1f}조 · 1%p 실행 {row['days_1pp'] if row['days_1pp'] is not None else '∞'}일 · 3%p {row['days_3pp'] if row['days_3pp'] is not None else '∞'}일 · 현금흐름 {r.net_flow_pct:+.2f}%/년(12개월 드리프트 σ {drift_sd}%p → {'충분' if flow_ok else '부족'}) · 비유동 {r.illiquid_share:.0%}")
    if row["cands"]:
        L("      " + " · ".join(f"{c['rule']} 순 {c['net_bp']:+.1f}({'가능' if c['feasible'] else '불가'} · 최대거래 {c['max_trade_trn']}조 {c['max_trade_days']}일 · CVaR초과 {c['pct_days_over_cvar']}%)" for c in row["cands"]))
    L(f"      → 규칙: 밴드 {row['band']} · 점검 {row['check']} · 실행 {row['exec']} | 안 A(NPS 규칙 동일 적용) {'성립' if row['optA_ok'] else '불성립'}: {row['optA_note']}")
res2 = {"institutions": inst_rows, "drift_12m_sd": drift_sd, "optA_ok": all(x["optA_ok"] for x in inst_rows),
        "optC_note": f"규칙 없음 → 패널 B&H 12개월 드리프트 95% {cond4['drift_12m']['p95']}%p · 최대 {cond4['drift_12m']['max']}%p → 위험자산 상한 {cond4['w_max_pct']}% 초과(2026 형 +9.0%p 재현) · B&H 순 {rules['bh']['net_bp']:+.1f}bp"}
L(f"[안 A 단일 규칙] {'성립' if res2['optA_ok'] else '불성립'} — " + " · ".join(f"{x['code']} {'○' if x['optA_ok'] else '×'}" for x in inst_rows))
L(f"[안 C 자율] {res2['optC_note']}")

res = {"asof": P["asof"], "agenda1": {"cond1": cond1, "rules": rules, "best_nps": {"rule": best_nps[1], "net_bp": best_nps[0]}, "best_small": {"rule": best_small[1], "net_bp": best_small[0]},
                                     "cond3": cond3, "cond3_meta": {"gap_pp": round(gap_target, 1), "adv_2026": adv_now, "adv_2025": adv_2025, "cap_per_day_trn": round(cap_per_day, 2), "adv_fut": ADV_FUT},
                                     "cond4": cond4, "options": opts, "sens_band": sens, "risk_target_liquid": round(RISK_TARGET * 100, 1)},
       "agenda2": res2}
json.dump(res, open(f"{D}/w6ss2_results.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(f"{D}/compute_log.txt", "w").write("\n".join(log) + "\n")
print("→ w6ss2_results.json · compute_log.txt")
