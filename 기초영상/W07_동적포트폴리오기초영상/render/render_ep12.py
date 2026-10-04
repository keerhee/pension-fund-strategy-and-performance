"""시즌 3 EP.12 '자주 할수록 좋다?' — 리밸런싱 빈도의 경제학. NPS 규모(1,866조) · 20년 모의 패널 · bp/년:
일간 DR 60.5 − 비용 21.5 = +39.0 · 주간 +49.2 · 월간 61.0 − 5.4 = +55.7(최적) · 분기 +53.7(2bp 차) · 반기 +50.7 · 연간 +49.1.
더 자주가 아니라 집행 가능한 빈도. (W07 SS2 12·13·20장 그대로)"""
from s3kit import *

EQ = [f"eq/ep12_{i}.png" for i in (1, 2, 3)]
FREQ = [("일간", 60.5, 21.5, 39.0), ("주간", 59.4, 10.2, 49.2), ("월간", 61.0, 5.4, 55.7),
        ("분기", 56.7, 3.1, 53.7), ("반기", 52.8, 2.1, 50.7), ("연간", 50.5, 1.4, 49.1)]


def cut1(t): return title(t, "EP.12 · 자주 할수록 좋다?", 860)


def cut2(t):
    body = (label("목표: 7개 자산 고정 비중", 0, -110, 38, NAVY, 900)
            + label("점검 · 복원 주기", 0, -40, 36, "#555", 800) + punch("매일", 0, 35, 84, fill=ORANGE, sw=10)
            + label("“자주 맞출수록 DR을 더 줍는다”", 0, 150, 38, BLUE, 900))
    return problem(t, "매일 맞추자!", ORANGE, "#FCEBDD", "펭의 리밸런싱 규칙 초안 (NPS 규모)", body, ["자주 맞출수록", "더 많이 벌겠죠?"], "매일 매일!")


def cut3(t): return twist(t, ["매일 하면 비용 21.5bp가 먹어.", "월간~분기가 최적이고 둘은 2bp 차이야."], "비용이 먹는다!", size=44, sfx_size=130)


BASE, K = 790, 5.2


