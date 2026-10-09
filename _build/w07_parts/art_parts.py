# -*- coding: utf-8 -*-
"""W07 강의본 Part I · II 분리 + Q&A 반영(2026-10-09) 그림.

matplotlib 차트와 SVG 인포그래픽(cairosvg로 PNG)을 art/ 에 만든다. 수치는 모두 여기서 다시 계산한다.
실행: .venv/bin/python _build/w07_parts/art_parts.py
"""
import math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "art"); os.makedirs(OUT, exist_ok=True)
FONT = os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc")
fm.fontManager.addfont(FONT)
plt.rcParams["font.family"] = fm.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"
NAVY, GRAY, ORANGE, GREEN, RED, BLUE = "#1B2C5E", "#9AA3AF", "#E8A04C", "#2E9E6B", "#C0392B", "#3B6FB6"
LB, LG, LR = "#EAF1FB", "#E6F5F0", "#FBEAEA"
N = lambda x: 0.5 * (1 + math.erf(x / 2 ** 0.5))


def clean(ax, grid="y"):
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_color(GRAY)
    if grid: ax.grid(axis=grid, color="#E5E7EB", lw=0.8); ax.set_axisbelow(True)
    ax.tick_params(colors="#374151", labelsize=11)


def save(fig, name):
    p = os.path.join(OUT, name); fig.savefig(p, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.08); plt.close(fig); print(p)


def svg(name, w, h, body):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'font-family="Noto Sans CJK KR">'
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker>'
         '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
         '<marker id="arg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker></defs>'
         f'<rect width="{w}" height="{h}" fill="white"/>{body}</svg>')
    p = os.path.join(OUT, name)
    cairosvg.svg2png(bytestring=s.encode(), write_to=p, output_width=w * 2, output_height=h * 2)
    open(p.replace(".png", ".svg"), "w").write(s); print(p)


def box(x, y, w, h, fill, stroke, rx=10, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=18, fill=NAVY, weight="normal", anchor="middle"):
    size = round(size * 1.12, 1)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def arrow(x1, y1, x2, y2, col=NAVY, sw=2.5, m="ar", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}" marker-end="url(#{m})"{d}/>'


# ── 1 손실 확률 — 연환산 로그 수익률의 분포가 좁아진다 ───────────────────────
def loss_prob():
    mu, s = 0.07, 0.16; m = mu - s * s / 2
    x = np.linspace(-0.45, 0.55, 800)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    for T, c in ((1, RED), (10, ORANGE), (30, GREEN)):
        sd = s / math.sqrt(T); y = np.exp(-(x - m) ** 2 / (2 * sd * sd)) / (sd * math.sqrt(2 * math.pi))
        p = N(-m * math.sqrt(T) / s)
        ax.plot(x, y, color=c, lw=2.2, label=f"{T}년 — 손실 확률 {p*100:.1f}%")
        ax.fill_between(x, 0, y, where=x < 0, color=c, alpha=.22)
    ax.axvline(0, color=NAVY, lw=1.2, ls="--"); ax.text(-0.012, ax.get_ylim()[1] * .55, "손실 경계 (0)", fontsize=10, color=NAVY, ha="right")
    ax.axvline(m, color=GRAY, lw=1); ax.text(m + .008, ax.get_ylim()[1] * .45, f"m = μ − σ²/2 = {m*100:.2f}%", fontsize=10, color="#374151")
    ax.set_xlabel("연환산 로그 수익률  R_T / T  ~  N(m, σ²/T)", fontsize=11)
    ax.set_yticks([]); clean(ax, grid=None); ax.spines["left"].set_visible(False)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v*100:.0f}%"))
    ax.legend(frameon=False, fontsize=10.5, loc="upper right")
    save(fig, "loss_prob.png")


# ── 2 동적 계획법 — 뒤에서부터 같은 문제 ─────────────────────────────────
def dp_backward():
    W, H = 1160, 190; b = ""
    labels = [("0기", "x* = 59.9%"), ("1기", "x* = 59.9%"), ("…", ""), ("T−1기", "x* = 59.9%"), ("T (종점)", "V_T = U(W)")]
    xs = [30, 260, 490, 640, 890]; ws = [200, 200, 120, 220, 240]
    for (a, c), x, w in zip(labels, xs, ws):
        fill, st = (LG, GREEN) if a.startswith("T (") else (LB, BLUE)
        if a == "…":
            b += txt(x + w / 2, 95, "…", 34, GRAY); continue
        b += box(x, 40, w, 100, fill, st)
        b += txt(x + w / 2, 80, a, 22, NAVY, "bold") + txt(x + w / 2, 115, c, 18, "#374151")
    for x1, x2 in ((890, 862), (640, 612), (490, 462), (260, 232)):
        b += arrow(x1, 158, x2, 158, RED, 2.5, "arr")
    b += txt(560, 185, "← 종점에서 한 칸씩 거슬러 올라가며 푼다 · 매 칸이 W와 무관한 같은 1기간 문제", 16, RED)
    b += txt(560, 26, "CRRA : V_t(W) = a_t · U(W) — 가치함수의 모양이 매기 같다 → 상수 a_t만 바뀌고 x*는 그대로", 16, NAVY, "bold")
    svg("dp_backward.png", W, H, b)


