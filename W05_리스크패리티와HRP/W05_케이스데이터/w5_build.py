# -*- coding: utf-8 -*-
"""
W5 IC 케이스 데이터 생성 — 기준일 2026-09-09
CSV 7개를 만든다. 공시 수치는 is_assumed=0, 교육용 가정은 is_assumed=1.
자산 6개(eq_kr·eq_gl·bond_kr·bond_gl·alt·cash)의 CMA·상관은 W4 케이스 데이터와 같은 값이다(모의 패널은 별도 생성)
(W2 패널 → W4 공분산 → W5 ERC/HRP 재사용 원칙). 바꾸려면 여기서 바꾼다.
"""
import numpy as np, pandas as pd
ASOF = "2026-09-09"

# ---------- 1. NPS SAA (공시) ----------
saa = [
 ("NPS","eq_kr","국내주식","target_2027",0.208,"2026-05-28","기금운용위원회 의결(2026.5.28) · 정책브리핑",0),
 ("NPS","eq_gl","해외주식","target_2027",0.356,"2026-05-28","기금운용위원회 의결(2026.5.28) · 정책브리핑",0),
 ("NPS","bond_kr","국내채권","target_2027",0.218,"2026-05-28","기금운용위원회 의결(2026.5.28) · 정책브리핑",0),
 ("NPS","bond_gl","해외채권","target_2027",0.074,"2026-05-28","기금운용위원회 의결(2026.5.28) · 정책브리핑",0),
 ("NPS","alt","대체투자","target_2027",0.143,"2026-05-28","기금운용위원회 의결(2026.5.28) · 정책브리핑",0),
 ("NPS","cash","단기자금","target_2027",0.001,"2026-05-28","잔여(교육용 가정)",1),
 ("NPS","equity","주식(국내+해외)","target_2031",0.55,"2026-05-28","기금운용위원회 의결(2026.5.28)",0),
 ("NPS","bond","채권(국내+해외)","target_2031",0.30,"2026-05-28","기금운용위원회 의결(2026.5.28)",0),
 ("NPS","alt","대체투자","target_2031",0.15,"2026-05-28","기금운용위원회 의결(2026.5.28)",0),
 ("NPS","risky","위험자산(기준포트폴리오)","reference_longterm",0.65,"2024-05-02","기금운용위원회 의결(2024.5) — 장기 운용방향 65:35, 대체투자부터 적용",0),
 ("NPS","safe","안전자산(기준포트폴리오)","reference_longterm",0.35,"2024-05-02","기금운용위원회 의결(2024.5)",0),
]
pd.DataFrame(saa,columns=["institution","asset","asset_kr","kind","weight","asof","source","is_assumed"]).to_csv("fml_w5_saa.csv",index=False)

# ---------- 2. CMA (W4와 동일, 교육용 가정) ----------
cma = pd.DataFrame({
 "asset":["eq_kr","eq_gl","bond_kr","bond_gl","alt","cash"],
 "asset_kr":["국내주식","해외주식","국내채권","해외채권","대체투자","단기자금"],
 "mu":[0.075,0.080,0.035,0.038,0.070,0.025],
 "sigma":[0.18,0.16,0.05,0.06,0.12,0.005],
})
cma["asof"]=ASOF; cma["source"]="W4 강의 Part A 입력과 동일(교육용 가정)"; cma["is_assumed"]=1
cma.to_csv("fml_w5_cma.csv",index=False)

# ---------- 3. 상관 — 정상 체제(W4와 동일) / 2022형 체제(교육용 가정) ----------
A = ["eq_kr","eq_gl","bond_kr","bond_gl","alt","cash"]
corr_normal = np.array([
 [1.00,0.70,0.10,0.05,0.55,0.00],
 [0.70,1.00,0.05,0.15,0.60,0.00],
 [0.10,0.05,1.00,0.50,0.10,0.10],
 [0.05,0.15,0.50,1.00,0.15,0.10],
 [0.55,0.60,0.10,0.15,1.00,0.00],
 [0.00,0.00,0.10,0.10,0.00,1.00]])
# 2022형: 주식-채권 상관이 +0.5로 뒤집힌다(강의 3교시 "정상기 −0.2 → 2022 +0.5"를 자산군 수준으로 옮긴 교육용 가정)
corr_2022 = np.array([
 [1.00,0.80,0.50,0.45,0.60,0.00],
 [0.80,1.00,0.45,0.55,0.65,0.00],
 [0.50,0.45,1.00,0.70,0.30,0.10],
 [0.45,0.55,0.70,1.00,0.35,0.10],
 [0.60,0.65,0.30,0.35,1.00,0.00],
 [0.00,0.00,0.10,0.10,0.00,1.00]])
