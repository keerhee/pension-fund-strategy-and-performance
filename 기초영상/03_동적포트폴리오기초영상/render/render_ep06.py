"""시즌 3 EP.06 '비행기가 내려앉듯' — 생애주기 배분. 인적자본이 줄어드는 만큼 금융자산 안 주식을 줄인다.
금융자산 내 주식 비중 30세 ~90% · 40세 ~80% · 50세 ~60% · 60세 ~40% · 70세 ~30%. Bogle의 '나이 = 채권': 30세 주식 70 · 50세 50.
언제 얼마로 바꿀지 미리 정하고 그대로 따른다. (W07 M9 2교시 20장 · 프라이머 5·7장 그대로)"""
from s3kit import *

EQ = [f"eq/ep06_{i}.png" for i in (1, 2, 3)]
LIFE = [(30, 90), (40, 80), (50, 60), (60, 40), (70, 30)]
BOGLE = [(a, 100 - a) for a in (30, 40, 50, 60, 70)]


def cut1(t): return title(t, "EP.06 · 비행기가 내려앉듯", 840)


def cut2(t):
    body = (label("64세까지", -200, -100, 36, "#555", 800) + punch("주식 90%", -200, -25, 64, fill=GREEN, sw=8)
            + label("65세 은퇴일", 200, -100, 36, "#555", 800) + punch("예금 100%", 200, -25, 64, fill=BLUE, sw=8)
            + label("“은퇴하는 날 한 번에 전환”", 0, 120, 42, NAVY, 900))
    return problem(t, "한 번에 착륙?", BLUE, "#E6ECF7", "펭의 은퇴 전환 계획", body, ["은퇴하는 날", "한 번에 바꾸면 되죠?"], "한 방에!")


def cut3(t): return twist(t, ["한 번에 바꾸면 그해 시장이 결과를 정해.", "미리 정한 경로로 서서히 옮겨."], "서서히 착륙!", size=44, sfx_size=140)


X0, X1, Y0, Y1 = 150, 930, 410, 800


def px(a, w): return X0 + (X1 - X0) * (a - 30) / 40, Y1 - (Y1 - Y0) * w / 100


def path(t, a0, pts, c, dash=""):
    g = ease_out(prog(t, a0, 1.4)); n = max(2, int(round(1 + (len(pts) - 1) * g)))
    xy = [px(*p) for p in pts[:n]]
    o = f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in xy)}" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round" {dash}/>'
    return o + "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{c}"/>' for x, y in xy)


def cut4(t):
    s = explainer_frame(t, "생애주기 배분", "금융자산 안 주식 비중 — 인적자본이 줄어든 만큼 줄인다")
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{NAVY}" stroke-width="4"/>'
             f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{NAVY}" stroke-width="4"/>'
             + "".join(label(f"{g}세", px(g, 0)[0], Y1 + 32, 26, NAVY, 800) for g in (30, 40, 50, 60, 70))
             + label("100%", X0 - 50, Y0, 22, GREY, 800) + label("0%", X0 - 35, Y1, 22, GREY, 800) + "</g>")
    s.append(path(t, .8, LIFE, GREEN))
    if t > 2.2:
        s.append(f'<g opacity="{ease_out(prog(t, 2.2, .4)):.2f}">' + "".join(label(f"{w}", px(a_, w)[0] + 34, px(a_, w)[1] - 26, 28, GREEN, 900) for a_, w in LIFE) + "</g>")
    s.append(path(t, 2.8, BOGLE, ORANGE, 'stroke-dasharray="16 10"'))
    s.append(f'<g opacity="{ease_out(prog(t, 3.0, .4)):.2f}"><rect x="610" y="440" width="34" height="10" fill="{GREEN}"/>' + label("생애주기", 654, 446, 26, GREEN, 900, anchor="start")
             + f'<rect x="610" y="480" width="34" height="10" fill="{ORANGE}"/>' + label("나이 = 채권", 654, 486, 26, ORANGE, 900, anchor="start") + "</g>")
    s.append(chip("방향은 같다 — 젊을수록 주식, 나이 들수록 채권", 540, 905, TEAL, back(prog(t, 3.8, .4)), w=860, size=32))
    s += eqs(t, EQ, (970, 1070, 1165), a0=4.6, scale=.48)
    s += explainer_tail(t, "언제 얼마로 바꿀지 미리 정한다", "시장을 보고 그때그때 정하지 않는 것이 핵심",
                        ["줄어드는 월급 채권만큼", "통장 안 채권을 늘리는 거야."])
    return s


