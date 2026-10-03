"""EP.31 'PE 벤치마크' — 9:16 웹툰 숏폼.
우리 펀드 IRR 14%. 같은 빈티지·전략이라도 벤치마크 A의 중간값이 13%면 +1%p(상위 절반), B의 중간값이 15%면 −1%p(하위 절반).
같은 성적, 다른 등수 — 빈티지·전략·지역·데이터원을 맞추고 EP.06 PME로 시장과도 비교한다."""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep31_{i}.png" for i in (1, 2, 3)]
Y0, KY = 820, 20            # IRR 0% 기준 y, 1%p = 20px (25% → 500px)


def cut1(t): return title_cut(t, "EP.31 · PE 벤치마크")


def cut2(t):
    return problem_cut(t, "#F6EEDB", "Top Quartile!", GOLD, "GP 마케팅 자료 · 펀드 3호", GOLD, "2018 빈티지 · 바이아웃 · IRR 14%",
                       ("등수", "Top 25%", GREEN, 76), ("기준표", "?", RED, 110), "무조건!",
                       ["상위 25%래요!", "다음 펀드도 무조건 가죠!"], sfx_size=90, mood="happy", bubble_size=56, bubble_w=780, title_size=100)


def cut3(t):
    return twist_cut(t, ["누구 표로 쟀는지부터 봐.", "같은 빈티지 · 같은 전략끼리 비교해야 해."], "어느 표 기준?", size=46, sfx_size=140)


def qbox(t, a0, x, lo, med, hi, name, c):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    y = lambda v: Y0 - v * KY
    o = [f'<g opacity="{g:.2f}">',
         f'<rect x="{x-110}" y="{y(hi):.0f}" width="220" height="{(hi-lo)*KY:.0f}" fill="{c}" opacity=".25" stroke="{c}" stroke-width="5"/>',
         f'<line x1="{x-110}" y1="{y(med):.0f}" x2="{x+110}" y2="{y(med):.0f}" stroke="{c}" stroke-width="8"/>',
         label(f"상위 {hi}%", x, y(hi) - 24, 30, c, 900), label(f"중간 {med}%", x + 125, y(med), 30, c, 900, "start"),
         label(f"하위 {lo}%", x, y(lo) + 30, 30, c, 900), label(name, x, Y0 + 48, 34, NAVY, 900), "</g>"]
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "같은 성적, 다른 등수", "2018 빈티지 · 바이아웃 · 사분위 IRR (예시)")
    s.append(qbox(t, .6, 280, 7, 13, 20, "벤치마크 A", TEAL))
    s.append(qbox(t, 1.4, 700, 8, 15, 22, "벤치마크 B", PURPLE_C))
    if t > 2.4:
        a = ease_out(prog(t, 2.4, .5)); y = Y0 - 14 * KY
        s.append(f'<line x1="110" y1="{y}" x2="{110 + 860*a:.0f}" y2="{y}" stroke="{RED}" stroke-width="6" stroke-dasharray="18 10"/>')
        if a > .9: s.append(label("우리 14%", 120, y - 22, 32, RED, 900, "start"))
    if t > 3.2:
        a = ease_out(prog(t, 3.2, .4))
        s.append(f'<g opacity="{a:.2f}">' + label("A 기준: 중간보다 위", 280, 915, 30, TEAL, 900) + label("B 기준: 중간보다 아래", 700, 915, 30, PURPLE_C, 900) + "</g>")
    s.append(chip("빈티지 · 전략 · 지역 · 데이터원을 맞춘다", 540, 1005, NAVY, back(prog(t, 4.0, .4)), w=800, size=38))
    s += explain_tail(t, EQ, (1105, 1185, 1270), 5.0, "등수는 표가 정한다 — PME로 시장과도 비교", 1475, 7.8,
                      ["EP.06 PME까지 같이 보면", "등수의 착시가 줄지."], 8.6, eq_scale=.46)
    return s


PURPLE_C = "#6B3FA0"


def cut5(t):
    return relief_cut(t, ["그럼 뭘로", "비교해요?"], ["빈티지·전략이 같은 표로 등수를 보고,", "EP.06 PME로 시장과도 견주지."], "두 개로!",
                      "체크: 빈티지 · 전략 · 지역 · 데이터원 · PME 병행", chip_size=34, mood="happy", sfx_size=110)


def cut6(t): return next_cut(t, TEAL, "First Close", "먼저 들어가면 뭐가 좋아?", topic_size=180)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep31.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
