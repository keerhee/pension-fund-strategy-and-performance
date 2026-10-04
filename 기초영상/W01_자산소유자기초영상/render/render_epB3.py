"""W01 EP.B3 '어느 쪽이 옳은가?' — 케이스 핵심 질문. GPFG(부채 없음 · 비유동 약 2.5% · 총비용 약 5bp)와 CPPIB(75년 부채 · 사모 30%+ · 총비용 약 90bp) 모두 성공했다.
'어느 쪽이 옳은가'가 아니라 '우리 조건에서 어느 답이 정당화되나' — 미션(상한 vs 하한) · 운용자율권이 격차를 정당화. 총비용 격차 Δc = 85bp는 Ang 프리미엄 50~100bp 상단에서만 성립.
(케이스 덱 1·5·12·13·17·37·38장 · 강의본 23·31장) — 예고는 W02(자산배분과 CAPM)."""
from wkit import *

TEX = [r"\Delta c = 90 - 5 = 85\ \mathrm{bp}",
       r"\mathrm{premium}\ 50 \sim 100\ \mathrm{bp} \;\Rightarrow\; 85\ \mathrm{bp}\ \mathrm{only\ near\ the\ top}"]
EQ = [f"eq/epB3_{i}.png" for i in (1, 2)]
for _tex, _p in zip(TEX, EQ): latex_png(_tex, _p)


