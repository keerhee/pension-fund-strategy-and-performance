"""시즌 4 EP.06 '끝값이 같은 두 펀드' — Sharpe(1966) = 초과수익 ÷ 총 변동성. 같은 연 9%(무위험 3%)라도 σ 12%면 0.50, σ 24%면 0.25(예시).
기준: 0.5 미만 부진 · 0.5–1.0 양호 · 1.0+ 우수 · 2.0+ 예외적(먼저 의심). (W09 프라이머 7·8장 · 강의본 18·22장 — 펀드 B σ 24%는 예시)"""
from s4kit import *
import math

EQ = [f"eq/ep06_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.06 · 끝값이 같은 두 펀드", 860)


def cut2(t):
    body = (f'<rect x="-350" y="-130" width="330" height="190" rx="18" fill="#E9F1E4"/><rect x="20" y="-130" width="330" height="190" rx="18" fill="#FBE9E9"/>'
            + label("가 펀드", -185, -85, 38, GREEN, 900) + label("연 9% · σ 12%", -185, -20, 34, NAVY, 900)
            + label("나 펀드", 185, -85, 38, RED, 900) + label("연 9% · σ 24%", 185, -20, 34, NAVY, 900)
            + label("펭: “수익이 같으니 둘 다 같은 점수”", 0, 130, 36, NAVY, 900))
    return problem(t, "둘 다 9%!", GREEN, "#E9F1E4", "펭의 펀드 비교표 (예시)", body, ["수익률이 똑같으니", "둘 다 똑같이 좋은 거죠?"], "동점!")


def cut3(t): return twist(t, ["같은 곳에 닿아도 크게 출렁였으면", "값이 낮아. 위험 1단위당 몫을 봐."], "출렁임도 값!", size=44, sfx_size=150)


X0, X1, YM = 120, 960, 600


def path(t, a0, amp, c, ph):
    g = ease_out(prog(t, a0, 1.4)); n = max(2, int(80 * g))
    pts = [(X0 + (X1 - X0) * k / 79, YM + 120 - 240 * k / 79 - amp * math.sin(k / 79 * 6 * math.pi + ph) * math.sin(k / 79 * math.pi)) for k in range(80)]
    return f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts[:n])}" fill="none" stroke="{c}" stroke-width="7" stroke-linejoin="round"/>'


def cut4(t):
    s = explainer_frame(t, "Sharpe 비율", "같은 끝값 · 다른 길 — 변동성 1단위당 초과수익 (무위험 3%)")
    s.append(path(t, .5, 25, GREEN, 0))
    s.append(path(t, 1.6, 110, RED, 1.2))
    s.append(f'<g opacity="{ease_out(prog(t, .5, .4)):.2f}"><circle cx="{X0}" cy="{YM+120}" r="12" fill="{NAVY}"/><circle cx="{X1}" cy="{YM-120}" r="12" fill="{NAVY}"/>'
             + label("출발", X0 + 10, YM + 160, 28, NAVY, 900) + label("같은 끝값", X1 - 60, YM - 160, 28, NAVY, 900) + "</g>")
    s.append(chip("가 펀드(A) 0.50", 300, 820, GREEN, back(prog(t, 3.0, .4)), w=320, size=34))
    s.append(chip("나 펀드(B) 0.25", 780, 820, RED, back(prog(t, 3.4, .4)), w=320, size=34))
    s += eqs(t, EQ, (880, 1000, 1110), a0=4.2, scale=(.5, .46, .42))
    s += explainer_tail(t, "같은 수익도 흔들림이 크면 값이 낮다", "0.5 미만 부진 · 1.0+ 우수 · 2.0+면 먼저 의심하라",
                        ["나 펀드는 같은 9%를 벌려고", "두 배의 위험을 썼어."])
    return s


def cut5(t): return relief(t, ["그런데 오를 때 출렁인 것도", "위험이에요?"], ["Sharpe는 그렇게 셈해.", "그게 억울하면 다음 화의 Sortino야."],
                           "억울한 벌점?", "체크: 초과수익 · 총 변동성 σ · 무위험 수익률 · 평가 기간", a_size=46, sfx_size=110)


def cut6(t): return next_cut(t, TEAL, "Sortino", "오르는 흔들림까지 벌점?", topic_size=200)


META = dict(
    episode="EP.06", title="끝값이 같은 두 펀드",
    concept="Sharpe 비율(1966) — 변동성 1단위당 초과수익 (E[Rp] − Rf)/σp. 끝값(수익)이 같아도 크게 출렁이며 도착한 펀드는 값이 낮다. 기준: 0.5 미만 부진 · 0.5–1.0 양호 · 1.0+ 우수 · 2.0+ 예외적(먼저 의심)",
    source="W09 프라이머 7·8장(끝값이 같아도 두 펀드의 값은 다르다 — 가 펀드는 얌전히, 나 펀드는 크게 출렁이며 같은 곳에, 변동성 한 단위당 번 몫) · 강의본 18장(Sharpe 기준) · 22장(연 9% · σ 12% → (9 − 3)/12 = 0.50)",
    cuts=[{"n": 2, "notice": "펭의 펀드 비교표(예시) · 가 펀드 연 9% · σ 12% / 나 펀드 연 9% · σ 24% · 펭: “수익이 같으니 둘 다 같은 점수”", "bubble": ["수익률이 똑같으니", "둘 다 똑같이 좋은 거죠?"], "sfx": "동점!"},
          {"n": 3, "bubble": ["같은 곳에 닿아도 크게 출렁였으면", "값이 낮아. 위험 1단위당 몫을 봐."], "sfx": "출렁임도 값!"},
          {"n": 4, "paths": "같은 출발 · 같은 끝값 · 가(얌전) vs 나(크게 출렁)", "chips": ["가 펀드(A) 0.50", "나 펀드(B) 0.25"], "latex": ["Sharpe = (E[Rp] − Rf)/σp", "A: (9 − 3)/12 = 0.50, B: (9 − 3)/24 = 0.25", "<0.5 weak, 0.5–1.0 good, 1.0+ strong"],
           "summary": "같은 수익도 흔들림이 크면 값이 낮다", "bubble": ["나 펀드는 같은 9%를 벌려고", "두 배의 위험을 썼어."]},
          {"n": 5, "bubbles": [["그런데 오를 때 출렁인 것도", "위험이에요?"], ["Sharpe는 그렇게 셈해.", "그게 억울하면 다음 화의 Sortino야."]], "sfx": "억울한 벌점?"},
          {"n": 6, "text": ["다음 화", "Sortino", "오르는 흔들림까지 벌점?"]}],
    check={"A": 0.5, "B": 0.25},
    **{"fact-check": "가 펀드(연 9% · σ 12%)는 강의본 22장 예제 펀드, 나 펀드 σ 24%는 대비용 예시. 두 경로는 개념도(사인파)이며 실제 수익률 데이터가 아니다. 무위험 3%는 강의본 22장 가정."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "06", META)
