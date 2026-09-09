# -*- coding: utf-8 -*-
"""
W5 IC 케이스 — 판정 조건 계산 (기준일 2026-09-09)
  [제1호 NPS] 조건 ① 위험 집중 · 조건 ② 기준포트폴리오 정합(기대수익) · 조건 ③ 위험한도(shortfall·CVaR) · 조건 ④ 2022형 스트레스 · 조건 ⑤ HRP 안정성
  [제2호 KIC] 조건 ① 팩터 집중 · 조건 ② 기대수익 비용 · 조건 ③ BL 뷰(W4)와의 양립(TE·팩터 상한)
실행: python w5_compute.py  → w5_results.json, compute_log.txt
"""
import json, numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.cluster.hierarchy import linkage, to_tree
np.set_printoptions(suppress=True, precision=4)
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); print(s); LOG.append(s)

P = pd.read_csv("fml_w5_params.csv").set_index("param")["value"]
f = lambda k: float(P[k])
cma = pd.read_csv("fml_w5_cma.csv"); A6=list(cma.asset); KR=dict(zip(cma.asset,cma.asset_kr))
corr = pd.read_csv("fml_w5_corr.csv",index_col=0).loc[A6,A6].values
corr22 = pd.read_csv("fml_w5_corr_2022.csv",index_col=0).loc[A6,A6].values
mu6 = cma.mu.values; sg6 = cma.sigma.values
saa = pd.read_csv("fml_w5_saa.csv")
w_now6 = saa[saa.kind=="target_2027"].set_index("asset").loc[A6,"weight"].values
scen = pd.read_csv("fml_w5_scenarios.csv").set_index("scenario")

# 5 위험자산(단기자금 제외 — 잔여 0.1%는 무시)
A5=A6[:5]; mu=mu6[:5]; sg=sg6[:5]
Sig = np.outer(sg,sg)*corr[:5,:5]; Sig22 = np.outer(sg,sg)*corr22[:5,:5]
w_now = w_now6[:5]/w_now6[:5].sum()
EQ = np.array([1,1,0,0,0],bool)

def rc(w,S=Sig):
    m = S@w; v = w@m; return w*m/v
def port(w,S=Sig):
    return float(w@mu), float(np.sqrt(w@S@w))
def shortfall(m,s,T=f("horizon_years"),infl=f("inflation")):
    # 5년 누적 수익 < 5년 누적 물가 확률 (로그정규 근사)
    mlog = np.log(1+m)-0.5*s*s
    return float(norm.cdf((T*np.log(1+infl)-T*mlog)/(s*np.sqrt(T))))
def cvar95(m,s):
    return float(m - s*norm.pdf(norm.ppf(0.95))/0.05)
def scen_ret(w6):
    return {k: float(np.dot(w6, scen.loc[k,A6].values.astype(float))) for k in ["A","B","C","D"]}
def to6(w5):
    return np.append(w5*(1-f("cash_fixed")), f("cash_fixed"))

def metrics(name,w5):
    m,s = port(w5); s22 = float(np.sqrt(w5@Sig22@w5))
    r = rc(w5); w6=to6(w5)
    d = dict(name=name, w=dict(zip(A5,map(float,w5))), mu=m, sigma=s, sigma_2022corr=s22,
             rc=dict(zip(A5,map(float,r))), rc_equity=float(r[EQ].sum()),
             shortfall=shortfall(m,s), cvar95=cvar95(m,s), cvar95_2022corr=cvar95(m,s22),
             scen=scen_ret(w6))
    return d

# ---------- 후보 1: 현행 SAA ----------
cands = {}
cands["현행 SAA(2027 목표)"] = metrics("현행 SAA(2027 목표)", w_now)

# ---------- 후보 2: ERC (5자산, 무레버리지, 롱온리) ----------
def erc(S):
    n=len(S)
    def obj(w):
        r=rc(w,S); return float(((r-1/n)**2).sum())*1e4
    cons=[{"type":"eq","fun":lambda w: w.sum()-1}]
    res=minimize(obj,np.ones(n)/n,bounds=[(0,1)]*n,constraints=cons,method="SLSQP",options=dict(maxiter=500,ftol=1e-12))
    return res.x
w_erc = erc(Sig)
cands["ERC(위험 균등)"] = metrics("ERC(위험 균등)", w_erc)