pd.DataFrame(corr_normal,index=A,columns=A).to_csv("fml_w5_corr.csv")
pd.DataFrame(corr_2022,index=A,columns=A).to_csv("fml_w5_corr_2022.csv")

# ---------- 4. 시나리오 — 자산군 수익률 (B는 NPS 2022 공시 실적, 나머지는 교육용 가정) ----------
scen = [
 # scenario, label, eq_kr, eq_gl, bond_kr, bond_gl, alt, cash, source, is_assumed
 ("A","정상기 2012–2019(연율)",0.040,0.110,0.035,0.035,0.070,0.018,"교육용 가정 — KOSPI 총수익·MSCI World(원화)·KTB 지수 2012–19 연율에 근사",1),
 ("B","2022년형 — 인플레 충격",-0.2276,-0.1234,-0.0556,-0.0491,0.0894,0.020,"NPS 2022 자산군별 수익률 공시(금액가중, 잠정) · 단기자금은 교육용 가정",0),
 ("C","2008년형 — 금융위기",-0.39,-0.25,0.10,0.15,-0.05,0.050,"교육용 가정 — KOSPI −40.7%, MSCI World 원화 환산(환율 상승 상쇄), 국고채 강세, 해외채권 환차익",1),
 ("D","스태그플레이션(1970년대형)",-0.10,-0.08,-0.06,-0.05,0.06,0.040,"교육용 가정 — 주식·채권 동반 하락, 실물자산 방어",1),
]
pd.DataFrame(scen,columns=["scenario","label","eq_kr","eq_gl","bond_kr","bond_gl","alt","cash","source","is_assumed"]).to_csv("fml_w5_scenarios.csv",index=False)

# ---------- 5. 판정 파라미터 ----------
params = [
 ("target_return","0.055",ASOF,"2025.3 연금개혁 전제 — 기금수익률 5.5%(기존 4.5%에서 1%p 제고). 기금위는 2025.5.29부터 중기자산배분에서 '목표수익률' 용어를 쓰지 않는다(2025–2029 표기 5.4%)",0),
 ("inflation","0.020",ASOF,"교육용 가정(shortfall 기준선 = 5년 누적 물가)",1),
 ("shortfall_cap","0.10",ASOF,"기금운용지침 위험한도 — 5년 누적 수익률이 5년 누적 물가 이하일 확률 10% 이내(교육용 표기)",0),
 ("cvar95_cap","-0.15",ASOF,"기준포트폴리오 위험한도 — 95% CVaR −15% 이내(기금운용지침)",0),
 ("horizon_years","5",ASOF,"2027–2031",0),
 ("rc_cap_candidates","0.90,0.80,0.70,0.60,0.50,0.40",ASOF,"주식 위험기여 상한 후보(교육용)",1),
 ("alt_max","0.15",ASOF,"대체투자 상한 — 2031 목표 15% 내외",0),
 ("cash_fixed","0.001",ASOF,"단기자금은 배분 대상에서 제외(잔여)",1),
 ("rc_concentration_line","0.75",ASOF,"위험 집중 기준선 — 강의 Part A '주식 RC ~75%'를 기준선으로(교육용)",1),
 ("eq_kr_min","0.15",ASOF,"국내주식 하한(교육용 가정) — 2027 목표 20.8%·2031 상한 19.4%(W4 K3) 사이의 정책 하한",1),
 ("bond_kr_min","0.15",ASOF,"국내채권 하한(교육용 가정) — 급여 지급·유동성",1),
 ("bond_gl_max","0.15",ASOF,"해외채권 상한(교육용 가정) — 2027 목표 7.4%의 2배",1),
 ("te_budget","0.010",ASOF,"W4 제1호 조건 — BL 뷰의 TE 예산 1.0%",0),
 ("factor_rc_cap","0.60",ASOF,"KIC 팩터 위험기여 상한 후보(교육용)",1),
 ("mu_loss_cap","0.005",ASOF,"위험예산 도입으로 허용하는 기대수익 하락 상한 0.5%p(교육용)",1),
 ("delta","2.5",ASOF,"BL 위험회피(W4와 동일)",1),
 ("tau","0.025",ASOF,"BL τ(W4와 동일)",1),
 ("factor_cap_band","0.02",ASOF,"팩터 상한의 운영 밴드 ±2%p(교육용) — SAA·TAA 허용범위처럼 뷰 틸트가 쓰는 여유",1),
 ("confidence_cap","0.20",ASOF,"W4 제1호 기본 답 — 이력 없는 뷰의 자신감 상한 20%",0),
]
pd.DataFrame(params,columns=["param","value","asof","source","is_assumed"]).to_csv("fml_w5_params.csv",index=False)

