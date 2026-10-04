"""W06 「지킬 것부터 사라」 EP.11 '남은 0.90억은 어디로?' — 9:16 웹툰 숏폼. (GBI 1막 끝)
EP.10 고객(55세 · 10억). 가장 싼 배분 9.10억 → 0.90억 남음 → 꿈 계좌 2.87억.
(a) 확률 30% 유지: 목표 5억 → 2.87 × e^0.93 = 7.28억 / (b) 목표 5억 유지: z = 0.07 → 달성 확률 약 53%.
자산이 8억이면 8 − 4.91 − 2.22 = 0.87억 → 상속 목표 약 2.2억(30%). Safety는 끝까지 줄이지 않는다. (W06 M8 22장 · 부록 B-3 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep11_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.11 · 남은 0.90억은 어디로?", chip_w=900)
    s.insert(2, punch("W06 · GBI 1막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 자산이 줄면 다 같이 줄인다?
    s = [bg("#F5E1E1")]
    s.append(punch("자산 −2억!", 540, 170, 120, fill=RED, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{RED}"/><rect x="-390" y="-180" width="780" height="26" fill="{RED}"/>'
                 + label("EP.10 고객 · 시장 하락 (가정)", 0, -202, 42, "#fff", 900)
                 + label("금융자산", -190, -80, 40, "#555", 800) + punch("10억 → 8억", 60, -80, 64, fill=RED, sw=9)
                 + label("Safety 4.91 · Market 2.22 · 꿈 1.97", 0, 30, 40, NAVY, 900)
                 + label("펭의 안: 세 계좌 모두 −20%", 0, 140, 42, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("공평하게!", 770, 965, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["돈이 줄었으니 계좌마다", "똑같이 20%씩 줄이면 되죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["Safety는 끝까지 안 줄여.", "줄일 땐 꿈의 계좌부터야."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=48))
    if t > 3.2:
        s.append(punch("밥은 지킨다!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


PX = 86   # 1억 = 86px


def stack(t, a0, y, title, segs):
    o = [f'<g opacity="{ease_out(prog(t, a0, .4)):.2f}">' + label(title, 100, y - 55, 32, NAVY, 900, anchor="start") + "</g>"]
    x = 100
    for i, (v, c, txt) in enumerate(segs):
        g = ease_out(prog(t, a0 + .2 + .35 * i, .4))
        w = v * PX
        if g > 0:
            o.append(f'<rect x="{x:.0f}" y="{y-35}" width="{w*g:.0f}" height="70" fill="{c}" stroke="#fff" stroke-width="3"/>')
            if g > .9:
                o.append(label(txt, x + w / 2, y, 30, "#fff", 900) if w > 120 else label(txt, x + w / 2, y + 62, 30, c, 900))
        x += w
    return "".join(o)


def cut4(t):   # 해설: 10억 / 8억 쌓기 막대 → (a)(b) 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("남거나 모자라면", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("EP.10 고객 · 가장 싼 배분 9.10억 (억 원)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(stack(t, .5, 460, "자산 10억 → 0.90억 남음", [(4.91, NAVY, "Safety 4.91"), (2.22, TEAL, "Market 2.22"), (1.97, ORANGE, "꿈 1.97"), (.90, GREEN, "+0.90")]))
    s.append(stack(t, 2.4, 650, "자산 8억 → 꿈 계좌만 줄인다", [(4.91, NAVY, "Safety 4.91"), (2.22, TEAL, "Market 2.22"), (.87, RED, "0.87")]))
    s.append(chip("(a) 확률 30% 유지 → 목표 7.28억", 300, 800, GREEN, back(prog(t, 4.0, .4)), w=460, size=29))
    s.append(chip("(b) 목표 5억 유지 → 확률 53%", 790, 800, GREEN, back(prog(t, 4.4, .4)), w=420, size=29))
    s.append(chip("8억이면 상속 목표 5억 → 약 2.2억", 540, 885, RED, back(prog(t, 4.8, .4)), w=640, size=32))
    for i, (y, sc) in enumerate(((950, .5), (1045, .5), (1155, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("Safety는 끝까지 줄이지 않는다", 540, 1400, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.6, .5))}">' + label("남으면 꿈을 키우고, 모자라면 꿈부터 줄인다", 540, 1480, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["우선순위가 곧", "줄이는 순서야."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=48))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 잉여 → 꿈 계좌 · 부족 → Aspirational부터 · Safety 고정", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=940, size=32)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["Safety조차", "못 사면요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["은퇴를 늦추거나", "필수 생활비를 다시 정해야지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=48))
    if t > 3.6:
        s.append(punch("출발선부터 다시!", 540, 740, 96, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, "#6B3FA0", "은퇴 채권", "노후 소득의 가격은 얼마?", topic_size=170)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep11.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
