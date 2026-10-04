#!/usr/bin/env python3
"""GBI 요약·기초 덱 — 수식 PNG · matplotlib 차트 · SVG 도해를 만든다.
실행: <python> assets.py   (작업 폴더 기준 상대경로: eq/ fig/ svg/)
숫자 출처: W06 M8 강의본 · 케이스 모범답안 · w8_sim_results.json · 도출 III(02_..._III.md)
"""
import os, json
from math import exp, log, sqrt
from statistics import NormalDist
import numpy as np
import cairosvg
from render_eq import render, INK, PAPER, LIME, DARK, WHITE
from zo_mpl import fig, save, C

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs("fig", exist_ok=True); os.makedirs("svg", exist_ok=True)
Z = NormalDist()
R = {}   # 이름 → ratio (build.js가 읽는다)

def eq(name, tex, fs=30, dark=False, white=False):
    bg = DARK if dark else (WHITE if white else PAPER)
    col = LIME if dark else INK
    _, r = render(tex, name + ".png", fontsize=fs, color=col, bg=bg)
    R["eq/" + name] = r

def chart(name, f):
    R["fig/" + name] = save(f, f"fig/{name}.png")

# ---------------------------------------------------------------- 수식
eq("risk1", r"\mathrm{Risk}=P\,(W_T<G)")
eq("es", r"\mathrm{ES}=\mathbb{E}\,[\,G-W_T\ |\ W_T<G\,]", dark=True)
eq("bpt", r"\max\ \sum_k U_k\quad \mathrm{s.t.}\quad P\,(W_k<G_k)\leq \alpha_k")
eq("K", r"K=G\cdot e^{-mT}\cdot e^{+z_p\,\sigma\sqrt{T}}", fs=34)
eq("gp", r"\ln K=\ln G-T\,g_p,\qquad g_p=m-z_p\,\frac{\sigma}{\sqrt{T}}")
eq("wstar", r"w^{*}=\frac{\lambda}{\sigma^{2}}-\frac{z_p}{\sigma\sqrt{T}},\qquad 0\leq w^{*}\leq 1", dark=True)
eq("floorRB", r"F=c\cdot\frac{1-(1+r)^{-T}}{r}=c\cdot\beta")
eq("rb45", r"P_{45}=\frac{P_{65}}{1.02^{20}}=\frac{3.92}{1.486}\approx 2.64", dark=True)
eq("atilde", r"\tilde{A}=\frac{A}{P(G)},\qquad P(G)=G\cdot B(t,T)")
eq("dA", r"\frac{\Delta\tilde{A}}{\tilde{A}}\approx w_{PSP}\,(R_{PSP}-R_{GHP})")
eq("cppi", r"E=m\,(A-F),\qquad w_{PSP}=\frac{m\,(A-F)}{A}")
eq("cppicond", r"m\,(A-F)\,x\leq A-F\quad\Leftrightarrow\quad x\leq\frac{1}{m}", dark=True)
eq("mrule", r"m=\min\left\{\frac{1}{L},\ \frac{\mu-r}{\gamma\,\sigma^{2}}\right\}", fs=34)
eq("flexi", r"F_t=0.8\,A_t,\qquad m_t=\frac{w_t^{TDF}}{1-0.8}")
eq("dm", r"P\,(R_p<H)\leq\alpha\quad\Leftrightarrow\quad m_p+\Phi^{-1}(\alpha)\,\sigma_p\geq H")
eq("gtot", r"\frac{1}{\gamma_{total}}=\sum_k\frac{a_k}{\gamma_k}", dark=True)
eq("digital", r"X_T^{*}=k_{asp}\,G\cdot\mathbf{1}\{\xi_T\leq\bar{\xi}\}")
eq("browne", r"P^{*}=\Phi\left(\Phi^{-1}(\tilde{A}_0)+\lambda\sqrt{T}\right)", dark=True)
eq("ess", r"F=k_{ess}\cdot P(G)=0.6\times 6756=4053")
eq("cppiA", r"w_{PSP}=\frac{m\,(\tilde{A}-k_{ess})}{\tilde{A}}", dark=True)
eq("beta", r"\beta_t=\sum_{s=T_R}^{T_R+n-1}B(t,s),\qquad F^{(i)}=\frac{A}{c\,\beta}=\frac{A/\beta}{c}")
eq("seq", r"A_{t+1}=A_t\,(1+R_{t+1})-C_{t+1}")
eq("amort", r"C_t=\frac{A_t}{\beta_t},\qquad C_t=c_{ess}+\frac{A_t^{flex}}{\beta_t}", dark=True)
eq("mort", r"\frac{1+r}{1-q}\approx 1+r+q")
eq("ltc", r"p\cdot X\cdot(1+\theta)=0.08\times 3\times 1.3\approx 0.31")
eq("case1", r"w_t=\min\left\{1,\ \frac{m\,(W_t-F_t)}{W_t}\right\}")
eq("case2", r"S_t=0.8\,S_{t-1}(1+\pi)+0.2\,z\,W_{t-1}")
# 한 장 요약용 (흰 카드)
eq("s_K", r"K=G\,e^{-mT+z_p\sigma\sqrt{T}}", white=True)
eq("s_cppi", r"w_{PSP}=\frac{m\,(A-F)}{A}", white=True)
eq("s_inc", r"F^{(i)}=A\,/\,(c\,\beta)", white=True)

