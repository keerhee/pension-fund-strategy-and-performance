"""시즌 2 「지킬 것부터 사라」 EP.15 'Cash Trap' — 9:16 웹툰 숏폼.
EP.07 이순자 씨(65→75세, 5억, Floor 3.50억, 매달 0.15억 인출) · CPPI 월간 리밸런싱 · 1,000 경로 · 주식 로그 6% σ 20%, GHP 실질 1.5%, seed 2026.
m 1→6: 중위 4.95 → 6.45(↑) · 최악 10% 평균 3.10 → 2.12(↓) · Cash Trap 0% → 20.7%. m 3 Trap 1.4% vs m 6 20.7%.
평균은 좋아지고 최악은 나빠진다. (W06 M8 실습데이터 Step 5 · w8_sim_results.json 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep15_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성

MED = [4.95, 5.74, 6.10, 6.30, 6.36, 6.45]
WORST = [3.10, 2.51, 2.24, 2.15, 2.13, 2.12]
TRAP = [0.0, 0.1, 1.4, 9.4, 16.5, 20.7]


def cut1(t):
    s = title_cut(t, "EP.15 · Cash Trap", chip_w=640)
    s.insert(2, punch("시즌 2 · GBI 2막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 중위가 높으니 m = 6?
    s = [bg("#F5E1E1")]
    s.append(punch("m을 키우자?", 540, 170, 110, fill=RED, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{RED}"/><rect x="-390" y="-180" width="780" height="26" fill="{RED}"/>'
                 + label("이순자 씨 CPPI 시뮬레이션 (EP.07)", 0, -202, 40, "#fff", 900)
                 + label("65 → 75세 · 1,000 경로 · 75세 자산 중위", 0, -105, 34, NAVY, 800)
                 + label("m = 3", -190, -20, 42, "#555", 900) + punch("6.10억", -190, 60, 76, fill=NAVY, sw=9)
                 + label("m = 6", 190, -20, 42, "#555", 900) + punch("6.45억", 190, 60, 76, fill=GREEN, sw=9)
                 + label("펭의 결론: m = 6으로!", 0, 165, 40, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("더 높다!", 770, 975, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["중위가 더 높으니까", "m = 6이 더 좋은 거죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["중위만 보면 그래. 다섯 번 중 한 번은", "현금에 갇혀 회복을 놓쳐."], 540, 330, 1020, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=44))
    if t > 3.2:
        s.append(punch("현금 감옥!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 850, 11          # Trap 막대 기준선, 1%p = 13px
XS = [300 + 128 * i for i in range(6)]


def cut4(t):   # 해설: m별 중위·최악 표 → Trap 막대 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("m을 키우면", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("이순자 씨 · 65→75세 · 1,000 경로 · 75세 자산 (억)", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("m", 110, 395, 32, NAVY, 900, anchor="start")
             + "".join(label(str(i + 1), x, 395, 34, NAVY, 900) for i, x in enumerate(XS))
             + f'<line x1="100" y1="425" x2="980" y2="425" stroke="{NAVY}" stroke-width="3"/></g>')
    for r, (name, vals, c, a0) in enumerate((("중위", MED, GREEN, 1.0), ("최악 10%", WORST, RED, 2.0))):
        y = 470 + 55 * r
        s.append(f'<g opacity="{ease_out(prog(t, a0, .3)):.2f}">' + label(name, 110, y, 28, c, 900, anchor="start") + "</g>")
        for i, (x, v) in enumerate(zip(XS, vals)):
            s.append(f'<g opacity="{ease_out(prog(t, a0 + .1 * i, .3)):.2f}">' + label(f"{v:.2f}", x, y, 32, c, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.8, .3)):.2f}">' + label("Cash Trap 확률", 110, 600, 30, NAVY, 900, anchor="start")
             + f'<line x1="230" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="4"/></g>')
    for i, (x, v) in enumerate(zip(XS, TRAP)):
        g = ease_out(prog(t, 3.0 + .25 * i, .4))
        if g <= 0: continue
        h = max(4, v * K) * g
        c = RED if v >= 9 else ORANGE if v >= 1 else GREY
        s.append(f'<rect x="{x-45}" y="{BASE-h:.0f}" width="90" height="{h:.0f}" fill="{c}" rx="5"/>')
        if g > .9: s.append(label(f"{v:.1f}%", x, BASE - max(4, v * K) - 24, 30, c, 900))
    for i, (y, sc) in enumerate(((905, .46), (1025, .48), (1115, .44))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.0 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.8, .5))}">' + label("평균은 좋아지고 최악은 나빠진다", 540, 1400, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("쿠션이 0에 붙으면 위험자산 0 → 회복장을 놓친다", 540, 1480, 34, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["m이 크면 작은 하락에도", "쿠션이 바닥나 버려."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 승수 m · 쿠션/자산 비율 · 최악 10% · 재설정 규칙", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=35)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["실제로 갇힌 적이", "있어요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["2008년에 일부 CPPI 상품이 바닥에서", "현금으로 바뀌어 반등을 놓쳤어."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("반등을 놓쳤다!", 540, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, TEAL, "Flexicure", "Floor를 매년 다시 잡으면?", topic_size=170)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep15.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
