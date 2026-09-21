#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W06 케이스 v3 도해 — 결정 트리 2개 + 글라이드패스 규칙. SVG 1600×640 → PNG(cairosvg). 본문 글자 30px 이상."""
import os, cairosvg
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = f"{os.path.dirname(HERE)}/img"
NAVY, BLUE, GREEN, GRAY, BODY, MUTED, HAIR, RED = "#1B2C5E", "#2E5BAA", "#3FA36F", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48"
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

# ── 제1호 결정 트리 ─────────────────────────────────────────────────────────
s = HEAD
s += box(40, 40, 560, 110, GRAY, HAIR, ["조건 ① H/F ≥ 0.625 인가?", "(향후 30년 보험료 PV ÷ 기금)"], 30, NAVY)
s += arrow(600, 95, 700, 95, label="예", lx=650, ly=75)
s += box(700, 40, 420, 110, "#EAF1FB", BLUE, ["지금 감축 근거 없음 (2026~41)", "총부 위험비중 30~39%"], 27) if False else ""
s += box(700, 40, 420, 110, "#EAF1FB", BLUE, ["지금 감축 근거 없음 (2026~41)", "총부 위험비중 30~39%"], 27)
s += arrow(320, 150, 320, 220, label="아니오 · 2042부터", lx=430, ly=195)
s += box(40, 220, 560, 110, GRAY, HAIR, ["조건 ② 종점 w ≥ w_h = 50% 인가?", "(μ ≥ 5.5%, 연금개혁 전제)"], 30, NAVY)
s += arrow(600, 275, 700, 275, label="아니오", lx=650, ly=250)
s += box(700, 220, 420, 110, "#FBEAEA", RED, ["탈락 — 안 C(종점 45%)", "μ 5.25% < 5.5%"], 28, RED)
s += arrow(320, 330, 320, 400, label="예", lx=350, ly=372)
s += box(40, 400, 560, 110, GRAY, HAIR, ["조건 ③ L_t ≤ 1년치 · ④ 소진 ≥ 2071", "· ⑤ 버퍼 ≥ 급여 1.5년치"], 30, NAVY)
s += arrow(600, 455, 700, 455, label="아니오", lx=650, ly=430)
s += box(700, 400, 420, 110, "#FBEAEA", RED, ["탈락 — 안 A(감축 없음)", "L 1.10년치 · 버퍼 1.4년치"], 28, RED)
s += arrow(320, 510, 320, 545, label="예", lx=350, ly=535)
s += box(40, 545, 1080, 85, "#E6F5F0", GREEN, ["기본 답 — 안 B: 2042년부터 연 1%p 감축, 종점 50%", "정점 2058 · 소진 2074 · L 0.76년치 · 버퍼 2.0년치"], 27, NAVY)
s += box(1160, 40, 400, 590, "#EAF1FB", BLUE, ["조건은 순서가 있다", "", "①이 시작 시점을,", "②가 종점을,", "③④⑤가 경로의", "안전성을 정한다", "", "C는 ①②에서,", "A는 ③⑤에서 탈락", "", "→ 남는 답은 B"], 28, NAVY, bold_first=True)
s += "</svg>"
open(f"{IMG}/tree_agenda1.svg", "w").write(s); cairosvg.svg2png(bytestring=s.encode(), write_to=f"{IMG}/tree_agenda1.png", output_width=3200)

