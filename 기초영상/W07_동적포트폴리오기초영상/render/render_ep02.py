"""시즌 3 EP.02 '장기 투자는 안전하다?' — 시간분산의 양면. σ 17% 주식: 연환산 σ/√T 17 → 3.1%, 누적 σ√T 17 → 93% (√30 ≈ 5.5).
둘 다 옳다 — 장기 투자자가 물어야 할 것은 금액의 위험. (W07 M9 1교시 7·9·10·11장 그대로)"""
from s3kit import *
from math import sqrt

EQ = [f"eq/ep02_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.02 · 장기 투자는 안전하다?", 900)


def cut2(t):
    body = (label("투자서의 한 줄", 0, -110, 36, "#555", 800)
            + label("“30년 들고 있으면", 0, -40, 46, NAVY, 900) + label("주식 위험은 3%로 줄어든다”", 0, 25, 46, NAVY, 900)
            + label("주식 변동성 σ = 17% (연)", 0, 150, 36, BLUE, 900))
    return problem(t, "장기는 안전?", GREEN, "#E9F1E4", "펭이 밑줄 친 문장", body, ["30년만 버티면", "주식도 안전한 거죠?"], "밑줄 쫙!")


def cut3(t): return twist(t, ["비율로는 줄지만 금액으론 커져.", "30년 뒤 흔들림은 1년의 5.5배야."], "둘 다 옳다!", size=46, sfx_size=150)


def curve(t, a0, x0, y0, w, h, vmax, f, c, ttl, end_lbl, below=False):
    g = ease_out(prog(t, a0, 1.6))
    pts = [(x0 + w * (T - 1) / 29, y0 + h - h * f(T) / vmax) for T in range(1, 31)]
    n = max(2, int(30 * g))
    o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#F7F9FC" stroke="{GREY}" stroke-width="2"/>',
         label(ttl, x0 + w / 2, y0 - 32, 30, c, 900),
         label("1년", x0, y0 + h + 28, 24, GREY, 800), label("30년", x0 + w, y0 + h + 28, 24, GREY, 800)]
    if g > 0:
        o.append(f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts[:n])}" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"/>')
        o.append(f'<circle cx="{pts[0][0]:.0f}" cy="{pts[0][1]:.0f}" r="9" fill="{c}"/>' + label("17%", pts[0][0] + 40, pts[0][1] - 26, 28, c, 900))
    if g > .95:
        x, y = pts[-1]
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{c}"/>' + label(end_lbl, x - 60, y + (66 if below else -34), 36, c, 900))
    return "".join(o)


def cut4(t):
    s = explainer_frame(t, "비율 vs 금액", "σ = 17% 주식 · 1년 → 30년 (IID 가정)")
    s.append(curve(t, .6, 110, 420, 380, 360, 20, lambda T: 17 / sqrt(T), GREEN, "연환산 σ/√T — 줄어든다", "3.1%"))
    s.append(curve(t, 2.4, 590, 420, 380, 360, 100, lambda T: 17 * sqrt(T), RED, "누적 σ√T — 커진다", "93%", below=True))
    s.append(chip("평균 페이스는 안정 · 도착 지점은 5.5배 벌어진다", 540, 900, NAVY, back(prog(t, 4.2, .4)), w=860, size=32))
    s += eqs(t, EQ, (965, 1080, 1190), a0=5.0, scale=(.46, .46, .5))
    s += explainer_tail(t, "장기 투자자가 볼 것은 금액의 위험", "“장기는 안전”은 비율만 본 착각 — Samuelson의 반격",
                        ["마라톤 평균 속도는 안정돼도", "도착 시간 차는 더 벌어지잖아."])
    return s


def cut5(t): return relief(t, ["그럼 오래 들수록", "덜 위험한 건 아니에요?"], ["‘비율’은 줄지만 잃을 수 있는 ‘금액’은", "시간과 함께 커져. 둘을 섞으면 안 돼."],
                           "금액을 봐!", "체크: 연환산 σ · 누적 σ · 투자 기간 T", a_size=42)


def cut6(t): return next_cut(t, NAVY, "1969년 MIT", "젊을수록 주식을 늘려야 할까?", topic_size=170)


META = dict(
    episode="EP.02", title="장기 투자는 안전하다?",
    concept="시간분산의 양면 — IID 가정에서 연환산 변동성 σ/√T는 줄고 누적 변동성 σ√T는 커진다. 같은 σ로 '장기는 안전'과 '장기일수록 금액 위험이 크다'가 동시에 나온다. 논쟁의 본질은 측정 단위 — 장기 투자자는 금액의 위험을 봐야 한다",
    source="W07 M9 1교시 7·9·10·11장(마라톤의 함정, σ = 17% 주식: 연환산 17% → 3.1% 수렴 · 누적 17% → 93% 확대, 30년 총 변동성은 1년의 약 5.5배(√30 ≈ 5.5), Samuelson의 반격)",
    cuts=[{"n": 2, "notice": "펭이 밑줄 친 문장 · 투자서 “30년 들고 있으면 주식 위험은 3%로 줄어든다” · σ = 17%", "bubble": ["30년만 버티면", "주식도 안전한 거죠?"], "sfx": "밑줄 쫙!"},
          {"n": 3, "bubble": ["비율로는 줄지만 금액으론 커져.", "30년 뒤 흔들림은 1년의 5.5배야."], "sfx": "둘 다 옳다!"},
          {"n": 4, "curves": {"연환산 σ/√T": "17 → 3.1%", "누적 σ√T": "17 → 93%"}, "latex": ["σ/√T = 17%/√30 = 3.1%", "σ√T = 17% × √30 = 93%", "√30 ≈ 5.5"],
           "summary": "장기 투자자가 볼 것은 금액의 위험", "bubble": ["마라톤 평균 속도는 안정돼도", "도착 시간 차는 더 벌어지잖아."]},
          {"n": 5, "bubbles": [["그럼 오래 들수록", "덜 위험한 건 아니에요?"], ["‘비율’은 줄지만 잃을 수 있는 ‘금액’은", "시간과 함께 커져. 둘을 섞으면 안 돼."]], "sfx": "금액을 봐!"},
          {"n": 6, "text": ["다음 화", "1969년 MIT", "젊을수록 주식을 늘려야 할까?"]}],
    check={"annualized": 3.10, "cumulative": 93.1, "sqrt30": 5.48},
    **{"fact-check": "IID 로그수익률 가정(강의본 11장). 평균회귀가 있으면 결론이 달라진다(Campbell–Viceira, EP.04 · 강의본 51장). '투자서의 한 줄'은 연출용 문장. σ 17%는 강의본 10장의 예시 숫자."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "02", META)