# ---------------------------------------------------------------- 차트
# (1) 위험 = 미달 확률: 3억 목표, 균형형에 2.22억, 10년
K0, G0, m0, s0, T0 = 2.22, 3.0, 0.045, 0.09, 10
mu, sd = log(K0) + m0 * T0, s0 * sqrt(T0)
x = np.linspace(1.2, 7.0, 600)
pdf = np.exp(-(np.log(x) - mu) ** 2 / (2 * sd * sd)) / (x * sd * sqrt(2 * np.pi))
pmiss = Z.cdf((log(G0) - mu) / sd)
f, ax = fig("panel")
ax.plot(x, pdf, color=C["teal"])
ax.fill_between(x, pdf, where=x < G0, color=C["red"], alpha=0.30, label=f"미달 확률 {pmiss*100:.0f}%")
ax.axvline(G0, color=C["body"], ls="--", lw=1.6)
ax.set_ylim(0, pdf.max() * 1.22); ax.text(G0 + 0.08, pdf.max() * 1.10, "목표 G = 3억", fontsize=15, color=C["body"])
ax.text(4.6, pdf.max() * 0.55, "중앙값 3.48억", fontsize=15, color=C["teal"])
ax.set_xlabel("10년 뒤 자산 (억)"); ax.set_yticks([]); ax.set_ylabel("확률 밀도")
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.82))
chart("c_risk", f)

# (2) 아홉 칸 필요 자본
P = {"GHP": (0.02, 0.0), "균형형": (0.045, 0.09), "주식": (0.06, 0.20)}
Gs = [("Safety 6억 · 95%", 6, 0.95), ("Market 3억 · 70%", 3, 0.70), ("Aspirational 5억 · 30%", 5, 0.30)]
f, ax = fig("wide")
cols = [C["hair"], C["muted"], C["body"]]
for gi, (lab, G, p) in enumerate(Gs):
    z = Z.inv_cdf(p)
    ks = [G * exp(-m * 10 + z * s * sqrt(10)) for (m, s) in P.values()]
    best = int(np.argmin(ks))
    for j, k in enumerate(ks):
        xx = gi * 4 + j
        ax.bar(xx, k, color=C["lime"] if j == best else cols[j], edgecolor=C["body"] if j == best else "none",
               label=list(P)[j] if gi == 0 else None, width=0.86)
        ax.text(xx, k + 0.18, f"{k:.2f}", ha="center", fontsize=15, fontweight="bold" if j == best else "normal")
