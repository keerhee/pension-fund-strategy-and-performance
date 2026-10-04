"""W06 「지킬 것부터 사라」 EP.17 '원리금 보장의 덫' — 9:16 웹툰 숏폼. (GBI 3막)
한국 DC 적립금의 80~87%가 원리금 보장, 실질 수익률 ~1%. 30년 뒤 실질 1억을 95%로 만드는 데 드는 돈(예시):
원리금(실질 1%) 1 ÷ 1.01³⁰ = 0.74억 vs 균형형(m 4.5% · σ 9%) e^(−0.54) = 0.58억. 0.58억을 원리금에 두면 30년 뒤 0.79억 → 목표 미달 확정.
가장 안전해 보이는 선택이 가장 위험하다. (W06 M8 3교시 55·59장 + 1교시 K 공식 · 부록 B-2 균형형 가정, 30년 1억은 교육용 예시)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep17_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.17 · 원리금 보장의 덫", chip_w=800)
    s.insert(2, punch("W06 · GBI 3막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 원리금 보장 100%가 제일 안전?
    s = [bg("#E6ECF7")]
    s.append(punch("손실 0%!", 540, 170, 120, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{BLUE}"/><rect x="-390" y="-180" width="780" height="26" fill="{BLUE}"/>'
                 + label("펭의 퇴직연금(DC) 화면 · 35세", 0, -202, 42, "#fff", 900)
                 + label("원리금 보장형", -190, -80, 40, "#555", 800) + punch("100%", -190, 10, 90, fill=BLUE, sw=11)
                 + label("원금 손실", 190, -80, 40, "#555", 800) + punch("0%", 190, 10, 90, fill=GREEN, sw=11)
                 + label("은퇴 목표액: (입력 안 함)", 0, 150, 40, GREY, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("완벽 방어!", 770, 975, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["원금이 절대 안 깨지니까", "이게 제일 안전한 거죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["원금은 지켜도 목표는 못 지켜.", "실질 1%면 확실하게 지각해."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=48))
    if t > 3.2:
        s.append(punch("확실한 지각!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 740, 420          # 1억 = 420px


def cut4(t):   # 해설: 필요 자본 막대 2개 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("목표의 가격", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("30년 뒤 실질 1억을 95% 확률로 — 오늘 드는 돈 (예시)", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (x, v, c, name, sub) in enumerate(((330, .74, BLUE, "원리금 보장", "실질 1% · 흔들림 0"), (750, .58, TEAL, "균형형", "m 4.5% · σ 9%"))):
        g = ease_out(prog(t, .7 + 1.0 * i, .5))
        if g <= 0: continue
        h = v * K * g
        s.append(f'<rect x="{x-90}" y="{BASE-h:.0f}" width="180" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"{v:.2f}억", x, BASE - v * K - 30, 44, c, 900))
            s.append(label(name, x, BASE + 40, 34, NAVY, 900))
            s.append(label(sub, x, BASE + 80, 26, GREY, 800))
    s.append(chip("확률 95%로 잡아도 균형형이 더 싸다", 540, 905, GREEN, back(prog(t, 2.8, .4)), w=700, size=34))
    s.append(chip("한국 DC 적립금의 80~87%가 원리금 보장 · 실질 ~1%", 540, 985, RED, back(prog(t, 3.4, .4)), w=900, size=30))
    for i, (y, sc) in enumerate(((1050, .48), (1150, .46), (1250, .5))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.4 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("가장 안전해 보이는 선택이 가장 위험하다", 540, 1420, 46, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("위험 = 원금 손실이 아니라 목표 미달 (EP.08)", 540, 1500, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["0.58억을 원리금에 두면", "30년 뒤 0.79억 — 확실히 미달이야."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=40))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry")
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 원리금 비중 · 실질 수익률 · 은퇴 목표액 · 디폴트옵션", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=34)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 이 덫은", "어떻게 깨요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["디폴트옵션(2022.7)과 IRP 로보 일임(2025.3).", "로보 운용금액이 1조 2,760억(2026.3)이야."], 540, 1720, 1020, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=40))
    if t > 3.6:
        s.append(punch("목표부터 묻자!", 540, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, NAVY, "IC 보너스", "연기금은 몇 %를 헤지할까?", topic_size=160)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep17.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
