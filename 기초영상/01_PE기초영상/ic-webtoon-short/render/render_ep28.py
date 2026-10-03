"""EP.28 '펀드 연장' — 9:16 웹툰 숏폼.
만기 10년차에 못 판 회사가 NAV 300 남았다. 2년 연장해 330에 팔면 연장 보수 1% × 300 × 2 = 6을 빼고 324,
지금 세컨더리로 팔면 85% = 255(EP.07). 차이 69가 '2년 기다림의 값'이다. 연장은 LP 동의 사항 — 보수를 줄이라고 요구한다."""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep28_{i}.png" for i in (1, 2, 3)]
BASE, K = 840, 1.15         # 1 = 1.15px (330 → 380px)


def cut1(t): return title_cut(t, "EP.28 · 펀드 연장")


def cut2(t):
    return problem_cut(t, "#FBE9DD", "만기인데?", ORANGE, "만기 연장 요청 · 10년차", ORANGE, "못 판 회사 4개 · 잔여 NAV 300",
                       ("연장", "+2년", NAVY, 96), ("연장 중 보수", "1%", RED, 96), "끝 아냐?",
                       ["만기면 끝 아니에요?", "돈은 언제 받아요?"], sfx_size=90, mood="shock", bubble_size=56, bubble_w=780)


def cut3(t):
    return twist_cut(t, ["못 판 회사가 남았어.", "더 기다리거나, 지금 팔거나 — 고르는 거야."], "연장 vs 매각!", size=46, sfx_size=140)


def cut4(t):
    s = explain_frame(t, "기다림의 값", "잔여 NAV 300 · 2년 연장 후 330 매각 · 연장 보수 1% (예시)")
    s.append(baseline(t, BASE))
    s.append(vbar(t, .6, 330, 324, K, BASE, GREEN, "324", ("① 2년 연장", "330 − 보수 6")))
    s.append(vbar(t, 1.6, 750, 255, K, BASE, GREY, "255", ("② 지금 매각", "세컨더리 85%")))
    if t > 2.6:
        s.append(f'<g opacity="{ease_out(prog(t, 2.6, .4)):.2f}">' + label("차이 69", 540, BASE - 290 * K, 42, NAVY, 900) + "</g>")
    s.append(chip("69 = 2년 더 기다리는 값 (예상이 맞다면)", 540, 1020, ORANGE, back(prog(t, 3.8, .4)), w=860, size=38))
    s += explain_tail(t, EQ, (1095, 1185, 1275), 4.8, "기다림의 값과 보수를 비교 — 연장은 LP 동의 사항", 1480, 7.6,
                      ["EP.07 세컨더리, EP.08 CV도", "연장의 대안이 되지."], 8.4, sum_size=40)
    return s


def cut5(t):
    return relief_cut(t, ["연장하는 동안", "보수는요?"], ["줄이거나 없애라고 요구하지.", "기다림을 GP 수입으로 만들면 안 되니까."], "보수 협상!",
                      "체크: 연장 횟수 · 연장 중 보수 · LP 동의 · 대안(세컨더리 · CV)", chip_size=34, mood="happy")


def cut6(t): return next_cut(t, GREY, "테일엔드", "마지막 몇 개 회사는?", topic_size=220)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep28.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
