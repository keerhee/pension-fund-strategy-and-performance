"""시즌 2 「지킬 것부터 사라」 EP.16 '매년 다시 잡는 Floor (Flexicure)' — 9:16 웹툰 숏폼. (GBI 2막 끝)
Flexicure(EDHEC 2018): 매년 초 F = 0.8A, 재설정 직후 쿠션 0.2A → 비중 = m × 0.2. A 10 · F 8 · m 3 출발, PSP 60%.
1년 뒤 벌었을 때(주식 +25%) A 11.5 → 재설정 F 9.2(이익 잠금) · 60% / 고정 F 8이면 91%.
잃었을 때(주식 −25%) A 8.5 → 재설정 F 6.8 · 60% / 고정이면 18%(Cash Trap 근접). 보호 대상은 금액이 아니라 '한 해 손실 ≤ 20%'.
(W06 M8 2교시 44~45장 그대로, EP.15 Cash Trap의 해법)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep16_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.16 · 매년 다시 잡는 Floor", chip_w=900)
    s.insert(2, punch("시즌 2 · GBI 2막", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: Floor는 끝까지 고정?
    s = [bg("#DDF0EE")]
    s.append(punch("Floor 고정?", 540, 170, 120, fill=TEAL, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{TEAL}"/><rect x="-390" y="-180" width="780" height="26" fill="{TEAL}"/>'
                 + label("CPPI 운용 1년 결산 (예시)", 0, -202, 42, "#fff", 900)
                 + label("출발 A 10 · F 8 · m 3 → 주식 60%", 0, -100, 38, NAVY, 900)
                 + label("올해 주식 −25% → A 8.5", 0, -25, 44, RED, 900)
                 + f'<rect x="-320" y="50" width="640" height="120" rx="18" fill="#E6ECF7"/>'
                 + label("펭의 안: Floor 8 그대로 유지", 0, 110, 40, BLUE, 900)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("약속은 약속!", 760, 975, 72, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["Floor를 내리면 보호가 깨지니까", "8억을 끝까지 지켜야죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=48))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["고정하면 주식 18%에 갇혀. 매년 Floor를", "다시 잡으면 60%로 회복에 참여하지."], 540, 330, 1030, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=42))
    if t > 3.2:
        s.append(punch("매년 리셋!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


COLX = [215, 480, 690, 890]
ROWS = [("벌었을 때 A 11.5", GREEN, "9.2 (잠금)", "60%", "91%", NAVY),
        ("잃었을 때 A 8.5", RED, "6.8", "60%", "18%", RED)]


def cut4(t):   # 해설: 1년 뒤 표 → 규칙 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("Flexicure 규칙", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("매년 초 F = 0.8A · m = 3 (45세 예시) · EDHEC 2018", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(chip("출발: A 10 · F 8 · m 3 → 주식 60%", 540, 405, NAVY, back(prog(t, .5, .4)), w=700, size=34))
    a = ease_out(prog(t, 1.2, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("1년 뒤", COLX[0], 490, 30, GREY, 900) + label("재설정 F", COLX[1], 490, 30, TEAL, 900)
             + label("재설정 후", COLX[2], 490, 30, TEAL, 900) + label("고정하면", COLX[3], 490, 30, GREY, 900)
             + f'<line x1="90" y1="520" x2="990" y2="520" stroke="{NAVY}" stroke-width="3"/></g>')
    for i, (name, c, f, w1, w2, c2) in enumerate(ROWS):
        y = 570 + 80 * i
        g = ease_out(prog(t, 1.8 + 1.2 * i, .4))
        s.append(f'<g opacity="{g:.2f}">' + label(name, COLX[0], y, 30, c, 900) + label(f, COLX[1], y, 34, TEAL, 900)
                 + label(w1, COLX[2], y, 38, TEAL, 900) + "</g>")
        s.append(chip(w2, COLX[3], y, c2, back(prog(t, 2.4 + 1.2 * i, .4)), w=140, size=34))
    s.append(f'<g opacity="{ease_out(prog(t, 4.6, .4)):.2f}">' + label("← Cash Trap 근접", 990, 700, 26, RED, 900, anchor="end") + "</g>")
    s.append(chip("나이별 m = TDF 주식 비중 ÷ 0.2 → 45세 3 · 65세 1", 540, 775, TEAL, back(prog(t, 5.0, .4)), w=880, size=30))
    for i, (y, sc) in enumerate(((845, .41), (960, .41), (1060, .41))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.6 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 8.2, .5))}">' + label("보호 대상은 금액이 아니라 ‘한 해 손실 ≤ 20%’", 540, 1400, 44, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.6, .5))}">' + label("벌면 잠그고, 잃으면 새 출발선 — Cash Trap을 피한다", 540, 1480, 34, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["매트를 해마다 새로 깔아서", "늘 같은 높이로 뛰는 셈이야."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry")
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: F = 0.8A · 나이별 m · 연중 손실 한도 · 고정 vs 재설정", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=940, size=33)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["Floor 금액이 줄어드는 건", "괜찮은 거예요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=48))
    if t > 1.6:
        s.append(bubble(["그게 대가야. 보호가 먼저면 고정,", "참여가 먼저면 재설정 — IC가 정해."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("IC가 고른다!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, "#B8462E", "디폴트옵션", "800만 명에게도 작동할까?", topic_size=160)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_ep16.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
