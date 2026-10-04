"""EP.33 'Re-up' — 9:16 웹툰 숏폼 (시즌 1 마지막 화).
3호 TVPI 1.5×지만 DPI는 0.4× — 아직 미실현이 많다. 성과 40% × 4 + 팀 30% × 5 + 전략 20% × 3 + 조건 10% × 2 = 3.9 ≥ 3.5 → 재출자.
다만 펀드 규모가 1,000 → 2,000으로 두 배라 같은 100이면 우리 비중은 10% → 5%. 관계가 아니라 근거로 다시 넣는다."""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep33_{i}.png" for i in (1, 2, 3)]
SX0, SW = 120, 840          # 점수 막대: 5점 = 840px


def cut1(t): return title_cut(t, "EP.33 · Re-up")


def cut2(t):
    return problem_cut(t, "#E3F1E8", "4호도 넣죠?", GREEN, "Re-up 요청 · 펀드 4호", GREEN, "3호 성과 · 펀드 규모 1,000 → 2,000",
                       ("3호 TVPI", "1.5×", GREEN, 96), ("3호 DPI", "0.4×", RED, 96), "당연히!",
                       ["3호 잘했으니", "당연히 또 넣죠!"], sfx_size=90, mood="happy", bubble_size=56, bubble_w=740)


def cut3(t):
    return twist_cut(t, ["아직 미실현이 많아 — DPI 0.4야.", "팀·전략·규모까지 다시 심사하지."], "다시 심사!", size=48, sfx_size=160)


def cut4(t):
    s = explain_frame(t, "근거로 다시 넣는다", "가중 점수표 · 통과선 3.5 · 각 항목 5점 만점 (예시)")
    rows = (("성과 40% × 4", 1.6, GREEN), ("팀 30% × 5", 1.5, TEAL), ("전략 20% × 3", 0.6, BLUE), ("조건 10% × 2", 0.2, GOLD))
    x = SX0
    for i, (name, v, c) in enumerate(rows):
        g = ease_out(prog(t, .6 + .5 * i, .45)); w = SW * v / 5
        s.append(f'<rect x="{x:.0f}" y="470" width="{w*g:.0f}" height="110" fill="{c}" stroke="#fff" stroke-width="3"/>')
        if g > .9:
            if w > 60: s.append(label(f"{v:g}", x + w / 2, 525, 34, "#fff", 900))
            s.append(label(name, SX0, 640 + 46 * i, 32, c, 900, "start"))
        x += w
    if t > 2.8:
        a = ease_out(prog(t, 2.8, .4)); xt = SX0 + SW * 3.5 / 5
        s.append(f'<line x1="{xt}" y1="{450 - 20*a:.0f}" x2="{xt}" y2="450" stroke="{RED}" stroke-width="6"/>'
                 f'<line x1="{xt}" y1="600" x2="{xt}" y2="{600 + 20*a:.0f}" stroke="{RED}" stroke-width="6"/>')
        if a > .9: s.append(label("통과 3.5", xt, 410, 32, RED, 900) + label("합계 3.9", SX0 + SW * 3.9 / 5 + 20, 525, 34, NAVY, 900, "start"))
    if t > 3.6:
        s.append(f'<g opacity="{ease_out(prog(t, 3.6, .4)):.2f}">' + label("규모 2배 → 우리 비중 10% → 5%", 760, 760, 32, RED, 900) + "</g>")
    s.append(chip("3.9 ≥ 3.5 → 재출자 · 규모 변화는 따로 확인", 540, 1010, GREEN, back(prog(t, 4.2, .4)), w=880, size=36))
    s += explain_tail(t, EQ, (1085, 1175, 1265), 5.2, "관계가 아니라 근거로 — 기준은 미리 정해 둔다", 1475, 8.0,
                      ["EP.03 DPI와 TVPI,", "EP.31 벤치마크가 다 여기 모이지."], 8.8, eq_scale=.46)
    return s


def cut5(t):
    return relief_cut(t, ["점수가 낮으면", "관계가 끊겨요?"], ["그럴 수 있어. 그래서 기준을 미리 정해", "GP와 공유하지. 그게 프로그램 운용이야."], "기준이 먼저!",
                      "체크: TVPI·DPI · 팀 안정성 · 전략 일관성 · 규모 증가 · 조건", chip_size=32, a_size=42, mood="happy", sfx_size=96)


def cut6(t): return next_cut(t, NAVY, "시즌 2", "지킬 것부터 사라 — LDI · GBI", topic_size=230)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep33.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
