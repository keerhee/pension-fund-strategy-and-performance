"""W06 「지킬 것부터 사라」 EP.02 '같은 약속, 다른 무게' — 9:16 웹툰 숏폼.
20년 뒤 100의 현재가치: 5%면 37.7, 3%면 55.4(+47%). 국민연금 순부채는 자체 5.5% 눈금으로 1,542조(FR 95%),
국채 곡선 눈금으로 2,122조(FR 69%) — 같은 약속이 1.4배. (W06 M7 1교시 숫자 그대로, EP.01 적립비율을 이어받음)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30.5), (30.5, 37.5), (37.5, 41)]
DUR = 41
EQ = [f"eq/ep02_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
PURPLE = "#6B3FA0"


def cut1(t):
    s = title_cut(t, "EP.02 · 같은 약속, 다른 무게", chip_w=900)
    s.insert(2, punch("W06 · 지킬 것부터 사라", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 같은 국민연금 부채가 보고서마다 다르다
    s = [bg("#F6E7D8")]
    s.append(punch("부채가 두 개?", 540, 170, 110, fill=ORANGE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{NAVY}"/><rect x="-390" y="-180" width="780" height="26" fill="{NAVY}"/>'
                 + label("IC 질의 · 국민연금 순부채는?", 0, -202, 42, "#fff", 900)
                 + label("보고서 A", -190, -70, 40, "#555", 800) + punch("1,542조", -190, 20, 76, fill=GREEN, sw=10)
                 + label("보고서 B", 190, -70, 40, "#555", 800) + punch("2,122조", 190, 20, 76, fill=RED, sw=10)
                 + label("같은 급여 약속 · 같은 기간 (2026~2071)", 0, 160, 38, NAVY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("580조 차이?!", 760, 965, 70, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["같은 약속인데", "누구 계산이 틀린 거예요?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["둘 다 맞아. 할인율이라는", "눈금이 다를 뿐이야."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=48))
    if t > 3.2:
        s.append(punch("눈금은 정치!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE = 820


def bar(t, a0, x, v, k, c, val, name):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = v * k * g
    o = [f'<rect x="{x-60}" y="{BASE-h:.0f}" width="120" height="{h:.0f}" fill="{c}" rx="6"/>']
    if g > .9:
        o.append(label(val, x, BASE - v * k - 30, 38, c, 900))
        o.append(label(name, x, BASE + 40, 30, NAVY, 800))
    return "".join(o)


def cut4(t):   # 해설: 20년 뒤 100의 PV 막대 → 국민연금 두 눈금 막대 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("눈금 바꿔 보기", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("현재가치 = 미래 약속 ÷ (1 + 할인율)", 822, 275, 38, NAVY, 700, anchor="end") + label("t", 828, 260, 26, NAVY, 800, anchor="start") + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(f'<line x1="540" y1="380" x2="540" y2="{BASE}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8" opacity="{ease_out(prog(t, 2.6, .4)):.2f}"/>')
    # 왼쪽: 20년 뒤 100
    s.append(f'<g opacity="{ease_out(prog(t, .5, .4)):.2f}">' + label("20년 뒤 100 (예시)", 295, 400, 36, NAVY, 900) + "</g>")
    s.append(bar(t, .7, 220, 37.7, 6, GREEN, "37.7", "할인율 5%"))
    s.append(bar(t, 1.3, 380, 55.4, 6, RED, "55.4", "할인율 3%"))
    s.append(chip("+47%", 380, BASE + 120, RED, back(prog(t, 1.9, .4)), w=200, size=40))
    # 오른쪽: 국민연금 순부채
    s.append(f'<g opacity="{ease_out(prog(t, 2.8, .4)):.2f}">' + label("국민연금 순부채", 785, 400, 36, NAVY, 900) + "</g>")
    s.append(bar(t, 3.0, 700, 1542, .16, GREEN, "1,542조", "자체 5.5%"))
    s.append(bar(t, 3.6, 870, 2122, .16, RED, "2,122조", "국채 곡선"))
    s.append(chip("FR 95%", 700, BASE + 120, GREEN, back(prog(t, 4.2, .4)), w=160, size=34))
    s.append(chip("FR 69%", 870, BASE + 120, RED, back(prog(t, 4.5, .4)), w=160, size=34))
    for i, y in enumerate((1010, 1120, 1230)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.3 + .8 * i, .5)), scale=.5))
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("같은 약속도 눈금에 따라 1.4배", 540, 1440, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("같은 적립금인데 적립비율 95% ↔ 69%", 540, 1515, 36, NAVY, 700) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["먼 약속일수록 할인율 차이가", "해마다 곱해져서 커져."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 실무 답(CalPERS) + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 할인율 근거 · 국채 기준 적립비율 · 적립배율과 구분", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=34)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 할인율을 높게", "잡으면 되잖아요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["부채가 작아 보일 뿐이야. CalPERS는", "7.5%를 6.8%로 내리느라 몇 년을 싸웠어."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=42))
    if t > 3.6:
        s.append(punch("숨긴다고 안 줄어!", 540, 740, 92, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, PURPLE, "숨은 공매도", "금리가 내리면 왜 손해일까?", topic_size=170)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep02.mp4",
        [2.8, 9.9, 16.5, 30.0, 37.0, 40.5])
