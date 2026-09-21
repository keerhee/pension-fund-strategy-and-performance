#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M9 케이스 v3 도해 — 결정 트리 2개 + 버킷→조건 + Floor 정의 + Yale/H대 대비. SVG 1600×640 → PNG(cairosvg). 본문 글자 30px 이상."""
import json, os, cairosvg
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(HERE); IMG = f"{W}/img"; D = f"{W}/data"
R = json.load(open(f"{D}/w7m9_results.json")); d1 = R["case1"]["default"]; d2 = R["case2"]["default"]
NAVY, BLUE, GREEN, GRAY, BODY, MUTED, HAIR, RED, AMB = "#1B2C5E", "#2E5BAA", "#3FA36F", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48", "#C77700"
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


# ── 케이스 1 결정 트리 ────────────────────────────────────────────────────────
s = HEAD
s += box(40, 40, 520, 105, GRAY, HAIR, ["조건 ① P(W_T < G_S) ≤ 5% 인 x 는?", "(Safety 버킷 — 목표 미달 확률)"], 28, NAVY)
s += arrow(560, 92, 730, 92, label="x = 0.80", lx=645, ly=72)
s += box(730, 40, 400, 105, "#FBEAEA", RED, ["탈락 — m ≥ 2 에서 7.6~15.9%", "m = 1 만 통과(주식 31%)"], 27, RED)
s += arrow(300, 145, 300, 205, label="x = 0.90 · 1.00", lx=440, ly=182)
s += box(40, 205, 520, 105, GRAY, HAIR, ["조건 ③ P(W_T ≥ G_M) ≥ 70% 인가?", "(Market 버킷 — 원리금보장 3.09% 우위)"], 28, NAVY)
s += arrow(560, 257, 730, 257, label="x = 1.00", lx=645, ly=237)
s += box(730, 205, 400, 105, "#FBEAEA", RED, ["탈락 — 쿠션 18.5% 로 최대 68%", "(m = 2 · 수수료 0.5% 에서도)"], 27, RED)
s += arrow(300, 310, 300, 370, label="x = 0.90 · 수수료 ≤ 0.5%", lx=470, ly=347)
s += box(40, 370, 520, 105, GRAY, HAIR, ["조건 ② Cash Trap ≤ 10% · ④ 위반 ≤ 1%", "인 m 은?"], 28, NAVY)
s += arrow(560, 422, 730, 422, label="m ≥ 3", lx=645, ly=402)
s += box(730, 370, 400, 105, "#FBEAEA", RED, ["탈락 — m = 3 은 ① 10.0%", "m ≥ 5 는 ② 13~19% · ④ 1~11%"], 27, RED)
s += arrow(300, 475, 300, 535, label="m ≤ 2", lx=360, ly=522)
s += box(40, 535, 1090, 90, "#E6F5F0", GREEN, [f"기본 답 — Floor x = {d1['floor_x']:.2f} · 승수 m ≤ {d1['m_max']} · 연 총보수 ≤ {d1['fee_max']}%  (조건부 승인)", "① 3.6% · ② 0.1% · ③ 73% · ④ 0% — 조건 ⑤ '보장' 표현 금지 · 재심 트리거를 의결문에"], 27, NAVY)
s += box(1165, 40, 395, 585, "#EAF1FB", BLUE, ["조건은 순서가 있다", "", "①이 Floor 의 하한을,", "③이 Floor 의 상한과", "수수료 상한을,", "②④가 승수 상한을", "정한다", "", "x=1.00 은 ③에서,", "x=0.80 은 ①에서,", "m≥3 은 ①②④에서", "탈락 → 남는 답은 하나"], 27, NAVY)
out("tree_case1", s)

