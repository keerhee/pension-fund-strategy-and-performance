"""시즌 3 EP.03 '1969년, MIT의 두 천재' — Samuelson의 역설과 Merton의 해. CRRA 투자자의 최적 주식 비중
w* = (μ − r)/(γσ²) = (7 − 3)/(4 × 16²) ≈ 39% — 기간 T가 식에 없다. (W07 M9 1교시 12·13·17장 · 에피소드 1(49장))"""
from s3kit import *

EQ = [f"eq/ep03_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.03 · 1969년, MIT의 두 천재", 940)


def cut2(t):
    body = (label("25세", -200, -100, 40, "#555", 800) + punch("주식 100%", -200, -20, 60, fill=GREEN, sw=8)
            + label("64세", 220, -100, 40, "#555", 800) + punch("주식 0%", 220, -20, 60, fill=BLUE, sw=8)
            + label("“기간이 길수록 주식을 더”", 0, 120, 44, NAVY, 900))
    return problem(t, "젊음 = 주식?", GREEN, "#E9F1E4", "펭의 평생 투자 계획", body, ["오래 들고 있을 거니까", "젊을 땐 주식이 정답이죠?"], "청춘은 주식!")


def cut3(t): return twist(t, ["Merton 공식엔 기간 T가 없어.", "같은 사람이면 25세도 64세도 39%야."], "T가 없다!", size=44, sfx_size=150)


BASE, K = 790, 8


def cut4(t):
    s = explainer_frame(t, "Merton의 해", "μ 7% · r 3% · γ 4 · σ 16% (강의본 예시) · CRRA 효용")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (x, lbl) in enumerate(((250, "1년"), (540, "10년"), (830, "30년"))):
        g = ease_out(prog(t, .7 + .6 * i, .5))
        if g <= 0: continue
        h = 39 * K * g
        s.append(f'<rect x="{x-80}" y="{BASE-h:.0f}" width="160" height="{h:.0f}" fill="{TEAL}" rx="6"/>')
        if g > .9:
            s.append(label("39%", x, BASE - 39 * K - 30, 44, TEAL, 900) + label(f"투자 기간 {lbl}", x, BASE + 38, 30, NAVY, 900))
    a = ease_out(prog(t, 2.8, .4))
    s.append(f'<line x1="140" y1="{BASE-39*K}" x2="950" y2="{BASE-39*K}" stroke="{RED}" stroke-width="4" stroke-dasharray="12 8" opacity="{a:.2f}"/>')
    s.append(chip("기간이 달라도 같은 높이 — Samuelson의 역설", 540, 900, RED, back(prog(t, 3.4, .4)), w=820, size=32))
    s += eqs(t, EQ, (965, 1080, 1190), a0=4.4, scale=(.5, .48, .48))
    s += explainer_tail(t, "1969년, 같은 호에 실린 두 논문", "Samuelson은 이산 시간으로, Merton은 연속 시간으로",
                        ["스승과 제자가 같은 해에", "같은 답에 도착했지."])
    return s


def cut5(t): return relief(t, ["그런데 금리가 바뀌어도", "계속 39%예요?"], ["그땐 미래 기회까지 헤지해야 해.", "Merton이 1973년에 답을 냈지."],
                           "기회가 변하면?", "체크: μ − r · γ · σ² · (기간 T는 없다)")


def cut6(t): return next_cut(t, "#6B3FA0", "헤징 수요", "내일의 기회를 오늘 살 수 있나?", topic_size=170)


META = dict(
    episode="EP.03", title="1969년, MIT의 두 천재",
    concept="Samuelson의 역설과 Merton의 해 — CRRA 효용 + 동적 프로그래밍의 최적 위험자산 비중 w* = (μ − r)/(γσ²)는 현재 상태에만 의존하고 투자 기간 T와 무관하다. '젊을수록 주식을 많이'는 기간만으로는 정당화되지 않는다 — 이 퍼즐이 동적 배분 이론의 출발점",
    source="W07 M9 1교시 12·13·17장(Samuelson의 역설 1969 — 로그 효용 하에서 최적 주식 비중은 기간과 무관, Merton 1969·1971 연속시간 해 — 시간 독립, 예: μ 7% · r 3% · γ 4 · σ 16%면 주식 약 39%, 1969년 같은 호에 실린 두 논문) · 에피소드 1(49장)",
    cuts=[{"n": 2, "notice": "펭의 평생 투자 계획 · 25세 주식 100% → 64세 주식 0% · “기간이 길수록 주식을 더”", "bubble": ["오래 들고 있을 거니까", "젊을 땐 주식이 정답이죠?"], "sfx": "청춘은 주식!"},
          {"n": 3, "bubble": ["Merton 공식엔 기간 T가 없어.", "같은 사람이면 25세도 64세도 39%야."], "sfx": "T가 없다!"},
          {"n": 4, "bars": {"1년": 0.39, "10년": 0.39, "30년": 0.39}, "latex": ["w* = (μ − r)/(γσ²)", "= (0.07 − 0.03)/(4 × 0.16²) = 0.04/0.1024 ≈ 39%", "w*(1 yr) = w*(30 yr) = 39%"],
           "summary": "1969년, 같은 호에 실린 두 논문", "bubble": ["스승과 제자가 같은 해에", "같은 답에 도착했지."]},
          {"n": 5, "bubbles": [["그런데 금리가 바뀌어도", "계속 39%예요?"], ["그땐 미래 기회까지 헤지해야 해.", "Merton이 1973년에 답을 냈지."]], "sfx": "기회가 변하면?"},
          {"n": 6, "text": ["다음 화", "헤징 수요", "내일의 기회를 오늘 살 수 있나?"]}],
    check={"w_star": 0.3906},
    **{"fact-check": "투자 기회(μ, r, σ)가 일정하고 인적자본이 없을 때의 결과. Samuelson(1969)은 로그 효용 기준의 역설, Merton(1969)은 CRRA 일반 해 — 두 논문이 같은 호(REStat 1969)에 실렸다는 것은 강의본 28장 표현을 따랐다(학술지명은 화면에 넣지 않음). '스승과 제자'는 강의본 94장 에피소드 제목. 펭의 계획(100% → 0%)은 연출용."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "03", META)
