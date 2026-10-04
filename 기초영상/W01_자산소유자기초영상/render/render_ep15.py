"""W01 EP.15 '왜 오른 것을 더 샀나' — CalPERS 2000년 닷컴. 1999 S&P +21% · Nasdaq +86%의 광기 속에 이사회 의사록 “기술주 비중이 낮다, 늘려야 한다”
→ 2000 초 확대 → 2000–02 Nasdaq −78%. 2009 적립비율 63%(역사적 최저). 2003 독립 감사의 네 결함 → 2004 개혁.
좋은 의사결정의 4요소 — 전문 이사회 · 독립적 CIO · 문서화된 프로세스 · 외부 검증. (W01 강의본 32·41장 그대로)"""
from wkit import *

TEX = [r"100 \times (1 + 0.86) = 186",
       r"186 \times (1 - 0.78) = 40.9 \quad \Rightarrow \quad 40.9 / 100 - 1 = -59\%"]
EQ = [f"eq/ep15_{i}.png" for i in (1, 2)]
for _tex, _p in zip(TEX, EQ): latex_png(_tex, _p)


def cut1(t): return title(t, "EP.15 · 왜 오른 것을 더 샀나", 900)


def cut2(t):
    body = (label("1999 · Nasdaq 한 해 상승률", 0, -110, 36, "#555", 800)
            + punch("+86%", 0, -15, 104, fill=GREEN, sw=12)
            + label("“기술주 비중이 낮다,", 0, 105, 36, NAVY, 900) + label("늘려야 한다”", 0, 160, 36, NAVY, 900))
    return problem(t, "다들 샀는데?", GREEN, "#E3F1E8", "CalPERS 이사회 의사록 · 1999", body,
                   ["오르는 걸 더 사는 게", "뭐가 문제예요?"], "더 사자!")


