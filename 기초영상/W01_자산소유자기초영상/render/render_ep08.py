"""W01 EP.08 'Yale의 산수' — 엔다우먼트. 영구 자본의 목표 수익률 = 지출 4~5% + 물가 2~3% = 7~8%.
Swensen의 Yale 모델: 1985 취임 시 미국 주식 · 채권 70% → 2008 대체 70% · 그해 −24% → 30년 연환산 11.1% · 기금 $42B.
'부채 없음'이 가장 공격적인 배분을 허락한다. (W01 강의본 20장 · 기획표 순서 8)"""
import os
from wkit import *

TEX = [r"r_{\mathrm{target}} = \mathrm{spending} + \mathrm{inflation} = 4.5\% + 2.5\% = 7.0\%",
       r"100 \times (1 - 0.24) = 76"]
EQ = [f"eq/ep08_{i + 1}.png" for i in range(len(TEX))]
for _f, _t in zip(EQ, TEX):
    if not os.path.exists(_f) or (len(sys.argv) > 1 and sys.argv[1] == "stills"): latex_png(_t, _f)

STEPS = [("1985", "Swensen 취임", "미국 주식 · 채권 70%", BLUE),
         ("2008", "대체 70%", "위기의 해 −24%", RED),
         ("30년", "연환산 11.1%", "기금 $42B", GREEN)]


def cut1(t): return title(t, "EP.08 · Yale의 산수", 760)


def cut2(t):
    body = (label("2008년 Yale 기금 배분", 0, -110, 36, "#555", 800)
            + label("사모 · 실물 · 헤지펀드", 0, -45, 36, NAVY, 900) + punch("대체 70%", 0, 45, 92, fill=RED, sw=11)
            + label("펭: “주식 · 채권은 겨우 30%?”", 0, 160, 38, BLUE, 900))
    return problem(t, "너무 공격적?", RED, "#F6E4E4", "펭의 대학 기금 리포트", body, ["대체투자를 70%나?", "너무 위험하지 않아요?"], "도박?!")


def cut3(t): return twist(t, ["갚아야 할 부채가 없으니까.", "영구 자본은 기다릴 수 있어."], "부채 없음!", size=48, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "Yale의 산수", "영구 자본의 목표 — 지출 4~5% + 물가 2~3% = 7~8%")
    # 왼쪽: 목표 수익률 쌓기 막대 (예시 4.5 + 2.5), 1%p = 60px
    base, k = 860, 60
    for i, (nm, v, c, a0) in enumerate([("지출", 4.5, NAVY, .5), ("물가", 2.5, ORANGE, 1.1)]):
        g = ease_out(prog(t, a0, .5)); h = v * k * g
        y0 = base - (0 if i == 0 else 4.5 * k)
        s.append(f'<rect x="130" y="{y0 - h:.0f}" width="230" height="{h:.0f}" fill="{c}"/>')
        if g > .8: s.append(label(nm, 245, y0 - v * k / 2 - 20, 34, "#fff", 900) + label(f"{v}%", 245, y0 - v * k / 2 + 22, 32, "#fff", 900))
    a = ease_out(prog(t, 1.6, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("목표 7% (예시)", 245, 395, 34, RED, 900)
             + f'<line x1="110" y1="{base}" x2="380" y2="{base}" stroke="{NAVY}" stroke-width="5"/></g>')
    # 오른쪽: 성적표 세 칸
    for i, (yr, l1, l2, c) in enumerate(STEPS):
        g = back(prog(t, 2.0 + .5 * i, .4))
        if g <= 0: continue
        y = 470 + 150 * i
        s.append(f'<g transform="translate(700,{y}) scale({g:.3f})"><rect x="-290" y="-58" width="580" height="116" rx="18" fill="{c}"/>'
                 + label(yr, -205, 0, 40, YELLOW, 900) + label(l1, 70, -20, 30, "#fff", 900) + label(l2, 70, 22, 26, "#fff", 800) + "</g>")
        if i > 0 and g > .5:
            s.append(f'<polygon points="688,{y - 92} 712,{y - 92} 700,{y - 72}" fill="{NAVY}"/>')
    s += eqs(t, EQ, (925, 1060), a0=4.0, scale=(.44, .46))
    s.append(f'<g opacity="{ease_out(prog(t, 4.4, .4)):.2f}">' + label("가정: 지출 4.5% · 물가 2.5%", 540, 1020, 26, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 5.2, .4)):.2f}">' + label("가정: 기금 100 · 2008년 −24% → 팔지 않고 회복을 기다린다", 540, 1150, 26, GREY, 800) + "</g>")
    s.append(chip("위기에도 모델을 바꾸지 않았다", 540, 1265, NAVY, back(prog(t, 6.0, .4)), w=700, size=34))
    s += explainer_tail(t, "‘부채 없음’이 가장 공격적인 배분을 허락한다", "Swensen의 네 기둥 — 주식 지향 · 비효율 시장 알파 · 장기 파트너 · 대체 최대 70%",
                        ["갚을 돈이 없으니", "−24%에도 팔 필요가 없었지."], a0=7.0, red_size=44)
    return s


