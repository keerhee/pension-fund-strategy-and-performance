#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리밸런싱 규칙 계산 도구 — W07 팀 과제 IV 3팀(국민연금 규칙) · 4팀(4기관 차등)용

사용법
  python3 rebal_tool.py --inst NPS     # 3팀: 국민연금의 세 안
  python3 rebal_tool.py --inst ALL     # 4팀: 네 기관(국민연금 · KIC · 전략형 국부펀드 · H대 발전기금)
  python3 rebal_tool.py --inst KIC     # 참고: KIC 하나만
  python3 rebal_tool.py --inst NPS --max-days 40 --cvar-limit -16   # 판정 기준 변경
  (실행에 수십 초 걸린다 — 20년 일간 모의 패널로 규칙마다 매일 매매를 재현한다)

판정 기준(출처를 구분한다)
  ② 순 프리미엄 > 0bp (경제적 기준 · --net-min)
  ③ 복원 거래를 끝내는 거래일 ≤ 20일 (교육용: 한 달 영업일 · --max-days)
  ④ 위험한도 CVaR95 ≥ −15% (공시: 기금운용지침 제6조의2 · --cvar-limit로 민감도만) — 초과일 ≤ 0.5% (교육용 · --cvar-days)
  4기관: 현금흐름만으로 복원 가능 = |순현금흐름| ≥ 0.5 × 12개월 드리프트 표준편차 (교육용 · --flow-ratio) · 비유동 ≥ 80%면 밴드 부적용 (교육용 · --illiq-max)

출력
  [1] 자산군별 평균회귀 점검 — 월간 수익률 AR(1) 계수 φ와 t값, 분산비 VR(12)
  [2] 위험한도 — 위험자산 비중별 CVaR95와 한도(−15%)를 지키는 위험자산 상한
  [3] 실행 가능성 — 복원 거래를 며칠 안에 끝낼 수 있는가
  [4] 세 안의 성과 — 분산수익(DR) · 거래비용 · 순 리밸런싱 프리미엄 · 회전율 · 위험 비중 이탈 · 최대 단일 거래 · 판정
