"""시즌 2 「지킬 것부터 사라」 EP.13 'Floor의 가격표' — 9:16 웹툰 숏폼.
Floor = 필수 목표(실질 연 2,400만 원 × 25년)의 연금현가 — 실제로 살 수 있는 금리(물가연동국채)로 잰다.
1.5% 4.97억 · 2.5% 4.42억 · 3.5% 3.96억. 자산 6억(가정)이면 쿠션 1.03억 vs 2.04억 — 낙관 할인율이 쿠션을 두 배로 부풀린다.
(W06 M8 2교시 41장 · 프라이머 숫자 그대로, 자산 6억은 교육용 가정, EP.02 할인율 눈금을 개인 Floor로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep13_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.13 · Floor의 가격표", chip_w=760)
    s.insert(2, punch("시즌 2 · GBI 2막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 3.5%로 재니 쿠션이 2억
    s = [bg("#E9F1E4")]
    s.append(punch("쿠션이 2억!", 540, 170, 120, fill=GREEN, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{GREEN}"/><rect x="-390" y="-180" width="780" height="26" fill="{GREEN}"/>'
                 + label("펭의 Floor 계산 · 자산 6억 (가정)", 0, -202, 42, "#fff", 900)
                 + label("필수 생활비 실질 연 2,400만 × 25년", 0, -105, 38, NAVY, 900)
                 + label("할인율 3.5% (기대수익률)", 0, -40, 40, ORANGE, 900)
                 + label("Floor", -190, 70, 40, "#555", 800) + punch("3.96억", -190, 140, 70, fill=NAVY, sw=9)
                 + label("쿠션", 190, 70, 40, "#555", 800) + punch("2.04억", 190, 140, 70, fill=GREEN, sw=9)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("여유 많다!", 770, 975, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["쿠션이 2억이나 되니까", "주식을 더 사도 되겠죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["Floor는 실제로 살 수 있는 금리로 재.", "낙관 할인율은 쿠션을 부풀려."], 540, 330, 1020, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=44))
    if t > 3.2:
        s.append(punch("가격표는 시장에서!", 540, 1650, 118, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K, A = 800, 65, 6.0
BARS = [(250, "1.5%", 4.97, GREEN), (520, "2.5%", 4.42, TEAL), (790, "3.5%", 3.96, ORANGE)]


def cut4(t):   # 해설: 할인율별 Floor 막대 + 자산선 → 쿠션 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("Floor 가격표", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("필수 생활비 실질 연 2,400만 원 × 25년 · 자산 6억 (가정)", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    ya = BASE - A * K
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="130" y1="{ya}" x2="950" y2="{ya}" stroke="{NAVY}" stroke-width="4" stroke-dasharray="14 9"/>'
             + label("자산 6억", 950, ya - 28, 30, NAVY, 900, anchor="end") + "</g>")
    for i, (x, r, f, c) in enumerate(BARS):
        g = ease_out(prog(t, 1.0 + .7 * i, .5))
        if g <= 0: continue
        h = f * K * g
        s.append(f'<rect x="{x-70}" y="{BASE-h:.0f}" width="140" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"F {f:.2f}", x, BASE - f * K + 36, 34, "#fff", 900))
            s.append(label(f"할인율 {r}", x, BASE + 38, 30, NAVY, 900))
            cg = ease_out(prog(t, 1.5 + .7 * i, .4))
            top, bot = ya, BASE - f * K
            s.append(f'<g opacity="{cg:.2f}"><rect x="{x-70}" y="{top}" width="140" height="{bot-top:.0f}" fill="{GOLD}" opacity=".18"/>'
                     + label(f"쿠션 {A-f:.2f}", x, (top + bot) / 2, 30, GOLD, 900) + "</g>")
    s.append(chip("시장가 (물가연동)", 250, 905, GREEN, back(prog(t, 3.6, .4)), w=330, size=30))
    s.append(chip("낙관 → 쿠션 2배", 790, 905, RED, back(prog(t, 4.0, .4)), w=330, size=30))
    for i, (y, sc) in enumerate(((965, .5), (1080, .48), (1165, .48))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.8 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.8, .5))}">' + label("낙관 할인율이 쿠션을 부풀린다", 540, 1400, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("EP.02의 눈금 싸움이 개인의 Floor에서도", 540, 1480, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["쿠션이 두 배로 보이면", "위험도 두 배로 사게 돼."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry")
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 할인율 출처 · 물가연동국채 금리 · 지급 기간", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 시장 금리가", "오르면요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["Floor가 내려가 쿠션이 저절로 늘어.", "1.5% → 2.5%면 4.97억 → 4.42억."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("진짜 여유는 시장이!", 540, 740, 88, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, ORANGE, "쿠션 × 승수", "쿠션은 어떻게 쓰나?", topic_size=150)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep13.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