# ── 제2호 결정 트리 ─────────────────────────────────────────────────────────
s = HEAD
s += box(40, 40, 480, 100, GRAY, HAIR, ["조건 ① 예측력 t_β ≥ 2 ?", "(10년 지평, Newey–West)"], 30, NAVY)
s += arrow(520, 90, 620, 90, label="아니오", lx=570, ly=65)
s += box(620, 40, 420, 100, "#FBEAEA", RED, ["기각 — 변동성 헤지", "t −1.57 · 캐리 140bp"], 28, RED)
s += arrow(280, 140, 280, 220, label="예 · 장기채 4.08 · TIPS 2.55", lx=470, ly=195)
s += box(40, 220, 480, 100, GRAY, HAIR, ["조건 ② |h_i| ≥ 5%p ?", "h = (1−1/γ)·β·σ_x/σ_a"], 30, NAVY)
s += arrow(520, 270, 620, 270, label="아니오", lx=570, ly=245)
s += box(620, 220, 420, 100, "#FFF4E5", "#C77700", ["조건부 — 예산 밖 시범", "(이번 결과에는 해당 없음)"], 26, BODY)
s += arrow(280, 320, 280, 400, label="예 · 장기채 +9.9 · TIPS +9.7", lx=470, ly=375)
s += box(40, 400, 480, 100, GRAY, HAIR, ["조건 ③ 캐리 비용 ≤ 30bp ?", "장기채 5 · TIPS 15 · 변동성 140"], 30, NAVY)
s += arrow(280, 500, 280, 545, label="예", lx=310, ly=535)
s += box(40, 545, 1000, 85, "#E6F5F0", GREEN, ["기본 답 — 채택 2: 장기채 오버레이 약 10%p + 물가연동채·실물 약 10%p", "조건 ④ 3년 손실 허용을 명문화해 조건부 승인"], 27, NAVY)
s += box(1080, 40, 480, 590, "#EAF1FB", BLUE, ["헤징 수요는", "'오늘의 수익'이 아니라", "'내일의 기회'를 산다", "", "그래서 조건 ④", "다년 손실 허용 없이는", "①~③을 통과해도", "실행이 안 된다", "", "γ=1 이면 헤징 수요 0", "— KIC 의 γ 가 5 라는", "전제가 답의 뿌리"], 27, NAVY)
s += "</svg>"
open(f"{IMG}/tree_agenda2.svg", "w").write(s); cairosvg.svg2png(bytestring=s.encode(), write_to=f"{IMG}/tree_agenda2.png", output_width=3200)

# ── 포기의 사다리 대신: '시간을 다루는 세 층' 도해 ───────────────────────────
s = HEAD
cols = [("1교시 · 시간분산", "같은 σ, 두 자", ["연환산 σ/√T 는 줄고", "누적 σ√T 는 는다", "→ 기금이 크면 '금액'이 문제", "(조건 ③)"], "#EAF1FB", BLUE),
        ("2교시 · 인적자본", "BMS 1992 의 기관판", ["H = 향후 30년 보험료 PV", "H/F 가 내려가면", "총부 위험비중이 올라간다", "(조건 ① 트리거)"], "#E6F5F0", GREEN),
        ("1교시 · ICAPM", "내일의 기회를 산다", ["헤징 수요 = (1−1/γ)·β·σx/σa", "예측력 t ≥ 2 인 상태변수만", "비용 ≤ 30bp", "(제2호 조건 ①~③)"], GRAY, MUTED)]
for i, (t1, t2, body, fill, stroke) in enumerate(cols):
    x = 40 + i * 520
    s += f"<rect x='{x}' y='40' width='480' height='560' rx='12' fill='{fill}' stroke='{stroke}' stroke-width='2'/>"
    s += f"<text x='{x+240}' y='105' text-anchor='middle' font-size='34' font-weight='700' fill='{NAVY}' {F}>{t1}</text>"
    s += f"<text x='{x+240}' y='155' text-anchor='middle' font-size='28' fill='{MUTED}' {F}>{t2}</text>"
    for j, l in enumerate(body):
        s += f"<text x='{x+240}' y='{240 + j*62}' text-anchor='middle' font-size='30' fill='{BODY}' {F}>{esc(l)}</text>"
    s += f"<text x='{x+240}' y='560' text-anchor='middle' font-size='26' fill='{stroke if stroke != MUTED else NAVY}' font-weight='700' {F}>{['제1호 조건 ③', '제1호 조건 ①', '제2호 조건 ①~③'][i]}</text>"
s += "</svg>"
open(f"{IMG}/three_layers.svg", "w").write(s); cairosvg.svg2png(bytestring=s.encode(), write_to=f"{IMG}/three_layers.png", output_width=3200)
print("svg → png: tree_agenda1, tree_agenda2, three_layers")