def next_week(t, color, l1, l2, question, size=150):
    s = [bg(color, "dotsW")]
    s.append(punch("다음 주 W02", 540, 500, 110, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch(l1, 540, 760, size, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch(l2, 540, 940, size, fill=YELLOW, scale=back(prog(t, .7, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label(question, 540, 1140, 54, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s


def cut1(t): return title(t, "EP.B3 · 어느 쪽이 옳은가?", 880)


def cut2(t):
    body = (f'<rect x="-360" y="-140" width="340" height="210" rx="18" fill="#FCE6DC"/><rect x="20" y="-140" width="340" height="210" rx="18" fill="#FCE6DC"/>'
            + label("GPFG", -190, -100, 38, ORANGE, 900) + label("비유동 2.5%", -190, -40, 34, NAVY, 900) + label("총비용 ~5bp", -190, 20, 34, NAVY, 900)
            + label("CPPIB", 190, -100, 38, ORANGE, 900) + label("사모 30%+", 190, -40, 34, NAVY, 900) + label("총비용 ~90bp", 190, 20, 34, NAVY, 900)
            + label("펭: “하나는 틀렸겠지!”", 0, 150, 36, BLUE, 900))
    return problem(t, "누가 맞나?", ORANGE, "#FCE6DC", "GPFG vs CPPIB — 정반대의 두 답", body,
                   ["정반대로 하는데", "둘 다 맞을 순 없잖아요?"], "정답은 하나?")


def cut3(t): return twist(t, ["둘 다 성공했어. 질문을 바꿔 —", "어떤 조건이 어느 답을 정당화하나."], "조건이 답!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "조건이 답을 가른다", "GPFG 대 CPPIB — 미션 · 자율권 · 비용을 나란히", head_size=100)
    rows = [(["미션", "세대 간 이전 · 부채 없음", "연금 부채 · 75년"], [NAVY, ORANGE, BLUE]),
            (["제약식", "쓰는 속도의 상한(3% 룰)", "벌어야 할 하한"], [NAVY, ORANGE, BLUE]),
            (["운용자율권", "적정 (중앙은행 산하)", "충분 (독립 법인)"], [NAVY, ORANGE, BLUE]),
            (["비유동 비중", "약 2.5%", "사모 30%+"], [NAVY, ORANGE, BLUE]),
            (["총비용", "약 5bp", "약 90bp"], [NAVY, ORANGE, BLUE])]
    s.append(table(t, .5, 3, [165, 450, 800], ["항목", "GPFG", "CPPIB"], rows, y0=390, dy=58, size=26, head_size=28))
    s += eqs(t, EQ, (735, 835), a0=3.8, scale=(.46, .42))
    s.append(chip("“CPPIB 30bp vs GPFG 5bp”는 운영비만 비교 — 감점", 540, 970, RED, back(prog(t, 5.2, .4)), w=900, size=29))
    s.append(f'<g opacity="{ease_out(prog(t, 5.6, .4)):.2f}">' + label("CPPIB 운영비 26bp · 총비용 ~90bp (FY2025) — 비교는 총비용끼리", 540, 1045, 25, GREY, 800) + "</g>")
    s.append(chip("공통 골격: 자율권이 비중을 정당화 · 자율권은 지표로 잰다", 540, 1170, GREEN, back(prog(t, 6.2, .4)), w=960, size=29))
    s += explainer_tail(t, "정답이 아니라 조건 — 재어 볼 수 있는 조건", "부채의 하한이 있는 쪽만 사모 30%를 정당화한다",
                        ["‘CPPIB가 옳다’가 아니라", "‘이 지표면 CPPIB의 길’이야."], a0=8.0, red_size=44)
    return s


def cut5(t): return relief(t, ["그럼 우리 NPS는", "어느 길이에요?"], ["미션은 CPPIB형, 체계는 GPFG형이야.", "그 비대칭을 조건으로 풀어야 해."],
                           "비대칭!", "체크: 미션 · 자율권 · 장기자본 · 비용 산수", a_size=44, sfx_size=130)


def cut6(t): return next_week(t, NAVY, "자산배분과", "CAPM", "무엇에 얼마를 담나?", size=150)


META = dict(
    episode="EP.B3", title="어느 쪽이 옳은가?",
    concept="케이스의 핵심 질문 — GPFG(부채 없음 · 비유동 약 2.5% · 총비용 약 5bp)와 CPPIB(75년 연금 부채 · 사모 30%+ · 총비용 약 90bp)는 정반대의 답으로 모두 성공했다. 질문은 '어느 쪽이 옳은가'가 아니라 '어떤 조건이 어느 답을 정당화하나'. 부채가 있는 쪽만 '벌어야 할 하한'을 갖고, 독립 법인의 운용자율권이 비유동 비중을 정당화한다. 총비용 격차 Δc = 85bp는 Ang의 프리미엄 50~100bp 상단에서만 성립 — 운영비(26bp)만 비교하면 틀린다. 공통 골격: 자율권이 비중을 정당화하고, 자율권은 지표로 잰다",
    source="W01 케이스 덱 1 · 5장(핵심 질문 — 어느 쪽이 옳은가가 아니라 어떤 조건이 어느 답을 정당화하나) · 12장(두 주인공 — 주식 70 · 채권 27.5 · 실물 2.5 / 사모 30+, 총비용 약 5bp / 운영비 26bp · 총비용 약 90bp) · 13장(미션의 정량화 — 3% 룰 '쓰는 속도의 상한' vs 요구수익률 '벌어야 하는 수익의 하한') · 17장(Δc ≈ 85bp, Ang 50~100bp) · 37장('CPPIB 30bp vs GPFG 5bp'는 운영비만 비교한 감점 발언) · 38장(공통 골격) · 20장(NPS 체계는 GPFG형, 배분 목표는 CPPIB 방향) · 강의본 23 · 31장 · 기획표 EP.B3",
    cuts=[{"n": 2, "notice": "GPFG vs CPPIB — 정반대의 두 답 · GPFG 비유동 2.5% · 총비용 ~5bp · CPPIB 사모 30%+ · 총비용 ~90bp · 펭: “하나는 틀렸겠지!”", "bubble": ["정반대로 하는데", "둘 다 맞을 순 없잖아요?"], "sfx": "정답은 하나?"},
          {"n": 3, "bubble": ["둘 다 성공했어. 질문을 바꿔 —", "어떤 조건이 어느 답을 정당화하나."], "sfx": "조건이 답!"},
          {"n": 4, "table": {"미션": "세대 간 이전 · 부채 없음 vs 연금 부채 · 75년", "제약식": "쓰는 속도의 상한(3% 룰) vs 벌어야 할 하한", "운용자율권": "적정(중앙은행 산하) vs 충분(독립 법인)", "비유동 비중": "약 2.5% vs 사모 30%+", "총비용": "약 5bp vs 약 90bp"},
           "latex": ["Δc = 90 − 5 = 85 bp", "premium 50~100 bp ⇒ 85 bp only near the top"], "chips": ["“CPPIB 30bp vs GPFG 5bp”는 운영비만 비교 — 감점", "공통 골격 — 자율권이 비중을 정당화하고, 자율권은 지표로 잰다"],
           "summary": "정답이 아니라 조건 — 재어 볼 수 있는 조건", "bubble": ["‘CPPIB가 옳다’가 아니라", "‘이 지표면 CPPIB의 길’이야."]},
          {"n": 5, "bubbles": [["그럼 우리 NPS는", "어느 길이에요?"], ["미션은 CPPIB형, 체계는 GPFG형이야.", "그 비대칭을 조건으로 풀어야 해."]], "sfx": "비대칭!"},
          {"n": 6, "text": ["다음 주 W02", "자산배분과 CAPM", "무엇에 얼마를 담나?"]}],
    check={"delta_c": 85},
    **{"fact-check": "기획표와 강의본 31장은 CPPIB 비용을 '~30bp(총비용 기준)', GPFG를 '5~7bp'로 적었으나 케이스 덱 12 · 17 · 37 · 41장은 'CPPIB 약 30bp는 운영비(26bp)뿐 — 총비용 약 90bp, GPFG 총비용 약 5bp'이며 30bp vs 5bp 비교를 감점 발언으로 지목한다. B3의 주 원자료인 케이스 덱을 따라 총비용 90bp vs 5bp(격차 85bp)로 표기했다. 모든 수치는 덱 표기(NBIM · CPPIB 연차보고서 원문 직접 확인 안 함). 예고 질문 '무엇에 얼마를 담나?'는 W02 주제(자산배분과 CAPM)에 맞춰 새로 쓴 문구 — 기획표에는 'W02 예고'만 있다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "B3", META)