# ---------- 후보 3: HRP (linkage 4종) ----------
def hrp(cov, corrm, method="single"):
    d = np.sqrt(0.5*(1-corrm)); n=len(cov)
    iu = np.triu_indices(n,1)
    Z = linkage(d[iu], method=method)
    order = to_tree(Z, rd=False).pre_order()
    w = np.ones(n)
    items=[order]
    while items:
        nxt=[]
        for it in items:
            if len(it)<=1: continue
            a=it[:len(it)//2]; b=it[len(it)//2:]
            def cvar(ix):
                c=cov[np.ix_(ix,ix)]; ivp=1/np.diag(c); ivp/=ivp.sum(); return float(ivp@c@ivp)
            va,vb=cvar(a),cvar(b); alpha=1-va/(va+vb)
            w[a]*=alpha; w[b]*=1-alpha
            nxt+= [a,b]
        items=nxt
    return w
hrp_w = {m: hrp(Sig,corr[:5,:5],m) for m in ["single","average","complete","ward"]}
for m,w in hrp_w.items():
    cands[f"HRP({m})"] = metrics(f"HRP({m})", w)

# ---------- 후보 4: 주식 RC 상한 프론티어 ----------
def cap_port(cap):
    n=5
    cons=[{"type":"eq","fun":lambda w: w.sum()-1},
          {"type":"ineq","fun":lambda w: cap - rc(w)[EQ].sum()},
          {"type":"ineq","fun":lambda w: f("alt_max") - w[4]},
          {"type":"ineq","fun":lambda w: w[0] - f("eq_kr_min")},
          {"type":"ineq","fun":lambda w: w[2] - f("bond_kr_min")},
          {"type":"ineq","fun":lambda w: f("bond_gl_max") - w[3]}]
    best=None
    for w0 in [w_now, np.ones(n)/n, w_erc, np.array([.2,.3,.3,.1,.1])]:
        res=minimize(lambda w:-w@mu, w0, bounds=[(0,1)]*n, constraints=cons, method="SLSQP", options=dict(maxiter=500,ftol=1e-12))
        if res.success and (best is None or res.fun<best.fun): best=res
    return best.x
caps=[float(x) for x in str(P["rc_cap_candidates"]).split(",")]
frontier=[]
for c in caps:
    w=cap_port(c); d=metrics(f"RC상한 {int(c*100)}%",w); d["cap"]=c; frontier.append(d)

# ---------- 기준포트폴리오(65:35) 기대수익 — 조건 ② 허들 ----------
eq_mix = w_now[:2]/w_now[:2].sum(); bd_mix = w_now[2:4]/w_now[2:4].sum()
mu_ref = 0.65*(eq_mix@mu[:2]) + 0.35*(bd_mix@mu[2:4])
sg_ref_w = np.array([0.65*eq_mix[0],0.65*eq_mix[1],0.35*bd_mix[0],0.35*bd_mix[1],0.0])
mu_ref_c, sg_ref = port(sg_ref_w)
hurdle = f("target_return")

# ---------- 판정 ----------
log("="*70); log("[제1호 NPS] 5자산 CMA(교육용) · 2027 목표 SAA 기준"); log("="*70)
c0=cands["현행 SAA(2027 목표)"]
log(f"[조건 ①] 현행 SAA 주식 위험기여 = {c0['rc_equity']*100:.1f}%  (자본 비중 {w_now[EQ].sum()*100:.1f}%)  σ={c0['sigma']*100:.2f}%  μ={c0['mu']*100:.2f}%")
log(f"     자산별 RC: " + ", ".join(f"{KR[a]} {c0['rc'][a]*100:.1f}%" for a in A5))
log(f"[조건 ②] 허들 — 기준포트폴리오 65:35 기대수익 {mu_ref*100:.2f}% (σ {sg_ref*100:.2f}%) · 구 목표수익률 표기 {hurdle*100:.1f}%")
log(f"[조건 ③] 위험한도 — CVaR95 ≥ {f('cvar95_cap')*100:.0f}% (정상 상관·2022형 상관 모두) · 참고 shortfall ≤ {f('shortfall_cap')*100:.0f}%(교육용 CMA에서는 전 후보 초과 — 판별력 없음)")
log(f"[조건 ④] 2022형 손실이 현행 SAA({c0['scen']['B']*100:.2f}%)보다 나쁘지 않을 것")
log("")
log(f"{'후보':26s} {'μ':>6s} {'σ':>6s} {'σ22':>6s} {'RCeq':>6s} {'SF':>6s} {'CVaR':>6s} {'CVaR22':>7s} {'A':>6s} {'B(2022)':>8s} {'C':>6s} {'D':>6s}  비중(국내주식·해외주식·국내채권·해외채권·대체)")
def row(d):
    w=d["w"]; ws="·".join(f"{w[a]*100:.0f}" for a in A5)
    log(f"{d['name']:26s} {d['mu']*100:6.2f} {d['sigma']*100:6.2f} {d['sigma_2022corr']*100:6.2f} {d['rc_equity']*100:6.1f} {d['shortfall']*100:6.1f} {d['cvar95']*100:6.1f} {d['cvar95_2022corr']*100:7.1f} {d['scen']['A']*100:6.1f} {d['scen']['B']*100:8.1f} {d['scen']['C']*100:6.1f} {d['scen']['D']*100:6.1f}  {ws}")
for d in cands.values(): row(d)
log("--- 주식 RC 상한 프론티어 (max μ s.t. RC_eq ≤ cap, 대체 ≤ 15%, 롱온리) ---")
for d in frontier: row(d)

# 결정: 조건 ②(μ ≥ 기준포트폴리오 μ − 허용폭 0.5%p? → 아니오: 기준포트폴리오와 동등 이상) · 조건 ③ · 조건 ④ 통과 후보 중 RC_eq 최소
def passes(d, hurdle_mu):
    return {"조건 ②": d["mu"]>=hurdle_mu-1e-9, "조건 ③": (d["cvar95"]>=f("cvar95_cap")) and (d["cvar95_2022corr"]>=f("cvar95_cap")),
            "조건 ④": d["scen"]["B"]>=c0["scen"]["B"]-1e-9}
log("")
log("[판정] 허들 = 기준포트폴리오 μ")
ok=[]
for d in frontier+list(cands.values()):
    p=passes(d,mu_ref); allp=all(p.values())
    log(f"  {d['name']:26s} 조건 ② {'통과' if p['조건 ②'] else '미달'} · 조건 ③ {'통과' if p['조건 ③'] else '미달'} · 조건 ④ {'통과' if p['조건 ④'] else '미달'}  → {'가능' if allp else '배제'}")
    if allp: ok.append(d)
x_star_ref = min(ok,key=lambda d:d["rc_equity"]) if ok else None
log(f"  → 통과 후보 중 주식 RC 최소: {x_star_ref['name'] if x_star_ref else '없음'}")
log(f"[판정] 허들 = 연금개혁 전제 기금수익률 {hurdle*100:.1f}%")
ok2=[]
for d in frontier+list(cands.values()):
    p=passes(d,hurdle); allp=all(p.values())
    log(f"  {d['name']:26s} 조건 ② {'통과' if p['조건 ②'] else '미달'} · 조건 ③ {'통과' if p['조건 ③'] else '미달'} · 조건 ④ {'통과' if p['조건 ④'] else '미달'}  → {'가능' if allp else '배제'}")
    if allp: ok2.append(d)
x_star_52 = min(ok2,key=lambda d:d["rc_equity"]) if ok2 else None
log(f"  → 통과 후보 중 주식 RC 최소: {x_star_52['name'] if x_star_52 else '없음'}")

# ---------- 조건 ⑤ HRP 안정성: linkage 범위 + 부트스트랩 ----------
log(""); log("[조건 ⑤] HRP 안정성")
rcs={m:cands[f'HRP({m})']['rc_equity'] for m in hrp_w}
log("  linkage별 주식 RC: " + ", ".join(f"{m} {v*100:.1f}%" for m,v in rcs.items()) + f"  → 범위 {(max(rcs.values())-min(rcs.values()))*100:.1f}%p")
panel = pd.read_csv("fml_w5_panel_sim.csv"); R = panel[[a+"_ret" for a in A5]].values
rng=np.random.default_rng(60080); boot=[]
for _ in range(300):
    idx=rng.integers(0,len(R),len(R)); Rb=R[idx]; C=np.cov(Rb.T)*12; cm=np.corrcoef(Rb.T)
    wb=hrp(C,cm,"single"); boot.append(rc(wb,C)[EQ].sum())
q=np.percentile(boot,[5,50,95])
log(f"  부트스트랩(300회, single) 주식 RC 5·50·95% = {q[0]*100:.1f} · {q[1]*100:.1f} · {q[2]*100:.1f}%")

# ================= 제2호 KIC =================
log(""); log("="*70); log("[제2호 KIC] 5자산 · 4팩터(교육용 가정)"); log("="*70)
kic = pd.read_csv("fml_w5_kic_factor.csv"); KA=list(kic.asset); KKR=dict(zip(kic.asset,kic.asset_kr))
B = kic[["b_growth","b_rates","b_credit","b_illiq"]].values
fs = pd.read_csv("fml_w5_kic_factor_sigma.csv"); FN=list(fs.factor); FKR=dict(zip(fs.factor,fs.factor_kr))
Fc = pd.read_csv("fml_w5_kic_factor_corr.csv",index_col=0).loc[FN,FN].values
Fcov = np.outer(fs.sigma.values,fs.sigma.values)*Fc
kcorr = pd.read_csv("fml_w5_kic_corr.csv",index_col=0).loc[KA,KA].values
ksig = kic.sigma.values; KSig = np.outer(ksig,ksig)*kcorr
wk = kic.w_now.values
delta=f("delta"); tau=f("tau")
pi = delta*KSig@wk                      # W4와 동일한 역최적화
def frc(w):
    e=B.T@w; v=e@Fcov@e; return e*(Fcov@e)/v, float(np.sqrt(v))
r0,fv0 = frc(wk)
log(f"현행 KIC 비중 {dict(zip(KA,wk))} · π(δ=2.5) = " + ", ".join(f"{KKR[a]} {x*100:.2f}%" for a,x in zip(KA,pi)))
log(f"[조건 ①] 팩터 위험기여(현행): " + ", ".join(f"{FKR[k]} {v*100:.1f}%" for k,v in zip(FN,r0)) + f"  (팩터 σ {fv0*100:.2f}%)  → 최대 {max(r0)*100:.1f}% vs 상한 {f('factor_rc_cap')*100:.0f}%")
mu_k0 = float(wk@pi)
# 팩터 ERC (무레버리지 롱온리)
def ferc():
    def obj(w):
        r,_=frc(w); return float(((r-0.25)**2).sum())*1e4
    res=minimize(obj,np.ones(5)/5,bounds=KB,constraints=[{"type":"eq","fun":lambda w:w.sum()-1}],method="SLSQP",options=dict(maxiter=500,ftol=1e-12))
    return res.x
KB=[(0.30,1),(0.10,1),(0,1),(0,0.15),(0,0.10)]   # 교육용 제도 제약: 주식 ≥30 · 미 국채 ≥10 · PE ≤15 · 인프라 ≤10
w_ferc=ferc(); r_ferc,_=frc(w_ferc); mu_ferc=float(w_ferc@pi)
log(f"     제도 제약(교육용): 글로벌 주식 ≥30% · 미 국채 ≥10% · PE ≤15% · 인프라 ≤10%")
log(f"[조건 ②] 팩터 ERC(제약) 비중: " + ", ".join(f"{KKR[a]} {x*100:.1f}%" for a,x in zip(KA,w_ferc)) + f" · 팩터 RC " + ", ".join(f"{v*100:.0f}" for v in r_ferc) + f" · μ {mu_ferc*100:.2f}% (현행 {mu_k0*100:.2f}%, Δ {(mu_ferc-mu_k0)*100:+.2f}%p vs 허용 −{f('mu_loss_cap')*100:.1f}%p)")
# 팩터 상한형(max μ s.t. max factor RC ≤ cap)
def fcap(cap):
    cons=[{"type":"eq","fun":lambda w:w.sum()-1},{"type":"ineq","fun":lambda w: cap-frc(w)[0].max()}]
    best=None
    for w0 in [wk,np.ones(5)/5,w_ferc]:
        res=minimize(lambda w:-w@pi,w0,bounds=KB,constraints=cons,method="SLSQP",options=dict(maxiter=500,ftol=1e-12))
        if res.success and (best is None or res.fun<best.fun): best=res
    return best.x if best is not None else None
fcaps=[0.80,0.70,0.60,0.50]; ftab=[]
for c in fcaps:
    w=fcap(c)
    if w is None:
        log(f"     팩터 상한 {int(c*100)}%: 제도 제약 아래 실행 불가(주식 ≥30%만으로 성장 팩터 RC가 상한을 넘는다)"); continue
    r,_=frc(w); m=float(w@pi)
    ftab.append(dict(cap=c,w=dict(zip(KA,map(float,w))),frc=dict(zip(FN,map(float,r))),mu=m,dmu=m-mu_k0))
    log(f"     팩터 상한 {int(c*100)}%: μ {m*100:.2f}% (Δ {(m-mu_k0)*100:+.2f}%p) · 비중 " + "·".join(f"{x*100:.0f}" for x in w) + " · 팩터 RC " + "·".join(f"{v*100:.0f}" for v in r))
n2_ok=[t for t in ftab if t["dmu"]>=-f("mu_loss_cap")]
fcap_star=min(n2_ok,key=lambda t:t["cap"]) if n2_ok else None
log(f"     → 기대수익 하락 ≤ {f('mu_loss_cap')*100:.1f}%p 안에서 가장 낮은 상한: {int(fcap_star['cap']*100) if fcap_star else '없음'}%")

# [조건 ③] BL 뷰(W4 시트, 자신감 상한 20%) → 사후 비중 → 팩터 RC·TE
V = pd.read_csv("fml_w5_kic_views.csv")
Pm = V[["p_eq_gl","p_ust","p_ig","p_alt_pe","p_alt_infra"]].values.astype(float); Q=V.q.values.astype(float)
conf = np.minimum(V.confidence.values.astype(float), f("confidence_cap"))
def bl_post(P_,Q_,Om):
    tS=tau*KSig
    M = np.linalg.inv(np.linalg.inv(tS)+P_.T@np.linalg.inv(Om)@P_)
    mu_bl = M@(np.linalg.inv(tS)@pi + P_.T@np.linalg.inv(Om)@Q_)
    return mu_bl, np.linalg.inv(delta*KSig)@mu_bl
def idzorek_omega(P_,Q_,conf_):
    # 각 뷰를 100% 확신으로 반영했을 때의 비중 이동 × 자신감 = 목표 이동 → Ω 역산(1차원 탐색)
    om=[]
    for i in range(len(Q_)):
        pk=P_[i:i+1]; qk=Q_[i:i+1]
        mu100 = pi + tau*KSig@pk.T@np.linalg.inv(pk@(tau*KSig)@pk.T)@(qk-pk@pi)
        w100 = np.linalg.inv(delta*KSig)@mu100
        target = wk + conf_[i]*(w100-wk)
        best=None
        for o in np.logspace(-7,-1,400):
            _,w=bl_post(pk,qk,np.array([[o]]))
            err=float(((w-target)**2).sum())
            if best is None or err<best[0]: best=(err,o)
        om.append(best[1])
    return np.diag(om)
Om = idzorek_omega(Pm,Q,conf)
mu_bl,w_bl = bl_post(Pm,Q,Om)
w_bl_n = w_bl/ w_bl.sum()
te = float(np.sqrt((w_bl_n-wk)@KSig@(w_bl_n-wk)))
w_bl_raw=w_bl_n.copy(); te_raw=te
if te>f("te_budget"):
    w_bl_n = wk + (w_bl_n-wk)*f("te_budget")/te
    te = float(np.sqrt((w_bl_n-wk)@KSig@(w_bl_n-wk)))
r_bl,_=frc(w_bl_n)
log(f"[조건 ③] 자신감 ≤20% 원사후 비중 TE {te_raw*100:.2f}% → TE 예산 1.0%로 축소")
log(f"[조건 ③] W4 뷰 시트(자신감 ≤20%) BL 사후 비중: " + ", ".join(f"{KKR[a]} {x*100:.1f}%" for a,x in zip(KA,w_bl_n)) + f" · TE {te*100:.2f}% (예산 {f('te_budget')*100:.1f}%) · 팩터 RC " + ", ".join(f"{FKR[k]} {v*100:.1f}%" for k,v in zip(FN,r_bl)) + f" → 최대 {max(r_bl)*100:.1f}%")
capstar = fcap_star["cap"] if fcap_star else f("factor_rc_cap")
log(f"     조건 ②가 고른 팩터 상한 {int(capstar*100)}% 안에 {'있음 → 뷰는 위험예산 봉투 안에서 작동' if max(r_bl)<=capstar else '없음 → TE 예산 안이어도 뷰가 팩터 봉투를 넘는다 → 뷰 반영은 팩터 상한을 제약으로 두고 다시 푼다'} · TE {'예산 안' if te<=f('te_budget')+1e-9 else '예산 초과'}")
# 봉투 안 뷰 반영: 기준 배분을 조건 ②의 상한형(80%) 배분으로 옮긴 뒤, 뷰 틸트(w_BL − w_mkt)를 TE 1% 안에서 얹고,
# 성장 팩터 RC가 상한을 넘으면 틸트를 줄인다(위험예산이 뷰를 자른다).
w_base = np.array([fcap_star["w"][a] for a in KA]) if fcap_star else wk
tilt = (w_bl_n - wk)
def with_tilt(k):
    w = w_base + k*tilt; return w/w.sum()
k=1.0; w_env=with_tilt(k); r_full,_=frc(w_env)
log(f"     상한형 {int(capstar*100)}% 배분 위에 뷰 틸트를 100% 얹으면 성장 RC {r_full[0]*100:.1f}% (상한 초과분 {(r_full[0]-capstar)*100:+.1f}%p)")
while frc(w_env)[0].max()>capstar+1e-9 and k>0:
    k-=0.01; w_env=with_tilt(k)
r_env,_=frc(w_env); te_env=float(np.sqrt((w_env-w_base)@KSig@(w_env-w_base)))
log(f"     경직 상한(밴드 0): 기준 배분을 상한형 {int(capstar*100)}% 배분(" + "·".join(f"{x*100:.0f}" for x in w_base) + f")으로 옮긴 뒤 뷰 틸트를 얹으면 틸트 {k*100:.0f}%만 남는다(성장 RC {r_env[0]*100:.1f}%) — 뷰가 전부 잘린다")
band=f("factor_cap_band"); kb=1.0; w_envb=with_tilt(kb)
while frc(w_envb)[0].max()>capstar+band+1e-9 and kb>0:
    kb-=0.01; w_envb=with_tilt(kb)
r_envb,_=frc(w_envb); te_envb=float(np.sqrt((w_envb-w_base)@KSig@(w_envb-w_base)))
log(f"     운영 밴드 +{band*100:.0f}%p: 틸트 {kb*100:.0f}% 반영 · 성장 RC {r_envb[0]*100:.1f}% (≤ {int((capstar+band)*100)}%) · TE {te_envb*100:.2f}% → 뷰는 살아 있고 봉투는 지켜진다 — 'BL과 위험예산의 충돌'(질문 ①)의 해법은 상한 + 밴드")
k=kb; w_env=w_envb; r_env=r_envb; te_env=te_envb
out=dict(assets=A5, assets_kr=[KR[a] for a in A5], w_now=dict(zip(A5,map(float,w_now))), mu_ref=float(mu_ref), sigma_ref=float(sg_ref), hurdle_old=hurdle,
         cands={k:v for k,v in cands.items()}, frontier=frontier, x_star_ref=x_star_ref["name"] if x_star_ref else None, x_star_52=x_star_52["name"] if x_star_52 else None,
         hrp_linkage_rc=rcs, boot_q=list(map(float,q)),
         kic=dict(assets=KA, pi=dict(zip(KA,map(float,pi))), w_now=dict(zip(KA,map(float,wk))), frc_now=dict(zip(FN,map(float,r0))), mu_now=mu_k0,
                  ferc=dict(w=dict(zip(KA,map(float,w_ferc))),frc=dict(zip(FN,map(float,r_ferc))),mu=mu_ferc), fcap_table=ftab, fcap_star=fcap_star["cap"] if fcap_star else None,
                  bl=dict(w=dict(zip(KA,map(float,w_bl_n))),te=te,frc=dict(zip(FN,map(float,r_bl))),omega=list(map(float,np.diag(Om))),conf=list(map(float,conf))),
                  bl_env=dict(w=dict(zip(KA,map(float,w_env))),te=te_env,frc=dict(zip(FN,map(float,r_env))),cap=capstar,tilt_kept=k,frc_full_tilt=dict(zip(FN,map(float,r_full))),w_base=dict(zip(KA,map(float,w_base))))))
json.dump(out,open("w5_results.json","w"),ensure_ascii=False,indent=1)
open("compute_log.txt","w").write("\n".join(LOG))
