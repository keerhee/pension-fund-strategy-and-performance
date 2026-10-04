"""시즌 4 EP.12 '3년 성적이면 안다?' — 짧은 기록으로는 실력과 운을 가를 수 없다. 1년치로 판단하려면 해마다 4%p는 앞서야 운이 아니라고 말할 수 있다(프라이머 13장).
t = IR × √T ≥ 2 → α ≥ 2 × TE / √T. TE 2%(예시)면 1년 4%p · 4년 2%p · 16년 1%p. 대부분의 펀드 평가가 이 문턱을 넘지 못한 채 이뤄진다.
(W09 프라이머 13·14장 · 강의본 20장(t-통계로 유의성) — TE 2% · t 2는 프라이머 값을 재현하는 가정)"""
from s4kit import *
from math import sqrt

EQ = [f"eq/ep12_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.12 · 3년 성적이면 안다?", 860)


def cut2(t):
    body = (label("최근 3년 · 벤치마크 대비", 0, -110, 36, "#555", 800)
            + label("2024", -230, -30, 30, "#555", 800) + label("+1.2%p", -230, 25, 42, GREEN, 900)
            + label("2025", 0, -30, 30, "#555", 800) + label("+0.8%p", 0, 25, 42, GREEN, 900)
            + label("2026", 230, -30, 30, "#555", 800) + label("+1.0%p", 230, 25, 42, GREEN, 900)
            + label("펭: “3년 연속 이겼으니 실력!”", 0, 140, 40, NAVY, 900))
    return problem(t, "3년 연승!", GREEN, "#E9F1E4", "펭의 매니저 평가 메모 (예시)", body, ["3년 연속 이겼으면", "실력 맞죠?"], "실력 확정!")


def cut3(t): return twist(t, ["1%p 차이는 운으로도 3년쯤 나와.", "1년이면 4%p는 앞서야 운이 아니야."], "운일 수도!", size=44, sfx_size=160)


X0, X1, Y0, Y1 = 150, 940, 420, 780


def px(T, a): return X0 + (X1 - X0) * (T - 1) / 19, Y1 - (Y1 - Y0) * a / 4.4


def cut4(t):
    s = explainer_frame(t, "실력의 문턱", "t = IR × √T ≥ 2 · 추적오차 TE 2% (예시) — 몇 %p를 앞서야 운이 아닌가")
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{NAVY}" stroke-width="4"/>'
             f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{NAVY}" stroke-width="4"/>'
             + "".join(label(f"{T}년", px(T, 0)[0], Y1 + 30, 24, NAVY, 800) for T in (1, 4, 9, 16, 20))
             + label("필요한 연 초과수익", X0 + 10, Y0 - 20, 24, GREY, 800, anchor="start") + "</g>")
    g = ease_out(prog(t, .8, 1.6)); n = max(2, int(77 * g))
    pts = [px(1 + k * .25, 4 / sqrt(1 + k * .25)) for k in range(77)]
    curve = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts[:n])
    s.append(f'<polygon points="{X0},{Y1} {curve} {pts[n-1][0]:.0f},{Y1}" fill="{GREEN}" opacity=".12"/>')
    s.append(f'<polyline points="{curve}" fill="none" stroke="{RED}" stroke-width="7"/>')
    for T, lab in ((1, "4%p"), (4, "2%p"), (16, "1%p")):
        if t > .8 + 1.6 * (T - 1) / 19:
            x, y = px(T, 4 / sqrt(T)); s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{RED}"/>' + label(lab, x + 46, y - 22, 30, RED, 900))
    if t > 2.6:
        x, y = px(3, 1.0)
        s.append(f'<g opacity="{ease_out(prog(t, 2.6, .4)):.2f}"><circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{GREEN}"/>' + label("펭 매니저 3년 · 1%p", x + 20, y + 36, 26, GREEN, 900, anchor="start") + "</g>")
    s.append(chip("곡선 아래는 운과 구별이 안 되는 구간", 540, 880, NAVY, back(prog(t, 3.2, .4)), w=700, size=32))
    s += eqs(t, EQ, (945, 1045, 1150), a0=4.0, scale=(.5, .46, .44))
    s += explainer_tail(t, "짧은 기록으로는 실력과 운을 못 가른다", "3년 성적이면 안다? — 운으로도 나온다 (프라이머 오해 3)",
                        ["16년을 1%p씩 이겨야", "운이 아니라고 말할 수 있어."])
    return s


