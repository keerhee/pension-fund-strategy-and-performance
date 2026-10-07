# -*- coding: utf-8 -*-
"""W07 보강 1 — 처음 배우는 TDF 그림.

실행: python w07_tdf_art.py  →  _art/w07tdf/
공시 수치(순자산·점유율·수익률·보수)는 출처를 덱 각주에 적는다.
생애주기·순서위험·동적 경로 그림은 수업용 가상 계산이다(그림 우하단에 밝힌다).
"""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, fig, equation, svg, box, limebox, darkbox,
                        arrow, text, INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER,
                        MUTED, HAIR, DARK, WIDE)

OUT = out_dir("w07tdf")
PI_STAR = 0.39          # 강의본 13쪽 예 — μ 7 · r 3 · γ 4 · σ 16
CAP_ACC, CAP_RET = 0.80, 0.40   # 적격 TDF 위험자산 상한(적립기 · 인출기)


def bx(x, y, w, h, title, sub=(), kind="white", ts=40, ss=31):
    """큰 글씨 상자 — 슬라이드에서 16pt 아래로 내려가지 않게(룰북 §7.2)."""
    fill, stroke, tc, sc = {"white": (WHITE, HAIR, INK, MUTED), "teal": (WHITE, TEAL, INK, MUTED),
                            "lime": (LIME, INK, DARK, DARK), "dark": (DARK, DARK, LIME, "#9FB0B2")}[kind]
    n = len(sub)
    top = y + (h - (ts + 14 + n * (ss + 12))) / 2 + ts
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="{3 if kind != "white" else 2}"/>'
         f'<text x="{x+w/2}" y="{top}" font-size="{ts}" font-weight="700" fill="{tc}" '
         f'text-anchor="middle">{title}</text>')
    for i, ln in enumerate(sub):
        s += (f'<text x="{x+w/2}" y="{top + 14 + (i+1)*(ss+12) - 4}" font-size="{ss}" fill="{sc}" '
              f'text-anchor="middle">{ln}</text>')
    return s


