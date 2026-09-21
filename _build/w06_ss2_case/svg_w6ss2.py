#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 SS2 케이스 v3 도해 — 결정 트리 2개 + 규칙의 해부 + 2026 타임라인. SVG 1600×640 → PNG(cairosvg). 본문 글자 30px 이상(주석 26px)."""
import json, os, cairosvg
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); IMG = f"{ROOT}/img"; os.makedirs(IMG, exist_ok=True)
R = json.load(open(f"{ROOT}/data/w6ss2_results.json")); A1, A2 = R["agenda1"], R["agenda2"]; OPT = A1["options"]; C3 = A1["cond3"]; C4 = A1["cond4"]
NAVY, BLUE, GREEN, GRAY, BODY, MUTED, HAIR, RED, ORANGE = "#1B2C5E", "#2E5BAA", "#3FA36F", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48", "#C77700"
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
    s += "</svg>"; open(f"{IMG}/{name}.svg", "w").write(s); cairosvg.svg2png(bytestring=s.encode(), write_to=f"{IMG}/{name}.png", output_width=3200); print("→", name)


# ── 제1호 결정 트리 ─────────────────────────────────────────────────────────
a, b, c = OPT["A"], OPT["B"], OPT["C"]
s = HEAD
s += box(40, 40, 560, 100, GRAY, HAIR, ["조건 ② 순 프리미엄 DR − 비용 > 0 ?", f"A {a['net_bp']:+.0f} · B {b['net_bp']:+.0f} · C {c['net_bp']:+.0f} bp"], 29, NAVY)
s += arrow(600, 90, 700, 90, label="아니오", lx=650, ly=68)
s += box(700, 40, 420, 100, "#FBEAEA", RED, ["탈락 — 해당 없음", "B&H 8.5bp 보다 셋 다 크다"], 26, RED)
s += arrow(320, 140, 320, 210, label="예 · 셋 다 통과", lx=440, ly=185)
s += box(40, 210, 560, 100, GRAY, HAIR, ["조건 ③ 복원 거래 ≤ 20 거래일 ?", f"현물 5% · 선물 20% 참여 (2026.6 갭 {A1['cond3_meta']['gap_pp']}%p)"], 29, NAVY)
s += arrow(600, 260, 700, 260, label="아니오", lx=650, ly=238)
s += box(700, 210, 420, 100, "#FBEAEA", RED, [f"탈락 — A {C3[0]['days_cash5pct_2026']:.0f}일 · C {C3[2]['days_cap25bp']}일", "현물로는 한 달 안에 못 끝낸다"], 26, RED)
s += arrow(320, 310, 320, 380, label=f"예 · B 선물 {C3[4]['days_fut20pct']:.0f}일", lx=440, ly=355)
s += box(40, 380, 560, 100, GRAY, HAIR, ["조건 ④ 위험자산 ≤ w_max 67.4% ?", f"CVaR95 ≥ −15% · 허용 드리프트 +{C4['band_max_pp']}%p"], 29, NAVY)
s += arrow(600, 430, 700, 430, label="아니오", lx=650, ly=408)
s += box(700, 380, 420, 100, "#FBEAEA", RED, [f"탈락 — A 분기 내 +{C4['drift_3m']['max']:.1f}%p", f"C 74% → CVaR {C4['cvar_2026_06']}%"], 26, RED)
s += arrow(320, 480, 320, 545, label="예", lx=350, ly=535)
s += box(40, 545, 1080, 85, "#E6F5F0", GREEN, [f"기본 답 — 안 B: 지침 밴드 ±3 월 점검 · 경계 복원 + 총 위험 ±2 선물 오버레이 · 현물 월 25bp 한도", f"순 {b['net_bp']:+.0f}bp · 드리프트 최대 +{b['risk_dev_max_pp']}%p · 조건 ⑤ 지침 별표 1 개정을 붙여 조건부 승인"], 24, NAVY)
s += box(1160, 40, 400, 590, "#EAF1FB", BLUE, ["조건은 순서가 있다", "", "②는 바닥(> 0)이지", "순위가 아니다 —", "③④를 넘은 안 중에서", "순 프리미엄이 큰 것", "", f"A 와의 격차 {a['net_bp']-b['net_bp']:.0f}bp 는", "'지킬 수 있는 규칙'의 값", "", "C 는 지키는 것이 없다", f"(2026 형 74% → {C4['cvar_2026_06']}%)"], 27, NAVY)
out("tree_agenda1", s)

