"""W06 「지킬 것부터 사라」 EP.03 '숨은 공매도' — 9:16 웹툰 숏폼.
EP.01과 같은 기금 A = 100(D_A 3), L = 80(D_L 20). 금리 −1%p → 자산 +3, 부채 +16.
잉여금 20 → 7 (−65%), 적립비율 125% → 107%. 갭 D_A − D_L = −17년. (W06 M7 2교시 숫자 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30.5), (30.5, 37.5), (37.5, 41)]
DUR = 41
EQ = [f"eq/ep03_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.03 · 숨은 공매도", chip_w=720)
    s.insert(2, punch("W06 · 지킬 것부터 사라", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 금리 인하 속보 → 펭의 오해(호재)
    s = [bg("#E6ECF7")]
    s.append(punch("금리가 내렸다!", 540, 170, 110, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{RED}"/><rect x="-390" y="-180" width="780" height="26" fill="{RED}"/>'
                 + label("속보 · 시장 금리 일제히 하락", 0, -202, 42, "#fff", 900)
                 + label("장기 금리", 0, -80, 40, "#555", 800) + punch("−1%p", 0, 20, 120, fill=BLUE)
                 + label("채권 가격 상승 · 주식시장 환호", 0, 160, 40, NAVY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("호재다!", 790, 965, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy", flap=prog(t, 2.0, 1.5)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["채권값이 오르니까", "우리 기금엔 좋은 거죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["자산은 3 늘지만 부채는 16 늘어.", "부채는 숨어 있는 공매도야."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("숨은 공매도!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s

BASE, K = 800, 3.6          # 막대 기준선 y, 1 단위 = 3.6px (100 → 360px)


def bar(t, a0, x, v, c, val, inside=False):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = v * K * g
    o = [f'<rect x="{x-60}" y="{BASE-h:.0f}" width="120" height="{h:.0f}" fill="{c}" rx="6"/>']
    if g > .9:
        o.append(label(val, x, BASE - v * K + 32, 40, "#fff", 900) if inside else label(val, x, BASE - v * K - 30, 40, c, 900))
        o.append(label("자산" if c == NAVY else "부채", x, BASE - 40, 32, "#fff", 900))
    return "".join(o)


def gap(t, a0, x, a, l, txt, c):
    """잉여금(자산 − 부채) 괄호: 부채 막대 꼭대기 ~ 자산 높이."""
    g = ease_out(prog(t, a0, .4))
    if g <= 0: return ""
    y1, y2 = BASE - a * K, BASE - l * K
    return (f'<g opacity="{g:.2f}"><line x1="{x-150}" y1="{y1:.0f}" x2="{x+20}" y2="{y1:.0f}" stroke="{c}" stroke-width="4" stroke-dasharray="10 7"/>'
            f'<path d="M {x+20} {y1:.0f} h 18 v {y2-y1:.0f} h -18" fill="none" stroke="{c}" stroke-width="6"/>'
            + label("잉여", x + 82, (y1 + y2) / 2 - 22, 28, c, 800) + label(txt, x + 82, (y1 + y2) / 2 + 18, 40, c, 900) + '</g>')


def cut4(t):   # 해설: 금리 −1%p 전/후 막대 → 적립비율 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("금리 −1%p 해부", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("EP.01 기금: 자산 100 (듀레이션 3) · 부채 80 (듀레이션 20)", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(bar(t, .6, 180, 100, NAVY, "100"))
    s.append(bar(t, 1.0, 320, 80, RED, "80"))
    s.append(gap(t, 1.6, 400, 100, 80, "20", GOLD))
    s.append(bar(t, 2.4, 620, 103, NAVY, "103"))
    s.append(bar(t, 2.8, 760, 96, RED, "96", inside=True))
    s.append(gap(t, 3.4, 840, 103, 96, "7", RED))
    s.append(f'<g opacity="{ease_out(prog(t, .6, .4)):.2f}">' + label("금리 −1%p 전", 250, BASE + 45, 36, NAVY, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.4, .4)):.2f}">' + label("금리 −1%p 후", 690, BASE + 45, 36, NAVY, 900) + "</g>")
    s.append(chip("적립비율 125%", 250, BASE + 130, NAVY, back(prog(t, 1.8, .4)), w=360, size=38))
    s.append(chip("107%  (잉여금 −65%)", 690, BASE + 130, RED, back(prog(t, 3.8, .4)), w=440, size=38))
    for i, y in enumerate((1025, 1125, 1225)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.8 + .8 * i, .5)), scale=.48))
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("금리 하락 = 숨은 공매도의 손실", 540, 1420, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("듀레이션 갭 = 3 − 20 = −17년", 540, 1500, 38, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["부채는 시소 맨 끝에 앉아서", "금리가 내리면 훨씬 크게 부풀어."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.0, .45)), size=42))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 자산 듀레이션 · 부채 듀레이션 · 듀레이션 갭", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 주식을 더 사면", "막을 수 있어요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["주식은 듀레이션이 거의 0이야.", "부채만큼 긴 채권이 있어야 막지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("길이를 맞춰!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, GOLD, "DV01", "금리 1bp에 몇 원씩 새나?")


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep03.mp4",
        [2.8, 9.9, 16.5, 30.0, 37.0, 40.5])