def cut4(t):
    s = explainer_frame(t, "빈도별 순 프리미엄", "NPS 규모 1,866조 · 20년 모의 패널 · bp/년 (DR = 순 + 비용)")
    s.append(f'<line x1="90" y1="{BASE}" x2="990" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (name, dr, cost, net) in enumerate(FREQ):
        x = 165 + 150 * i
        g = ease_out(prog(t, .7 + .4 * i, .5))
        if g <= 0: continue
        hn, hc = net * K * g, cost * K * g; best = name == "월간"
        s.append(f'<rect x="{x-50}" y="{BASE-hn:.0f}" width="100" height="{hn:.0f}" fill="{GREEN if best else TEAL}" rx="4"/>')
        s.append(f'<rect x="{x-50}" y="{BASE-hn-hc:.0f}" width="100" height="{hc:.0f}" fill="{RED}" opacity=".75" rx="4"/>')
        if g > .9:
            s.append(label(f"+{net:g}", x, BASE - dr * K - 26, 32, GREEN if best else TEAL, 900) + label(name, x, BASE + 34, 30, NAVY, 900))
    s.append(f'<g opacity="{ease_out(prog(t, 3.4, .4)):.2f}"><rect x="610" y="405" width="28" height="22" fill="{TEAL}"/>' + label("순 프리미엄", 648, 416, 24, TEAL, 900, anchor="start")
             + f'<rect x="790" y="405" width="28" height="22" fill="{RED}" opacity=".75"/>' + label("거래비용", 828, 416, 24, RED, 900, anchor="start") + "</g>")
    s.append(chip("일간은 비용 21.5bp에 잠식 · 월간 +56 ≈ 분기 +54", 540, 890, NAVY, back(prog(t, 3.8, .4)), w=860, size=32))
    s += eqs(t, EQ, (955, 1055, 1150), a0=4.4, scale=(.5, .48, .46))
    s += explainer_tail(t, "더 자주가 아니라 집행 가능한 빈도", "연간은 드리프트로 DR 자체가 준다 — 50.5bp",
                        ["줍는 동전보다 내는 통행료가", "커지면 안 되잖아."])
    return s


def cut5(t): return relief(t, ["국민연금은 실제로", "어떻게 하는 게 좋아요?"], ["월 점검 · 한 달 25bp 한도 · 선물로 먼저", "맞추는 안이 +42bp야. IC 보너스에서 보자."],
                           "규칙의 값!", "체크: 빈도 · 거래비용(스프레드 + 시장충격) · 실행 한도", a_size=40, sfx_size=120)


def cut6(t): return next_cut(t, RED, "평균회귀", "리밸런싱은 언제나 통할까?", topic_size=180)


META = dict(
    episode="EP.12", title="자주 할수록 좋다?",
    concept="리밸런싱 빈도의 경제학 — 분산수익 DR도 거래비용(스프레드 + 시장충격)도 빈도와 함께 변한다. 순 프리미엄 = DR − 비용은 일간이 비용에 잠식되고 월간~분기가 최적(2bp 차). 연간은 비중 드리프트로 DR 자체가 준다. 핵심은 '더 자주'가 아니라 '집행 가능한 빈도'",
    source="W07 SS2 12·13·20장(NPS 규모 1,866조 · 20년 모의 패널 · bp/년 — 일간 DR 60.5 · 비용 21.5 · 순 39.0, 주간 59.4 · 10.2 · 49.2, 월간 61.0 · 5.4 · 55.7(최적), 분기 56.7 · 3.1 · 53.7(2bp 차), 반기 52.8 · 2.1 · 50.7, 연간 50.5 · 1.4 · 49.1, 케이스 1 안 B 월 점검 · 25bp 한도 +42bp)",
    cuts=[{"n": 2, "notice": "펭의 리밸런싱 규칙 초안(NPS 규모) · 목표: 7개 자산 고정 비중 · 점검 · 복원 주기 매일 · “자주 맞출수록 DR을 더 줍는다”", "bubble": ["자주 맞출수록", "더 많이 벌겠죠?"], "sfx": "매일 매일!"},
          {"n": 3, "bubble": ["매일 하면 비용 21.5bp가 먹어.", "월간~분기가 최적이고 둘은 2bp 차이야."], "sfx": "비용이 먹는다!"},
          {"n": 4, "bars": {f[0]: {"DR": f[1], "cost": f[2], "net": f[3]} for f in FREQ}, "latex": ["net = DR − cost", "daily: 60.5 − 21.5 = 39 bp", "monthly: 61.0 − 5.4 ≈ 56 bp, quarterly ≈ 54"],
           "summary": "더 자주가 아니라 집행 가능한 빈도", "bubble": ["줍는 동전보다 내는 통행료가", "커지면 안 되잖아."]},
          {"n": 5, "bubbles": [["국민연금은 실제로", "어떻게 하는 게 좋아요?"], ["월 점검 · 한 달 25bp 한도 · 선물로 먼저", "맞추는 안이 +42bp야. IC 보너스에서 보자."]], "sfx": "규칙의 값!"},
          {"n": 6, "text": ["다음 화", "평균회귀", "리밸런싱은 언제나 통할까?"]}],
    check={"daily_net": 39.0, "monthly_net": 55.6, "quarterly_net": 53.6},
    **{"fact-check": "표 숫자는 SS2 케이스의 20년 모의 패널(fml_w7ss2_panel_daily_sim, 교육용) 계산값. 월간 61.0 − 5.4는 55.6이지만 강의본 표기는 반올림 전 값으로 55.7 — 화면 수식은 '≈ 56'으로 적었다. +42bp는 케이스 1 기본 답(안 B)으로 학생 덱에 공개된 값. '통행료' 비유는 연출용."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "12", META)
