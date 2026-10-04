"""시즌 2 「지킬 것부터 사라」 EP.B2 '디폴트옵션에 Flexicure를?' — 9:16 웹툰 숏폼. (IC 보너스 2 — W06 M8 케이스 1부)
K퇴직연금(가상) Flexicure형 등록 심의 · 표준 가입자 55→65세 · 초기 1.00 · G_S = 1.01¹⁰ ≈ 1.10. 세 숫자 Floor x · 승수 m · 총보수 c를 판정 조건으로 거른다.
① 목표 미달 ≤ 5%: m 2 3.6% · m 3 10.0% / ② Cash Trap ≤ 10%: m 2 0.1% · m 6 19.2% / ③ 수수료 후 Market ≥ 70%: 0.5% 73% · 0.8% 67% /
④ 2022형 충격 위반 ≤ 1%: GHP 연동 0% · 고정 100% → 기본 답 x 0.90 · m ≤ 2 · c ≤ 0.5% 조건부 승인. 반면교사 2022 TDF −16.9% · LTCM 27배.
(케이스 덱 1부 2~3장 · 강의본 36장·부록 그대로 — 결론은 학생 덱 2장 '표결 후 공개')"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/epB2_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.B2 · 디폴트옵션에 Flexicure를?", chip_w=980)
    s.insert(2, punch("시즌 2 · IC 보너스", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 세 숫자를 전부 최대로?
    s = [bg("#E9F1E4")]
    s.append(punch("다 최대로!", 540, 170, 120, fill=GREEN, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{GREEN}"/><rect x="-390" y="-180" width="780" height="26" fill="{GREEN}"/>'
                 + label("IC · K퇴직연금(가상) Flexicure형 등록", 0, -202, 38, "#fff", 900)
                 + label("펭의 발의안", 0, -110, 38, GREY, 900)
                 + label("Floor x", -250, -30, 36, "#555", 800) + punch("100%", -250, 50, 74, fill=BLUE, sw=9)
                 + label("승수 m", 0, -30, 36, "#555", 800) + punch("6", 0, 50, 74, fill=ORANGE, sw=9)
                 + label("총보수 c", 250, -30, 36, "#555", 800) + punch("1.5%", 250, 50, 74, fill=RED, sw=9)
                 + label("“원금 보장 + 고수익” 문구 포함", 0, 170, 34, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("최강 조합!", 770, 975, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["가장 안전하고 가장 많이 벌게", "셋 다 최대로 하면 되죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=48))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["세 숫자는 서로 싸워. 조건으로 거르면", "x 0.90 · m ≤ 2 · 보수 ≤ 0.5%만 남아."], 540, 330, 1030, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=42))
    if t > 3.2:
        s.append(punch("좌표로 표결!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


COLX = [250, 520, 700, 890]
ROWS = [("① 목표 미달", "≤ 5%", "m 2 · 3.6%", "m 3 · 10.0%"),
        ("② Cash Trap", "≤ 10%", "m 2 · 0.1%", "m 6 · 19.2%"),
        ("③ 수수료 후 Market", "≥ 70%", "0.5% · 73%", "0.8% · 67%"),
        ("④ 2022형 충격 위반", "≤ 1%", "GHP 연동 0%", "고정 100%")]


def cut4(t):   # 해설: 판정 조건 표 → 답 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("판정 조건으로 거르기", 540, 150, 96, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("표준 가입자 55→65세 · 초기 1.00 · 4,000 경로 (케이스)", 540, 275, 32, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("조건", COLX[0], 390, 28, NAVY, 900) + label("임계", COLX[1], 390, 28, NAVY, 900)
             + label("통과", COLX[2], 390, 28, GREEN, 900) + label("탈락", COLX[3], 390, 28, RED, 900)
             + f'<line x1="80" y1="420" x2="1000" y2="420" stroke="{NAVY}" stroke-width="3"/></g>')
    for r, (name, th, ok, ng) in enumerate(ROWS):
        y = 465 + 66 * r
        g = ease_out(prog(t, 1.0 + .8 * r, .4))
        s.append(f'<g opacity="{g:.2f}">' + label(name, COLX[0], y, 27, NAVY, 900) + label(th, COLX[1], y, 28, GREY, 900)
                 + label(ok, COLX[2], y, 27, GREEN, 900) + label(ng, COLX[3], y, 27, RED, 900) + "</g>")
    s.append(chip("기본 답: x 0.90 · m ≤ 2 · 총보수 ≤ 0.5% 조건부", 540, 760, GREEN, back(prog(t, 4.4, .4)), w=900, size=32))
    for i, (y, sc) in enumerate(((825, .44), (920, .46), (1020, .46))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.0 + .8 * i, .5)), scale=sc))
    s.append(chip("‘보장’ 문구 금지 · GHP 연동 · 재심 트리거 (조건 ⑤)", 540, 1170, NAVY, back(prog(t, 7.4, .4)), w=860, size=30))
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("Floor는 낮추고, m은 묶고, 보수는 깎는다", 540, 1400, 46, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("이름(‘Flexicure형’)이 아니라 좌표(x · m · c)로 승인한다", 540, 1480, 32, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["EP.14의 1/m, EP.15의 Cash Trap이", "그대로 표결 숫자가 돼."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=42))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: Floor x · 승수 m · 총보수 c · ‘보장’ 금지 · 재심 트리거", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=940, size=33)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["이렇게까지 조심할", "이유가 있어요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["2022년 TDF는 −16.9%였고, LTCM은", "매트 없이 27배 레버리지로 뛰었지."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("매트부터!", 330, 740, 120, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, "#6B3FA0", "Yale 모델", "대학기금이 흉내 낼 수 있나?", topic_size=160)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_epB2.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
