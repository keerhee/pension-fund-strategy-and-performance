#!/usr/bin/env python3
"""Das–Markowitz–Scheid–Statman(2010) 심리계정 덱 — 수식 PNG · matplotlib 차트 · SVG 도해.
실행: <python> assets.py   (작업 폴더 기준: eq/ fig/ svg/ · ratios.json · numbers.json)
숫자는 전부 원 논문 식 (4)의 μ·Σ에서 numpy로 재계산한다(논문 표와 대조는 numbers.json).
"""
import os, json
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq, minimize, minimize_scalar
import cairosvg
from render_eq import render, INK, PAPER, LIME, DARK, WHITE
from zo_mpl import fig, save, C

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
for d in ("eq", "fig", "svg"):
    os.makedirs(d, exist_ok=True)
R, NUM = {}, {}

# =============================================================== 계산
mu = np.array([0.05, 0.10, 0.25])
S = np.array([[0.0025, 0, 0], [0, 0.04, 0.02], [0, 0.02, 0.25]])
one = np.ones(3)
Si = np.linalg.inv(S)
A, B, Cc = one @ Si @ mu, mu @ Si @ mu, one @ Si @ one
D = B * Cc - A * A
K = D / Cc
g = Si @ one / Cc
v = Si @ (mu - A / Cc * one)


def w_of(gam):
    return Si @ (mu - (A - gam) / Cc * one) / gam


def ms(x):
    return float(x @ mu), float(np.sqrt(x @ S @ x))


def gamma_of(H, a):
    f = lambda gm: A / Cc + K / gm + norm.ppf(a) * np.sqrt(1 / Cc + K / gm ** 2) - H
    return brentq(f, 0.05, 30)


ACC = [("은퇴", -0.10, 0.05), ("교육", -0.05, 0.15), ("상속", -0.15, 0.20)]
GAM = [gamma_of(H, a) for _, H, a in ACC]
WS = [w_of(gm) for gm in GAM]
a_k = np.array([0.6, 0.2, 0.2])
AGG = a_k @ np.array(WS)
G_TOT = 1 / (a_k @ (1 / np.array(GAM)))
z5 = -norm.ppf(0.05)
QMAX = A / Cc - np.sqrt((z5 ** 2 - K) / Cc)

cons = [{"type": "eq", "fun": lambda x: x.sum() - 1}]


def qp(gam):
    r = minimize(lambda x: -(x @ mu - gam / 2 * x @ S @ x), np.ones(3) / 3, bounds=[(0, 1)] * 3,
                 constraints=cons, method="SLSQP", options={"ftol": 1e-14, "maxiter": 500})
    return r.x


def lo_account(H, a):
    zz = norm.ppf(a)
    r = minimize(lambda x: -(x @ mu), np.ones(3) / 3, bounds=[(0, 1)] * 3,
                 constraints=cons + [{"type": "ineq", "fun": lambda x: x @ mu + zz * np.sqrt(x @ S @ x) - H}],
                 method="SLSQP", options={"ftol": 1e-14})
    return np.clip(r.x, 0, 1)


def lo_frontier_m(sig):
    r = minimize(lambda x: -(x @ mu), np.ones(3) / 3, bounds=[(0, 1)] * 3,
                 constraints=cons + [{"type": "ineq", "fun": lambda x: sig ** 2 - x @ S @ x}],
                 method="SLSQP", options={"ftol": 1e-15})
    return float(r.x @ mu)


LO = [lo_account(H, a) for _, H, a in ACC]
AGG_LO = a_k @ np.array(LO)
m_lo, s_lo = ms(AGG_LO)
FRONT_LO = lo_frontier_m(s_lo)
U = lambda x, gm: x @ mu - gm / 2 * x @ S @ x


def misspec(gm, e):
    return np.mean([U(w_of(gm), gm) - U(w_of(gm * (1 + sg * e)), gm) for sg in (1, -1)]) * 1e4


# 손계산 예
x60 = np.array([0.6, 0.3, 0.1]); m60, s60 = ms(x60)
quad = [0.05 ** 2 - z5 ** 2 * (0.0025 + 0.04), 2 * 0.15 * 0.05 + z5 ** 2 * 2 * 0.0025, 0.15 ** 2 - z5 ** 2 * 0.0025]
w2 = max(np.roots(quad))
# 대안
g_h3 = brentq(lambda gm: A / Cc + K / gm - z5 * np.sqrt(1 / Cc + K / gm ** 2) + 0.03, 0.5, 32.7)
roy_sf = np.sqrt(B * Cc - 0) and None
m_roy, s_roy = ms(Si @ mu / A)

NUM.update(A=A, B=B, C=Cc, D=D, K=K, g=g.tolist(), v=v.tolist(), gammas=GAM,
           weights=[x.tolist() for x in WS], ms=[ms(x) for x in WS],
           p_loss=[float(norm.cdf(-ms(x)[0] / ms(x)[1])) for x in WS] + [float(norm.cdf(-ms(AGG)[0] / ms(AGG)[1]))],
           agg=AGG.tolist(), agg_ms=ms(AGG), gamma_tot=G_TOT, gamma_arith=float(a_k @ GAM),
           wavg_sd=float(a_k @ [ms(x)[1] for x in WS]),
           qmax=QMAX, check60=(m60, s60, m60 - z5 * s60, float(norm.cdf((-0.10 - m60) / s60))),
           two_asset=dict(quad=quad, w=float(w2)), gamma_H3=g_h3, ms_H3=ms(w_of(g_h3)), w_H3=w_of(g_h3).tolist(),
           roy=dict(m=m_roy, s=s_roy, alpha_min=float(norm.cdf(-m_roy / s_roy)), w=(Si @ mu / A).tolist()),
           lo=[x.tolist() for x in LO], lo_ms=[ms(x) for x in LO], agg_lo=AGG_LO.tolist(), agg_lo_ms=(m_lo, s_lo),
           front_lo=FRONT_LO, loss_bp=(FRONT_LO - m_lo) * 1e4, front_at_1989=lo_frontier_m(0.1989),
           misspec={f"{gm:.4f}": [misspec(gm, e) for e in (0.1, 0.2, 0.3)] for gm in (3.7950, 2.7063, 0.8773)},
           gamma_3975=ms(w_of(3.975)))
