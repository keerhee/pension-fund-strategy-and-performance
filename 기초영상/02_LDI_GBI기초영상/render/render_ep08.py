"""시즌 2 「지킬 것부터 사라」 EP.08 '위험 = 지각할 확률' — 9:16 웹툰 숏폼.
95 · 70 · 30은 비중이 아니라 목표 달성 확률이다. Safety 20번 중 19번 · Market 10번 중 7번 · Aspirational 10번 중 3번.
위험 = P(W_T < G), 미달 허용 α = 5% · 30% · 70%, z = 1.645 · 0.524 · −0.524. (W06 M8 1교시 강의본 그대로, EP.07 이순자 씨 목표표 이어받음)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep08_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.08 · 위험 = 지각할 확률", chip_w=860)
    s.insert(2, punch("시즌 2 · GBI 1막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 95 / 70 / 30을 비중으로 읽는 펭
    s = [bg("#E6ECF7")]
    s.append(punch("95 · 70 · 30?", 540, 170, 110, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{BLUE}"/><rect x="-390" y="-180" width="780" height="26" fill="{BLUE}"/>'
                 + label("이순자 씨 GBI 설계안 (EP.07)", 0, -202, 42, "#fff", 900)
                 + label("Safety", -250, -70, 38, NAVY, 900) + punch("95", -250, 20, 100, fill=NAVY, sw=12)
                 + label("Market", 0, -70, 38, TEAL, 900) + punch("70", 0, 20, 100, fill=TEAL, sw=12)
                 + label("Aspirational", 250, -70, 34, ORANGE, 900) + punch("30", 250, 20, 100, fill=ORANGE, sw=12)
                 + label("단위: %", 0, 160, 38, GREY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("합이 195%?!", 760, 965, 72, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["95·70·30을 다 더하면", "195%인데 비중이 왜 이래요?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["그건 비중이 아니라 확률이야.", "목표에 지각하지 않을 확률."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=48))
    if t > 3.2:
        s.append(punch("비중 ≠ 확률!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


ROWS = [("Safety", NAVY, 20, 19, "20번 중 19번", "필수 생활비", (460, 525)),
        ("Market", TEAL, 10, 7, "10번 중 7번", "여유 생활 · 의료비", (685,)),
        ("Aspir.", ORANGE, 10, 3, "10번 중 3번", "상속 · 꿈", (845,))]


def dots(t, a0, c, n, k, ys):
    o = []
    for i in range(n):
        g = ease_out(prog(t, a0 + .05 * i, .25))
        if g <= 0: continue
        x = 360 + 66 * (i % 10); y = ys[i // 10]
        if i < k:
            o.append(f'<circle cx="{x}" cy="{y}" r="{24*g:.1f}" fill="{c}"/>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="{24*g:.1f}" fill="#fff" stroke="{RED}" stroke-width="5" stroke-dasharray="7 5"/>')
    return "".join(o)


def cut4(t):   # 해설: 확률 점 그림 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("확률로 읽기", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("● 제때 도착   ○ 지각(목표 미달)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    for j, (tier, c, n, k, txt, goal, ys) in enumerate(ROWS):
        a0 = .6 + 1.4 * j; yc = sum(ys) / len(ys)
        s.append(chip(tier, 180, yc - 22, c, back(prog(t, a0, .4)), w=190, size=32))
        s.append(f'<g opacity="{ease_out(prog(t, a0 + .2, .4)):.2f}">' + label(txt, 180, yc + 38, 26, c, 900) + "</g>")
        s.append(dots(t, a0 + .2, c, n, k, ys))
        s.append(f'<g opacity="{ease_out(prog(t, a0 + 1.1, .3)):.2f}">' + label(goal, 655, ys[-1] + 52, 26, GREY, 800) + "</g>")
    s.append(chip("σ 12%는 목표 달성을 말해 주지 않는다", 540, 960, RED, back(prog(t, 5.0, .4)), w=760, size=34))
    for i, y in enumerate((1030, 1120, 1210)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.8 + .8 * i, .5)), scale=.5))
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("위험 = 흔들림(σ)이 아니라 지각할 확률", 540, 1420, 48, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.8, .5))}">' + label("확률이 높을수록 떼어 둘 돈이 커진다", 540, 1500, 36, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["얼마나 늦을지가 아니라", "늦을 확률이 중요해."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.6, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry")
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 목표별 달성 확률 · 미달 허용치 α · σ 말고 P", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["10번 중 3번이면", "그 목표는 왜 세워요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["3번만 돼도 좋은 꿈이니까.", "대신 밥(Safety)부터 채운 다음이야."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("꿈도 계획!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, TEAL, "마음속 계좌", "계좌를 나누면 뭐가 달라지나?", topic_size=150)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep08.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
