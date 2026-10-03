# -*- coding: utf-8 -*-
"""보충교재 16 — Gârleanu–Pedersen 동적 거래 모델의 그림.

실행: ../.venv/bin/python gp_art.py            (→ _art/gp/, 아이보리 바탕 — 보충 덱용)
      GP_WHITE=1 ../.venv/bin/python gp_art.py (→ _art/gp_white/, 흰 바탕 — W07 강의본 삽입용)
모든 수치는 여기서 직접 계산한다(손계산 표·시뮬레이션). 원 논문: Gârleanu·Pedersen, JF 68(6) 2013.
"""
import os
import numpy as np
import primer_lib as PL

WHITE_BG = os.environ.get("GP_WHITE") == "1"
if WHITE_BG:
    PL.PAPER = "#FFFFFF"
    PL.plt.rcParams.update({"figure.facecolor": "#FFFFFF", "axes.facecolor": "#FFFFFF",
                            "savefig.facecolor": "#FFFFFF"})
from primer_lib import (out_dir, save, clean, svg, text, arrow, vrule, hrule,
                        equation as eq_png, INK, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)
plt = PL.plt
PAPER = PL.PAPER

OUT = out_dir("gp_white" if WHITE_BG else "gp")
FIG = (10.6, 4.2)
EX = "수업용으로 지어낸 예시입니다"
SIM = "컴퓨터로 만든 가상 실험입니다"


def cbox(x, y, w, h, title, subs=(), kind="white", stroke=HAIR, ts=34, ss=26):
    fill, tc, sc = {"white": (WHITE, INK, MUTED), "dark": (DARK, LIME, "#B8C6C8"),
                    "lime": (LIME, DARK, DARK), "paper": (PAPER, INK, MUTED)}[kind]
    st = {"dark": DARK, "lime": INK}.get(kind, stroke)
    lh = ss * 1.45
    block = ts + (len(subs) * lh + 10 if subs else 0)
    top = y + (h - block) / 2 + ts * 0.85
    b = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" '
         f'stroke="{st}" stroke-width="2.5"/>')
    b += text(x + w / 2, top, title, ts, tc, bold=True)
    for i, t in enumerate(subs):
        b += text(x + w / 2, top + 12 + (i + 1) * lh, t, ss, sc)
    return b


# ── GP 공식 ──────────────────────────────────────────────────────
def a_of(gamma, lam, rho=0.0):
    k = gamma * (1 - rho) + lam * rho
    return (-k + np.sqrt(k * k + 4 * gamma * lam * (1 - rho) ** 2)) / (2 * (1 - rho))


def simulate(T=200_000, phis=(0.5, 0.05), B=(0.1, 0.1), gamma=1.0, lam=2.0, seed=11):
    """자산 1개(σ² = 1), 신호 두 개(각각 분산 1인 AR(1)). 비중 단위는 ‘위험 1 단위’."""
    rng = np.random.default_rng(seed)
    phis, B = np.array(phis), np.array(B)
    f = np.zeros((T + 1, len(phis)))
    sd = np.sqrt(1 - (1 - phis) ** 2)
    for t in range(T):
        f[t + 1] = (1 - phis) * f[t] + sd * rng.standard_normal(len(phis))
    r = (f[:-1] @ B) + rng.standard_normal(T)            # r_{t+1} = B f_t + u
    a = a_of(gamma, lam)
    mk = (f[:-1] @ B) / gamma                             # Markowitz = (γσ²)⁻¹ B f
    aim = (f[:-1] @ (B / (1 + phis * a / gamma))) / gamma
    return dict(f=f, r=r, mk=mk, aim=aim, a=a, gamma=gamma, lam=lam)


