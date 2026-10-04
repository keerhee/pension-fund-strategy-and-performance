"""EP.14 '공동투자' — 9:16 웹툰 숏폼.
같은 딜 B(100 → 5년 뒤 200)를 펀드로 들어가면 Carry 20 · 관리보수 10을 떼고 170(1.70×),
공동투자(Co-investment)로 직접 들어가면 보수·Carry 0으로 200(2.00×). 반반 섞으면 1.85×.
(EP.09 2 and 20의 보수를 줄이는 방법 — 대신 고르는 눈과 속도가 필요)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep14_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t): return title_cut(t, "EP.14 · 공동투자")


def cut2(t):   # 문제: 보수 0 공동투자 제안 → 펭의 오해
    s = [bg("#E3F1E8")]
    s.append(punch("보수 0원?!", 540, 170, 116, fill=GREEN, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{GREEN}"/><rect x="-390" y="-180" width="780" height="26" fill="{GREEN}"/>'
                 + label("Co-investment 제안 · 딜 B", 0, -202, 42, "#fff", 900)
                 + label("회신 기한: 10일", 0, -90, 44, RED, 900)
                 + label("관리보수", -170, 10, 40, "#555", 800) + punch("0", -170, 90, 100, fill=GREEN)
                 + label("Carry", 170, 10, 40, "#555", 800) + punch("0", 170, 90, 100, fill=GREEN)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("공짜?!", 820, 965, 90, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=12))
    inner.append(penguin(540, 1290, .7, "happy" if t > 2.3 else "worry", flap=prog(t, 2.3, 1.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["보수가 0이면 공짜잖아요!", "들어오는 건 다 받죠!"], 540, 1700, 900, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=54))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["보수 대신 우리가 직접 골라야 해.", "그것도 10일 안에 실사까지 끝내고."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("고르는 눈!", 540, 1650, 160, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 860, 2.0          # 막대 기준선 y, 1 단위 = 2px (200 → 400px)


def seg(t, a0, x, lo, hi, c, txt=None, side=None, dy=0):
    """쌓는 막대의 lo~hi 구간. txt가 있으면 막대 안(흰 글자) 또는 왼쪽(side='left')에 라벨."""
    g = ease_out(prog(t, a0, .45))
    if g <= 0: return ""
    y_hi, y_lo = BASE - hi * K, BASE - lo * K
    h = (y_lo - y_hi) * g
    o = [f'<rect x="{x-100}" y="{y_lo-h:.0f}" width="200" height="{h:.0f}" fill="{c}"/>']
    if txt and g > .9:
        ym = (y_hi + y_lo) / 2 + dy
        o.append(label(txt, x - 120, ym, 32, c, 900, "end") if side == "left" else label(txt, x, ym, 44, "#fff", 900))
    return "".join(o)


def cut4(t):   # 해설: 두 막대 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("같은 딜, 다른 몫", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("딜 B · 100 → 5년 뒤 200 · 보수 2% · Carry 20% (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="120" y1="{BASE}" x2="960" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    # ① 펀드 경유: LP 170 + Carry 20 + 보수 10 = 200
    s.append(seg(t, .6, 380, 0, 170, GREEN, "LP 170"))
    s.append(seg(t, 1.3, 380, 170, 190, GOLD, "Carry 20", "left", dy=10))
    s.append(seg(t, 1.9, 380, 190, 200, GREY, "보수 10", "left", dy=-14))
    # ② 공동투자: LP 200
    s.append(seg(t, 2.7, 760, 0, 200, GREEN, "LP 200"))
    a = ease_out(prog(t, .6, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("① 펀드 경유", 380, BASE + 45, 36, NAVY, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.7, .4)):.2f}">' + label("② 공동투자", 760, BASE + 45, 36, NAVY, 900) + "</g>")
    s.append(chip("1.70×", 380, BASE + 125, NAVY, back(prog(t, 3.4, .4)), w=260, size=44))
    s.append(chip("2.00×", 760, BASE + 125, GREEN, back(prog(t, 3.7, .4)), w=260, size=44))
    if t > 4.2:
        s.append(punch("+30", 570, BASE - 250, 72, fill=GREEN, scale=back(prog(t, 4.2, .4)), rot=-6))
    for i, y in enumerate((1065, 1155, 1250)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.6 + .7 * i, .5)), scale=.47))
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("보수 30을 아끼는 대신, 딜은 우리가 고른다", 540, 1470, 44, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["펀드와 섞으면 1.85×.", "보수를 평균해서 낮추는 거지."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.0, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 역선택 · 집중 위험 · 결정 기한 · 실사 인력 · 보수 조건", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=33)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["GP는 왜 좋은 딜을", "나눠 줘요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["딜이 펀드 한도보다 크니까.", "남는 딜만 온다면 역선택이고."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("역선택 주의!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, BLUE, "빈티지 분산", "한 해에 몰아 넣으면 안 되나?", topic_size=180)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep14.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
