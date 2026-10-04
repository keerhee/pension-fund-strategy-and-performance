"""W01 EP.06 '위험은 사라지지 않는다' — DB와 DC. 약속의 형태가 다르면 굴리는 방법이 다르다.
DB: 잉여금 A − L의 출렁임 최소화(자산 100 · 부채 80 → 잉여 20, 가정) · DC: 목표액 미달 확률 최소화 — W6 LDI · GBI 복선.
위험은 사라지지 않는다 — 누가 지느냐만 달라진다. (W01 강의본 15 · 16 · 17장 · 기획표 순서 6 그대로)"""
from wkit import *

TEX = [r"S = A - L = 100 - 80 = 20",
       r"\mathrm{FR} = A / L = 100 / 80 = 1.25",
       r"A: 100 \rightarrow 90 \quad \Rightarrow \quad S = 90 - 80 = 10"]
EQ = [f"eq/ep06_{i}.png" for i in (1, 2, 3)]
for f, tx in zip(EQ, TEX):
    if len(sys.argv) > 1 or not os.path.exists(f): latex_png(tx, f)

COLS = [("DB — 확정급여", "지급액을 미리 약속", "위험: 사용자 · 정부", "목표: A − L 출렁임 최소화", "W6 LDI", BLUE),
        ("DC — 확정기여", "넣어줄 금액만 약속", "위험: 근로자 본인", "목표: 목표액 미달 확률 최소화", "W6 GBI", GREEN)]


def cut1(t): return title(t, "EP.06 · 위험은 사라지지 않는다", 960)


def cut2(t):
    body = (label("퇴직연금 제도 변경 안내", 0, -110, 36, "#555", 800)
            + punch("DB → DC 전환", 0, 0, 80, fill=ORANGE, sw=10)
            + label("펭: “이제 회사는 위험 끝!”", 0, 150, 38, BLUE, 900))
    return problem(t, "위험 끝?", ORANGE, "#FBE9DF", "회사 공지", body, ["DC로 바꾸면 위험이", "없어지는 거죠?"], "위험 0?")


def cut3(t): return twist(t, ["위험은 사라지지 않아.", "누가 지느냐만 달라질 뿐이야."], "위험 이동!", size=46, sfx_size=150)


def col_card(t, a0, x, cols):
    nm, promise, who, goal, tag, c = cols
    g = back(prog(t, a0, .45))
    if g <= 0: return ""
    return (f'<g transform="translate({x},545) scale({g:.3f})"><rect x="-225" y="-165" width="450" height="330" rx="20" fill="#fff" stroke="{c}" stroke-width="7"/>'
            f'<rect x="-225" y="-165" width="450" height="76" rx="20" fill="{c}"/><rect x="-225" y="-110" width="450" height="21" fill="{c}"/>'
            + label(nm, 0, -127, 32, "#fff", 900) + label(promise, 0, -45, 27, NAVY, 800)
            + label(who, 0, 10, 28, RED, 900) + label(goal, 0, 65, 24 if len(goal) > 14 else 26, NAVY, 800)
            + f'<rect x="-75" y="100" width="150" height="44" rx="12" fill="{c}"/>' + label(tag, 0, 122, 24, "#fff", 900) + "</g>")


def cut4(t):
    s = explainer_frame(t, "위험은 누가 지나", "약속의 형태가 다르면 굴리는 방법이 다르다")
    s.append(col_card(t, .4, 295, COLS[0]))
    s.append(col_card(t, 1.0, 785, COLS[1]))
    s.append(chip("DB 손계산 — 자산 100 · 부채 80 (가정)", 540, 770, BLUE, back(prog(t, 2.2, .4)), w=760, size=32))
    s.append(eq_img(EQ[0], 540, 825, ease_out(prog(t, 2.8, .5)), scale=.58))
    s.append(eq_img(EQ[1], 540, 915, ease_out(prog(t, 3.4, .5)), scale=.58))
    s.append(f'<g opacity="{ease_out(prog(t, 3.8, .4)):.2f}">' + label("잉여금 20 · 적립비율 125%", 540, 1015, 30, BLUE, 900) + "</g>")
    s.append(eq_img(EQ[2], 540, 1050, ease_out(prog(t, 4.4, .5)), scale=.52))
    s.append(f'<g opacity="{ease_out(prog(t, 4.8, .4)):.2f}">' + label("자산 −10%에 잉여금은 반 토막 — 메우는 건 회사 · 정부", 540, 1150, 29, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 5.4, .4)):.2f}">' + label("DC라면 같은 −10%가 내 계좌에서 그대로 빠진다", 540, 1220, 29, GREEN, 900) + "</g>")
    s.append(chip("ALM · LDI · 면역화  vs  TDF · GBI · 글라이드패스", 540, 1300, NAVY, back(prog(t, 6.0, .4)), w=900, size=30))
    s += explainer_tail(t, "위험은 사라지지 않는다 — 누가 지느냐만 바뀐다", "그 “누가”가 운용의 목적함수를 정한다",
                        ["DB는 회사가, DC는 내가", "그 출렁임을 떠안아."], a0=7.2, red_size=40)
    return s


