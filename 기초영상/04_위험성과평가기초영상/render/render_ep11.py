"""시즌 4 EP.11 '점수 +2가 알파 3%' — Grinold의 예측 규칙 α = σ × IC × z. 표준화 점수 z(평균 0 · 분산 1)를 기대 초과수익으로 바꾼다.
IC 0.05: 종목 A σ 30% · z +2.0 → +3.0% · B σ 20% · z +1.0 → +1.0% · C σ 25% · z −1.5 → −1.9%. IC가 작으면 점수 +2도 3%로 '수축' — 과신을 막는다.
기본 예측 공식(최소제곱 직선)에서 유도: 기울기 = Cov/Var. (W09 강의본 24·25장 그대로)"""
from s4kit import *

EQ = [f"eq/ep11_{i}.png" for i in (1, 2, 3)]
STK = [("A", 30, 2.0, 3.0), ("B", 20, 1.0, 1.0), ("C", 25, -1.5, -1.875)]


def cut1(t): return title(t, "EP.11 · 점수 +2가 알파 3%", 840)


def cut2(t):
    body = (label("종목 A · 모델 점수 z", 0, -110, 36, "#555", 800) + punch("+2.0", 0, -30, 84, fill=GREEN, sw=10)
            + label("펭: “상위 2σ니까 30% 오른다!”", 0, 100, 40, NAVY, 900)
            + label("종목 A 변동성 σ 30%", 0, 160, 30, GREY, 800))
    return problem(t, "점수 대박!", GREEN, "#E9F1E4", "펭의 퀀트 신호 메모", body, ["점수가 +2면", "엄청 오르는 거죠?"], "+30%?!")


def cut3(t): return twist(t, ["IC가 0.05면 점수 +2도", "알파 3%로 줄여서 써야 해."], "확신을 줄여!", size=46, sfx_size=150)


ZERO, K = 670, 40


def cut4(t):
    s = explainer_frame(t, "α = σ × IC × z", "IC 0.05 — 표준화 점수를 기대 초과수익으로 바꾸는 규칙")
    s.append(f'<line x1="100" y1="{ZERO}" x2="980" y2="{ZERO}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (nm, sg, z, a) in enumerate(STK):
        x = 250 + 290 * i
        g = ease_out(prog(t, .8 + .7 * i, .5))
        if g <= 0: continue
        c = GREEN if a > 0 else RED; h = abs(a) * K * g; y = ZERO - h if a > 0 else ZERO
        s.append(f'<rect x="{x-80}" y="{y:.0f}" width="160" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"{a:+.1f}%", x, ZERO - a * K + (-28 if a > 0 else 32), 38, c, 900))
            s.append(label(f"종목 {nm}", x, 420, 32, NAVY, 900) + label(f"σ {sg}% · z {z:+.1f}", x, 458, 26, GREY, 800))
    s.append(chip("점수 +2 → 알파 +30%가 아니라 +3% — 과신을 막는 수축", 540, 875, NAVY, back(prog(t, 3.2, .4)), w=900, size=30))
    s += eqs(t, EQ, (945, 1045, 1145), a0=4.0, scale=(.5, .48, .4))
    s += explainer_tail(t, "IC가 작으면 확신도 작게", "기본 예측 공식 = 오차를 가장 작게 만드는 직선 — 기울기는 공분산 ÷ 분산",
                        ["맞힐 확률이 낮은 만큼", "기대도 줄여 거는 거야."])
    return s


def cut5(t): return relief(t, ["그럼 이 알파를", "그대로 사면 돼요?"], ["비중 제약이 있으면 다 못 옮겨.", "그래서 IR = TC · IC · √BR이 돼."],
                           "제약도 계산!", "체크: 점수 표준화 · IC · 종목 변동성 · 전이계수 TC", a_size=46, sfx_size=120)


def cut6(t): return next_cut(t, RED, "실력 vs 운", "3년 성적이면 알 수 있나?", topic_size=180)


META = dict(
    episode="EP.11", title="점수 +2가 알파 3%",
    concept="Grinold의 예측 규칙 α = σ × IC × z — 표준화된 신호(평균 0 · 분산 1)를 기대 초과수익으로 바꾸는 규칙. IC가 작으면 강한 점수도 작은 알파로 '수축'되어 과신을 막는다. 기본 예측 공식(오차 제곱을 최소화하는 직선, 기울기 = 공분산 ÷ 분산)에서 유도되며, 알파를 비중으로 옮기면 IR = TC · IC · √BR",
    source="W09 강의본 24장(두 번째 공식 — 알파 = 변동성 × IC × 점수, 네 가정, 예 IC 0.05: A σ 30% · z +2.0 → +3.0% · B 20% · +1.0 → +1.0% · C 25% · −1.5 → −1.9%, IC가 0.05로 작으면 점수 +2도 알파 3%로 수축, IR = TC · IC · √BR(보충교재 15)) · 25장(증명 — 기본 예측 공식은 오차를 가장 작게 만드는 직선, 기울기 = 공분산 ÷ 분산)",
    cuts=[{"n": 2, "notice": "펭의 퀀트 신호 메모 · 종목 A 모델 점수 z +2.0 · 펭: “상위 2σ니까 30% 오른다!” · 종목 A 변동성 σ 30%", "bubble": ["점수가 +2면", "엄청 오르는 거죠?"], "sfx": "+30%?!"},
          {"n": 3, "bubble": ["IC가 0.05면 점수 +2도", "알파 3%로 줄여서 써야 해."], "sfx": "확신을 줄여!"},
          {"n": 4, "bars": {f"종목 {s_[0]} (σ {s_[1]}% · z {s_[2]:+.1f})": f"{s_[3]:+.2f}%" for s_ in STK}, "latex": ["α = σ × IC × z", "A: 30% × 0.05 × 2.0 = 3.0%", "B: 20 × 0.05 × 1.0 = 1.0, C: 25 × 0.05 × (−1.5) ≈ −1.9"],
           "summary": "IC가 작으면 확신도 작게", "bubble": ["맞힐 확률이 낮은 만큼", "기대도 줄여 거는 거야."]},
          {"n": 5, "bubbles": [["그럼 이 알파를", "그대로 사면 돼요?"], ["비중 제약이 있으면 다 못 옮겨.", "그래서 IR = TC · IC · √BR이 돼."]], "sfx": "제약도 계산!"},
          {"n": 6, "text": ["다음 화", "실력 vs 운", "3년 성적이면 알 수 있나?"]}],
    check={"A": 3.0, "B": 1.0, "C": -1.875},
    **{"fact-check": "종목 A · B · C와 IC 0.05는 강의본 24장 예제. C는 −1.875%를 강의본처럼 −1.9%로 반올림. 펭의 '+30%'는 σ × z(IC = 1을 가정한 것과 같은 과신)를 연출한 것. TC(전이계수)는 보충교재 15 · 케이스 1 8장."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "11", META)