def run_policy(target, rate, r, gamma, lam):
    x = np.zeros_like(target)
    prev = 0.0
    for t in range(len(target)):
        prev = prev + rate * (target[t] - prev)
        x[t] = prev
    dx = np.diff(np.concatenate([[0.0], x]))
    ret = x * r
    risk = gamma / 2 * x ** 2
    cost = lam / 2 * dx ** 2
    return dict(x=x, ret=ret.mean(), risk=risk.mean(), cost=cost.mean(),
                net=(ret - risk - cost).mean(), turn=np.abs(dx).mean())


# ── 1. 딜레마: 목표를 그대로 좇으면 ──────────────────────────────
def dilemma():
    S = simulate(T=400, seed=4)
    t0, n = 200, 120
    mk = S["mk"][t0:t0 + n] * 100
    gp = run_policy(S["aim"], S["a"] / S["lam"], S["r"], S["gamma"], S["lam"])["x"][t0:t0 + n] * 100
    fig, ax = plt.subplots(figsize=FIG)
    t = np.arange(n)
    ax.plot(t, mk, color=MUTED, lw=2.0, label="매번 목표(Markowitz)를 그대로")
    ax.plot(t, gp, color=TEAL, lw=3.8, label="GP — 조준점으로 일부만")
    ax.axhline(0, color=HAIR, lw=1)
    tm, tg = np.abs(np.diff(mk)).sum(), np.abs(np.diff(gp)).sum()
    ax.text(n - 1, ax.get_ylim()[0] * 0.92, f"거래량 합: 목표 추종 {tm:,.0f} · GP {tg:,.0f} (약 {tm/tg:.0f}분의 1)",
            ha="right", fontsize=15, color=INK, fontweight="bold")
    ax.set_xlabel("기간", fontsize=14); ax.set_ylabel("보유 (×100)", fontsize=14)
    ax.legend(fontsize=14.5, frameon=False, loc="upper left", bbox_to_anchor=(0, 1.2), ncol=2)
    clean(ax); fig.tight_layout()
    return save(fig, "dilemma.png", "거래량 = 매 기간 보유 변화의 절댓값 합 · 빠른 신호(φ = 0.5)와 느린 신호(φ = 0.05) — " + SIM)


# ── 2. 신호는 사라진다: 반감기 ─────────────────────────────────
def decay():
    k = np.arange(0, 41)
    fig, ax = plt.subplots(figsize=FIG)
    for phi, c, lab in [(0.5, RED, "빠른 신호 φ = 0.5 — 반감기 1기간 (예: 5일 반전)"),
                        (0.05, TEAL, "느린 신호 φ = 0.05 — 반감기 약 13.5기간 (예: 1년 모멘텀)")]:
        ax.plot(k, (1 - phi) ** k, color=c, lw=4, label=lab)
        hl = np.log(0.5) / np.log(1 - phi)
        ax.scatter([hl], [0.5], s=110, color=c, zorder=5)
    ax.axhline(0.5, color=INK, lw=1.2, ls="--")
    ax.text(40, 0.53, "처음의 절반", ha="right", fontsize=14, color=INK)
    ax.set_xlabel("몇 기간 뒤", fontsize=14); ax.set_ylabel("남아 있는 예측력", fontsize=14)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=15, frameon=False, loc="upper right")
    clean(ax); fig.tight_layout()
    return save(fig, "decay.png", "매 기간 φ만큼 사라진다 — k기간 뒤 (1 − φ)의 k제곱")


