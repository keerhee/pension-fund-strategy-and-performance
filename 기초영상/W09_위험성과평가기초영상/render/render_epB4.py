"""시즌 4 EP.B4 '하나의 자로 모두를?' — W09 케이스 2 페르소나 매트릭스. 대상이 자를 정한다: 운용자는 TWR(현금흐름 시점 무관 — 운용 실력), 투자자는 MWR(IRR — 실제 경험).
청년(적립기) TWR · Sharpe · 누적수익 / 중년(전환기) Sharpe · Sortino · IR / 은퇴 근접(인출기) MDD · Sortino · Calmar · MWR / 대체투자 KS-PME.
은퇴가 가까울수록 σ가 아니라 MDD. (케이스 2 덱 3·6·11·14장 — 시즌 4 마지막)"""
from s4kit import *

EQ = [f"eq/epB4_{i}.png" for i in (1, 2, 3)]
PER = [("청년 · 적립기", "장기 성장 · 변동성 감내", "TWR · Sharpe · 누적수익", GREEN), ("중년 · 전환기", "성장과 방어의 균형", "Sharpe · Sortino · IR", TEAL),
       ("은퇴 근접 · 인출기", "낙폭 · 인출 지속성", "MDD · Sortino · Calmar · MWR", RED), ("대체투자", "시장 대비 · 현금흐름", "KS-PME · IRR(MWR)", "#6B3FA0")]


def cut1(t): return title(t, "EP.B4 · 하나의 자로 모두를?", 860)


def cut2(t):
    body = (label("국민성장펀드 측정 체계 초안 (교육용 가상)", 0, -110, 32, "#555", 800)
            + label("모든 상품 · 모든 가입자", 0, -40, 40, NAVY, 900)
            + punch("Sharpe 하나로", 0, 40, 70, fill=TEAL, sw=9)
            + label("펭: “하나로 통일하면 비교가 쉽잖아요”", 0, 150, 34, BLUE, 900))
    return problem(t, "Sharpe로 통일!", TEAL, "#DDF0EE", "IC 제2호 · 측정체계위원회", body, ["지표가 하나면", "비교하기 편하죠?"], "통일!")


def cut3(t): return twist(t, ["청년과 은퇴자는 위험의 뜻부터 달라.", "대상과 목적이 자를 정하는 거야."], "자는 여러 개!", size=44, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "페르소나 × 측정 도구", "운용자는 TWR · 투자자는 MWR — 대상이 자를 정한다 (케이스)")
    for i, (who, care, tools, c) in enumerate(PER):
        g = back(prog(t, .6 + .5 * i, .4))
        if g <= 0: continue
        y = 440 + 108 * i
        s.append(f'<g transform="translate(540,{y}) scale({g:.3f})"><rect x="-450" y="-46" width="900" height="92" rx="16" fill="{c}"/>'
                 + label(who, -300, -14, 30, "#fff", 900) + label(care, -300, 22, 22, "#fff", 800)
                 + f'<rect x="-120" y="-34" width="560" height="68" rx="12" fill="#fff"/>' + label(tools, 160, 0, 28, c, 900) + "</g>")
    s.append(chip("은퇴가 가까울수록 σ가 아니라 MDD", 540, 880, RED, back(prog(t, 2.8, .4)), w=640, size=32))
    s += eqs(t, EQ, (945, 1045, 1140), a0=3.6, scale=(.4, .44, .44))
    s += explainer_tail(t, "목적과 수명이 자를 바꾼다", "만능 지표 0회 — 대상 · 목적에 맞는 지표 선택의 논리로 평가",
                        ["무엇을, 누구에게, 어떤 자로", "재는지가 측정의 전부야."])
    return s


def cut5(t): return relief(t, ["W09에서 결국", "뭘 배운 거예요?"], ["잘했는지는 한 숫자로 못 알아.", "무엇을 · 무엇과 · 얼마 동안 견줬나지."],
                           "견주는 법!", "체크: 위험 척도 · 성과 지표 · 실력 문턱 · 출처 분해 · 대상별 자", happy=True, a_size=44, chip_size=32)