def cut5(t): return relief(t, ["우리 연기금도", "따라 하면요?"], ["연기금은 매달 연금을 줘야 해.", "부채가 있으면 같은 배분은 못 하지."],
                           "조건이 달라!", "체크: 지출률 · 물가 · 영구 지평 · 부채 없음", a_size=44, sfx_size=110)


def cut6(t): return next_cut(t, "#5B3F8C", "석유를 주식으로", "청구권자 없는 돈은?", topic_size=124)


META = dict(
    episode="EP.08", title="Yale의 산수",
    concept="엔다우먼트의 목표 수익률은 산수로 정해진다 — 지출 4~5% + 물가 2~3% = 7~8%(영구 유지). 갚아야 할 부채가 없는 영구 자본이라 Yale은 대체투자를 70%까지 늘렸고, 2008년 −24%에도 모델을 바꾸지 않아 30년 연환산 11.1%를 냈다. '부채 없음'이 가장 공격적인 배분을 허락한다. 매달 연금을 지급해야 하는 연기금은 같은 배분을 그대로 따라 할 수 없다",
    source="W01 강의본 20장(엔다우먼트 — Yale 모델의 산수: Swensen의 네 기둥 ① 주식 지향 ② 비효율 시장 알파 ③ 외부 매니저 장기 파트너십 ④ 대체 최대 70% · 1985 취임 시 미국 주식 · 채권 70% · 2008 대체 70% · 위기의 해 −24% · 30년 연환산 11.1% · 기금 $42B · 지출 4~5% + 영구 유지 = 목표 7~8%) · 14장 표(엔다우먼트 — 부채 없음, 영구 지출 4~5%, 대체 40~70%) · 기획표 순서 8",
    cuts=[{"n": 2, "notice": "펭의 대학 기금 리포트 · 2008년 Yale 기금 배분 · 사모 · 실물 · 헤지펀드 · 대체 70% · 펭: “주식 · 채권은 겨우 30%?”", "bubble": ["대체투자를 70%나?", "너무 위험하지 않아요?"], "sfx": "도박?!"},
          {"n": 3, "bubble": ["갚아야 할 부채가 없으니까.", "영구 자본은 기다릴 수 있어."], "sfx": "부채 없음!"},
          {"n": 4, "bar": {"지출": "4.5% (예시)", "물가": "2.5% (예시)", "목표": "7%"}, "steps": [f"{a} — {b} · {c}" for a, b, c, _ in STEPS],
           "latex": ["r_target = spending + inflation = 4.5% + 2.5% = 7.0%", "100 × (1 − 0.24) = 76 (가정: 기금 100) → 팔지 않고 회복을 기다린다"],
           "chip": "위기에도 모델을 바꾸지 않았다", "summary": "‘부채 없음’이 가장 공격적인 배분을 허락한다", "bubble": ["갚을 돈이 없으니", "−24%에도 팔 필요가 없었지."]},
          {"n": 5, "bubbles": [["우리 연기금도", "따라 하면요?"], ["연기금은 매달 연금을 줘야 해.", "부채가 있으면 같은 배분은 못 하지."]], "sfx": "조건이 달라!"},
          {"n": 6, "text": ["다음 화", "석유를 주식으로", "청구권자 없는 돈은?"]}],
    check={"target": 7.0, "after_2008": 76},
    **{"fact-check": "지출 4~5% · 목표 7~8% · 대체 70% · 2008 −24% · 30년 연환산 11.1% · $42B는 강의본 20장 표기(Yale 연차보고서 원자료는 직접 확인하지 않음). 물가 2~3%는 기획표 표기(강의본 20장은 '지출 4~5% + 영구 유지'로만 씀) — 화면의 4.5% · 2.5% · 기금 100은 예시. 2008년 −24%는 Yale 회계연도(FY2009, 2009.6 종료) 기준으로 흔히 인용되는 값 — 기억 기반. '1985 → 2021'의 30년 구간 정의는 덱 표기 그대로."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "08", META)