json.dump(NUM, open("numbers.json", "w"), indent=1, ensure_ascii=False, default=float)
print(json.dumps({k: NUM[k] for k in ("gammas", "gamma_tot", "qmax", "loss_bp", "agg_lo_ms", "front_lo")}, default=float))


# =============================================================== 수식
def eq(name, tex, fs=30, dark=False, white=False):
    bg = DARK if dark else (WHITE if white else PAPER)
    col = LIME if dark else INK
    _, r = render(tex, name + ".png", fontsize=fs, color=col, bg=bg)
    R["eq/" + name] = r


T1, Si_ = r"^{\top}", r"\Sigma^{-1}"
eq("mvt", r"\max_{w}\ w^{\top}\mu-\frac{\gamma}{2}\,w^{\top}\Sigma\,w\quad \mathrm{s.t.}\quad w^{\top}\mathbf{1}=1")
eq("w3", r"w=\frac{1}{\gamma}\,\Sigma^{-1}\left(\mu-\frac{\mathbf{1}^{\top}\Sigma^{-1}\mu-\gamma}{\mathbf{1}^{\top}\Sigma^{-1}\mathbf{1}}\,\mathbf{1}\right)", dark=True)
eq("ma", r"\max_{w}\ w^{\top}\mu\quad \mathrm{s.t.}\quad \mathrm{Prob}\,[\,r_p\leq H\,]\leq\alpha,\quad w^{\top}\mathbf{1}=1")
eq("ineq6", r"H\ \leq\ w^{\top}\mu+\Phi^{-1}(\alpha)\,\left(w^{\top}\Sigma\,w\right)^{1/2}")
eq("zform", r"m_p-z\,\sigma_p\ \geq\ H,\qquad z=-\Phi^{-1}(\alpha)", dark=True)
# 손계산 ① 60·30·10
eq("m60", r"m=0.6\,(5\%)+0.3\,(10\%)+0.1\,(25\%)=8.50\%")
eq("v60", r"\sigma^{2}=0.6^{2}(0.0025)+0.3^{2}(0.04)+0.1^{2}(0.25)+2(0.3)(0.1)(0.02)=0.0082")
eq("q60", r"8.50\%-1.645\times 9.06\%=-6.40\%\ \geq\ H=-10\%", dark=True)
eq("p60", r"\mathrm{Prob}\,[\,r<-10\%\,]=\Phi\left(\frac{-10\%-8.50\%}{9.06\%}\right)=\Phi(-2.04)=2.05\%")
# 손계산 ② 두 자산
eq("m2", r"m(w)=5\%+5\%\,w,\qquad \sigma(w)=\sqrt{(1-w)^{2}(0.05)^{2}+w^{2}(0.20)^{2}}")
eq("q2", r"(15\%+5\%\,w)^{2}=1.645^{2}\left[(1-w)^{2}(0.05)^{2}+w^{2}(0.20)^{2}\right]")
eq("poly2", r"-0.1125\,w^{2}+0.0285\,w+0.0157=0")
eq("root2", r"w^{*}=\frac{0.0285+\sqrt{0.0285^{2}+4\,(0.1125)(0.0157)}}{2\,(0.1125)}=52.2\%", dark=True)
# 행렬
eq("abcd", r"A=\mathbf{1}^{\top}\Sigma^{-1}\mu,\quad B=\mu^{\top}\Sigma^{-1}\mu,\quad C=\mathbf{1}^{\top}\Sigma^{-1}\mathbf{1},\quad D=BC-A^{2}")
eq("abcdn", r"A=22.917,\quad B=1.4167,\quad C=426.04,\quad D=78.385", dark=True)
eq("lag", r"L=w^{\top}\mu-\frac{\gamma}{2}\,w^{\top}\Sigma\,w+\lambda\,(1-w^{\top}\mathbf{1})")
eq("foc", r"\mu-\gamma\,\Sigma\,w-\lambda\mathbf{1}=0\ \ \Rightarrow\ \ w=\frac{1}{\gamma}\,\Sigma^{-1}(\mu-\lambda\mathbf{1}),\quad \lambda=\frac{A-\gamma}{C}")
eq("gv", r"w(\gamma)=g+\frac{1}{\gamma}\,v,\qquad g=\frac{\Sigma^{-1}\mathbf{1}}{C},\qquad v=\Sigma^{-1}\left(\mu-\frac{A}{C}\,\mathbf{1}\right)", dark=True)
eq("msig", r"m(\gamma)=\frac{A}{C}+\frac{K}{\gamma},\qquad \sigma^{2}(\gamma)=\frac{1}{C}+\frac{K}{\gamma^{2}},\qquad K=\frac{D}{C}")
eq("msign", r"\frac{A}{C}=5.38\%,\qquad \frac{1}{C}=0.002347\ \ (\sigma_{min}=4.84\%),\qquad K=0.18399", dark=True)
eq("eq7", r"\frac{A}{C}+\frac{K}{\gamma}+\Phi^{-1}(\alpha)\,\sqrt{\frac{1}{C}+\frac{K}{\gamma^{2}}}=H")
eq("xform", r"x=\frac{1}{\gamma}:\quad \left(\frac{A}{C}-H+K\,x\right)^{2}=z^{2}\left(\frac{1}{C}+K\,x^{2}\right)")
eq("xroot", r"-0.4639\,x^{2}+0.0566\,x+0.0173=0\ \ \Rightarrow\ \ x=0.2635,\ \ \gamma=3.795", dark=True)
eq("wret", r"w=g+0.2635\,v=(53.9\%,\ 26.6\%,\ 19.5\%)")
eq("chkret", r"m=10.23\%,\ \ \sigma=12.30\%,\ \ 10.23\%-1.645\times 12.30\%=-10.00\%", dark=True)
# 합산
eq("agg", r"\sum_{k}a_k\,w(\gamma_k)=g+v\,\sum_{k}\frac{a_k}{\gamma_k}\ =\ g+\frac{1}{\gamma_{tot}}\,v")
eq("gtot", r"\frac{1}{\gamma_{tot}}=\frac{0.6}{3.795}+\frac{0.2}{2.706}+\frac{0.2}{0.877}=0.4600\ \ \Rightarrow\ \ \gamma_{tot}=2.174", dark=True)
eq("sigtot", r"\sigma_{tot}=\sqrt{w_{tot}^{\top}\,\Sigma\,w_{tot}}=20.32\%")
# 가능성
eq("q10", r"Q_{max}=\max_{w^{\top}\mathbf{1}=1}\ \ w^{\top}\mu+\Phi^{-1}(\alpha)\,\sqrt{w^{\top}\Sigma\,w}")
eq("qclosed", r"Q_{max}=\frac{A}{C}-\sqrt{\frac{z^{2}-K}{C}}=5.38\%-7.69\%=-2.31\%", dark=True)
# 롱온리
eq("lo20", r"\max_{w}\ w^{\top}\mu\quad \mathrm{s.t.}\quad w^{\top}\mu+\Phi^{-1}(\alpha)\sqrt{w^{\top}\Sigma\,w}\geq H,\quad w^{\top}\mathbf{1}=1,\quad L\leq w\leq U")
eq("lo25", r"\mathrm{solve}_{\gamma}\ \ w(\gamma)^{\top}\mu+\Phi^{-1}(\alpha)\sqrt{w(\gamma)^{\top}\Sigma\,w(\gamma)}=H", dark=True)
# 롱온리 손풀이 (상속 계정, 채권 0에 묶고 두 자산으로)
eq("lo_m", r"m(w)=10\%+15\%\,w,\qquad \sigma^{2}(w)=0.04-0.04\,w+0.25\,w^{2}")
eq("lo_q", r"(25\%+15\%\,w)^{2}=0.8416^{2}\,(0.04-0.04\,w+0.25\,w^{2})")
eq("lo_poly", r"-0.1546\,w^{2}+0.1033\,w+0.0342=0")
eq("lo_root", r"w^{*}=\frac{0.1033+\sqrt{0.1033^{2}+4\,(0.1546)(0.0342)}}{2\,(0.1546)}=91.1\%", dark=True)
# 오지정
eq("loss", r"\Delta=\frac{K\,\gamma}{2}\left(\frac{1}{\gamma}-\frac{1}{\gamma\,'}\right)^{2},\qquad \gamma\,'=\gamma\,(1\pm e)")
# 공통 언어
eq("four", r"\gamma\ \Leftrightarrow\ \sigma_{max}\ \Leftrightarrow\ \mathrm{VaR}_{95}=-(m-1.645\,\sigma)\ \Leftrightarrow\ (H,\ \alpha)")
# 요약용 (흰 카드)
eq("s_ineq", r"m+\Phi^{-1}(\alpha)\,\sigma\geq H", white=True)
eq("s_gv", r"w=g+v/\gamma", white=True)
eq("s_gt", r"1/\gamma_{tot}=\sum_k a_k/\gamma_k", white=True)


