"""EP.26 'GP 커밋먼트' — 9:16 웹툰 숏폼.
GP도 자기 돈을 넣는다 — 약정 1,000의 2% = 20. 10년 관리보수 200의 10분의 1이다. 펀드가 0.9×로 끝나면 GP도 2를 잃는다.
같이 잃어야 같이 조심한다 — 다만 현금인지, 보수 면제(cashless)로 채운 것인지 확인한다. (EP.09 2 and 20과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep26_{i}.png" for i in (1, 2, 3)]
BASE, K = 840, 1.8          # 1 = 1.8px (200 → 360px)


def cut1(t): return title_cut(t, "EP.26 · GP 커밋먼트", chip_w=820)


def cut2(t):
    return problem_cut(t, "#E4ECF6", "GP는 얼마 넣나?", BLUE, "LPA 요약 · 펀드 3호 · 약정 1,000", BLUE, "GP 커밋먼트 조항",
                       ("GP 출자", "2%", NAVY, 100), ("금액", "20", GOLD, 100), "겨우?",
                       ["GP는 남의 돈만", "굴리는 거 아니었어요?"], sfx_size=96, mood="shock", bubble_size=54, bubble_w=800, title_size=100)


def cut3(t):
    return twist_cut(t, ["GP도 자기 돈을 넣어.", "같이 잃어야 같이 조심하거든."], "Skin in the Game!", size=48, sfx_size=110)


def cut4(t):
    s = explain_frame(t, "얼마나 같이 잃나", "약정 1,000 · GP 출자 2% · 관리보수 2% × 10년 (예시)")
    s.append(baseline(t, BASE))
    s.append(vbar(t, .6, 260, 200, K, BASE, ORANGE, "200", ("10년 보수",)))
    s.append(vbar(t, 1.4, 540, 20, K, BASE, NAVY, "20", ("GP 출자",)))
    s.append(vbar(t, 2.2, 820, 2, K, BASE, RED, "−2", ("0.9×일 때", "GP 손실"), top_size=42))
    if t > 3.0:
        s.append(f'<g opacity="{ease_out(prog(t, 3.0, .4)):.2f}">' + label("보수의 10분의 1", 540, BASE - 120, 32, NAVY, 900) + "</g>")
    s.append(chip("GP 출자 20 = 보수 200의 10%", 540, 1010, NAVY, back(prog(t, 4.2, .4)), w=680, size=40))
    s += explain_tail(t, EQ, (1085, 1175, 1265), 5.2, "같이 잃어야 같이 조심한다 — 현금인지부터 본다", 1475, 8.0,
                      ["EP.09 보수만 받는 GP와", "자기 돈 넣은 GP는 다르지."], 8.8)
    return s


def cut5(t):
    return relief_cut(t, ["2%면 너무", "적지 않아요?"], ["펀드보다 GP 개인 재산 대비가 중요해.", "보수 면제로 채우면 진짜 돈이 아니지."], "현금 확인!",
                      "체크: 출자 비율 · 현금 vs 보수 면제 · 개인 재산 대비 · 납입 시점", chip_size=34, mood="happy")


def cut6(t): return next_cut(t, TEAL, "웨어하우징", "펀드가 생기기 전에 산다?", topic_size=190)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep26.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