def cut6(t):   # 시즌 종료 + 다음 예고
    s = [bg(NAVY, "dotsW")]
    s.append(punch("W09 끝!", 540, 520, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("잘했는지 어떻게 아나", 540, 800, 92, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("다음: W10 주식퀀트모델 — 측정에서 전략으로", 540, 1020, 42, "#fff", 800) + "</g>")
    s.append(penguin(380, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .6, "happy"))
    s.append(owl(720, 1610 + (1 - ease_out(prog(t, 1.6, .6))) * 400, .6, blink=(2.6 < t < 2.75)))
    return s


META = dict(
    episode="EP.B4", title="하나의 자로 모두를?",
    concept="대상과 목적이 측정 도구를 정한다 — 운용자의 실력은 TWR(현금흐름 시점 무관), 투자자의 경험은 MWR(IRR). 개인은 나이와 목적에 따라 위험의 뜻이 달라 청년(적립기) TWR · Sharpe, 중년(전환기) Sharpe · Sortino · IR, 은퇴 근접(인출기) MDD · Sortino · Calmar · MWR, 대체투자는 KS-PME. 만능 지표는 없다",
    source="W09 케이스 2 덱(학생 배포) 3장(국민성장펀드 측정체계위원회 — 대체투자 PME 채택 + 3 페르소나 × 5 지표 매트릭스, 위원회 설정 · 수치는 교육용 가상 시나리오) · 6장(TWR — 운용자의 성적 · MWR — 투자자의 경험, 대상이 자를 정한다) · 11장(3 페르소나 × 5 측정 도구, 은퇴가 가까울수록 σ가 아니라 MDD) · 14장(“대체투자는 KS-PME로 시장 대비 판정” · “은퇴 근접은 MDD · Sortino 가중”) · 루브릭(만능 지표 0회)",
    cuts=[{"n": 2, "notice": "IC 제2호 · 측정체계위원회 · 국민성장펀드 측정 체계 초안(교육용 가상) · 모든 상품 · 모든 가입자 Sharpe 하나로 · 펭: “하나로 통일하면 비교가 쉽잖아요”", "bubble": ["지표가 하나면", "비교하기 편하죠?"], "sfx": "통일!"},
          {"n": 3, "bubble": ["청년과 은퇴자는 위험의 뜻부터 달라.", "대상과 목적이 자를 정하는 거야."], "sfx": "자는 여러 개!"},
          {"n": 4, "matrix": {p[0]: f"{p[1]} — {p[2]}" for p in PER}, "latex": ["TWR: manager skill, MWR (IRR): investor experience", "retiree: MDD, Sortino, Calmar, MWR", "alternatives: KS-PME > 1 ⇒ beat the index"],
           "summary": "목적과 수명이 자를 바꾼다", "bubble": ["무엇을, 누구에게, 어떤 자로", "재는지가 측정의 전부야."]},
          {"n": 5, "bubbles": [["W09에서 결국", "뭘 배운 거예요?"], ["잘했는지는 한 숫자로 못 알아.", "무엇을 · 무엇과 · 얼마 동안 견줬나지."]], "sfx": "견주는 법!"},
          {"n": 6, "type": "season_end", "text": ["W09 끝!", "잘했는지 어떻게 아나", "다음: W10 주식퀀트모델 — 측정에서 전략으로"]}],
    **{"fact-check": "국민성장펀드는 실존 정책펀드(2025.12 출범)이나 위원회 설정과 측정 체계 초안은 케이스의 교육용 가상 시나리오. 페르소나별 지표는 케이스 11장 표 그대로(대체투자 행은 케이스 3 · 9장의 KS-PME 채택 안건을 더한 것). 결론 문장은 학생 덱 14장의 '채택되는 발언' 예시까지만 썼다. 시즌 마지막이라 6컷은 W10 예고."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "B4", META)