# ── 3 리밸런싱 = 변동성 매도 (두 패널) ─────────────────────────────────
def rebal_short():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.6, 3.7), gridspec_kw={"width_ratios": [1.05, 1]})
    # (a) 만기 부 — 1년, x = 60%, r = 3%, σ = 16% 연속 리밸런싱(정확 해)
    x, r, s, T = .6, .03, .18, 10.0
    R = np.linspace(.25, 4.2, 400)           # 주가 총수익 S_T/S_0 (10년)
    bh = x * R + (1 - x) * math.exp(r * T)
    cm = R ** x * math.exp((1 - x) * (r + x * s * s / 2) * T)
    a1.plot(R, bh, color=GRAY, lw=2.2, label="매수후보유 — 직선")
    a1.plot(R, cm, color=NAVY, lw=2.6, label="리밸런싱 — 오목")
    a1.fill_between(R, bh, cm, where=cm >= bh, color=GREEN, alpha=.25)
    a1.fill_between(R, bh, cm, where=cm < bh, color=RED, alpha=.18)
    lo, hi = R[np.argmax(cm >= bh)], R[len(R) - 1 - np.argmax((cm >= bh)[::-1])]
    a1.text(1.6, .55, "중간(제자리~완만한 상승)\n리밸런싱이 더 남긴다", ha="center", fontsize=10.5, color=GREEN)
    a1.text(.3, 1.35, "크게 하락", fontsize=10, color=RED); a1.text(3.4, 2.15, "크게 상승", fontsize=10, color=RED)
    a1.set_xlabel("10년 뒤 주가 (처음 = 1) · σ 18% · r 3% · 주식 60%", fontsize=10.5); a1.set_ylabel("10년 뒤 부 (처음 = 1)", fontsize=11)
    a1.set_title("(가) 만기 부 — 큰 움직임에서 덜 남기는 대신 횡보에서 더 번다", fontsize=12, color=NAVY, loc="left")
    a1.legend(frameon=False, fontsize=10, loc="upper left"); clean(a1)
    # (나) 두 경로
    def run(path):
        S = np.cumprod(np.r_[1, path]); b = 1.03 ** (1 / 12)
        bh = x * S + (1 - x) * b ** np.arange(len(S)); w = [1.0]
        for g in path: w.append(w[-1] * (x * g + (1 - x) * b))
        return S, np.array(w) / bh - 1
    side = [1.15, 1 / 1.15] * 6; trend = [1.04] * 12
    for path, c, lab in ((side, GREEN, "횡보 — 오르내리다 제자리"), (trend, RED, "추세 — 한 방향으로 상승")):
        S, d = run(path); a2.plot(range(13), d * 100, color=c, lw=2.4, marker="o", ms=3.5, label=lab)
    a2.axhline(0, color=GRAY, lw=1)
    a2.set_xlabel("개월", fontsize=11); a2.set_ylabel("리밸런싱 − 매수후보유 (%)", fontsize=11)
    a2.set_title("(나) 경로가 갈라놓는다 — 횡보에서 벌고 추세에서 잃는다", fontsize=12, color=NAVY, loc="left")
    a2.legend(frameon=False, fontsize=10, loc="lower left"); clean(a2)
    fig.tight_layout(); save(fig, "rebal_short.png")


# ── 4 모두가 리밸런싱하면 — 오목한 쪽과 볼록한 쪽 ─────────────────────────
def everyone():
    W, H = 600, 330; b = ""
    b += box(15, 30, 250, 220, LB, BLUE) + box(335, 30, 250, 220, LR, RED)
    b += txt(140, 62, "오목한 전략", 21, NAVY, "bold") + txt(140, 88, "내리면 산다 · 변동성 매도", 15, "#374151")
    for i, s in enumerate(["고정 비중 리밸런싱", "연기금 · 국부펀드", "가치 투자자"]):
        b += txt(140, 128 + i * 34, "· " + s, 17, NAVY)
    b += txt(460, 62, "볼록한 전략", 21, RED, "bold") + txt(460, 88, "내리면 판다 · 변동성 매수", 15, "#374151")
    for i, s in enumerate(["CPPI · 포트폴리오 보험", "추세추종(CTA)", "마진콜 · 손절 매도"]):
        b += txt(460, 128 + i * 34, "· " + s, 17, RED)
    b += arrow(268, 115, 330, 115, GREEN, 3, "arg") + txt(300, 105, "산다", 14, GREEN, "bold")
    b += arrow(332, 180, 270, 180, RED, 3, "arr") + txt(300, 172, "판다", 14, RED, "bold")
    b += txt(300, 285, "하락장 — 볼록한 쪽이 판 주식을 오목한 쪽이 받는다", 17, NAVY, "bold")
    b += txt(300, 312, "모두가 오목하면 거래 상대가 없다 → 가격이 대신 움직이고 보너스는 사라진다", 14.5, "#374151")
    svg("everyone.png", W, H, b)