# ---------- 6. KIC 5자산 + 4팩터 (W4 입력 재사용 + 교육용 팩터 적재) ----------
kic = pd.DataFrame({
 "asset":["eq_gl","ust","ig","alt_pe","alt_infra"],
 "asset_kr":["글로벌 주식","미 국채","IG 채권","PE","인프라"],
 "w_now":[0.50,0.20,0.15,0.10,0.05],
 "sigma":[0.15,0.06,0.05,0.20,0.12],
 "b_growth":[1.00,0.00,0.10,1.20,0.50],
 "b_rates":[0.00,1.00,0.80,0.00,0.40],
 "b_credit":[0.10,0.00,1.00,0.20,0.20],
 "b_illiq":[0.00,0.00,0.00,1.00,0.80],
})
kic["asof"]=ASOF; kic["source"]="w_now·sigma는 W4 KIC 입력(교육용 가정), 팩터 적재 b_*는 교육용 가정"; kic["is_assumed"]=1
kic.to_csv("fml_w5_kic_factor.csv",index=False)
F = ["growth","rates","credit","illiq"]
fcorr = np.array([[1.0,-0.2,0.5,0.6],[-0.2,1.0,0.3,0.0],[0.5,0.3,1.0,0.3],[0.6,0.0,0.3,1.0]])
fsig = np.array([0.15,0.055,0.04,0.07])
fc = pd.DataFrame(fcorr,index=F,columns=F); fc.to_csv("fml_w5_kic_factor_corr.csv")
pd.DataFrame({"factor":F,"factor_kr":["성장(주식)","금리(듀레이션)","크레딧","비유동성"],"sigma":fsig,"asof":ASOF,"source":"교육용 가정","is_assumed":1}).to_csv("fml_w5_kic_factor_sigma.csv",index=False)
# KIC 5자산 상관(W4와 동일) — BL 검정용
kc = np.array([[1,-0.1,0.2,0.7,0.5],[-0.1,1,0.6,-0.1,0.1],[0.2,0.6,1,0.1,0.2],[0.7,-0.1,0.1,1,0.45],[0.5,0.1,0.2,0.45,1]],float)
pd.DataFrame(kc,index=kic.asset,columns=kic.asset).to_csv("fml_w5_kic_corr.csv")
# 뷰 시트(W4와 동일)
views = pd.DataFrame([
 (1,"미 국채 초과수익 0.5%로 상승","absolute",0,1,0,0,0,0.005,0.7),
 (2,"미 국채가 IG 채권을 0.2%p 상회","relative",0,1,-1,0,0,0.002,0.6),
 (3,"PE 초과수익 2.5%에 그침","absolute",0,0,0,1,0,0.025,0.5)],
 columns=["view_id","view_kr","view_type","p_eq_gl","p_ust","p_ig","p_alt_pe","p_alt_infra","q","confidence"])
views["asof"]=ASOF; views["source"]="W4 제1호 뷰 시트(교육용 가정)"; views["is_assumed"]=1
views.to_csv("fml_w5_kic_views.csv",index=False)

# ---------- 7. 모의 월간 패널 (seed 60080, 부트스트랩 전용 — 실제 수익률이 아니다) ----------
rng = np.random.default_rng(60080)
mu_m = cma.mu.values/12; sig_m = cma.sigma.values/np.sqrt(12)
cov = np.outer(sig_m,sig_m)*corr_normal
R = rng.multivariate_normal(mu_m,cov,size=120)
dates = pd.date_range("2016-09-30",periods=120,freq="ME")
panel = pd.DataFrame(R,columns=[a+"_ret" for a in A]); panel.insert(0,"date",dates.strftime("%Y-%m-%d")); panel["rf"]=0.025/12
panel.to_csv("fml_w5_panel_sim.csv",index=False)
print("CSV 생성 완료")
