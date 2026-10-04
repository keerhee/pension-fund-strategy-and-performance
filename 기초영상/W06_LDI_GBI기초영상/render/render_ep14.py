"""W06 「지킬 것부터 사라」 EP.14 '쿠션 × 승수' — 9:16 웹툰 숏폼.
위험자산(PSP) 금액 E = m(A − F), 비중 w = m(A − F)/A. F 5억 · m 4: A 10억 → 200%(상한 100%), A 6억 → 67%, A 5억 → 0%.
위험자산이 x만큼 떨어질 때 손실 m(A − F)x < 쿠션 A − F → x < 1/m = 25%. 하락하면 자동으로 줄이고 오르면 늘린다(Black–Jones 1987 CPPI).
(W06 M8 2교시 37장 그대로, EP.13 Floor ≈ 5억을 이어받음)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep14_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.14 · 쿠션 × 승수", chip_w=700)
    s.insert(2, punch("W06 · GBI 2막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 쿠션만큼만 주식에?
    s = [bg("#FCEBDD")]
    s.append(punch("쿠션 1억이면?", 540, 170, 110, fill=ORANGE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{ORANGE}"/><rect x="-390" y="-180" width="780" height="26" fill="{ORANGE}"/>'
                 + label("펭의 배분안 · 자산 6억 (EP.13)", 0, -202, 42, "#fff", 900)
                 + label("Floor 5억 · 쿠션 1억", 0, -100, 44, NAVY, 900)
                 + f'<rect x="-320" y="-30" width="640" height="200" rx="18" fill="#FBF3EA"/>'
                 + label("주식 1억 (17%)", 0, 30, 48, ORANGE, 900)
                 + label("국채(GHP) 5억", 0, 110, 44, NAVY, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("너무 소심?", 770, 975, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["잃어도 되는 돈이 1억이니까", "주식도 1억만 넣으면 되죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=48))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["쿠션의 m배를 넣어. 주식이 1/m보다", "덜 빠지면 Floor는 그대로 지켜져."], 540, 330, 1020, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=44))
    if t > 3.2:
        s.append(punch("쿠션 × m!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


BASE, K, F = 790, 38, 5.0
COLS = [(250, 10, "200% → 100%", GREEN), (540, 6, "67%", ORANGE), (830, 5, "0%", RED)]


def cut4(t):   # 해설: 자산 10 / 6 / 5에서 Floor + 쿠션 쌓기 → 비중 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("쿠션이 비중을 정한다", 540, 150, 96, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("Floor 5억 · 승수 m = 4 (예시)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    yf = BASE - F * K
    s.append(f'<g opacity="{ease_out(prog(t, .5, .4)):.2f}"><line x1="110" y1="{yf}" x2="970" y2="{yf}" stroke="{NAVY}" stroke-width="3" stroke-dasharray="12 8"/>'
             + "</g>")
    for i, (x, a, w, c) in enumerate(COLS):
        g = ease_out(prog(t, .8 + 1.0 * i, .5))
        if g <= 0: continue
        s.append(f'<rect x="{x-75}" y="{BASE-F*K*g:.0f}" width="150" height="{F*K*g:.0f}" fill="{NAVY}" rx="4"/>')
        cu = (a - F) * K * g
        if cu > 0:
            s.append(f'<rect x="{x-75}" y="{yf-cu:.0f}" width="150" height="{cu:.0f}" fill="{GOLD}" rx="4"/>')
        if g > .9:
            s.append(label("Floor 5", x, BASE - F * K / 2, 30, "#fff", 900))
            s.append(label(f"A {a}억", x, BASE - a * K - 28, 34, NAVY, 900))
            if a - F > 2: s.append(label(f"쿠션 {a-F:.0f}", x, yf - (a - F) * K / 2, 30, "#fff", 900))
            s.append(chip(f"주식 {w}", x, BASE + 50, c, back(prog(t, 1.2 + 1.0 * i, .4)), w=320 if i == 0 else 200, size=30))
    s.append(f'<g opacity="{ease_out(prog(t, 3.6, .4)):.2f}">' + label("레버리지 금지 → 상한 100%", 250, BASE + 112, 26, GREY, 900) + "</g>")
    for i, (y, sc) in enumerate(((975, .48), (1085, .48), (1195, .48))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.6, .5))}">' + label("1/m보다 덜 떨어지면 Floor는 지켜진다", 540, 1400, 46, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("떨어지면 줄이고, 오르면 늘린다 — CPPI (Black–Jones 1987)", 540, 1480, 32, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["쿠션이 매트 두께야.", "얇아지면 스스로 낮게 뛰지."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=46))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "happy", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 승수 m · 급락 한도 1/m · 상한 100% · 재조정 주기", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=920, size=35)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["m을 크게 하면", "더 많이 벌겠네요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["오를 땐 그래. 대신 1/m이 작아져서", "급락 한 번에 매트가 사라질 수 있어."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=42))
    if t > 3.6:
        s.append(punch("m은 양날의 칼!", 540, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t): return next_cut(t, RED, "Cash Trap", "갇히지 않으려면?", topic_size=170)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep14.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