# ── 3. 이차 비용: 쪼갤수록 싸다 ─────────────────────────────────
def quad_cost():
    fig, axes = plt.subplots(1, 2, figsize=FIG, gridspec_kw={"width_ratios": [1, 1.1]})
    ax = axes[0]
    q = np.linspace(0, 1, 100)
    ax.plot(q * 100, q * 100, color=AMBER, lw=3.5, label="비례 비용 (수수료·스프레드)")
    ax.plot(q * 100, q ** 2 * 100, color=TEAL, lw=4, label="이차 비용 (시장충격)")
    ax.set_xlabel("이번에 거래하는 양", fontsize=14); ax.set_ylabel("비용", fontsize=14)
    ax.set_title("작은 거래는 이차 비용이 거의 0", fontsize=16, color=INK, pad=10)
    ax.legend(fontsize=13.5, frameon=False, loc="upper left")
    clean(ax)
    ax = axes[1]
    labs, vals = ["한 번에\n100", "두 번에\n50씩", "네 번에\n25씩"], [1, .5, .25]
    ax.bar(range(3), vals, color=[RED, AMBER, TEAL], width=.56)
    for i, v in enumerate(vals):
        ax.text(i, v + .03, ["1", "½", "¼"][i], ha="center", fontsize=20, fontweight="bold", color=INK)
    ax.set_xticks(range(3)); ax.set_xticklabels(labs, fontsize=14)
    ax.set_ylim(0, 1.2); ax.set_yticks([])
    ax.set_title("같은 100을 사도 쪼개면 총비용이 준다", fontsize=16, color=INK, pad=10)
    clean(ax, grid=None)
    fig.tight_layout()
    return save(fig, "quad_cost.png", "이차 비용: (100)² = 2 × (50)² × 2 = 4 × (25)² × 4")


# ── 4. 두 원칙 도해 ─────────────────────────────────────────────
def two_principles():
    Y = 250
    xs = {"hold": 170, "new": 520, "aim": 870, "mk": 1330}
    b = f'<line x1="80" y1="{Y}" x2="1540" y2="{Y}" stroke="{INK}" stroke-width="3"/>'
    b += text(80, Y - 16, "← 주식 비중 작음", 22, MUTED, anchor="start")
    # 미래 목표들(점선 점)
    for i, x in enumerate([1330, 1180, 1070, 990, 935]):
        b += f'<circle cx="{x}" cy="{Y}" r="{13 - i*1.6}" fill="{MUTED}" opacity="{1 - i*0.16}"/>'
    b += text(1150, Y - 70, "오늘·내일·모레의 목표 (신호가 사라지며 줄어든다)", 25, MUTED)
    b += f'<path d="M1330,{Y-40} L940,{Y-40}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="8,6" marker-end="url(#aM)"/>'
    # 점
    b += f'<circle cx="{xs["hold"]}" cy="{Y}" r="16" fill="{INK}"/>'
    b += f'<circle cx="{xs["aim"]}" cy="{Y}" r="18" fill="{RED}"/>'
    b += f'<circle cx="{xs["new"]}" cy="{Y}" r="18" fill="{TEAL}"/>'
    b += f'<circle cx="{xs["mk"]}" cy="{Y}" r="16" fill="none" stroke="{INK}" stroke-width="4"/>'
    b += text(xs["hold"], Y + 60, "어제 보유", 30, INK, bold=True)
    b += text(xs["mk"], Y + 60, "오늘 목표", 30, INK, bold=True)
    b += text(xs["mk"], Y + 96, "(Markowitz)", 24, MUTED)
    b += text(xs["aim"], Y + 60, "조준점", 32, RED, bold=True)
    b += text(xs["aim"], Y + 96, "미래 목표들의 평균", 24, RED)
    b += text(xs["new"], Y + 60, "오늘 보유", 32, TEAL, bold=True)
    # 원칙 1: 부분 이동 화살표
    b += f'<path d="M{xs["hold"]},{Y-26} Q{(xs["hold"]+xs["new"])/2},{Y-120} {xs["new"]-6},{Y-30}" fill="none" stroke="{TEAL}" stroke-width="5" marker-end="url(#aT)"/>'
    b += f'<path d="M{xs["new"]+10},{Y-26} Q{(xs["new"]+xs["aim"])/2},{Y-90} {xs["aim"]-10},{Y-30}" fill="none" stroke="{TEAL}" stroke-width="3" stroke-dasharray="8,7"/>'
    b += text((xs["hold"] + xs["aim"]) / 2, Y - 142, "원칙 1 · 간격의 일부(a/λ)만 이번에 메운다", 30, TEAL, bold=True)
    # 원칙 2: 조준점
    b += f'<rect x="{xs["aim"]-235}" y="{Y+118}" width="700" height="96" rx="12" fill="{WHITE}" stroke="{RED}" stroke-width="2.5"/>'
    b += text(xs["aim"] + 115, Y + 158, "원칙 2 · 오늘 목표가 아니라 그 앞을 겨눈다", 29, RED, bold=True)
    b += text(xs["aim"] + 115, Y + 196, "곧 사라질 신호는 덜, 오래갈 신호는 더 반영", 26, INK)
    b += text(xs["hold"] + 150, Y + 175, "날아가는 새는", 27, MUTED)
    b += text(xs["hold"] + 150, Y + 212, "지나갈 자리를 쏜다", 27, MUTED)
    return svg("two_principles.png", b, h=500)


