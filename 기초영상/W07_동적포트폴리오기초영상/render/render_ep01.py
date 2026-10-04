"""W07 「시간은 답을 바꾼다」 EP.01 '+50% 뒤 −50%' — 9:16 웹툰 숏폼. (시간분산 1)
100이 1년차 +50%로 150, 2년차 −50%로 75. 산술 평균 수익률은 0%인데 남은 돈은 75 — 25%가 사라진다.
손에 남는 수익 g ≈ μ − σ²/2, σ 20%면 0.2² ÷ 2 = 0.02 → 해마다 2%p. (W07 프라이머 9·10·16장 그대로, 기획표 EP01_Cuts 시트 구성)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep01_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
SEASON = "W07 · 시간은 답을 바꾼다"


def cut1(t):
    s = title_cut(t, "EP.01 · +50% 뒤 −50%", chip_w=720)
    s.insert(2, punch(SEASON, 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 평균 0%면 원금 그대로?
    s = [bg("#E6ECF7")]
    s.append(punch("평균은 0%!", 540, 170, 120, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{BLUE}"/><rect x="-390" y="-180" width="780" height="26" fill="{BLUE}"/>'
                 + label("펭의 투자 일지 · 원금 100", 0, -202, 42, "#fff", 900)
                 + label("1년차", -190, -85, 40, "#555", 800) + punch("+50%", -190, 0, 90, fill=GREEN, sw=11)
                 + label("2년차", 190, -85, 40, "#555", 800) + punch("−50%", 190, 0, 90, fill=RED, sw=11)
                 + label("평균 수익률 = (50 − 50) ÷ 2 = 0%", 0, 140, 38, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("본전이다!", 770, 975, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["평균이 0%니까", "원금 100은 그대로죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["평균은 0%인데 네 돈은 75야.", "출렁임이 수익을 깎아."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=48))
    if t > 3.2:
        s.append(punch("출렁임 = 비용!", 540, 1650, 130, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 800, 2.6          # 1 = 2.6px (150 → 390px)
BARS = [(250, 100, NAVY, "출발"), (540, 150, GREEN, "1년차 +50%"), (830, 75, RED, "2년차 −50%")]


def cut4(t):   # 해설: 100 → 150 → 75 막대 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("100 → 150 → 75", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("같은 폭으로 오르고 내리면 제자리가 아니다", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    y100 = BASE - 100 * K
    s.append(f'<line x1="130" y1="{y100}" x2="950" y2="{y100}" stroke="{NAVY}" stroke-width="3" stroke-dasharray="12 8" opacity="{ease_out(prog(t, .6, .4)):.2f}"/>')
    for i, (x, v, c, name) in enumerate(BARS):
        g = ease_out(prog(t, .7 + .8 * i, .5))
        if g <= 0: continue
        h = v * K * g
        s.append(f'<rect x="{x-80}" y="{BASE-h:.0f}" width="160" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(str(v), x, BASE - v * K - 30, 44, c, 900))
            s.append(label(name, x, BASE + 38, 32, NAVY, 900))
    a = ease_out(prog(t, 3.2, .4))
    s.append(f'<g opacity="{a:.2f}"><path d="M 918 {y100} h 18 v {25*K} h -18" fill="none" stroke="{RED}" stroke-width="6"/>'
             + label("−25", 982, y100 + 25 * K / 2, 34, RED, 900) + "</g>")
    s.append(chip("평균 수익률 0% · 실제 −25%", 540, 915, RED, back(prog(t, 3.8, .4)), w=560, size=36))
    for i, (y, sc) in enumerate(((985, .5), (1080, .5), (1185, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("변동성을 줄이는 일이 곧 버는 일", 540, 1400, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("손에 남는 수익 = 평균 − 출렁임의 값(σ²/2)", 540, 1480, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["반토막을 메우려면", "두 배가 필요하거든."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.0, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 산술 평균 · 기하 평균 · σ²/2", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=760, size=40)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 오래 들고 있으면", "출렁임이 사라지나요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=48))
    if t > 1.6:
        s.append(bubble(["평균 페이스는 안정되지만", "도착 지점은 오히려 더 벌어져."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("오래 ≠ 안전!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, TEAL, "비율 vs 금액", "장기 투자는 정말 안전할까?", topic_size=150)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s3_ep01.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