def cut5(t): return relief(t, ["그럼 매니저 평가는", "어떻게 해요?"], ["기간을 길게, 그리고 과정을 봐.", "어디서 벌었는지 쪼개 보는 거지."],
                           "과정을 봐!", "체크: 평가 기간 · 추적오차 · t-통계 · 초과수익의 출처", a_size=46, sfx_size=120)


def cut6(t): return next_cut(t, GREEN, "Brinson 분해", "+3.2%p는 어디서 왔나?", topic_size=170)


META = dict(
    episode="EP.12", title="3년 성적이면 안다?",
    concept="실력과 운의 구분 — 초과수익이 운이 아니라고 말하려면 t = IR × √T ≥ 2가 필요하다. 즉 α ≥ 2 × TE / √T: 추적오차 2%면 1년에 4%p, 4년이면 2%p, 16년이면 1%p를 꾸준히 앞서야 한다. 대부분의 펀드 평가는 이 문턱을 넘지 못한 짧은 기록으로 이뤄진다",
    source="W09 프라이머 13장(짧은 기록으로는 실력과 운을 가를 수 없다 — 1년치로 판단하려면 해마다 4%p는 앞서야 운이 아니라고 말할 수 있다, 대부분의 펀드 평가가 이 문턱을 넘지 못한다) · 14장(오해 3: 3년 성적이면 안다 — 운으로도 나온다) · 강의본 20장(Jensen α — t-통계로 유의성 검증)",
    cuts=[{"n": 2, "notice": "펭의 매니저 평가 메모(예시) · 최근 3년 벤치마크 대비 2024 +1.2%p · 2025 +0.8%p · 2026 +1.0%p · 펭: “3년 연속 이겼으니 실력!”", "bubble": ["3년 연속 이겼으면", "실력 맞죠?"], "sfx": "실력 확정!"},
          {"n": 3, "bubble": ["1%p 차이는 운으로도 3년쯤 나와.", "1년이면 4%p는 앞서야 운이 아니야."], "sfx": "운일 수도!"},
          {"n": 4, "curve": "필요 연 초과수익 = 2 × 2% / √T — 1년 4 · 4년 2 · 16년 1%p", "point": "펭 매니저 3년 · 1%p(곡선 아래)", "latex": ["t = IR × √T ≥ 2", "α ≥ 2 × TE / √T (TE = 2%)", "T = 1: 4%p, T = 4: 2%p, T = 16: 1%p"],
           "summary": "짧은 기록으로는 실력과 운을 못 가른다", "bubble": ["16년을 1%p씩 이겨야", "운이 아니라고 말할 수 있어."]},
          {"n": 5, "bubbles": [["그럼 매니저 평가는", "어떻게 해요?"], ["기간을 길게, 그리고 과정을 봐.", "어디서 벌었는지 쪼개 보는 거지."]], "sfx": "과정을 봐!"},
          {"n": 6, "text": ["다음 화", "Brinson 분해", "+3.2%p는 어디서 왔나?"]}],
    check={"T1": 4.0, "T4": 2.0, "T16": 1.0, "peng_t": 1.0 / 2 * 3 ** .5},
    **{"fact-check": "TE 2% · t ≥ 2는 프라이머 13장의 '1년이면 4%p'를 재현하는 가정(화면에 '예시' 표기)이며 프라이머 원 차트의 가정과 다를 수 있다. 펭 매니저 3년 성적(1.2 · 0.8 · 1.0%p)은 연출용 — TE 2%면 t = 0.5 × √3 ≈ 0.87로 2에 못 미친다. 정규 · 독립 가정."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "12", META)
