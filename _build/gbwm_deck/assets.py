#!/usr/bin/env python3
"""DORS GBWM 연작 덱 — 수식 PNG · matplotlib 차트 · SVG 도해.
실행: <python> compute.py (numbers.json · arrays.npz) → <python> assets.py → node build.js
숫자는 전부 numbers.json(재계산)에서 읽는다. 원문 값은 numbers.json의 paper_* 키.
"""
import os, json
import numpy as np
from scipy.stats import norm
import cairosvg
from render_eq import render, INK, PAPER, LIME, DARK, WHITE
from zo_mpl import fig, save, C

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
for d in ("eq", "fig", "svg"):
    os.makedirs(d, exist_ok=True)
N = json.load(open("numbers.json"))
A = np.load("arrays.npz")
R = {}


def eq(name, tex, fs=30, dark=False, white=False):
    bg = DARK if dark else (WHITE if white else PAPER)
    _, r = render(tex, name + ".png", fontsize=fs, color=LIME if dark else INK, bg=bg)
    R["eq/" + name] = r


def chart(name, f):
    R["fig/" + name] = save(f, f"fig/{name}.png")


pct = lambda x, d=1: f"{100 * x:.{d}f}%"
Y18, Y20 = N["y2018"], N["y2020"]

# =============================================================== 수식
eq("gbm", r"\tilde{W}(t)=W(0)\,e^{\left(\mu-\sigma^{2}/2\right)t+\sigma\sqrt{t}\,Z},\qquad Z\sim N(0,1)")
eq("gplc", r"\mu=\frac{1}{2}\,\sigma^{2}+\frac{z_{0}}{\sqrt{t}}\,\sigma+\frac{1}{t}\,\ln\frac{W(t)}{W(0)}", dark=True)
eq("zfun", r"z(\sigma,\mu)=\frac{\sqrt{t}}{\sigma}\left(\mu-\frac{\sigma^{2}}{2}-r\right),\qquad r=\frac{1}{t}\ln\frac{W(t)}{W(0)}")
eq("ef", r"\sigma^{2}=a\,\mu^{2}+b\,\mu+c\qquad (a,\ b,\ c\ \ \mathrm{from}\ \ \mu,\ \Sigma)")
eq("cubic", r"a^{2}\mu^{3}+\frac{3ab}{2}\,\mu^{2}+\left(ac+\frac{b^{2}}{2}-b-2ar\right)\mu+\frac{bc}{2}-2c-br=0", dark=True)
s_o, m_o, p_o = Y18["ogpp"]
zo = (m_o - s_o ** 2 / 2 - Y18["intercept"]) * np.sqrt(10) / s_o
eq("znum", rf"z=\frac{{\sqrt{{10}}}}{{{s_o:.3f}}}\left({m_o:.4f}-\frac{{{s_o:.3f}^{{2}}}}{{2}}-{Y18['intercept']:.4f}\right)={zo:.3f}\ \ \Rightarrow\ \ \Phi(z)={100 * p_o:.1f}\%")
# 2020
eq("obj20", r"\max_{A(0),\,\ldots,\,A(T-1)}\ \ \Pr\left[\,W(T)\geq G\,\right]", fs=34, dark=True)
eq("imax", r"i_{max}=\left\lceil\frac{\left(\ln\hat{W}_{max}-\ln\hat{W}_{min}\right)\rho}{\sigma_{min}}\right\rceil,\qquad \hat{W}_{min,\,max}:\ Z=\mp 3")
eq("trans", r"p(W_{j}\,|\,W_{i},\mu)\ \propto\ \phi\left(\frac{1}{\sigma}\left[\ln\frac{W_{j}}{W_{i}+C(t)}-\left(\mu-\frac{\sigma^{2}}{2}\right)\right]\right)")
eq("bell", r"V(W_{i},t)=\max_{\mu\in[\mu_{min},\,\mu_{max}]}\ \sum_{j}V(W_{j},t+1)\ p(W_{j}\,|\,W_{i},\mu),\qquad V(W,T)=\mathbf{1}[W\geq G]", dark=True)
eq("fwd", r"p(W_{j},t+1)=\sum_{i}p(W_{j}\,|\,W_{i},\mu_{i,t})\ p(W_{i},t)")
H = N["hand"]
eq("hz", r"z_{j}=\frac{\ln(W_{j}/100)-(0.0886-0.1954^{2}/2)}{0.1954},\qquad q_{j}=\frac{\phi(z_{j})}{\sum_{k}\phi(z_{k})}")
eq("hv0", rf"V(100,0)=\max\{{\,{H['E0'][0]:.3f}\ (A),\ \ {H['E0'][1]:.3f}\ (B)\,\}}={max(H['E0']):.3f}", dark=True)
# 2022
eq("bell22", r"V(W_{i},t)=\max_{k,\,l}\left[\,u_{k}(t)+\sum_{J}V(W_{J},t+1)\ q\left(W_{J}\,|\,W_{i}+I(t)-c_{k}(t),\ \mu_{l}\right)\right]", dark=True)
eq("eu", r"E^{*}[u]=\sum_{g}u_{g}\ \Pr[\mathrm{fulfill}\ g]\qquad 1855=1000\times 0.123+2000\times 0.866")
eq("cplx", r"O\left(i_{max}\left[\,T\,l_{max}+\sum_{t}k_{max}(t)\right]\right)\quad \mathrm{vs}\quad 100^{\,n}", dark=True)
# EGP
eq("upd", r"U_{new}=U_{old}+\Delta U\,(d-p_{old}),\qquad \mathrm{stop:}\ \ \frac{U}{\|U\|}=\frac{d-p}{\|d-p\|}", dark=True)
eq("sec", r"W_{0}^{(n+1)}=W_{0}^{(n)}-s_{n}\,\frac{W_{0}^{(n)}-W_{0}^{(n-1)}}{s_{n}-s_{n-1}},\qquad s=\pm\|d-p_{prox}\|")
for nm, tex in [("s_gplc", r"\mu=\sigma^{2}/2+z\sigma/\sqrt{t}+r"), ("s_bell", r"V_{t}=\max_{\mu}E[V_{t+1}]"),
                ("s_bell22", r"V_{t}=\max_{k,l}[u_{k}+E\,V_{t+1}]"), ("s_upd", r"U\ \leftarrow\ U+\Delta U(d-p)")]:
    eq(nm, tex, white=True)

# =============================================================== 차트
a18, b18, c18 = Y18["abc"]
sig18 = lambda M: np.sqrt(a18 * M * M + b18 * M + c18)
r18, rl18 = Y18["intercept"], np.log(300 / 400) / 10
mv = -b18 / 2 / a18
Mu = np.linspace(mv, 0.30, 600); Su = sig18(Mu)
zz = lambda S, M, r: (M - S * S / 2 - r) * np.sqrt(10) / S

