"""W06 「지킬 것부터 사라」 EP.09 '일곱 번 거절당한 이론' — 9:16 웹툰 숏폼.
행동 포트폴리오 이론(BPT, Shefrin–Statman 2000): 계좌별 만족의 합을 최대로, 단 계좌마다 미달 확률 ≤ α_k (5% · 30% · 70%).
Thaler의 Mental Accounting(1985)을 최적화 문제로 썼다. 주요 학술지 7번 거절 → 2000년 게재 → Thaler 노벨상(2017) 뒤 재평가.
마음속 계좌는 오류가 아니라 인터페이스. (W06 M8 1교시 강의본 그대로, EP.08 확률을 계좌로 나눔)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep09_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.09 · 일곱 번 거절당한 이론", chip_w=900)
    s.insert(2, punch("W06 · GBI 1막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 통장 쪼개기는 비효율?
    s = [bg("#F1E6F4")]
    s.append(punch("통장 쪼개기?", 540, 170, 110, fill="#6B3FA0", scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    books = "".join(f'<rect x="{x-110}" y="-40" width="220" height="150" rx="14" fill="{c}"/>'
                    + label(n, x, 35, 34, "#fff", 900) for x, n, c in ((-250, "생활비", NAVY), (0, "여행 적금", TEAL), (250, "비상금", ORANGE)))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="#6B3FA0"/><rect x="-390" y="-180" width="780" height="26" fill="#6B3FA0"/>'
                 + label("상담 메모 · 펭의 통장 세 개", 0, -202, 42, "#fff", 900)
                 + label("“한 계좌로 합쳐 최적화하세요” (MVO)", 0, -100, 36, RED, 900)
                 + books + label("돈엔 꼬리표가 없다?", 0, 175, 38, GREY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("비효율?!", 780, 965, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["통장을 쪼개는 건", "비합리적인 습관이죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["경제학은 오류라고 했지만 GBI는", "그 습관을 설계의 손잡이로 써."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("습관이 설계도!", 540, 1650, 130, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


ACC = [("Safety 계좌", NAVY, "α 5%", "물가연동국채 사다리"),
       ("Market 계좌", TEAL, "α 30%", "균형형 60 / 40"),
       ("Aspir. 계좌", ORANGE, "α 70%", "주식 · 대체")]


def cut4(t):   # 해설: 거절 타임라인 → 계좌 3개 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("BPT의 여정", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("행동 포트폴리오 이론 · Shefrin–Statman", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    # 타임라인: 거절 7번 → 2000 게재 → 2017 노벨상
    s.append(f'<line x1="110" y1="440" x2="970" y2="440" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .3)):.2f}"/>')
    s.append(f'<g opacity="{ease_out(prog(t, .4, .3)):.2f}">' + label("1994", 140, 395, 28, GREY, 800) + "</g>")
    for i in range(7):
        g = back(prog(t, .6 + .22 * i, .25))
        if g > 0:
            x = 150 + 70 * i
            s.append(f'<g transform="translate({x},440) scale({g:.3f})"><circle r="27" fill="#fff" stroke="{RED}" stroke-width="5"/>'
                     + label("×", 0, 0, 38, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.2, .3)):.2f}">' + label("주요 학술지 거절 7번", 360, 495, 28, RED, 900) + "</g>")
    s.append(chip("2000 게재", 730, 440, GREEN, back(prog(t, 2.4, .35)), w=180, size=30))
    s.append(chip("2017 Thaler 노벨상", 835, 515, GOLD, back(prog(t, 2.8, .35)), w=300, size=28))
    # 계좌 3개
    for i, (name, c, a, asset) in enumerate(ACC):
        g = back(prog(t, 3.4 + .5 * i, .4))
        if g <= 0: continue
        x = 220 + 320 * i
        s.append(f'<g transform="translate({x},720) scale({g:.3f})"><rect x="-140" y="-120" width="280" height="240" rx="22" fill="{c}"/>'
                 + label(name, 0, -70, 34, "#fff", 900) + punch(a, 0, 0, 64, fill=YELLOW, sw=8)
                 + label(asset, 0, 75, 26, "#fff", 800) + "</g>")
    for i, (y, sc) in enumerate(((880, .5), (1015, .5), (1105, .48))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.4 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("마음속 계좌는 오류가 아니라 인터페이스", 540, 1400, 46, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("“노후 계좌는 건드리지 않는다” → 패닉 매도의 방화벽", 540, 1480, 34, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["계좌마다 목표와 지각 허용치를", "따로 두는 최적화야."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry")
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 계좌별 목표 · 계좌별 α · 계좌별 자산", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=860, size=38)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그렇게 좋은 이론이", "왜 7번이나 거절됐어요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=48))
    if t > 1.6:
        s.append(bubble(["너무 비주류라고 했지. 행동재무학이", "주류가 된 뒤에야 다시 읽혔어."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("거절 ≠ 틀림!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, "#6B3FA0", "필요 자본 K", "목표마다 얼마를 떼어 두나?", topic_size=140)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep09.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
