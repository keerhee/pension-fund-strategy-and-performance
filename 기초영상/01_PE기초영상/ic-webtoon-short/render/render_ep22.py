"""EP.22 'LPAC' — 9:16 웹툰 숏폼.
GP가 회사 K를 1호 펀드에서 2호 펀드로 100에 넘기려 한다(독립 평가 110). 1호 LP는 10을 잃고 2호 LP는 10을 얻는다.
우리 기금은 1호에만 20% → 우리 몫 −2. GP가 양쪽에 서는 이해상충이라 LPAC(5석) 중 3석의 승인이 필요하다. (EP.08 컨티뉴에이션과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep22_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title_cut(t, "EP.22 · LPAC")


def cut2(t):
    return problem_cut(t, "#E3F1EF", "LPAC 소집?", TEAL, "LPAC 소집 통지 · 안건 1건", TEAL, "회사 K: 1호 → 2호 펀드로 이전",
                       ("이전 가격", "100", NAVY, 96), ("독립 평가", "110", RED, 96), "회의 또?",
                       ["GP가 알아서 하면 되지", "회의는 왜 해요?"], sfx_size=84, mood="happy", bubble_size=54, bubble_w=800)


def cut3(t):
    return twist_cut(t, ["GP가 파는 쪽과 사는 쪽에 다 서 있잖아.", "이해상충은 LPAC가 승인해야 해."], "이해상충!", size=44, sfx_size=160)


def fund_box(t, a0, x, name, delta, c):
    p = back(prog(t, a0, .45))
    if p <= 0: return ""
    return (f'<g transform="translate({x},530) scale({p:.3f})"><rect x="-150" y="-110" width="300" height="220" rx="20" fill="#fff" stroke="{c}" stroke-width="8"/>'
            + label(name, 0, -50, 42, c, 900) + label(delta, 0, 30, 46, RED if delta.startswith("−") else GREEN, 900) + "</g>")


def cut4(t):
    s = explain_frame(t, "누가 손해를 보나", "회사 K · 이전가 100 · 독립 평가 110 · 우리는 1호에 20% (예시)")
    s.append(fund_box(t, .6, 250, "1호 펀드", "−10", NAVY))
    s.append(fund_box(t, 1.0, 830, "2호 펀드", "+10", TEAL))
    if t > 1.6:
        a = ease_out(prog(t, 1.6, .5))
        s.append(f'<line x1="410" y1="530" x2="{410 + 250*a:.0f}" y2="530" stroke="{GOLD}" stroke-width="10"/>'
                 + (f'<polygon points="660,510 690,530 660,550" fill="{GOLD}"/>' if a > .95 else ""))
        if a > .9: s.append(label("회사 K", 540, 490, 34, GOLD, 900) + label("100에 이전", 540, 580, 30, NAVY, 800))
    if t > 2.4:
        s.append(f'<g opacity="{ease_out(prog(t, 2.4, .4)):.2f}">' + label("공정가 110 → 10만큼 1호에서 2호로 이동", 540, 690, 34, RED, 900) + "</g>")
    for i in range(5):                                   # LPAC 5석, 3석 승인
        p = back(prog(t, 3.2 + .2 * i, .35))
        if p <= 0: continue
        c = GREEN if i < 3 else GREY
        s.append(f'<g transform="translate({300 + 120*i},820) scale({p:.3f})"><circle r="44" fill="{c}"/>' + label("✓" if i < 3 else "", 0, 4, 44, "#fff", 900) + "</g>")
    if t > 4.4: s.append(label("LPAC 5석 중 3석 승인", 540, 905, 32, NAVY, 900))
    s.append(chip("우리 몫: 20% × (−10) = −2", 540, 1000, RED, back(prog(t, 4.8, .4)), w=640, size=40))
    s += explain_tail(t, EQ, (1080, 1170, 1260), 5.8, "가격이 공정한지 — 독립 평가로 LPAC가 확인한다", 1470, 8.4,
                      ["EP.08 컨티뉴에이션처럼", "GP가 양쪽에 서면 꼭 거치지."], 9.2)
    return s


def cut5(t):
    return relief_cut(t, ["LPAC 자리는", "누가 앉아요?"], ["보통 큰 LP들이야.", "자리를 받으면 시간과 책임도 같이 오지."], "책임도!",
                      "체크: 이해상충 승인 · 독립 평가 · 의결 정족수 · 무보수 봉사 · 면책", chip_size=33, mood="happy", sfx_size=110)


def cut6(t): return next_cut(t, RED, "GP 해임", "운용사를 바꿀 수 있나?", topic_size=220)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep22.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
