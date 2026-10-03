"""EP.19 '허들의 종류' — 9:16 웹툰 숏폼.
같은 8% 허들이라도 5년이면 복리 146.9 · 단리 140. 회수 150이면 (100% 캐치업 가정) GP Carry는 3.1 vs 10.
회수 200처럼 성과가 넉넉하면 캐치업으로 둘 다 20이 된다 — 차이는 허들 근처 성과에서 난다. (EP.10 캐치업과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep19_{i}.png" for i in (1, 2, 3)]
BASE, K = 820, 2.4          # 1 단위 = 2.4px (150 → 360px)


def cut1(t): return title_cut(t, "EP.19 · 허들의 종류")


def cut2(t):
    return problem_cut(t, "#F6EEDB", "둘 다 8%?", GOLD, "LPA 비교 · 우선수익(허들)", GOLD, "펀드 X와 펀드 Y · 5년 · 납입 100",
                       ("펀드 X", "8% 복리", NAVY, 60), ("펀드 Y", "8% 단리", TEAL, 60), "똑같죠?",
                       ["둘 다 8%니까", "똑같은 조건이죠?"], sfx_size=84, mood="happy", bubble_size=56, bubble_w=760)


def cut3(t):
    return twist_cut(t, ["이자가 붙는 방식이 달라.", "5년이면 기준선이 7 가까이 벌어져."], "복리 vs 단리!", size=48, sfx_size=140)


def stack(t, a0, x, lp, gp, tag, gp_c):
    o = []
    g = ease_out(prog(t, a0, .5)); h = lp * K * g
    o.append(f'<rect x="{x-110}" y="{BASE-h:.0f}" width="220" height="{h:.0f}" fill="{GREEN}"/>')
    if g > .9: o.append(label(f"LP {lp:g}", x, BASE - lp * K / 2, 42, "#fff", 900))
    g2 = ease_out(prog(t, a0 + .7, .4)); h2 = gp * K * g2
    o.append(f'<rect x="{x-110}" y="{BASE-lp*K-h2:.0f}" width="220" height="{h2:.0f}" fill="{gp_c}"/>')
    if g2 > .9:
        o.append(label(f"GP {gp:g}", x + 130, BASE - lp * K - gp * K / 2, 36, gp_c, 900, "start"))
        o.append(label(tag, x, BASE + 42, 34, NAVY, 900))
    return "".join(o)


def cut4(t):
    s = explain_frame(t, "기준선이 다르다", "납입 100 · 5년 · 회수 150 · 100% 캐치업 (예시)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(stack(t, .6, 280, 146.9, 3.1, "① 복리 허들", GOLD))
    s.append(stack(t, 2.0, 700, 140, 10, "② 단리 허들", GOLD))
    for x, v, a0 in ((280, 146.9, 1.0), (700, 140, 2.4)):
        if t > a0:
            a = ease_out(prog(t, a0, .4)); y = BASE - v * K
            s.append(f'<line x1="{x-150}" y1="{y:.0f}" x2="{x-150+300*a:.0f}" y2="{y:.0f}" stroke="{RED}" stroke-width="4" stroke-dasharray="12 8"/>')
    if t > 3.4:
        s.append(f'<g opacity="{ease_out(prog(t, 3.4, .4)):.2f}">' + label("허들선", 130, BASE - 146.9 * K - 18, 26, RED, 900, "start") + "</g>")
    s.append(chip("회수 200이면? 캐치업으로 둘 다 GP 20", 540, 1000, NAVY, back(prog(t, 4.4, .4)), w=820, size=38))
    s += explain_tail(t, EQ, (1080, 1170, 1260), 5.4, "성과가 허들 근처일수록 복리·단리 차이가 커진다", 1470, 8.0,
                      ["EP.10 캐치업이 끝까지 가면", "결국 20%로 같아지지."], 8.8, sum_size=40, eq_scale=.46)
    return s


def cut5(t):
    return relief_cut(t, ["그럼 어떤 조건을", "봐야 해요?"], ["복리인지, 납입액 기준인지, 언제부터 세는지.", "같은 8%도 계산서가 달라."], "계산서 확인!",
                      "체크: 복리/단리 · 기준(납입/약정) · 기산 시점 · 캐치업 비율", chip_size=33, a_size=42, mood="happy", sfx_size=90)


def cut6(t): return next_cut(t, NAVY, "평가 지연", "PE는 왜 덜 떨어져 보이나?", topic_size=200)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep19.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