# ── 5. 거래 속도 a/λ ─────────────────────────────────────────────
def trade_rate():
    lam = np.logspace(-2, 3, 300)
    fig, ax = plt.subplots(figsize=FIG)
    for g, c in [(0.5, BLUE), (1, TEAL), (5, RED)]:
        ax.plot(lam, a_of(g, lam) / lam, color=c, lw=3.6, label=f"위험회피 γ = {g:g}")
    ax.scatter([2], [0.5], s=140, color=TEAL, zorder=5)
    ax.annotate("γ = 1, λ = 2 → a = 1, 매번 절반씩", (2, .5), xytext=(22, 18), textcoords="offset points",
                fontsize=15, color=INK, fontweight="bold")
    ax.set_xscale("log")
    ax.set_xlabel("거래비용 계수 λ (눈금 한 칸 = 10배)", fontsize=14)
    ax.set_ylabel("거래 속도 a/λ", fontsize=14)
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=15, frameon=False, loc="lower left")
    clean(ax); fig.tight_layout()
    return save(fig, "trade_rate.png", "할인 ρ = 0 — 공식 (9)를 그대로 그린 그림입니다")


# ── 6. 조준점 = 미래 목표의 가중평균 ──────────────────────────────
def aim_weights():
    gamma, lam = 1.0, 2.0
    a = a_of(gamma, lam); z = gamma / (gamma + a)
    tau = np.arange(0, 9)
    fig, axes = plt.subplots(1, 2, figsize=FIG, sharey=True)
    for ax, phi, c, name in [(axes[0], .5, RED, "빠른 신호 φ = 0.5"), (axes[1], .05, TEAL, "느린 신호 φ = 0.05")]:
        fut = (1 - phi) ** tau
        aim = 1 / (1 + phi * a / gamma)
        ax.bar(tau, fut, color=c, alpha=.8, width=.62)
        ax.axhline(aim, color=INK, lw=2.4, ls="--")
        ax.text(8.4, aim + .04, f"조준점 {aim:.3f}", ha="right", fontsize=16, fontweight="bold", color=INK)
        for t in tau[:4]:
            ax.text(t, -0.13, f"{z*(1-z)**t:.2f}", ha="center", fontsize=12.5, color=MUTED)
        ax.set_title(name, fontsize=17, color=c, pad=8)
        ax.set_xlabel("τ 기간 뒤의 목표 (아래 숫자 = 그 목표의 가중치)", fontsize=13)
        ax.set_ylim(-0.2, 1.15); ax.set_xticks(tau)
        clean(ax)
    axes[0].set_ylabel("오늘 목표를 1로 둔 크기", fontsize=13)
    fig.tight_layout()
    return save(fig, "aim_weights.png", f"γ = 1, λ = 2 → z = {z:.2f} · τ기간 뒤 목표의 가중치 = z × (1 − z)의 τ제곱")


