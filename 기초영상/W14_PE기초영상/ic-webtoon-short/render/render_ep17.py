"""EP.17 '펀드 오브 펀드' — 9:16 웹툰 숏폼.
EP.09의 Gross 2.0× → Net 1.48×(아래 펀드의 2 and 20) 위에 FoF 보수 1% × 10년 = 10, FoF Carry 10% × 38 = 3.8이
한 겹 더 얹힌다 → LP 134.2 = 1.34×. 그 0.14×가 접근성·분산·실사 인력의 값어치인지 따진다."""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep17_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
BASE, K = 830, 1.8          # 막대 기준선 y, 1 단위 = 1.8px (200 → 360px)
PURPLE = "#6B3FA0"


def vbar(t, a0, x, v, c, top, bottom, w=180):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = v * K * g
    o = [f'<rect x="{x-w/2}" y="{BASE-h:.0f}" width="{w}" height="{h:.0f}" fill="{c}" rx="6"/>']
    if g > .9:
        o.append(label(top, x, BASE - h - 30, 42, c, 900))
        for k, line in enumerate(bottom):
            o.append(label(line, x, BASE + 42 + 36 * k, 32, NAVY, 900))
    return "".join(o)


def cut1(t): return title_cut(t, "EP.17 · 펀드 오브 펀드", chip_w=860)


def cut2(t):   # 문제: 보수 1%짜리 FoF 제안 → 펭의 오해
    s = [bg("#EEE7F6")]
    s.append(punch("보수 1%?", 540, 170, 120, fill=PURPLE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{PURPLE}"/><rect x="-390" y="-180" width="780" height="26" fill="{PURPLE}"/>'
                 + label("제안서 · Fund of Funds", 0, -202, 42, "#fff", 900)
                 + label("PE 펀드 20개에 분산 투자", 0, -90, 44, NAVY, 900)
                 + label("관리보수", -170, 10, 40, "#555", 800) + punch("1%", -170, 90, 100, fill=GREEN)
                 + label("Carry", 170, 10, 40, "#555", 800) + punch("10%", 170, 90, 100, fill=GREEN)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("싸다!", 820, 965, 96, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=12))
    inner.append(penguin(540, 1290, .7, "happy" if t > 2.3 else "worry", flap=prog(t, 2.3, 1.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["보수가 1%밖에 안 되네요?", "2 and 20보다 훨씬 싸요!"], 540, 1700, 880, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=54))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["그 1%는 위에 얹는 거야.", "아래 펀드 2 and 20은 그대로 내고."], 540, 330, 1000, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=50))
    if t > 3.2:
        s.append(punch("보수 두 겹!", 540, 1650, 160, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


def cut4(t):   # 해설: Gross → 펀드 Net → FoF LP 막대 → 칩 → 수식 → 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("두 겹을 빼면", 540, 150, 108, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("약정 100 · EP.09 숫자 위에 FoF 1% + 10% (예시)", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(vbar(t, .6, 230, 200, NAVY, "2.00×", ["Gross"]))
    s.append(vbar(t, 1.6, 540, 148, TEAL, "1.48×", ["펀드 Net", "(EP.09)"]))
    s.append(vbar(t, 2.6, 850, 134.2, GREEN, "1.34×", ["FoF 거친", "LP"]))
    if t > 2.0:
        s.append(f'<g opacity="{ease_out(prog(t, 2.0, .4)):.2f}">' + label("−52", 385, BASE - 300, 36, RED, 900)
                 + label("2 and 20", 385, BASE - 262, 28, RED, 800) + "</g>")
    if t > 3.0:
        s.append(f'<g opacity="{ease_out(prog(t, 3.0, .4)):.2f}">' + label("−13.8", 695, BASE - 300, 36, RED, 900)
                 + label("1% + 10%", 695, BASE - 262, 28, RED, 800) + "</g>")
    s.append(chip("200 → 148 → 134", 540, 1010, PURPLE, back(prog(t, 4.0, .4)), w=600, size=42))
    for i, y in enumerate((1085, 1175, 1265)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.0 + .7 * i, .5)), scale=.47))
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("아래 2 and 20 + 위 1% + 10% = 보수 두 겹", 540, 1470, 42, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["0.14×가 무엇의 값인지", "따져 봐야 하지."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 8.6, .45)), size=48))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 이중 보수 · 접근성 · 분산 · 실사 역량 · 세컨더리·공동투자 비중", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=940, size=30)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 FoF는", "왜 써요?"], 400, 320, 600, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=54))
    if t > 1.6:
        s.append(bubble(["못 들어가는 GP 접근, 분산, 실사 인력.", "그걸 직접 못 하면 사는 값이지."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("값어치 비교!", 330, 740, 96, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, TEAL, "키맨 조항", "핵심 인력이 떠나면?", topic_size=200)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep17.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