def cut3(t): return twist(t, ["결과보다 나쁜 건 근거가 없었다는 거야.", "‘왜 사나’가 의사록에 한 줄도 없었지."], "근거 0줄!", size=44, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "꼭대기에서 산 대가", "Nasdaq 지수 100 가정 — 1999년 +86%, 2000–02년 −78%", head_size=96)
    def Y(v): return 690 - v * 1.45
    pts = [(200, 100, "1999 초", "100"), (500, 186, "1999 말", "186"), (860, 40.9, "2002", "40.9")]
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="120" y1="{Y(0):.0f}" x2="960" y2="{Y(0):.0f}" stroke="{NAVY}" stroke-width="4"/>'
             f'<line x1="120" y1="{Y(100):.0f}" x2="960" y2="{Y(100):.0f}" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>'
             + label("출발점 100", 960, Y(100) - 22, 22, GREY, 800, anchor="end") + "</g>")
    for i in range(2):
        g = ease_out(prog(t, .8 + 1.0 * i, .8))
        if g <= 0: continue
        (x0, v0, *_), (x1, v1, *_) = pts[i], pts[i + 1]
        xe, ve = x0 + (x1 - x0) * g, v0 + (v1 - v0) * g
        s.append(f'<line x1="{x0}" y1="{Y(v0):.0f}" x2="{xe:.0f}" y2="{Y(ve):.0f}" stroke="{GREEN if i == 0 else RED}" stroke-width="9" stroke-linecap="round"/>')
    for i, (x, v, yr, txt) in enumerate(pts):
        g = ease_out(prog(t, .5 + 1.0 * i, .4))
        if g <= 0: continue
        dy = -40 if i < 2 else 40
        s.append(f'<g opacity="{g:.2f}"><circle cx="{x}" cy="{Y(v):.0f}" r="13" fill="{NAVY}"/>'
                 + label(txt, x + (0 if i != 1 else 0), Y(v) + dy, 32, NAVY, 900) + label(yr, x, Y(0) + 32, 26, NAVY, 900) + "</g>")
    if t > 2.0:
        g = back(prog(t, 2.0, .4))
        s.append(f'<g transform="translate(730,388) rotate(6) scale({g:.3f})"><rect x="-150" y="-36" width="300" height="72" rx="14" fill="none" stroke="{RED}" stroke-width="6"/>'
                 + label("여기서 더 샀다", 0, 0, 32, RED, 900) + "</g>")
    s.append(chip("2009 적립비율 63% — 역사적 최저", 540, 790, RED, back(prog(t, 3.0, .4)), w=700, size=34))
    s += eqs(t, EQ, (860, 960), a0=3.6, scale=(.46, .44))
    four = ["전문 이사회", "독립적 CIO", "문서화된 프로세스", "외부 검증"]
    s.append(f'<g opacity="{ease_out(prog(t, 5.4, .4)):.2f}">' + label("좋은 의사결정의 4요소 (2003 독립 감사 → 2004 개혁)", 540, 1110, 28, NAVY, 900) + "</g>")
    for i, nm in enumerate(four):
        g = back(prog(t, 5.8 + .35 * i, .35))
        if g <= 0: continue
        x, y = 300 + 480 * (i % 2), 1190 + 95 * (i // 2)
        s.append(f'<g transform="translate({x},{y}) scale({g:.3f})"><rect x="-220" y="-38" width="440" height="76" rx="16" fill="{TEAL}"/>'
                 + label(f"{'①②③④'[i]} {nm}", 0, 0, 32, "#fff", 900) + "</g>")
    s += explainer_tail(t, "좋은 결정 = 근거가 기록된 결정", "결과가 아니라 과정(근거 기록)을 감사한다",
                        ["‘왜 샀나’에 답할", "기록이 없었던 거야."], a0=8.0)
    return s


def cut5(t): return relief(t, ["그 뒤엔 어떻게", "고쳤어요?"], ["2004 · 2017 개혁으로 CIO 권한을 보강했어.", "2025엔 미국 최초로 TPA 전환을 선언했고."],
                           "구조를 고쳤다!", "체크: 전문 이사회 · 독립 CIO · 문서화 · 외부 검증", happy=True, a_size=42, sfx_size=110)


def cut6(t): return next_cut(t, RED, "34년의 증명", "성공한 개혁은?", topic_size=150)


META = dict(
    episode="EP.15", title="왜 오른 것을 더 샀나",
    concept="근거가 기록되지 않은 결정 — CalPERS 2000년 닷컴. 1999년 Nasdaq +86%의 광기 속에 이사회는 “기술주 비중이 낮다, 늘려야 한다”며 비중을 키웠고 2000–02년 Nasdaq −78%로 큰 손실, 2009년 적립비율은 역사적 최저 63%. 지수 100 가정이면 꼭대기 186에서 40.9까지 — 출발점 대비 −59%. 2003 독립 감사가 지적한 결함(전문성 부족 · 모멘텀 추종 · CIO 권한 부족 · 독립성 부재)의 처방이 좋은 의사결정의 4요소다",
    source="W01 강의본 41장(1999 S&P +21% · Nasdaq +86%, 이사회 의사록 “기술주 비중이 낮다, 늘려야 한다”, 2000 초 확대 → 2000–02 Nasdaq −78%, 2003 독립 감사의 네 결함 → 2004 개혁, 좋은 의사결정의 4요소) · 32장(2009 적립비율 63% 역사적 최저 · 2025 미국 최초 TPA 전환 선언) · 36장(2004 · 2017 개혁으로 CIO 권한 보강) · 기획표 EP.15",
    cuts=[{"n": 2, "notice": "CalPERS 이사회 의사록 · 1999 · Nasdaq 한 해 상승률 +86% · “기술주 비중이 낮다, 늘려야 한다”", "bubble": ["오르는 걸 더 사는 게", "뭐가 문제예요?"], "sfx": "더 사자!"},
          {"n": 3, "bubble": ["결과보다 나쁜 건 근거가 없었다는 거야.", "‘왜 사나’가 의사록에 한 줄도 없었지."], "sfx": "근거 0줄!"},
          {"n": 4, "line": {"1999 초": 100, "1999 말": 186, "2002": 40.9}, "stamp": "여기서 더 샀다", "chip": "2009 적립비율 63% — 역사적 최저",
           "latex": ["100 × (1 + 0.86) = 186", "186 × (1 − 0.78) = 40.9 ⇒ 40.9/100 − 1 = −59%"], "four": ["전문 이사회", "독립적 CIO", "문서화된 프로세스", "외부 검증"],
           "summary": "좋은 결정 = 근거가 기록된 결정", "bubble": ["‘왜 샀나’에 답할", "기록이 없었던 거야."]},
          {"n": 5, "bubbles": [["그 뒤엔 어떻게", "고쳤어요?"], ["2004 · 2017 개혁으로 CIO 권한을 보강했어.", "2025엔 미국 최초로 TPA 전환을 선언했고."]], "sfx": "구조를 고쳤다!"},
          {"n": 6, "text": ["다음 화", "34년의 증명", "성공한 개혁은?"]}],
    check={"peak": 186, "trough": 40.92, "vs_start": -0.5908},
    **{"fact-check": "Nasdaq +86%(1999) · −78%(2000–02) · 2009 적립비율 63% · 의사록 문구는 강의본 41 · 32장 표기(원자료 미확인). 지수 100 가정의 경로(100 → 186 → 40.9)는 화면용 예시로, −78%는 2000–02 고점 대비 하락폭을 1999년 말 수준에 그대로 적용한 단순화다. CalPERS의 실제 손실 규모(덱 '수조 원')는 넣지 않았다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "15", META)