# ── 7. 신호별 반영 비율 ─────────────────────────────────────────
def signal_weight():
    hl = np.logspace(-0.3, 3, 300)                 # 반감기(기간)
    phi = 1 - 0.5 ** (1 / hl)
    fig, ax = plt.subplots(figsize=FIG)
    for lam, c in [(0.2, BLUE), (2, TEAL), (20, RED)]:
        a = a_of(1.0, lam)
        ax.plot(hl, 1 / (1 + phi * a), color=c, lw=3.6, label=f"거래비용 λ = {lam:g}  (a/λ = {a/lam:.2f})")
    ax.set_xscale("log")
    for h, lab in [(1, "5일 반전"), (13.5, "1년 모멘텀"), (206, ""), ]:
        pass
    ax.axvline(1, color=HAIR, lw=1.4); ax.axvline(13.5, color=HAIR, lw=1.4)
    ax.text(1.06, .08, "반감기 1기간", fontsize=13, color=MUTED)
    ax.text(14.3, .08, "13.5기간", fontsize=13, color=MUTED)
    ax.set_xlabel("신호의 반감기 (기간, 눈금 한 칸 = 10배)", fontsize=14)
    ax.set_ylabel("조준점에 반영되는 비율", fontsize=14)
    ax.set_ylim(0, 1.03)
    ax.legend(fontsize=15, frameon=False, loc="lower right")
    clean(ax); fig.tight_layout()
    return save(fig, "signal_weight.png", "γ = 1 · 반영 비율 1 / (1 + φ·a/γ)")


# ── 8. 세 기간 손계산 ────────────────────────────────────────────
def three_period():
    a = a_of(1, 2); q = a / 2
    f1, f2 = 100.0, 100.0
    x = 0.0
    rows = []
    for t in range(1, 4):
        mk = f1 + f2
        aim = f1 / (1 + .5 * a) + f2 / (1 + .05 * a)
        nx = x + q * (aim - x)
        rows.append((t, mk, aim, nx, nx - x))
        x = nx
        f1 *= .5; f2 *= .95
    cmk = sum(d ** 2 for d in np.diff([0] + [r[1] for r in rows]))
    cgp = sum(r[4] ** 2 for r in rows)
    return rows, cmk, cgp


def cost_bars():
    rows, cmk, cgp = three_period()
    fig, ax = plt.subplots(figsize=(10.6, 3.6))
    ax.barh([1, 0], [cmk, cgp], color=[MUTED, TEAL], height=.56)
    ax.set_yticks([1, 0]); ax.set_yticklabels(["목표 추종", "GP"], fontsize=16, color=INK)
    for y, v in [(1, cmk), (0, cgp)]:
        ax.text(v + 600, y, f"{v:,.0f}", va="center", fontsize=18, fontweight="bold", color=INK)
    ax.set_xlim(0, cmk * 1.18); ax.set_xticks([])
    ax.set_title(f"세 기간 비용 지수 (거래량²의 합) — GP는 약 {cmk/cgp:.1f}분의 1", fontsize=16, color=INK, pad=10)
    clean(ax, grid=None); fig.tight_layout()
    return save(fig, "cost_bars.png", "γ = 1, λ = 2, σ² = 1 · 두 신호가 100씩, 기댓값대로 소멸")


# ── 9. 표본 경로 ────────────────────────────────────────────────
def sim_paths():
    S = simulate(T=600, seed=8)
    gp = run_policy(S["aim"], S["a"] / S["lam"], S["r"], 1, 2)["x"]
    t0, n = 300, 120
    t = np.arange(n)
    fig, ax = plt.subplots(figsize=FIG)
    ax.plot(t, S["mk"][t0:t0 + n] * 100, color=HAIR if not WHITE_BG else "#C9D1D0", lw=2.2, label="Markowitz 목표")
    ax.plot(t, S["aim"][t0:t0 + n] * 100, color=BLUE, lw=2.4, ls="--", label="조준점 — 흔들림을 거름")
    ax.plot(t, gp[t0:t0 + n] * 100, color=TEAL, lw=4, label="GP 보유 — 한 번 더 부드럽게")
    ax.axhline(0, color=HAIR, lw=1)
    ax.set_xlabel("기간", fontsize=14); ax.set_ylabel("보유 (×100)", fontsize=14)
    ax.legend(fontsize=14, frameon=False, loc="upper left", bbox_to_anchor=(0, 1.2), ncol=3)
    clean(ax); fig.tight_layout()
    return save(fig, "sim_paths.png", "φ = 0.5 · 0.05, 신호당 B = 0.1, γ = 1, λ = 2 — " + SIM)