ax.set_xticks([1, 5, 9]); ax.set_xticklabels([g[0] for g in Gs], fontsize=15)
ax.set_ylabel("필요 자본 K (억)"); ax.set_ylim(0, 10.6); ax.grid(axis="x", visible=False)
ax.legend(loc="upper right", ncol=3, title="라임 = 그 목표에서 가장 싼 포트폴리오", title_fontsize=14)
chart("c_nine", f)

# (3) 최적 주식 비중 vs 달성 확률
ps = np.linspace(0.05, 0.99, 300)
w = np.clip(1.5 - np.array([Z.inv_cdf(p) for p in ps]) / (0.2 * sqrt(10)), 0, 1) * 100
f, ax = fig("panel")
ax.plot(ps * 100, w, color=C["teal"])
for p, lab in [(0.30, "30% → 100%"), (0.70, "70% → 67%"), (0.95, "95% → 0%")]:
    wv = min(1, max(0, 1.5 - Z.inv_cdf(p) / 0.632)) * 100
    ax.plot(p * 100, wv, "o", color=C["red"] if p == 0.95 else C["body"])
    ax.annotate(lab, (p * 100, wv), textcoords="offset points", xytext=(-40 if p > 0.9 else 6, 10), fontsize=15)
ax.set_xlabel("목표 달성 확률 p (%)"); ax.set_ylabel(r"주식 비중 $w^{*}$ (%)"); ax.set_ylim(-5, 118)
chart("c_wstar", f)

# (4) Floor vs 실질금리
rr = np.linspace(0.005, 0.04, 200)
Fl = 0.24 * (1 - (1 + rr) ** -25) / rr
f, ax = fig("panel")
ax.plot(rr * 100, Fl, color=C["teal"])
for r_, c_ in [(0.015, C["body"]), (0.025, C["teal"]), (0.035, C["red"])]:
    v = 0.24 * (1 - (1 + r_) ** -25) / r_
    ax.plot(r_ * 100, v, "o", color=c_)
    ax.annotate(f"{r_*100:.1f}% → {v:.2f}억" + (" (낙관)" if r_ == 0.035 else ""), (r_ * 100, v),
                textcoords="offset points", xytext=(8, 6), fontsize=15, color=c_)
ax.set_xlabel("실질금리 r (%)"); ax.set_ylabel("Floor F (억)"); ax.set_xlim(0.3, 5.6)
chart("c_floor", f)

# (5) 목표의 자: 현금 vs GHP의 확보율
rates = [0.03, 0.04, 0.05]
cash = [5000 / (1e4 / (1 + r) ** 10) * 100 for r in rates]
f, ax = fig("panel")
xx = np.arange(3)
b1 = ax.bar(xx - 0.2, cash, 0.38, color=C["muted"], label="현금 5,000만")
b2 = ax.bar(xx + 0.2, [74] * 3, 0.38, color=C["lime"], edgecolor=C["body"], label="GHP 0.74좌")
for i in range(3):
    ax.text(i - 0.2, cash[i] + 1.5, f"{cash[i]:.0f}%", ha="center", fontsize=15)
    ax.text(i + 0.2, 75.5, "74%", ha="center", fontsize=15, fontweight="bold")
ax.set_xticks(xx); ax.set_xticklabels(["금리 3%로 하락", "4% (출발)", "5%로 상승"])
ax.set_ylabel(r"목표 확보율 $\tilde{A}$ (%)"); ax.set_ylim(0, 114); ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", ncol=2)
chart("c_numeraire", f)

# (6) CPPI 비중 곡선
A = np.linspace(4.0, 12.0, 400)
f, ax = fig("panel")
for m_, c_, ls in [(4, C["teal"], "-"), (2, C["amber"], "--")]:
    ax.plot(A, np.clip(m_ * (A - 5) / A, 0, 1) * 100, color=c_, ls=ls, label=f"m = {m_}")
ax.axvline(5, color=C["red"], ls=":", lw=1.6); ax.text(5.1, 108, "Floor 5억", color=C["red"], fontsize=15)
for a_, lab in [(10, "10억 → 100%"), (6, "6억 → 67%"), (5, "5억 → 0%")]:
    v = min(1, max(0, 4 * (a_ - 5) / a_)) * 100
    ax.plot(a_, v, "o", color=C["body"]); ax.annotate(lab, (a_, v), textcoords="offset points", xytext=(8, -16), fontsize=15)