# =============================================================== 차트
def chart(name, f):
    R["fig/" + name] = save(f, f"fig/{name}.png")


gg = np.geomspace(0.35, 200, 600)
fm = A / Cc + K / gg
fs_ = np.sqrt(1 / Cc + K / gg ** 2)
acc_col = [C["teal"], C["blue"], C["amber"]]

# (1) 표준정규 꼬리 — α별 z
xx = np.linspace(-3.4, 3.4, 600)
f, ax = fig("panel")
ax.plot(xx, norm.pdf(xx), color=C["body"], lw=2.2)
for (lab, H, a), col in zip(ACC, acc_col):
    q = norm.ppf(a)
    ax.axvline(q, color=col, lw=2.0, ls="--")
    ax.text(1.0, 0.40 - 0.05 * ACC.index((lab, H, a)), f"α {a*100:.0f}% → {q:.3f}", ha="left", fontsize=15, color=col)
ax.fill_between(xx, norm.pdf(xx), where=xx < norm.ppf(0.05), color=C["red"], alpha=0.35)
ax.set_xlim(-3.4, 3.4); ax.set_ylim(0, 0.45); ax.set_yticks([])
ax.set_xlabel(r"표준화 수익률  $(r-m)\,/\,\sigma$"); ax.set_ylabel("확률 밀도")
chart("c_ztail", f)

# (2) 60·30·10 분포
xr = np.linspace(-0.25, 0.40, 600)
f, ax = fig("panel")
pdf = norm.pdf(xr, m60, s60)
ax.plot(xr * 100, pdf, color=C["teal"])
ax.fill_between(xr * 100, pdf, where=xr < m60 - z5 * s60, color=C["teal"], alpha=0.25, label="하위 5% 꼬리")
ax.fill_between(xr * 100, pdf, where=xr < -0.10, color=C["red"], alpha=0.55, label="H 아래 2.05%")
ax.axvline(-10, color=C["red"], ls="--", lw=1.8); ax.axvline((m60 - z5 * s60) * 100, color=C["teal"], ls=":", lw=1.8)
ax.text(-11, pdf.max() * 0.72, "H\n−10%", ha="right", fontsize=15, color=C["red"])
ax.text(-6.4, pdf.max() * 1.03, "하위 5% −6.40%", ha="center", fontsize=15, color=C["teal"])
ax.set_ylim(0, pdf.max() * 1.15); ax.set_yticks([])
ax.set_xlabel("연 수익률 (%)"); ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86))
chart("c_check", f)

# (3) 두 자산: 하위 5% 경계 vs w
wv = np.linspace(0, 1, 300)
m_w = 0.05 + 0.05 * wv
s_w = np.sqrt((1 - wv) ** 2 * 0.0025 + wv ** 2 * 0.04)
q_w = m_w - z5 * s_w
f, ax = fig("panel")
ax.plot(wv * 100, q_w * 100, color=C["teal"], label="하위 5% 수익률")
ax.plot(wv * 100, m_w * 100, color=C["blue"], label="기대수익 m(w)")
ax.axhline(-10, color=C["red"], ls="--", lw=1.8)
ax.text(98, -8.8, "H = −10%", fontsize=15, color=C["red"], ha="right")
for wt, col, lab in [(0.5, C["body"], "0.5 통과"), (0.6, C["muted"], "0.6 위반")]:
    qv = 0.05 + 0.05 * wt - z5 * np.sqrt((1 - wt) ** 2 * 0.0025 + wt ** 2 * 0.04)
    ax.plot(wt * 100, qv * 100, "o", color=col)
    ax.annotate(lab, (wt * 100, qv * 100), textcoords="offset points", xytext=(10, 4) if wt == 0.6 else (-75, 10), fontsize=15, color=col)