# ── 01 · 순자산 추이 ─────────────────────────────────────────────
def aum():
    yrs = ["2016", "2020", "2022", "2023", "2024", "2025"]
    val = [0.07, 5.2, 10.5, 12.1, 16.6, 25.6]
    f, ax = fig()
    cols = [MUTED] * 5 + [TEAL]
    b = ax.bar(yrs, val, color=cols, width=0.58)
    for r, v in zip(b, val):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.6, f"{v:,.1f}조" if v >= 1 else "0.07조",
                ha="center", va="bottom", fontsize=17, fontweight="bold",
                color=TEAL if v == val[-1] else INK)
    ax.set_ylim(0, 30)
    ax.set_ylabel("순자산 (조원, 연말)", fontsize=14)
    clean(ax)
    ax.tick_params(labelsize=16)
    ax.annotate("1년 새 +55%", xy=(5, 25.6), xytext=(3.55, 24.0), fontsize=16, color=RED,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    save(f, "aum.png", note="2016~2024 자본시장연구원(2026.3) · 2025 금융감독원(2026.3)")


# ── 01 · 펀드 하나에 맡기는 세 가지 ────────────────────────────────
def one_fund():
    b = ""
    b += bx(20, 190, 340, 240, "내가 하는 일", ["빈티지 하나", "예: TDF2050"])
    b += arrow(370, 310, 450, 310)
    b += (f'<rect x="460" y="20" width="790" height="580" rx="14" fill="{WHITE}" '
          f'stroke="{TEAL}" stroke-width="3" stroke-dasharray="10 8"/>')
    b += text(855, 76, "운용사가 대신 하는 일", 36, TEAL, bold=True)
    b += bx(490, 100, 730, 150, "① 자산배분", ["주식·채권·대체 하위펀드에 나눠 담기"])
    b += bx(490, 268, 730, 150, "② 리밸런싱", ["틀어진 비중을 정기적으로 되돌리기"])
    b += bx(490, 436, 730, 150, "③ 글라이드패스", ["해마다 위험자산을 조금씩 줄이기"])
    b += arrow(1260, 310, 1320, 310)
    b += bx(1330, 190, 250, 240, "은퇴까지", ["손댈 일이", "거의 없다"], kind="lime")
    svg("one_fund.png", b, w=1600, h=620)


# ── 02 · 생애주기 — 총부와 함의 비중 ───────────────────────────────
def lifecycle():
    ages = np.arange(25, 86)
    g, rd, s, rf = 0.03, 0.03, 0.15, 0.04           # 임금 증가 · 할인 · 저축률 · 수익률
    inc = np.where(ages < 65, 0.40 * (1 + g) ** (ages - 25), 0.0)    # 억원
    H = np.array([sum(inc[j] / (1 + rd) ** (j - i) for j in range(i, len(ages)))
                  - inc[i] for i in range(len(ages))])
    F = np.zeros(len(ages)); F[0] = 0.10
    for i in range(1, len(ages)):
        if ages[i] <= 65:
            F[i] = F[i - 1] * (1 + rf) + s * inc[i - 1]
        else:
            F[i] = max(F[i - 1] * (1 + rf) - 0.35, 0)
    w = np.minimum(PI_STAR * (1 + H / np.maximum(F, 1e-6)), 1.0)
    cap = np.where(ages < 65, CAP_ACC, CAP_RET)

    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE)
    a1.stackplot(ages, F, H, colors=[INK, "#BFD8D6"], labels=["금융자산 F", "인적자본 H"])
    a1.axvline(65, color=MUTED, ls=":", lw=1.5)
    a1.text(65.6, 15.5, "은퇴 65세", fontsize=13, color=MUTED)
    a1.set_title("총부 = 금융자산 + 인적자본 (억원)", fontsize=16, loc="left", color=INK)
    a1.text(31, 9, "인적자본 H", fontsize=17, color=INK, fontweight="bold")
    a1.text(70, 4, "금융자산 F", fontsize=17, color=WHITE, fontweight="bold")
    a1.set_xlabel("나이", fontsize=14); clean(a1)

    a2.plot(ages, w * 100, color=TEAL, lw=3.4, label="이론이 말하는 주식 비중")
    a2.plot(ages, cap * 100, color=RED, lw=2, ls="--", label="적격 TDF 위험자산 상한")
    a2.fill_between(ages, cap * 100, 100, color=RED, alpha=0.06)
    a2.axhline(PI_STAR * 100, color=MUTED, lw=1.4, ls=":")
    a2.text(26, PI_STAR * 100 - 7, "H = 0이면 Merton 비중 39%", fontsize=13, color=MUTED)
    a2.set_ylim(0, 105); a2.set_ylabel("금융자산 중 주식 (%)", fontsize=14)
    a2.set_xlabel("나이", fontsize=14)
    a2.set_title("H가 줄어드는 만큼 주식이 줄어든다", fontsize=16, loc="left", color=INK)
    a2.legend(loc="lower left", fontsize=13, frameon=False); clean(a2)
    f.tight_layout(w_pad=3)
    save(f, "lifecycle.png", note="가상 계산 — 연봉 4천만 원·임금 3%·저축 15%·수익 4%·π* 39%")
    i35, i55 = 10, 30
    print(f"   35세 H={H[i35]:.1f} F={F[i35]:.2f} · 55세 H={H[i55]:.1f} F={F[i55]:.2f} · "
          f"80% 상한 아래로 내려오는 나이 {ages[np.argmax(w < 0.8)]}")


