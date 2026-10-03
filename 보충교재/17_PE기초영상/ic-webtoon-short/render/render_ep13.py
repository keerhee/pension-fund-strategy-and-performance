"""EP.13 'GP Stakes' — 9:16 웹툰 숏폼.
펀드가 아니라 운용사(GP) 지분 20%를 40에 산다. 운용사는 약정 1,000에서 관리보수 2%(20)를 받고
비용 12를 쓰면 FRE 8, Carry는 연평균 10(가정). 우리 몫은 20% × (8 + 10) = 3.6 → 연 9%(보수 4% + Carry 5%).
(EP.09 2 and 20을 운용사 쪽에서 본 회차)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep13_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
PURPLE = "#6B3FA0"


def cut1(t): return title_cut(t, "EP.13 · GP Stakes")


def cut2(t):   # 문제: 운용사 지분 인수 제안서 → 펭의 오해
    s = [bg("#EEE7F6")]
    s.append(punch("운용사를 산다고?", 540, 170, 104, fill=PURPLE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{PURPLE}"/><rect x="-390" y="-180" width="780" height="26" fill="{PURPLE}"/>'
                 + label("IC 안건 · GP Stakes 투자", 0, -202, 42, "#fff", 900)
                 + label("대상: 운용사 A (펀드 아님)", 0, -90, 44, NAVY, 900)
                 + label("지분", -170, 10, 40, "#555", 800) + punch("20%", -170, 90, 96, fill=PURPLE)
                 + label("매입가", 170, 10, 40, "#555", 800) + punch("40", 170, 90, 96, fill=GOLD)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("우리가 GP?!", 740, 965, 74, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=12))
    inner.append(penguin(540, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["펀드가 아니라 운용사를 사요?", "그럼 우리가 GP가 되는 거예요?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["운용은 안 해. 소수 지분만 사서", "GP가 버는 보수와 Carry를 나눠 받지."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("보수에 투자!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 840, 18          # 막대 기준선 y, 1 단위 = 18px (20 → 360px)


def wbar(t, a0, x, lo, hi, c, val, name, inside=True):
    """폭포형 막대: lo~hi 구간을 그린다. 값 라벨은 막대 위, 항목 이름은 기준선 아래."""
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    y_hi, y_lo = BASE - hi * K, BASE - lo * K
    h = (y_lo - y_hi) * g
    o = [f'<rect x="{x-60}" y="{y_lo-h:.0f}" width="120" height="{h:.0f}" fill="{c}" rx="6"/>']
    if g > .9:
        o.append(label(val, x, y_hi - 30, 38, c, 900))
        for k, line in enumerate(name):
            o.append(label(line, x, BASE + 40 + 38 * k, 30, NAVY, 800))
    return "".join(o)


def cut4(t):   # 해설: 폭포형 막대 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("GP는 뭘로 버나", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("약정 1,000 · 관리보수 2% · 비용 12 · Carry 연 10 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(wbar(t, .6, 190, 0, 20, NAVY, "20", ["관리보수"]))
    s.append(wbar(t, 1.4, 360, 8, 20, GREY, "−12", ["인건비", "· 비용"]))
    s.append(wbar(t, 2.2, 530, 0, 8, TEAL, "8", ["FRE"]))
    s.append(wbar(t, 3.0, 700, 0, 10, GOLD, "10", ["Carry", "(연평균)"]))
    if t > 3.8:
        a = ease_out(prog(t, 3.8, .4))
        s.append(f'<path d="M 530 {BASE-235} C 560 {BASE-330}, 700 {BASE-330}, 700 {BASE-260}" fill="none" stroke="{GREEN}" stroke-width="5" opacity="{a:.2f}"/>')
        s.append(f'<path d="M 615 {BASE-310} C 760 {BASE-340}, 880 {BASE-240}, 895 {BASE-120}" fill="none" stroke="{GREEN}" stroke-width="6" stroke-dasharray="12 8" opacity="{a:.2f}"/>')
        s.append(f'<g opacity="{a:.2f}">' + label("(8 + 10) × 20%", 860, BASE - 330, 34, GREEN, 900) + "</g>")
    s.append(wbar(t, 4.2, 900, 0, 3.6, GREEN, "3.6", ["우리 몫"]))
    s.append(chip("연 3.6 ÷ 매입가 40 = 9%", 540, 1000, PURPLE, back(prog(t, 5.2, .45)), w=700, size=40))
    for i, y in enumerate((1080, 1170, 1265)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 6.2 + .7 * i, .5)), scale=.47))
    s.append(f'<g opacity="{ease_out(prog(t, 8.6, .5))}">' + label("꾸준한 건 보수(4%), 출렁이는 건 Carry(5%)", 540, 1485, 44, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["EP.09의 2 and 20을", "운용사 쪽에서 받는 셈이지."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: FRE 안정성 · 핵심 인력 · AUM 성장 · 이해상충 · 출구", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=33)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 위험은", "없는 거예요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["AUM이 줄면 보수도 줄어.", "핵심 인력이 떠나면 회사가 비지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("사람이 자산!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, "#1E7F4F", "공동투자", "보수 없이 딜에 같이 들어간다?", topic_size=200)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep13.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
