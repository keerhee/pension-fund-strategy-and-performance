"""시즌 3 EP.14 '가만히 있는 것도 전략' — 비례 비용이면 무거래 구간(Davis–Norman 1990). 합성시장 μ 7% · σ 18% · γ 3 · 편도 25bp:
매일 Merton 비중으로 리밸런싱 — 확실성등가 315.1bp · 비용 손실 14.7bp · 거래량 57% / 무거래 구간(반폭 ±3%p) — 328.7bp · 1.1bp · 3% (상한 329.8bp).
구간 안에선 가만히, 밖이면 경계까지만. (W07 M9 3교시 33장 그대로, SS2 리밸런싱 밴드의 이론적 근거)"""
from s3kit import *
import random

EQ = [f"eq/ep14_{i}.png" for i in (1, 2, 3)]
random.seed(7)
PATH, w, TRADES = [], 0.0, []
for k in range(60):
    w += random.gauss(0, 1.3)
    if abs(w) > 3: TRADES.append(k); w = 3.0 if w > 0 else -3.0
    PATH.append(w)


def cut1(t): return title(t, "EP.14 · 가만히 있는 것도 전략", 900)


def cut2(t):
    body = (label("목표 주식 비중에서", 0, -110, 38, "#555", 800) + punch("0.1%p", 0, -35, 80, fill=ORANGE, sw=10)
            + label("만 틀어져도 매일 즉시 복원", 0, 60, 40, NAVY, 900)
            + label("편도 거래비용 25bp", 0, 140, 36, RED, 900))
    return problem(t, "즉시 복원!", ORANGE, "#FCEBDD", "펭의 리밸런싱 규칙", body, ["목표에서 조금이라도 벗어나면", "바로 고쳐야 하잖아요?"], "칼같이!", bubble_size=46)


def cut3(t): return twist(t, ["비용이 있으면 구간 안에선 가만히,", "밖으로 나가면 경계까지만 맞춰."], "가만히도 전략!", size=44, sfx_size=130)


X0, X1, YC, KY = 130, 950, 590, 26


