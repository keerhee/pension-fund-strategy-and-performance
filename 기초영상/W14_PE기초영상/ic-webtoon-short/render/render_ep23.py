"""EP.23 'GP 해임' — 9:16 웹툰 숏폼.
무과실 해임(No-fault removal)은 잘못이 없어도 LP 75% 동의로 GP를 바꿀 수 있다. A 40 + B 25 + C 15 = 80% ≥ 75%로 가결.
대신 공짜가 아니다 — 해임 보상으로 관리보수 1년치 20, 쌓인 Carry 15 중 60%(9)는 GP가 가져간다. (EP.18 키맨 조항과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep23_{i}.png" for i in (1, 2, 3)]
VX0, VW = 120, 840          # 투표 막대: x 시작, 100% 폭
BASE, K = 880, 8.0          # 비용 막대: 1 = 8px (20 → 160px)


def cut1(t): return title_cut(t, "EP.23 · GP 해임")


def cut2(t):
    return problem_cut(t, "#FBE3E6", "GP를 바꾸자!", RED, "LP 연서 · 해임 안건", RED, "성과 부진 3년 · 잘못은 없음",
                       ("해임 유형", "무과실", NAVY, 80), ("필요 동의", "75%", RED, 92), "바로 해고!",
                       ["성과가 나쁘면", "바로 해고하면 되죠!"], sfx_size=80, mood="happy", bubble_size=56, bubble_w=760)


def cut3(t):
    return twist_cut(t, ["잘못이 없어도 해임은 할 수 있어.", "대신 정족수가 높고 보상이 붙지."], "무과실 해임!", size=46, sfx_size=140)


def cut4(t):
    s = explain_frame(t, "해임은 공짜가 아니다", "약정 1,000 · 무과실 해임 정족수 75% (예시)")
    s.append(label("① 해임 투표 (약정 비중)", 120, 410, 34, NAVY, 900, "start") if t > .5 else "")
    x = VX0
    for i, (who, v, c) in enumerate((("A 40", 40, GREEN), ("B 25", 25, TEAL), ("C 15", 15, BLUE), ("D 10", 10, GREY), ("E 10", 10, GREY))):
        g = ease_out(prog(t, .6 + .3 * i, .35)); w = VW * v / 100
        s.append(f'<rect x="{x:.0f}" y="440" width="{w*g:.0f}" height="100" fill="{c}" stroke="#fff" stroke-width="3"/>')
        if g > .9: s.append(label(who, x + w / 2, 490, 32, "#fff", 900))
        x += w
    if t > 2.3:
        a = ease_out(prog(t, 2.3, .4)); xt = VX0 + VW * .75
        s.append(f'<line x1="{xt}" y1="{440 - 30*a:.0f}" x2="{xt}" y2="440" stroke="{RED}" stroke-width="6"/>'
                 f'<line x1="{xt}" y1="540" x2="{xt}" y2="{540 + 30*a:.0f}" stroke="{RED}" stroke-width="6"/>')
        if a > .9: s.append(label("75%", xt, 600, 32, RED, 900) + label("찬성 80% → 가결", VX0 + VW * .4, 600, 32, GREEN, 900))
    if t > 3.0: s.append(label("② 해임 비용", 120, 660, 34, NAVY, 900, "start"))
    for x0, v, c, top, bot, a0 in ((330, 20, ORANGE, "20", "해임 보상", 3.2), (750, 9, GOLD, "9", "Carry 유지", 3.8)):
        g = ease_out(prog(t, a0, .45)); h = v * K * g
        s.append(f'<rect x="{x0-90}" y="{BASE-h:.0f}" width="180" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9: s.append(label(top, x0, BASE - h - 28, 40, c, 900) + label(bot, x0, BASE + 40, 32, NAVY, 900))
    s.append(f'<line x1="200" y1="{BASE}" x2="880" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, 3.2, .4)):.2f}"/>')
    s.append(chip("가결 80% · 비용 20 + 9 = 29", 540, 1000, RED, back(prog(t, 4.6, .4)), w=640, size=40))
    s += explain_tail(t, EQ, (1080, 1170, 1260), 5.6, "바꿀 수는 있다 — 비용과 후임까지 계산하고", 1470, 8.2,
                      ["EP.18 키맨 조항이 브레이크라면", "해임은 운전대를 바꾸는 거지."], 9.0)
    return s


def cut5(t):
    return relief_cut(t, ["그럼 GP가 사기를", "치면요?"], ["그건 유과실(For-cause) 해임이야.", "정족수가 낮고 GP는 Carry를 잃지."], "유과실은 다르다!",
                      "체크: 해임 정족수 · 해임 보상 · Carry 귀속 · 후임 GP", chip_size=34, mood="shock", sfx_size=80)


def cut6(t): return next_cut(t, GREEN, "ESG 조항", "수익 말고 무엇을 약속받나?", topic_size=200)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep23.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
