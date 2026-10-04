"""W01 EP.14 '물가에서 인구를 뺀다' — 자동조정장치(2024 정부안). 인상률 = 물가 − 가입자 감소 − 기대여명 증가(최근 3년 평균):
3.0% − 1.0% − 0.3% = 1.7% → 월 100만 원 → 101.7만 원. 명목 삭감은 없다(최소 인상률 0.31% 하한) — 물가 인상분을 인구구조만큼 덜 얹을 뿐.
발동 시점 2036 · 2049 · 2054 — 이를수록 재정 효과도, 기존 · 근접 수급자의 감소분도 크다. 2025 개정에는 빠졌다. (W01 강의본 42·43장 그대로)"""
from wkit import *

TEX = [r"r = \pi - \Delta N - \Delta e = 3.0\% - 1.0\% - 0.3\% = 1.7\%",
       r"100 \times 1.017 = 101.7 \quad \mathrm{vs} \quad 100 \times 1.030 = 103.0",
       r"103.0 - 101.7 = 1.3 \quad (\mathrm{nominal\ cut} = 0)"]
EQ = [f"eq/ep14_{i}.png" for i in (1, 2, 3)]
for _tex, _p in zip(TEX, EQ): latex_png(_tex, _p)


def next2(t, color, l1, l2, question, size=150):
    """next_cut의 두 줄 제목판(긴 회차 제목용)."""
    s = [bg(color, "dotsW")]
    s.append(punch("다음 화", 540, 500, 120, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch(l1, 540, 760, size, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch(l2, 540, 940, size, fill=YELLOW, scale=back(prog(t, .7, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label(question, 540, 1140, 54, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s


def cut1(t): return title(t, "EP.14 · 물가에서 인구를 뺀다", 900)


def cut2(t):
    body = (label("2024 연금개혁 정부안", 0, -110, 36, "#555", 800)
            + label("반대 측의 이름", 0, -40, 38, NAVY, 900) + punch("“자동삭감장치”", 0, 50, 80, fill=RED, sw=10)
            + label("펭: “내 연금이 줄어든다고?”", 0, 165, 38, BLUE, 900))
    return problem(t, "연금이 깎인다?", RED, "#F5E1E1", "펭의 뉴스 스크랩 · 자동조정장치", body,
                   ["자동조정장치 생기면", "제 연금 깎이는 거예요?"], "삭감 공포!", mood_after="shock")


def cut3(t): return twist(t, ["명목 금액은 안 깎여. 물가만큼 올리던 걸", "인구만큼 덜 올리는 거야."], "덜 올린다!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "물가 − 인구 = 인상률", "자동조정장치 — 명목 삭감이 아니라 인상률 조정 (2024 정부안 예시)", head_size=96)
    base, k = 700, 80          # 1%p = 80px
    bars = [("물가상승률", 0, 3.0, BLUE, "+3.0%"), ("가입자 감소", 3.0, 2.0, RED, "−1.0%p"),
            ("기대여명 증가", 2.0, 1.7, ORANGE, "−0.3%p"), ("인상률", 0, 1.7, GREEN, "1.7%")]
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="110" y1="{base}" x2="970" y2="{base}" stroke="{NAVY}" stroke-width="4"/></g>')
    for i, (nm, lo, hi, c, v) in enumerate(bars):
        g = ease_out(prog(t, .6 + .6 * i, .45))
        if g <= 0: continue
        x = 220 + 215 * i
        y0, y1 = base - lo * k, base - hi * k
        top, h = min(y0, y1), abs(y1 - y0) * g
        yy = top if hi >= lo else top
        s.append(f'<g opacity="{g:.2f}"><rect x="{x-70}" y="{yy:.0f}" width="140" height="{h:.0f}" rx="6" fill="{c}"/>'
                 + label(v, x, min(y0, y1) - 28, 32, c, 900) + label(nm, x, base + 34, 26, NAVY, 900) + "</g>")
        if 0 < i < 3:   # 연결 점선
            s.append(f'<line x1="{x-215+70}" y1="{base-lo*k:.0f}" x2="{x-70}" y2="{base-lo*k:.0f}" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6" opacity="{g:.2f}"/>')
    s.append(chip("명목 삭감은 없다 — 최소 인상률 0.31% 하한", 540, 820, GREEN, back(prog(t, 3.2, .4)), w=820, size=32))
    s += eqs(t, EQ, (900, 1015, 1125), a0=3.9, scale=(.44, .42, .42))
    s.append(f'<g opacity="{ease_out(prog(t, 6.2, .5)):.2f}">' + label("π 물가 · ΔN 가입자 감소 · Δe 기대여명 증가 · 월 100만 원 기준(예시, 만 원)", 540, 1250, 25, GREY, 800) + "</g>")
    s += explainer_tail(t, "인구충격을 공식으로 세대 간에 나눈다", "2025 개정에는 빠졌다 — 쟁점은 장기 실질가치의 하락 폭",
                        ["깎는 게 아니라", "덜 올리는 거야."], a0=7.0)
    return s


def cut5(t): return relief(t, ["그럼 언제", "발동돼요?"], ["후보가 셋이야. 2036 · 2049 · 2054년 —", "이를수록 재정 효과도, 수급자 감소분도 커."],
                           "시점이 쟁점!", "체크: 물가 − 가입자 감소 − 기대여명 · 하한 0.31%", a_size=42, sfx_size=110)


def cut6(t): return next2(t, "#6B3FA0", "왜 오른 것을", "더 샀나", "무엇이 수익률을 앞서나?", size=140)


META = dict(
    episode="EP.14", title="물가에서 인구를 뺀다",
    concept="자동조정장치 — 인구충격을 미리 정한 공식으로 세대 간에 나누는 규칙. 연금 인상률을 물가상승률에서 가입자 감소율과 기대여명 증가분(최근 3년 평균)만큼 뺀다: 3.0% − 1.0% − 0.3% = 1.7%, 월 100만 원 → 101.7만 원(현행 103만 원). 명목 삭감은 없고(최소 인상률 0.31% 하한) 장기 실질가치가 덜 오를 뿐. 발동 시점 후보 2036 · 2049 · 2054년, 2025 개정에는 빠졌다",
    source="W01 강의본 43장(자동조정장치 — 현행 물가 연동 vs 개정안 인상률 = 물가 − 가입자 감소 − 기대여명 증가, 예 3.0% − 1.0% − 0.3% = 1.7% · 월 100만 원 → 101.7만 원, 최소 인상률 0.31% 하한, 발동 2036 · 2049 · 2054, 찬성 세대 간 위험공유 · 반대 “자동삭감장치”) · 42장(2025 합의는 도입 보류) · 기획표 EP.14",
    cuts=[{"n": 2, "notice": "펭의 뉴스 스크랩 · 자동조정장치 · 2024 연금개혁 정부안 · 반대 측의 이름 “자동삭감장치” · 펭: “내 연금이 줄어든다고?”", "bubble": ["자동조정장치 생기면", "제 연금 깎이는 거예요?"], "sfx": "삭감 공포!"},
          {"n": 3, "bubble": ["명목 금액은 안 깎여. 물가만큼 올리던 걸", "인구만큼 덜 올리는 거야."], "sfx": "덜 올린다!"},
          {"n": 4, "waterfall": {"물가상승률": 3.0, "가입자 감소": -1.0, "기대여명 증가": -0.3, "인상률": 1.7}, "chip": "명목 삭감은 없다 — 최소 인상률 0.31% 하한",
           "latex": ["r = π − ΔN − Δe = 3.0% − 1.0% − 0.3% = 1.7%", "100 × 1.017 = 101.7 vs 100 × 1.030 = 103.0", "103.0 − 101.7 = 1.3 (nominal cut = 0)"],
           "summary": "인구충격을 공식으로 세대 간에 나눈다", "bubble": ["깎는 게 아니라", "덜 올리는 거야."]},
          {"n": 5, "bubbles": [["그럼 언제", "발동돼요?"], ["후보가 셋이야. 2036 · 2049 · 2054년 —", "이를수록 재정 효과도, 수급자 감소분도 커."]], "sfx": "시점이 쟁점!"},
          {"n": 6, "text": ["다음 화", "왜 오른 것을 더 샀나", "무엇이 수익률을 앞서나?"]}],
    check={"rate": 1.7, "pension": 101.7, "gap_vs_current": 1.3},
    **{"fact-check": "공식 · 예시 숫자(3.0 − 1.0 − 0.3 = 1.7%, 100 → 101.7만 원) · 0.31% 하한 · 발동 시점 세 후보는 강의본 43장 그대로(2024 정부안의 예시 — 실제 변수 값은 해마다 다름). 현행 103만 원 비교와 차이 1.3만 원은 같은 예시에서 계산한 값. 발동 시점의 정의(2036 급여지출 > 보험료수입 · 2049 기금 감소 5년 전 · 2054 기금 감소 시작)는 덱 표기, 정부안 원문은 직접 확인하지 않음."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "14", META)