# ── 제2호 결정 트리 — 기관별 흐름 ─────────────────────────────────────────────
ins = {r["code"]: r for r in A2["institutions"]}
s = HEAD
s += box(40, 40, 440, 100, GRAY, HAIR, ["조건 ③′ 비유동 지분 ≥ 80% ?", "(팔아서 비중을 맞출 자산이 있나)"], 28, NAVY)
s += arrow(480, 90, 640, 90, label="예 · 국부펀드", lx=560, ly=66)
s += box(640, 40, 440, 100, "#FBEAEA", RED, ["밴드 부적용", "집중 한도 · 유동성 계정 하한 · 연 1회"], 26, RED)
s += arrow(260, 140, 260, 210, label="아니오", lx=320, ly=185)
s += box(40, 210, 440, 100, GRAY, HAIR, ["조건 ③ 3%p 복원 > 20 거래일 ?", f"NPS {ins['NPS']['days_3pp']:.0f}일 · KIC {ins['KIC']['days_3pp']:.1f}일 · H대 0일"], 28, NAVY)
s += arrow(480, 260, 640, 260, label="예 · 국민연금", lx=560, ly=236)
s += box(640, 210, 440, 100, "#E6F5F0", GREEN, ["제1호 규칙 B", "밴드 ±3 + 총 위험 ±2 오버레이 · 월 · 한도"], 26, NAVY)
s += arrow(260, 310, 260, 380, label="아니오", lx=320, ly=355)
s += box(40, 380, 440, 100, GRAY, HAIR, ["조건 ④′ 현금흐름 ≥ ½σ(드리프트) ?", f"임계 {0.5*A2['drift_12m_sd']:.1f}%/년 · H대 3.0 · KIC 0"], 28, NAVY)
s += arrow(480, 430, 640, 430, label="예 · H대", lx=560, ly=406)
s += box(640, 380, 440, 100, "#E6F5F0", GREEN, ["현금흐름 우선 · 월 점검", f"지출·기부로 복원 → 잔여 현물 · 순 {ins['UNIV']['rule_best_net']:+.0f}bp"], 26, NAVY)
s += arrow(260, 480, 260, 545, label="아니오 · KIC", lx=340, ly=535)
s += box(40, 545, 1040, 85, "#E6F5F0", GREEN, [f"월말 목표 복원 · 현물 즉시(시장충격 0) — KIC 순 {ins['KIC']['rule_best_net']:+.0f}bp, NPS 규칙을 그대로 쓰면 {ins['KIC']['rule_nps_net']:+.0f}bp", "기본 답 — 안 B 지표 기반 차등: 네 기관 네 규칙, 지표는 하나의 표"], 25, NAVY)
s += box(1120, 40, 440, 590, "#EAF1FB", BLUE, ["규칙은 기관의 것이", "아니라 좌표의 것이다", "", "실행일수 · 현금흐름 ·", "비유동 비중 · 위험한도", "네 지표가 규칙을 정한다", "", "안 A(단일 규칙)는", "KIC 에서 DR 을 버리고", "H대에서 위험을 못 지키며", "국부펀드에는 적용이 안 된다", "", "안 C(자율)는 규칙이 없다"], 26, NAVY)
out("tree_agenda2", s)

# ── 규칙의 해부 — 다섯 다이얼 ───────────────────────────────────────────────────
s = HEAD
dials = [("① 자산군 밴드 폭", "b_class", ["지침 별표 1", "국내주식 ±3 · 해외 ±4", "국내채권 ±7 · 해외 ±0.5", "경계까지 복원(지침)"], "#EAF1FB", BLUE),
         ("② 총 위험 밴드", "b_total", ["기준포트폴리오 65 ± 2", "CVaR95 −15% 가 정한 폭", f"상한 {C4['w_max_pct']}% · 허용 +{C4['band_max_pp']}", "이탈 시 즉시 복원"], "#E6F5F0", GREEN),
         ("③ 점검 주기", "check", ["월 1회 (자산군 밴드)", "매일 (총 위험 밴드)", "전월 평균 비중 기준", "(2026.7 규칙 유지)"], GRAY, MUTED),
         ("④ 실행 한도", "cap", ["현물 월 25bp · 20영업일", f"= 일 {A1['cond3_meta']['cap_per_day_trn']}조", "시장충격 17bp 이내", "초과분은 이월"], "#FCF2E0", ORANGE),
         ("⑤ 수단", "instrument", ["현물(자산군 밴드)", "지수선물 오버레이(총 위험)", f"선물 20% 참여 → {C3[4]['days_fut20pct']:.0f}일", "순 익스포저 한도 ±3%p"], "#EAF1FB", BLUE)]