# (1) 효율선을 따라가며 목표 확률 — 2018 예
f, ax = fig("panel")
pg = norm.cdf(zz(Su, Mu, r18)); pl = norm.cdf(zz(Su, Mu, rl18))
ax.plot(Su * 100, pg * 100, color=C["teal"], label="목표 50만 달러 달성")
ax.plot(Su * 100, pl * 100, color=C["blue"], label="손실 문턱 30만 달러 유지")
i = np.argmax(pg)
ax.plot(Su[i] * 100, pg[i] * 100, "o", color=C["red"], ms=10)
ax.annotate(f"최대 {pg[i] * 100:.1f}%\nσ {Su[i] * 100:.1f}%", (Su[i] * 100, pg[i] * 100), textcoords="offset points", xytext=(14, -58), fontsize=15, color=C["red"])
ax.annotate("변동성을 줄이면\n목표 확률도 줄어든다", (3, norm.cdf(zz(sig18(0.035), 0.035, r18)) * 100), xytext=(7, 36), fontsize=15,
            arrowprops=dict(arrowstyle="->", color=C["body"], lw=1.4))
ax.set_xlim(0, 45); ax.set_ylim(0, 105)
ax.set_xlabel("효율선 위 포트폴리오의 변동성 σ (%)"); ax.set_ylabel("10년 뒤 확률 (%)"); ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.02))
chart("c_risk", f)

# (2) 등고선 가족 (원문 그림 4)
f, ax = fig("panel")
sg = np.linspace(0, 0.45, 300)
for p, col in [(0.5, C["hair"]), (0.6, C["muted"]), (0.7, C["muted"]), (0.8, C["teal"]), (0.9, C["blue"]), (0.95, C["blue"]), (0.99, C["amber"])]:
    z0 = norm.ppf(p)
    ax.plot(sg * 100, (sg ** 2 / 2 + z0 * sg / np.sqrt(10) + r18) * 100, color=col, lw=3.0 if p == 0.8 else 1.8)
    ax.text(sg[-1] * 100 + 0.5, (sg[-1] ** 2 / 2 + z0 * sg[-1] / np.sqrt(10) + r18) * 100, f"{p * 100:.0f}%", fontsize=14, va="center", color=col if p != 0.5 else C["muted"])
ax.plot(0, r18 * 100, "o", color=C["red"], ms=9)
ax.annotate(f"모두 μ = r = {r18 * 100:.2f}%에서 만난다", (0, r18 * 100), xytext=(4, 46), fontsize=15, color=C["red"],
            arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.4))
ax.set_xlim(0, 52); ax.set_ylim(-2, 60)
ax.set_xlabel("변동성 σ (%)"); ax.set_ylabel("기대수익률 μ (%)")
chart("c_gplc", f)

# (3) 접점 (원문 그림 8–11)
f, ax = fig("panel")
Mall = np.linspace(-0.09, 0.30, 600)
ax.plot(sig18(Mall) * 100, Mall * 100, color=C["body"], lw=2.4, label="효율선 (원문 점으로 역산)")
for p, col, lab, r_ in [(p_o, C["red"], f"{p_o * 100:.1f}% 등고선", r18), (0.8, C["teal"], "80% 등고선", r18), (0.95, C["blue"], "95% 손실 문턱선", rl18)]:
    z0 = norm.ppf(p)
    ax.plot(sg * 100, (sg ** 2 / 2 + z0 * sg / np.sqrt(10) + r_) * 100, color=col, lw=2.0, ls="--" if p == 0.95 else "-", label=lab)
pts = [("최적점", Y18["ogpp"][:2], C["red"], (14, -34)), ("상단 목표점", Y18["ugp"], C["teal"], (-250, 18)),
       ("손실 문턱점", Y18["ltp"], C["blue"], (14, -34))]
for lab, (s_, m_), col, off in pts:
    ax.plot(s_ * 100, m_ * 100, "o", color=col, ms=9)
    ax.annotate(f"{lab} ({s_:.3f}, {m_:.3f})", (s_ * 100, m_ * 100), textcoords="offset points", xytext=off, fontsize=14, color=col)
ax.set_xlim(0, 48); ax.set_ylim(-8, 30)
ax.set_xlabel("변동성 σ (%)"); ax.set_ylabel("기대수익률 μ (%)"); ax.legend(loc="upper left", fontsize=13)
chart("c_tangent", f)

# (4) W(0) 민감도
sens = np.array(Y18["w0_sens"])
f, ax = fig("panel")
ax.plot(sens[:, 0] / 10, sens[:, 1] * 100, color=C["teal"], marker="o", ms=5)
for w0_, off in [(300, (10, 4)), (350, (10, 6)), (400, (10, 6)), (450, (10, 6))]:
    k = int(np.argmin(abs(sens[:, 0] - w0_)))
    ax.plot(sens[k, 0] / 10, sens[k, 1] * 100, "o", color=C["red"] if w0_ == 400 else C["body"], ms=9)
    ax.annotate(f"σ* {sens[k, 1] * 100:.1f}% · 확률 {sens[k, 3] * 100:.1f}%", (sens[k, 0] / 10, sens[k, 1] * 100), textcoords="offset points",
                xytext=off, fontsize=14, color=C["red"] if w0_ == 400 else C["body"])
ax.set_xlim(29, 52); ax.set_ylim(0, 32)
ax.set_xlabel("초기 자산 W(0) (만 달러) · 목표 50만 달러 · 10년"); ax.set_ylabel("최적점의 변동성 σ* (%)")
chart("c_w0", f)

# (5) 2020 효율선 + 15개
mus, sigs = np.array(Y20["mus"]), np.array(Y20["sigs"])
a20, b20, c20 = Y20["abc"]
Mf = np.linspace(-b20 / 2 / a20 - 0.02, 0.10, 400)
f, ax = fig("panel")
ax.plot(np.sqrt(a20 * Mf ** 2 + b20 * Mf + c20) * 100, Mf * 100, color=C["body"], lw=2.0, label="효율선 (공매도 허용)")
ax.plot(sigs * 100, mus * 100, "o", color=C["teal"], ms=8, label="포트폴리오 0 ~ 14")
for k in (0, 7, 14):
    ax.annotate(f"{k}번 ({sigs[k] * 100:.1f}%, {mus[k] * 100:.2f}%)", (sigs[k] * 100, mus[k] * 100), textcoords="offset points",
                xytext=(10, -18) if k else (12, 10), fontsize=14)
names = ["미국 채권", "해외 주식", "미국 주식"]
sd = np.sqrt(np.diag(np.array([[0.0017, -0.0017, -0.0021], [-0.0017, 0.0396, 0.0309], [-0.0021, 0.0309, 0.0392]])))
for nm, m_, s_ in zip(names, [0.0493, 0.0770, 0.0886], sd):
    ax.plot(s_ * 100, m_ * 100, "s", color=C["amber"], ms=8)
    ax.annotate(nm, (s_ * 100, m_ * 100), textcoords="offset points", xytext=(10, -18) if nm == "미국 채권" else (8, 8), fontsize=14, color=C["amber"])