def cut4(t):
    s = explainer_frame(t, "무거래 구간", "합성시장 μ 7% · σ 18% · γ 3 · 편도 25bp · 10년 × 20,000경로")
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><rect x="{X0}" y="{YC-3*KY}" width="{X1-X0}" height="{6*KY}" fill="{TEAL}" opacity=".14"/>'
             f'<line x1="{X0}" y1="{YC}" x2="{X1}" y2="{YC}" stroke="{NAVY}" stroke-width="3" stroke-dasharray="12 8"/>'
             + "".join(f'<line x1="{X0}" y1="{YC + k*3*KY}" x2="{X1}" y2="{YC + k*3*KY}" stroke="{TEAL}" stroke-width="3"/>' for k in (-1, 1))
             + label("점선 = 목표 w*", X0, YC - 3 * KY - 20, 24, NAVY, 900, anchor="start") + label("+3%p", X1 - 4, YC - 3 * KY - 20, 24, TEAL, 900, anchor="end")
             + label("−3%p", X1 - 4, YC + 3 * KY + 22, 24, TEAL, 900, anchor="end") + "</g>")
    g = ease_out(prog(t, .8, 2.4)); n = max(2, int(60 * g))
    pts = [(X0 + (X1 - X0) * k / 59, YC - v * KY) for k, v in enumerate(PATH[:n])]
    s.append(f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>')
    for k in TRADES:
        if k < n:
            x, y = pts[k]; s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{RED}"/>')
    s.append(f'<g opacity="{ease_out(prog(t, 3.2, .4)):.2f}">' + label("● 거래는 경계에 닿을 때만", X0, 410, 28, RED, 900, anchor="start") + "</g>")
    s.append(chip("매일 복원: 비용 손실 14.7bp · 거래량 57%", 540, 790, GREY, back(prog(t, 3.6, .4)), w=760, size=32))
    s.append(chip("무거래 구간 ±3%p: 1.1bp · 3%", 540, 885, GREEN, back(prog(t, 4.0, .4)), w=640, size=34))
    s += eqs(t, EQ, (950, 1050, 1140), a0=4.8, scale=(.42, .46, .48))
    s += explainer_tail(t, "비용이 있으면 경계까지만 되돌린다", "Davis–Norman(1990) — RL이 먼저 재현해야 할 첫 번째 벽",
                        ["확실성등가 329.8 중", "328.7을 지켜 내는 셈이야."])
    return s


def cut5(t): return relief(t, ["주문이 아주 크면", "어떻게 해요?"], ["시장충격이 커지면 간격의 일부씩 옮기는", "Gârleanu–Pedersen 방식이 나아."],
                           "조금씩!", "체크: 편도 비용 · 밴드 반폭 · 경계 복원 · 거래량", a_size=42, sfx_size=120)


def cut6(t): return next_cut(t, "#6B3FA0", "강화학습", "기계가 스스로 배우게 하면?", topic_size=180)


META = dict(
    episode="EP.14", title="가만히 있는 것도 전략",
    concept="무거래 구간(no-trade region, Davis–Norman 1990) — 비례 거래비용이 있으면 목표 비중을 매일 쫓는 것보다, 목표 둘레의 구간 안에서는 가만히 있고 구간을 벗어날 때만 경계까지 되돌리는 것이 낫다. 구간 반폭은 비용의 세제곱근에 비례(점근). 리밸런싱 밴드의 이론적 근거이자 RL이 먼저 재현해야 할 기준선",
    source="W07 M9 3교시 33장(합성시장 μ 7% · σ 18% · γ 3 · 편도 25bp — 비용 없는 Merton 329.8bp / 매일 Merton 리밸런싱 315.1bp · 비용 손실 14.7bp · 거래량 57% / 무거래 구간(반폭 3%p) 328.7bp · 1.1bp · 3%, 구간 반폭 ∝ 비용 c의 세제곱근, 10년 × 20,000경로 · 시뮬레이션 최적 반폭 3~5%p vs 점근 4.3%p, 2교시 밴드 · SS2 밴드의 근거) · 34장(이차 비용이면 GP 부분 이동)",
    cuts=[{"n": 2, "notice": "펭의 리밸런싱 규칙 · 목표 주식 비중에서 0.1%p만 틀어져도 매일 즉시 복원 · 편도 거래비용 25bp", "bubble": ["목표에서 조금이라도 벗어나면", "바로 고쳐야 하잖아요?"], "sfx": "칼같이!"},
          {"n": 3, "bubble": ["비용이 있으면 구간 안에선 가만히,", "밖으로 나가면 경계까지만 맞춰."], "sfx": "가만히도 전략!"},
          {"n": 4, "band": "목표 w* ± 3%p · 경로는 개념도(무작위 seed 7)", "chips": ["매일 복원: 비용 손실 14.7bp · 거래량 57%", "무거래 구간 ±3%p: 1.1bp · 3%"], "latex": ["half width ∝ c^(1/3) (c = 25bp, ±3%p)", "cost loss: 14.7 → 1.1 bp/yr", "turnover: 57% → 3%"],
           "summary": "비용이 있으면 경계까지만 되돌린다", "bubble": ["확실성등가 329.8 중", "328.7을 지켜 내는 셈이야."]},
          {"n": 5, "bubbles": [["주문이 아주 크면", "어떻게 해요?"], ["시장충격이 커지면 간격의 일부씩 옮기는", "Gârleanu–Pedersen 방식이 나아."]], "sfx": "조금씩!"},
          {"n": 6, "text": ["다음 화", "강화학습", "기계가 스스로 배우게 하면?"]}],
    check={"CE_upper": 329.8, "CE_daily": 315.1, "CE_band": 328.7},
    **{"fact-check": "숫자는 강의본 33장의 합성시장 시뮬레이션(가상 실험). 해설 컷의 비중 경로는 무작위 개념도이며 시뮬레이션 결과가 아니다. 반폭 ±3%p는 강의본이 비교에 쓴 값(시뮬레이션 최적 3~5%p, 점근 4.3%p). '세제곱근 비례'는 점근 근사. GP 언급은 보충교재 16 · 강의본 34장."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "14", META)