ax.set_xlabel("자산 A (억)"); ax.set_ylabel("위험자산 비중 (%)"); ax.set_ylim(-5, 118)
ax.legend(loc="center right")
chart("c_cppi", f)

# (7) 승수 민감도 (실습 Step 5)
sim = json.load(open(os.path.join(HERE, "data", "w8_sim_results.json")))
ms = [1, 2, 3, 4, 5, 6]
med = [sim["cppi"][str(k)]["median"] for k in ms]
w10 = [sim["cppi"][str(k)]["worst10"] for k in ms]
trap = [sim["cppi"][str(k)]["trap"] * 100 for k in ms]
br = [sim["cppi"][str(k)]["breach"] * 100 for k in ms]
f, (a1, a2) = fig("wide", 1, 2)
a1.plot(ms, med, "o-", color=C["teal"], label="중위 자산")
a1.plot(ms, w10, "o-", color=C["red"], label="최악 10% 평균")
a1.axhline(sim["FT"], color=C["amber"], ls="--", lw=1.6, label="75세 Floor 2.13억")
a1.set_xlabel("승수 m"); a1.set_ylabel("75세 자산 (억)"); a1.set_ylim(0, 13.5); a1.legend(loc="upper left", fontsize=14)
a2.bar(np.array(ms) - 0.2, trap, 0.4, color=C["red"], label="Cash Trap")
a2.bar(np.array(ms) + 0.2, br, 0.4, color=C["muted"], label="Floor 위반")
for k, t in zip(ms, trap):
    a2.text(k - 0.2, t + 0.6, f"{t:.1f}", ha="center", fontsize=14)
a2.set_xlabel("승수 m"); a2.set_ylabel("확률 (%)"); a2.set_ylim(0, 25); a2.legend(loc="upper left", fontsize=14)
a2.grid(axis="x", visible=False)
chart("c_msens", f)

# (8) 디지털 해: 상태별 ξ
f, ax = fig("panel")
st = ["대호황", "호황", "부진", "폭락"]; xi = [0.6, 0.8, 1.0, 1.4]
ax.bar(st, xi, color=[C["lime"], C["lime"], C["hair"], C["hair"]], edgecolor=C["body"], width=0.62)
ax.axhline(0.8, color=C["red"], ls="--", lw=1.6, label=r"문턱 $\bar{\xi}=0.8$")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88), fontsize=15)
for i, (v, q) in enumerate(zip(xi, [15, 20, 25, 35])):
    ax.text(i, v + 0.04, f"쿠폰 {q}", ha="center", fontsize=15)
ax.set_ylabel(r"확률 대비 값 $\xi=q/p$"); ax.set_ylim(0, 1.65); ax.grid(axis="x", visible=False)
ax.text(-0.3, 1.52, "라임 두 장 = 비용 35 → 달성 확률 50%", fontsize=15, color=C["body"])
chart("c_digital", f)

# (9) 필수+희망: 승수별 확률 (도출 III 5-7)
mm = [1, 2, 3, 4, 5]; pa = [0.4, 8.6, 13.7, 14.0, 12.2]; p1 = [3.6, 17.4, 20.9, 19.4, 16.1]
f, ax = fig("panel")
ax.bar(np.array(mm) - 0.2, pa, 0.4, color=C["teal"], label="희망 목표 1.2억 달성")
ax.bar(np.array(mm) + 0.2, p1, 0.4, color=C["blue"], label="1억 이상")
for k, v in zip(mm, pa):
    ax.text(k - 0.2, v + 0.6, f"{v:.1f}", ha="center", fontsize=14)
ax.set_xlabel("승수 m (필수 6,000만은 모두 확보)"); ax.set_ylabel("확률 (%)"); ax.set_ylim(0, 30)
ax.legend(loc="upper left", fontsize=14); ax.grid(axis="x", visible=False)
ax.text(3.1, 26.5, "바닥 없는 극대화: 82%", fontsize=15, color=C["red"])
chart("c_essasp", f)