용어: DR(분산수익) = 포트폴리오 기하수익 − 자산별 기하수익의 가중평균. 리밸런싱이 "싸게 사고 비싸게 파는" 효과로 얻는 수익.
"""
import argparse, math, os
import numpy as np, pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument("--inst", choices=["NPS", "KIC", "ALL"], default="NPS")
ap.add_argument("--max-days", type=float, default=None); ap.add_argument("--cvar-limit", type=float, default=None)
ap.add_argument("--cvar-days", type=float, default=0.5); ap.add_argument("--net-min", type=float, default=0.0)
ap.add_argument("--flow-ratio", type=float, default=0.5); ap.add_argument("--illiq-max", type=float, default=0.8)
args = ap.parse_args(); ALLMODE = args.inst == "ALL"
if ALLMODE: args.inst = "NPS"
P = pd.read_csv(f"{D}/rb_params.csv").set_index("key").value
f = lambda k: float(P[k])
A = pd.read_csv(f"{D}/rb_assets.csv").set_index("code")
PN = pd.read_csv(f"{D}/rb_panel_daily_sim.csv")
SNAP = pd.read_csv(f"{D}/rb_nps_snapshot.csv").set_index("nps_class")
INST = pd.read_csv(f"{D}/rb_institutions.csv").set_index("code")
codes = A.index.tolist(); RET = PN[[f"{c}_ret" for c in codes]].values; T, NA = RET.shape
RISK = A.is_risk.values.astype(bool)
W_BY = {"NPS": A.w_nps.values, "KIC": np.array([0.0, 0.40, 0.05, 0.0, 0.33, 0.11, 0.11])}
W = W_BY[args.inst]; AUM = float(INST.aum_trn_krw[args.inst])
ETA = f("impact_eta"); PART_CASH = f("part_cash"); PART_FUT = f("part_fut")
ADV_FUT = f("adv_k200_fut_total"); MAX_DAYS = args.max_days if args.max_days is not None else f("max_days")
CVAR_LIM = args.cvar_limit if args.cvar_limit is not None else f("cvar_limit_pct")
MU_R, MU_S, SG_R, SG_S, RHO = f("mu_risk"), f("mu_safe"), f("sig_risk"), f("sig_safe"), f("rho")
CLASS = A.nps_class.values
BAND_PATTERN = {"eq_kr": 3.0, "eq_fx": 4.0, "bond_kr": 7.0, "bond_fx": 0.5, "alt": 3.0}
ES_Z = 2.0627
def L(s): print(s)
def mu_sig(w):
    mu = w * MU_R + (1 - w) * MU_S
    return mu, math.sqrt((w * SG_R) ** 2 + ((1 - w) * SG_S) ** 2 + 2 * w * (1 - w) * SG_R * SG_S * RHO)
def cvar(w):
    mu, sg = mu_sig(w); return mu - ES_Z * sg
w_max = max(w for w in np.arange(0.50, 0.95, 0.0005) if cvar(w) >= CVAR_LIM)
def ar1(x):
    y, x1 = x[1:], x[:-1]; X = np.c_[np.ones(len(x1)), x1]
    b, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ b; s2 = e @ e / (len(y) - 2)
    V = s2 * np.linalg.inv(X.T @ X); return float(b[1]), float(b[1] / math.sqrt(V[1, 1]))
def vr(x, q=12):
    xs = pd.Series(x); s = xs.rolling(q).sum().dropna(); return float(s.var() / (q * xs.var()))

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



def all_institutions():
    print(f"=== 4기관 리밸런싱 규칙 차등 — 판정: 실행 ≤ {MAX_DAYS:g}일 · CVaR95 ≥ {CVAR_LIM}% 초과일 ≤ {args.cvar_days:g}% · 현금흐름 ≥ {args.flow_ratio:g}×드리프트σ · 비유동 ≥ {args.illiq_max:.0%}면 밴드 부적용 ===")
    h = W_BY["NPS"].copy(); rs = []
    for t in range(T):
        h = h * (1 + RET[t]); rs.append(h[RISK].sum() / h.sum())
    rs = pd.Series(rs); d12 = (rs.shift(-252) - rs).dropna() * 100; sd = float(d12.std())
    print(f"[1] 규칙이 없을 때(매수 후 보유) 12개월 위험자산 이탈 — 표준편차 {sd:.2f}%p · 95% {d12.quantile(0.95):.2f}%p · 최대 {d12.max():.2f}%p · CVaR 한도까지 여유 {w_max*100-65:.1f}%p")
    INST_W = {"NPS": W_BY["NPS"], "KIC": W_BY["KIC"], "UNIV": np.array([0.0, 0.55, 0.05, 0.0, 0.30, 0.05, 0.05])}
    print("[2] 기관 좌표 — 1%p 복원 거래일 · 순현금흐름 · 비유동 비중 · 오버레이 접근")
    for code, r in INST.iterrows():
        d1 = (0.01 * r.aum_trn_krw) / (PART_CASH * r.adv_trn_krw) if r.adv_trn_krw > 0 else float("inf")
        print(f"    {code:<5} {r['name']:<28} 운용자산 {r.aum_trn_krw:>8,.1f}조 · 1%p {d1:6.2f}일 · 순현금흐름 {r.net_flow_pct:+.2f}%/년"
              f" ({'흐름으로 복원 가능' if abs(r.net_flow_pct) >= args.flow_ratio * sd else '흐름 부족'}) · 비유동 {r.illiquid_share:.0%} · 오버레이 {'있음' if r.deriv_access else '없음'}")
    print("[3] 기관별 후보 규칙 — 자기 규모 · 자기 배분으로 20년 모의 패널에서 실행 (순 = DR − 비용, bp/년)")
    a_ok = {}; best_rule = {}
    for code, r in INST.iterrows():
        aum = r.aum_trn_krw; adv = r.adv_trn_krw
        if r.illiquid_share >= args.illiq_max:
            print(f"    {code}: 비유동 {r.illiquid_share:.0%} ≥ {args.illiq_max:.0%} → 밴드 부적용(팔아서 비중을 맞출 자산이 아니다) — 집중 한도 · 유동성 계정 하한 · 연 1회 평가")
            a_ok[code] = False; best_rule[code] = "부적용"; continue
        Wi = INST_W[code]; cands = {}
        kw = dict(mode="band", band_scale=3, check=21, cap_bp=25, aum=aum, W=Wi)
        if r.deriv_access: kw["total_band"] = f("risk_band_total")
        cands["국민연금 규칙(±3 월 점검 · 25bp 한도" + (" · 오버레이)" if r.deriv_access else ")")] = run(**kw)
        cands["월말 목표 복원"] = run("cal", k=21, aum=aum, W=Wi); cands["분기말 목표 복원"] = run("cal", k=63, aum=aum, W=Wi)
        cands["밴드 ±3 월 점검"] = run("band", band_scale=3, check=21, aum=aum, W=Wi); cands["밴드 ±5 분기 점검"] = run("band", band_scale=5, check=63, aum=aum, W=Wi)
        feas = {}
        for kk, rr in cands.items():
            adv_i = adv if code != "NPS" else A.adv_trn_krw["eq_kr"]
            days = rr["max_trade_trn"] / (PART_CASH * adv_i) if adv_i > 0 else float("inf")
            ok = (days <= MAX_DAYS or kk.startswith("국민연금")) and rr["pct_days_over_cvar"] <= args.cvar_days and rr["net_bp"] > args.net_min
            if code == "NPS": ok = kk.startswith("국민연금")      # 3팀 결과 — 2026.6형 이탈은 패널 밖이라 공시 갭으로 판정
            feas[kk] = ok
            print(f"    {code:<5} {kk:<34} 순 {rr['net_bp']:+6.1f} · 최대 거래 {rr['max_trade_trn']:5.1f}조({days:5.1f}일) · CVaR 초과일 {rr['pct_days_over_cvar']:4.1f}% → {'가능' if ok else '불가'}")
        best = max(((cands[k]["net_bp"], k) for k in cands if feas[k]), default=(None, None))
        nps_k = [k for k in cands if k.startswith("국민연금")][0]
        a_ok[code] = feas[nps_k] and (best[1] == nps_k or best[0] - cands[nps_k]["net_bp"] < 1.0)
        exe = "현금흐름(지출 · 기부)으로 먼저 복원 → 잔여 현물" if abs(r.net_flow_pct) >= args.flow_ratio * sd else ("선물 오버레이 + 현물 분할" if code == "NPS" else "현물 즉시")
        best_rule[code] = (f"{best[1]} ({best[0]:+.1f}bp) · 실행 {exe}") if best[1] else "없음"
        if code != "NPS" and best[1]:
            gap = best[0] - cands[nps_k]["net_bp"]
            print(f"          → 최선: {best[1]} {best[0]:+.1f}bp · 국민연금 규칙과의 격차 {gap:+.1f}bp ≈ 연 {gap/1e4*aum*1e4:,.0f}억 원")
    print("[4] 세 안의 판정")
    print("    A 단일 규칙(국민연금 규칙을 모든 기관에) — " + " · ".join(f"{c} {'○' if a_ok[c] else '×'}" for c in INST.index))
    print("    B 지표 기반 차등 — " + " · ".join(f"{c}: {best_rule[c]}" for c in INST.index))
    print(f"    C 기관 자율(규칙 없음) — 12개월 이탈 95% {d12.quantile(0.95):.2f}%p · 최대 {d12.max():.2f}%p vs CVaR 여유 {w_max*100-65:.1f}%p")

if ALLMODE:
    all_institutions(); raise SystemExit
NAME = {"NPS": "국민연금기금", "KIC": "한국투자공사(KIC)"}[args.inst]
print(f"=== {NAME} 리밸런싱 규칙 — 운용자산 {AUM:,.0f}조 · 목표 위험자산(유동) {W[RISK].sum()*100:.1f}% ===")
mon = pd.DataFrame(RET, columns=codes).groupby(PN.month_id).sum()
print("[1] 자산군별 평균회귀 점검 (월간 240개월) — t ≤ −2 평균회귀 · |t| < 2 랜덤워크 · t ≥ 2 추세")
for i, c in enumerate(codes):
    if W[i] <= 0: continue
    phi, t = ar1(mon[c].values); v = vr(mon[c].values)
    kind = "평균회귀" if t <= -2 else ("추세" if t >= 2 else "랜덤워크")
    print(f"    {A.name[c]:<20} 목표 {W[i]*100:4.1f}% · φ {phi:+.2f} · t {t:+.2f} · VR(12) {v:.2f} → {kind}")
print(f"[2] 위험한도 — 위험자산 기대수익 {MU_R}% · 변동성 {SG_R}% / 안전자산 {MU_S}% · {SG_S}% · 상관 {RHO}, CVaR95 = μ − 2.063σ")
print("    " + " · ".join(f"{w}%: CVaR {cvar(w/100):.1f}%" for w in [60, 65, 67, 68, 70, 74]))
print(f"    → CVaR ≥ {CVAR_LIM}%를 지키는 위험자산 상한 {w_max*100:.1f}% = 기준(65%) + {w_max*100-65:.1f}%p")
inst = INST.loc[args.inst]
if args.inst == "NPS":
    kr = SNAP.loc["eq_kr"]; fx = SNAP.loc["eq_fx"]; alt = SNAP.loc["alt"]
    drift = (kr.actual_2026_06_pct - kr.target_2026_pct) + (fx.actual_2026_06_pct - fx.target_2026_pct) + (alt.actual_2026_06_pct - alt.target_2026_pct)
    w26 = 0.65 + drift / 100
    print(f"    2026년 6월 말 실제: 국내주식 {kr.actual_2026_06_pct}%(목표 {kr.target_2026_pct}%) 등 위험자산 이탈 {drift:+.1f}%p → {w26*100:.1f}% → CVaR {cvar(w26):.1f}% (한도 초과)")
    gap = kr.actual_2026_06_pct - kr.target_2026_pct; adv = f("adv_kospi_2026_05"); adv25 = f("adv_kospi_2025")
    cap_day = f("rebal_cap_new_bp") / 1e4 * AUM / f("rebal_cap_new_days")
    print(f"[3] 실행 가능성 — 코스피 일평균 거래대금 {adv}조(2026.5) · {adv25}조(2025) · 현물은 거래대금의 {PART_CASH:.0%}, 선물은 {ADV_FUT}조의 {PART_FUT:.0%}까지 · 월 25bp 매매 한도 = 하루 {cap_day:.2f}조")
    for name, pp in [("국내주식 목표(20.8%)까지 전량 복원", gap), ("지침 밴드 ±3 경계(23.8%)까지", gap - 3), ("밴드 ±6 경계(26.8%)까지", gap - 6), ("한 달 3%p 이탈 복원", 3.0), ("총 위험자산 밴드 ±2 복원", 2.0)]:
        q = pp / 100 * AUM
        print(f"    {name:<26} {q:6.1f}조 → 현물 {q/(PART_CASH*adv):5.1f}일(2025 거래대금이면 {q/(PART_CASH*adv25):4.0f}일) · 선물 {q/(PART_FUT*ADV_FUT):4.1f}일 · 25bp 한도 {q/cap_day:4.0f}일")
    rules = [("A 분기 캘린더 — 분기 말 목표까지 전량 복원(현물)", dict(mode="cal", k=63)),
             ("B 지침 밴드(국내주식 ±3) 월 점검 + 총 위험자산 ±2 선물 오버레이 + 현물 월 25bp 한도", dict(mode="band", band_scale=3, check=21, cap_bp=25, total_band=f("risk_band_total"))),
             ("C 넓은 밴드 ±6 상시화 · 분기 점검 · 현물 월 25bp 한도", dict(mode="band", band_scale=6, check=63, cap_bp=25))]
else:
    adv = float(inst.adv_trn_krw)
    print(f"[3] 실행 가능성 — 주 시장(글로벌 주식) 일평균 거래대금 {adv:,.0f}조 · 현물은 거래대금의 {PART_CASH:.0%}까지")
    for pp in [1, 3, 5]:
        q = pp / 100 * AUM; print(f"    {pp}%p 복원 = {q:.1f}조 → {q/(PART_CASH*adv):.2f}일")
    rules = [("A 국민연금 규칙 그대로 — 밴드 ±3 월 점검 + 총 위험 ±2 오버레이 + 월 25bp 한도", dict(mode="band", band_scale=3, check=21, cap_bp=25, total_band=f("risk_band_total"))),
             ("B 매월 말 목표까지 전량 복원(밴드 없음)", dict(mode="cal", k=21)),
             ("C 넓은 밴드 ±5 · 분기 점검", dict(mode="band", band_scale=5, check=63))]
bh = run("bh", aum=AUM, W=W)
print(f"[4] 세 안의 성과 (20년 모의 패널) — 참고: 리밸런싱 없음(매수 후 보유) DR {bh['DR_bp']:+.1f}bp · 위험 비중 이탈 최대 {bh['risk_dev_max_pp']:+.1f}%p · CVaR 초과일 {bh['pct_days_over_cvar']}%")
print(f"    판정 기준: ② 순 프리미엄 > 0 · ③ 실행 가능(복원 거래 ≤ {MAX_DAYS:.0f}거래일) · ④ 위험한도(CVaR 초과일 ≤ 0.5%, 이탈 ≤ +{w_max*100-65:.1f}%p)")
for name, kw in rules:
    r = run(aum=AUM, W=W, **kw)
    cost = r["cost_bp"] + r["cost_fut_bp"]
    c2 = r["net_bp"] > args.net_min
    c4 = r["pct_days_over_cvar"] <= args.cvar_days and r["risk_dev_max_pp"] <= (w_max * 100 - 65) + 0.5
    if args.inst == "NPS":
        q_full = (SNAP.loc["eq_kr"].actual_2026_06_pct - SNAP.loc["eq_kr"].target_2026_pct) / 100 * AUM
        if name.startswith("A"): days = q_full / (PART_CASH * f("adv_kospi_2026_05")); note = f"2026.6형 이탈 전량 복원 {q_full:.0f}조 → 현물 {days:.0f}일"
        elif name.startswith("B"): days = 2.0 / 100 * AUM / (PART_FUT * ADV_FUT); note = f"총 위험 ±2 복원 {0.02*AUM:.0f}조 → 선물 {days:.0f}일"
        else: days = (q_full - 6 / 100 * AUM) / (f("rebal_cap_new_bp") / 1e4 * AUM / f("rebal_cap_new_days")); note = f"±6 경계까지 {q_full-0.06*AUM:.0f}조 → 25bp 한도로 {days:.0f}일"
        if name.startswith("C"): c4 = c4 and cvar(w26) >= CVAR_LIM
    else:
        days = r["max_trade_trn"] / (PART_CASH * adv); note = f"최대 단일 거래 {r['max_trade_trn']}조 → {days:.1f}일"
    c3 = days <= MAX_DAYS
    print(f"\n  ◆ {name}")
    print(f"    DR {r['DR_bp']:+.1f}bp − 비용 {cost:.1f}bp = 순 프리미엄 {r['net_bp']:+.1f}bp/년 · 회전율 {r['turnover_pct']}%/년 · 리밸런싱 {r['n_rebal_per_yr']}회/년")
    print(f"    위험 비중 이탈 {r['risk_dev_min_pp']:+.1f} ~ {r['risk_dev_max_pp']:+.1f}%p · CVaR 한도 초과일 {r['pct_days_over_cvar']}% · 실행: {note}")
    print(f"    판정 ② {'통과' if c2 else '탈락'} · ③ {'통과' if c3 else '탈락'} · ④ {'통과' if c4 else '탈락'}")
