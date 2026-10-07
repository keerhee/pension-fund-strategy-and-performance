"""시즌 3 EP.13 '공짜 점심은 아니다' — 리밸런싱 프리미엄은 평균회귀가 있어야 진짜(Chambers 2014). 월간 수익률 AR(1) φ의 t값(240개월):
신흥주식 −3.37 · 상장 부동산 −3.28(평균회귀) · 국내주식 −1.58 · 선진주식 −0.25 · 글로벌채권 +0.55 · 원자재 +0.95(랜덤워크) · 국고채 +2.52(추세).
|t| ≥ 2인 자산에만 좁은(평균회귀) · 넓은(추세) 밴드가 정당하다. (W07 SS2 15·16장 · w7ss2_results.json agenda1.cond1 그대로)"""
from s3kit import *

EQ = [f"eq/ep13_{i}.png" for i in (1, 2, 3)]
ASSETS = [("신흥주식", -3.37), ("상장 부동산", -3.28), ("국내주식", -1.58), ("선진주식", -0.25), ("글로벌채권", 0.55), ("원자재", 0.95), ("국고채 10년", 2.52)]


def cut1(t): return title(t, "EP.13 · 공짜 점심은 아니다", 880)


def cut2(t):
    body = (label("NPS 규모 월간 DR", 0, -110, 36, "#555", 800) + punch("+61bp", 0, -35, 80, fill=GREEN, sw=10)
            + label("펭의 결론: 리밸런싱 = 공짜 알파", 0, 75, 40, NAVY, 900)
            + label("→ 모든 자산을 좁은 밴드로", 0, 140, 40, BLUE, 900))
    return problem(t, "공짜 알파?", GREEN, "#E9F1E4", "펭의 리밸런싱 메모", body, ["리밸런싱은 하면 할수록", "공짜로 버는 거죠?"], "공짜 점심!")


def cut3(t): return twist(t, ["평균회귀가 있는 자산에서만 진짜 수익이야.", "랜덤워크면 회계상 효과일 뿐이지."], "조건부 점심!", size=42, sfx_size=140)


ZX, KX = 590, 72


def cut4(t):
    s = explainer_frame(t, "평균회귀 검정", "월간 수익률 AR(1) φ의 t값 · 240개월 · |t| ≥ 2만 신호로 본다")
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="{ZX}" y1="395" x2="{ZX}" y2="795" stroke="{NAVY}" stroke-width="3"/>'
             + "".join(f'<line x1="{ZX + k*2*KX}" y1="395" x2="{ZX + k*2*KX}" y2="795" stroke="{RED}" stroke-width="3" stroke-dasharray="10 8"/>' for k in (-1, 1))
             + label("−2", ZX - 2 * KX, 812, 24, RED, 900) + label("+2", ZX + 2 * KX, 812, 24, RED, 900) + label("0", ZX, 812, 24, NAVY, 900) + "</g>")
    for i, (nm, tv) in enumerate(ASSETS):
        y = 425 + 56 * i
        g = ease_out(prog(t, .7 + .3 * i, .45))
        if g <= 0: continue
        c = GREEN if tv <= -2 else ORANGE if tv >= 2 else GREY
        w = tv * KX * g; x = ZX + min(0, w)
        s.append(label(nm, 100, y, 28, NAVY, 900, anchor="start"))
        s.append(f'<rect x="{x:.0f}" y="{y-18}" width="{abs(w):.0f}" height="36" fill="{c}" rx="5"/>')
        if g > .9: s.append(label(f"{tv:+.2f}", 985, y, 28, c, 900, anchor="end"))
    s.append(f'<g opacity="{ease_out(prog(t, 3.0, .4)):.2f}">' + label("평균회귀", 230, 830, 26, GREEN, 900) + label("랜덤워크", ZX, 845, 26, GREY, 900)
             + label("추세", 820, 830, 26, ORANGE, 900) + "</g>")
    s.append(chip("평균회귀 → 좁은 밴드 · 추세 → 넓은 밴드 · 나머지 → 지침 값", 540, 905, NAVY, back(prog(t, 3.6, .4)), w=920, size=30))
    s += eqs(t, EQ, (965, 1060, 1160), a0=4.4, scale=(.5, .46, .37))
    s += explainer_tail(t, "평균회귀가 있어야 진짜 프리미엄", "Chambers(2014) — 랜덤워크면 DR은 회계적 효과일 수 있다",
                        ["내린 게 다시 오를 때만", "싸게 산 게 이득이 되거든."])
    return s