# (10) 은퇴소득: 금리별 살 수 있는 연소득
f, ax = fig("panel")
rl = ["실질 3%", "2% (출발)", "1%"]; ci = [3536, 2674, 2008]
xx = np.arange(3)
ax.bar(xx - 0.2, ci, 0.38, color=C["muted"], label="현금 3억")
ax.bar(xx + 0.2, [2674] * 3, 0.38, color=C["lime"], edgecolor=C["body"], label="Retirement Bond")
for i, v in enumerate(ci):
    ax.text(i - 0.2, v + 60, f"{v:,}", ha="center", fontsize=14)
    ax.text(i + 0.2, 2734, "2,674", ha="center", fontsize=14, fontweight="bold")
ax.set_xticks(xx); ax.set_xticklabels(rl); ax.set_ylabel("살 수 있는 연소득 (만 원)"); ax.set_ylim(0, 4300)
ax.legend(loc="upper right", fontsize=14); ax.grid(axis="x", visible=False)
chart("c_income", f)

# (11) 시퀀스 리스크
f, ax = fig("panel")
ax.plot([0, 1, 2], [100, 20, 0], "o-", color=C["red"], label="불황 먼저 (−50% → +50%)")
ax.plot([0, 1, 2], [100, 120, 30], "o-", color=C["teal"], label="호황 먼저 (+50% → −50%)")
ax.text(2.04, 0, "0 (파산)", fontsize=15, color=C["red"], va="center")
ax.text(2.04, 30, "30", fontsize=15, color=C["teal"], va="center")
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["출발", "1년 뒤", "2년 뒤"]); ax.set_xlim(-0.15, 2.5)
ax.set_ylabel("자산 (매년 30 인출 후)"); ax.set_ylim(-8, 170); ax.legend(loc="upper right", fontsize=14)
chart("c_seq", f)

# (12) 케이스 1: Floor 90%에서 승수별 조건 ①·②
f, ax = fig("panel")
mk = ["m 1", "m 2", "m 3", "m 6"]; c1 = [0.1, 3.6, 10.0, 21.3]; c2 = [0.0, 0.1, 1.4, 19.2]
xx = np.arange(4)
ax.bar(xx - 0.2, c1, 0.4, color=[C["teal"], C["lime"], C["teal"], C["teal"]], edgecolor=C["body"], label="① Safety 미달")
ax.bar(xx + 0.2, c2, 0.4, color=C["muted"], label="② Cash Trap")
ax.axhline(5, color=C["red"], ls="--", lw=1.5); ax.text(-0.45, 5.6, "① 임계 5%", color=C["red"], fontsize=14)
ax.axhline(10, color=C["amber"], ls=":", lw=1.5); ax.text(-0.45, 10.6, "② 임계 10%", color=C["amber"], fontsize=14)
for i, v in enumerate(c1):
    # 임계선(5%) 바로 아래에 걸리는 라벨은 막대 안쪽으로 내린다
    if 5 - 1.6 < v + 0.6 < 5 + 0.4:
        ax.text(i - 0.2, v / 2, f"{v:.1f}", ha="center", va="center", fontsize=14, fontweight="bold")
    else:
        ax.text(i - 0.2, v + 0.6, f"{v:.1f}", ha="center", fontsize=14)
ax.set_xticks(xx); ax.set_xticklabels(mk); ax.set_ylabel("확률 (%)"); ax.set_ylim(0, 25)
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88), fontsize=14); ax.grid(axis="x", visible=False)
chart("c_case1", f)

