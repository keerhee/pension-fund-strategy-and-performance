"""W01 EP.B1 'NPS 대체투자 15%' — 케이스 IC 제1호. '15% 로드맵 승인'은 이미 의결된 계획의 재승인이라 결정이 아니다 — 트리거를 표결한다.
판정 조건 ① 운용자율권 0~1/4 낮음 · ② 장기자본 약속 충족(2040년대 전환) · ③ 접근권 GP 의존 ~90% 미충족 · ④ 비용 Δc 85bp vs 프리미엄 중앙값 75bp 빠듯
→ 상향도 하향도 정당화 안 됨 — 15% 유지 + 상향(20%) · 하향(12%) 트리거. (케이스 덱 4·5·17·21·22·38장)"""
from wkit import *

TEX = [r"\Delta c = 90 - 5 = 85\ \mathrm{bp}",
       r"\Delta c - \bar{p} = 85 - 75 = 10\ \mathrm{bp} \;\Rightarrow\; \alpha_{\mathrm{access}} \geq 10\ \mathrm{bp}"]
EQ = [f"eq/epB1_{i}.png" for i in (1, 2)]
for _tex, _p in zip(TEX, EQ): latex_png(_tex, _p)


def next2(t, color, l1, l2, question, size=150):
    s = [bg(color, "dotsW")]
    s.append(punch("다음 화", 540, 500, 120, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch(l1, 540, 760, size, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch(l2, 540, 940, size, fill=YELLOW, scale=back(prog(t, .7, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label(question, 540, 1140, 54, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s


def cut1(t): return title(t, "EP.B1 · NPS 대체투자 15%", 880)


def cut2(t):
    body = (label("NPS 대체투자 비중 (2026.6)", 0, -110, 36, "#555", 800)
            + punch("14.0%", 0, -20, 100, fill=GOLD, sw=12)
            + label("2030 목표 15% · CPPIB는 사모 30%+", 0, 85, 34, NAVY, 900)
            + label("펭: “CPPIB만큼 올리자!”", 0, 155, 36, BLUE, 900))
    return problem(t, "15%, 올려?", GOLD, "#FBF1DD", "IC 제1호 · NPS 대체투자 2030 목표", body,
                   ["CPPIB처럼 30%까지", "확 올리면 안 돼요?"], "더 올려!")


def cut3(t): return twist(t, ["‘올릴까 내릴까’를 정하지 마.", "언제 올리고 언제 내릴지를 표결해."], "트리거 표결!", size=46, sfx_size=140)


def cut4(t):
    s = explainer_frame(t, "조건 넷을 대입하라", "제1호 판정 조건 ①~④ — 지표와 임계를 표결 전에 박는다", head_size=96)
    rows = [(["① 운용자율권", "3/4 이상", "0~1/4", "낮음"], [NAVY, GREY, NAVY, RED]),
            (["② 장기자본 약속", "전환 10년+", "2040년대", "충족"], [NAVY, GREY, NAVY, GREEN]),
            (["③ 접근권 역량", "GP 의존 ≤ 80%", "~90%", "미충족"], [NAVY, GREY, NAVY, RED]),
            (["④ 비용 산수", "Δc ≤ 75bp", "85bp", "빠듯"], [NAVY, GREY, NAVY, ORANGE])]
    s.append(table(t, .5, 4, [205, 470, 690, 880], ["조건", "임계", "NPS", "판정"], rows, y0=390, dy=60, size=27, head_size=26))
    s += eqs(t, EQ, (700, 795), a0=3.2, scale=(.46, .44))
    s.append(f'<g opacity="{ease_out(prog(t, 4.6, .5)):.2f}">' + label("Δc = CPPIB 총비용 ~90bp − GPFG ~5bp · 75bp = 비유동성 프리미엄 중앙값(Ang 50~100bp)", 540, 908, 21, GREY, 800) + "</g>")
    for i, (txt, c) in enumerate((("↑ 상향 20% — 조건 ① + ③ 충족이 확인되면", GREEN),
                                  ("= 유지 15% — 지금 조건의 기본 답", NAVY),
                                  ("↓ 하향 12% — 조건 ④ 불성립(5년 PME < 1.0) 시", RED))):
        s.append(chip(txt, 540, 990 + 92 * i, c, back(prog(t, 5.2 + .5 * i, .4)), w=900, size=30))
    if t > 6.8:
        s.append(punch("유지 + 트리거", 790, 1270, 56, fill=YELLOW, scale=back(prog(t, 6.8, .4)), rot=-6, sw=8))
    s += explainer_tail(t, "표결 대상은 비중이 아니라 트리거", "평가 주기 3년 · 트리거 조건을 기금위 의결문에 명문화",
                        ["올릴 근거도, 내릴 근거도", "아직 없어 — 유지 + 트리거."], a0=8.0)
    return s


def cut5(t): return relief(t, ["트리거는 누가", "판정해요?"], ["외부평가가 3년 주기로 판정하고,", "그 지표는 공시해야 해."],
                           "공시로 판정!", "체크: 자율권 · 장기자본 · 접근권 · 비용 산수", happy=True, a_size=46, sfx_size=120)


def cut6(t): return next2(t, GOLD, "KIC TPA의", "세 조건", "KIC는?", size=150)


META = dict(
    episode="EP.B1", title="NPS 대체투자 15%",
    concept="IC 제1호 — NPS 2030 대체투자 목표 15%. 이미 의결된 계획의 재승인은 결정이 아니므로 '올릴까 내릴까'가 아니라 트리거를 표결한다. 판정 조건 ① 운용자율권 0~1/4(낮음) · ② 장기자본 약속 충족 · ③ GP 의존 ~90%(미충족) · ④ 총비용 격차 Δc 85bp vs 프리미엄 중앙값 75bp(빠듯 — 접근권 α가 10bp 이상 있어야 성립)를 대입하면 상향도 하향도 정당화되지 않는다 → 15% 유지 + 상향(20%, ① + ③ 충족 시) · 하향(12%, ④ 불성립 시) 트리거",
    source="W01 케이스 덱 4장(판정 조건 한눈에 — 조건 ①~④의 지표 · 임계 · 케이스 대입) · 5장(기본 답 15% 유지 + 상향 · 하향 트리거) · 17장(비용 프레임 — CPPIB 운영비 26bp · 총비용 ≈ 90bp · GPFG ≈ 5bp · 격차 ≈ 85bp, Ang 50~100bp) · 20장(대체투자 260.9조 원 · 14.0%, 2026.6) · 21장(표결 질문 — 20% 상향 · 12% 하향 트리거, 평가 주기 3년) · 22장(판정 조건 4개) · 26장(외부평가 3년 주기 · 지표 공시) · 38장(모범답안) · 기획표 EP.B1",
    cuts=[{"n": 2, "notice": "IC 제1호 · NPS 대체투자 2030 목표 · NPS 대체투자 비중(2026.6) 14.0% · 2030 목표 15% · CPPIB는 사모 30%+ · 펭: “CPPIB만큼 올리자!”", "bubble": ["CPPIB처럼 30%까지", "확 올리면 안 돼요?"], "sfx": "더 올려!"},
          {"n": 3, "bubble": ["‘올릴까 내릴까’를 정하지 마.", "언제 올리고 언제 내릴지를 표결해."], "sfx": "트리거 표결!"},
          {"n": 4, "table": {"① 운용자율권": "3/4 이상 · NPS 0~1/4 · 낮음", "② 장기자본 약속": "전환 10년+ · 2040년대 · 충족", "③ 접근권 역량": "GP 의존 ≤ 80% · ~90% · 미충족", "④ 비용 산수": "Δc ≤ 75bp · 85bp · 빠듯"},
           "latex": ["Δc = 90 − 5 = 85 bp", "Δc − p̄ = 85 − 75 = 10 bp ⇒ α_access ≥ 10 bp"],
           "chips": ["↑ 상향 20% — 조건 ① + ③ 충족이 확인되면", "= 유지 15% — 지금 조건의 기본 답", "↓ 하향 12% — 조건 ④ 불성립(5년 PME < 1.0) 시"], "stamp": "유지 + 트리거",
           "summary": "표결 대상은 비중이 아니라 트리거", "bubble": ["올릴 근거도, 내릴 근거도", "아직 없어 — 유지 + 트리거."]},
          {"n": 5, "bubbles": [["트리거는 누가", "판정해요?"], ["외부평가가 3년 주기로 판정하고,", "그 지표는 공시해야 해."]], "sfx": "공시로 판정!"},
          {"n": 6, "text": ["다음 화", "KIC TPA의 세 조건", "KIC는?"]}],
    check={"delta_c": 85, "gap_vs_median": 10},
    **{"fact-check": "모든 수치 · 임계는 케이스 덱 표기(NPS 2026.6 잠정 · CPPIB FY2025 연차보고 · Ang 2014 — 원자료 직접 확인 안 함). 'α ≥ 10bp'는 덱 31장의 순 초과수익 조건(프리미엄 + α ≥ Δc)에 중앙값 75bp를 넣어 계산한 값이다. 덱 31장은 같은 자리에 'α ≥ 30bp (중앙값 75bp에서 성립하려면)'라고 적어 85 − 75 = 10과 맞지 않는다 — 화면은 산수대로 10bp. 상향 트리거의 구체 지표(mandate 주기 법제화 + 공동투자 20%)는 38장 모범답안이라 화면에는 조건 번호로만 표기."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "B1", META)