def cut5(t): return relief(t, ["그럼 추세가 있는", "국고채는요?"], ["오른 걸 바로 팔면 손해일 수 있어.", "밴드를 넓게 두라는 신호야."],
                           "넓게 둬!", "체크: 자산별 AR(1) φ · t값 · 밴드 폭 · 지침 값", a_size=46, sfx_size=120)


def cut6(t): return next_cut(t, TEAL, "무거래 구간", "가만히 있는 것도 전략일까?", topic_size=170)


META = dict(
    episode="EP.13", title="공짜 점심은 아니다",
    concept="리밸런싱 프리미엄의 조건 — 평균회귀가 있어야 진짜 초과수익(Chambers 2014). 랜덤워크 자산에서 DR은 기하·산술의 회계적 효과일 수 있고, 추세 자산에서는 오른 것을 파는 것이 손해일 수 있다. 자산군별 월간 수익률 AR(1) φ의 t값으로 밴드를 정한다 — 평균회귀(t ≤ −2)는 좁게, 추세(t ≥ 2)는 넓게, 나머지는 지침 값",
    source="W07 SS2 15·16장(자산군별 AR(1) φ의 t값, 신흥주식 · 상장 부동산 φ −0.21(t −3.3) 강한 회귀, 선진주식 랜덤워크, 국고채 +0.16 추세, Chambers 2014 공짜 점심이 아니다) · W07_SS2_케이스데이터 w7ss2_results.json agenda1.cond1(7자산 φ · t · 판정)",
    cuts=[{"n": 2, "notice": "펭의 리밸런싱 메모 · NPS 규모 월간 DR +61bp · 펭의 결론: 리밸런싱 = 공짜 알파 → 모든 자산을 좁은 밴드로", "bubble": ["리밸런싱은 하면 할수록", "공짜로 버는 거죠?"], "sfx": "공짜 점심!"},
          {"n": 3, "bubble": ["평균회귀가 있는 자산에서만 진짜 수익이야.", "랜덤워크면 회계상 효과일 뿐이지."], "sfx": "조건부 점심!"},
          {"n": 4, "t_values": dict(ASSETS), "latex": ["r_t = φ r_{t−1} + ε_t", "φ < 0 and |t| ≥ 2 ⇒ mean reversion", "EM: φ = −0.21 (t = −3.37), KTB: φ = +0.16 (t = +2.52)"],
           "summary": "평균회귀가 있어야 진짜 프리미엄", "bubble": ["내린 게 다시 오를 때만", "싸게 산 게 이득이 되거든."]},
          {"n": 5, "bubbles": [["그럼 추세가 있는", "국고채는요?"], ["오른 걸 바로 팔면 손해일 수 있어.", "밴드를 넓게 두라는 신호야."]], "sfx": "넓게 둬!"},
          {"n": 6, "text": ["다음 화", "무거래 구간", "가만히 있는 것도 전략일까?"]}],
    check={"EM_t": -3.37, "REIT_t": -3.28, "KTB_t": 2.52},
    **{"fact-check": "t값은 SS2 케이스의 교육용 모의 패널(240개월) 추정치이며 실제 시장 통계가 아니다. 강의본 25장은 신흥 · 부동산을 묶어 φ −0.21(t −3.3)으로 적었고, 화면 표는 케이스 결과 파일의 자산별 값(−3.37 · −3.28)을 썼다. 밴드 판정 규칙(|t| ≥ 2)은 케이스 1 조건 ①."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "13", META)