# ── 5 확실성등가 차이 vs γ ───────────────────────────────────────────
def ce_gamma():
    def W2(reb, x=.6):
        out = []
        for a in (2, .5):
            for c in (2, .5):
                out.append((x * a + (1 - x) * 1.1) * (x * c + (1 - x) * 1.1) if reb else x * a * c + (1 - x) * 1.21)
        return np.array(out)
    def CE(w, g): return (np.mean(w ** (1 - g))) ** (1 / (1 - g))
    gs = [0.3, 0.51, 1.5, 3, 5]; v = [(CE(W2(1), g) / CE(W2(0), g) - 1) * 100 for g in gs]
    fig, ax = plt.subplots(figsize=(5.6, 3.3))
    cols = [GREEN if t > 0 else RED for t in v]; cols[1] = NAVY
    bars = ax.bar([f"γ = {g}" for g in gs], v, color=cols, width=.6)
    for bb, t in zip(bars, v):
        ax.text(bb.get_x() + bb.get_width() / 2, t + (0.35 if t > 0 else -0.35), f"{t:+.2f}%", ha="center",
                va="bottom" if t > 0 else "top", fontsize=11, color=NAVY if t > 0 else RED, fontweight="bold")
    ax.axhline(0, color=GRAY, lw=1); ax.set_ylim(-13, 3)
    ax.set_ylabel("CE 차이 (리밸런싱 − 보유)", fontsize=10.5); clean(ax)
    ax.set_title("같은 60:40 리밸런싱 — 그 비중이 최적인 γ = 0.51에게만 이득", fontsize=11.5, color=NAVY, loc="left")
    save(fig, "ce_gamma.png")


# ── 6 Kelly — 성장률과 γ = 4의 확실성등가 ────────────────────────────────
def kelly_curves():
    mu, r, s = .07, .03, .16; x = np.linspace(0, 3.2, 400)
    g = r + x * (mu - r) - .5 * x * x * s * s
    c4 = r + x * (mu - r) - 2 * x * x * s * s
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ax.plot(x * 100, g * 100, color=NAVY, lw=2.5, label="로그 성장률 g(x) — Kelly가 최대화")
    ax.plot(x * 100, c4 * 100, color=RED, lw=2.5, label="γ = 4 투자자의 확실성등가 CE(x)")
    xk, x4 = (mu - r) / s ** 2, (mu - r) / (4 * s ** 2)
    ax.scatter([xk * 100], [(r + xk * (mu - r) - .5 * xk * xk * s * s) * 100], color=NAVY, zorder=3, s=40)
    ax.scatter([xk * 100], [(r + xk * (mu - r) - 2 * xk * xk * s * s) * 100], color=RED, zorder=3, s=40)
    ax.scatter([x4 * 100], [(r + x4 * (mu - r) - 2 * x4 * x4 * s * s) * 100], color=RED, zorder=3, s=40)
    ax.annotate("Kelly 156%\ng 6.13%", (xk * 100, 6.13), (190, 7.1), fontsize=10, color=NAVY, arrowprops=dict(arrowstyle="-", color=NAVY))
    ax.annotate("γ = 4 최적 39%\nCE 3.78%", (x4 * 100, 3.78), (60, 0.2), fontsize=10, color=RED, arrowprops=dict(arrowstyle="-", color=RED))
    ax.annotate("Kelly를 γ = 4가 들면\nCE −3.25%", (xk * 100, -3.25), (190, -6.5), fontsize=10, color=RED, arrowprops=dict(arrowstyle="-", color=RED))
    ax.axhline(0, color=GRAY, lw=1); ax.set_ylim(-9, 9)
    ax.set_xlabel("주식 비중 x (%)", fontsize=11); ax.set_ylabel("연율 (%)", fontsize=11)
    ax.legend(frameon=False, fontsize=9.5, loc="lower left"); clean(ax)
    save(fig, "kelly_curves.png")