def cut5(t): return relief(t, ["시장이 좋을 땐", "경로를 바꿔도 돼요?"], ["그때그때 정하지 않는 게 핵심이야.", "미리 정한 경로를 그대로 따라가."],
                           "규칙대로!", "체크: 나이별 주식 비중 · 이동 속도 · 은퇴 시점", happy=True, a_size=44, sfx_size=120)


def cut6(t): return next_cut(t, ORANGE, "To vs Through", "은퇴 뒤에도 계속 줄일까?", topic_size=125)


META = dict(
    episode="EP.06", title="비행기가 내려앉듯",
    concept="생애주기 배분과 글라이드패스 — 인적자본(채권 같은 월급)이 나이와 함께 줄어드는 만큼 금융자산 안 주식 비중을 줄인다. 언제 얼마로 바꿀지 미리 정하고 그대로 따르는 것이 핵심(시장 타이밍이 아니다). Bogle의 '나이 = 채권'은 같은 방향의 경험적 압축",
    source="W07 M9 2교시 20장(나이별 금융자산 내 주식 비중 30세 ~90% · 40세 ~80% · 50세 ~60% · 60세 ~40% · 70세 ~30%, Bogle 1970년대 룰 '나이 = 채권 비중' — 30세 채권 30 · 주식 70 / 50세 채권 50 · 주식 50) · 프라이머 5·7장(비행기가 내려앉듯 서서히 낮춘다, 미리 정해 두고 그대로 따른다)",
    cuts=[{"n": 2, "notice": "펭의 은퇴 전환 계획 · 64세까지 주식 90% · 65세 은퇴일 예금 100% · “은퇴하는 날 한 번에 전환”", "bubble": ["은퇴하는 날", "한 번에 바꾸면 되죠?"], "sfx": "한 방에!"},
          {"n": 3, "bubble": ["한 번에 바꾸면 그해 시장이 결과를 정해.", "미리 정한 경로로 서서히 옮겨."], "sfx": "서서히 착륙!"},
          {"n": 4, "lines": {"생애주기": LIFE, "나이 = 채권": BOGLE}, "latex": ["w_equity = 100 − age (Bogle)", "30: 100 − 30 = 70%, 50: 100 − 50 = 50%", "lifecycle: 90% (30) → 30% (70)"],
           "summary": "언제 얼마로 바꿀지 미리 정한다", "bubble": ["줄어드는 월급 채권만큼", "통장 안 채권을 늘리는 거야."]},
          {"n": 5, "bubbles": [["시장이 좋을 땐", "경로를 바꿔도 돼요?"], ["그때그때 정하지 않는 게 핵심이야.", "미리 정한 경로를 그대로 따라가."]], "sfx": "규칙대로!"},
          {"n": 6, "text": ["다음 화", "To vs Through", "은퇴 뒤에도 계속 줄일까?"]}],
    check={"bogle_30": 70, "bogle_50": 50},
    **{"fact-check": "나이별 비중은 강의본 20장의 근사값(~)이다. '나이 = 채권'은 이론적 최적이 아니라 경험적 압축(강의본 23장 비판, EP.08). 펭의 '은퇴일 일괄 전환'은 연출용 대비 사례. 시장 타이밍 대신 사전 경로라는 원칙은 프라이머 7장 표현을 따랐다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "06", META)
