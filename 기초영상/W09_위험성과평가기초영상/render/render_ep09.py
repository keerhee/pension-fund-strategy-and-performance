"""시즌 4 EP.09 '한 펀드, 네 성적표' — 연 9% · σ 12% · TE 4% · MDD 22% 펀드(무위험 3%): Sharpe 0.50(양호의 하한) · Sortino 0.75(꽤 양호)
· IR 0.25(경계선) · Calmar 0.41(평범). '좋은 펀드인가'는 답이 없고 '어떤 목적에 좋은가'만 답이 있다. Treynor · Jensen α는 체계 위험 β만 본다.
(W09 강의본 20·21·22장 그대로)"""
from s4kit import *

EQ = [f"eq/ep09_{i}.png" for i in (1, 2, 3)]
CARDS = [("Sharpe", "0.50", "양호의 하한", TEAL, "표준 비교"), ("Sortino", "0.75", "꽤 양호", GREEN, "은퇴 · 보수적"),
         ("IR", "0.25", "경계선", ORANGE, "액티브 위임"), ("Calmar", "0.41", "평범", RED, "헤지펀드 · CTA")]


def cut1(t): return title(t, "EP.09 · 한 펀드, 네 성적표", 860)


def cut2(t):
    body = (label("연 9% · σ 12% · TE 4% · MDD 22%", 0, -100, 38, NAVY, 900)
            + f'<rect x="-330" y="-40" width="660" height="120" rx="18" fill="#E6ECF7"/>'
            + label("펭: “지표 하나만 골라서", 0, -5, 36, BLUE, 900) + label("보고서 맨 위에 쓰면 되죠?”", 0, 45, 36, BLUE, 900)
            + label("(예제 펀드 · 무위험 3%)", 0, 150, 30, GREY, 800))
    return problem(t, "점수 하나만!", BLUE, "#E6ECF7", "펭의 평가 보고서 초안", body, ["가장 좋은 지표 하나로", "평가하면 되죠?"], "하나면 충분!")


def cut3(t): return twist(t, ["같은 펀드가 지표마다 ‘양호’에서", "‘경계선’까지 오가. 목적이 자를 골라."], "자가 결론을!", size=44, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "같은 펀드, 다른 결론", "연 9% · σ 12% · TE 4% · MDD 22% · 무위험 3%", head_size=94)
    for i, (nm, v, j, c, use) in enumerate(CARDS):
        g = back(prog(t, .6 + .5 * i, .4))
        if g <= 0: continue
        x = 300 + 480 * (i % 2); y = 485 + 205 * (i // 2)
        s.append(f'<g transform="translate({x},{y}) scale({g:.3f})"><rect x="-210" y="-92" width="420" height="184" rx="22" fill="{c}"/>'
                 + label(nm, 0, -58, 34, "#fff", 900) + label(v, 0, 2, 64, "#fff", 900) + label(f"{j} · {use}", 0, 66, 24, "#fff", 800) + "</g>")
    s += eqs(t, EQ, (830, 935, 1050), a0=3.4, scale=(.42, .44, .4))
    s += explainer_tail(t, "‘좋은 펀드인가’가 아니라 ‘어떤 목적에 좋은가’", "Treynor · Jensen α는 β만 본다 — α는 어떤 모형 대비인지 늘 물어라",
                        ["은퇴 계좌라면 Sortino,", "위탁 평가라면 IR을 먼저 봐."], red_size=40)
    return s


def cut5(t): return relief(t, ["그럼 보고서엔", "뭘 써요?"], ["목적과 함께 여러 지표를 나란히.", "하나만 고르면 원하는 결론이 나와."],
                           "체리피킹 금지!", "체크: 평가 목적 · 지표의 분모 · 기준값 · 평가 기간", a_size=46, sfx_size=100)


def cut6(t): return next_cut(t, "#6B3FA0", "IR = IC√BR", "실력은 어디서 나오나?", topic_size=170)


META = dict(
    episode="EP.09", title="한 펀드, 네 성적표",
    concept="6대 성과 지표는 분모가 다르다 — 같은 펀드(연 9% · σ 12% · TE 4% · MDD 22%)가 Sharpe 0.50(양호의 하한) · Sortino 0.75(꽤 양호) · IR 0.25(경계선) · Calmar 0.41(평범)로 평가가 갈린다. '좋은 펀드인가'는 답이 없고 '어떤 목적에 좋은가'만 답이 있다. Treynor · Jensen α는 체계 위험(β)만 보며 모형 의존적",
    source="W09 강의본 20장(Treynor와 Jensen α — 분모 β, CAPM 초과, α는 모형 의존적) · 21장(6대 지표 — 분자 · 분모 · 용도) · 22장(같은 포트폴리오, 다른 결론 — Sharpe (9 − 3)/12 = 0.50 양호의 하한 · Sortino (9 − 3)/8 = 0.75 꽤 양호 · IR 1/4 = 0.25 경계선 · Calmar 9/22 = 0.41 평범)",
    cuts=[{"n": 2, "notice": "펭의 평가 보고서 초안 · 연 9% · σ 12% · TE 4% · MDD 22% · 펭: “지표 하나만 골라서 보고서 맨 위에 쓰면 되죠?” · (예제 펀드 · 무위험 3%)", "bubble": ["가장 좋은 지표 하나로", "평가하면 되죠?"], "sfx": "하나면 충분!"},
          {"n": 3, "bubble": ["같은 펀드가 지표마다 ‘양호’에서", "‘경계선’까지 오가. 목적이 자를 골라."], "sfx": "자가 결론을!"},
          {"n": 4, "cards": {c[0]: f"{c[1]} · {c[2]} · {c[4]}" for c in CARDS}, "latex": ["Sharpe = (9 − 3)/12 = 0.50, Sortino = (9 − 3)/8 = 0.75", "IR = 1/4 = 0.25, Calmar = 9/22 ≈ 0.41", "Treynor = (Rp − Rf)/β, α_J = Rp − [Rf + β(Rm − Rf)]"],
           "summary": "‘좋은 펀드인가’가 아니라 ‘어떤 목적에 좋은가’", "bubble": ["은퇴 계좌라면 Sortino,", "위탁 평가라면 IR을 먼저 봐."]},
          {"n": 5, "bubbles": [["그럼 보고서엔", "뭘 써요?"], ["목적과 함께 여러 지표를 나란히.", "하나만 고르면 원하는 결론이 나와."]], "sfx": "체리피킹 금지!"},
          {"n": 6, "text": ["다음 화", "IR = IC√BR", "실력은 어디서 나오나?"]}],
    check={"sharpe": 0.5, "sortino": 0.75, "IR": 0.25, "calmar": 0.409},
    **{"fact-check": "네 값과 판정어(양호의 하한 · 꽤 양호 · 경계선 · 평범)는 강의본 22장 그대로. 용도 표기(표준 비교 · 은퇴 · 보수적 · 액티브 · 헤지펀드 · CTA)는 21장 표. Treynor · Jensen은 수식만 보이고 예제 값은 넣지 않았다(강의본에도 없음)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "09", META)