ax.set_xlim(0, 24); ax.set_ylim(4.0, 9.8)
ax.set_xlabel("변동성 σ (%)"); ax.set_ylabel("기대수익률 μ (%)"); ax.legend(loc="upper left", fontsize=13)
chart("c_ef20", f)

# (6)(7) 가치함수 · 전략 지도 (원문 그림 3–4)
W20, V20, L20 = A["W20"], A["V20"], A["L20"]
band = (W20 >= 37) & (W20 <= 226)
for name, M_, cmap, lab in [("c_value", V20, "YlGnBu", "목표 확률 V"), ("c_policy", L20, "YlOrRd", "포트폴리오 번호")]:
    f, ax = fig("panel")
    im = ax.pcolormesh(np.arange(10), W20[band], M_[:, band].T, cmap=cmap, shading="nearest",
                       vmin=0, vmax=1 if name == "c_value" else 14)
    ax.set_yscale("log"); ax.set_yticks([40, 60, 100, 150, 200]); ax.set_yticklabels(["40", "60", "100", "150", "200"])
    ax.minorticks_off()
    ax.set_xticks(range(10)); ax.set_xlabel("시점 t (년)"); ax.set_ylabel("자산 W (로그 눈금)")
    cb = f.colorbar(im, ax=ax, pad=0.02); cb.set_label(lab); cb.outline.set_visible(False)
    ax.axhline(200, color=C["red"], lw=1.6, ls="--"); ax.grid(False)
    ax.plot(0, 100, "o", color=C["red"], ms=8)
    chart(name, f)

# (8) DP 대 고정 · 정적
fx = Y20["fixed"]
labs = ["0번 고정", "7번 고정", "14번 고정", "2018 정적 · 한 번", "2018 정적 · 매년", "동적계획법"]
vals = [fx[0], fx[7], fx[14], Y20["oneshot_static"], Y20["repeated_static"], Y20["P200"]]
f, ax = fig("wide")
cols = [C["hair"]] * 3 + [C["muted"], C["blue"], C["lime_dk"]]
ax.barh(labs[::-1], np.array(vals[::-1]) * 100, color=cols[::-1])
for k, v in enumerate(vals[::-1]):
    ax.text(v * 100 + 0.8, k, f"{v * 100:.1f}%", va="center", fontsize=15, fontweight="bold" if k == 0 else "normal")
ax.axvline(66.9, color=C["red"], ls="--", lw=1.6); ax.text(67.6, 4.6, "원문 66.9%", fontsize=14, color=C["red"])
ax.set_xlim(0, 80); ax.set_ylim(-0.6, 5.9); ax.set_xlabel("P[W(10) ≥ 200] · W(0) = 100 (%)"); ax.grid(axis="y", visible=False)
chart("c_compare", f)

# (9) 분포 (원문 그림 2)
P20 = A["P20"]
f, ax = fig("panel")
cm = __import__("matplotlib").colormaps["viridis"]
for t in range(1, 11):
    surv = 1 - np.cumsum(P20[t]) + P20[t]
    ax.plot(W20, surv, color=cm((t - 1) / 9), lw=2.6 if t == 10 else 1.4, label=f"t = {t}" if t in (1, 5, 10) else None)
ax.axvline(200, color=C["red"], ls="--", lw=1.6); ax.text(205, 0.92, "G = 200", fontsize=15, color=C["red"])
ax.set_xlim(40, 400); ax.set_ylim(0, 1.02)
ax.set_xlabel("자산 W"); ax.set_ylabel("P[W(t) ≥ W]"); ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.85))
chart("c_dist", f)

# (10) 납입 · 인출 (표 5 · 6)
cf = np.array(Y20["cashflow"]); pc = np.array(Y20["paper_cashflow"])
o = np.argsort(cf[:, 0]); cf = cf[o]; pc = pc[np.argsort(pc[:, 0])]
f, ax = fig("panel")
ax.plot(cf[:, 0], cf[:, 3] * 100, color=C["teal"], marker="o", label="P[W(10) ≥ 200] 재계산")
ax.plot(cf[:, 0], cf[:, 1] * 100, color=C["red"], marker="o", label="파산 확률 재계산")
ax.plot(pc[:, 0], pc[:, 3] * 100, "x", color=C["body"], ms=10, mew=2.2, label="원문 표 5 · 6")
ax.plot(pc[:, 0], pc[:, 1] * 100, "x", color=C["body"], ms=10, mew=2.2)
ax.set_xlabel("해마다 넣는(+) · 빼는(−) 금액 C (W(0) = 100)"); ax.set_ylabel("확률 (%)"); ax.legend(loc="upper center", fontsize=13)
chart("c_cash", f)

# (11) 은퇴 예 · TDF (표 7)
rt = np.array(Y20["retire"]); pr = np.array(Y20["paper_retire"])
f, ax = fig("panel")
ax.plot(rt[:, 0], rt[:, 1] * 100, color=C["teal"], marker="o", label="DP 재계산")
ax.plot(rt[:, 0], rt[:, 2] * 100, color=C["amber"], marker="o", label="TDF 재계산 (모의 20만)")
ax.plot(pr[:, 0], pr[:, 1] * 100, "x", color=C["body"], ms=10, mew=2.2, label="원문 표 7")
ax.plot(pr[:, 0], pr[:, 2] * 100, "x", color=C["body"], ms=10, mew=2.2)
k15 = list(rt[:, 0]).index(15)
ax.annotate("", (15, rt[k15, 1] * 100), (15, rt[k15, 2] * 100), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.8))
ax.annotate(f"c = 15에서 +{(rt[k15, 1] - rt[k15, 2]) * 100:.1f}%p", (15, (rt[k15, 1] + rt[k15, 2]) * 50), xytext=(21, 22), fontsize=15, color=C["red"], fontweight="bold", arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.4))
ax.set_xlabel("은퇴 전 연 납입 c (천 달러, 실질)"); ax.set_ylabel("80세까지 지급 능력 유지 (%)"); ax.legend(loc="upper left", fontsize=13)
chart("c_retire", f)

# (12) 결정 구간 — 시점 5에서 산다 · 건너뛴다
W22, tk, fg = A["W22"], A["take"], A["forgo"]
mk = (W22 >= 80) & (W22 <= 260)
f, ax = fig("panel")
ax.plot(W22[mk], fg[mk], color=C["blue"], label="건너뛴다: 10년 목표만 노림")
ax.plot(W22[mk], np.where(np.isfinite(tk[mk]), tk[mk], np.nan), color=C["teal"], label="산다: 2000 + 이후 기댓값")
best = np.maximum(fg, np.where(np.isfinite(tk), tk, -np.inf))
sw = N["y2022_switch"]
for x in sw:
    if 80 <= x <= 260: ax.axvline(x, color=C["red"], ls=":", lw=1.6)
