"""EP.27 '웨어하우징' — 9:16 웹툰 숏폼.
GP가 새 펀드 결성 전에 회사를 100에 미리 사 두고(웨어하우징), 결성 뒤 원가 + 보유 이자 5% = 105에 펀드로 넘긴다.
그사이 가치가 120이면 새 펀드 LP는 +15로 J-커브를 건너뛰고, 90이면 −15를 떠안는다 — 그래서 LPAC 승인과 거부권. (EP.01 · EP.22와 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep27_{i}.png" for i in (1, 2, 3)]
BASE, K = 840, 3.2          # 1 = 3.2px (120 → 384px)


def cut1(t): return title_cut(t, "EP.27 · 웨어하우징", chip_w=820)


def cut2(t):
    return problem_cut(t, "#E3F1EF", "벌써 회사가?", TEAL, "신규 3호 펀드 · 결성 제안서", TEAL, "씨드 자산 3개를 원가 + 이자로 인수",
                       ("인수 가격", "105", NAVY, 96), ("결성 전 매입", "1년 전", GOLD, 70), "벌써?!",
                       ["펀드도 안 생겼는데", "벌써 회사가 있어요?"], sfx_size=90, mood="shock", bubble_size=56, bubble_w=780)


def cut3(t):
    return twist_cut(t, ["GP가 미리 사서 창고에 넣어 둔 거야.", "그걸 웨어하우징이라고 하지."], "웨어하우징!", size=46, sfx_size=150)


def cut4(t):
    s = explain_frame(t, "넘기는 값과 지금 값", "1년 전 100에 매입 · 보유 이자 5% · 원가 + 이자로 이전 (예시)")
    s.append(baseline(t, BASE))
    s.append(vbar(t, .6, 300, 120, K, BASE, GREEN, "120", ("오른 경우",)))
    s.append(vbar(t, 1.4, 780, 90, K, BASE, RED, "90", ("떨어진 경우",)))
    if t > 2.2:
        a = ease_out(prog(t, 2.2, .5)); y = BASE - 105 * K
        s.append(f'<line x1="140" y1="{y:.0f}" x2="{140 + 800*a:.0f}" y2="{y:.0f}" stroke="{NAVY}" stroke-width="6" stroke-dasharray="16 10"/>')
        if a > .9: s.append(label("이전가 105", 540, y - 24, 34, NAVY, 900))
    if t > 3.0:
        a = ease_out(prog(t, 3.0, .4))
        s.append(f'<g opacity="{a:.2f}">' + label("+15", 300, BASE - 112.5 * K, 36, "#fff", 900) + label("−15", 950, BASE - 97.5 * K, 38, RED, 900) + "</g>")
    s.append(chip("오르면 J-커브를 건너뛰고, 떨어지면 떠안는다", 540, 1010, TEAL, back(prog(t, 4.0, .4)), w=900, size=36))
    s += explain_tail(t, EQ, (1085, 1175, 1265), 5.0, "원가 이전은 양날 — 떨어졌을 때 거부권이 있어야", 1475, 7.8,
                      ["EP.01 J-커브의 바닥을", "미리 지나온 자산인 셈이지."], 8.6)
    return s


def cut5(t):
    return relief_cut(t, ["떨어진 회사도", "떠안아요?"], ["그래서 LPAC 승인과 안 받을 권리를 넣어.", "EP.22와 같은 이해상충이지."], "거부권!",
                      "체크: 인수 가격 · 보유 비용 · 현재 가치 · LPAC 승인 · 거부권", chip_size=34, a_size=44, mood="shock", sfx_size=120)


def cut6(t): return next_cut(t, ORANGE, "펀드 연장", "10년 만기를 늘린다고?", topic_size=210)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep27.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
