"""시즌 3 EP.16 'RL이 넘어야 할 벽' — 기준선(baseline) 사다리. Gârleanu–Pedersen(JF 2013) 20만 기간 가상 실험(γ 1 · λ 2, a/λ = 0.5):
기간당 순효용 목표 추종 −7.2 · 조준만 42.7 · 부분 이동만(최적 속도 0.40) 67.4 · GP 69.8 — RL이 69.8을 재현하는지가 첫 시험.
사다리 0 현금·보유 → 1 정기 리밸런싱 → 2 변동성 목표 → 3 수축 MVO → 4 무거래 구간·GP·MPO → 5 RL. (W07 M9 3교시 34·35·36장 그대로)"""
from s3kit import *

EQ = [f"eq/ep16_{i}.png" for i in (1, 2, 3)]
STRAT = [("목표 추종", -7.2, GREY), ("조준만", 42.7, TEAL), ("부분 이동만", 67.4, TEAL), ("GP", 69.8, GREEN)]


def cut1(t): return title(t, "EP.16 · RL이 넘어야 할 벽", 860)


def cut2(t):
    body = (label("논문 요약 (Samsudin 2021)", 0, -110, 36, "#555", 800)
            + label("RL", -200, -35, 40, "#555", 900) + punch("+20%", -200, 40, 78, fill=GREEN, sw=10)
            + label("MVO", 200, -35, 40, "#555", 900) + punch("−1%", 200, 40, 78, fill=RED, sw=10)
            + label("펭: “바로 도입하자!”", 0, 160, 40, BLUE, 900))
    return problem(t, "RL 압승?", "#6B3FA0", "#F1E6F4", "펭이 가져온 AI 운용 논문", body, ["RL이 21%p나 이겼대요!", "바로 도입해요!"], "RL 최고!")


def cut3(t): return twist(t, ["약한 상대(30시점 MVO)랑 붙은 거야.", "기준선 사다리 4단계부터 이겨야 해."], "상대를 봐!", size=44, sfx_size=150)


BASE, K = 680, 3.5


def cut4(t):
    s = explainer_frame(t, "기준선 사다리", "GP 20만 기간 가상 실험 · γ 1 · λ 2 · 기간당 순효용")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (nm, v, c) in enumerate(STRAT):
        x = 210 + 220 * i
        g = ease_out(prog(t, .7 + .6 * i, .5))
        if g <= 0: continue
        h = abs(v) * K * g; y = BASE - h if v > 0 else BASE
        s.append(f'<rect x="{x-70}" y="{y:.0f}" width="140" height="{h:.0f}" fill="{c}" rx="6"/>')
        if g > .9:
            s.append(label(f"{v:+.1f}", x, BASE - v * K - 28 if v > 0 else BASE + abs(v) * K + 28, 38, RED if nm == "GP" else c, 900))
            s.append(label(nm, x, BASE - 30 if v < 0 else BASE + 36, 28, NAVY, 900))
    steps = ["0 보유", "1 리밸런싱", "2 변동성", "3 MVO", "4 구간·GP", "5 RL"]
    for i, st in enumerate(steps):
        g = ease_out(prog(t, 3.2 + .2 * i, .3))
        x = 105 + 148 * i
        s.append(f'<g opacity="{g:.2f}"><rect x="{x}" y="{870 - 14*i}" width="140" height="{50 + 14*i}" rx="8" fill="{RED if i == 5 else (GREEN if i == 4 else NAVY)}"/>'
                 + label(st, x + 70, 895, 22, "#fff", 900) + "</g>")
    s += eqs(t, EQ, (960, 1055, 1150), a0=4.6, scale=(.46, .5, .42))
    s += explainer_tail(t, "4단계를 못 이긴 RL은 단순 규칙의 재발명", "같은 비용 · 같은 체결 조건에서 사다리를 차례로 넘는다",
                        ["조준과 부분 이동을 합친", "GP 69.8이 첫 번째 시험이야."], red_size=42)
    return s


