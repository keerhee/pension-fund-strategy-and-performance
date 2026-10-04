"""W06 「지킬 것부터 사라」 EP.10 '꿈의 계좌는 주식이 가장 싸다' — 9:16 웹툰 숏폼.
55세 · 금융자산 10억 · 10년 뒤 은퇴. 필요 자본 K = G·e^(−mT + z_p σ√T).
Safety 6억·95%: GHP 4.91 / 균형형 6.11 / 주식 9.32 → GHP가 가장 쌈. Aspirational 5억·30%: GHP 4.09 / 균형형 2.75 / 주식 1.97 → 주식이 가장 쌈.
가장 싼 것만 고르면 4.91 + 2.22 + 1.97 = 9.10억 ≤ 10억, 49 / 22 / 29는 결과. (W06 M8 1교시 21~22장 · 부록 B-2 그대로)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep10_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.10 · 꿈의 계좌는 주식이 가장 싸다", chip_w=1000)
    s.insert(2, punch("W06 · GBI 1막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 꿈 계좌는 국채에?
    s = [bg("#FCEBDD")]
    s.append(punch("꿈은 어디에?", 540, 170, 110, fill=ORANGE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{ORANGE}"/><rect x="-390" y="-180" width="780" height="26" fill="{ORANGE}"/>'
                 + label("상담 · 55세 · 금융자산 10억 · 10년 뒤 은퇴", 0, -202, 38, "#fff", 900)
                 + label("Aspirational 계좌 (꿈)", 0, -100, 42, ORANGE, 900)
                 + label("10년 뒤 상속 5억 · 달성 확률 30%", 0, -25, 40, NAVY, 900)
                 + f'<rect x="-300" y="50" width="600" height="120" rx="18" fill="#E6ECF7"/>'
                 + label("펭의 제안: 전액 국채(GHP)", 0, 110, 40, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("안전 제일!", 770, 965, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["꿈 계좌도 소중하니까", "안전한 국채에 넣어야죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["확률 30% 목표는 주식이", "가장 적은 돈으로 닿아."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=48))
    if t > 3.2:
        s.append(punch("주식이 제일 싸다!", 540, 1650, 120, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K = 800, 36
COLS = [("GHP", NAVY), ("균형형", TEAL), ("주식", ORANGE)]


def group(t, a0, cx, title, vals, best):
    o = [f'<g opacity="{ease_out(prog(t, a0, .4)):.2f}">' + label(title, cx, 385, 32, NAVY, 900) + "</g>"]
    for i, (v, (name, c)) in enumerate(zip(vals, COLS)):
        g = ease_out(prog(t, a0 + .3 + .4 * i, .5))
        if g <= 0: continue
        x = cx - 120 + 120 * i; h = v * K * g
        o.append(f'<rect x="{x-48}" y="{BASE-h:.0f}" width="96" height="{h:.0f}" fill="{c}" rx="6"'
                 + (f' stroke="{GOLD}" stroke-width="8"' if i == best and g > .9 else "") + "/>")
        if g > .9:
            o.append(label(f"{v:.2f}", x, BASE - v * K - 28, 34, RED if i == best else c, 900))
            o.append(label(name, x, BASE + 35, 28, NAVY, 800))
    return "".join(o)


def cut4(t):   # 해설: Safety vs Aspirational 필요 자본 막대 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("필요 자본 K", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("55세 · 10억 · 10년 · 실질 억 원 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(group(t, .5, 300, "Safety 6억 · 95%", (4.91, 6.11, 9.32), 0))
    s.append(group(t, 2.3, 780, "Aspirational 5억 · 30%", (4.09, 2.75, 1.97), 2))
    s.append(chip("95%면 GHP 최저", 300, 910, NAVY, back(prog(t, 4.0, .4)), w=340, size=34))
    s.append(chip("30%면 주식 최저", 780, 910, ORANGE, back(prog(t, 4.3, .4)), w=340, size=34))
    s.append(chip("가장 싼 것만: 4.91 + 2.22 + 1.97 = 9.10억 ≤ 10억", 540, 1000, GREEN, back(prog(t, 4.8, .4)), w=920, size=32))
    for i, (y, sc) in enumerate(((1065, .5), (1155, .5), (1250, .44))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("z가 음수면 변동성이 돈을 아낀다", 540, 1420, 50, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.6, .5))}">' + label("49 / 22 / 29 배분은 입력이 아니라 결과", 540, 1500, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["좋은 운이 필요한 목표엔", "흔들림이 오히려 도움이 돼."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 목표 G · 확률 p · 기간 T · 자산별 m과 σ", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=880, size=38)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 Safety도 주식으로", "하면 더 싸지 않아요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=48))
    if t > 1.6:
        s.append(bubble(["95%면 주식은 9.32억이 들어.", "나쁜 운까지 막아야 하니까."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("확률이 답을 바꾼다!", 540, 740, 88, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, GREEN, "남은 0.90억", "남는 돈은 어디로 보내나?", topic_size=150)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep10.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