qs = 0.05 + 0.05 * w2 - z5 * np.sqrt((1 - w2) ** 2 * 0.0025 + w2 ** 2 * 0.04)
ax.plot(w2 * 100, qs * 100, "o", color=C["red"], ms=10)
ax.annotate("w* = 52.2%", (w2 * 100, qs * 100), textcoords="offset points", xytext=(8, -34), fontsize=15, color=C["red"], fontweight="bold")
ax.set_xlabel("저위험 주식형 비중 w (%)"); ax.set_ylabel("연 수익률 (%)"); ax.set_ylim(-24, 14)
ax.legend(loc="lower left")
chart("c_two", f)

# (4) 효율선 위 γ 눈금
f, ax = fig("panel")
ax.plot(fs_ * 100, fm * 100, color=C["teal"])
for gm in (1, 2, 4, 8):
    m_, s_ = A / Cc + K / gm, np.sqrt(1 / Cc + K / gm ** 2)
    ax.plot(s_ * 100, m_ * 100, "o", color=C["body"])
    ax.annotate(f"γ = {gm}", (s_ * 100, m_ * 100), textcoords="offset points", xytext=(10, -14), fontsize=15)
ax.plot(np.sqrt(1 / Cc) * 100, A / Cc * 100, "s", color=C["red"], ms=9)
ax.annotate("최소분산 g (γ → ∞)", (np.sqrt(1 / Cc) * 100, A / Cc * 100), textcoords="offset points", xytext=(12, -22), fontsize=15, color=C["red"])
ax.set_xlim(0, 45); ax.set_ylim(3, 26)
ax.set_xlabel("표준편차 σ (%)"); ax.set_ylabel("기대수익률 m (%)")
chart("c_fgamma", f)

# (5) 효율선 + 은퇴 계정의 VaR 직선
f, ax = fig("panel")
ax.plot(fs_ * 100, fm * 100, color=C["teal"], label="효율선")
sl = np.linspace(0, 45, 100)
ax.plot(sl, (-0.10 + z5 * sl / 100) * 100, color=C["red"], ls="--", lw=2.0, label="m = H + 1.645σ (H = −10%)")
ax.fill_between(sl, (-0.10 + z5 * sl / 100) * 100, 40, color=C["red"], alpha=0.06)
m1, s1 = ms(WS[0])
ax.plot(s1 * 100, m1 * 100, "o", color=C["body"], ms=10)
ax.annotate("은퇴 계정 γ = 3.795\n(12.30%, 10.23%)", (s1 * 100, m1 * 100), textcoords="offset points", xytext=(30, -16), fontsize=15)
ax.text(1, 22, "직선 위쪽 = 조건 충족", fontsize=15, color=C["red"])
ax.set_xlim(0, 30); ax.set_ylim(0, 24)
ax.set_xlabel("표준편차 σ (%)"); ax.set_ylabel("기대수익률 m (%)"); ax.legend(loc="lower right")
chart("c_vline", f)

# (6) 비중 vs γ
gl = np.geomspace(0.5, 12, 400)
WW = np.array([w_of(x) for x in gl]) * 100
f, ax = fig("panel")
for j, (lab, col) in enumerate(zip(["채권형", "저위험 주식형", "고위험 주식형"], [C["teal"], C["blue"], C["amber"]])):
    ax.plot(gl, WW[:, j], color=col, label=lab)
ax.axhline(0, color=C["body"], lw=1.0)
for gm, (lab, _, _) in zip(GAM, ACC):
    ax.axvline(gm, color=C["muted"], ls=":", lw=1.6)
    ax.text(gm * (0.96 if lab == "교육" else 1.04), 128, f"{lab}\n{gm:.3f}", fontsize=15, color=C["body"], va="top", ha="right" if lab == "교육" else "left")
ax.set_xscale("log"); ax.set_xticks([0.5, 1, 2, 4, 8]); ax.set_xticklabels(["0.5", "1", "2", "4", "8"])
ax.set_ylim(-150, 135); ax.set_xlabel("위험회피도 γ (로그 눈금)"); ax.set_ylabel("비중 (%)")
ax.legend(loc="lower right")
chart("c_wgamma", f)

# (7) 효율선 + 세 계정 + 합산 (논문 그림 1 재현)
f, ax = fig("wide")
ax.plot(fs_ * 100, fm * 100, color=C["teal"], label="효율선 (공매도 허용)")
for (lab, H, a), x, col in zip(ACC, WS, acc_col):
    m_, s_ = ms(x)
    ax.plot(s_ * 100, m_ * 100, "D", color=col, ms=10, label=f"{lab} (H {H*100:.0f}%, α {a*100:.0f}%)")
mA, sA = ms(AGG)
ax.plot(sA * 100, mA * 100, "o", color=C["red"], ms=11, label="합산 60 · 20 · 20")
ax.annotate("합산 (20.32%, 13.84%)", (sA * 100, mA * 100), textcoords="offset points", xytext=(20, -44), fontsize=15, color=C["red"])
ax.set_xlim(0, 80); ax.set_ylim(0, 30)
ax.set_xlabel("표준편차 σ (%)"); ax.set_ylabel("기대수익률 m (%)"); ax.legend(loc="lower right", ncol=1)
chart("c_frontier3", f)

# (8) (H, α) → γ 지도
Hs = np.linspace(-0.20, 0.0, 121); As = np.linspace(0.02, 0.30, 113)
Gm = np.full((len(As), len(Hs)), np.nan)
for i, a in enumerate(As):
    zz_ = -norm.ppf(a)
    if zz_ ** 2 <= K:
        continue
    for j, H in enumerate(Hs):
        # x = 1/γ 의 2차식 (A/C − H + Kx)² = z²(1/C + Kx²) 의 큰 근 = 기대수익 최대 해
        c0 = A / Cc - H
        qa, qb, qc = K * K - zz_ ** 2 * K, 2 * c0 * K, c0 * c0 - zz_ ** 2 / Cc
        disc = qb * qb - 4 * qa * qc
        xstar = 1 / np.sqrt(Cc * (zz_ ** 2 - K))      # 하위 분위수 최대점
        if disc < 0 or c0 > 0 and False:
            continue
        roots = [(-qb + sg * np.sqrt(disc)) / (2 * qa) for sg in (1, -1)] if disc >= 0 else []
        roots = [r_ for r_ in roots if r_ >= xstar - 1e-12]
        if roots and (A / Cc + K * xstar - zz_ * np.sqrt(1 / Cc + K * xstar ** 2)) >= H:
            Gm[i, j] = 1 / max(roots)
