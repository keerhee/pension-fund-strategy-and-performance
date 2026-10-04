"""EP.20 '평가 지연' — 9:16 웹툰 숏폼.
상장주식이 Q1 −20%일 때 PE NAV는 −5%로 보고된다(평가가 한 박자 늦다). Geltner 언스무딩(φ = 0.5)으로 되돌리면
Q1 −10%, Q2 −15% — 보고 합계 −15% vs 언스무딩 −25%. 변동성이 작아 보이는 착시. (EP.06 PME · EP.07 분모 효과와 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep20_{i}.png" for i in (1, 2, 3)]
BASE, K = 480, 14           # 0% 기준선 y(위쪽), 1%p = 14px 아래로 (−20% → 280px)


def cut1(t): return title_cut(t, "EP.20 · 평가 지연")


def cut2(t):
    return problem_cut(t, "#E4ECF6", "PE는 안 빠졌다?", BLUE, "1분기 성과 보고", BLUE, "같은 분기, 같은 경기",
                       ("상장주식", "−20%", RED, 92), ("PE NAV", "−5%", GREEN, 92), "PE 짱!",
                       ["PE가 주식보다", "훨씬 안전하네요!"], sfx_size=90, mood="happy", bubble_size=56, bubble_w=760, title_size=100)


def cut3(t):
    return twist_cut(t, ["덜 떨어진 게 아니라 늦게 반영한 거야.", "평가가 한 박자씩 따라오거든."], "평가 지연!", size=46, sfx_size=160)


def dbar(t, a0, x, v, c, w=110):
    g = ease_out(prog(t, a0, .45))
    if g <= 0: return ""
    h = -v * K * g
    o = [f'<rect x="{x-w/2}" y="{BASE}" width="{w}" height="{h:.0f}" fill="{c}" rx="4"/>']
    if g > .9: o.append(label(f"{v:g}%", x, BASE + h + 30, 32, c, 900))
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "늦게 따라오는 NAV", "Geltner 언스무딩 φ = 0.5 · 분기 수익률 (예시)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    lg = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{lg:.2f}">'
             + f'<rect x="120" y="370" width="26" height="26" fill="{GREY}"/>' + label("상장주식", 156, 384, 28, NAVY, 800, "start")
             + f'<rect x="400" y="370" width="26" height="26" fill="{GREEN}"/>' + label("PE 보고", 436, 384, 28, NAVY, 800, "start")
             + f'<rect x="640" y="370" width="26" height="26" fill="{RED}"/>' + label("PE 언스무딩", 676, 384, 28, NAVY, 800, "start") + "</g>")
    for q, (x0, pub, rep, true, a0) in enumerate(((300, -20, -5, -10, .8), (720, -5, -10, -15, 2.6))):
        s.append(dbar(t, a0, x0 - 125, pub, GREY))
        s.append(dbar(t, a0 + .5, x0, rep, GREEN))
        s.append(dbar(t, a0 + 1.0, x0 + 125, true, RED))
        if t > a0: s.append(label(f"Q{q+1}", x0, 820, 40, NAVY, 900))
    s.append(chip("보고 합계 −15% vs 언스무딩 −25%", 540, 1000, RED, back(prog(t, 4.6, .4)), w=760, size=38))
    s += explain_tail(t, EQ, (1075, 1175, 1265), 5.6, "변동성이 작아 보이는 건 착시 — 위험은 줄지 않았다", 1480, 8.2,
                      ["보고 숫자로 위험을 재면", "분산효과를 과대평가하지."], 9.0, sum_size=40, eq_scale=.46)
    return s


def cut5(t):
    return relief_cut(t, ["그럼 PE 비중이 갑자기", "늘어난 건요?"], ["주식이 먼저 빠져서 그래.", "EP.07 분모 효과의 출발점이지."], "착시 주의!",
                      "체크: 평가 시차 · 언스무딩 · 상장 대용 지수 · 위험 예산 · 분모 효과", chip_size=31, q_size=48, mood="shock")


def cut6(t): return next_cut(t, PURPLE_NEXT, "Side Letter", "큰 LP만 받는 특별 조건?", topic_size=180)


PURPLE_NEXT = "#6B3FA0"

if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep20.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