# ── 케이스 2 결정 트리 ────────────────────────────────────────────────────────
lk = {l["illiq_cap_pct"]: l["survival_years"] for l in R["case2"]["lockup"]}
s = HEAD
s += box(40, 40, 520, 105, GRAY, HAIR, ["조건 ① 락업 생존 연수 ≥ 10 인 x 는?", "(2022형 + 목돈 600억 + 캐피탈콜)"], 28, NAVY)
s += arrow(560, 92, 730, 92, label="x ≥ 30", lx=645, ly=72)
s += box(730, 40, 400, 105, "#FBEAEA", RED, [f"탈락 — 30%: {lk[30]}년 · 60%: {lk[60]}년", "Yale 형(60%)은 2년 만에 매도"], 26, RED)
s += arrow(300, 145, 300, 205, label=f"x ≤ 20 ({lk[20]}년 이상)", lx=460, ly=182)
s += box(40, 205, 520, 105, GRAY, HAIR, ["조건 ② 실질가치 유지 ≥ 50% 인 z 는?", "(세대 간 중립 · z ≥ 현행 4.0%)"], 28, NAVY)
s += arrow(560, 257, 730, 257, label="z = 5.25", lx=645, ly=237)
s += box(730, 205, 400, 105, "#FBEAEA", RED, ["탈락 — Yale 의 5.25% 는 46%", "x = 0 이면 4.0% 까지만"], 27, RED)
s += arrow(300, 310, 300, 370, label="x = 20 · z ≤ 4.5 (59%)", lx=470, ly=347)
s += box(40, 370, 520, 105, GRAY, HAIR, ["조건 ④ 3년 지출 유지 ≥ 95% 인 y 는?", "조건 ③ 직접 PE·VC 요건(인력 3 · 매니저 15)?"], 27, NAVY)
s += arrow(560, 422, 730, 422, label="y ≤ 25", lx=645, ly=402)
s += box(730, 370, 400, 105, "#FBEAEA", RED, ["y = 25%: 14% · 20%: 0% → 탈락", "직접 PE·VC 불가 → 펀드오브펀드"], 25, RED)
s += arrow(300, 475, 300, 535, label="y ≥ 30", lx=360, ly=522)
s += box(40, 535, 1090, 90, "#E6F5F0", GREEN, [f"기본 답 — 비유동 대체 상한 {d2['x']}%(펀드오브펀드 · 세컨더리) · 안전 유동자산 하한 {d2['y']}% · 지출률 {d2['z']}%", "80/20 평활 · 고정 지출 3.5% Floor · 조건 ⑤ 분모 효과 시 신규 약정 중단 — 조건부 승인"], 27, NAVY)
s += box(1165, 40, 395, 585, "#EAF1FB", BLUE, ["Yale 모델은 방향이 아니라", "네 숫자의 문제다", "", "①이 x 의 상한을,", "②가 z 의 상한을,", "④가 y 의 하한을,", "③이 대체의 형태를", "정한다", "", "Yale 형(60 · 5.25)은", "①②에서, GPFG 형(0)은", "②에서 4.0% 로 묶인다"], 27, NAVY)
out("tree_case2", s)

# ── 버킷 → 조건 도해 (케이스 1) ──────────────────────────────────────────────
s = HEAD
cols = [("Safety 버킷 (≥ 95%)", "은퇴 시 원금 + 연 1% = G_S 1.10", ["Floor = x · G_S · P(t,T)", "GHP(만기 매칭 국채)로 복제", "→ 조건 ① 목표 미달 ≤ 5%", "→ 조건 ④ 2022형 Floor 위반 ≤ 1%"], "#E6F5F0", GREEN),
        ("Market 버킷 (≥ 70%)", "원리금보장 3.09% 10년 = G_M 1.356", ["쿠션 C = W − F 에 m 배 PSP", "수수료가 쿠션에서 나간다", "→ 조건 ③ P(W_T ≥ G_M) ≥ 70%", "(수수료 상한을 정한다)"], "#EAF1FB", BLUE),
        ("Cash Trap (실무의 함정)", "쿠션 소진 → PSP 0% 락인", ["분기 리밸런싱: 1/m 손실에 깨짐", "m=2 50% · m=3 33% · m=6 17%", "→ 조건 ② Cash Trap ≤ 10%", "→ 조건 ⑤ '보장' 금지 · 재심"], GRAY, MUTED)]
