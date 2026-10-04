"""시즌 4 EP.10 '정확도 × √베팅 수' — Grinold의 근본법칙(1989) IR = IC × √BR. IC는 예측 · 실현 상관, BR은 독립적 베팅 수.
재량형 IC 0.20 · BR 4 → 0.40 vs 퀀트형 IC 0.05 · BR 100 → 0.50(예시). Renaissance는 IC 0.02~0.05 · BR 수천으로 IR 2~4(강의본).
(W09 강의본 23장 · 케이스 1 8장 — 재량형 · 퀀트형 숫자는 예시)"""
from s4kit import *

EQ = [f"eq/ep10_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.10 · 정확도 × √베팅 수", 860)


def cut2(t):
    body = (f'<rect x="-350" y="-130" width="330" height="190" rx="18" fill="#F1E6F4"/><rect x="20" y="-130" width="330" height="190" rx="18" fill="#E6ECF7"/>'
            + label("재량형 매니저", -185, -85, 34, "#6B3FA0", 900) + label("적중률 높음", -185, -25, 32, NAVY, 900) + label("1년에 4번 베팅", -185, 20, 30, NAVY, 800)
            + label("퀀트 매니저", 185, -85, 34, BLUE, 900) + label("적중률 낮음", 185, -25, 32, NAVY, 900) + label("1년에 100번 베팅", 185, 20, 30, NAVY, 800)
            + label("펭: “잘 맞히는 재량형이 이긴다”", 0, 140, 38, NAVY, 900))
    return problem(t, "누가 이기나?", "#6B3FA0", "#F1E6F4", "펭의 위탁 매니저 비교 (예시)", body, ["더 잘 맞히는 쪽이", "당연히 이기죠?"], "적중률!")


def cut3(t): return twist(t, ["성과는 정확도 곱하기 √베팅 수야.", "조금 덜 맞혀도 많이 걸면 이길 수 있어."], "폭도 실력!", size=44, sfx_size=160)


BASE, K = 760, 520


def cut4(t):
    s = explainer_frame(t, "근본법칙 IR = IC√BR", "IC = 예측과 실현의 상관 · BR = 독립적 베팅 수 (Grinold 1989)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (x, nm, ic, br, ir, c) in enumerate(((300, "재량형", .20, 4, .40, "#6B3FA0"), (780, "퀀트형", .05, 100, .50, BLUE))):
        g = ease_out(prog(t, .8 + 1.0 * i, .5))
        if g <= 0: continue
        h = ir * K * g
        s.append(f'<rect x="{x-90}" y="{BASE-h:.0f}" width="180" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"IR {ir:.2f}", x, BASE - ir * K - 30, 40, c, 900) + label(f"{nm} · IC {ic:.2f} · BR {br}", x, BASE + 36, 28, NAVY, 900))
    s.append(chip("IC는 쉽게 오르지 않는다 — 0.05만 넘어도 우수", 540, 880, NAVY, back(prog(t, 2.8, .4)), w=820, size=32))
    s += eqs(t, EQ, (945, 1050, 1150), a0=3.6, scale=(.5, .46, .48))
    s += explainer_tail(t, "액티브 성과 = 예측 정확도 × √베팅 수", "Renaissance: IC 0.02~0.05 · BR 수천 → IR 2~4",
                        ["100번 거는 사람은 10번 거는 사람보다", "√10배, 약 3배 유리해."], owl_size=38)
    return s


def cut5(t): return relief(t, ["그럼 베팅을 무조건", "많이 하면 되겠네요?"], ["서로 닮은 베팅은 한 번으로 쳐.", "상관된 BR은 부풀려진 숫자야."],
                           "독립이어야!", "체크: IC(적중) · BR(독립 베팅 수) · 상관 · 비용(TC)", a_size=46, sfx_size=110)


def cut6(t): return next_cut(t, TEAL, "알파 공식", "점수를 알파로 바꾸면?", topic_size=190)


META = dict(
    episode="EP.10", title="정확도 × √베팅 수",
    concept="Grinold의 근본법칙(1989) IR = IC × √BR — 액티브 성과는 예측 정확도(IC, 예측과 실현의 상관)와 독립적 베팅 수(BR)의 제곱근의 곱. 고 IC · 저 BR(재량형) vs 저 IC · 고 BR(퀀트)의 트레이드오프. IC는 쉽게 오르지 않고(0.05만 넘어도 우수), 상관된 베팅은 BR을 부풀린다",
    source="W09 강의본 23장(근본법칙 — IC 예측 정확도 · BR 독립적 베팅 수, 고 IC · 저 BR(재량적) vs 저 IC · 고 BR(퀀트), Renaissance IC 0.02–0.05 · BR 수천 → IR 2–4) · 케이스 1 8장(IC 0.05만 넘어도 우수 · 쉽게 오르지 않는다, 100 bets가 10보다 √10배, 상관 bets는 BR 부풀림, TC 제약) · 보충교재 15(FLAM 일반화)",
    cuts=[{"n": 2, "notice": "펭의 위탁 매니저 비교(예시) · 재량형: 적중률 높음 · 1년에 4번 베팅 / 퀀트: 적중률 낮음 · 1년에 100번 베팅 · 펭: “잘 맞히는 재량형이 이긴다”", "bubble": ["더 잘 맞히는 쪽이", "당연히 이기죠?"], "sfx": "적중률!"},
          {"n": 3, "bubble": ["성과는 정확도 곱하기 √베팅 수야.", "조금 덜 맞혀도 많이 걸면 이길 수 있어."], "sfx": "폭도 실력!"},
          {"n": 4, "bars": {"재량형 IC 0.20 · BR 4": 0.40, "퀀트형 IC 0.05 · BR 100": 0.50}, "latex": ["IR = IC × √BR", "0.20 × √4 = 0.40, 0.05 × √100 = 0.50", "IC 0.03 × √3,000 ≈ 1.6"],
           "summary": "액티브 성과 = 예측 정확도 × √베팅 수", "bubble": ["100번 거는 사람은 10번 거는 사람보다", "√10배, 약 3배 유리해."]},
          {"n": 5, "bubbles": [["그럼 베팅을 무조건", "많이 하면 되겠네요?"], ["서로 닮은 베팅은 한 번으로 쳐.", "상관된 BR은 부풀려진 숫자야."]], "sfx": "독립이어야!"},
          {"n": 6, "text": ["다음 화", "알파 공식", "점수를 알파로 바꾸면?"]}],
    check={"discretionary": 0.40, "quant": 0.50, "renaissance_like": 1.64},
    **{"fact-check": "재량형(IC 0.20 · BR 4)과 퀀트형(IC 0.05 · BR 100)은 교육용 예시. 셋째 수식(IC 0.03 · BR 3,000 → 1.6)은 강의본의 Renaissance 범위를 보여 주는 예시로, 강의본의 IR 2~4는 실제 보고치이며 근본법칙 그대로 재현되지는 않는다(TC · 비용 등). '약 3배'는 √10 ≈ 3.16."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "10", META)
