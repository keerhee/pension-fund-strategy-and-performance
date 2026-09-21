#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W07 M8 케이스 v3 도해 — 결정 트리 · 대차대조표 · 부채 벤치마크(LBP) · 오전 개념→오후 조건. SVG 1600×640 → PNG(cairosvg). 본문 글자 30px 이상(보조 26px)."""
import json, os, cairosvg
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE); IMG = f"{W}/img"; os.makedirs(IMG, exist_ok=True)
R = json.load(open(f"{W}/data/w7m8_results.json")); LI, AS, MK = R["liability"], R["assets"], R["market"]; OPT = {o["option"]: o for o in R["options"]}
NAVY, BLUE, GREEN, GRAY, BODY, MUTED, HAIR, RED, AMBER = "#1B2C5E", "#2E5BAA", "#3FA36F", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48", "#C77700"
F = "font-family='Noto Sans CJK KR, Apple SD Gothic Neo, sans-serif'"


def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def box(x, y, w, h, fill, stroke, lines, size=30, color=BODY, bold_first=True, rx=10):
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' stroke='{stroke}' stroke-width='2'/>"
    n = len(lines); lh = size * 1.32; y0 = y + h / 2 - lh * (n - 1) / 2 + size * 0.36
    for i, l in enumerate(lines):
        wt = "700" if (i == 0 and bold_first) else "400"
        s += f"<text x='{x + w/2}' y='{y0 + i*lh}' text-anchor='middle' font-size='{size}' font-weight='{wt}' fill='{color}' {F}>{esc(l)}</text>"
    return s


