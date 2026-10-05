# -*- coding: utf-8 -*-
"""롱온리 Das–Markowitz를 엑셀 '해 찾기'로 푸는 그림(시트 배치 · 대화창 · scipy 코드) — M8 강의본과 DMSS 제로원 덱이 함께 쓴다.
숫자: 상속 계정 H = −15%, α = 20%(z = 0.8416) — 롱온리 해 0 · 8.893 · 91.107%, 기대 23.67%, σ 45.94%, 하위 경계 −15.00%(scipy 검산).
사용: from solver_fig import solver_svg, layers_svg; png(solver_svg(), path)"""
import cairosvg

FONT = "Pretendard"; MONO = "Menlo"
INK, MUTED, TEAL, LIME, DARK, LINE, CARD = "#102027", "#64757D", "#0B6B68", "#B7F34A", "#071A1D", "#DDE3E2", "#F7F5F0"


def _esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, t, size=28, w="400", col=INK, anchor="start", font=FONT):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" xml:space="preserve">{_esc(t)}</text>')


def rect(x, y, w, h, fill="#FFFFFF", stroke=LINE, sw=2, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(body, W, H, bg=CARD):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs><marker id="ar" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">'
            f'<path d="M0,0 L12,6 L0,12 z" fill="{TEAL}"/></marker></defs>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def png(svg, path, W=None, H=None):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path, output_width=W, output_height=H)
    return path


def solver_svg(bg=CARD):
    W, H = 1800, 780
    b = ""
    # ── 왼쪽: 시트 배치
    b += T(20, 44, "① 시트 배치 — 상속 계정(H −15%, α 20%)", 30, "700", TEAL)
    rows = [("B2:B4", "비중 w (변수 셀)", "0 · 8.9 · 91.1%"),
            ("C2:C4", "기대수익 μ", "5% · 10% · 25%"),
            ("E2:G4", "공분산 Σ (3 × 3)", "원문 가상 자산 값"),
            ("B6", "=SUM(B2:B4)", "1"),
            ("B7", "=SUMPRODUCT(B2:B4,C2:C4)", "23.67%"),
            ("B8", "=MMULT(TRANSPOSE(B2:B4),MMULT(E2:G4,B2:B4))", "0.2111"),
            ("B9", "=SQRT(B8)", "45.94%"),
            ("B10", "=B7-NORM.S.INV(0.8)*B9", "−15.00%"),
            ("B11", "H (문턱)", "−15%")]
    x0, y0, cw = 20, 66, (120, 640, 230)
    b += rect(x0, y0, sum(cw), 50, DARK, DARK)
    for j, (h, xx) in enumerate(zip(("셀", "내용 · 수식", "값"), (0, cw[0], cw[0] + cw[1]))):
        b += T(x0 + xx + 14, y0 + 34, h, 26, "700", LIME)
    for i, r in enumerate(rows):
        y = y0 + 50 + i * 50
        b += rect(x0, y, sum(cw), 50, "#FFFFFF" if i % 2 == 0 else CARD)
        b += T(x0 + 14, y + 34, r[0], 26, "700")
        mono = r[1].startswith("=")
        b += T(x0 + cw[0] + 14, y + 34, r[1], 23 if mono else 26, "400", TEAL if mono else INK, font=MONO if mono else FONT)
        b += T(x0 + cw[0] + cw[1] + 14, y + 34, r[2], 26)
    # ── 오른쪽: 해 찾기 대화창
    dx, dy, dw, dh = 1050, 20, 730, 500
    b += rect(dx, dy, dw, dh, "#FFFFFF", "#9FB0B2", 3, 8)
    b += f'<rect x="{dx}" y="{dy}" width="{dw}" height="52" rx="8" fill="#E8ECEC"/>'
    b += T(dx + 24, dy + 36, "해 찾기 매개 변수", 28, "700")
    def field(y, lab, val, w=300):
        return T(dx + 28, y + 30, lab, 25) + rect(dx + 300, y, w, 42, "#FFFFFF", "#9FB0B2") + T(dx + 314, y + 30, val, 25, font=MONO)
    b += field(dy + 72, "목표 설정:", "$B$7")
    b += T(dx + 28, dy + 158, "대상:", 25) + (f'<circle cx="{dx+172}" cy="{dy+149}" r="11" fill="none" stroke="{TEAL}" stroke-width="3"/><circle cx="{dx+172}" cy="{dy+149}" r="5" fill="{TEAL}"/>'
      + T(dx + 192, dy + 158, "최대값", 25, "700", TEAL)
      + f'<circle cx="{dx+310}" cy="{dy+149}" r="11" fill="none" stroke="{MUTED}" stroke-width="3"/>' + T(dx + 330, dy + 158, "최소", 25, "400", MUTED)
      + f'<circle cx="{dx+420}" cy="{dy+149}" r="11" fill="none" stroke="{MUTED}" stroke-width="3"/>' + T(dx + 440, dy + 158, "지정값", 25, "400", MUTED))
    b += field(dy + 180, "변수 셀 변경:", "$B$2:$B$4")
    b += T(dx + 28, dy + 268, "제한 조건에 종속:", 25)
    b += rect(dx + 28, dy + 280, dw - 56, 76, "#FFFFFF", "#9FB0B2")
    b += T(dx + 44, dy + 310, "$B$6 = 1", 24, font=MONO) + T(dx + 44, dy + 344, "$B$10 >= $B$11", 24, font=MONO)
    b += rect(dx + 22, dy + 370, dw - 44, 46, LIME, LIME, 2, 4)
    b += (rect(dx + 40, dy + 381, 24, 24, "#FFFFFF", INK, 3) + f'<path d="M{dx+44},{dy+393} L{dx+51},{dy+401} L{dx+61},{dy+385}" fill="none" stroke="{INK}" stroke-width="4"/>'
      + T(dx + 78, dy + 402, "제한되지 않는 변수를 음이 아닌 수로 설정  ← 롱온리", 25, "700"))
    b += T(dx + 28, dy + 462, "해법 선택:", 25) + rect(dx + 200, dy + 432, 260, 42, "#FFFFFF", "#9FB0B2") + T(dx + 214, dy + 462, "GRG 비선형", 25)
    b += rect(dx + 560, dy + 432, 140, 42, TEAL, TEAL, 2, 4) + T(dx + 630, dy + 462, "해 찾기", 25, "700", "#FFFFFF", "middle")
    # ── 결과 비교
    ry = 540
    b += rect(dx, ry, dw, 104, "#FFFFFF")
    b += T(dx + 24, ry + 40, "체크 끔(공매도 허용) → −78.9 · 96.2 · 82.7%, 기대 26.35%", 25)
    b += T(dx + 24, ry + 84, "체크 켬(롱온리) → 0 · 8.9 · 91.1%, 기대 23.67%", 25, "700", TEAL)
    # ── 아래: scipy 코드
    cy0 = 580
    b += rect(20, cy0, 1010, 186, DARK, DARK)
    code = ["from scipy.optimize import minimize",
            "c = [{'type': 'eq', 'fun': lambda w: w.sum() - 1},",
            "     {'type': 'ineq', 'fun': lambda w: w@mu - 0.8416*np.sqrt(w@S@w) + 0.15}]",
            "r = minimize(lambda w: -w@mu, [1/3]*3, method='SLSQP',",
            "             bounds=[(0, 1)]*3, constraints=c)   # r.x → 0, 0.089, 0.911"]
    for i, c in enumerate(code):
        b += T(40, cy0 + 40 + i * 34, c, 21, "400", LIME if i == 0 else "#FFFFFF", font=MONO)
    b += T(dx, 690, "② 해 찾기 대화창 · ③ 같은 문제를 파이썬으로(왼쪽 아래)", 24, "700", MUTED)
    b += T(dx, 730, "bounds = (0, 1)이 엑셀의 ‘음이 아닌 수’ 체크와 같다", 24, "700", MUTED)
    return wrap(b, W, H, bg), W, H


def layers_svg(bg=CARD):
    """두 층 구조 — 자산 100 = floor 80 + 쿠션 20 → GHP 40 + 위험 블록 60(= Das–Markowitz 계정 합산)."""
    W, H = 1100, 500
    b = ""
    def col(x, title, parts):
        o = T(x + 120, 40, title, 28, "700", TEAL, "middle")
        y = 60
        for lab, val, h, fill, tc in parts:
            o += rect(x, y, 240, h, fill, fill if fill != "#FFFFFF" else LINE)
            o += T(x + 120, y + h / 2 + 4, lab, 26, "700", tc, "middle") + T(x + 120, y + h / 2 + 38, val, 26, "400", tc, "middle")
            y += h
        return o
    b += col(20, "자산 A = 100", [("쿠션 C", "100 − 80 = 20", 80, LIME, INK), ("floor F", "필수 목표의 현재가치 80", 340, "#FFFFFF", INK)])
    b += f'<line x1="270" y1="100" x2="420" y2="160" stroke="{TEAL}" stroke-width="4" marker-end="url(#ar)"/>'
    b += T(345, 112, "× m = 3", 26, "700", TEAL, "middle")
    b += col(430, "실제 보유", [("위험 블록 E", "3 × 20 = 60", 240, DARK, "#FFFFFF"), ("GHP", "100 − 60 = 40", 180, "#FFFFFF", INK)])
    b += f'<line x1="680" y1="180" x2="770" y2="180" stroke="{TEAL}" stroke-width="4" marker-end="url(#ar)"/>'
    b += rect(780, 60, 300, 240, "#FFFFFF")
    b += T(930, 96, "위험 블록 안 — Das–Markowitz", 22, "700", TEAL, "middle")
    for i, t in enumerate(["은퇴 · 교육 · 상속", "계정별 (H, α)로 풀어", "60 · 20 · 20으로 합산", "채권 39.9 · 저위험 24.7", "· 고위험 35.4%(롱온리)"]):
        b += T(930, 140 + i * 34, t, 23, "400", INK, "middle")
    b += T(930, 350, "얼마나 위험을 지나 → CPPI", 24, "700", MUTED, "middle")
    b += T(930, 386, "무엇으로 지나 → Das–Markowitz", 24, "700", MUTED, "middle")
    return wrap(b, W, H, bg), W, H