f, ax = fig("panel")
lv = [0.5, 1, 2, 3, 4, 6, 10, 20, 40]
cs = ax.contourf(Hs * 100, As * 100, np.log(Gm), levels=np.log([0.3] + lv + [400]), cmap="YlGnBu")
cl = ax.contour(Hs * 100, As * 100, Gm, levels=lv, colors=C["body"], linewidths=0.8)
ax.clabel(cl, fmt=lambda x: f"{x:g}", fontsize=13)
for (lab, H, a), col in zip(ACC, acc_col):
    ax.plot(H * 100, a * 100, "D", color=C["red"], ms=9)
    ax.annotate(lab, (H * 100, a * 100), textcoords="offset points", xytext=(8, 6), fontsize=15, color=C["red"], fontweight="bold")
ax.set_xlabel("최소 수익률 H (%)"); ax.set_ylabel("미달 확률 한도 α (%)")
ax.text(-0.5, 2.6, "불가능", fontsize=15, color=C["body"], ha="right", bbox=dict(fc=C["paper"], ec="none", pad=1))
ax.grid(False)
chart("c_gmap", f)

# (9) 표 2 재현 — 같은 포트폴리오, 여러 (H, α)
Hl = np.linspace(-0.25, 0.25, 300)
f, ax = fig("panel")
for (lab, _, _), x, col in zip(ACC, WS, acc_col):
    m_, s_ = ms(x); ax.plot(Hl * 100, norm.cdf((Hl - m_) / s_) * 100, color=col, label=lab)
mA, sA = ms(AGG); ax.plot(Hl * 100, norm.cdf((Hl - mA) / sA) * 100, color=C["body"], ls="--", label="합산")
m1, s1 = ms(WS[0])
for H, txt_, off in [(-0.10, "(−10%, 5%)", (8, -18)), (0.0, "(0%, 20.3%)", (-120, 8))]:
    p = norm.cdf((H - m1) / s1) * 100
    ax.plot(H * 100, p, "o", color=C["red"], ms=9)
    ax.annotate(txt_, (H * 100, p), textcoords="offset points", xytext=off, fontsize=15, color=C["red"])
ax.set_xlabel("문턱 H (%)"); ax.set_ylabel("H에 못 미칠 확률 (%)"); ax.legend(loc="upper left")
chart("c_table2", f)

# (10) 합산 위험 막대
f, ax = fig("panel")
labs = ["은퇴", "교육", "상속", "가중평균", "공분산 반영"]
vals = [ms(x)[1] * 100 for x in WS] + [NUM["wavg_sd"] * 100, ms(AGG)[1] * 100]
cols = [C["hair"]] * 3 + [C["muted"], C["lime"]]
ax.barh(labs[::-1], vals[::-1], color=cols[::-1], edgecolor=[C["body"]] + ["none"] * 4)
for i, v_ in enumerate(vals[::-1]):
    ax.text(v_ + 0.8, i, f"{v_:.2f}%", va="center", fontsize=15, fontweight="bold" if i == 0 else "normal")
ax.set_xlim(0, 60); ax.set_xlabel("표준편차 (%)"); ax.grid(axis="y", visible=False)
chart("c_aggsd", f)

# (11) 하위 5% 분위수 Q 를 효율선 위에서
f, ax = fig("panel")
Qv = fm - z5 * fs_
ax.plot(fs_ * 100, Qv * 100, color=C["teal"], label="하위 5% 수익률 (효율선 위)")
i0 = np.argmax(Qv)
ax.plot(fs_[i0] * 100, Qv[i0] * 100, "o", color=C["red"], ms=10)
ax.annotate("Q_max = −2.31%\n(σ 5.02%, γ 32.8)", (fs_[i0] * 100, Qv[i0] * 100), textcoords="offset points", xytext=(6, -72), fontsize=15, color=C["red"])
ax.axhline(0, color=C["red"], ls="--", lw=1.8); ax.text(44, 1.2, "H = 0% (불가능)", ha="right", fontsize=15, color=C["red"])
ax.axhline(-10, color=C["body"], ls=":", lw=1.6); ax.text(44, -8.8, "H = −10% (가능)", ha="right", fontsize=15)
ax.set_xlim(0, 45); ax.set_ylim(-60, 8)
ax.set_xlabel("표준편차 σ (%)"); ax.set_ylabel("하위 5% 수익률 (%)"); ax.legend(loc="lower left")
chart("c_qmax", f)

# (12) 가능 영역 — α 별 최대 H
al = np.linspace(0.01, 0.40, 300)
zz = -norm.ppf(al)
Hmax = np.where(zz > np.sqrt(K), A / Cc - np.sqrt(np.maximum(zz ** 2 - K, 0) / Cc), np.nan)
f, ax = fig("panel")
ax.plot(al * 100, Hmax * 100, color=C["teal"], label="도달 가능한 최대 H")
ax.fill_between(al * 100, -20, Hmax * 100, color=C["teal"], alpha=0.10)
ar = NUM["roy"]["alpha_min"]
ap = dict(arrowstyle="->", color=C["body"], lw=1.4)
ax.plot(5, 0, "X", color=C["red"], ms=12)
ax.annotate("(0%, 5%) 불가능", (5, 0), xytext=(1, 8.5), fontsize=15, color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.4))
ax.plot(5, -3, "o", color=C["body"], ms=8)
ax.annotate("H를 −3%로 낮추기", (5, -3), xytext=(9, -8.5), fontsize=15, arrowprops=ap)
ax.plot(ar * 100, 0, "o", color=C["body"], ms=8)
ax.annotate(f"α를 {ar*100:.1f}%로 높이기", (ar * 100, 0), xytext=(17, 6.5), fontsize=15, arrowprops=ap)
for (lab, H, a), col in zip(ACC, acc_col):
    ax.plot(a * 100, H * 100, "D", color=col, ms=8)