# ── 10. 네 전략 비교 ────────────────────────────────────────────
def sim_compare():
    S = simulate()
    g, lam, a = S["gamma"], S["lam"], S["a"]
    res = {}
    res["목표 추종"] = run_policy(S["mk"], 1.0, S["r"], g, lam)
    best = max(((q, run_policy(S["mk"], q, S["r"], g, lam)) for q in np.arange(.05, 1.0, .05)),
               key=lambda z: z[1]["net"])
    res[f"부분 이동만\n(최적 {best[0]:.2f})"] = best[1]
    res["조준만\n(한 번에)"] = run_policy(S["aim"], 1.0, S["r"], g, lam)
    res["GP\n(조준 + 부분)"] = run_policy(S["aim"], a / lam, S["r"], g, lam)
    names = list(res)
    fig, ax = plt.subplots(figsize=FIG)
    xs = np.arange(len(names)); w = .2
    comp = [("기대수익", "ret", BLUE, 1), ("위험 벌점", "risk", AMBER, -1), ("거래비용", "cost", RED, -1), ("순효용", "net", TEAL, 1)]
    for j, (lab, k, c, sgn) in enumerate(comp):
        v = [sgn * res[n][k] * 1e4 for n in names]
        ax.bar(xs + (j - 1.5) * w, v, width=w, color=c, label=lab)
        if k == "net":
            for x_, vv in zip(xs, v):
                ax.text(x_ + 1.5 * w, vv + (4 if vv >= 0 else -14), f"{vv:.1f}", ha="center", fontsize=15,
                        fontweight="bold", color=INK)
    ax.axhline(0, color=INK, lw=1)
    ax.set_xticks(xs); ax.set_xticklabels(names, fontsize=14, color=INK)
    ax.set_ylabel("기간당 평균 (단위 0.0001)", fontsize=14)
    ax.legend(fontsize=13.5, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(.5, 1.13))
    clean(ax); fig.tight_layout()
    out = save(fig, "sim_compare.png", "20만 기간 · γ = 1, λ = 2 — " + SIM)
    with open(os.path.join(OUT, "sim_compare.txt"), "w") as fh:
        for n in names:
            d = res[n]
            fh.write(f"{n.replace(chr(10),' ')}\tret={d['ret']*1e4:.1f}\trisk={d['risk']*1e4:.1f}\tcost={d['cost']*1e4:.1f}\tnet={d['net']*1e4:.1f}\tturn={d['turn']*100:.2f}\n")
    return out