def cut5(t): return relief(t, ["그럼 RL은", "왜 쓰는 거예요?"], ["사다리 넷이 설명 못 한 나머지만", "RL의 몫이야. 그걸 증명해야 하지."],
                           "나머지만!", "체크: 같은 비용 · 같은 체결 · 기준선 6단계 · 순효용", a_size=44, sfx_size=120)


def cut6(t): return next_cut(t, NAVY, "시장의 과거", "실무는 왜 신중할까?", topic_size=180)


META = dict(
    episode="EP.16", title="RL이 넘어야 할 벽",
    concept="기준선(baseline) 사다리 — RL 결과는 같은 비용 · 체결 조건에서 여섯 단계 비교 전략(0 현금·보유, 1 정기 리밸런싱, 2 변동성 목표, 3 수축 MVO, 4 무거래 구간·GP·MPO, 5 RL)과 비교해야 한다. 4단계(비용 인지형 공식 · 수치해)를 못 이긴 RL은 단순 규칙을 복잡하게 다시 배운 것. 첫 시험은 Gârleanu–Pedersen의 조준 + 부분 이동(69.8)을 재현하는 것",
    source="W07 M9 3교시 34장(GP JF 2013 — γ 1 · λ 2 → a/λ = 0.5) · 35장(20만 기간 시뮬레이션 기간당 순효용 — 목표 추종 −7.2 · 부분 이동만(최적 속도 0.40) 67.4 · 조준만 42.7 · GP 69.8, 가상 실험) · 36장(기준선 사다리 6단계, Samsudin(2021) ‘RL 20% 대 MVO −1%’는 30시점 MVO라는 약한 상대 — 사다리가 없는 비교)",
    cuts=[{"n": 2, "notice": "펭이 가져온 AI 운용 논문 · 논문 요약(Samsudin 2021) · RL +20% · MVO −1% · 펭: “바로 도입하자!”", "bubble": ["RL이 21%p나 이겼대요!", "바로 도입해요!"], "sfx": "RL 최고!"},
          {"n": 3, "bubble": ["약한 상대(30시점 MVO)랑 붙은 거야.", "기준선 사다리 4단계부터 이겨야 해."], "sfx": "상대를 봐!"},
          {"n": 4, "bars": {s[0]: s[1] for s in STRAT}, "ladder": ["0 보유", "1 리밸런싱", "2 변동성", "3 MVO", "4 구간·GP", "5 RL"], "latex": ["a/λ = 0.5 (γ = 1, λ = 2)", "69.8 > 67.4 > 42.7 > −7.2", "RL ≥ ladder step 4 (band, GP, MPO)"],
           "summary": "4단계를 못 이긴 RL은 단순 규칙의 재발명", "bubble": ["조준과 부분 이동을 합친", "GP 69.8이 첫 번째 시험이야."]},
          {"n": 5, "bubbles": [["그럼 RL은", "왜 쓰는 거예요?"], ["사다리 넷이 설명 못 한 나머지만", "RL의 몫이야. 그걸 증명해야 하지."]], "sfx": "나머지만!"},
          {"n": 6, "text": ["다음 화", "시장의 과거", "실무는 왜 신중할까?"]}],
    check={"GP": 69.8, "partial": 67.4, "aim": 42.7, "chase": -7.2},
    **{"fact-check": "순효용 숫자는 강의본 35장의 가상 실험(20만 기간 · γ 1 · λ 2) 값. Samsudin(2021) 'RL 20% 대 MVO −1%'는 강의본 36장 표기를 따랐다(논문 세부는 화면에 넣지 않음). 사다리 단계 이름은 화면용으로 줄였다(2 변동성 = 변동성 목표, 3 MVO = 수축 MVO(1기간), 4 = 무거래 구간 · GP · MPO)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "16", META)
