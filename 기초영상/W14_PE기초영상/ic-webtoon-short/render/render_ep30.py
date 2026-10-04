"""EP.30 '공정가치 평가' — 9:16 웹툰 숏폼.
회사 P: EBITDA 10 × 비교 배수 12 = EV 120, 순부채 40을 빼 지분가치 80. 실적은 그대로인데 배수를 14로 바꾸면
10 × 14 − 40 = 100 (+25%). 배수 2 차이가 NAV 25% — PE 회사 값은 GP가 IPEV 가이드라인으로 매기고 감사가 확인한다. (EP.20 평가 지연과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep30_{i}.png" for i in (1, 2, 3)]
BASE, K = 860, 2.8          # 1 = 2.8px (140 → 392px)


def cut1(t): return title_cut(t, "EP.30 · 공정가치 평가", chip_w=840)


def cut2(t):
    return problem_cut(t, "#E4ECF6", "25% 상승?!", BLUE, "분기 평가 보고 · 회사 P", BLUE, "매출 · 이익은 지난 분기와 같음",
                       ("지난 분기", "80", NAVY, 100), ("이번 분기", "100", GREEN, 100), "대박!",
                       ["회사가 한 분기 만에", "25%나 컸네요!"], sfx_size=96, mood="happy", bubble_size=56, bubble_w=780)


def cut3(t):
    return twist_cut(t, ["실적은 그대로야.", "비교 배수를 12에서 14로 바꿨지."], "배수 바꿨다!", size=50, sfx_size=150)


def stack(t, a0, x, ev, tag):
    o = []
    g = ease_out(prog(t, a0, .5)); h = 40 * K * g
    o.append(f'<rect x="{x-110}" y="{BASE-h:.0f}" width="220" height="{h:.0f}" fill="{GREY}"/>')
    if g > .9: o.append(label("순부채 40", x, BASE - 20 * K, 34, "#fff", 900))
    eq = ev - 40
    g2 = ease_out(prog(t, a0 + .6, .45)); h2 = eq * K * g2
    o.append(f'<rect x="{x-110}" y="{BASE-40*K-h2:.0f}" width="220" height="{h2:.0f}" fill="{GREEN}"/>')
    if g2 > .9:
        o.append(label(f"지분 {eq}", x, BASE - 40 * K - eq * K / 2, 40, "#fff", 900))
        o.append(label(f"EV {ev}", x, BASE - ev * K - 26, 34, NAVY, 900) + label(tag, x, BASE + 40, 32, NAVY, 900))
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "배수가 값을 정한다", "회사 P · EBITDA 10 · 순부채 40 · 비교 배수 12 vs 14 (예시)")
    s.append(baseline(t, BASE))
    s.append(stack(t, .6, 300, 120, "배수 12×"))
    s.append(stack(t, 2.0, 760, 140, "배수 14×"))
    if t > 3.4:
        s.append(f'<g opacity="{ease_out(prog(t, 3.4, .4)):.2f}">' + label("+25%", 530, BASE - 100 * K, 52, RED, 900) + "</g>")
    s.append(chip("EV는 17% 올랐는데 지분은 25% 올랐다 — 부채 때문", 540, 1010, BLUE, back(prog(t, 4.2, .4)), w=930, size=34))
    s += explain_tail(t, EQ, (1085, 1175, 1265), 5.2, "배수 2 차이가 NAV 25% — 근거부터 본다", 1475, 8.0,
                      ["EP.20 평가 지연에 더해", "평가 방법도 NAV를 흔들지."], 8.8)
    return s


def cut5(t):
    return relief_cut(t, ["그 배수는", "누가 정해요?"], ["GP가 IPEV 가이드라인으로 정하고", "감사와 LPAC가 확인하지."], "근거 확인!",
                      "체크: 비교 회사 · 배수 근거 · 순부채 · 감사 의견 · 변경 사유", chip_size=34, mood="happy")


def cut6(t): return next_cut(t, GOLD, "PE 벤치마크", "우리 펀드는 상위권인가?", topic_size=180)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep30.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
