"""시즌 4 EP.03 '분산했더니 위험이 늘었다?' — VaR의 부분가법성 위반(Artzner 1999). 독립 자산 A · B가 각각 4% 확률로 −100, 그 외 0:
95% VaR(A) = VaR(B) = 0(4% < 5%), 합치면 손실 확률 1 − 0.96² = 7.8% > 5% → VaR(A + B) = 100. CVaR는 네 공리를 모두 지킨다 → Basel이 VaR를 ES로 교체(FRTB 2019 확정).
(W09 강의본 11·12·40장 그대로)"""
from s4kit import *

EQ = [f"eq/ep03_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.03 · 분산했더니 위험이 늘었다?", 980)


def cut2(t):
    body = (f'<rect x="-350" y="-130" width="330" height="150" rx="18" fill="#F1E6F4"/><rect x="20" y="-130" width="330" height="150" rx="18" fill="#F1E6F4"/>'
            + label("자산 A", -185, -90, 38, "#6B3FA0", 900) + label("VaR 0", -185, -30, 46, NAVY, 900)
            + label("자산 B", 185, -90, 38, "#6B3FA0", 900) + label("VaR 0", 185, -30, 46, NAVY, 900)
            + label("A + B 합치면", -120, 95, 38, "#555", 800) + punch("VaR 100", 160, 95, 66, fill=RED, sw=8))
    return problem(t, "0 + 0 = 100?", "#6B3FA0", "#F1E6F4", "펭의 분산 투자 보고서 (95% VaR)", body, ["나눠 담았는데", "위험이 왜 늘어요?"], "계산 오류?!")


def cut3(t): return twist(t, ["계산은 맞아. VaR라는 자가 고장 난 거야.", "분산이 위험을 늘리는 것처럼 보이게 하지."], "자가 틀렸다!", size=42, sfx_size=140)


def cut4(t):
    s = explainer_frame(t, "좋은 위험 척도의 네 공리", "Artzner(1999) Coherent Risk Measure — 어기는 척도를 찾아라", head_size=86)
    rows = [(["① 단조성", "더 나쁜 자산 = 더 큰 위험", "—"], [NAVY, NAVY, GREY]),
            (["② 부분가법성", "분산하면 위험이 늘지 않는다", "VaR 위반"], [NAVY, NAVY, RED]),
            (["③ 양의 동질성", "포지션 2배 → 위험 2배", "—"], [NAVY, NAVY, GREY]),
            (["④ 평행이동 불변", "무위험 현금 추가 → 위험 감소", "σ 위반"], [NAVY, NAVY, RED])]
    s.append(table(t, .5, 3, [190, 530, 880], ["공리", "뜻", "위반"], rows, size=27, head_size=25, dy=60))
    s.append(chip("CVaR는 네 공리를 모두 지킨다 → Basel FRTB: VaR → ES(2019 확정)", 540, 735, GREEN, back(prog(t, 3.0, .4)), w=960, size=27))
    s += eqs(t, EQ, (810, 915, 1035), a0=3.8, scale=(.44, .38, .44))
    s += explainer_tail(t, "VaR를 쓰되, VaR만 믿지 말라", "집중 포지션이 VaR상 ‘안전’해 보이는 규제 차익의 함정",
                        ["4%짜리 사고는 VaR 눈에", "아예 안 보이거든."])
    return s


def cut5(t): return relief(t, ["한 편의 논문이", "규제를 바꿨어요?"], ["1999년 증명이 20년 걸려", "2019년 Basel FRTB로 확정됐지."],
                           "공리가 규제를!", "체크: 척도의 공리 · 꼬리 확률 < 신뢰수준 · 집중 포지션", happy=True, a_size=46, sfx_size=110)


def cut6(t): return next_cut(t, ORANGE, "반토막", "50% 잃으면 얼마 벌어야?", topic_size=200)


META = dict(
    episode="EP.03", title="분산했더니 위험이 늘었다?",
    concept="VaR의 치명적 결함 — 부분가법성 위반. 각각 4% 확률로 크게 잃는 독립 자산은 95% VaR가 0이지만, 합치면 손실 확률이 7.8%로 5%를 넘어 VaR가 100이 된다. 분산이 위험을 늘린 것처럼 보여 분산 인센티브를 왜곡한다. Artzner(1999)의 Coherent 네 공리를 CVaR(ES)는 모두 충족 → Basel FRTB가 VaR를 ES로 교체",
    source="W09 강의본 11장(Coherent 4공리 — 단조성 · 부분가법성(VaR 위반) · 양의 동질성 · 평행이동 불변(σ 위반), CVaR 모두 충족 → Basel III가 VaR를 ES로) · 12장(반례 — A · B 각 4% 확률로 −100, 95% VaR 0, 합치면 손실 확률 ≈ 7.8% → VaR(A + B) = 100) · 40장(1999 논문 → 2013 FRTB 협의안 → 2019 최종 확정, 시행 2025)",
    cuts=[{"n": 2, "notice": "펭의 분산 투자 보고서(95% VaR) · 자산 A VaR 0 · 자산 B VaR 0 · A + B 합치면 VaR 100", "bubble": ["나눠 담았는데", "위험이 왜 늘어요?"], "sfx": "계산 오류?!"},
          {"n": 3, "bubble": ["계산은 맞아. VaR라는 자가 고장 난 거야.", "분산이 위험을 늘리는 것처럼 보이게 하지."], "sfx": "자가 틀렸다!"},
          {"n": 4, "table": {"① 단조성": "—", "② 부분가법성": "VaR 위반", "③ 양의 동질성": "—", "④ 평행이동 불변": "σ 위반"}, "latex": ["VaR95(A) = VaR95(B) = 0 (4% < 5%)", "P(loss) = 1 − 0.96² = 7.8% > 5% ⇒ VaR(A + B) = 100", "VaR(A + B) > VaR(A) + VaR(B)"],
           "summary": "VaR를 쓰되, VaR만 믿지 말라", "bubble": ["4%짜리 사고는 VaR 눈에", "아예 안 보이거든."]},
          {"n": 5, "bubbles": [["한 편의 논문이", "규제를 바꿨어요?"], ["1999년 증명이 20년 걸려", "2019년 Basel FRTB로 확정됐지."]], "sfx": "공리가 규제를!"},
          {"n": 6, "text": ["다음 화", "반토막", "50% 잃으면 얼마 벌어야?"]}],
    check={"p_loss": 0.0784},
    **{"fact-check": "반례의 숫자(4% · −100)는 강의본 12장의 교육용 예. 1 − 0.96² = 7.84%이며 두 자산이 동시에 잃을 확률(0.16%)을 포함한다 — 합친 포트폴리오의 95% 분위 손실은 최소 100이라는 단순화를 강의본 표기대로 따랐다. FRTB 연도(2013 협의안 · 2019 확정 · 시행 2025)는 강의본 40장."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "03", META)