# (13) 케이스 2: 비유동 비중별 생존 연수와 세대 간 중립 확률
xs = ["0%", "10%", "20%", "30%", "60%"]; yrs = [22, 17, 13, 9, 2]; neu = [40, 53, 59, 68, 81]
f, (a1, a2) = fig("square", 2, 1)
a1.bar(xs, yrs, color=[C["teal"], C["teal"], C["lime"], C["muted"], C["muted"]], edgecolor=C["body"], width=0.6)
a1.axhline(10, color=C["red"], ls="--", lw=1.5, label="락업 10년"); a1.legend(loc="upper right", fontsize=14)
for i, v in enumerate(yrs):
    a1.text(i, v + 0.5, f"{v}년", ha="center", fontsize=14)
a1.set_ylabel("버티는 연수"); a1.set_ylim(0, 28); a1.grid(axis="x", visible=False)
a2.bar(xs, neu, color=[C["muted"], C["teal"], C["lime"], C["teal"], C["teal"]], edgecolor=C["body"], width=0.6)
a2.axhline(50, color=C["red"], ls="--", lw=1.5, label="임계 50%"); a2.legend(loc="upper left", fontsize=14); a2.set_ylim(0, 112)
for i, v in enumerate(neu):
    a2.text(i, v + 1.5, f"{v}%", ha="center", fontsize=14)
a2.set_xlabel("비유동 대체 비중 (지출률 4.5%)"); a2.set_ylabel("실질가치 유지 (%)")
a2.grid(axis="x", visible=False)
chart("c_case2", f)

# ---------------------------------------------------------------- SVG
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

def T(x, y, t, size=30, w="400", col="#102027", anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}">{t}</text>')

