"""W06 「지킬 것부터 사라」 EP.07 '같은 65세, 같은 5억' — 9:16 웹툰 숏폼. (GBI 1막 시작)
이순자 씨: 5억 + NPS 월 150만, 생활비 월 300만은 부족 불가 → Safety = (300 − 150) × 12 × 23년 현가(실질 1.5%) ≈ 3.5억 = 5억의 70%.
김영수 씨: 5억 + 임대 월 200만, 기본 생활은 임대로 충분 → Safety ≈ 0. TDF(65세 주식 20%)는 둘에게 같은 답.
(W06 M8 1교시 강의본 숫자 그대로 — 3.50억은 연금현가 19.33 × 1,800만 = 3.48억)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep07_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.07 · 같은 65세, 같은 5억", chip_w=860)
    s.insert(2, punch("W06 · GBI 1막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: TDF 추천서가 두 사람에게 같다
    s = [bg("#E9F1E4")]
    s.append(punch("똑같은 처방?", 540, 170, 110, fill=GREEN, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{GREEN}"/><rect x="-390" y="-180" width="780" height="26" fill="{GREEN}"/>'
                 + label("은퇴 상품 추천서 · 65세 · 금융자산 5억", 0, -202, 40, "#fff", 900)
                 + label("TDF (은퇴 시점형)", 0, -95, 44, NAVY, 900)
                 + label("주식 20 · 채권 80", 0, -20, 56, GREEN, 900)
                 + f'<rect x="-350" y="40" width="330" height="130" rx="18" fill="#F4E9DC"/><rect x="20" y="40" width="330" height="130" rx="18" fill="#F4E9DC"/>'
                 + label("이순자 님 ✓", -185, 105, 40, NAVY, 900) + label("김영수 님 ✓", 185, 105, 40, NAVY, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("둘 다 같아!", 760, 965, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["나이도 같고 돈도 같으니", "같은 상품이 맞는 거죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["TDF는 나이만 봐. 개인에게도 부채가", "있어 — 각자 지켜야 할 목표 말이야."], 540, 330, 1020, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=44))
    if t > 3.2:
        s.append(punch("목표가 먼저!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


TIERS = [("Safety 95%", NAVY, "생활비 부족분 월 150만", "임대로 충분"),
         ("Market 70%", TEAL, "의료비 예비 1억", "세계여행"),
         ("Aspir. 30%", ORANGE, "손주 교육 5천만", "자녀 증여")]


def cut4(t):   # 해설: 두 사람 목표표 → TDF 줄 → Safety 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("목표표 비교", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("같은 65세 · 같은 금융자산 5억 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("이순자", 540, 380, 38, NAVY, 900) + label("NPS 월 150만", 540, 422, 26, GREY, 800)
             + label("김영수", 860, 380, 38, NAVY, 900) + label("임대 월 200만", 860, 422, 26, GREY, 800)
             + f'<line x1="90" y1="450" x2="990" y2="450" stroke="{NAVY}" stroke-width="3"/></g>')
    for i, (tier, c, a1, a2) in enumerate(TIERS):
        y = 500 + 78 * i
        s.append(chip(tier, 190, y, c, back(prog(t, .9 + .5 * i, .4)), w=200, size=30))
        g = ease_out(prog(t, 1.1 + .5 * i, .4))
        s.append(f'<g opacity="{g:.2f}">' + label(a1, 540, y, 30, c if i == 0 else NAVY, 900 if i == 0 else 800)
                 + label(a2, 860, y, 30, GREEN if i == 0 else NAVY, 900 if i == 0 else 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.6, .4)):.2f}">' + label("TDF라면 둘 다: 주식 20 · 채권 80", 540, 745, 34, GREY, 800)
             + f'<line x1="270" y1="747" x2="810" y2="747" stroke="{RED}" stroke-width="4" opacity="{ease_out(prog(t, 3.0, .3)):.2f}"/></g>')
    s.append(chip("이순자 Safety ≈ 3.5억", 300, 830, NAVY, back(prog(t, 3.4, .4)), w=440, size=36))
    s.append(chip("김영수 Safety ≈ 0", 790, 830, GREEN, back(prog(t, 3.8, .4)), w=380, size=36))
    for i, (y, sc) in enumerate(((900, .5), (995, .46), (1095, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 6.8, .4))}">' + label("(만 원 · 실질 1.5% · 23년) → 약 3.5억 = 5억의 70%", 540, 1230, 32, NAVY, 700) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("같은 5억, 다른 부채 → 다른 배분", 540, 1400, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("이순자는 생활비부터 잠그고, 김영수는 성장에 더 쓴다", 540, 1480, 34, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["이순자 씨의 부채는", "23년 치 생활비 부족분이야."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry")
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 필수 생활비 · 공적연금 · 목표 금액 · 시점 · 우선순위", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=930, size=33)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 이순자 씨는", "주식을 아예 못 사요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["3.5억으로 생활비부터 잠그고,", "남는 1.5억으로 꿈을 사면 돼."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("밥 먼저, 디저트는 나중!", 540, 740, 80, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, BLUE, "지각할 확률", "위험은 무엇으로 재나?", topic_size=150)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep07.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
