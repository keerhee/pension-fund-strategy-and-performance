"""시즌 4 EP.02 '최악 5개월의 평균' — 월 수익률 100개를 나쁜 순으로 줄 세우면 95% 꼬리는 최악 5개월.
최악 손실 12 · 9 · 8 · 7 · 6 · (5) → 역사적 VaR(95%) = 6% · CVaR = (12 + 9 + 8 + 7 + 6) ÷ 5 = 8.4%. 정규(μ 0.5% · σ 4%)면 VaR 6.1 · CVaR 7.8(7.75) — 꼬리가 정규보다 두껍다.
(W09 강의본 10·14장 그대로)"""
from s4kit import *

EQ = [f"eq/ep02_{i}.png" for i in (1, 2, 3)]
LOSS = [12, 9, 8, 7, 6, 5, 4, 4, 3]


def cut1(t): return title(t, "EP.02 · 최악 5개월의 평균", 840)


def cut2(t):
    body = (label("월 수익률 100개월 · 95% VaR", 0, -105, 36, "#555", 800)
            + punch("VaR 6%", 0, -20, 84, fill=BLUE, sw=10)
            + label("펭: “최악이어도 6%까지만 잃는다”", 0, 115, 38, NAVY, 900))
    return problem(t, "최대 6%?", BLUE, "#E6ECF7", "펭의 위험 보고서", body, ["VaR가 6%면", "최악이 6%라는 거죠?"], "6%면 끝!")


def cut3(t): return twist(t, ["VaR는 경계선일 뿐이야.", "넘친 날엔 평균 8.4%를 잃어."], "경계 너머!", size=46, sfx_size=150)


BASE, K = 760, 26


def cut4(t):
    s = explainer_frame(t, "100개월을 줄 세우기", "최악부터 — 95% 기준이면 최악 5개월이 꼬리 (월 손실 %)")
    s.append(f'<line x1="90" y1="{BASE}" x2="990" y2="{BASE}" stroke="{NAVY}" stroke-width="4" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, v in enumerate(LOSS):
        x = 140 + 100 * i
        g = ease_out(prog(t, .6 + .2 * i, .4))
        if g <= 0: continue
        c = RED if i < 5 else GREY
        h = v * K * g
        s.append(f'<rect x="{x-38}" y="{BASE-h:.0f}" width="76" height="{h:.0f}" fill="{c}" rx="5"/>')
        if g > .9: s.append(label(str(v), x, BASE - v * K - 24, 30, c, 900) + label(f"{i+1}위", x, BASE + 30, 24, NAVY, 800))
    if t > 2.6:
        a = ease_out(prog(t, 2.6, .4)); vx = 140 + 100 * 4 + 50
        s.append(f'<g opacity="{a:.2f}"><line x1="{vx}" y1="{BASE-6*K-60}" x2="{vx}" y2="{BASE}" stroke="{BLUE}" stroke-width="5" stroke-dasharray="12 8"/>'
                 + label("VaR = 6", vx + 70, BASE - 6 * K - 50, 30, BLUE, 900)
                 + f'<path d="M 102 {BASE-12*K-40} h 436" stroke="{RED}" stroke-width="5" fill="none"/>' + label("꼬리 5개월 평균 = CVaR 8.4", 320, BASE - 12 * K - 66, 30, RED, 900) + "</g>")
    s.append(chip("정규분포로 재면 CVaR 7.8 < 실제 8.4 → 꼬리가 더 두껍다", 540, 860, NAVY, back(prog(t, 3.4, .4)), w=900, size=30))
    s += eqs(t, EQ, (925, 1030, 1140), a0=4.2, scale=(.46, .46, .42))
    s += explainer_tail(t, "VaR는 경계, CVaR는 그 너머의 평균", "Basel(FRTB)도 99% VaR 대신 97.5% ES(=CVaR)를 쓴다",
                        ["20번 중 19번은 6%보다 덜 잃지만,", "나머지 1번은 평균 8.4%야."], owl_size=40)
    return s


def cut5(t): return relief(t, ["CVaR면 이제", "안전한 거죠?"], ["같은 평온기 데이터면 같이 틀려.", "그래서 스트레스 테스트를 따로 해."],
                           "모델 밖도 봐!", "체크: 신뢰수준 · 추정법(정규 · 역사적 · MC) · 스트레스 시나리오", a_size=44, chip_size=32, sfx_size=110)


def cut6(t): return next_cut(t, "#6B3FA0", "부분가법성", "합치면 위험이 줄어들까?", topic_size=170)


META = dict(
    episode="EP.02", title="최악 5개월의 평균",
    concept="VaR와 CVaR의 손계산 — 월 수익률 100개를 나쁜 순으로 줄 세우면 95% 꼬리는 최악 5개월. VaR는 그 경계(6%), CVaR는 꼬리의 평균 손실(8.4%). 같은 데이터를 정규분포로 재면 CVaR가 7.8%로 작게 나와 꼬리가 정규보다 두꺼움을 알려 준다",
    source="W09 강의본 10장(VaR는 분위점, CVaR는 그 너머 꼬리의 평균 — CVaR > VaR) · 14장(100개월 예 — 최악 손실 12 · 9 · 8 · 7 · 6 · 5, VaR(95%) 6%, CVaR (12 + 9 + 8 + 7 + 6)/5 = 8.4%, 정규 μ 0.5% · σ 4% → VaR 1.645 × 4 − 0.5 = 6.1% · CVaR 2.063 × 4 − 0.5 = 7.8%, CVaR도 같은 데이터면 같이 틀린다 → 스트레스 테스트, Basel FRTB 97.5% ES)",
    cuts=[{"n": 2, "notice": "펭의 위험 보고서 · 월 수익률 100개월 · 95% VaR 6% · 펭: “최악이어도 6%까지만 잃는다”", "bubble": ["VaR가 6%면", "최악이 6%라는 거죠?"], "sfx": "6%면 끝!"},
          {"n": 3, "bubble": ["VaR는 경계선일 뿐이야.", "넘친 날엔 평균 8.4%를 잃어."], "sfx": "경계 너머!"},
          {"n": 4, "bars": {"최악 1~9위 손실(%)": LOSS}, "latex": ["VaR95 = 6% (5th worst of 100)", "CVaR95 = (12 + 9 + 8 + 7 + 6)/5 = 8.4%", "normal: 1.645 × 4 − 0.5 = 6.1, 2.063 × 4 − 0.5 ≈ 7.8"],
           "summary": "VaR는 경계, CVaR는 그 너머의 평균", "bubble": ["20번 중 19번은 6%보다 덜 잃지만,", "나머지 1번은 평균 8.4%야."]},
          {"n": 5, "bubbles": [["CVaR면 이제", "안전한 거죠?"], ["같은 평온기 데이터면 같이 틀려.", "그래서 스트레스 테스트를 따로 해."]], "sfx": "모델 밖도 봐!"},
          {"n": 6, "text": ["다음 화", "부분가법성", "합치면 위험이 줄어들까?"]}],
    check={"VaR": 6, "CVaR": 8.4, "normal_VaR": 6.08, "normal_CVaR": 7.75},
    **{"fact-check": "6위 이하 손실(5 · 4 · 4 · 3)은 강의본 표의 5 이후를 채운 개념도용 값이며 VaR · CVaR 계산에는 쓰지 않는다. 정규 CVaR 7.75를 강의본은 7.8로 반올림. 역사적 VaR를 '5번째로 나쁜 값'으로 정의한 것은 강의본 14장 방식(경계 정의에 따라 5번째 · 6번째 · 보간이 달라질 수 있다)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "02", META)