for x, ha_, dx in zip([s for s in sw if 80 <= s <= 260], ["right", "left", "left"], [-2, 2, 2]):
    ax.text(x + dx, 400, f"{x:.0f}", fontsize=15, color=C["red"], fontweight="bold", ha=ha_)
ax.fill_between(W22[mk], 0, 5200, where=(fg[mk] > np.nan_to_num(tk[mk], neginf=-1)) & (W22[mk] >= 100), color=C["blue"], alpha=0.08)
ax.set_ylim(0, 5200); ax.set_xlabel("시점 5의 자산 W(5)"); ax.set_ylabel("기대 효용")
ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.33), fontsize=13)
chart("c_switch", f)

# (13) 일곱 목표
S7 = N["y2022_seven"]
f, ax = fig("wide")
x = np.arange(7); wd = 0.2
ax.bar(x - 1.5 * wd, np.array(S7["paper"]["p"]) * 100, wd, color=C["hair"], label="Run 1 원문 (W(0) 30)")
ax.bar(x - 0.5 * wd, np.array(S7["p"]) * 100, wd, color=C["teal"], label="Run 1 재계산")
ax.bar(x + 0.5 * wd, np.array(S7["paper"]["p7"]) * 100, wd, color=C["muted"], label="Run 7 원문 (W(0) 50 · 납입)")
ax.bar(x + 1.5 * wd, np.array(S7["p7"]) * 100, wd, color=C["lime_dk"], label="Run 7 재계산")
for k, tg in enumerate([60, 99, 30, 60, 30, 99, 60]):
    ax.plot([k - 2 * wd, k + 2 * wd], [tg, tg], color=C["red"], lw=2.2)
ax.plot([], [], color=C["red"], lw=2.2, label="원하는 최소 확률")
ax.set_xticks(x); ax.set_xticklabels([f"{k + 1} (t {t})" for k, (t, c) in enumerate([(5, 25), (8, 17), (10, 15), (11, 80), (17, 50), (22, 60), (24, 130)])], fontsize=13)
ax.set_ylabel("달성 확률 (%)"); ax.set_ylim(0, 150); ax.set_yticks([0, 25, 50, 75, 100]); ax.legend(loc="upper left", ncol=3, fontsize=12)
ax.grid(axis="x", visible=False)
chart("c_seven", f)

# (14) 목표 수 대 계산량
sc = np.array(N["scaling"])
f, ax = fig("panel")
n_ = np.arange(1, 25)
ax.semilogy(n_, 100.0 ** n_, color=C["red"], label="한 계좌 격자 MC 후보 수 = 100ⁿ (M8 46장)")
ax.semilogy(n_, 20 * n_, color=C["amber"], label="계좌 분리 + 이분법 = 20n")
ax2 = ax.twinx()
ax2.plot(sc[:, 0], sc[:, 1], "o-", color=C["teal"], label="DP 실측 시간 (초, 오른쪽)")
ax2.set_ylabel("DP 시간 (초) · 25년 · 556칸", color=C["teal"]); ax2.tick_params(axis="y", colors=C["teal"]); ax2.grid(False)
ax2.spines["right"].set_visible(True); ax2.set_ylim(0, max(sc[:, 1]) * 1.6)
ax.set_xlabel("목표 수 n"); ax.set_ylabel("후보 수 (로그)")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=12)
chart("c_scal", f)

# (15) 2022 은퇴 세 목표 · TDF (표 8)
R8 = N["y2022_retire"]
f, ax = fig("panel")
x = np.arange(3); wd = 0.2
for k, (vals_, col, lab) in enumerate([(R8["paper_dp"], C["hair"], "DP 원문"), (R8["dp"], C["teal"], "DP 재계산"),
                                        (R8["paper_tdf"], C["muted"], "TDF 원문"), (R8["tdf"], C["amber"], "TDF 재계산")]):
    ax.bar(x + (k - 1.5) * wd, np.array(vals_) * 100, wd, color=col, label=lab)
    for j, v in enumerate(vals_):
        ax.text(x[j] + (k - 1.5) * wd, v * 100 + 1.2, f"{v * 100:.0f}", ha="center", fontsize=13)
ax.set_xticks(x); ax.set_xticklabels(["70세 연금", "85세 연금", "95세 증여"])
ax.set_ylabel("앞 목표를 모두 낸 경로 (%)"); ax.set_ylim(0, 118); ax.set_yticks([0, 20, 40, 60, 80, 100]); ax.legend(loc="upper center", fontsize=12, ncol=4)
ax.grid(axis="x", visible=False)
chart("c_ret22", f)

# (16) EGPF
E = N["egp"]
fr = np.array(E["fr50"])
f, ax = fig("panel")
ax.plot(fr[:, 1] * 100, fr[:, 2] * 100, color=C["body"], lw=1.4, zorder=1)
sc_ = ax.scatter(fr[:, 1] * 100, fr[:, 2] * 100, c=fr[:, 3], cmap="YlOrRd", vmin=0, vmax=14, s=70, zorder=2, edgecolor=C["body"], linewidth=0.6)
cb = f.colorbar(sc_, ax=ax, pad=0.02); cb.set_label("처음 고르는 포트폴리오"); cb.outline.set_visible(False)
p1max = fr[:, 1].max(); p2at = fr[np.argmax(fr[:, 1]), 2]
ax.plot([p1max * 100, p1max * 100], [0, p2at * 100], color=C["body"], ls="--", lw=1.4)
ax.fill_between([0, 100], [0, 0], [100, 100], color="none")
ax.annotate(f"학자금 목표만: {fr[:, 2].max() * 100:.1f}%", (0, fr[:, 2].max() * 100), xytext=(8, 94), fontsize=14,
            arrowprops=dict(arrowstyle="->", color=C["body"], lw=1.2))
ax.annotate(f"차 목표만: {p1max * 100:.1f}% · {p2at * 100:.1f}%", (p1max * 100, p2at * 100), xytext=(10, 5), fontsize=14,
            arrowprops=dict(arrowstyle="->", color=C["body"], lw=1.2))
ax.text(52, 70, "불가능", fontsize=16, color=C["red"], fontweight="bold")
ax.text(14, 30, "가능하지만 비효율", fontsize=15, color=C["muted"])
ax.set_xlim(0, 80); ax.set_ylim(0, 100)
ax.set_xlabel("목표 1 · 10년 뒤 차 100 확률 (%)"); ax.set_ylabel("목표 2 · 20년 뒤 학자금 150 확률 (%)")
chart("c_egpf", f)

# (17) 근접점 · 최소 초기 자금
f, ax = fig("panel")
for key, col, lab in [("fr50", C["muted"], "W(0) = 50"), ("fr_min", C["teal"], f"W(0) = {E['minW']:.1f} (최소)"), ("fr100", C["blue"], "W(0) = 100")]:
    q = np.array(E[key]); ax.plot(q[:, 1] * 100, q[:, 2] * 100, color=col, marker="o", ms=4, label=lab)