def kelly_prob():
    mu, r, s = .07, .03, .16; xk, x4 = 1.5625, .390625
    gk = r + xk * (mu - r) - .5 * xk * xk * s * s; g4 = r + x4 * (mu - r) - .5 * x4 * x4 * s * s
    T = np.linspace(1, 200, 300); p = [N((gk - g4) * math.sqrt(t) / ((xk - x4) * s)) for t in T]
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(T, np.array(p) * 100, color=NAVY, lw=2.5)
    for t in (10, 30, 100):
        v = N((gk - g4) * math.sqrt(t) / ((xk - x4) * s)) * 100
        ax.scatter([t], [v], color=ORANGE, zorder=3); ax.text(t + 3, v - 6, f"{t}년 {v:.0f}%", fontsize=10.5, color=NAVY)
    ax.set_ylim(40, 100); ax.set_xlabel("투자 기간 T (년)", fontsize=11); ax.set_ylabel("Kelly 부 > 39% 부일 확률 (%)", fontsize=10)
    ax.set_title("확률로는 Kelly가 거의 확실히 이긴다", fontsize=11.5, color=NAVY, loc="left"); clean(ax)
    save(fig, "kelly_prob.png")


# ── 7 To vs Through ─────────────────────────────────────────────────
def to_through():
    age = np.arange(25, 91)
    to = np.where(age < 60, 70 - (70 - 20) * np.clip((age - 25) / 35, 0, 1) ** 1.6, 20)
    th = np.where(age < 60, 90 - (90 - 50) * np.clip((age - 25) / 35, 0, 1) ** 1.8,
                  np.maximum(30, 50 - (age - 60) * 20 / 7))
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.plot(age, th, color=BLUE, lw=2.6, label="Through — B부장 (나눠 쓴다)")
    ax.plot(age, to, color=ORANGE, lw=2.6, label="To — A부장 (목돈으로 꺼낸다)")
    ax.axvline(60, color=GRAY, ls="--", lw=1.2); ax.text(60.5, 92, "은퇴 60세", fontsize=10, color="#374151")
    ax.axvspan(58, 60, color=ORANGE, alpha=.15); ax.text(33, 8, "A부장의 위험: 은퇴 직전 1~2년의 폭락", fontsize=9.5, color=ORANGE)
    ax.axvspan(60, 85, color=BLUE, alpha=.06); ax.text(61.5, 40, "B부장의 위험:\n오래 사는데 돈이 먼저 바닥", fontsize=9.5, color=BLUE)
    ax.set_ylim(0, 100); ax.set_xlabel("나이", fontsize=11); ax.set_ylabel("주식 비중 (%)", fontsize=11)
    ax.legend(frameon=False, fontsize=10, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2); clean(ax)
    save(fig, "to_through.png")


# ── 8 기관의 인적자본 — H/F가 줄 때 금융자산의 주식 비중 ─────────────────────
def hf_wf():
    h = np.linspace(2.0, 0, 200); ws = .30
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for bH, c, lab in ((0, BLUE, "채권형 H (β_H = 0) — 하향 경로"), (.5, RED, "주식형 H (β_H = 0.5) — 상향 경로")):
        wf = np.clip(ws * (1 + h) - bH * h, 0, 1) * 100
        ax.plot(h, wf, color=c, lw=2.6, label=lab)
    ax.invert_xaxis(); ax.set_xlabel("H / F  (미래 유입의 현재가치 ÷ 적립금) — 오른쪽으로 갈수록 ‘나이 든’ 기금", fontsize=9.5)
    ax.set_ylabel("금융자산의 주식 비중 (%)", fontsize=10.5); ax.set_ylim(0, 100)
    ax.text(1.95, 4, "총부 기준 목표 w* = 30%", fontsize=10, color="#374151")
    ax.legend(frameon=False, fontsize=10, loc="upper right"); clean(ax)
    save(fig, "hf_wf.png")


# ── 9 톱니 소비 — 바닥과 잉여 ───────────────────────────────────────────
def ratchet():
    W, H = 1160, 330; b = ""
    def stack(x, title, parts, note):
        out = txt(x + 110, 28, title, 18, NAVY, "bold"); y = 50; sc = 1.9
        for v, lab, fill, st in parts:
            hh = v * sc
            out += box(x, y, 220, hh, fill, st, rx=4) + txt(x + 110, y + hh / 2 + 6, lab, 15, NAVY if fill != RED else "white", "bold")
            y += hh
        return out + txt(x + 110, y + 24, note, 14, "#374151")
    b += stack(30, "① 지금 — 부 100", [(25, "잉여 25", LG, GREEN), (75, "바닥 75 = TIPS", LB, BLUE)], "연 소비 1.5 ÷ 실질금리 2% = 75")
    b += stack(330, "② 주식 노출 = 2 × 잉여", [(50, "주식 50 (잉여 25 + 차입 25)", "#FCEBD9", ORANGE), (75, "TIPS 75", LB, BLUE)], "m = 2 — ‘레버리지 주식’")
    b += stack(630, "③ 주가 반 토막", [(0.01, "", LG, GREEN), (75, "TIPS 75 — 바닥은 그대로", LB, BLUE)], "주식 25 − 차입 25 = 잉여 0 · 소비 1.5 유지")
    b += stack(930, "④ 주가 상승 → 톱니", [(30, "잉여 30", LG, GREEN), (90, "새 바닥 90 (소비 1.8)", LB, BLUE)], "바닥 = 지금까지의 최고 소비(최댓값)")
    for x in (258, 558, 858):
        b += arrow(x, 150, x + 66, 150, NAVY, 2.5)
    svg("ratchet.png", W, H, b)


