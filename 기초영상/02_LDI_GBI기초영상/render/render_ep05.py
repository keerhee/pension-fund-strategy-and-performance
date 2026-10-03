"""시즌 2 「지킬 것부터 사라」 EP.05 'Redington의 방패' — 9:16 웹툰 숏폼.
부채: 10년 뒤 100, y = 5%(연속복리) → PV 60.65. 같은 돈으로 바벨(5년 38.94 + 15년 64.20, D 10 · C 125) vs 5년물 몽땅(77.88, D 5).
금리 −2%p: 바벨 +0.37 · 5년물 −7.05 / +2%p: 바벨 +0.25 · 5년물 +5.22. Redington 3조건 A ≥ L · D_A A = D_L L · C_A A ≥ C_L L.
(W06 M7 2교시 강의본 숫자 그대로, +2%p는 같은 식으로 계산)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep05_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.05 · Redington의 방패", chip_w=820)
    s.insert(2, punch("시즌 2 · 지킬 것부터 사라", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 같은 돈 60.65로 두 안 → 펭의 오해
    s = [bg("#E8EEF3")]
    s.append(punch("어느 채권으로?", 540, 170, 110, fill=TEAL, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{TEAL}"/><rect x="-390" y="-180" width="780" height="26" fill="{TEAL}"/>'
                 + label("IC 안건 · 10년 뒤 100 지급 덮기", 0, -202, 42, "#fff", 900)
                 + label("예산 = 부채 현재가치 60.65 (예시)", 0, -90, 40, NAVY, 900)
                 + f'<rect x="-350" y="-20" width="330" height="180" rx="18" fill="#F4E9DC"/><rect x="20" y="-20" width="330" height="180" rx="18" fill="#F4E9DC"/>'
                 + label("안 A", -185, 25, 40, RED, 900) + label("5년물 몽땅", -185, 100, 40, NAVY, 800)
                 + label("안 B", 185, 25, 40, GREEN, 900) + label("5년 + 15년 반반", 185, 100, 38, NAVY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("똑같은데?!", 760, 965, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.3 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["같은 돈이면", "아무거나 사도 되죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["돈만 맞추면 1단계야. 듀레이션도,", "휘어짐(볼록성)도 맞춰야 방패지."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("방패는 3조건!", 540, 1650, 130, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


ZERO, K = 840, 11          # 손익 막대 0선 y, 1 단위 = 11px


def pl(t, a0, x, v, c):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = max(6, abs(v) * K) * g
    y = ZERO - h if v > 0 else ZERO
    txt = f"{v:+.2f}".replace("-", "−")
    ly = ZERO - max(6, abs(v) * K) - 28 if v > 0 else ZERO + abs(v) * K + 30
    o = f'<rect x="{x-50}" y="{y:.0f}" width="100" height="{h:.0f}" fill="{c}" rx="5"/>'
    return o + (label(txt, x, ly, 36, c, 900) if g > .9 else "")


def cut4(t):   # 해설: 3조건 표 → 금리 ±2%p 손익 막대 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("방패 시험", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("부채: 10년 뒤 100 · 금리 5% · 예산 60.65 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    # 3조건 표
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("Redington 3조건", 110, 400, 34, NAVY, 900, anchor="start")
             + label("바벨 (B)", 700, 400, 34, GREEN, 900) + label("5년물 (A)", 900, 400, 34, RED, 900)
             + f'<line x1="100" y1="435" x2="980" y2="435" stroke="{NAVY}" stroke-width="3"/></g>')
    rows = [("① 출발선 A ≥ L", "✓ 60.65", "✓ 60.65", GREEN),
            ("② 금액 듀레이션 일치", "✓ D 10", "× D 5", RED),
            ("③ 볼록성 자산 ≥ 부채", "✓ C 125", "× C 25", RED)]
    for i, (name, b, sh, c2) in enumerate(rows):
        g = ease_out(prog(t, .9 + .6 * i, .4)); y = 485 + 65 * i
        s.append(f'<g opacity="{g:.2f}">' + label(name, 110, y, 34, NAVY, 800, anchor="start")
                 + label(b, 700, y, 34, GREEN, 900) + label(sh, 900, y, 34, c2, 900) + "</g>")
    # 손익 막대
    a = ease_out(prog(t, 2.9, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("금리 −2%p", 330, 685, 36, NAVY, 900) + label("금리 +2%p", 750, 685, 36, NAVY, 900)
             + f'<line x1="120" y1="{ZERO}" x2="960" y2="{ZERO}" stroke="{NAVY}" stroke-width="4"/>'
             + label("잉여금 손익", 120, ZERO + 30, 28, GREY, 800, anchor="start") + "</g>")
    s.append(pl(t, 3.1, 270, .37, GREEN)); s.append(pl(t, 3.5, 390, -7.05, RED))
    s.append(pl(t, 3.9, 690, .25, GREEN)); s.append(pl(t, 4.3, 810, 5.22, RED))
    s.append(f'<g opacity="{ease_out(prog(t, 4.7, .4)):.2f}"><rect x="640" y="910" width="28" height="28" fill="{GREEN}"/>'
             + label("바벨: 양쪽 다 +", 678, 924, 30, GREEN, 900, anchor="start")
             + f'<rect x="640" y="955" width="28" height="28" fill="{RED}"/>' + label("5년물: 금리 방향 베팅", 678, 969, 30, RED, 900, anchor="start") + "</g>")
    for i, (y, sc) in enumerate(((1025, .5), (1115, .5), (1230, .48))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.4 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("듀레이션만 맞추면 반쪽 — 볼록성까지", 540, 1420, 48, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.6, .5))}">' + label("자산 현금흐름이 부채를 양쪽에서 감싸야 한다", 540, 1500, 36, NAVY, 700) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["1952년 액추어리 Redington이", "이 세 조건을 정리했어."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.6, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: A ≥ L · 금액 듀레이션 · 볼록성 · 재조정 주기", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 바벨 한 번 사면", "끝인 거죠?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["시간이 가면 D와 C가 변해.", "그래서 주기적으로 다시 맞추지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("다시 맞춰!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, NAVY, "Doom Loop", "모자란 헤지는 어떻게 채우나?", topic_size=160)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep05.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