def arrow(x1, y1, x2, y2, color=MUTED, label=None, lx=None, ly=None):
    s = f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' stroke-width='3' marker-end='url(#ah)'/>"
    if label:
        s += f"<text x='{lx if lx is not None else (x1+x2)/2}' y='{ly if ly is not None else (y1+y2)/2 - 10}' text-anchor='middle' font-size='26' fill='{color}' {F}>{esc(label)}</text>"
    return s


HEAD = "<svg xmlns='http://www.w3.org/2000/svg' width='1600' height='640' viewBox='0 0 1600 640'><defs><marker id='ah' markerWidth='10' markerHeight='10' refX='9' refY='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='#6B7280'/></marker></defs><rect width='1600' height='640' fill='white'/>"


def out(name, s):
    open(f"{IMG}/{name}.svg", "w").write(s); cairosvg.svg2png(bytestring=s.encode(), write_to=f"{IMG}/{name}.png", output_width=3200); print("→", name)


# ── 결정 트리 ────────────────────────────────────────────────────────────────
A, B, C = OPT["A"], OPT["B"], OPT["C"]
s = HEAD
s += box(40, 30, 560, 100, GRAY, HAIR, ["조건 ① 갭 실재 + 부채 지표(LBP)가 있는가?", f"−100bp → FR_g {LI['FR_g']*100:.0f}% → {A['fr_g_down100']*100:.0f}% (임계 −5%p)"], 28, NAVY)
s += arrow(600, 80, 700, 80, label="지표 없음", lx=650, ly=60)
s += box(700, 30, 420, 100, "#FBEAEA", RED, ["탈락 — 안 A(현행)", "확인된 갭을 재지도 않는다"], 28, RED)
s += arrow(320, 130, 320, 190, label="예 · 안 B · 안 C", lx=440, ly=170)
s += box(40, 190, 560, 100, GRAY, HAIR, ["조건 ② 시장이 받아 주는가?", "현물 ≤ 장기물 발행 30%×5년 · IRS ≤ 연 거래 5%"], 28, NAVY)
s += arrow(600, 240, 700, 240, label="아니오", lx=650, ly=220)
s += box(700, 190, 420, 100, "#FBEAEA", RED, [f"탈락 — 안 C(IRS 명목 {C['irs_notional_trn']:,.0f}조)", f"상한 {MK['cap_irs_trn']}조의 {C['irs_vs_cap']:.1f}배"], 28, RED)
s += arrow(320, 290, 320, 350, label="예 · 안 B", lx=400, ly=332)
s += box(40, 350, 560, 100, GRAY, HAIR, ["조건 ③ 버퍼 · ④ 허들 · ⑤ 지침", "증거금 ≤ 유동자산 · μ ≥ 5.5% · 별표 1 · 파생 조항"], 28, NAVY)
s += arrow(600, 400, 700, 400, label="C 는 여기서도", lx=650, ly=380)
s += box(700, 350, 420, 100, "#FBEAEA", RED, [f"C — 증거금 {C['vm_3d_trn']:,.0f}조 > 유동자산 {AS['liquid_trn']:.0f}조", "지침에 파생 조항 없음"], 26, RED)
s += arrow(320, 450, 320, 520, label="예", lx=350, ly=505)
s += box(40, 520, 1080, 100, "#E6F5F0", GREEN, [f"기본 답 — 안 B: LBP 도입 + 헤지 {B['hedge_ratio']*100:.0f}%(현물 30년 {B['buy_bond_trn']:.0f}조 · 5년) 조건부 승인", f"갭 {B['gap_years']:.0f}년 · μ {B['mu_after_pct']:.2f}% · 증거금 0 · 남는 갭의 부담자를 의결문에 적는다"], 26, NAVY)
s += box(1160, 30, 400, 590, "#EAF1FB", BLUE, ["조건은 순서가 있다", "", "①이 '헤지할 갭이 있는가'를,", "②가 '얼마까지 가능한가'를,", "③④⑤가 '그 수단이 안전·", "합법한가'를 정한다", "", "A 는 ①에서, C 는 ②③⑤에서", "탈락한다", "", "→ 남는 답은 B, 그리고", "B 의 크기는 시장이 정한다"], 27, NAVY)
s += "</svg>"; out("tree_agenda1", s)

# ── 대차대조표 도해 — 자산 1,458 · 부채 두 눈금 · DV01 ────────────────────────────
s = HEAD
scale = 440 / LI["L_gov_down100_trn"]      # px per 조 (막대 최대 높이 440)
def bar(x, w, v, fill, label, sub, top=590):
    h = v * scale; y = top - h
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='{fill}'/>"
            f"<text x='{x+w/2}' y='{y-16}' text-anchor='middle' font-size='30' font-weight='700' fill='{NAVY}' {F}>{esc(label)}</text>"
            f"<text x='{x+w/2}' y='{top+38}' text-anchor='middle' font-size='26' fill='{BODY}' {F}>{esc(sub)}</text>")
F0 = 1458.0
s += f"<text x='40' y='60' font-size='34' font-weight='700' fill='{NAVY}' {F}>대차대조표 — 같은 자산, 세 개의 부채 눈금</text>"
s += bar(60, 200, F0, GREEN, f"A = {F0:,.0f}조", "적립금 2025년 말")
s += bar(340, 200, LI["L_hurdle_trn"], MUTED, f"L = {LI['L_hurdle_trn']:,}조", "자체 기준 5.5% · FR " + f"{LI['FR_h']*100:.0f}%")
s += bar(620, 200, LI["L_gov_trn"], NAVY, f"L = {LI['L_gov_trn']:,}조", "국채 곡선 · FR " + f"{LI['FR_g']*100:.0f}%")
s += bar(900, 200, LI["L_gov_down100_trn"], RED, f"L = {LI['L_gov_down100_trn']:,}조", "−100bp · FR " + f"{LI['FR_g_down100']*100:.0f}%")
s += f"<line x1='40' y1='590' x2='1140' y2='590' stroke='{MUTED}' stroke-width='2'/>"
s += box(1180, 100, 380, 490, "#EAF1FB", BLUE, ["금리 민감도(DV01)", "", f"부채 {LI['DV01_L_trn']:.2f}조/bp", f"(D_L {LI['D_L']:.0f}년 × {LI['L_gov_trn']:,}조)", "", f"자산 {AS['DV01_A_trn']:.2f}조/bp", f"(국내채권 288조 × D 5.5)", "", f"헤지 비율 {AS['hedge_ratio_0']*100:.0f}% · 갭 {AS['gap0_years']:.0f}년", "금리 1bp = 부채 7.4조"], 27, NAVY)
s += "</svg>"; out("balance_sheet", s)