ax.set_xlim(0, 40); ax.set_ylim(-20, 12)
ax.set_xlabel("미달 확률 한도 α (%)"); ax.set_ylabel("최소 수익률 H (%)"); ax.legend(loc="lower right")
chart("c_feas", f)

# (13) 롱온리 대 무제약 (논문 그림 6 재현)
sig_lo = np.linspace(0.0485, 0.5, 120)
m_lo_f = np.array([lo_frontier_m(s_) if s_ <= 0.5 else np.nan for s_ in sig_lo])
mask = np.diff(np.r_[0, m_lo_f]) > -1e-6
f, ax = fig("wide")
ax.plot(fs_ * 100, fm * 100, color=C["teal"], label="효율선 · 공매도 허용")
ax.plot(sig_lo * 100, m_lo_f * 100, color=C["amber"], lw=3.2, label="효율선 · 롱온리")
for (lab, _, _), x in zip(ACC, LO):
    m_, s_ = ms(x); ax.plot(s_ * 100, m_ * 100, "s", color=C["body"], ms=9)
    ax.annotate(f"{lab} {m_*100:.2f}%", (s_ * 100, m_ * 100), textcoords="offset points", xytext=(-10, 14) if lab == "교육" else (10, -22), fontsize=15)
mB, sB = ms(WS[2]); ax.plot(sB * 100, mB * 100, "D", color=C["muted"], ms=9)
ax.annotate("상속 무제약 26.35%", (sB * 100, mB * 100), textcoords="offset points", xytext=(-190, 4), fontsize=15, color=C["muted"])
ax.plot(s_lo * 100, m_lo * 100, "o", color=C["red"], ms=10, label="계정별 롱온리 합산")
ax.annotate(f"합산 {m_lo*100:.2f}% · 효율선 {FRONT_LO*100:.2f}%", (s_lo * 100, m_lo * 100), textcoords="data", xytext=(1.5, 21), fontsize=15, color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.4))
ax.set_xlim(0, 55); ax.set_ylim(0, 30)
ax.set_xlabel("표준편차 σ (%)"); ax.set_ylabel("기대수익률 m (%)"); ax.legend(loc="lower right")
chart("c_longonly", f)

# (14) 위험회피도 오지정 손실 (표 3)
paper3 = {3.7950: [2.50, 10.94, 28.72], 2.7063: [3.50, 15.34, 40.27], 0.8773: [5.29, 23.15, 44.22]}
f, ax = fig("panel")
xs = np.arange(3); wd = 0.26
for k, (gm, col) in enumerate(zip(paper3, acc_col)):
    rc = [misspec(gm, e) for e in (0.1, 0.2, 0.3)]
    ax.bar(xs + (k - 1) * wd, rc, wd * 0.92, color=col, label=f"γ {gm:.3f}")
    for j, (r_, p_) in enumerate(zip(rc, paper3[gm])):
        if abs(r_ - p_) > 0.05:
            ax.plot(xs[j] + (k - 1) * wd, p_, "_", color=C["red"], ms=22, mew=3)
    ax.text(xs[2] + (k - 1) * wd, rc[2] + 2, f"{rc[2]:.0f}", ha="center", fontsize=15)
ax.plot([], [], "_", color=C["red"], ms=18, mew=3, label="논문 표 3 (γ 0.877)")
ax.axhline(12.4, color=C["red"], ls="--", lw=1.6); ax.text(-0.42, 16, "롱온리 손실 12bp", fontsize=15, color=C["red"])
ax.set_xticks(xs); ax.set_xticklabels(["γ ±10%", "γ ±20%", "γ ±30%"])
ax.set_ylabel("손실 (bp, 연)"); ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88)); ax.grid(axis="x", visible=False)
ax.set_ylim(0, 140)
chart("c_misspec", f)

# (15) 심리계정 효율선: 기대수익 vs α (H 고정)
f, ax = fig("panel")
alg = np.linspace(0.01, 0.35, 200)
for H, col in [(-0.05, C["blue"]), (-0.10, C["teal"]), (-0.15, C["amber"]), (0.0, C["muted"])]:
    mm = []
    for a in alg:
        try:
            mm.append(ms(w_of(gamma_of(H, a)))[0] * 100)
        except Exception:
            mm.append(np.nan)
    ax.plot(alg * 100, mm, color=col, label=f"H = {H*100:.0f}%")
for (lab, H, a), x in zip(ACC, WS):
    ax.plot(a * 100, ms(x)[0] * 100, "D", color=C["red"], ms=9)
    ax.annotate(lab, (a * 100, ms(x)[0] * 100), textcoords="offset points", xytext=(-14, 10), fontsize=15, color=C["red"])
ax.set_ylim(4, 40); ax.set_xlabel("미달 확률 한도 α (%)"); ax.set_ylabel("기대수익률 (%)"); ax.legend(loc="upper left")
chart("c_mafront", f)

# (16) γ 에 따른 미달 확률 (논문 그림 3)
f, ax = fig("panel")
gl2 = np.linspace(0.5, 30, 400)
for H, col in [(-0.05, C["blue"]), (0.0, C["teal"]), (0.05, C["amber"]), (0.10, C["red"])]:
    pr = [norm.cdf((H - ms(w_of(x))[0]) / ms(w_of(x))[1]) * 100 for x in gl2]
    ax.plot(gl2, pr, color=col, label=f"H = {H*100:+.0f}%")
ax.set_xlabel("위험회피도 γ"); ax.set_ylabel("H에 못 미칠 확률 (%)"); ax.legend(loc="center right")
ax.set_ylim(0, 90)
chart("c_fig3", f)


# (17) 롱온리 손풀이 — 채권 0, 고위험 비중 w 하나
wv2 = np.linspace(0, 1, 300)
zb = -norm.ppf(0.20)
m2_ = 0.10 + 0.15 * wv2; s2_ = np.sqrt(0.04 - 0.04 * wv2 + 0.25 * wv2 ** 2); q2_ = m2_ - zb * s2_
f, ax = fig("panel")
ax.plot(wv2 * 100, q2_ * 100, color=C["teal"], label="하위 20% 수익률")
ax.plot(wv2 * 100, m2_ * 100, color=C["blue"], label="기대수익 m(w)")
ax.axhline(-15, color=C["red"], ls="--", lw=1.8); ax.text(2, -19.8, "H = −15%", fontsize=15, color=C["red"])
for wt, lab, off in [(0.9, "0.9 통과", (-90, 14)), (1.0, "1.0 위반", (-62, -26))]:
    qv = 0.10 + 0.15 * wt - zb * np.sqrt(0.04 - 0.04 * wt + 0.25 * wt ** 2)
    ax.plot(wt * 100, qv * 100, "o", color=C["body"]); ax.annotate(lab, (wt * 100, qv * 100), textcoords="offset points", xytext=off, fontsize=15)