# ── 10 GP — 조준점의 가중치 ─────────────────────────────────────────────
def gp_aim():
    tau = np.arange(0, 12)
    fast, slow = 100 * .5 ** tau, 100 * .95 ** tau
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.bar(tau - .2, fast, width=.4, color=RED, alpha=.8, label="빠른 신호의 미래 목표 (φ 0.5)")
    ax.bar(tau + .2, slow, width=.4, color=BLUE, alpha=.8, label="느린 신호의 미래 목표 (φ 0.05)")
    ax.axhline(66.7, color=RED, ls="--", lw=1.6); ax.text(11.6, 69, "조준점 반영 0.667", fontsize=10, color=RED, ha="right")
    ax.axhline(95.2, color=BLUE, ls="--", lw=1.6); ax.text(11.6, 98, "조준점 반영 0.952", fontsize=10, color=BLUE, ha="right")
    ax.set_xlabel("τ 기 뒤", fontsize=11); ax.set_ylabel("신호가 가리키는 목표", fontsize=10.5); ax.set_ylim(0, 150)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right"); clean(ax)
    save(fig, "gp_aim.png")


def gp_path():
    fa = fs = 100.; x = 0; T = 10; tg, am, gp = [], [], []
    for t in range(T):
        tgt = fa + fs; aim = fa / 1.5 + fs / 1.05; x = x + .5 * (aim - x)
        tg.append(tgt); am.append(aim); gp.append(x); fa *= .5; fs *= .95
    t = np.arange(1, T + 1)
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.plot(t, tg, color=GRAY, lw=2.4, marker="o", ms=4, label="비용 무시 목표 = 목표 추종의 보유")
    ax.plot(t, am, color=ORANGE, lw=2, ls="--", label="GP 조준점")
    ax.plot(t, gp, color=NAVY, lw=2.6, marker="s", ms=4, label="GP 보유")
    ax.annotate("1기 +200 사고\n2기 55 판다", (2, 145), (3.2, 175), fontsize=10, color="#374151", arrowprops=dict(arrowstyle="-", color=GRAY))
    ax.annotate("1기 81만 사고\n2기 21 더 산다", (2, 102.4), (3.6, 55), fontsize=10, color=NAVY, arrowprops=dict(arrowstyle="-", color=NAVY))
    ax.set_xlabel("기간", fontsize=11); ax.set_ylabel("포지션", fontsize=11); ax.set_ylim(0, 215)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right"); clean(ax)
    save(fig, "gp_path.png")