ax.plot(70, 80, "*", color=C["red"], ms=18, label="원하는 점 d = (70%, 80%)")
pp = E["prox50"]
ax.plot(pp[0] * 100, pp[1] * 100, "o", color=C["body"], ms=10)
ax.annotate("", (70, 80), (pp[0] * 100, pp[1] * 100), arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.6))
ax.annotate(f"근접점 ({pp[0] * 100:.1f}, {pp[1] * 100:.1f})\n거리 {E['dist50']:.3f}", (pp[0] * 100, pp[1] * 100), textcoords="data", xytext=(2, 60), fontsize=14,
            arrowprops=dict(arrowstyle="->", color=C["body"], lw=1.2))
ax.set_xlim(0, 100); ax.set_ylim(0, 105)
ax.set_xlabel("목표 1 확률 (%)"); ax.set_ylabel("목표 2 확률 (%)"); ax.legend(loc="lower left", fontsize=12)
chart("c_egpmin", f)

# (18) M8 세 목표 DP 전략 지도
W8, L8 = A["W8"], A["L8"]
M8 = N["m8"]
b8 = (W8 >= 3) & (W8 <= 20)
f, ax = fig("panel")
im = ax.pcolormesh(np.arange(10), W8[b8], (L8[:, b8].T * 5), cmap="YlOrRd", shading="nearest", vmin=0, vmax=100)
ax.set_yscale("log"); ax.set_yticks([4, 6, 9, 14, 20]); ax.set_yticklabels(["4", "6", "9", "14", "20"]); ax.minorticks_off()
for y_, lab in [(6, "Safety 6"), (9, "Market 9"), (14, "Aspirational 14")]:
    ax.axhline(y_, color=C["body"], lw=1.2, ls="--")
    ax.text(9.6, y_ * 1.02, lab, fontsize=13, ha="right", va="bottom")
ax.plot(0, M8["minW"], "o", color=C["teal"], ms=9)
cb = f.colorbar(im, ax=ax, pad=0.02); cb.set_label("주식 비중 (%)"); cb.outline.set_visible(False)
ax.set_xticks(range(10)); ax.set_xlabel("시점 t (년)"); ax.set_ylabel("자산 (억, 로그)"); ax.grid(False)
chart("c_m8", f)

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


def T(x, y, t, size=30, w="400", col="#102027", anchor="middle", fam=FONT):
    t = str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" xml:space="preserve">{t}</text>')


def box(x, y, w, h, kind="white", r=0):
    fill, stroke = {"white": ("#FFFFFF", "#DDE3E2"), "lime": ("#B7F34A", "#B7F34A"), "dark": ("#071A1D", "#071A1D"),
                    "ghost": ("#F7F5F0", "#DDE3E2"), "teal": ("#0B6B68", "#0B6B68")}[kind]
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def arrow(x1, y1, x2, y2, dash=False):
    d = ' stroke-dasharray="10 8"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#0B6B68" stroke-width="4"{d} marker-end="url(#ar)"/>'


TC = {"white": ("#0B6B68", "#102027"), "ghost": ("#64757D", "#102027"), "dark": ("#B7F34A", "#FFFFFF"), "lime": ("#071A1D", "#071A1D")}


def card(x, y, w, h, kind, title, lines, ts=32, ls=30, gap=46):
    b = box(x, y, w, h, kind)
    tc, bc = TC[kind]
    b += T(x + w / 2, y + 54, title, ts, "700", tc)
    for j, l in enumerate(lines):
        b += T(x + w / 2, y + 54 + 58 + j * gap, l, ls, "400", bc)
    return b


# (S1) 계보 지도 1600×500
W_, H_ = 1600, 500
nodes = [("Roy 1952", ["안전우선"], ["미달 확률 최소"], "ghost"), ("DMSS 2010", ["심리계정"], ["(H, α) → γ", "한 기간"], "white"),
         ("DORS 2018", ["효율선 위", "목표 확률"], ["정적 · 하나"], "white"), ("DORS 2020", ["동적계획법"], ["목표 하나", "여러 기간"], "white"),
         ("DORS 2022", ["여러 목표", "부분 달성"], ["살지 말지"], "white"), ("DORS 2023", ["목표 확률", "프런티어"], ["최소 자금"], "lime")]
b = ""
bw, gapx = 236, 37
for k, (yr, t1, t2, kind) in enumerate(nodes):
    x = 10 + k * (bw + gapx)
    b += box(x, 10, bw, 230, kind)
    tc = "#071A1D" if kind == "lime" else "#0B6B68"
    b += T(x + bw / 2, 56, yr, 32, "700", "#071A1D" if kind == "lime" else "#64757D")
    for j, part in enumerate(t1):
        b += T(x + bw / 2, 104 + j * 38, part, 31, "700", tc)
    for j, part in enumerate(t2):
        b += T(x + bw / 2, 104 + len(t1) * 38 + 14 + j * 36, part, 29)
    if k < 5:
        b += arrow(x + bw + 3, 125, x + bw + gapx - 3, 125)
solves = [None, ("문턱 · 확률로", "γ를 대신"), ("목표 확률 최대", "접점 = 3차식"), ("해마다 다시", "Bellman 역산"), ("목표 우선순위", "효용 가중 DP"), ("확률로 상담", "근접점 · 할선")]
for k, sv in enumerate(solves):
    if not sv: continue
    x = 10 + k * (bw + gapx) + bw / 2
    b += T(x, 284, sv[0], 30, "700", "#0B6B68") + T(x, 322, sv[1], 30)
b += T(10 + bw / 2, 284, "푸는 것 →", 30, "700", "#64757D")
b += box(10, 360, 1580, 130, "dark")
b += T(800, 412, "후속 강화학습 — Das–Varma 2020 (JOIM) · 여러 목표 RL 2024 (IEEE AIxB) · 메타 RL 2026 (JFDS 게재 예정)", 30, "700", "#B7F34A")
b += T(800, 462, "세금 · 사망 · 목표 미루기처럼 상태가 늘면 격자 DP 대신 학습으로 — 저자 사이트 목록", 30, "400", "#FFFFFF")
svg_save("s_lineage", b, W_, H_)

# (S2) 요건 아홉 · 정보 여덟 1600×500
W_, H_ = 1600, 500
props = ["① 명료성 — 목표가 분명하다", "② 맞춤 — 목표마다 다른 조언", "③ 위험 구체성 — 확률을 늘 보인다",
         "④ 위험 준수 — 조언이 확률을 따른다", "⑤ 고객 언어 — 금액 · 시점 · 확률", "⑥ 상태 기준 — 종목 말고 전체",
         "⑦ 효율 — 늘 효율선 위", "⑧ 상태 의존 — 시장 따라 점이 움직인다", "⑨ 재조정 규칙 — 정기 · 수시"]
