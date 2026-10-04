"""시즌 4 EP.07 '오르는 흔들림은 억울해' — Sortino = 초과수익 ÷ 하방 변동성 σdown. 강의본 22장 펀드(연 9% · σ 12% · σdown 8%):
Sharpe (9 − 3)/12 = 0.50 → Sortino (9 − 3)/8 = 0.75. 목표 이하 수익만 위험 — 은퇴 · 보수적 투자자에 맞다. (W09 강의본 18·21·22장 그대로)"""
from s4kit import *
import math

EQ = [f"eq/ep07_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.07 · 오르는 흔들림은 억울해", 900)


def cut2(t):
    body = (label("가 펀드 (EP.06)", 0, -110, 36, "#555", 800)
            + label("Sharpe", -190, -40, 36, "#555", 800) + punch("0.50", -190, 35, 76, fill=TEAL, sw=9)
            + label("올해 큰 흔들림", 190, -40, 34, "#555", 800) + punch("↑ 위로", 190, 35, 66, fill=GREEN, sw=8)
            + label("“많이 올라서 출렁였는데 벌점이라니”", 0, 150, 36, NAVY, 900))
    return problem(t, "억울해요!", TEAL, "#DDF0EE", "펭의 항의 메모", body, ["많이 오른 것도", "위험으로 치나요?"], "억울!")


def cut3(t): return twist(t, ["내려가는 흔들림만 위험으로 세면 돼.", "그게 Sortino야."], "아래만 센다!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "Sharpe vs Sortino", "분모만 바꾼다 — 총 변동성 σ 12% → 하방 변동성 σdown 8%", head_size=90)
    X0, X1, YM = 120, 960, 600
    rets = [math.sin(k * 1.7) * 60 + math.sin(k * .6) * 40 for k in range(24)]
    for k, r in enumerate(rets):
        g = ease_out(prog(t, .5 + .05 * k, .3))
        if g <= 0: continue
        x = X0 + (X1 - X0) * k / 23; c = RED if r < 0 else GREEN
        h = abs(r) * 1.6 * g; y = YM - h if r > 0 else YM
        op = 1 if (r < 0 or t < 2.8) else .25
        s.append(f'<rect x="{x-14:.0f}" y="{y:.0f}" width="28" height="{h:.0f}" fill="{c}" opacity="{op}"/>')
    s.append(f'<line x1="{X0-20}" y1="{YM}" x2="{X1+20}" y2="{YM}" stroke="{NAVY}" stroke-width="4" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(f'<g opacity="{ease_out(prog(t, 2.8, .4)):.2f}">' + label("위로 흔들림은 빼고 — 아래만 센다", 540, 430, 30, RED, 900) + "</g>")
    s.append(chip("Sharpe 0.50", 300, 820, TEAL, back(prog(t, 3.2, .4)), w=300, size=34))
    s.append(chip("Sortino 0.75", 780, 820, GREEN, back(prog(t, 3.6, .4)), w=300, size=34))
    s += eqs(t, EQ, (880, 1000, 1100), a0=4.4, scale=(.5, .48, .44))
    s += explainer_tail(t, "같은 펀드가 0.50에서 0.75로", "목표 이하 수익만 위험 — 은퇴 · 보수적 투자자의 잣대",
                        ["잃는 게 무서운 사람에겐", "아래쪽 흔들림만 위험이야."])
    return s


def cut5(t): return relief(t, ["그럼 Sortino가", "늘 더 좋은 거예요?"], ["목적이 정해. 상승도 불확실성으로", "볼지, 하락만 위험으로 볼지."],
                           "목적이 자를!", "체크: 목표 수익(최소 허용) · 하방 변동성 · 평가 기간", a_size=44, sfx_size=110)


def cut6(t): return next_cut(t, ORANGE, "+8%의 성적", "+8%면 잘한 건가요?", topic_size=170)


META = dict(
    episode="EP.07", title="오르는 흔들림은 억울해",
    concept="Sortino 비율 — 분모를 하방 변동성(목표 이하 수익만의 흔들림)으로 바꾼 Sharpe. 오르는 쪽 흔들림에 벌점을 주지 않는다. 같은 펀드가 Sharpe 0.50에서 Sortino 0.75로 — 은퇴 · 보수적 투자자처럼 손실이 무서운 사람의 잣대",
    source="W09 강의본 18장(Sharpe와 Sortino — 분모를 하방 변동성 σdown으로, 목표 이하 수익률만 위험 — 은퇴 · 보수적, “상승의 변동성까지 벌점을 주는 게 맞는가”) · 21장(6대 지표 — Sortino 용도 은퇴 · 보수적) · 22장(연 9% · σ 12% 펀드 — Sharpe 0.50, Sortino (9 − 3)/8 = 0.75)",
    cuts=[{"n": 2, "notice": "펭의 항의 메모 · 가 펀드(EP.06) Sharpe 0.50 · 올해 큰 흔들림 ↑ 위로 · “많이 올라서 출렁였는데 벌점이라니”", "bubble": ["많이 오른 것도", "위험으로 치나요?"], "sfx": "억울!"},
          {"n": 3, "bubble": ["내려가는 흔들림만 위험으로 세면 돼.", "그게 Sortino야."], "sfx": "아래만 센다!"},
          {"n": 4, "bars": "월 수익률 개념도 — 위(초록)는 흐리게, 아래(빨강)만 센다", "chips": ["Sharpe 0.50", "Sortino 0.75"], "latex": ["Sortino = (E[Rp] − Rf)/σ_down", "(9 − 3)/12 = 0.50 → (9 − 3)/8 = 0.75", "σ_down: only returns below target"],
           "summary": "같은 펀드가 0.50에서 0.75로", "bubble": ["잃는 게 무서운 사람에겐", "아래쪽 흔들림만 위험이야."]},
          {"n": 5, "bubbles": [["그럼 Sortino가", "늘 더 좋은 거예요?"], ["목적이 정해. 상승도 불확실성으로", "볼지, 하락만 위험으로 볼지."]], "sfx": "목적이 자를!"},
          {"n": 6, "text": ["다음 화", "+8%의 성적", "+8%면 잘한 건가요?"]}],
    check={"sharpe": 0.5, "sortino": 0.75},
    **{"fact-check": "σdown 8%는 강의본 22장 예제 값. 막대는 월 수익률 개념도(사인 합성)이며 실제 데이터가 아니다. 하방 변동성의 목표 수익(0% · 무위험 · 최소 허용 수익)은 정의에 따라 다르다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "07", META)