# ── 11. 비용 구조별 최적 행동: 무거래 구간 vs 부분 이동 ─────────────
def band_vs_gp():
    rng = np.random.default_rng(21)
    n = 150
    target = 60 + np.cumsum(rng.normal(0, 1.1, n))
    target = 60 + (target - 60) * .6
    band, hw = [], 3.0
    x = 60.0
    for tt in target:
        if x > tt + hw: x = tt + hw
        elif x < tt - hw: x = tt - hw
        band.append(x)
    gp, x = [], 60.0
    for tt in target:
        x = x + .25 * (tt - x); gp.append(x)
    fig, axes = plt.subplots(1, 2, figsize=FIG, sharey=True)
    t = np.arange(n)
    ax = axes[0]
    ax.fill_between(t, target - hw, target + hw, color=AMBER, alpha=.18)
    ax.plot(t, target, color=MUTED, lw=1.6)
    ax.plot(t, band, color=AMBER, lw=3.6)
    ax.set_title("비례 비용 → 무거래 구간", fontsize=17, color=INK, pad=8)
    ax.text(2, target.min() - 2.2, "구간 안에서는 가만히, 밖이면 경계까지", fontsize=14, color=INK)
    ax = axes[1]
    ax.plot(t, target, color=MUTED, lw=1.6, label="목표")
    ax.plot(t, gp, color=TEAL, lw=3.6, label="보유")
    ax.set_title("이차 비용 → 매번 조금씩 (GP)", fontsize=17, color=INK, pad=8)
    ax.text(2, target.min() - 2.2, "간격의 일정 비율을 매번 메운다", fontsize=14, color=INK)
    ax.legend(fontsize=14, frameon=False, loc="upper right")
    for ax in axes:
        ax.set_xlabel("기간", fontsize=13); clean(ax)
    axes[0].set_ylabel("주식 비중(%)", fontsize=13)
    fig.tight_layout()
    return save(fig, "band_vs_gp.png", "같은 목표 경로, 비용 구조만 다르다 — " + EX)


# ── 12. 어디에 쓰나: 비용 × 신호 지도 ─────────────────────────────
def where_map():
    b = text(460, 40, "신호 없음 (목표 비중이 고정)", 29, MUTED, bold=True)
    b += text(1140, 40, "신호 있음 (목표가 움직인다)", 29, MUTED, bold=True)
    b += text(60, 190, "비례 비용", 29, MUTED, bold=True, anchor="start")
    b += text(60, 226, "(수수료 중심)", 24, MUTED, anchor="start")
    b += text(60, 400, "이차 비용", 29, MUTED, bold=True, anchor="start")
    b += text(60, 436, "(대형 · 충격 중심)", 24, MUTED, anchor="start")
    b += cbox(260, 70, 400, 250, "무거래 구간", ["리밸런싱 밴드", "W07 SS2 · 2교시 24쪽"], ts=36, ss=26, stroke=AMBER)
    b += cbox(810, 70, 660, 250, "구간 + 움직이는 중심", ["닫힌 해 없음 → MPO · RL", "RL이 가장 쓸모 있는 칸"], "dark", ts=36, ss=26)
    b += cbox(260, 290 + 50, 400, 250, "나눠서 이동", ["전환을 여러 기간에", "글라이드패스 실행"], ts=36, ss=26, stroke=TEAL)
    b += cbox(810, 290 + 50, 660, 250, "Gârleanu–Pedersen", ["조준점으로 일부만 이동", "TAA · 팩터 틸트 · 대형 신호 운용"], "lime", ts=38, ss=27)
    return svg("where_map.png", b, h=600)


