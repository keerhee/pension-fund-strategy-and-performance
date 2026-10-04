"""W06 「지킬 것부터 사라」 EP.12 '젊을수록 노후가 싸다' — 9:16 웹툰 숏폼. (GBI 2막 시작)
Retirement Bond(RB): 쿠폰도 원금 상환도 없이 은퇴일부터 실질 소득만 준다. 연 2,400만 원 × 20년, 실질 r = 2%.
65세에 사면 0.24 × 16.35 = 3.92억, 45세에 사면 3.92 ÷ 1.02²⁰(1.486) = 2.64억 → 약 33% 싸다. RB 가격이 곧 Floor.
(W06 M8 2교시 28~30장 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep12_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
PURPLE = "#6B3FA0"


def cut1(t):
    s = title_cut(t, "EP.12 · 젊을수록 노후가 싸다", chip_w=880)
    s.insert(2, punch("W06 · GBI 2막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 노후 대비면 긴 국채?
    s = [bg("#EEE7F6")]
    s.append(punch("노후 = 긴 국채?", 540, 170, 110, fill=PURPLE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{PURPLE}"/><rect x="-390" y="-180" width="780" height="26" fill="{PURPLE}"/>'
                 + label("펭의 노후 설계 메모 (45세)", 0, -202, 42, "#fff", 900)
                 + label("원하는 것: 65세부터 20년간", 0, -100, 40, NAVY, 900)
                 + label("매년 실질 2,400만 원", 0, -35, 48, PURPLE, 900)
                 + f'<rect x="-320" y="40" width="640" height="130" rx="18" fill="#E6ECF7"/>'
                 + label("펭의 답: 20년 국고채를 산다", 0, 105, 40, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("길면 되지!", 770, 965, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["노후 대비면 그냥", "긴 국채를 사면 되죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["국채는 지금부터 쿠폰을 주고 원금을 갚지.", "노후엔 65세부터 소득만 주는 채권이야."], 540, 330, 1030, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=42))
    if t > 3.2:
        s.append(punch("잔고 말고 소득!", 540, 1650, 130, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


X0, PXY = 130, 20.5          # 45세 x, 1년 = 20.5px (45~85세)


def ax(age): return X0 + (age - 45) * PXY


def flows(t, a0, base, title, c, items):
    o = [f'<g opacity="{ease_out(prog(t, a0, .4)):.2f}">' + label(title, 110, base - 165, 32, c, 900, anchor="start")
         + f'<line x1="{X0-10}" y1="{base}" x2="{ax(85)+10}" y2="{base}" stroke="{NAVY}" stroke-width="4"/></g>']
    for k, (age, h) in enumerate(items):
        g = ease_out(prog(t, a0 + .3 + .04 * k, .3))
        if g > 0:
            o.append(f'<rect x="{ax(age)+2:.0f}" y="{base-h*g:.0f}" width="16" height="{h*g:.0f}" fill="{c}"/>')
    return "".join(o)


def cut4(t):   # 해설: 국고채 vs RB 현금흐름 → 가격 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("현금흐름 비교", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("연 2,400만 원(실질) × 20년 · 실질금리 2% (예시)", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(flows(t, .5, 560, "20년 국고채 — 지금부터 쿠폰, 65세에 원금", BLUE, [(a, 14) for a in range(45, 65)] + [(64, 120)]))
    s.append(flows(t, 2.0, 780, "Retirement Bond — 65세부터 소득만", PURPLE, [(a, 60) for a in range(65, 85)]))
    a = ease_out(prog(t, 3.2, .4))
    s.append(f'<g opacity="{a:.2f}">' + "".join(label(f"{g}세", ax(g), 815, 28, NAVY, 800) for g in (45, 65, 85))
             + f'<line x1="{ax(65)}" y1="420" x2="{ax(65)}" y2="570" stroke="{RED}" stroke-width="3" stroke-dasharray="10 8"/>'
             + f'<line x1="{ax(65)}" y1="645" x2="{ax(65)}" y2="790" stroke="{RED}" stroke-width="3" stroke-dasharray="10 8"/>' + "</g>")
    s.append(chip("65세에 사면 3.92억", 300, 885, NAVY, back(prog(t, 3.8, .4)), w=400, size=34))
    s.append(chip("45세에 사면 2.64억", 780, 885, GREEN, back(prog(t, 4.2, .4)), w=400, size=34))
    for i, (y, sc) in enumerate(((955, .48), (1060, .5), (1170, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.0 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("RB 가격이 곧 Floor — 오늘의 Safety 목표", 540, 1410, 46, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("쿠폰도 원금 상환도 없이, 은퇴일부터 소득만", 540, 1490, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["20년 일찍 사면", "노후 소득이 3분의 1 싸져."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 은퇴 시점 · 실질 연 소득 · 지급 기간 · 실질금리", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=35)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그런 채권은", "어디서 사요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["발행국이 거의 없어. 브라질 RendA+가", "처음이고, 보통은 GHP로 복제해."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("없으면 복제!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, NAVY, "Floor", "지켜야 할 바닥은 얼마?", topic_size=220)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep12.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
