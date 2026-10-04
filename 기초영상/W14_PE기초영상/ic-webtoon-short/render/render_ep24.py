"""EP.24 'ESG 조항' — 9:16 웹툰 숏폼.
펀드가 회사 A(기업가치 100, 배출 500t)에 20, 회사 B(150, 300t)에 30을 넣었다. 지분만큼 배출도 우리 몫이다(PCAF식 귀속):
A 20/100 × 500 = 100, B 30/150 × 300 = 60 → 합계 160 tCO2e. 측정해야 줄일 수 있다 — 그래서 LP가 ESG 조항(배제 목록 · 연 1회 보고)을 요구한다."""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep24_{i}.png" for i in (1, 2, 3)]
BASE, K = 860, .8           # 1 tCO2e = 0.8px (500 → 400px)


def cut1(t): return title_cut(t, "EP.24 · ESG 조항")


def cut2(t):
    return problem_cut(t, "#E3F1E8", "탄소 정보 없음?", GREEN, "LP 요청서 · ESG 조항", GREEN, "GP 연차 보고: 탄소 정보 없음",
                       ("배제 목록", "추가", NAVY, 80), ("탄소 보고", "연 1회", GREEN, 76), "수익만?",
                       ["수익만 잘 내면", "되는 거 아니에요?"], sfx_size=88, mood="happy", bubble_size=56, bubble_w=760, title_size=100)


def cut3(t):
    return twist_cut(t, ["연기금은 수십 년을 들고 가.", "측정 못 하는 위험은 관리도 못 하지."], "측정부터!", size=46, sfx_size=160)


def ebar(t, a0, x, total, ours, name, share):
    o = []
    g = ease_out(prog(t, a0, .5)); h = total * K * g
    o.append(f'<rect x="{x-100}" y="{BASE-h:.0f}" width="200" height="{h:.0f}" fill="{GREY}" rx="6"/>')
    if g > .9: o.append(label(f"회사 배출 {total}t", x, BASE - h - 28, 32, GREY, 900) + label(name, x, BASE + 40, 34, NAVY, 900))
    g2 = ease_out(prog(t, a0 + .8, .45)); h2 = ours * K * g2
    o.append(f'<rect x="{x-100}" y="{BASE-h2:.0f}" width="200" height="{h2:.0f}" fill="{GREEN}" rx="6"/>')
    if g2 > .9:
        o.append(label(f"우리 몫 {ours}", x, BASE - h2 / 2, 34, "#fff", 900))
        o.append(label(share, x, BASE + 80, 28, GREEN, 900))
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "지분만큼 배출도", "투자액 ÷ 기업가치 × 배출량 (PCAF식 · 예시)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(ebar(t, .6, 330, 500, 100, "회사 A", "투자 20 / 가치 100"))
    s.append(ebar(t, 2.2, 750, 300, 60, "회사 B", "투자 30 / 가치 150"))
    s.append(chip("우리 몫 배출 160 tCO2e · 투자 50", 540, 1010, GREEN, back(prog(t, 4.2, .4)), w=720, size=38))
    s += explain_tail(t, EQ, (1085, 1180, 1275), 5.2, "지분만큼 배출도 우리 몫 — 재야 줄인다", 1480, 8.0,
                      ["숫자가 있어야", "GP와 줄일 계획을 얘기하지."], 8.8)
    return s


def cut5(t):
    return relief_cut(t, ["그럼 탄소 많은 회사는", "다 빼요?"], ["배제만 답은 아니야.", "전환 계획을 약속받는 방법도 있지."], "전환 계획!",
                      "체크: 배제 목록 · PCAF 보고 · 측정 범위 · 전환 계획", chip_size=34, q_size=48, mood="happy")


def cut6(t): return next_cut(t, GOLD, "배당 리캡", "빚을 내서 배당한다?", topic_size=210)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep24.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
