"""EP.32 'First Close' — 9:16 웹툰 숏폼.
펀드 4호 첫 마감(First Close)에 100을 약정하면 얼리버드 보수 1.75%로 5년간 (2% − 1.75%) × 100 × 5 = 1.25를 아낀다.
12개월 뒤 최종 마감에 들어온 LP는 그동안 콜된 30에 동등화 이자 8% × 30 × 1 = 2.4를 얹어 32.4를 내고, 이자 2.4는 먼저 들어간 LP에게 간다.
대신 먼저 들어가면 포트폴리오를 덜 보고 결정한다(블라인드 위험)."""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep32_{i}.png" for i in (1, 2, 3)]
TX0, TX1, TY = 160, 920, 560   # 타임라인


def cut1(t): return title_cut(t, "EP.32 · First Close", chip_w=820)


def cut2(t):
    return problem_cut(t, "#E3F1EF", "얼리버드?", TEAL, "펀드 4호 · First Close 안내", TEAL, "첫 마감 참여 LP에 보수 할인",
                       ("관리보수", "1.75%", GREEN, 84), ("최종 마감", "1년 뒤", GOLD, 84), "급하게?",
                       ["늦게 들어가도 같은 펀드인데", "왜 서둘러요?"], sfx_size=88, mood="shock", bubble_size=52, bubble_w=880)


def cut3(t):
    return twist_cut(t, ["먼저 오면 보수를 깎아 주고,", "늦게 오면 그동안의 이자를 내지."], "얼리버드!", size=50, sfx_size=160)


def cut4(t):
    s = explain_frame(t, "먼저 vs 나중", "약정 100 · 얼리버드 1.75% · 동등화 이자 8% · 12개월 (예시)")
    a = ease_out(prog(t, .5, .5))
    s.append(f'<line x1="{TX0}" y1="{TY}" x2="{TX0 + (TX1-TX0)*a:.0f}" y2="{TY}" stroke="{NAVY}" stroke-width="6"/>')
    for x, top, bot, a0, c in ((TX0, "First Close", "0개월", .8, TEAL), (TX1, "Final Close", "12개월", 1.4, GOLD)):
        p = back(prog(t, a0, .4))
        if p > 0:
            s.append(f'<g transform="translate({x},{TY}) scale({p:.3f})"><circle r="26" fill="{c}"/></g>')
            s.append(label(top, x, TY - 60, 34, c, 900) + label(bot, x, TY + 60, 30, NAVY, 800))
    if t > 2.0:
        s.append(f'<g opacity="{ease_out(prog(t, 2.0, .4)):.2f}">' + label("그사이 콜 30 · 투자 시작", 540, TY - 40, 30, NAVY, 900) + "</g>")
    s.append(chip("우리(먼저): 보수 1.25 절감", 300, 720, TEAL, back(prog(t, 2.6, .4)), w=470, size=34))
    s.append(chip("LP B(나중): 30 + 이자 2.4", 780, 720, GOLD, back(prog(t, 3.2, .4)), w=470, size=34))
    if t > 3.8:
        a = ease_out(prog(t, 3.8, .4))
        s.append(f'<path d="M 780 770 C 700 860, 420 860, 330 775" fill="none" stroke="{GREEN}" stroke-width="6" stroke-dasharray="14 9" opacity="{a:.2f}"/>'
                 + f'<g opacity="{a:.2f}">' + label("이자 2.4 → 먼저 온 LP", 540, 880, 32, GREEN, 900) + "</g>")
    s.append(chip("먼저 오면 할인, 늦게 오면 이자", 540, 1000, NAVY, back(prog(t, 4.4, .4)), w=700, size=40))
    s += explain_tail(t, EQ, (1080, 1170, 1260), 5.4, "대신 먼저 결정하는 위험 — 볼 수 있는 게 적다", 1475, 8.2,
                      ["EP.02 캐피털 콜을 늦게 시작한", "LP가 내는 이자인 셈이지."], 9.0, eq_scale=.46)
    return s


def cut5(t):
    return relief_cut(t, ["먼저 들어가면", "손해는 없어요?"], ["포트폴리오를 덜 보고 결정하지.", "블라인드 위험이 더 크니까."], "블라인드!",
                      "체크: 할인 조건 · 동등화 이자 · 최종 마감일 · 블라인드 위험", chip_size=34, mood="shock", sfx_size=110)


def cut6(t): return next_cut(t, GREEN, "Re-up", "다음 펀드도 또 넣을까?", topic_size=240)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep32.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
