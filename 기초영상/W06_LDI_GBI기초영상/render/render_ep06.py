"""W06 「지킬 것부터 사라」 EP.06 '2022 영국 Doom Loop' — 9:16 웹툰 숏폼.
EP.01 기금(자산 DV01 0.03 · 부채 DV01 0.16)이 모자란 0.13을 고정 수취 IRS(D 20)로 채운다: 20 × N × 0.0001 = 0.13 → 명목 65.
금리 +100bp → 잉여금은 0(헤지 성공)이지만 IRS 변동증거금 13을 오늘 현금으로 낸다. 현금 5(가정) → Gilt 매도 → Doom Loop.
영국 감독당국 250bp 버퍼 → 0.13 × 250 = 32.5. (W06 M7 3교시 강의본: £45B 감세 · Gilt 나흘 +1%p · 32일 · 250bp, 기금 숫자는 교육용 가정)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep06_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.06 · 2022 영국 Doom Loop", chip_w=880)
    s.insert(2, punch("W06 · 지킬 것부터 사라", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 미니예산 → Gilt 급락 → 증거금 콜
    s = [bg("#F5E1E1")]
    s.append(punch("마진콜?!", 540, 170, 120, fill=RED, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{RED}"/><rect x="-390" y="-180" width="780" height="26" fill="{RED}"/>'
                 + label("속보 · 2022.9.23 영국 미니예산", 0, -202, 42, "#fff", 900)
                 + label("£45B 감세 → 30년 Gilt 나흘 새 +1%p", 0, -95, 40, NAVY, 900)
                 + f'<rect x="-350" y="-30" width="700" height="190" rx="18" fill="#FBE9E9"/>'
                 + label("LDI 운용사 통지", 0, 15, 36, "#555", 800)
                 + label("내일까지 증거금 13 납부", 0, 95, 50, RED, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("현금 5뿐!", 770, 965, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["헤지를 100% 해 놨는데", "왜 돈을 내라는 거예요?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["헤지 방향은 옳았어. 부채도 16 줄었지.", "문제는 오늘 낼 현금이 없었던 거야."], 540, 330, 1020, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=44))
    if t > 3.2:
        s.append(punch("현금이 없다!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


NODES = [(310, 470, ["금리 급등", "(Gilt 가격 ↓)"], RED), (770, 470, ["IRS 손실", "→ 증거금 콜"], ORANGE),
         (770, 700, ["현금 부족", "→ Gilt 매도"], GOLD), (310, 700, ["다 같이 팔아", "Gilt 가격 ↓"], NAVY)]


def loop(t, a0):
    o = []
    for i, (x, y, lines, c) in enumerate(NODES):
        g = back(prog(t, a0 + .5 * i, .4))
        if g <= 0: continue
        o.append(f'<g transform="translate({x},{y}) scale({g:.3f})"><rect x="-190" y="-62" width="380" height="124" rx="22" fill="{c}"/>'
                 + label(lines[0], 0, -22, 36, "#fff", 900) + label(lines[1], 0, 26, 32, "#fff", 800) + "</g>")
    arrows = [(505, 470, 575, 470), (770, 537, 770, 633), (575, 700, 505, 700), (310, 633, 310, 537)]
    for i, (x1, y1, x2, y2) in enumerate(arrows):
        g = ease_out(prog(t, a0 + .5 * i + .3, .3))
        if g <= 0: continue
        o.append(f'<g opacity="{g:.2f}"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{NAVY}" stroke-width="8" marker-end="url(#ah)"/></g>')
    if t > a0 + 2.2:   # 가운데 회전 표시
        o.append(f'<g transform="translate(540,585) rotate({(t - a0) * 90:.0f})"><circle r="44" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="60 20"/></g>')
    return ('<defs><marker id="ah" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5" orient="auto">'
            f'<path d="M0,0 L5,2.5 L0,5 z" fill="{NAVY}"/></marker></defs>' + "".join(o))


def cut4(t):   # 해설: Doom Loop 고리 → 칩 2개 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("Doom Loop", 540, 150, 120, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("EP.01 기금 + IRS로 헤지 100% · 현금 5 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(loop(t, .5))
    s.append(chip("금리 +1%p: 잉여금 변화 0", 300, 860, GREEN, back(prog(t, 3.0, .4)), w=470, size=34))
    s.append(chip("오늘 낼 현금 13 > 보유 5", 780, 860, RED, back(prog(t, 3.5, .4)), w=440, size=34))
    for i, (y, sc) in enumerate(((955, .48), (1055, .48), (1155, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.4, .5))}">' + label("레버리지 헤지에는 현금 버퍼가 함께", 540, 1350, 48, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 7.8, .5))}">' + label("위기 뒤 영국 감독당국: 250bp 급등을 견딜 현금", 540, 1425, 34, NAVY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("미니예산(9/23) → Truss 사임(10/25)까지 32일", 540, 1495, 32, GREY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["한 기금의 매도는 괜찮아도", "1,000개가 동시에 팔면 무너져."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 스왑 DV01 · 현금 버퍼 · 재충전 기한 5영업일", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 레버리지 헤지는", "쓰면 안 되나요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["써도 돼. 다만 250bp를 버틸", "현금을 따로 쥐고 있어야 해."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("버퍼 먼저!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, GREEN, "GBI", "개인에게 부채는 뭘까?")


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep06.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
