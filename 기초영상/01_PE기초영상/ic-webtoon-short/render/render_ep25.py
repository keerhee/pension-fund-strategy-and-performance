"""EP.25 '배당 리캡' — 9:16 웹툰 숏폼.
회사 M(기업가치 150, 부채 50, 자본 100)이 빚 40을 더 내 펀드에 배당한다(Dividend Recap).
리캡 뒤 자본 60 + 배당 40 = 100 — 가치는 그대로, 부채 비율만 33% → 60%. DPI는 오르고 위험도 오른다.
(EP.12 NAV 론은 펀드가, 리캡은 회사가 빌린다)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep25_{i}.png" for i in (1, 2, 3)]
BASE, K = 860, 2.4          # 1 = 2.4px (150 → 360px)


def cut1(t): return title_cut(t, "EP.25 · 배당 리캡")


def cut2(t):
    return problem_cut(t, "#F6EEDB", "깜짝 배당!", GOLD, "Distribution Notice · 회사 M", GOLD, "매각 없음 · 재원: 회사 차입",
                       ("배당", "40", GREEN, 100), ("회사 부채", "+40", RED, 96), "실적 좋나?",
                       ["회사가 돈을 잘 벌어서", "배당 준 거죠?"], sfx_size=80, mood="happy", bubble_size=56, bubble_w=780)


def cut3(t):
    return twist_cut(t, ["회사가 빚을 내서 준 거야.", "배당 재자본화, Dividend Recap이지."], "Dividend Recap!", size=46, sfx_size=120)


def sbar(t, a0, x, debt, eq, tag):
    o = []
    g = ease_out(prog(t, a0, .5)); h = debt * K * g
    o.append(f'<rect x="{x-100}" y="{BASE-h:.0f}" width="200" height="{h:.0f}" fill="{GREY}"/>')
    if g > .9: o.append(label(f"부채 {debt}", x, BASE - debt * K / 2, 36, "#fff", 900))
    g2 = ease_out(prog(t, a0 + .6, .45)); h2 = eq * K * g2
    o.append(f'<rect x="{x-100}" y="{BASE-debt*K-h2:.0f}" width="200" height="{h2:.0f}" fill="{GREEN}"/>')
    if g2 > .9:
        o.append(label(f"자본 {eq}", x, BASE - debt * K - eq * K / 2, 36, "#fff", 900))
        o.append(label(tag, x, BASE + 40, 32, NAVY, 900) + label("EV 150", x, BASE - 150 * K - 26, 32, NAVY, 900))
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "가치는 그대로", "회사 M · 기업가치 150 · 추가 차입 40 → 배당 (예시)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(sbar(t, .6, 260, 50, 100, "① 리캡 전"))
    s.append(sbar(t, 2.0, 590, 90, 60, "② 리캡 후"))
    g = ease_out(prog(t, 3.4, .45)); h = 40 * K * g
    s.append(f'<rect x="800" y="{BASE-h:.0f}" width="140" height="{h:.0f}" fill="{GOLD}" rx="6"/>')
    if g > .9: s.append(label("배당 40", 870, BASE - h / 2, 32, "#fff", 900) + label("펀드로", 870, BASE + 40, 32, GOLD, 900))
    s.append(chip("자본 100 = 60 + 배당 40 · 부채 비율 33% → 60%", 540, 1000, GOLD, back(prog(t, 4.4, .4)), w=900, size=36))
    s += explain_tail(t, EQ, (1075, 1165, 1260), 5.4, "가치는 그대로, 빚만 늘었다 — DPI도 위험도 오른다", 1480, 8.2,
                      ["EP.12 NAV 론은 펀드가,", "리캡은 회사가 빌리는 거지."], 9.0, sum_size=40)
    return s


def cut5(t):
    return relief_cut(t, ["빚이 늘면", "위험하지 않아요?"], ["금리가 오르면 이자가 회사를 누르지.", "배당 재원이 이익인지 빚인지부터 봐."], "재원 확인!",
                      "체크: 부채 비율 · 이자보상배율 · 배당 재원 · 금리 민감도", chip_size=34, mood="shock")


def cut6(t): return next_cut(t, NAVY, "GP 커밋먼트", "GP도 자기 돈을 넣나?", topic_size=180)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep25.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