# ── 11 CRRA vs 손실 회피 ──────────────────────────────────────────────
def utility_shapes():
    z = np.linspace(-.3, .3, 400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
    W = 1 + z
    for g, c in ((2, BLUE), (5, NAVY)):
        u = (W ** (1 - g) - 1) / (1 - g); a1.plot(z * 100, u, color=c, lw=2.3, label=f"CRRA γ = {g}")
    a1.set_title("CRRA — 부 전체를 매끈하게", fontsize=11.5, color=NAVY, loc="left")
    a1.set_xlabel("수익률 (%)", fontsize=10); a1.legend(frameon=False, fontsize=9.5); clean(a1); a1.axvline(0, color=GRAY, lw=.8)
    v = np.where(z >= 0, np.abs(z) ** .88, -2.25 * np.abs(z) ** .88)
    a2.plot(z * 100, v, color=RED, lw=2.5); a2.axvline(0, color=GRAY, lw=.8); a2.axhline(0, color=GRAY, lw=.8)
    a2.annotate("기준점(원금)에서 꺾인다", (0, 0), (3, -.55), fontsize=10, color=RED, arrowprops=dict(arrowstyle="-", color=RED))
    a2.text(-29, .2, "손실은 2.25배 무겁게", fontsize=10, color=RED)
    a2.set_title("손실 회피 — 기준점 대비 이익 · 손실", fontsize=11.5, color=NAVY, loc="left"); a2.set_xlabel("수익률 (%)", fontsize=10); clean(a2)
    fig.tight_layout(); save(fig, "utility_shapes.png")


# ── 12 SmartNest 흐름 ───────────────────────────────────────────────
def smartnest():
    W, H = 1160, 250; b = ""
    b += box(10, 40, 280, 170, LB, BLUE) + txt(150, 72, "입력 — 사람마다 다르다", 18, NAVY, "bold")
    for i, s in enumerate(["희망 은퇴 소득 · 최소 소득", "다른 소득원(공적연금 · DB)", "현재 급여 · 급여 변화"]):
        b += txt(150, 110 + i * 32, s, 15.5, "#374151")
    b += arrow(295, 125, 360, 125)
    b += box(365, 55, 300, 140, "#FCEBD9", ORANGE) + txt(515, 92, "목표 = 은퇴 후 실질 연금 소득", 17, NAVY, "bold")
    b += txt(515, 128, "그 소득을 사는 값 = 개인의 ‘부채’", 15.5, "#374151") + txt(515, 160, "(은퇴 날짜가 아니라 소득을 목표로)", 14, GRAY)
    b += arrow(670, 100, 760, 70) + arrow(670, 150, 760, 180)
    b += box(765, 25, 385, 90, LG, GREEN) + txt(957, 58, "장기 TIPS — 부채 헤지", 17, NAVY, "bold")
    b += txt(957, 90, "은퇴가 가까울수록 늘린다 · 개인용 LDI", 14.5, "#374151")
    b += box(765, 135, 385, 90, LB, BLUE) + txt(957, 168, "글로벌 주식 — 희망 포트폴리오", 17, NAVY, "bold")
    b += txt(957, 200, "젊을 때 최대 98% · 위협받으면 CPPI로 보호", 14.5, "#374151")
    b += txt(580, 240, "TDF는 출생연도만 보고 같은 경로 — SmartNest는 소득 목표 · 다른 연금 · 급여로 사람마다 다른 경로", 15, NAVY)
    svg("smartnest.png", W, H, b)


# ── 13 세 안의 위험자산 비중 경로 ───────────────────────────────────────
def derisk():
    yrs = np.arange(2026, 2076)
    A = np.full(len(yrs), 65.0)
    B = np.array([65 if y < 2042 else max(50, 65 - (y - 2041)) for y in yrs], float)
    C = np.array([65 if y < 2027 else max(45, 65 - (y - 2026)) for y in yrs], float)
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.plot(yrs, A, color=GRAY, lw=2.5, label="A 감축 없음 — 65% 유지")
    ax.plot(yrs, B, color=NAVY, lw=2.8, label="B 트리거형 — 2042년부터 연 1%p, 50%에서 멈춤")
    ax.plot(yrs, C, color=RED, lw=2.5, label="C 즉시 감축 — 2027년부터 연 1%p, 45%에서 멈춤")
    ax.axvline(2042, color=ORANGE, ls="--", lw=1.4); ax.text(2042.5, 56, "H/F < 0.625 (2042)", fontsize=10, color=ORANGE)
    ax.axvline(2037, color=GRAY, ls=":", lw=1.2); ax.text(2036.5, 69.5, "순유출 2037", fontsize=9.5, color="#374151", ha="right")
    ax.set_ylim(28, 72); ax.set_ylabel("위험자산 비중 (%)", fontsize=10.5)
    ax.legend(frameon=False, fontsize=9.3, loc="lower left"); clean(ax)
    save(fig, "derisk.png")


# ── 14 헤징 수요의 인과 사슬 ───────────────────────────────────────────
def hedge_chain():
    W, H = 1160, 210; b = ""
    b += box(10, 60, 230, 90, LB, BLUE) + txt(125, 98, "10년 금리 하락", 19, NAVY, "bold") + txt(125, 128, "상태변수 x가 움직인다", 14, "#374151")
    b += arrow(245, 85, 330, 45) + arrow(245, 125, 330, 165)
    b += box(335, 5, 380, 80, LR, RED) + txt(525, 38, "앞으로 재투자 수익이 낮아진다", 17, RED, "bold") + txt(525, 66, "미래 투자 기회 악화 (b > 0)", 14, "#374151")
    b += box(335, 125, 380, 80, LG, GREEN) + txt(525, 158, "바로 그때 장기 국채 값이 오른다", 17, GREEN, "bold") + txt(525, 186, "헤지 자산과 x의 상관 ρ < 0", 14, "#374151")
    b += arrow(720, 45, 800, 95) + arrow(720, 165, 800, 115)
    b += box(805, 50, 345, 110, "#FCEBD9", ORANGE) + txt(977, 88, "장기 국채 = 나쁜 미래에", 18, NAVY, "bold")
    b += txt(977, 115, "돈을 주는 보험", 18, NAVY, "bold") + txt(977, 143, "→ 단기 최적보다 더 담는다 (γ > 1)", 14, "#374151")
    svg("hedge_chain.png", W, H, b)


# ── 15 네 겹 — LH · SAA · TAA · OPP ───────────────────────────────────
def layers():
    W, H = 560, 300; b = ""
    rows = [("헤징 수요 (OPP)", "(1 − 1/γ) β_z — 미래 기회 헤지", "#FCEBD9", ORANGE),
            ("전술 (TAA)", "(1/γ)(μ_t − μ̄)/σ² — 지금의 조건", LB, BLUE),
            ("전략 (SAA)", "(1/γ)(μ̄ − r)/σ² — 장기 평균", LB, BLUE),
            ("부채 헤지 (LH)", "(1 − 1/γ) β_L — W6 LDI", LG, GREEN)]
    for i, (a, c, f, s) in enumerate(rows):
        y = 10 + i * 66
        b += box(10, y, 540, 58, f, s, rx=6) + txt(28, y + 25, a, 17, NAVY, "bold", anchor="start") + txt(28, y + 48, c, 14, "#374151", anchor="start")
    b += txt(280, 292, "아래에서 위로 — 지급 의무 → 프리미엄 → 기회 (실무 순서)", 14, NAVY)
    svg("layers.png", W, H, b)


# ── Kelly 부록 그림 ──────────────────────────────────────────────────
def kelly_discrete():
    f = np.linspace(0, .5, 300); G = .6 * np.log(1 + f) + .4 * np.log(1 - f)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(f * 100, G * 100, color=NAVY, lw=2.5); ax.axhline(0, color=GRAY, lw=1)
    ax.scatter([20], [(.6 * math.log(1.2) + .4 * math.log(.8)) * 100], color=GREEN, zorder=3, s=40)
    ax.annotate("켈리 f* = 20%\nG = 2.0%/판", (20, 2.01), (27, 2.3), fontsize=10, color=GREEN, arrowprops=dict(arrowstyle="-", color=GREEN))
    ax.annotate("2배(40%) 걸면 성장 0", (40, 0), (25, -1.6), fontsize=10, color=RED, arrowprops=dict(arrowstyle="-", color=RED))
    ax.set_xlabel("건 비율 f (%)", fontsize=11); ax.set_ylabel("판당 로그 성장률 G (%)", fontsize=10); ax.set_ylim(-3, 3)
    ax.set_title("승률 60% · 이기면 +100% · 지면 −100%", fontsize=11, color=NAVY, loc="left"); clean(ax)
    save(fig, "kelly_discrete.png")


def kelly_drag():
    mu, r, s = .10, 0, .20; f = np.linspace(0, 5, 300)
    gain, drag = f * (mu - r), .5 * f * f * s * s
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(f * 100, gain * 100, color=GREEN, lw=2.2, label="수익 f(μ − r) — 직선")
    ax.plot(f * 100, drag * 100, color=RED, lw=2.2, label="드래그 ½f²σ² — 제곱")
    ax.plot(f * 100, (gain - drag) * 100, color=NAVY, lw=2.8, label="성장률 g(f)")
    ax.axvline(250, color=GRAY, ls="--", lw=1.2); ax.text(255, 41, "f* = (μ−r)/σ² = 250%", fontsize=10, color=NAVY)
    ax.set_xlabel("비중 f (%)", fontsize=11); ax.set_ylabel("연율 (%)", fontsize=11); ax.set_ylim(-5, 50)
    ax.set_title("μ − r = 10%, σ = 20%", fontsize=11, color=NAVY, loc="left")
    ax.legend(frameon=False, fontsize=9.5, loc="upper left"); clean(ax)
    save(fig, "kelly_drag.png")


def kelly_fraction():
    c = np.linspace(0, 2.2, 300)
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(c, (2 * c - c * c) * 100, color=NAVY, lw=2.6, label="초과 성장률 (켈리 대비) = 2c − c²")
    ax.plot(c, c * c * 100, color=RED, lw=2.2, ls="--", label="로그 부 분산 (켈리 대비) = c²")
    for cc, lab in ((.25, "쿼터"), (.5, "하프"), (1, "풀"), (2, "2배")):
        ax.scatter([cc], [(2 * cc - cc * cc) * 100], color=ORANGE, zorder=3)
        ax.text(cc - .14, (2 * cc - cc * cc) * 100 + 6, lab, fontsize=10, color=NAVY)
    ax.set_ylim(0, 160); ax.set_xlabel("켈리 분수 c = 1/γ", fontsize=11); ax.set_ylabel("%", fontsize=11)
    ax.legend(frameon=False, fontsize=9.3, loc="upper left"); clean(ax)
    save(fig, "kelly_fraction.png")


def kelly_skew():
    f = np.linspace(0, 1.95, 400)
    gn = f * .06 - .5 * f * f * .04
    gs = .887 * np.log(1 + .131 * f) + .113 * np.log(np.maximum(1 - .5 * f, 1e-9))
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(f * 100, gn * 100, color=NAVY, lw=2.5, label="정규 — 평균 · 분산만")
    ax.plot(f * 100, gs * 100, color=RED, lw=2.5, label="2점 분포 — −50% 폭락 11.3%")
    ax.axvline(150, color=NAVY, ls="--", lw=1.1); ax.axvline(91, color=RED, ls="--", lw=1.1)
    ax.text(152, -1.6, "150%", fontsize=10, color=NAVY); ax.text(60, -1.6, "91%", fontsize=10, color=RED)
    ax.set_ylim(-2, 5.2); ax.set_xlabel("비중 f (%)", fontsize=11); ax.set_ylabel("기대 로그 성장률 (%)", fontsize=10)
    ax.set_title("평균 6% · 표준편차 20% · 샤프 0.3은 같다", fontsize=11, color=NAVY, loc="left")
    ax.legend(frameon=False, fontsize=9.5, loc="upper left"); clean(ax)
    save(fig, "kelly_skew.png")


# ── 무거래 구간 — 목표 주변의 띠 ─────────────────────────────────────
def nt_band():
    rng = np.random.default_rng(7); n = 120; tgt, hw = .60, .03
    r = rng.normal(.006, .045, n)
    free, band, trades = [tgt], [tgt], []
    for t, g in enumerate(r, 1):
        f = free[-1] * (1 + g) / (free[-1] * (1 + g) + (1 - free[-1]) * 1.002); free.append(f)
        b = band[-1] * (1 + g) / (band[-1] * (1 + g) + (1 - band[-1]) * 1.002)
        if b > tgt + hw: trades.append((t, b, tgt + hw)); b = tgt + hw
        elif b < tgt - hw: trades.append((t, b, tgt - hw)); b = tgt - hw
        band.append(b)
    x = np.arange(n + 1)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.axhspan((tgt - hw) * 100, (tgt + hw) * 100, color=GREEN, alpha=.13)
    ax.axhline(tgt * 100, color=GREEN, lw=1.5, ls="--")
    ax.plot(x, np.array(free) * 100, color=GRAY, lw=1.6, label="그냥 두면 — 비중이 표류")
    ax.plot(x, np.array(band) * 100, color=NAVY, lw=2.3, label="무거래 구간 — 띠 안에선 가만히")
    for t, a, b in trades:
        ax.annotate("", (t, b * 100), (t, a * 100), arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.scatter([t for t, _, _ in trades], [b * 100 for _, _, b in trades], color=RED, s=14, zorder=4, label="띠를 벗어난 순간 — 경계까지만 거래")
    ax.annotate("", (3, (tgt + hw) * 100), (3, tgt * 100), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
    ax.text(4.5, (tgt + hw / 2) * 100 - .4, "반폭 3%p", fontsize=10.5, color=GREEN, fontweight="bold")
    ax.text(n - 1, tgt * 100 + .5, "목표 60%", fontsize=10, color=GREEN, ha="right")
    ax.set_xlabel("개월 (모의 경로)", fontsize=11); ax.set_ylabel("주식 비중 (%)", fontsize=11)
    ax.legend(frameon=False, fontsize=9.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2); clean(ax)
    save(fig, "nt_band.png")


# ── 세 가지 대응 — 매번 맞추기 · 고정 · 조금씩 ─────────────────────────────
def three_ways():
    rng = np.random.default_rng(3); T = 24
    tgt = np.clip(60 + np.cumsum(rng.normal(0, 4, T)) * .6 + rng.normal(0, 5, T), 35, 85)
    a = tgt.copy(); b = np.full(T, 60.0); c = np.zeros(T); x = 60.0
    for t in range(T): x = x + .35 * (tgt[t] - x); c[t] = x
    n = lambda v: int((np.abs(np.diff(np.r_[60, v])) > .5).sum())
    t = np.arange(1, T + 1)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(t, tgt, color=GRAY, lw=1.4, ls="--", marker="o", ms=3, label="목표 비중 (예측이 바뀔 때마다 이동)")
    ax.step(t, a, where="mid", color=RED, lw=2.0, label=f"① 매번 목표로 — 거래 {n(a)}번, 거래량 큼")
    ax.plot(t, b, color=BLUE, lw=2.4, label="② 비중 고정 — 거래 0번, 예측 무시")
    ax.plot(t, c, color=NAVY, lw=2.6, label="③ 조금씩 옮기기 — 거래량 작음")
    ax.set_xlabel("기간", fontsize=11); ax.set_ylabel("주식 비중 (%)", fontsize=11); ax.set_ylim(25, 100)
    ax.legend(frameon=False, fontsize=9.3, loc="upper left", ncol=1); clean(ax)
    save(fig, "three_ways.png")


if __name__ == "__main__":
    for fn in (loss_prob, dp_backward, rebal_short, everyone, ce_gamma, kelly_curves, kelly_prob, to_through, hf_wf, ratchet,
               gp_aim, gp_path, utility_shapes, smartnest, derisk, hedge_chain, layers,
               kelly_discrete, kelly_drag, kelly_fraction, kelly_skew, nt_band, three_ways):
        fn()