for i, (t1, t2, body, fill, stroke) in enumerate(cols):
    x = 40 + i * 520
    s += f"<rect x='{x}' y='40' width='480' height='560' rx='12' fill='{fill}' stroke='{stroke}' stroke-width='2'/>"
    s += f"<text x='{x+240}' y='105' text-anchor='middle' font-size='34' font-weight='700' fill='{NAVY}' {F}>{esc(t1)}</text>"
    s += f"<text x='{x+240}' y='155' text-anchor='middle' font-size='27' fill='{MUTED}' {F}>{esc(t2)}</text>"
    for j, l in enumerate(body):
        s += f"<text x='{x+240}' y='{245 + j*68}' text-anchor='middle' font-size='30' fill='{BODY}' {F}>{esc(l)}</text>"
    s += f"<text x='{x+240}' y='560' text-anchor='middle' font-size='26' fill='{stroke if stroke != MUTED else NAVY}' font-weight='700' {F}>{['강의 1교시 · 2교시', '강의 3교시 (비용 0.8~1.5%)', '강의 2교시 (CPPI 의 한계)'][i]}</text>"
out("buckets_case1", s)

# ── Floor 정의 두 가지 (케이스 1 조건 ④) ─────────────────────────────────────
s = HEAD
s += box(40, 40, 740, 80, NAVY, NAVY, ["Floor = GHP 가격 (금리 연동)"], 32, "white")
s += box(820, 40, 740, 80, RED, RED, ["Floor = 고정 명목 원금"], 32, "white")
s += box(40, 140, 740, 200, "#E6F5F0", GREEN, ["금리 +300bp → 만기 매칭 국채 −21%", "Floor 도 같은 만큼 내려간다 (P(t,T) 하락)", "→ 쿠션 불변 · 위반 0% · '만기에 x·G_S' 는 그대로"], 28, BODY, bold_first=False)
s += box(820, 140, 740, 200, "#FBEAEA", RED, ["금리 +300bp → 국채 −21%, Floor 는 그대로", "→ x 1.00 이면 위반 100% · 쿠션 음수 · 즉시 락인", "'원금 보장' 이라 부르려면 보험사 자본이 필요하다"], 28, BODY, bold_first=False)
s += box(40, 370, 740, 230, GRAY, HAIR, ["무엇을 약속하는가", "\"은퇴 시점에 Safety 목표의 90% 를 확보하도록", "국채로 매칭해 운용한다\" — 목표 언어", "법령상 '원리금보장상품'이 아니다 → 조건 ⑤"], 27, NAVY)
s += box(820, 370, 740, 230, GRAY, HAIR, ["무엇을 약속하는가", "\"원금을 보장한다\" — 수익률 언어", "지급 능력이 있는 자만 쓸 수 있는 말", "디폴트옵션 안정형(원리금보장 85.4%)의 언어"], 27, NAVY)
out("floor_def", s)

# ── Yale vs H대 (케이스 2 조건 ③) ───────────────────────────────────────────
s = HEAD
hdr = ["", "Yale (공시)", "H대학교 (가상)", "조건에서의 뜻"]
rows = [["규모", "441억 달러 · 지출 21억", "5,000억 원 · 지출 200억", "최소 출자 100억 × 15 = 30%"],
        ["지평", "영구 — 그래도 2025년 세컨더리 매각", "목돈 600억 · 건축 · 소송", "조건 ① 락업 10년을 버티나"],
        ["접근권", "일류 PE·VC 의 초기 LP", "신규 LP · 실적 없음", "조건 ③ 직접 → 펀드오브펀드"],
        ["인력", "투자 전문 인력 수십 명", "대체 전담 1명", "조건 ③ 인력 ≥ 3"],
        ["지출 규칙", "5.25% · 80/20 평활 · 예산 1/3", "4.0% 현행 · 고정 지출 3.5%", "조건 ② z ≤ 4.5%"]]
cw = [220, 470, 430, 400]; xs = [40]
for w in cw[:-1]: xs.append(xs[-1] + w + 10)
for j, h in enumerate(hdr):
    s += box(xs[j], 40, cw[j], 70, NAVY if j else "white", NAVY if j else "white", [h], 28, "white" if j else NAVY)
for i, r in enumerate(rows):
    y = 125 + i * 100
    for j, c in enumerate(r):
        fill = GRAY if j == 0 else ("#EAF1FB" if j == 1 else ("#FBEAEA" if j == 2 else "#E6F5F0"))
        s += box(xs[j], y, cw[j], 88, fill, HAIR, [c], 26, NAVY if j == 0 else BODY, bold_first=(j == 0))
out("yale_vs_h", s)
print("svg → png done")