def cut5(t): return relief(t, ["그럼 NPS는", "DB예요, DC예요?"], ["명목 DB, 실질 DC적 요소야. 급여산식은", "법에, 조정 장치는 정치에 있어."],
                           "명목 DB!", "체크: 위험 부담자 · 운용 목표 · 자산배분 언어", a_size=42, chip_size=32, sfx_size=120)


def cut6(t): return next_cut(t, "#8A5A00", "약속이 이자를 넘을 때", "부채를 진 다른 부족은?", topic_size=105)


META = dict(
    episode="EP.06", title="위험은 사라지지 않는다",
    concept="DB와 DC — 약속의 형태가 다르면 굴리는 방법이 다르다. DB(확정급여)는 지급액을 약속하고 투자위험은 사용자 · 정부가 진다: 목표는 잉여금 A − L의 출렁임 최소화(W6 LDI). 자산 100 · 부채 80이면 잉여 20 · 적립비율 125%, 자산이 10% 빠지면 잉여금은 10으로 반 토막(가정). DC(확정기여)는 기여만 약속하고 위험은 근로자 본인이 진다: 목표는 목표액 미달 확률 최소화(W6 GBI). 위험은 사라지지 않는다 — 누가 지느냐만 달라진다. NPS는 명목 DB, 실질 DC적 요소",
    source="W01 강의본 15장(DB와 DC — 수식 없이 먼저, 위험은 사라지지 않는다 — 누가 지느냐만 달라진다) · 16장(두 개의 다른 수학 — Surplus = A − L · Funding Ratio = A/L, DB는 A−L 출렁임 최소화(W6 LDI) · DC는 목표액 미달 확률 최소화(W6 GBI)) · 17장(세 가지 차이 — 위험 부담자 · 운용 목표 · 자산배분 언어(ALM · LDI · 면역화 vs TDF · GBI · 글라이드패스), NPS는 “명목 DB, 실질 DC적 요소” — 급여산식은 법에, 조정 메커니즘은 정치에) · 기획표 순서 6",
    cuts=[{"n": 2, "notice": "회사 공지 · 퇴직연금 제도 변경 안내 · DB → DC 전환 · 펭: “이제 회사는 위험 끝!”", "bubble": ["DC로 바꾸면 위험이", "없어지는 거죠?"], "sfx": "위험 0?"},
          {"n": 3, "bubble": ["위험은 사라지지 않아.", "누가 지느냐만 달라질 뿐이야."], "sfx": "위험 이동!"},
          {"n": 4, "columns": [c[:5] for c in COLS], "latex": TEX,
           "labels": ["잉여금 20 · 적립비율 125%", "자산 −10%에 잉여금은 반 토막 — 메우는 건 회사 · 정부", "DC라면 같은 −10%가 내 계좌에서 그대로 빠진다"],
           "chips": ["DB 손계산 — 자산 100 · 부채 80 (가정)", "ALM · LDI · 면역화  vs  TDF · GBI · 글라이드패스"],
           "summary": "위험은 사라지지 않는다 — 누가 지느냐만 바뀐다", "bubble": ["DB는 회사가, DC는 내가", "그 출렁임을 떠안아."]},
          {"n": 5, "bubbles": [["그럼 NPS는", "DB예요, DC예요?"], ["명목 DB, 실질 DC적 요소야. 급여산식은", "법에, 조정 장치는 정치에 있어."]], "sfx": "명목 DB!"},
          {"n": 6, "text": ["다음 화", "약속이 이자를 넘을 때", "부채를 진 다른 부족은?"]}],
    check={"S": 20, "FR": 1.25, "S_after_A-10%": 10},
    **{"fact-check": "자산 100 · 부채 80은 기획표의 가정 숫자(강의본 16장은 수식 Surplus = A − L · Funding Ratio = A/L만 제시). 자산 −10% 충격(A 100 → 90, 부채 불변)은 이 화에서 덧붙인 설명용 가정 — 실제로는 금리가 움직이면 부채 L도 같이 움직인다(그래서 W6 LDI가 A와 L을 함께 맞춘다). NPS '명목 DB, 실질 DC적 요소'는 강의본 17장의 해석(법적 분류가 아님 — 덱 표기). DC 디폴트옵션(2023~)은 17장 표기, 원자료 미확인."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "06", META)
