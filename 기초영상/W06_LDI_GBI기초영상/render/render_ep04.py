"""시즌 2 「지킬 것부터 사라」 EP.04 'DV01과 헤지비율' — 9:16 웹툰 숏폼.
EP.01·03과 같은 기금. 자산 DV01 = 3 × 100 × 0.0001 = 0.03, 부채 DV01 = 20 × 80 × 0.0001 = 0.16 → 1bp당 잉여금 −0.13.
헤지비율 h = 300 / 1,600 ≈ 19%. 국민연금: 부채 DV01 7.4조/bp, 헤지 2.1%. (W06 M7 2교시·케이스 숫자 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30.5), (30.5, 37.5), (37.5, 41)]
DUR = 41
EQ = [f"eq/ep04_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.04 · DV01과 헤지비율", chip_w=820)
    s.insert(2, punch("시즌 2 · 지킬 것부터 사라", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 듀레이션 3 대 20 → 펭의 오해(15% 헤지)
    s = [bg("#F3EBD6")]
    s.append(punch("얼마나 막았나?", 540, 170, 110, fill=GOLD, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{NAVY}"/><rect x="-390" y="-180" width="780" height="26" fill="{NAVY}"/>'
                 + label("IC 질의 · 금리 위험 헤지 현황", 0, -202, 42, "#fff", 900)
                 + label("자산 듀레이션", -190, -70, 38, "#555", 800) + punch("3년", -190, 20, 96, fill=NAVY, sw=12)
                 + label("부채 듀레이션", 190, -70, 38, "#555", 800) + punch("20년", 190, 20, 96, fill=RED, sw=12)
                 + label("자산 100 · 부채 80 (EP.01 기금)", 0, 160, 38, NAVY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("3 ÷ 20 = 15%?", 720, 965, 66, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=8))
    inner.append(penguin(330, 1290, .7, "happy" if t < 2.3 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["3 대 20이니까", "금리 위험은 15% 막은 거죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["듀레이션은 %야. 자산과 부채는", "크기가 달라서 금액으로 비교해야 해."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=44))
    if t > 3.2:
        s.append(punch("금액으로!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 800, 2200          # 막대 기준선 y, DV01 0.1 = 220px


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


def gauge(t, a0, y, title, h, c, txt):
    g = ease_out(prog(t, a0, .6))
    if g <= 0: return ""
    x0, w = 590, 380
    return (f'<g opacity="{min(1, g * 2):.2f}">' + label(title, x0, y - 50, 34, NAVY, 900, anchor="start")
            + f'<rect x="{x0}" y="{y}" width="{w}" height="60" rx="12" fill="#E6E8EE"/>'
            + f'<rect x="{x0}" y="{y}" width="{max(6, w * h * g):.0f}" height="60" rx="12" fill="{c}"/>'
            + label(txt, x0 + max(6, w * h * g) + 14, y + 30, 38, c, 900, anchor="start") + '</g>')


def cut4(t):   # 해설: DV01 막대 → 헤지비율 게이지 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("1bp에 얼마?", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("DV01 = 금리 1bp(0.01%p)에 움직이는 금액", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="520" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(bar(t, .6, 180, .03, NAVY, "0.03"))
    s.append(bar(t, 1.0, 320, .16, RED, "0.16"))
    s.append(gap(t, 1.6, 400, .16, .03, "0.13", RED).replace(">잉여<", ">차이<"))
    s.append(chip("1bp당 잉여금 −0.13", 280, BASE + 80, RED, back(prog(t, 2.2, .4)), w=420, size=36))
    s.append(f'<line x1="550" y1="400" x2="550" y2="{BASE + 120}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8" opacity="{ease_out(prog(t, 2.6, .4)):.2f}"/>')
    s.append(gauge(t, 2.8, 470, "헤지비율 h · 이 기금", .1875, GREEN, "19%"))
    s.append(gauge(t, 3.6, 650, "h · 국민연금", .021, RED, "2.1%"))
    s.append(chip("부채 DV01 7.4조/bp", 780, BASE + 80, NAVY, back(prog(t, 4.2, .4)), w=400, size=36))
    for i, (y, sc) in enumerate(((1000, .5), (1100, .45), (1195, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.0 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.8, .5))}">' + label("헤지는 %가 아니라 금액(DV01)으로", 540, 1430, 48, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("100bp면 0.13 × 100 = 13 → EP.03의 잉여금 20 → 7", 540, 1505, 34, NAVY, 700) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["부채가 1bp에 0.16 움직이는데", "자산은 0.03만 따라가."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.2, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 실무 답(국민연금) + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 부채 DV01 · 자산 DV01 · 헤지비율 h", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=860, size=38)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["국민연금도 장기채를", "더 사면 되잖아요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["순부채가 국고채 전체의 1.8배야.", "시장에서 다 살 수가 없어."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("시장이 작다!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, "#B8462E", "Redington", "잉여금을 지키는 수학은?", topic_size=160)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep04.mp4",
        [2.8, 9.9, 16.5, 30.0, 37.0, 40.5])