# ── 13. 연기금 대형 전환: 남는 간격과 비용 ─────────────────────────
def pension_shift():
    n = np.arange(0, 13)
    fig, axes = plt.subplots(1, 2, figsize=FIG, gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axes[0]
    for q, c in [(0.2, BLUE), (0.35, TEAL), (0.5, RED)]:
        ax.plot(n, 5 * (1 - q) ** n, color=c, lw=3.6, marker="o", ms=6, label=f"a/λ = {q}")
    ax.axhline(0.5, color=INK, lw=1.2, ls="--")
    ax.text(12, .62, "간격 10% 이하", ha="right", fontsize=13.5, color=INK)
    ax.set_xlabel("분기", fontsize=13.5); ax.set_ylabel("남은 간격 (%p)", fontsize=13.5)
    ax.set_title("5%p 전환에서 남은 간격", fontsize=16, color=INK, pad=8)
    ax.legend(fontsize=14, frameon=False, loc="upper right")
    clean(ax)
    ax = axes[1]
    qs = [1.0, 0.5, 0.35, 0.2]
    rel = [q / (2 - q) for q in qs]
    ax.bar(range(4), rel, color=[RED, AMBER, TEAL, BLUE], width=.58)
    for i, v in enumerate(rel):
        ax.text(i, v + .03, f"{v:.2f}", ha="center", fontsize=16, fontweight="bold", color=INK)
    ax.set_xticks(range(4)); ax.set_xticklabels(["한 번에", "a/λ\n0.5", "a/λ\n0.35", "a/λ\n0.2"], fontsize=13.5)
    ax.set_ylim(0, 1.2); ax.set_yticks([])
    ax.set_title("충격비용 (한 번에 = 1)", fontsize=16, color=INK, pad=8)
    clean(ax, grid=None)
    fig.tight_layout()
    return save(fig, "pension_shift.png", "조준점이 고정일 때 — 남은 간격 = 처음 간격 × (1 − a/λ)의 n제곱 · 총비용 비율 = (a/λ) ÷ (2 − a/λ)")


# ── 수식 ────────────────────────────────────────────────────────
def equations():
    E = [("eq_markowitz", r"$x^{*}_{t} \;=\; (\gamma\,\Sigma)^{-1}\,B\,f_t$", 46, 6.4),
         ("eq_signal", r"$r_{t+1} \;=\; B\,f_t \;+\; u_{t+1}$", 46, 6.4),
         ("eq_decay", r"$f_{t+1} - f_t \;=\; -\,\Phi\, f_t \;+\; \varepsilon_{t+1}$", 44, 7.6),
         ("eq_cost", r"$TC_t \;=\; \frac{1}{2}\,\Delta x_t^{\top}\,\Lambda\,\Delta x_t,\qquad \Lambda = \lambda\,\Sigma$", 42, 9.0),
         ("eq_obj", r"$\max_{x}\ \mathrm{E}\sum_{t}(1-\rho)^{t}\left[\,x_t^{\top}B f_t \;-\; \frac{\gamma}{2}\,x_t^{\top}\Sigma\, x_t \;-\; \frac{1}{2}\,\Delta x_t^{\top}\Lambda\,\Delta x_t\right]$", 36, 11.4),
         ("eq_rule", r"$x_t \;=\; \left(1-\frac{a}{\lambda}\right)x_{t-1} \;+\; \frac{a}{\lambda}\;\mathrm{aim}_t$", 46, 8.4),
         ("eq_a", r"$a \;=\; \frac{-\,k \;+\; \sqrt{k^{2} + 4\,\gamma\,\lambda\,(1-\rho)^{2}}}{2\,(1-\rho)},\qquad k = \gamma(1-\rho) + \lambda\rho$", 36, 11.4),
         ("eq_aim_sum", r"$\mathrm{aim}_t \;=\; \sum_{\tau=0}^{\infty}\, z\,(1-z)^{\tau}\;\mathrm{E}_t\!\left[x^{*}_{t+\tau}\right],\qquad z = \frac{\gamma}{\gamma + a}$", 38, 11.0),
         ("eq_aim_signal", r"$\mathrm{aim}_t \;=\; (\gamma\,\Sigma)^{-1}\,\sum_{k}\ \frac{B_k\,f_{k,t}}{1 + \phi_k\, a/\gamma}$", 42, 9.0)]
    for n, tex, fs, w in E:
        eq_png(tex, n + ".png", fontsize=fs, width=w)


if __name__ == "__main__":
    dilemma(); decay(); quad_cost(); two_principles(); trade_rate(); aim_weights()
    signal_weight(); cost_bars(); sim_paths(); sim_compare(); band_vs_gp(); where_map()
    pension_shift(); equations()
    rows, cmk, cgp = three_period()
    for r in rows:
        print("  t=%d  mk=%.1f  aim=%.1f  x=%.1f  dx=%+.1f" % r)
    print("  cost mk=%.0f gp=%.0f" % (cmk, cgp))
    print(open(os.path.join(OUT, "sim_compare.txt")).read())