for i, (t1, t2, body, fill, stroke) in enumerate(dials):
    x = 30 + i * 312
    s += f"<rect x='{x}' y='40' width='292' height='560' rx='12' fill='{fill}' stroke='{stroke}' stroke-width='2'/>"
    s += f"<text x='{x+146}' y='100' text-anchor='middle' font-size='31' font-weight='700' fill='{NAVY}' {F}>{esc(t1)}</text>"
    s += f"<text x='{x+146}' y='145' text-anchor='middle' font-size='26' fill='{MUTED}' {F}>{esc(t2)}</text>"
    for j, l in enumerate(body):
        s += f"<text x='{x+146}' y='{235 + j*64}' text-anchor='middle' font-size='25' fill='{BODY}' {F}>{esc(l)}</text>"
    s += f"<text x='{x+146}' y='560' text-anchor='middle' font-size='26' font-weight='700' fill='{stroke if stroke != MUTED else NAVY}' {F}>{['조건 ① · ⑤', '조건 ④', '조건 ②', '조건 ③', '조건 ③ · ⑤'][i]}</text>"
out("rule_anatomy", s)

# ── 2026 타임라인 ──────────────────────────────────────────────────────────────
s = HEAD
s += f"<line x1='60' y1='330' x2='1540' y2='330' stroke='{NAVY}' stroke-width='4'/>"
ev = [("2025.12.30", "코스피 4,214", "국내주식 18.1% (264조)", NAVY, True), ("2026.1.26", "리밸런싱 한시 유예", "SAA 이탈해도 6월 말까지 안 판다", ORANGE, False),
      ("3.31", "코스피 5,052", "국내주식 21.0% (321조)", NAVY, True), ("5.28", "목표 14.9 → 20.8%", "SAA 밴드 ±3 → ±6(한시) · 25.8%+α", ORANGE, False),
      ("6.19 / 6.30", "장중 고점 9,386", "6월 말 29.1% (543조) · 유예 종료", NAVY, True), ("7.2", "리밸런싱 재개", "월 25bp · 20영업일 · 일 0.23조", ORANGE, False),
      ("7.7", "코스피 6,259 (−33%)", "국내주식 약 23.5% · 평가액 −142조", RED, True), ("9.18", "코스피 6,894", "기준일 — 규칙을 다시 정한다", GREEN, False)]
n = len(ev)
for i, (d, t1, t2, col, up) in enumerate(ev):
    x = 150 + i * (1300 / (n - 1))
    s += f"<circle cx='{x}' cy='330' r='14' fill='{col}'/>"
    y0 = 120 if up else 420
    s += f"<line x1='{x}' y1='{330 - 16 if up else 346}' x2='{x}' y2='{y0 + (100 if up else -10)}' stroke='{HAIR}' stroke-width='2'/>"
    s += f"<text x='{x}' y='{y0}' text-anchor='middle' font-size='27' font-weight='700' fill='{col}' {F}>{esc(d)}</text>"
    s += f"<text x='{x}' y='{y0+38}' text-anchor='middle' font-size='27' fill='{BODY}' {F}>{esc(t1)}</text>"
    s += f"<text x='{x}' y='{y0+74}' text-anchor='middle' font-size='24' fill='{MUTED}' {F}>{esc(t2)}</text>"
s += f"<text x='800' y='600' text-anchor='middle' font-size='28' font-weight='700' fill='{NAVY}' {F}>규칙을 끈 여섯 달 동안 비중은 +11%p, 규칙을 다시 켜기 전에 시장은 −33% — 리밸런싱은 '할까'가 아니라 '어떤 규칙으로'의 문제다</text>"
out("timeline_2026", s)
