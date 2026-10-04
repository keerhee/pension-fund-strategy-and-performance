"""EP.21 'Side Letter' — 9:16 웹툰 숏폼.
LP A(약정 300)가 Side Letter로 관리보수 1.5%를 받았다. MFN(최혜국 대우) 기준이 약정 200 이상이면
LP B(200)는 같은 조건을 골라 5년간 5를 아끼고(A는 7.5), LP C(50)는 기준 미달이라 2%를 그대로 낸다.
같은 펀드, 다른 보수 — 약정 크기와 MFN이 가른다."""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep21_{i}.png" for i in (1, 2, 3)]
PURPLE = "#6B3FA0"
X0, KX = 260, 2.0           # 가로 막대 시작 x, 약정 1 = 2px (300 → 600px)


def cut1(t): return title_cut(t, "EP.21 · Side Letter")


def cut2(t):
    return problem_cut(t, "#EEE7F6", "LP A만 할인?", PURPLE, "Side Letter 공개 · 펀드 Z", PURPLE, "LP A (약정 300)에게만",
                       ("관리보수", "1.5%", GREEN, 92), ("우리 펀드", "2.0%", RED, 92), "불공평!",
                       ["다른 LP만 깎아 줬어요?", "우리는 2%인데요!"], sfx_size=90, mood="shock", bubble_size=54, bubble_w=820)


def cut3(t):
    return twist_cut(t, ["그래서 MFN 조항이 있지.", "약정이 기준 이상이면 같은 조건을 고를 수 있어."], "최혜국 대우!", size=44, sfx_size=140)


def hbar(t, a0, y, who, v, c, fee, fee_c):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    w = v * KX * g
    o = [label(who, X0 - 20, y, 36, NAVY, 900, "end"),
         f'<rect x="{X0}" y="{y-45}" width="{w:.0f}" height="90" fill="{c}" rx="8"/>']
    if g > .9:
        o.append(label(f"{v}", X0 + w / 2 if w > 120 else X0 + w + 40, y, 38, "#fff" if w > 120 else c, 900))
        o.append(chip(fee, 950, y, fee_c, 1, w=140, size=34))
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "누가 1.5%를 받나", "펀드 Z · 5년 · MFN 기준 약정 200 이상 (예시)")
    s.append(hbar(t, .6, 480, "LP A", 300, PURPLE, "1.5%", GREEN))
    s.append(hbar(t, 1.4, 640, "LP B", 200, TEAL, "1.5%", GREEN))
    s.append(hbar(t, 2.2, 800, "LP C", 50, GREY, "2.0%", RED))
    if t > 3.0:
        a = ease_out(prog(t, 3.0, .4)); x = X0 + 200 * KX
        s.append(f'<line x1="{x}" y1="{400}" x2="{x}" y2="{400 + 470*a:.0f}" stroke="{RED}" stroke-width="5" stroke-dasharray="14 9"/>')
        if a > .9: s.append(label("MFN 기준 200", x, 382, 30, RED, 900))
    if t > 3.6:
        s.append(f'<g opacity="{ease_out(prog(t, 3.6, .4)):.2f}">' + label("MFN 선택", 950, 700, 26, TEAL, 900) + "</g>")
    s.append(chip("5년 보수 절감: A 7.5 · B 5 · C 0", 540, 1000, PURPLE, back(prog(t, 4.6, .4)), w=760, size=38))
    s += explain_tail(t, EQ, (1080, 1170, 1260), 5.6, "같은 펀드, 다른 보수 — 약정 크기와 MFN이 가른다", 1470, 8.2,
                      ["Side Letter는 비밀이 아니야.", "MFN으로 목록을 받아 보지."], 9.0, sum_size=40)
    return s


def cut5(t):
    return relief_cut(t, ["그럼 A의 조건을", "다 따라가요?"], ["규제·세금처럼 A만의 사정은 빠져.", "고를 수 있는 목록과 기한을 봐야지."], "목록 확인!",
                      "체크: MFN 기준 약정액 · 선택 기한 · 제외 조항 · 보수 · 공시", chip_size=33, mood="happy")


def cut6(t): return next_cut(t, TEAL, "LPAC", "LP가 GP에게 말하는 자리?", topic_size=230)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep21.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
