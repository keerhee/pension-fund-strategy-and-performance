"""시즌 4 EP.04 '반토막의 수학' — MDD(고점 대비 최대 낙폭)와 Calmar. MDD 50% → 복구에 +100% 필요. 필요 수익 = 1/(1 − MDD) − 1:
10% → 11% · 20% → 25% · 30% → 43% · 50% → 100%. Calmar = 연수익 ÷ MDD(예: 9 ÷ 22 = 0.41). 투자자는 σ가 아니라 낙폭에 반응한다.
(W09 강의본 15·22장 그대로, 낙폭별 필요 수익은 같은 식으로 계산)"""
from s4kit import *

EQ = [f"eq/ep04_{i}.png" for i in (1, 2, 3)]
MDD = [(10, 11), (20, 25), (30, 43), (50, 100)]


def cut1(t): return title(t, "EP.04 · 반토막의 수학", 760)


def cut2(t):
    body = (label("작년", -190, -100, 38, "#555", 800) + punch("−50%", -190, -25, 80, fill=RED, sw=10)
            + label("올해", 190, -100, 38, "#555", 800) + punch("+50%", 190, -25, 80, fill=GREEN, sw=10)
            + label("펭: “잃은 만큼 다시 벌었으니 본전!”", 0, 120, 38, NAVY, 900))
    return problem(t, "본전 회복?", ORANGE, "#FCEBDD", "펭의 펀드 2년 성적", body, ["50% 잃고 50% 벌었으니", "원금 회복이죠?"], "회복 완료!")


def cut3(t): return twist(t, ["100이 50이 되면, 다시 100이 되려면", "+100%가 필요해. 지금은 75야."], "반토막 = 두 배!", size=44, sfx_size=140)


BASE, K = 790, 3.4


def cut4(t):
    s = explainer_frame(t, "낙폭과 복구", "고점 대비 최대 낙폭 MDD → 원금 회복에 필요한 수익")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (d, r) in enumerate(MDD):
        cx = 210 + 220 * i
        for j, (v, c, nm) in enumerate(((d, RED, "낙폭"), (r, GREEN, "복구"))):
            g = ease_out(prog(t, .7 + .6 * i + .25 * j, .45))
            if g <= 0: continue
            x = cx - 45 + 90 * j; h = v * K * g
            s.append(f'<rect x="{x-38}" y="{BASE-h:.0f}" width="76" height="{h:.0f}" fill="{c}" rx="5"/>')
            if g > .9: s.append(label(f"{'−' if j == 0 else '+'}{v}%", x, BASE - v * K - 24, 28, c, 900))
        s.append(f'<g opacity="{ease_out(prog(t, .7 + .6 * i, .4)):.2f}">' + label(f"MDD {d}%", cx, BASE + 34, 28, NAVY, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 3.2, .4)):.2f}"><rect x="110" y="410" width="28" height="22" fill="{RED}"/>' + label("낙폭", 148, 421, 26, RED, 900, anchor="start")
             + f'<rect x="230" y="410" width="28" height="22" fill="{GREEN}"/>' + label("복구에 필요한 수익", 268, 421, 26, GREEN, 900, anchor="start") + "</g>")
    s.append(chip("투자자는 σ가 아니라 낙폭에 반응한다 — 환매 · 해지를 부르는 숫자", 540, 895, NAVY, back(prog(t, 3.6, .4)), w=940, size=28))
    s += eqs(t, EQ, (960, 1060, 1155), a0=4.4, scale=(.44, .46, .44))
    s += explainer_tail(t, "낙폭이 깊을수록 복구는 가파르게 멀어진다", "Calmar = 수익 1%를 낙폭 몇 %로 샀나 · 3년 이상으로 볼 것",
                        ["30%만 빠져도", "43%를 벌어야 해."])
    return s


def cut5(t): return relief(t, ["연기금도 낙폭이", "그렇게 중요해요?"], ["적립비율과 유동성 위기로 바로 이어져.", "깊이가 곧 공포야."],
                           "깊이 = 공포!", "체크: MDD · 회복 기간 · Calmar · 평가 기간 3년 이상", a_size=44, sfx_size=110)


def cut6(t): return next_cut(t, NAVY, "LTCM", "모델이 틀리면?", topic_size=200)


META = dict(
    episode="EP.04", title="반토막의 수학",
    concept="MDD(고점 대비 최대 낙폭)와 Calmar — 투자자는 σ가 아니라 낙폭에 반응한다. 잃은 비율보다 되찾는 데 필요한 수익이 더 크다: 필요 수익 = 1/(1 − MDD) − 1, MDD 50%면 +100%. Calmar = 연수익 ÷ MDD로 '수익 1%를 낙폭 몇 %로 샀는가'를 본다(헤지펀드 · CTA 표준, 3년 이상으로)",
    source="W09 강의본 15장(MDD와 Calmar — 투자자는 σ가 아니라 낙폭에 반응, MDD 50% → 복구에 +100%, Calmar = 연수익/MDD, 기간 의존 큼 3년 이상, 기관 — 적립비율 · 유동성 위기와 직결) · 22장(Calmar 9/22 = 0.41) · 프라이머 9장(W07 EP.01과 같은 +50 / −50 직관)",
    cuts=[{"n": 2, "notice": "펭의 펀드 2년 성적 · 작년 −50% · 올해 +50% · 펭: “잃은 만큼 다시 벌었으니 본전!”", "bubble": ["50% 잃고 50% 벌었으니", "원금 회복이죠?"], "sfx": "회복 완료!"},
          {"n": 3, "bubble": ["100이 50이 되면, 다시 100이 되려면", "+100%가 필요해. 지금은 75야."], "sfx": "반토막 = 두 배!"},
          {"n": 4, "bars": {f"MDD {d}%": f"+{r}%" for d, r in MDD}, "latex": ["100 × (1 − 0.5) = 50 ⇒ 100/50 − 1 = +100%", "required = 1/(1 − MDD) − 1", "Calmar = annual return/MDD = 9/22 ≈ 0.41"],
           "summary": "낙폭이 깊을수록 복구는 가파르게 멀어진다", "bubble": ["30%만 빠져도", "43%를 벌어야 해."]},
          {"n": 5, "bubbles": [["연기금도 낙폭이", "그렇게 중요해요?"], ["적립비율과 유동성 위기로 바로 이어져.", "깊이가 곧 공포야."]], "sfx": "깊이 = 공포!"},
          {"n": 6, "text": ["다음 화", "LTCM", "모델이 틀리면?"]}],
    check={"req": {"10": 11.1, "20": 25.0, "30": 42.9, "50": 100.0}, "calmar": 0.409},
    **{"fact-check": "10 · 20 · 30%의 필요 수익(11 · 25 · 43%)은 강의본의 50% → 100% 식을 같은 식으로 계산해 더한 값(반올림). '깊이가 곧 공포'는 강의본 9장 비유. 펭의 2년 성적은 연출용(W07 EP.01과 같은 경로)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "04", META)
