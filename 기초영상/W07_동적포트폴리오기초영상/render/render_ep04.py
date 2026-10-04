"""시즌 3 EP.04 '내일의 기회를 오늘 산다' — ICAPM 헤징 수요(Merton 1973). h = (1 − 1/γ)·β·σx/σa.
KIC 장기 국채 오버레이: γ 5 · β 1.077 · σx 0.485 · σa 4.22 → 9.9%p. γ 1·2·5·10 → 0 · 6.2 · 9.9 · 11.1%p. VIX는 t −1.57 · 140bp로 기각.
(W07 M9 1교시 14·15장 · 심층 56장 · W07_케이스데이터 w7m9_results.json agenda2 그대로)"""
from s3kit import *

EQ = [f"eq/ep04_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.04 · 내일의 기회를 오늘 산다", 960)


def cut2(t):
    body = (label("장기 국채 기대수익 (올해)", 0, -105, 36, "#555", 800) + punch("낮음", 0, -30, 74, fill=BLUE, sw=9)
            + label("펭의 결론: “단기로 보면 장기채 0%”", 0, 90, 40, NAVY, 900)
            + label("γ 5 · 10년 지평 · 영구 자본", 0, 160, 32, GREY, 800))
    return problem(t, "장기채는 빼자?", BLUE, "#E6ECF7", "KIC 자산배분 검토 (교육용)", body, ["올해 기대수익이 낮으면", "장기채는 안 사도 되죠?"], "0%로!")


def cut3(t): return twist(t, ["장기 투자자는 내일 금리가 떨어질 때를", "대비해 오늘 장기채를 더 사."], "헤징 수요!", size=44, sfx_size=150)


BASE, K = 780, 24


def cut4(t):
    s = explainer_frame(t, "헤징 수요 h", "ICAPM (Merton 1973) · KIC 교육용 모의 패널 480개월 · 10년 지평")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(f'<g opacity="{ease_out(prog(t, .5, .4)):.2f}">' + label("위험회피 γ가 클수록 장기채 헤징 수요가 커진다", 540, 395, 30, NAVY, 900) + "</g>")
    for i, (x, gm, v) in enumerate(((220, 1, 0.0), (430, 2, 6.2), (650, 5, 9.9), (860, 10, 11.1))):
        g = ease_out(prog(t, .8 + .6 * i, .5))
        if g <= 0: continue
        h = max(4, v * K) * g; c = RED if gm == 5 else TEAL
        s.append(f'<rect x="{x-70}" y="{BASE-h:.0f}" width="140" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"+{v:.1f}%p", x, BASE - max(4, v * K) - 28, 36, c, 900) + label(f"γ = {gm}", x, BASE + 36, 30, NAVY, 900))
    s.append(chip("KIC는 γ 5 → 장기채 +9.9%p · 물가연동 +9.7%p", 540, 885, NAVY, back(prog(t, 3.6, .4)), w=860, size=32))
    s += eqs(t, EQ, (950, 1070, 1180), a0=4.4, scale=(.5, .48, .48))
    s += explainer_tail(t, "단기 최적에서 멀어지는 만큼이 내일의 보험", "다기간 투자자에게만 있는 수요 — 근시안(γ = 1)이면 0",
                        ["오늘 수익이 아니라", "내일의 기회를 사는 포지션이야."])
    return s


def cut5(t): return relief(t, ["그럼 VIX 헤지도", "사 두면 좋겠네요?"], ["VIX는 예측력 t −1.57로 약하고", "비용이 연 140bp야. 그래서 기각."],
                           "아무거나 X!", "체크: 예측력 t ≥ 2 · 크기 ≥ 5%p · 캐리 비용 ≤ 30bp", a_size=44)


def cut6(t): return next_cut(t, GREEN, "인적자본", "사람도 자산일까?", topic_size=190)


META = dict(
    episode="EP.04", title="내일의 기회를 오늘 산다",
    concept="ICAPM 헤징 수요 — 투자 기회(금리 · 인플레 · 변동성)가 시간에 따라 변하면 다기간 투자자는 단기 최적 포트폴리오(myopic) 외에 미래 기회 악화에 대비한 추가 포지션(hedging demand)을 잡는다. h = (1 − 1/γ)·β·σx/σa — γ가 클수록, 예측력이 있을수록 커지고 근시안(γ = 1)이면 0",
    source="W07 M9 1교시 14·15장(ICAPM 1973, myopic + hedging demand, KIC 계산값 γ = 5 · 10년 지평에서 약 +10%p, 헤징 사례 — 금리 · 변동성 · 인플레) · 심층 56장 · W07_케이스데이터 w7m9_results.json agenda2(장기 국채 β 1.077 · t 4.08 · σ_state 0.485 · σ_asset 4.22 → 9.9%p · 5bp, 물가연동 9.7%p · 15bp, VIX t −1.57 · −4.6%p · 140bp 기각, γ 민감도 1·2·5·10 → 0 · 6.2 · 9.9 · 11.1)",
    cuts=[{"n": 2, "notice": "KIC 자산배분 검토(교육용) · 장기 국채 기대수익(올해) 낮음 · 펭의 결론 “단기로 보면 장기채 0%” · γ 5 · 10년 지평", "bubble": ["올해 기대수익이 낮으면", "장기채는 안 사도 되죠?"], "sfx": "0%로!"},
          {"n": 3, "bubble": ["장기 투자자는 내일 금리가 떨어질 때를", "대비해 오늘 장기채를 더 사."], "sfx": "헤징 수요!"},
          {"n": 4, "bars": {"γ=1": 0.0, "γ=2": 6.2, "γ=5": 9.9, "γ=10": 11.1}, "latex": ["h = (1 − 1/γ)·β·σx/σa", "= 0.8 × 1.077 × 0.485/4.22 ≈ 9.9%p", "γ = 1 ⇒ h = 0 (myopic)"],
           "summary": "단기 최적에서 멀어지는 만큼이 내일의 보험", "bubble": ["오늘 수익이 아니라", "내일의 기회를 사는 포지션이야."]},
          {"n": 5, "bubbles": [["그럼 VIX 헤지도", "사 두면 좋겠네요?"], ["VIX는 예측력 t −1.57로 약하고", "비용이 연 140bp야. 그래서 기각."]], "sfx": "아무거나 X!"},
          {"n": 6, "text": ["다음 화", "인적자본", "사람도 자산일까?"]}],
    check={"h_bond": 0.0990},
    **{"fact-check": "KIC 숫자는 교육용 모의 패널(480개월) 계산값이며 KIC의 실제 정책이 아니다. 근사식 h = (1 − 1/γ)·β·σx/σa는 강의본 56장 형식을 따른 단순화(Campbell–Viceira류). '올해 기대수익 낮음'은 연출용 문구."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "04", META)