info = ["기간 t", "초기 자산 W(0)", "목표 자산 W(t)", "목표 확률", "손실 문턱 자산", "손실 문턱 확률", "좋은 상태의 선호", "나쁜 상태의 선호"]
b = box(10, 10, 1010, 480, "white") + T(515, 58, "GBWM이 갖출 요건 아홉 (원문 3절)", 32, "700", "#0B6B68")
for k, p in enumerate(props):
    x = 40 if k < 5 else 540
    y = 120 + (k if k < 5 else k - 5) * 72
    b += T(x, y, p, 29, "400", "#102027", "start")
b += box(1040, 10, 550, 480, "dark") + T(1315, 58, "고객에게 묻는 정보 여덟", 32, "700", "#B7F34A")
for k, p in enumerate(info):
    col = "#B7F34A" if k >= 6 else "#FFFFFF"
    x = 1070 if k % 2 == 0 else 1330
    b += T(x, 130 + (k // 2) * 92, f"({k + 1}) {p}", 29 if len(p) < 8 else 27, "400", col, "start")
svg_save("s_props", b, W_, H_)

# (S3) 좋은 상태 · 나쁜 상태 1600×620
W_, H_ = 1600, 620
b = box(10, 20, 770, 580, "white") + T(395, 74, "좋은 상태 — 목표 영역이 효율선과 겹친다", 30, "700", "#0B6B68")
for k, (o1, o2) in enumerate([("선택 1", "목표 확률 최대 → 최적점"), ("선택 2", "확률 ≥ 목표 확률 안에서 기대수익 최대 → 상단 목표점"),
                              ("선택 3", "둘의 σ 평균 → 중간점")]):
    b += T(50, 150 + k * 80, o1, 30, "700", "#102027", "start") + T(170, 150 + k * 80, o2, 26 if len(o2) > 22 else 29, "400", "#102027", "start")
b += T(50, 420, "손실 문턱점이 상단 목표점보다 왼쪽이면", 29, "400", "#64757D", "start")
b += T(50, 465, "선택 2 · 3은 손실 문턱점에서 멈춘다", 29, "700", "#0B6B68", "start")
b += T(50, 545, f"원문 예: 최적점 σ {Y18['ogpp'][0]:.3f} · 상단 {Y18['ugp'][0]:.3f}", 28, "400", "#64757D", "start")
b += box(820, 20, 770, 580, "dark") + T(1205, 74, "나쁜 상태 — 목표와 손실 문턱이 충돌", 30, "700", "#B7F34A")
for k, (o1, o2) in enumerate([("선택 1", "목표 확률 최대 → 최적점(위험↑)"), ("선택 2", "손실 문턱 유지 → 문턱점(위험↓)"),
                              ("선택 3", "둘의 σ 평균 → 중간점")]):
    b += T(860, 150 + k * 80, o1, 30, "700", "#B7F34A", "start") + T(980, 150 + k * 80, o2, 29, "400", "#FFFFFF", "start")
b += T(860, 420, "문턱선까지 효율선 위로 뜨면 선택 2도", 29, "400", "#9FB0B2", "start")
b += T(860, 465, "미달 확률을 줄이려 위험을 다시 늘린다", 29, "700", "#FFFFFF", "start")
b += T(860, 545, "고객은 이 선호 둘만 미리 말해 둔다 (정보 7 · 8)", 28, "400", "#9FB0B2", "start")
svg_save("s_options", b, W_, H_)

# (S4) 상태 × 시점 격자 1600×620
W_, H_ = 1600, 620
b = ""
xs = [150, 470, 800, 1130]; ys = [110, 210, 310, 410, 510]
for xi, x in enumerate(xs):
    b += T(x, 585, ["t = 0", "t = 1", "…", "t = T"][xi], 30, "700", "#64757D")
    for yi, y in enumerate(ys):
        kind = "lime" if (xi == 3 and yi <= 1) else ("dark" if (xi == 0 and yi == 2) else "white")
        b += f'<circle cx="{x}" cy="{y}" r="24" fill="{ {"lime": "#B7F34A", "dark": "#071A1D", "white": "#FFFFFF"}[kind]}" stroke="#0B6B68" stroke-width="3"/>'
for y2 in ys:
    b += f'<line x1="166" y1="310" x2="444" y2="{y2}" stroke="#0B6B68" stroke-width="2.5" opacity="0.6"/>'
b += T(108, 320, "W(0)", 30, "700", "#102027", "end")
b += T(1180, 125, "≥ G → V = 1", 30, "700", "#0B6B68", "start") + T(1180, 425, "< G → V = 0", 30, "400", "#64757D", "start")
b += T(300, 60, "행동 = 효율선 위 μ 하나 (15개 중)", 30, "700", "#0B6B68")
b += T(800, 60, "전이 = 로그정규 확률", 30, "700", "#0B6B68")
b += f'<path d="M1100,40 C900,0 700,0 520,40" fill="none" stroke="#C00000" stroke-width="4" stroke-dasharray="12 8" marker-end="url(#ar)"/>'
b += T(1360, 260, "가치를 뒤에서", 30, "700", "#C00000") + T(1360, 300, "앞으로 옮긴다", 30, "700", "#C00000")
b += T(1360, 360, "(Bellman 역산)", 28, "400", "#C00000")
svg_save("s_state", b, W_, H_)

# (S5) 손계산 ① — 자산 100에서 공격형 B로 한 해 (1600×600)
W_, H_ = 1600, 600
Wh = H["W"]
cols = [("다음 자산 W_j", [f"{w:.1f}" for w in Wh]), ("ln(W_j/100)", [f"{np.log(w / 100):+.2f}" for w in Wh]),
        ("z_j", [f"{z:+.3f}" for z in H["zB"]]), ("φ(z_j)", [f"{p:.3f}" for p in H["phiB"]]),
        ("q_j = φ ÷ 합", [f"{q:.3f}" for q in H["qB"]]), ("보수형 A의 q_j", [f"{q:.3f}" for q in H["qA"]])]
cw = 1580 / 6
b = ""
for j, (hd, vals_) in enumerate(cols):
    x = 10 + j * cw
    b += T(x + cw / 2, 60, hd, 28, "700", "#64757D")
    for i_, v in enumerate(vals_):
        y = 100 + i_ * 70
        on = (j == 4 and Wh[i_] >= H["G"])
        if j == 0 and Wh[i_] >= H["G"]:
            b += box(x + 20, y, cw - 40, 56, "lime")
        if on:
            b += box(x + 20, y, cw - 40, 56, "dark")
        b += T(x + cw / 2, y + 40, v, 30, "700" if on or j == 0 else "400", "#B7F34A" if on else "#102027")
b += f'<line x1="10" y1="458" x2="1590" y2="458" stroke="#DDE3E2" stroke-width="2"/>'
sB = sum(q for q, w in zip(H["qB"], Wh) if w >= H["G"]); sA = sum(q for q, w in zip(H["qA"], Wh) if w >= H["G"])
b += T(10 + 3.5 * cw, 505, f"합 {sum(H['phiB']):.3f}", 30, "400", "#64757D")
b += T(800, 570, f"한 해 뒤 목표 칸(≥ {H['G']}) 확률 — 공격형 B {sB:.3f} · 보수형 A {sA:.3f}", 32, "700", "#0B6B68")
svg_save("s_hand1", b, W_, H_)

# (S6) 손계산 ② — 시점 1 표와 시점 0 (1600×620)
W_, H_ = 1600, 620
hd = ["시점 1 자산", "A로 갈 때 E[V(2)]", "B로 갈 때 E[V(2)]", "고른다", "V(·, 1)"]
cw = [300, 340, 340, 260, 300]
xs_ = np.cumsum([10] + cw[:-1])
b = ""
for j, h_ in enumerate(hd):
    b += T(xs_[j] + cw[j] / 2, 54, h_, 28, "700", "#64757D")
for i_ in range(5):
    y = 82 + i_ * 70
    ch = H["c1"][i_]
    row = [f"{Wh[i_]:.1f}", f"{H['E1'][0][i_]:.3f}", f"{H['E1'][1][i_]:.3f}", "A 보수형" if ch == 0 else "B 공격형", f"{H['V1'][i_]:.3f}"]
    if ch == 1:
        b += box(xs_[3] + 20, y, cw[3] - 40, 56, "dark")
    for j, v in enumerate(row):
        hl = (j == 1 and ch == 0) or (j == 2 and ch == 1)
        b += T(xs_[j] + cw[j] / 2, y + 40, v, 30, "700" if hl or j == 3 else "400",
               "#B7F34A" if (j == 3 and ch == 1) else ("#0B6B68" if hl else "#102027"))
b += f'<line x1="10" y1="440" x2="1590" y2="440" stroke="#102027" stroke-width="2"/>'
b += T(10 + 150, 500, "시점 0 · 100", 30, "700")
b += T(xs_[1] + cw[1] / 2, 500, f"{H['E0'][0]:.3f}", 30) + T(xs_[2] + cw[2] / 2, 500, f"{H['E0'][1]:.3f}", 30, "700", "#0B6B68")
b += box(xs_[3] + 20, 460, cw[3] - 40, 56, "dark") + T(xs_[3] + cw[3] / 2, 500, "B 공격형", 30, "700", "#B7F34A")
b += box(xs_[4] + 20, 460, cw[4] - 40, 56, "lime") + T(xs_[4] + cw[4] / 2, 500, f"{max(H['E0']):.3f}", 30, "700", "#071A1D")
b += T(800, 585, f"비교 — 두 해 모두 A 고정 {H['fixedA']:.3f} · 두 해 모두 B 고정 {H['fixedB']:.3f} · 해마다 다시 고르면 {max(H['E0']):.3f}", 30, "700", "#0B6B68")
svg_save("s_hand2", b, W_, H_)

# (S7) 같은 해 목표 조합 30 → 24 → 13 (1600×620)
W_, H_ = 1600, 620
CC = N["y2022_conc"]
b = card(10, 20, 480, 580, "white", "① 조합 30개", ["목표 1 (0 · 7) × 2", "목표 2 (0 · 9 · 20) × 3", "목표 3 (0 · 10 · … · 40) × 5",
                                                  "= 30개의 (비용, 효용)", "예: 7 + 20 + 30 = 57", "→ 효용 100 + 300 + 400"], 32, 28, 64)
b += arrow(496, 300, 556, 300)
b += card(560, 20, 480, 580, "white", "② 정렬 · 같은 비용 정리", ["비용 오름차순으로", "같은 비용이면 효용 큰 것만", "30 → 24칸", "(예: 비용 20 → 300만 남김)"], 32, 28, 70)
b += arrow(1046, 300, 1106, 300)
b += box(1110, 20, 480, 580, "dark") + T(1350, 74, "③ 지배 제거 → 13칸", 32, "700", "#B7F34A")
cs, us = CC["cost"], CC["util"]
for k in range(13):
    y = 128 + k * 36
    b += T(1240, y, f"{cs[k]:.0f}", 26, "400", "#FFFFFF") + T(1460, y, f"{us[k]:.0f}", 26, "400", "#B7F34A")
b += T(1240, 108 - 6, "", 10)
svg_save("s_combine", b, W_, H_)

# (S8) 언제 무엇을 쓰나 — 의사결정 흐름 (1600×500)
W_, H_ = 1600, 500
b = ""
qs = ["목표가 하나인가?", "한 기간 · 계정별 하한인가?", "목표 간 우선순위를 확률로?", "바닥을 규칙으로 보장하려면?"]
outs = [("예 · 여러 기간 → 2020 DP (자산 × 시점 격자)", "white"), ("예 → Das–Markowitz (H, α) → γ", "white"),
        ("예 → EGP 근접점 · 아니면 2022 DP", "lime"), ("→ CPPI · Flexicure (floor + 승수 m)", "dark")]
for k, (q, (t_, kk)) in enumerate(zip(qs, outs)):
    y = 8 + k * 124
    b += box(10, y, 560, 98, "white" if k < 3 else "ghost") + T(290, y + 61, q, 32, "700", "#102027" if k < 3 else "#64757D")
    b += arrow(574, y + 49, 660, y + 49)
    b += box(664, y, 926, 98, kk) + T(1127, y + 61, t_, 31, "700", {"white": "#102027", "lime": "#071A1D", "dark": "#B7F34A"}[kk])
    if k < 3:
        b += f'<line x1="290" y1="{y + 100}" x2="290" y2="{y + 122}" stroke="#0B6B68" stroke-width="4"/>'
svg_save("s_flow", b, W_, H_)

# (S9) 실무 활용 절차 (1600×600)
W_, H_ = 1600, 600
steps = [("① 목표 수집", ["금액 · 시점 · 부분 목표", "원하는 확률"], "white"), ("② 효율선 · 가정", ["자본시장 가정 μ · Σ", "포트폴리오 15개"], "white"),
         ("③ DP 또는 MC", ["DP로 전략 · 확률", "MC로 검증"], "white"), ("④ 확률 대시보드", ["목표별 확률 · 근접점", "효용은 숨긴다"], "white"),
         ("⑤ 매년 재계산", ["자산 · 가정 · 목표 갱신", "전략 표 다시"], "lime")]
b = ""
for k, (t_, ls, kind) in enumerate(steps):
    x = 10 + k * 318
    b += box(x, 30, 290, 330, kind)
    b += T(x + 145, 100, t_, 32, "700", "#071A1D" if kind == "lime" else "#0B6B68")
    for j, l in enumerate(ls):
        b += T(x + 145, 190 + j * 60, l, 27 if len(l) > 10 else 29, "400", "#071A1D" if kind == "lime" else "#102027")
    if k < 4:
        b += arrow(x + 293, 195, x + 315, 195)
b += f'<path d="M1440,364 C1440,440 160,440 160,368" fill="none" stroke="#0B6B68" stroke-width="4" stroke-dasharray="12 8" marker-end="url(#ar)"/>'
b += box(10, 470, 1580, 110, "dark")
b += T(800, 520, "운용팀은 효율선(②), 자문팀은 목표 · 확률(①④)을 맡는다 — 원문 2018 4.5절 · 2020 1절의 '플러그 앤 플레이'", 30, "700", "#B7F34A")
b += T(800, 562, "도구: 2020 DP는 numpy 1초 · 2022 여러 목표는 수 초 · 확률이 목표에 못 미치면 납입 · 목표 · 효용을 고친다", 28, "400", "#FFFFFF")
svg_save("s_pipeline", b, W_, H_)

# (S10) 한국 대입 (1600×500)
W_, H_ = 1600, 500
KO = N["korea"]
b = card(10, 10, 510, 480, "white", "디폴트옵션 · DC", ["위험자산 70% 한도", f"μmax {Y20['mus'][-1] * 100:.2f} → {KO['mu_cap'] * 100:.2f}%",
                                                   f"두 배 확률 {pct(Y20['P200'])} → {pct(KO['P200_cap'])}", "TDF는 나이, DP는 자산도", "케이스 1부 Floor · m"], 33, 30, 70)
b += card(545, 10, 510, 480, "white", "IRP · 목표 계좌형", ["은퇴 · 교육 · 주거 목표", "시점 · 금액 · 부분 목표", "→ 2022 비용 · 효용 벡터",
                                                       "가입자에게는 확률만", "납입 c를 최소로 역산"], 33, 30, 70)
b += card(1080, 10, 510, 480, "dark", "H대 기금 지출 z", ["해마다 지출 = 목표", "4.5%는 완전 목표", "3.5%(175억)는 부분 목표",
                                                    "= Floor(필수 목표)", "비유동 x는 μ · Σ 제약"], 33, 30, 70)
svg_save("s_korea", b, W_, H_)

# (S11) Claude Code 프롬프트 (1600×540)
W_, H_ = 1600, 540
lines = ["너는 목표기반 자산관리 분석가다. numpy만 써서 gbwm_dp.py 하나를 만들고 실행해줘.",
         "[논문] Das · Ostrov · Radhakrishnan · Srivastav (2020) 2절을 그대로 구현한다.",
         "[가정] 기대수익 (0.0493, 0.0770, 0.0886) · 공분산 원문 표 1(0.0309 대칭)",
         "  효율선 위 μ 0.0526 ~ 0.0886 등간격 15개 · W(0) 100 · G 200 · T 10년",
         "  격자: ln W를 σmin/3 간격, Z = ±3으로 끝을 잡고 W(0)이 격자점이 되게",
         "[할 일] ① 전이확률 행 정규화 ② V(T) = 1{W ≥ G}에서 Bellman 역산 ③ 분포 전파",
         "  ④ 고정 비교 ⑤ 번호가 바뀌는 자산 ⑥ C = +1 +3 +5 −1 −5 −10 (파산 처리)",
         "[검증] 약 330칸 · P ≈ 0.666 (원문 0.669) · 시작 μ 0.0835 · C −10 파산 약 12%",
         "  1분 안 · argparse --rho --m --G · 주석 한국어 — 안 맞으면 스스로 고쳐줘"]
b = box(10, 10, 1580, 520, "dark", 14)
for k, l in enumerate(lines):
    col = "#B7F34A" if l.startswith("[") else "#FFFFFF"
    b += T(44, 66 + k * 54, l, 30, "700" if l.startswith("[") else "400", col, "start")
svg_save("s_prompt", b, W_, H_)

# (S12) 실행 결과 — 두 단 (1600×540)
W_, H_ = 1600, 540
out = [l.rstrip().replace("-", "−").replace("(목표가 거의 확실한 구간)", "") for l in open("gbwm_dp_output.txt", encoding="utf-8") if l.strip()]
out = [l for l in out if not (l.startswith("  0번") or l.startswith("효율선"))]
L1 = []
for l in out:
    if l.startswith("기본 예"):
        a_, b_ = l.split(" · 시작"); L1 += [a_, "  시작" + b_]
    elif l.startswith("비교"):
        a_, b_ = l.split(" → "); L1 += [a_, "  → " + b_]
    else:
        L1.append(l)
k_ = next(i for i, l in enumerate(L1) if l.startswith("납입"))
colL, colR = L1[:k_], L1[k_:]
b = box(10, 10, 1580, 520, "ghost", 14) + T(36, 54, "$ python3 gbwm_dp.py", 28, "700", "#0B6B68", "start")
for c, (x0, col) in enumerate([(36, colL), (840, colR)]):
    for k, l in enumerate(col):
        hl = ("기본 예" in l) or ("C = −10" in l) or ("→ DP" in l)
        b += T(x0, 100 + k * 42, l.replace("최적 포트폴리오 번호 — 자산이 적으면 공격적(14번), 많으면 보수적(0번):", "전략 경계 — 적으면 14번 · 많으면 0번:"),
               24, "700" if hl else "400", "#C00000" if "기본 예" in l else "#102027", "start")
svg_save("s_output", b, W_, H_)

# (S13) 한 장 요약 (1600×500)
W_, H_ = 1600, 500
b = ""
cols4 = [("2018 정적", ["효율선 × 등고선", "접점 = 3차식", f"예: {pct(Y18['ogpp'][2])}"], "white"),
         ("2020 동적", ["자산 × 시점 격자", "뒤처지면 공격", f"{pct(Y20['P200'])} vs 고정 {pct(max(Y20['fixed']))}"], "white"),
         ("2022 여러 목표", ["살지 말지 + 투자", "부분 목표 · 효용", "조합을 세지 않는다"], "white"),
         ("2023 EGP", ["확률 프런티어", "근접점 · 최소 자금", f"{E['minW']:.1f} (원문 79.9)"], "lime")]
for k, (t_, ls, kind) in enumerate(cols4):
    x = 10 + k * 398
    b += card(x, 10, 380, 290, kind, t_, ls, 34, 31, 58)
    if k < 3: b += arrow(x + 382, 150, x + 396, 150)
chk = [("위험 = 목표 미달 확률", "σ↓가 늘 안전은 아니다"), ("TDF 대비 (은퇴 예)", f"+{(Y20['retire'][3][1] - Y20['retire'][3][2]) * 100:.0f}%p"),
       ("M8 세 목표", f"9.13 → 약 {N['m8']['minW']:.1f}억")]
for k, (t1, t2) in enumerate(chk):
    x = 10 + k * 530
    b += box(x, 320, 520, 170, "dark" if k == 0 else "ghost")
    b += T(x + 260, 390, t1, 32, "700", "#B7F34A" if k == 0 else "#64757D")
    b += T(x + 260, 450, t2, 32, "700", "#FFFFFF" if k == 0 else "#102027")
svg_save("s_summary", b, W_, H_)

json.dump(R, open("ratios.json", "w"), indent=1, ensure_ascii=False)
print(f"ratios → ratios.json ({len(R)})")
