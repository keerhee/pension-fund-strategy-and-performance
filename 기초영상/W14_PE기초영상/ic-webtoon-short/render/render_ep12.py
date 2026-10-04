"""EP.12 'NAV 론' — 9:16 웹툰 숏폼.
NAV 100 포트폴리오를 담보로 20(LTV 20%)을 빌려 LP에게 먼저 분배하면, 2년 뒤 130 매각 때
이자 4와 원금 20을 갚고 106만 남는다. IRR은 14.0% → 15.1%로 오르고 총 회수는 130 → 126으로 준다.
(EP.05 Subscription Line과 같은 구조 — 시계를 앞당기면 IRR은 오르고 MOIC는 내려간다)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep12_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t): return title_cut(t, "EP.12 · NAV 론")


def cut2(t):   # 문제: 매각도 없는데 분배 통지서 → 펭의 오해
    s = [bg("#E4ECF6")]
    s.append(punch("매각 없는 분배?", 540, 170, 108, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{BLUE}"/><rect x="-390" y="-180" width="780" height="26" fill="{BLUE}"/>'
                 + label("Distribution Notice · 7년차", 0, -202, 42, "#fff", 900)
                 + label("매각 딜: 없음", 0, -90, 46, NAVY, 900)
                 + label("LP 분배", -170, 10, 40, "#555", 800) + punch("20", -170, 90, 100, fill=GREEN)
                 + label("재원", 170, 10, 40, "#555", 800) + punch("NAV Facility", 170, 90, 52, fill=GOLD)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("대박?!", 840, 960, 90, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=14))
    inner.append(penguin(540, 1290, .7, "happy" if t > 2.3 else "worry", flap=prog(t, 2.3, 1.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["팔린 회사도 없는데 분배금이!", "펀드가 대박 났나 봐요!"], 540, 1700, 920, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=52))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["그건 수익이 아니라 빚이야.", "포트폴리오를 담보로 빌려서 먼저 준 거지."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("NAV Loan!", 540, 1650, 170, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


def timeline(t, y0, tag, c, a0, loan, chip_txt):
    """y0 = 기준선, 0~2년. 위로 = LP가 받는 돈·매각, 아래로 = 차입·상환.
    loan=True면 0년차 차입 20(아래) → LP 분배 20(위), 2년차 매각 130(위)에서 상환 24(아래)."""
    X0, X1, k = 340, 960, 1.25
    xs = lambda yr: X0 + (X1 - X0) * yr / 2
    o = []
    ap = ease_out(prog(t, a0, .4))
    o.append(f'<g opacity="{ap:.2f}">' + chip(tag, 175, y0, c, 1, w=250, size=34)
             + f'<line x1="{X0-30}" y1="{y0}" x2="{X1+30}" y2="{y0}" stroke="{NAVY}" stroke-width="5"/>'
             + "".join(f'<line x1="{xs(y)}" y1="{y0-10}" x2="{xs(y)}" y2="{y0+10}" stroke="{NAVY}" stroke-width="4"/>' for y in range(3))
             + '</g>')
    if loan:
        g = ease_out(prog(t, a0 + .4, .4)); h = 20 * k * g
        o.append(f'<rect x="{xs(0)-30}" y="{y0}" width="60" height="{h:.0f}" fill="{GREY}"/>')
        if g > .9: o.append(label("차입 20", xs(0) + 45, y0 + h + 14, 30, GREY, 900, "start"))
        g1 = ease_out(prog(t, a0 + .9, .4)); h = 20 * k * g1
        o.append(f'<rect x="{xs(0)-30}" y="{y0-h:.0f}" width="60" height="{h:.0f}" fill="{GREEN}"/>')
        if g1 > .9: o.append(label("LP +20", xs(0) + 45, y0 - h - 16, 32, GREEN, 900, "start"))
    g2 = ease_out(prog(t, a0 + 1.6, .5))
    if g2 > 0:
        h = 130 * k * g2
        o.append(f'<rect x="{xs(2)-34}" y="{y0-h:.0f}" width="68" height="{h:.0f}" fill="{GREEN}"/>')
        if g2 > .9: o.append(label("매각 130", xs(2) - 52, y0 - h + 24, 32, GREEN, 900, "end"))
    if loan:
        g3 = ease_out(prog(t, a0 + 2.3, .4)); h = 24 * k * g3
        o.append(f'<rect x="{xs(2)-34}" y="{y0}" width="68" height="{h:.0f}" fill="{RED}"/>')
        if g3 > .9: o.append(label("상환 −24 (원금 20 + 이자 4)", xs(2) - 52, y0 + h - 6, 30, RED, 900, "end"))
    o.append(chip(chip_txt, 590, y0 + 125, c, back(prog(t, a0 + 2.8, .4)), w=600, size=38))
    return "".join(o)


def cut4(t):   # 해설: 두 타임라인 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("빌려서 먼저 주면", 540, 150, 100, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("NAV 100 · LTV 20% · 금리 10% · 2년 뒤 130 매각 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<g opacity="{ease_out(prog(t, .4, .4))}">'
             + "".join(label(str(y), 340 + 310 * y, 385, 32, "#777", 700) for y in range(3))
             + label("연차", 1010, 350, 28, "#777", 700, "end") + "</g>")
    s.append(timeline(t, 650, "① 안 빌림", NAVY, .5, False, "IRR 14.0% · 총 130"))
    s.append(timeline(t, 1000, "② NAV 론", TEAL, 3.5, True, "IRR 15.1% · 총 20 + 106 = 126"))
    for i, y in enumerate((1195, 1285, 1375)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 7.0 + .7 * i, .5)), scale=.47))
    s.append(f'<g opacity="{ease_out(prog(t, 9.3, .5))}">' + label("IRR은 오르고, 손에 쥐는 돈은 4 줄었다", 540, 1535, 44, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["시계를 앞당긴 값이", "이자 4야. EP.05와 같은 구조지."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 10.0, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 용도 · LTV · 금리 · LPA 차입 한도 · LP 통지", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=34)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 NAV 론은", "나쁜 거예요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["후속투자·방어 자금엔 쓸모 있어.", "분배용이면 용도와 비용부터 따져야지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("용도가 핵심!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, "#6B3FA0", "GP Stakes", "운용사 자체에 투자한다?", topic_size=180)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep12.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