wst = 0.911072
ax.plot(wst * 100, -15, "o", color=C["red"], ms=10)
ax.annotate("w* = 91.1%", (wst * 100, -15), textcoords="offset points", xytext=(-190, -26), fontsize=15, color=C["red"], fontweight="bold")
ax.set_xlabel("고위험 주식형 비중 w (%) · 나머지는 저위험"); ax.set_ylabel("연 수익률 (%)"); ax.set_ylim(-22, 30)
ax.legend(loc="upper left")
chart("c_lohand", f)

# =============================================================== SVG
FONT = "Pretendard"


def svg_save(name, body, W, H):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
         f'<defs><marker id="ar" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">'
         f'<path d="M0,0 L12,6 L0,12 z" fill="#0B6B68"/></marker></defs>'
         f'<rect width="{W}" height="{H}" fill="#F7F5F0"/>{body}</svg>')
    open(f"svg/{name}.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"fig/{name}.png", output_width=W, output_height=H)
    R["fig/" + name] = W / H
    print(f"  o svg {name} {W}x{H}")


def T(x, y, t, size=30, w="400", col="#102027", anchor="middle", italic=False):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}"{st}>{t}</text>')


def box(x, y, w, h, kind="white"):
    fill, stroke = {"white": ("#FFFFFF", "#DDE3E2"), "lime": ("#B7F34A", "#B7F34A"),
                    "dark": ("#071A1D", "#071A1D"), "ghost": ("#F7F5F0", "#DDE3E2")}[kind]
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0B6B68" stroke-width="4" marker-end="url(#ar)"/>'


def bracket(x, y, h, left=True):
    d = 14 if left else -14
    return (f'<path d="M{x+d},{y} L{x},{y} L{x},{y+h} L{x+d},{y+h}" fill="none" stroke="#102027" stroke-width="3"/>')


def matrix(x, y, rows, cw, rh, size=32, name=None):
    b = ""
    n, m = len(rows), len(rows[0])
    H = n * rh + 16
    b += bracket(x, y, H) + bracket(x + m * cw + 20, y, H, left=False)
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            b += T(x + 10 + j * cw + cw / 2, y + 8 + i * rh + rh * 0.68, c, size)
    return b, x + m * cw + 20


# (S1) 계정으로 생각한다 — MVT 한 질문 vs 심리계정 세 질문 (1600×560)
W, H = 1600, 560
b = box(30, 40, 520, 480, "white")
b += T(290, 100, "평균-분산 이론 (MVT)", 34, "700", "#64757D")
b += T(290, 190, "전체 포트폴리오 하나", 32)
b += T(290, 290, "질문: 당신의 위험회피도", 30)
b += T(290, 345, "γ는 얼마입니까?", 30)
b += T(290, 450, "답하기 어렵다", 32, "700", "#C00000")
b += arrow(570, 280, 640, 280)
b += box(660, 40, 910, 480, "ghost")
b += T(1115, 100, "심리계정 (Shefrin–Statman BPT)", 34, "700", "#0B6B68")
for i, (lab, H_, a_, kind) in enumerate([("은퇴", "−10%", "5%", "dark"), ("교육", "−5%", "15%", "white"), ("상속", "−15%", "20%", "white")]):
    x = 690 + i * 295
    b += box(x, 140, 260, 340, kind)
    tc = "#B7F34A" if kind == "dark" else "#102027"
    bc = "#FFFFFF" if kind == "dark" else "#102027"
    b += T(x + 130, 200, lab, 36, "700", tc)
    b += T(x + 130, 285, f"최소 수익률 {H_}", 30, "400", bc)
    b += T(x + 130, 345, f"미달 확률 ≤ {a_}", 30, "400", bc)
    b += T(x + 130, 430, "답하기 쉽다", 30, "700", "#B7F34A" if kind == "dark" else "#0B6B68")
svg_save("s_accounts", b, W, H)

# (S2) 논문의 결과 셋 (1600×560)
W, H = 1600, 560
items = [("① 문제 동치", ["(H, α) 제약 최대화 =", "평균-분산 + 내재 γ", "= VaR 제약 = Telser형"], "white"),
         ("② 합쳐도 효율", ["계정 해가 모두 효율선 위", "공매도 허용이면", "합산도 효율선 위"], "white"),
         ("③ 마찰은 작다", ["공매도 금지 손실 수 bp", "γ 오지정 손실보다 작다", "샤프비율 손실 < 6%"], "lime")]
b = ""
for i, (t, ls, k) in enumerate(items):
    x = 30 + i * 530
    b += box(x, 40, 480, 480, k)
    b += T(x + 240, 120, t, 40, "700", "#0B6B68" if k != "lime" else "#071A1D")
    for j, l in enumerate(ls):
        b += T(x + 240, 240 + j * 80, l, 32)
    if i < 2:
        b += arrow(x + 488, 280, x + 522, 280)
svg_save("s_claims", b, W, H)

# (S3) 자산 셋 — μ 와 Σ (1600×560)
W, H = 1600, 560
b = T(60, 60, "기대수익률 μ", 32, "700", "#64757D", "start")
mb, xe = matrix(60, 90, [["0.05"], ["0.10"], ["0.25"]], 150, 100)
b += mb
b += T(420, 60, "공분산 Σ", 32, "700", "#64757D", "start")
mb, xe2 = matrix(420, 90, [["0.0025", "0", "0"], ["0", "0.0400", "0.0200"], ["0", "0.0200", "0.2500"]], 170, 100)
b += mb
rows = [("채권형", "5% · 5%"), ("저위험 주식형", "10% · 20%"), ("고위험 주식형", "25% · 50%")]
b += T(1000, 60, "자산 (평균 · 표준편차)", 32, "700", "#64757D", "start")
for i, (n_, ms_) in enumerate(rows):
    y = 90 + i * 112
    b += box(1000, y, 570, 96, "white" if i else "ghost")
    b += T(1030, y + 60, n_, 32, "700", "#102027", "start") + T(1545, y + 60, ms_, 32, "400", "#102027", "end")
b += T(800, 500, "두 주식형의 상관 0.02 ÷ (0.20 × 0.50) = 0.20 · 채권은 두 주식과 무상관 · 무위험 자산 없음", 30, "400", "#0B6B68")
svg_save("s_data", b, W, H)

# (S4) Σ⁻¹ 과 중간값 — 한 줄 와이드 (1600×330)
W, H = 1600, 330
b = T(40, 40, "Σ⁻¹", 32, "700", "#64757D", "start")
mb, _ = matrix(40, 60, [["400", "0", "0"], ["0", "26.042", "−2.083"], ["0", "−2.083", "4.167"]], 150, 82, 32)
b += mb
b += T(560, 40, "Σ⁻¹μ", 32, "700", "#64757D", "start")
mb, _ = matrix(560, 60, [["20.000"], ["2.083"], ["0.833"]], 150, 82, 32)
b += mb
b += T(790, 40, "Σ⁻¹1", 32, "700", "#64757D", "start")
mb, _ = matrix(790, 60, [["400.000"], ["23.958"], ["2.083"]], 170, 82, 32)
b += mb
b += box(1040, 60, 530, 262, "dark")
b += T(1305, 112, "성분을 더하면", 32, "700", "#B7F34A")
b += T(1305, 172, "A = 20 + 2.083 + 0.833 = 22.917", 30, "700", "#FFFFFF")
b += T(1305, 232, "C = 400 + 23.958 + 2.083 = 426.04", 30, "700", "#FFFFFF")
b += T(1305, 292, "B = μ · Σ⁻¹μ = 1.4167", 30, "700", "#FFFFFF")
svg_save("s_inv", b, W, H)

# (S5) 롱온리 γ 탐색 루프 — 가로 한 줄 (1600×190)
W, H = 1600, 190
b = ""
steps = [("① γ를 정한다", "white"), ("② QP · 식 (26)–(29)", "white"), ("③ 분위수 = H? · 식 (25)", "white"), ("④ 내재 γ · 롱온리 비중", "lime")]
for i, (t, k) in enumerate(steps):
    x = 10 + i * 400
    b += box(x, 10, 350, 110, k) + T(x + 175, 78, t, 32, "700", "#071A1D" if k == "lime" else "#102027")
    if i < 3:
        b += arrow(x + 354, 65, x + 396, 65)
b += '<path d="M985,124 C985,182 185,182 185,130" fill="none" stroke="#0B6B68" stroke-width="4" stroke-dasharray="10 8" marker-end="url(#ar)"/>'
svg_save("s_qp", b, W, H)

# (S6) 계보 — Roy → Kataoka / Telser (1600×600)
W, H = 1600, 600
b = box(560, 30, 480, 120, "dark") + T(800, 82, "Roy (1952) 안전우선", 36, "700", "#B7F34A") + T(800, 132, "미달 확률을 가장 작게", 32, "400", "#FFFFFF")
b += arrow(700, 155, 380, 230) + arrow(900, 155, 1220, 230)
b += box(60, 240, 640, 220, "white")
b += T(380, 300, "Kataoka (1963)형 — M8 방법 1", 36, "700", "#64757D")
b += T(380, 365, "미달 확률 고정 → 하위 경계 최대", 34)
b += T(380, 420, "목표 G · 시점 T · 확률 p → K", 34)
b += box(900, 240, 640, 220, "lime")
b += T(1220, 300, "Telser (1956)형 — M8 방법 2", 36, "700", "#071A1D")
b += T(1220, 365, "미달 확률 한도 → 기대수익 최대", 34, "400", "#071A1D")
b += T(1220, 420, "Das–Markowitz: (H, α) → γ", 34, "700", "#071A1D")
b += T(800, 545, "둘 다 정규분포 아래 ‘평균 − z × 변동성’ 조건 하나로 바뀐다", 36, "700", "#0B6B68")
svg_save("s_lineage", b, W, H)

# (S7) 한 장 요약 흐름 (1600×520)
W, H = 1600, 520
steps = [("① 목표 언어", "계정마다 (H, α)", "white"), ("② 분위수 조건", "m − zσ ≥ H", "white"),
         ("③ 내재 γ", "식 (7) 풀기", "white"), ("④ 계정 비중", "g + v / γ", "white"), ("⑤ 합산", "1/γ 가중평균", "lime")]
b = ""
for i, (t1, t2, k) in enumerate(steps):
    x = 5 + i * 322
    b += box(x, 20, 290, 220, k)
    b += T(x + 145, 105, t1, 36, "700", "#0B6B68" if k != "lime" else "#071A1D")
    b += T(x + 145, 180, t2, 34, "700")
    if i < 4:
        b += arrow(x + 293, 130, x + 319, 130)
chk = [("가능성 점검", "α 5%면 H ≤ −2.31%"), ("롱온리 (계정별)", "연 12bp 손실"), ("γ 오지정 ±20%", "연 11 ~ 47bp 손실")]
for i, (t1, t2) in enumerate(chk):
    x = 5 + i * 535
    b += box(x, 285, 520, 220, "dark" if i == 0 else "ghost")
    b += T(x + 260, 370, t1, 36, "700", "#B7F34A" if i == 0 else "#64757D")
    b += T(x + 260, 445, t2, 36, "700", "#FFFFFF" if i == 0 else "#102027")
svg_save("s_summary", b, W, H)

# (S8) 롱온리를 엑셀 해 찾기 · scipy로 — M8 강의본과 같은 그림(_build/w06_m8_rework/solver_fig.py)
import sys as _sys
_sys.path.insert(0, os.path.join(HERE, "..", "w06_m8_rework"))
from solver_fig import solver_svg, png as _svgpng
_s, _W, _H = solver_svg("#F7F5F0")
open("svg/s_solver.svg", "w").write(_s)
_svgpng(_s, "fig/s_solver.png", _W, _H)
R["fig/s_solver"] = _W / _H
print(f"  o svg s_solver {_W}x{_H}")

json.dump(R, open("ratios.json", "w"), indent=1, ensure_ascii=False)
print(f"ratios → ratios.json ({len(R)})")
