"""시즌 3 EP.11 '분산은 수익도 낳는다' — 분산수익 DR(Booth–Fama 1992) = 고정 비중 포트의 기하수익 − 자산 기하수익의 가중평균 ≈ ½(Σwσ² − σp²).
σ 20% 두 자산 · 50/50(예시): ρ 0 → σp² 0.02 → DR 1%p, ρ 0.5 → 0.5%p, ρ 1 → 0. NPS 규모 월간 리밸런싱 DR 61bp/년.
(W07 SS2 2·9·10장 · 프라이머 10장 — 두 자산 수치는 교육용 예시)"""
from s3kit import *

EQ = [f"eq/ep11_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.11 · 분산은 수익도 낳는다", 920)


def cut2(t):
    body = (label("자산 A · 자산 B (예시)", 0, -110, 38, NAVY, 900)
            + label("둘 다 σ 20% · 같은 기대수익", 0, -45, 38, "#555", 800)
            + label("섞으면?", -170, 50, 40, "#555", 800) + punch("50/50", 60, 50, 74, fill=TEAL, sw=9)
            + label("펭: 평균의 평균은 평균", 0, 155, 38, BLUE, 900))
    return problem(t, "섞어도 같다?", TEAL, "#DDF0EE", "펭의 포트폴리오 실험", body, ["같은 자산 둘을 섞어도", "수익은 그대로죠?"], "평균은 평균!")


def cut3(t): return twist(t, ["비중을 지키면 포트 분산이 줄어.", "EP.01의 ‘깎이는 몫’이 줄어든 만큼 더 남지."], "분산 = 수익!", size=42, sfx_size=150)


BASE, K = 780, 300


def cut4(t):
    s = explainer_frame(t, "분산수익 DR", "σ 20% 두 자산 · 50/50 고정 비중 · 상관 ρ만 바꾼다 (예시)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(f'<g opacity="{ease_out(prog(t, .5, .4)):.2f}">' + label("상관이 낮을수록 분산수익이 크다", 540, 400, 32, NAVY, 900) + "</g>")
    for i, (x, rho, v) in enumerate(((250, "0", 1.0), (540, "0.5", .5), (830, "1", 0.0))):
        g = ease_out(prog(t, .8 + .7 * i, .5))
        if g <= 0: continue
        h = max(4, v * K) * g; c = GREEN if v > .7 else TEAL if v > 0 else GREY
        s.append(f'<rect x="{x-80}" y="{BASE-h:.0f}" width="160" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"+{v:.1f}%p", x, BASE - max(4, v * K) - 28, 38, c, 900) + label(f"ρ = {rho}", x, BASE + 36, 32, NAVY, 900))
    s.append(chip("NPS 규모 실측 패널: 월간 리밸런싱 DR ≈ 61bp/년", 540, 885, NAVY, back(prog(t, 3.4, .4)), w=880, size=32))
    s += eqs(t, EQ, (945, 1090, 1190), a0=4.2, scale=(.5, .46, .48))
    s += explainer_tail(t, "분산은 위험만 줄이는 게 아니다", "Booth–Fama(1992) — 고정 비중 = 리밸런싱이 핵심",
                        ["포트 분산이 작을수록", "기하수익이 높아지는 거야."])
    return s


def cut5(t): return relief(t, ["상관이 1이면", "어떻게 돼요?"], ["똑같이 움직이면 DR은 0이야.", "따로 놀수록 리밸런싱이 벌어."],
                           "따로 놀아야!", "체크: 자산별 σ · 상관 ρ · 고정 비중 유지", happy=True, a_size=46, sfx_size=110)


def cut6(t): return next_cut(t, NAVY, "얼마나 자주?", "매일 맞추면 더 벌까?", topic_size=170)


META = dict(
    episode="EP.11", title="분산은 수익도 낳는다",
    concept="분산수익 DR(diversification return, Booth–Fama 1992) — 고정 비중 포트폴리오의 기하수익이 자산 기하수익의 가중평균보다 높은 몫 ≈ ½(Σwσ² − σp²). 리밸런싱으로 비중을 지키면 포트 분산이 작아져 변동성 비용(σ²/2, EP.01)이 줄어든 만큼 더 남는다. 상관이 낮을수록 크고, 상관 1이면 0",
    source="W07 SS2 2·9·10장(DR 정의 ≈ ½(Σwσ² − σp²) · Booth–Fama 1992 · 상관이 낮을수록 DR 커짐 · 기하평균 ≈ 산술평균 − 분산/2, NPS 규모 월간 DR 61bp · 연간 50bp) · 프라이머 10장(깎이는 몫 σ²/2)",
    cuts=[{"n": 2, "notice": "펭의 포트폴리오 실험 · 자산 A · 자산 B(예시) · 둘 다 σ 20% · 같은 기대수익 · 섞으면? 50/50 · 펭: 평균의 평균은 평균", "bubble": ["같은 자산 둘을 섞어도", "수익은 그대로죠?"], "sfx": "평균은 평균!"},
          {"n": 3, "bubble": ["비중을 지키면 포트 분산이 줄어.", "EP.01의 ‘깎이는 몫’이 줄어든 만큼 더 남지."], "sfx": "분산 = 수익!"},
          {"n": 4, "bars": {"ρ=0": 1.0, "ρ=0.5": 0.5, "ρ=1": 0.0}, "latex": ["DR = ½(Σ w_i σ_i² − σ_p²)", "ρ = 0: σ_p² = 0.02 ⇒ ½(0.04 − 0.02) = 1%p", "ρ = 1: σ_p² = 0.04 ⇒ DR = 0"],
           "summary": "분산은 위험만 줄이는 게 아니다", "bubble": ["포트 분산이 작을수록", "기하수익이 높아지는 거야."]},
          {"n": 5, "bubbles": [["상관이 1이면", "어떻게 돼요?"], ["똑같이 움직이면 DR은 0이야.", "따로 놀수록 리밸런싱이 벌어."]], "sfx": "따로 놀아야!"},
          {"n": 6, "text": ["다음 화", "얼마나 자주?", "매일 맞추면 더 벌까?"]}],
    check={"DR_rho0": 0.01, "DR_rho05": 0.005, "DR_rho1": 0.0},
    **{"fact-check": "두 자산 σ 20% · 50/50 · ρ 0/0.5/1은 교육용 예시이며 DR 근사식(로그정규 · 연속 리밸런싱)을 따른다. NPS 61bp는 SS2 케이스의 20년 모의 패널(7자산) 월간 리밸런싱 값. DR이 진짜 초과수익인지는 평균회귀에 달렸다(Chambers 2014, EP.13)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "11", META)