# ── 부채 벤치마크(LBP) — 무엇을 담나 ─────────────────────────────────────────────
s = HEAD
cols = [("① 현금흐름 스케줄", "연도별 순유출 B_t − C_t", ["2026~2071 · 교육용 추계", "순유출 전환 2037", "정점·소진은 2025 재정추계에 맞춤", "→ 매년 갱신(재정추계 주기)"], "#EAF1FB", BLUE),
        ("② 할인 곡선", "국고채 곡선 = 시장 눈금", ["자체 5.5% 는 목표, 국채는 가격", f"FR_h {LI['FR_h']*100:.0f}% vs FR_g {LI['FR_g']*100:.0f}%", "두 숫자를 나란히 공시", "→ 할인율 층위를 섞지 않는다"], "#E6F5F0", GREEN),
        ("③ 민감도 프로파일", "키레이트 DV01 · 갭 · 헤지 비율", [f"DV01_L {LI['DV01_L_trn']:.1f}조/bp", f"갭 {AS['gap0_years']:.0f}년 · 헤지 비율 {AS['hedge_ratio_0']*100:.0f}%", "30년 구간에 민감도 집중", "→ 헤지 수단·크기의 근거"], GRAY, MUTED)]
for i, (t1, t2, body, fill, stroke) in enumerate(cols):
    x = 40 + i * 520
    s += f"<rect x='{x}' y='40' width='480' height='560' rx='12' fill='{fill}' stroke='{stroke}' stroke-width='2'/>"
    s += f"<text x='{x+240}' y='105' text-anchor='middle' font-size='34' font-weight='700' fill='{NAVY}' {F}>{esc(t1)}</text>"
    s += f"<text x='{x+240}' y='155' text-anchor='middle' font-size='28' fill='{MUTED}' {F}>{esc(t2)}</text>"
    for j, l in enumerate(body):
        s += f"<text x='{x+240}' y='{240 + j*62}' text-anchor='middle' font-size='30' fill='{BODY}' {F}>{esc(l)}</text>"
    s += f"<text x='{x+240}' y='560' text-anchor='middle' font-size='26' fill='{stroke if stroke != MUTED else NAVY}' font-weight='700' {F}>{['안건서 조건 ① 의 입력', '조건 ① 의 판정 눈금', '조건 ②·③ 의 입력'][i]}</text>"
s += "</svg>"; out("lbp_diagram", s)

# ── 오전 개념 → 오후 조건 ─────────────────────────────────────────────────────────
s = HEAD
rows = [("1교시 · 적립비율 FR = A/L · 할인율의 정치학", "조건 ① 갭의 실재 — 자체 5.5% 와 국채 곡선 나란히", BLUE),
        ("2교시 · 듀레이션 갭 · 면역화 3조건 · 2펀드", "조건 ② 시장 수용 — 매칭 포트폴리오를 살 시장이 있는가", GREEN),
        ("3교시 · 2022 영국 — 250bp 버퍼 · 5영업일", "조건 ③ 유동성 버퍼 — 3일 +200bp 증거금 ≤ 유동자산", RED),
        ("연금개혁 전제 5.5% · 기금운용지침 별표 1", "조건 ④ 허들 μ ≥ 5.5% · ⑤ 거버넌스(허용범위 · 파생 조항)", AMBER)]
for i, (l, r, c) in enumerate(rows):
    y = 40 + i * 145
    s += box(40, y, 700, 115, GRAY, HAIR, [l], 28, NAVY)
    s += arrow(740, y + 57, 830, y + 57, color=c)
    s += box(830, y, 730, 115, "#FFFFFF", c, [r], 28, BODY)
s += "</svg>"; out("concept_map", s)
print("svg done")
