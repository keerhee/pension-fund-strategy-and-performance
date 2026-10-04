"""W06 「지킬 것부터 사라」 EP.01 '자산 +7%인데 왜 혼나요?' — 9:16 웹툰 숏폼.
자산 100이 +7%(107), 부채 80이 +10%(88). 적립비율 125% → 121.6%, 잉여금 20 → 19.
잉여금 수익률 R_S = r_A − (L/A)·r_L = 7 − 0.8×10 = −1%. (W06 M7 1교시 숫자 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep01_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.01 · 자산 +7%인데 왜 혼나요?", chip_w=960)
    s.insert(2, punch("W06 · 지킬 것부터 사라", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 운용 성과 보고 +7% → 이사회 '재검토' → 펭의 오해
    s = [bg("#E3F0E8")]
    s.append(punch("+7% 벌었는데?", 540, 170, 110, fill=GREEN, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{NAVY}"/><rect x="-390" y="-180" width="780" height="26" fill="{NAVY}"/>'
                 + label("이사회 보고 · 올해 운용 성과", 0, -202, 42, "#fff", 900)
                 + label("자산 수익률", -170, -70, 40, "#555", 800) + punch("+7%", -170, 20, 110, fill=GREEN)
                 + label("목표 수익률", 170, -70, 40, "#555", 800) + label("5%", 170, 20, 80, GREY, 900)
                 + label("목표 초과 달성 ✓", 0, 160, 44, GREEN, 900)
                 + '</g>')
    if t > 2.0:   # 이사회 도장
        a = back(prog(t, 2.0, .35))
        inner.append(f'<g transform="translate(790,960) rotate(-12) scale({a:.3f})">'
                     f'<circle r="120" fill="#fff" stroke="{RED}" stroke-width="10"/><circle r="100" fill="none" stroke="{RED}" stroke-width="4"/>'
                     + label("재검토", 0, -16, 52, RED, 900) + label("이사회", 0, 44, 32, RED, 800) + '</g>')
    inner.append(penguin(400, 1290, .7, "shock" if t > 2.4 else "happy", sweat=prog(t, 2.4, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["목표보다 2%p나 더 벌었는데", "왜 혼나는 거예요?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["연기금 성적표는 자산이 아니라", "자산 대 부채야. 부채는 +10%였어."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("자산 ÷ 부채!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 800, 3.6          # 막대 기준선 y, 1 단위 = 3.6px (100 → 360px)


def bar(t, a0, x, v, c, val):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = v * K * g
    o = [f'<rect x="{x-60}" y="{BASE-h:.0f}" width="120" height="{h:.0f}" fill="{c}" rx="6"/>']
    if g > .9:
        o.append(label(val, x, BASE - v * K - 30, 40, c, 900))
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


def cut4(t):   # 해설: 작년/올해 막대 → 적립비율 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("성적표 다시 보기", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("자산 100 · 부채 80 → 자산 +7% · 부채 +10% (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(bar(t, .6, 180, 100, NAVY, "100"))
    s.append(bar(t, 1.0, 320, 80, RED, "80"))
    s.append(gap(t, 1.6, 400, 100, 80, "20", GOLD))
    s.append(bar(t, 2.4, 620, 107, NAVY, "107"))
    s.append(bar(t, 2.8, 760, 88, RED, "88"))
    s.append(gap(t, 3.4, 840, 107, 88, "19", RED))
    a = ease_out(prog(t, .6, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("작년", 250, BASE + 45, 38, NAVY, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.4, .4)):.2f}">' + label("올해", 690, BASE + 45, 38, NAVY, 900) + "</g>")
    s.append(chip("적립비율 125%", 250, BASE + 130, NAVY, back(prog(t, 1.8, .4)), w=360, size=38))
    s.append(chip("121.6%  (−3.4%p)", 690, BASE + 130, RED, back(prog(t, 3.8, .4)), w=400, size=38))
    for i, y in enumerate((1020, 1130, 1240)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.8 + .8 * i, .5)), scale=.5))
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("좋은 해 = 부채보다 많이 번 해", 540, 1440, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("잉여금 20 → 19, 자산 대비 −1%", 540, 1515, 36, NAVY, 700) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["7%를 벌어도 부채가 10% 늘면", "잉여금은 오히려 줄어."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.0, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 적립비율 · 잉여금 수익률 · 부채 증가율", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=38)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 성과는 앞으로", "뭘로 봐야 해요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["자산 수익률 말고 잉여금 수익률.", "비교 기준(BM)이 부채인 셈이지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("부채가 BM!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, TEAL, "할인율", "부채는 누가, 어떻게 재나?")


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep01.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
