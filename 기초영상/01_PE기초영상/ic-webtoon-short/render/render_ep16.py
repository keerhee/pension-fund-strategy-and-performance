"""EP.16 '페이싱' — 9:16 웹툰 숏폼.
기금 1,000 · PE 목표 10% → 목표 NAV 100. 약정한 돈은 평균 70%만 투자돼 있으므로(콜은 늦고 분배는 빠르다)
100 ÷ 70% ≈ 143을 약정해야 한다(오버커밋). EP.15처럼 4개 빈티지로 나누면 해마다 ≈ 36. (EP.02 캐피털 콜 · EP.07 분모 효과)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep16_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
BASE, K = 830, 2.6          # 막대 기준선 y, 1 단위 = 2.6px (143 → 372px)


def seg(t, a0, x, lo, hi, c, w, txt=None, txt_c="#fff", size=40):
    g = ease_out(prog(t, a0, .45))
    if g <= 0: return ""
    y_hi, y_lo = BASE - hi * K, BASE - lo * K
    h = (y_lo - y_hi) * g
    o = [f'<rect x="{x-w/2}" y="{y_lo-h:.0f}" width="{w}" height="{h:.0f}" fill="{c}"/>']
    if txt and g > .9:
        o.append(label(txt, x, (y_hi + y_lo) / 2, size, txt_c, 900))
    return "".join(o)


def cut1(t): return title_cut(t, "EP.16 · 페이싱")


def cut2(t):   # 문제: 목표 100이면 100만 약정 → 펭의 오해
    s = [bg("#FBE9DD")]
    s.append(punch("목표 10%!", 540, 170, 116, fill=ORANGE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{ORANGE}"/><rect x="-390" y="-180" width="780" height="26" fill="{ORANGE}"/>'
                 + label("자산배분안 · PE 프로그램", 0, -202, 42, "#fff", 900)
                 + label("기금 1,000 · PE 목표 비중 10%", 0, -90, 42, NAVY, 900)
                 + label("목표 NAV", -170, 10, 40, "#555", 800) + punch("100", -170, 90, 96, fill=GREEN)
                 + label("약정안", 170, 10, 40, "#555", 800) + punch("100?", 170, 90, 96, fill=RED)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("딱 맞죠?", 780, 965, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=12))
    inner.append(penguin(540, 1290, .7, "happy" if t > 2.3 else "worry", flap=prog(t, 2.3, 1.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["목표가 100이니까", "100만 약정하면 되죠?"], 540, 1700, 820, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=56))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["약정한 돈이 다 들어가 있진 않아.", "콜은 늦고 분배는 빨라서 늘 덜 차지."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("오버커밋!", 540, 1650, 170, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


def cut4(t):   # 해설: 약정 막대(NAV + 미투자) + 빈티지 4개 → 칩 → 수식 → 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("100을 채우려면", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("평균 투자 비율 70% · 4개 빈티지로 분산 (예시)", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(seg(t, .6, 300, 0, 100, GREEN, 220, "NAV 100"))
    s.append(seg(t, 1.4, 300, 100, 143, GREY, 220, "미투자 43", size=34))
    if t > 2.0:
        a = ease_out(prog(t, 2.0, .4))
        s.append(f'<g opacity="{a:.2f}">' + label("약정 143", 300, BASE - 143 * K - 30, 40, NAVY, 900)
                 + label("콜 대기 · 이미 분배", 300, BASE + 42, 30, GREY, 900) + "</g>")
    for i, yr in enumerate((2026, 2027, 2028, 2029)):
        x = 600 + 110 * i
        s.append(seg(t, 2.8 + .35 * i, x, 0, 36, TEAL, 80))
        if t > 3.2 + .35 * i:
            s.append(label("36", x, BASE - 36 * K - 26, 34, TEAL, 900) + label(str(yr), x, BASE + 42, 26, NAVY, 800))
    if t > 4.6:
        s.append(f'<g opacity="{ease_out(prog(t, 4.6, .4)):.2f}">' + label("해마다 나눠 약정", 765, BASE - 210, 34, TEAL, 900) + "</g>")
    s.append(chip("목표 100 → 약정 143 (1.43배)", 540, 1000, NAVY, back(prog(t, 5.2, .4)), w=720, size=40))
    for i, y in enumerate((1080, 1170, 1270)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 6.0 + .7 * i, .5)), scale=.47))
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("미투자 43은 콜에 대비해 유동성으로 대기", 540, 1480, 42, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["EP.15처럼 4개 빈티지로", "나눠서 해마다 36씩."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.2, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 콜 속도 · 분배 속도 · 미납 약정 · 유동성 버퍼 · 분모 효과", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=32)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["많이 약정했는데 콜이", "한꺼번에 오면요?"], 400, 320, 640, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=50))
    if t > 1.6:
        s.append(bubble(["분배가 멈추면 그럴 수 있어. EP.07 분모 효과지.", "미납 약정만큼 유동성을 남겨 둬야 해."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=42))
    if t > 3.6:
        s.append(punch("버퍼 필수!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, PURPLE_NEXT, "펀드 오브 펀드", "보수를 두 번 낸다?", topic_size=150)


PURPLE_NEXT = "#6B3FA0"

if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep16.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