def box(x, y, w, h, kind="white"):
    fill, stroke = {"white": ("#FFFFFF", "#DDE3E2"), "lime": ("#B7F34A", "#B7F34A"),
                    "dark": ("#071A1D", "#071A1D"), "ghost": ("#F7F5F0", "#DDE3E2")}[kind]
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0B6B68" stroke-width="4" marker-end="url(#ar)"/>'

# (S1) LDI에서 이어받는 것 — 대응표 (전체폭 1600×480, 글씨 32px ≈ 17pt)
rows = [("지킬 것", "부채 현재가치 L", "목표 현재가치 P(G) · K"),
        ("지키는 자산", "LHP — 장기채", "GHP — 물가연동국채"),
        ("버틸 여유", "잉여금 A − L · 적립비율", "쿠션 A − F · 바닥 F"),
        ("두 블록", "PSP + LHP", "PSP + GHP"),
        ("위험의 뜻", "적립비율 하락", "목표 미달 확률")]
W, H = 1600, 500
b = T(185, 36, "개념", 30, "700", "#64757D") + T(635, 36, "기관 · M7 LDI", 32, "700", "#64757D") + T(1255, 36, "개인 · M8 GBI", 32, "700", "#0B6B68")
for i, (k, l, g) in enumerate(rows):
    y = 56 + i * 88
    b += box(20, y, 330, 76, "ghost") + T(185, y + 50, k, 34, "700")
    b += box(370, y, 530, 76, "white") + T(635, y + 50, l, 33)
    last = i == len(rows) - 1
    b += arrow(910, y + 38, 962, y + 38)
    b += box(975, y, 600, 76, "lime" if last else "dark")
    b += T(1275, y + 50, g, 33, "700", "#071A1D" if last else "#B7F34A")
svg_save("s_bridge", b, W, H)

# (S2) 3계층 버킷 피라미드 (1120×720, 우측 열 표시 폭 약 5.5in → 44px ≈ 16pt)
W, H = 1120, 720
tiers = [("③ Aspirational ≥ 30%", "상속 · 꿈 — 주식 · 대체", "white", 720),
         ("② Market ≥ 70%", "여유 생활 — 균형형", "white", 900),
         ("① Safety ≥ 95%", "필수 생활비 — RB · GHP", "dark", 1100)]
b = ""
for i, (t1, t2, k, w) in enumerate(tiers):
    y = 20 + i * 235; x = (W - w) / 2
    b += box(x, y, w, 215, k)
    c1, c2 = ("#B7F34A", "#FFFFFF") if k == "dark" else ("#102027", "#64757D")
    b += T(W / 2, y + 92, t1, 50, "700", c1) + T(W / 2, y + 162, t2, 44, "400", c2)
svg_save("s_bucket", b, W, H)

# (S3) RB → GHP → Floor → Flexicure 체인 (1600×330)
W, H = 1600, 330
items = [("① RB", "이상 자산", "white"), ("② GHP", "복제 포트폴리오", "white"),
         ("③ Floor", "GHP의 현재가치", "white"), ("④ Flexicure", "쿠션 비례 PSP", "lime")]
b = ""
bw, gap = 345, 60
for i, (t1, t2, k) in enumerate(items):
    x = 20 + i * (bw + gap)
    b += box(x, 20, bw, 290, k) + T(x + bw / 2, 140, t1, 48, "700") + T(x + bw / 2, 220, t2, 40, "400", "#102027" if k == "lime" else "#64757D")
    if i < 3:
        b += arrow(x + bw + 6, 165, x + bw + gap - 6, 165)
svg_save("s_chain", b, W, H)

# (S4) 방법 지도 (1600×480)
rows = [("잉여금 흔들림 한도", "고정 비중 + 리스크 예산", "변동성 · VaR", "2절 (LDI)"),
        ("계정별 최악 한도", "심리계정 → γ 번역", "(H, α)", "4절 · 04부"),
        ("반드시 지킬 바닥", "CPPI (바닥은 GHP로)", "Floor · m", "3절 · 03부"),
        ("바닥 위 희망 목표", "바닥을 지킨 CPPI", "필수 비율 · m", "5절 · 04부"),
        ("평생 소득", "RB + Flexicure · 상각 인출", "β · 소득 바닥", "6–7절 · 05부"),
        ("드문 큰 꼬리", "부분 보험 + 예비 자산", "보험료 vs 버퍼", "8절 · 05부")]
W, H = 1600, 490
xs_ = [(10, 380), (405, 560), (980, 300), (1295, 295)]
heads = ["지키고 싶은 것", "쓸 방법", "핵심 손잡이", "도출 III · 이 덱"]
b = "".join(T(x + w / 2, 30, h, 28, "700", "#64757D") for (x, w), h in zip(xs_, heads))
for i, r in enumerate(rows):
    y = 46 + i * 74
    for j, ((x, w), t) in enumerate(zip(xs_, r)):
        k = "dark" if j == 0 else ("lime" if j == 3 else "white")
        b += box(x, y, w, 64, k)
        col = "#B7F34A" if k == "dark" else "#102027"
        b += T(x + w / 2, y + 43, t, 31, "700" if j in (0, 3) else "400", col)
svg_save("s_map", b, W, H)

# (S5) 한 장 요약 — 기관 LDI vs 개인 GBI (가로 대비표 1600×330)
cols = ["지킬 것", "값", "복제 자산", "여유", "비중 규칙", "위험"]
ldi = ["부채 L", "부채 현재가치", "LHP", "잉여금", "리스크 예산", "적립비율 하락"]
gbi = ["목표 G · 소득 c", "K · P(G) · cβ", "GHP · RB", "쿠션 · Floor", "CPPI · Flexicure", "목표 미달 확률"]
W, H = 1600, 330
cw = 236; x0 = 170
b = ""
for j, c in enumerate(cols):
    x = x0 + j * (cw + 4)
    b += T(x + cw / 2, 44, c, 30, "700", "#64757D")
    b += box(x, 66, cw, 116, "white") + T(x + cw / 2, 136, ldi[j], 30)
    last = j == len(cols) - 1
    b += box(x, 196, cw, 116, "lime" if last else "dark") + T(x + cw / 2, 266, gbi[j], 30, "700", "#071A1D" if last else "#B7F34A")
b += T(80, 136, "기관 LDI", 30, "700", "#64757D") + T(80, 266, "개인 GBI", 30, "700", "#0B6B68")
svg_save("s_summary", b, W, H)

json.dump(R, open("ratios.json", "w"), indent=1, ensure_ascii=False)
print(f"ratios → ratios.json ({len(R)})  pmiss={pmiss:.3f}")
