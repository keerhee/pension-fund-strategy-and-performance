"""EP.15 '빈티지 분산' — 9:16 웹툰 숏폼.
신규 약정 300을 2021년 한 번에 넣으면 그 빈티지 1.3× → 390, 2020·2021·2022에 100씩 나누면
(1.9 + 1.3 + 1.6) × 100 = 480 → 1.6×. 최고의 해를 놓치는 대신 최악의 해를 피한다. (EP.01 J-커브와 연결)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep15_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
BASE, K = 830, 180          # 막대 기준선 y, 1.0× = 180px


def vbar(t, a0, x, v, c, top, bottom, w=160, outline=None):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = v * K * g
    o = [f'<rect x="{x-w/2}" y="{BASE-h:.0f}" width="{w}" height="{h:.0f}" fill="{c}" rx="6"'
         + (f' stroke="{outline}" stroke-width="8"' if outline else "") + "/>"]
    if g > .9:
        o.append(label(top, x, BASE - h - 30, 40, c, 900))
        o.append(label(bottom, x, BASE + 42, 34, NAVY, 900))
    return "".join(o)


def cut1(t): return title_cut(t, "EP.15 · 빈티지 분산")


def cut2(t):   # 문제: 한 해 몰아 약정 → 펭의 오해
    s = [bg("#E4ECF6")]
    s.append(punch("올해 몰빵?", 540, 170, 112, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{BLUE}"/><rect x="-390" y="-180" width="780" height="26" fill="{BLUE}"/>'
                 + label("IC 안건 · PE 신규 약정", 0, -202, 42, "#fff", 900)
                 + label("시장 분위기: 역대 최고", 0, -90, 44, NAVY, 900)
                 + label("약정액", -170, 10, 40, "#555", 800) + punch("300", -170, 90, 96, fill=BLUE)
                 + label("시기", 170, 10, 40, "#555", 800) + punch("2021 한 번", 170, 90, 58, fill=RED)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("지금이 기회!", 760, 965, 74, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=12))
    inner.append(penguin(540, 1290, .7, "happy" if t > 2.3 else "worry", flap=prog(t, 2.3, 1.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["올해 시장이 최고니까", "한 번에 다 넣죠!"], 540, 1700, 820, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=56))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["최고로 보이는 해가 제일 비싼 해야.", "그래서 해마다 나눠 약정하지."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("나눠서 매년!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


def cut4(t):   # 해설: 빈티지별 막대 → 평균선 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("해마다 성적이 다르다", 540, 150, 96, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("빈티지별 최종 MOIC (예시) · 약정 300", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="120" y1="{BASE}" x2="960" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(vbar(t, .6, 260, 1.9, GREEN, "1.9×", "2020"))
    s.append(vbar(t, 1.3, 540, 1.3, RED, "1.3×", "2021", outline=NAVY if t > 2.6 else None))
    s.append(vbar(t, 2.0, 800, 1.6, TEAL, "1.6×", "2022"))
    if t > 2.6:
        a = ease_out(prog(t, 2.6, .4))
        s.append(f'<g opacity="{a:.2f}">' + label("호황 꼭지 · 비싸게 샀다", 540, BASE + 88, 30, RED, 900) + "</g>")
    if t > 3.4:
        a = ease_out(prog(t, 3.4, .5)); y = BASE - 1.6 * K
        s.append(f'<line x1="140" y1="{y}" x2="{140 + 790*a:.0f}" y2="{y}" stroke="{NAVY}" stroke-width="5" stroke-dasharray="16 10"/>')
        if a > .9: s.append(label("평균", 975, y - 22, 28, NAVY, 900) + label("1.6×", 975, y + 22, 28, NAVY, 900))
    s.append(chip("전부 2021: 390", 300, 1010, RED, back(prog(t, 4.4, .4)), w=400, size=38))
    s.append(chip("나눠서: 480", 780, 1010, GREEN, back(prog(t, 4.8, .4)), w=400, size=38))
    for i, y in enumerate((1085, 1175, 1270)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.8 + .7 * i, .5)), scale=.47))
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("최고의 해를 놓치는 대신, 최악의 해를 피한다", 540, 1480, 42, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["좋은 해였는지는", "지나고 나서야 알 수 있거든."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.2, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 빈티지 수 · 매년 약정액 · 전략 · 지역 · GP 분산", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=34)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 몇 년에", "나눠요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["보통 3~5년, 해마다 비슷하게.", "그 속도를 정하는 게 페이싱이야."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("꾸준히!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, ORANGE, "페이싱", "매년 얼마씩 약정해야 하나?", topic_size=220)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep15.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