# ── 02 · 세 가지 글라이드패스와 한국 규정 ──────────────────────────
def glidepaths():
    ages = np.arange(25, 81)
    aggr = np.interp(ages, [25, 40, 65, 72, 80], [90, 90, 50, 30, 30])   # Through
    cons = np.interp(ages, [25, 35, 65, 80], [70, 70, 20, 20])           # To
    rule = np.clip(100 - ages, 0, 100)
    cap = np.where(ages < 65, 80, 40)
    f, ax = fig()
    ax.fill_between(ages, cap, 100, color=RED, alpha=0.07, step="post")
    ax.step(ages, cap, color=RED, lw=2, ls="--", where="post")
    ax.plot(ages, aggr, color=INK, lw=3.2)
    ax.plot(ages, cons, color=TEAL, lw=3.2)
    ax.plot(ages, rule, color=MUTED, lw=2, ls=":")
    ax.axvline(65, color=MUTED, lw=1.2, ls=":")
    ax.text(26, 92.5, "공격형 · Through  90 → 30%", fontsize=15, color=INK, fontweight="bold")
    ax.text(26, 56, "보수형 · To  70 → 20%", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(47, 56, "나이 = 채권 (100 − 나이)", fontsize=14, color=MUTED)
    ax.text(48, 84, "적격 TDF 상한 — 적립기 80%", fontsize=14, color=RED)
    ax.text(66, 44, "인출기 40%", fontsize=14, color=RED)
    ax.text(65.4, 2, "은퇴 65세", fontsize=13, color=MUTED)
    ax.set_xlim(25, 80); ax.set_ylim(0, 100)
    ax.set_xlabel("나이", fontsize=14); ax.set_ylabel("주식(위험자산) 비중 (%)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "glidepaths.png", note="경로는 강의본 21쪽 예시 · 상한은 적격 TDF 요건")


# ── 02 · 순서 위험 ────────────────────────────────────────────────
def sequence():
    r = np.array([-20, -12, 4, 8, 10, 12, 7, 6, 9, 8, 7, 6, 5, 9, 10, 8, 6, 7, 5, 8]) / 100
    def run(rs, w0=5.0, wd=0.35):
        v = [w0]
        for x in rs:
            v.append(max(v[-1] * (1 + x) - wd, 0))
        return np.array(v)
    A, B = run(r), run(r[::-1])
    ages = np.arange(65, 86)
    f, ax = fig()
    ax.plot(ages, B, color=TEAL, lw=3.2)
    ax.plot(ages, A, color=RED, lw=3.2)
    ax.text(85.2, B[-1], f"좋은 해 먼저\n{B[-1]:.1f}억", fontsize=15, color=TEAL, va="center",
            fontweight="bold")
    dep = ages[np.argmax(A <= 0)]
    ax.text(dep + 0.3, 0.35, f"나쁜 해 먼저 — {dep}세에 바닥", fontsize=15, color=RED,
            va="bottom", fontweight="bold")
    ax.set_xlim(65, 88); ax.set_ylim(0, max(B) * 1.12)
    ax.set_xlabel("나이", fontsize=14); ax.set_ylabel("남은 자산 (억원)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    ax.text(65.4, max(B) * 1.04,
            f"같은 20년 수익률을 순서만 뒤집었다 · 산술평균 {r.mean()*100:.1f}% · 해마다 3,500만 원 인출",
            fontsize=14, color=MUTED)
    save(f, "sequence.png", note="가상 계산 — 65세 5억 원으로 시작")
    print(f"   순서위험: 나쁜 해 먼저 {A[-1]:.2f} · 좋은 해 먼저 {B[-1]:.2f}")


# ── 03 · 운용사 점유율 ────────────────────────────────────────────
def share():
    names = ["미래에셋", "삼성", "KB", "한국투자", "신한", "그 밖 14곳"]
    vals = [34.4, 14.4, 13.5, 11.7, 9.0, 17.0]
    f, ax = fig()
    y = np.arange(len(names))[::-1]
    ax.barh(y, vals, color=[TEAL] + [MUTED] * 5, height=0.6)
    for yi, v in zip(y, vals):
        ax.text(v + 0.6, yi, f"{v:.1f}%", va="center", fontsize=16, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=16)
    ax.set_xlim(0, 45); ax.set_xlabel("TDF 순자산 점유율 (%)", fontsize=14)
    clean(ax, grid="x")
    ax.text(22, 1.0, "1위 점유율\n2024.1  40.6% → 2026.1  34.4%", fontsize=15, color=RED)
    save(f, "share.png", note="딜사이트 2026.1 집계 · 19개사 204개 펀드")


# ── 03 · 디폴트옵션의 역설 ────────────────────────────────────────
def default_option():
    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE, gridspec_kw={"width_ratios": [1.25, 1]})
    a1.barh([0], [85], color=MUTED, height=0.7)
    a1.barh([0], [15], left=[85], color=TEAL, height=0.7)
    a1.text(42, 0, "원리금보장형  85%", ha="center", va="center", fontsize=18, color=WHITE,
            fontweight="bold")
    a1.text(92.5, 0, "실적\n배당\n15%", ha="center", va="center", fontsize=13, color=WHITE,
            fontweight="bold")
    a1.set_xlim(0, 100); a1.set_ylim(-0.55, 0.6); a1.set_yticks([])
    a1.set_title("디폴트옵션 적립금 53.3조 원의 구성 (2025말)", fontsize=16, loc="left")
    clean(a1, grid=None); a1.spines["left"].set_visible(False)
    a1.tick_params(labelsize=13); a1.set_xlabel("%", fontsize=13)

    lab, v = ["디폴트옵션\n전체", "TDF"], [4.0, 14.0]
    bb = a2.bar(lab, v, color=[MUTED, TEAL], width=0.52)
    for r_, x in zip(bb, v):
        a2.text(r_.get_x() + r_.get_width() / 2, x + 0.4, f"{x:.0f}%", ha="center",
                fontsize=18, fontweight="bold")
    a2.set_ylim(0, 17); a2.set_title("2025년 연간 수익률", fontsize=16, loc="left")
    clean(a2); a2.tick_params(labelsize=15)
    f.tight_layout(w_pad=4)
    save(f, "default_option.png", note="아시아투데이 2026.6.30 (고용노동부·자본시장연구원 자료 인용)")


# ── 03 · 빈티지별 수익률과 보수 ───────────────────────────────────
def vintage_ret_fee():
    vin = ["2025", "2030", "2035", "2040", "2045", "2050"]
    ret = [9.59, 12.10, 13.19, 14.78, 15.58, 17.73]
    fee = [0.48, 0.47, 0.53, 0.59, 0.68, 0.71]
    f, (a1, a2) = plt.subplots(1, 2, figsize=WIDE)
    for ax, v, c, t, fmt, top in ((a1, ret, TEAL, "2024년 1년 수익률 (%)", "{:.1f}", 20),
                                  (a2, fee, INK, "총보수 (연 %)", "{:.2f}", 0.82)):
        bb = ax.bar(vin, v, color=c, width=0.6)
        for r_, x in zip(bb, v):
            ax.text(r_.get_x() + r_.get_width() / 2, x + top * 0.015, fmt.format(x),
                    ha="center", va="bottom", fontsize=14, fontweight="bold")
        ax.set_ylim(0, top); ax.set_title(t, fontsize=16, loc="left")
        ax.set_xlabel("빈티지 (TDF20XX)", fontsize=13); clean(ax); ax.tick_params(labelsize=13)
    f.tight_layout(w_pad=4)
    save(f, "vintage_ret_fee.png", note="자본시장연구원 이슈보고서 26-08 (2024년말 단순평균)")


# ── 04 · TDF 2.0 지도 ────────────────────────────────────────────
def tdf2_map():
    cells = [("① 동적 경로", ["경로에 폭을 두고", "시장 따라 조정"]),
             ("② 자산 다변화", ["사모·인프라·물가채", "미국 EO 14330"]),
             ("③ 하락 관리", ["변동성 목표", "은퇴 직전 방어"]),
             ("④ 저비용·ETF화", ["ETF로 채운 TDF", "상장 TDF ETF"]),
             ("⑤ 개인화", ["로보어드바이저", "관리계좌"]),
             ("⑥ 은퇴소득 결합", ["TIF · 연금 편입", "LifePath Paycheck"])]
    b = ""
    W_, H_, gx, gy = 500, 200, 30, 30
    for k, (t, sub) in enumerate(cells):
        x = 20 + (k % 3) * (W_ + gx); y = 20 + (k // 3) * (H_ + gy)
        b += bx(x, y, W_, H_, t, sub, kind="lime" if k == 5 else ("white" if k < 3 else "teal"))
    b += text(800, 520, "위 줄 — 무엇을 담나 · 아래 줄 — 누구에게 어떻게 돌려주나", 32, MUTED)
    svg("tdf2_map.png", b, w=1600, h=550)


# ── 04 · 정적 vs 동적 글라이드패스 ────────────────────────────────
def dynamic_gp():
    rng = np.random.default_rng(7)
    t = np.arange(0, 31)
    static = np.interp(t, [0, 10, 30], [80, 80, 40])
    z = np.zeros(len(t))
    for i in range(1, len(t)):
        z[i] = 0.75 * z[i - 1] + rng.normal(0, 0.65)
    dyn = static - np.clip(6 * z, -10, 10)
    f, ax = fig()
    ax.fill_between(t, static - 10, static + 10, color=TEAL, alpha=0.10)
    ax.plot(t, static, color=INK, lw=2.6, ls="--")
    ax.plot(t, dyn, color=TEAL, lw=3.2)
    ax.text(0.3, 92, "허용 폭 ±10%p", fontsize=14, color=TEAL)
    ax.text(16, 36, "정적 경로(점선) — 미리 정한 그대로", fontsize=15, color=INK)
    ax.text(3.0, 63, "동적 경로 — 비쌀 때 덜, 쌀 때 더", fontsize=15, color=TEAL,
            fontweight="bold")
    ax.set_xlim(0, 30); ax.set_ylim(20, 100)
    ax.set_xlabel("가입 후 경과 연수 (30년 뒤 은퇴)", fontsize=14)
    ax.set_ylabel("주식 비중 (%)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "dynamic_gp.png", note="가상 신호(밸류에이션 z점수)로 만든 예시")


# ── 04 · LifePath Paycheck 구조 ──────────────────────────────────
def paycheck():
    x0, x1, a0, a1 = 70, 1530, 25, 90
    X = lambda a: x0 + (a - a0) / (a1 - a0) * (x1 - x0)
    b = ""
    b += text(800, 56, "적립은 TDF가, 인출은 종신연금이 맡는다 — 한 상품 안에서", 36, INK, bold=True)
    b += f'<rect x="{X(25)}" y="100" width="{X(55)-X(25)}" height="130" rx="10" fill="{WHITE}" stroke="{HAIR}" stroke-width="2"/>'
    b += text((X(25) + X(55)) / 2, 178, "보통의 TDF로 적립", 36, INK, bold=True)
    b += f'<rect x="{X(55)}" y="100" width="{X(65)-X(55)}" height="130" rx="10" fill="#DDEBEA" stroke="{TEAL}" stroke-width="3"/>'
    b += text((X(55) + X(65)) / 2, 156, "평생소득", 32, TEAL, bold=True)
    b += text((X(55) + X(65)) / 2, 202, "10→30%", 32, TEAL, bold=True)
    b += f'<rect x="{X(65)}" y="100" width="{X(90)-X(65)}" height="130" rx="10" fill="{DARK}"/>'
    b += text((X(65) + X(90)) / 2, 156, "연금으로 평생 소득", 34, LIME, bold=True)
    b += text((X(65) + X(90)) / 2, 202, "+ 남은 TDF로 인출", 32, "#9FB0B2")
    b += f'<rect x="{X(59.5)}" y="260" width="{X(71)-X(59.5)}" height="90" rx="10" fill="{LIME}" stroke="{INK}" stroke-width="2"/>'
    b += text((X(59.5) + X(71)) / 2, 318, "연금 구매 창", 31, DARK, bold=True)
    b += text(X(71) + 20, 318, "59.5~71세에 연금을 살지 정한다", 30, INK, anchor="start")
    b += f'<line x1="{x0}" y1="400" x2="{x1}" y2="400" stroke="{MUTED}" stroke-width="2"/>'
    for a in (25, 40, 55, 65, 75, 90):
        b += f'<line x1="{X(a)}" y1="390" x2="{X(a)}" y2="410" stroke="{MUTED}" stroke-width="2"/>'
        b += text(X(a), 452, f"{a}세", 30, MUTED)
    b += text(800, 530, "TDF는 운용사, 연금은 보험사가 공급 · 미국 DC 플랜의 기본 상품(QDIA)으로 지정 가능", 30, MUTED)
    svg("paycheck.png", b, w=1600, h=570)


# ── 05 · 같은 55세, 세 사람 ───────────────────────────────────────
def personal():
    hf = 1.0
    who = ["공무원", "금융업 종사자", "창업자"]
    beta = [0.0, 0.3, 0.6]
    w = [max(PI_STAR * (1 + hf) - b_ * hf, 0) * 100 for b_ in beta]
    f, ax = fig()
    bb = ax.bar(who, w, color=[TEAL, MUTED, MUTED], width=0.55)
    for r_, x, b_ in zip(bb, w, beta):
        ax.text(r_.get_x() + r_.get_width() / 2, x + 1.5, f"{x:.0f}%", ha="center",
                fontsize=20, fontweight="bold")
        ax.text(r_.get_x() + r_.get_width() / 2, -9, f"β_H = {b_:.1f}", ha="center",
                fontsize=14, color=MUTED)
    ax.set_ylim(-12, 95); ax.set_ylabel("금융자산 중 주식 (%)", fontsize=14)
    ax.axhline(0, color=HAIR, lw=1)
    clean(ax); ax.tick_params(labelsize=16)
    ax.text(1.55, 80, "모두 55세 · H = F · π* = 39%", fontsize=15, color=MUTED)
    save(f, "personal.png", note="가상 계산 — w = π*(1 + H/F) − β_H·H/F")


# ── 05 · TDF에서 기관형 글라이드패스까지 ───────────────────────────
def evolution():
    b = ""
    b += text(800, 60, "같은 원리 — 미래 현금흐름의 현재가치가 위험자산 비중을 정한다", 36, INK, bold=True)
    xs = [20, 420, 820, 1220]
    items = [("TDF", ["적립기", "은퇴일 맞춰 축소"], "white"),
             ("TIF", ["인출기", "목표 소득 인출"], "white"),
             ("연금 결합", ["평생 소득", "장수 위험 이전"], "teal"),
             ("기관형", ["기금의 나이 H/F", "오후 IC 제1호"], "lime")]
    for x, (t, sub, k) in zip(xs, items):
        b += bx(x, 110, 360, 250, t, sub, kind=k)
    for x in xs[:-1]:
        b += arrow(x + 362, 235, x + 398, 235)
    b += text(800, 440, "개인은 월급(인적자본)이, 연기금은 보험료 수입(H)이 줄어드는 만큼 위험을 줄인다", 30, MUTED)
    svg("evolution.png", b, w=1600, h=480)


# ── 04 · 사모·부동산 편입 다섯 단계 ──────────────────────────────
def private_steps():
    steps = [("① 입력 보정", ["평활화 제거", "보수 차감"]),
             ("② 편입 판정", ["한계 샤프", "α > 0 ?"]),
             ("③ 비중", ["최적 비중과", "유동성 상한의 최소"]),
             ("④ 재원", ["베타 매칭", "주식·채권에서"]),
             ("⑤ 경로", ["빈티지별 κ", "순유출부터 축소"])]
    b = ""
    W_, gap = 268, 50
    for k, (t, sub) in enumerate(steps):
        x = 20 + k * (W_ + gap)
        b += bx(x, 120, W_, 260, t, sub, kind="lime" if k == 2 else ("teal" if k in (1, 3) else "white"),
                ts=36, ss=28)
        if k < 4:
            b += arrow(x + W_ + 6, 250, x + W_ + gap - 6, 250)
    b += text(800, 70, "앞 단계의 답이 다음 단계의 입력이 된다", 34, INK, bold=True)
    b += text(800, 450, "예시 가정 — 사모주식 순 초과수익 6% · 보정 변동성 25% · 주식과 상관 0.8 · γ 4", 28, MUTED)
    svg("private_steps.png", b, w=1600, h=500)


def denominator():
    w = np.linspace(0, 0.20, 201)
    f, ax = fig()
    for d, c_, lw, a in ((0.20, MUTED, 2, 0.8), (0.30, TEAL, 3.4, 1), (0.40, INK, 2, 0.8)):
        ax.plot(w * 100, w / (1 - d * (1 - w)) * 100, color=c_, lw=lw, alpha=a)
        ax.text(20.3, 0.20 / (1 - d * 0.8) * 100, f"상장자산 −{int(d*100)}%", fontsize=14,
                color=c_, va="center", fontweight="bold" if d == 0.30 else "normal")
    ax.plot(w * 100, w * 100, color=HAIR, lw=1.5, ls=":")
    ax.text(16.5, 15.6, "하락이 없을 때", fontsize=13, color=MUTED)
    ax.axhline(15, color=RED, ls="--", lw=2)
    ax.text(0.3, 15.6, "비유동 한도 15%", fontsize=14, color=RED)
    ax.axvline(11, color=TEAL, ls=":", lw=1.6)
    ax.plot([11], [15.0], "o", color=TEAL, ms=9)
    ax.annotate("평시 11% → 위기 직후 15%", xy=(11, 15), xytext=(2.2, 22), fontsize=15, color=TEAL,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.set_xlim(0, 24); ax.set_ylim(0, 30)
    ax.set_xlabel("평시 목표 비중 w (%)", fontsize=14); ax.set_ylabel("위기 직후 비유동 비중 (%)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "denominator.png", note="사모 평가는 그대로, 상장자산만 d만큼 하락한다고 가정")


def ill_path():
    ages = np.arange(25, 81)
    wbar = np.interp(ages, [25, 40, 65, 80], [80, 80, 40, 40])
    kappa = np.interp(ages, [25, 65, 72, 80], [0.137, 0.137, 0.05, 0.05])
    ill = kappa * wbar
    f, ax = fig()
    ax.plot(ages, wbar, color=INK, lw=2.6, label="위험자산 경로 w̄(τ)")
    ax.fill_between(ages, 0, ill, color=TEAL, alpha=0.30)
    ax.plot(ages, ill, color=TEAL, lw=3.2)
    ax.axhline(11, color=RED, ls="--", lw=1.8)
    ax.text(44, 12.6, "분모 효과 상한 11%", fontsize=14, color=RED)
    ax.axvline(65, color=MUTED, ls=":", lw=1.4)
    ax.text(65.5, 72, "은퇴 · 순유출 시작", fontsize=14, color=MUTED)
    ax.text(26, 83, "위험자산 경로 80% → 40%", fontsize=15, color=INK, fontweight="bold")
    ax.text(26, 18, "비유동 비중 = 0.137 × 80% ≈ 11%", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(68.5, 5.2, "κ 0.05 → 2%", fontsize=14, color=TEAL)
    ax.set_xlim(25, 80); ax.set_ylim(0, 92)
    ax.set_xlabel("나이", fontsize=14); ax.set_ylabel("비중 (%)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "ill_path.png", note="수업용 예시 — κ = 위험자산 가운데 비유동 자산의 몫")


def private_equations():
    equation(r"$\alpha_i=(\mu_i-r)-\beta_{i,P}\,(\mu_P-r)>0$", "eq_alpha.png", fontsize=44)
    equation(r"$w^{*}=\dfrac{1}{\gamma}\,\Sigma^{-1}(\mu-r)$", "eq_mv.png", fontsize=46)
    equation(r"$w_{\mathrm{stress}}=\dfrac{w}{1-d\,(1-w)}\leq c\quad\Leftrightarrow\quad w\leq\dfrac{c\,(1-d)}{1-d\,c}$",
             "eq_liqcap.png", fontsize=40)
    equation(r"$\Delta w_{\mathrm{eq}}=-\beta\,w,\qquad \Delta w_{\mathrm{bond}}=-(1-\beta)\,w$",
             "eq_funding.png", fontsize=42)
    equation(r"$w_{\mathrm{ill}}(\tau)=\kappa(\tau)\cdot\bar{w}(\tau)$", "eq_illpath.png", fontsize=46)


# ── 02 · 왜 TDF인가 — 투자기간별 최적 주식 비중 시뮬레이션 ─────────
# 시뮬레이션 (1)·(2) 표는 첨부 강의 「왜 TDF를 추천하는가: 시뮬레이션 기반 분석」의 결과를 옮긴 것이다.
HOR = [1, 3, 5, 10, 15, 20, 25, 30, 40, 50]
SIM1_AVG = [62, 72, 82, 92, 96, 98, 98, 100, 100, 100]
SIM2_AVG = [62, 66, 76, 84, 88, 92, 92, 94, 96, 100]
QP = dict(ms=0.10, ss=0.16, mb=0.045, sb=0.06, rho=0.0)   # 분위수 공식용 교육용 가정


def _qopt(T, q):
    from statistics import NormalDist
    z = NormalDist().inv_cdf(q)
    best, bv = 0, -9
    for w in np.round(np.arange(0, 1.01, 0.1), 1):
        m = w * QP["ms"] + (1 - w) * QP["mb"]
        v = (w * QP["ss"]) ** 2 + ((1 - w) * QP["sb"]) ** 2 + 2 * w * (1 - w) * QP["rho"] * QP["ss"] * QP["sb"]
        val = (m - v / 2) * T + z * np.sqrt(v * T)
        if val > bv: best, bv = w, val
    return best


def formula_avg():
    return [round(np.mean([_qopt(T, q) for q in (0.1, 0.2, 0.3, 0.4, 0.5)]) * 100) for T in HOR]


def glide_sim():
    fa = formula_avg()
    f, ax = fig()
    ax.plot(HOR, SIM1_AVG, color=MUTED, lw=2.4, marker="o", ms=7)
    ax.plot(HOR, SIM2_AVG, color=TEAL, lw=3.4, marker="o", ms=8)
    ax.plot(HOR, fa, color=RED, lw=2.2, ls="--", marker="s", ms=6)
    ax.invert_xaxis()
    ax.set_xlim(52, -1); ax.set_ylim(40, 105)
    ax.text(49, 101.5, "시뮬레이션 (1) — 통계 모형", fontsize=15, color=MUTED)
    ax.text(46, 84, "시뮬레이션 (2) — 부트스트랩", fontsize=15, color=TEAL, fontweight="bold")
    ax.text(46, 77, "분위수 공식 (다음 장)", fontsize=15, color=RED)
    ax.set_xlabel("남은 투자기간 (년) — 오른쪽으로 갈수록 은퇴에 가깝다", fontsize=14)
    ax.set_ylabel("평균 최적 주식 비중 (%)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "glide_sim.png", note="(1)·(2) 첨부 강의 결과 · 공식은 교육용 가정 μ 10/4.5% · σ 16/6% · ρ 0")
    print("   공식 평균:", fa)


def quantile_cross():
    from statistics import NormalDist
    z = NormalDist().inv_cdf(0.10)
    T = np.linspace(0.01, 30, 300)
    f, ax = fig()
    cols = {1.0: RED, 0.5: AMBER, 0.0: INK}
    labs = {1.0: "주식 100", 0.5: "주식 50 · 채권 50", 0.0: "채권 100"}
    offs = {1.0: 18, 0.5: -18, 0.0: 0}
    for w in (1.0, 0.5, 0.0):
        m = w * QP["ms"] + (1 - w) * QP["mb"]
        v = (w * QP["ss"]) ** 2 + ((1 - w) * QP["sb"]) ** 2
        y = 100 * np.exp((m - v / 2) * T + z * np.sqrt(v * T))
        ax.plot(T, y, color=cols[w], lw=3 if w != 0.5 else 2.2)
        ax.text(30.4, y[-1] + offs[w], labs[w], fontsize=14, color=cols[w], va="center", fontweight="bold")
    gs = QP["ms"] - QP["ss"] ** 2 / 2; gb = QP["mb"] - QP["sb"] ** 2 / 2
    Ts = (z * (QP["ss"] - QP["sb"]) / (gs - gb)) ** 2
    ys = 100 * np.exp(gb * Ts + z * QP["sb"] * np.sqrt(Ts))
    ax.axvline(Ts, color=TEAL, ls=":", lw=1.8)
    ax.plot([Ts], [ys], "o", color=TEAL, ms=10)
    ax.annotate(f"T* ≈ {Ts:.1f}년\n이후 주식 100이 하위 10%에서도 채권 100을 앞선다", xy=(Ts, ys),
                xytext=(1.0, 330), fontsize=15, color=TEAL, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.set_xlim(0, 38); ax.set_xlabel("투자기간 T (년)", fontsize=14)
    ax.set_ylabel("하위 10% 분위의 자산 (시작 = 100)", fontsize=14)
    clean(ax); ax.tick_params(labelsize=14)
    save(f, "quantile_cross.png", note="교육용 가정 μ 10/4.5% · σ 16/6% · ρ 0 · 로그정규 근사")
    print(f"   T* = {Ts:.2f}")


def sim_equations():
    equation(r"$W_T=W_0\,(1+g)^{T}$", "eq_compound.png", fontsize=48)
    equation(r"$w^{*}(T,q)=\arg\max_{w}\;Q_q\!\left[W_T(w)\right],\qquad \bar{w}(T)=\dfrac{1}{5}\sum_{q}w^{*}(T,q)$",
             "eq_qrule.png", fontsize=38)
    equation(r"$Q_q\!\left[\ln W_T(w)\right]=\ln W_0+g(w)\,T+z_q\,\sigma(w)\sqrt{T},\qquad g=\mu-\dfrac{\sigma^{2}}{2}$",
             "eq_qlog.png", fontsize=36)
    equation(r"$T^{*}=\left(\dfrac{z_q\,(\sigma_s-\sigma_b)}{g_s-g_b}\right)^{2}$", "eq_tstar.png", fontsize=44)


def equations():
    equation(r"$\pi^{*}=\dfrac{\mu-r}{\gamma\,\sigma^{2}}$", "eq_merton.png", fontsize=44)
    equation(r"$w=\pi^{*}\left(1+\dfrac{H}{F}\right)-\beta_{H}\,\dfrac{H}{F}$",
             "eq_lifecycle.png", fontsize=44)
    # 04 · 최신 기법 — 기법마다 핵심 식 하나
    equation(r"$w_t=\bar{w}(\tau)+\mathrm{clip}\left(\dfrac{\Delta\mu_t}{\gamma\,\sigma^{2}},\,-b,\,b\right)$",
             "eq_dynamic.png", fontsize=42)
    equation(r"$r_t=\dfrac{r^{*}_{t}-\phi\,r^{*}_{t-1}}{1-\phi},\qquad \sigma=\sigma^{*}\sqrt{\dfrac{1+\phi}{1-\phi}}$",
             "eq_unsmooth.png", fontsize=40)
    equation(r"$w_t=\bar{w}(\tau)\cdot\min\left(1,\,\dfrac{\sigma_{\mathrm{target}}}{\hat{\sigma}_t}\right)$",
             "eq_voltarget.png", fontsize=42)
    equation(r"$\dfrac{W_T^{(c)}}{W_T^{(0)}}=\left(\dfrac{1+r-c}{1+r}\right)^{T}\approx e^{-cT}$",
             "eq_fee.png", fontsize=42)
    equation(r"$a_x=\sum_{t=1}^{\infty}\,{}_{t}p_{x}\,v^{t},\qquad 1+r_{\mathrm{ann}}=\dfrac{1+r}{p_x}$",
             "eq_annuity.png", fontsize=40)
    # 05 · 확장
    equation(r"$H=\sum_{t=1}^{T}\dfrac{y}{(1+r_H)^{t}}=y\cdot\dfrac{1-(1+r_H)^{-T}}{r_H}$",
             "eq_humancap.png", fontsize=40)
    equation(r"$c=W_0\cdot\dfrac{r}{1-(1+r)^{-N}}$", "eq_withdraw.png", fontsize=44)
    equation(r"$w^{\mathrm{total}}=\dfrac{w_F}{1+H/F},\qquad w_h=\dfrac{h-\mu_s}{\mu_r-\mu_s}$",
             "eq_institution.png", fontsize=42)


if __name__ == "__main__":
    aum(); one_fund(); lifecycle(); glidepaths(); sequence()
    share(); default_option(); vintage_ret_fee()
    tdf2_map(); dynamic_gp(); paycheck(); personal(); evolution(); equations()
    private_steps(); denominator(); ill_path(); private_equations()
    glide_sim(); quantile_cross(); sim_equations()
