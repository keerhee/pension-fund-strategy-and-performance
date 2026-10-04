"""W01 EP.17 '정치와 운용 사이' — 운용 독립성(arm's length): 정치와 운용 사이의 제도적 분리. 네 차원 — 법적 형태 · 이사회 임명 · 운용 권한 · 개입 시계.
스펙트럼 위 상대 위치 NPS < KIC < GPFG < CPPIB. 거버넌스는 수익률의 함수가 아니라 선행 지표.
판정(케이스 덱): 4차원 중 3개 이상 충족 = 충분(CPPIB 4/4) · 1개 이하 = 낮음(NPS 0~1/4). (W01 강의본 36·37장 · 케이스 2·4·11장)"""
from wkit import *

TEX = [r"\mathrm{CPPIB}:\ 4/4 \;\geq\; 3 \;\Rightarrow\; \mathrm{sufficient}",
       r"\mathrm{NPS}:\ 0 \sim 1/4 \;\leq\; 1 \;\Rightarrow\; \mathrm{low}"]
EQ = [f"eq/ep17_{i}.png" for i in (1, 2)]
for _tex, _p in zip(TEX, EQ): latex_png(_tex, _p)


def cut1(t): return title(t, "EP.17 · 정치와 운용 사이", 860)


def cut2(t):
    body = (f'<rect x="-360" y="-135" width="340" height="190" rx="18" fill="#E3ECF7"/><rect x="20" y="-135" width="340" height="190" rx="18" fill="#E3ECF7"/>'
            + label("NPS 기금위원장", -190, -95, 32, BLUE, 900) + label("= 복지부 장관", -190, -40, 34, NAVY, 900) + label("위원 다수 정부 측", -190, 15, 26, "#555", 800)
            + label("CPPIB 이사회", 190, -95, 32, BLUE, 900) + label("연방 + 9개 주", 190, -40, 34, NAVY, 900) + label("전문가 이사회", 190, 15, 26, "#555", 800)
            + label("펭: “정부가 챙기면 든든하지!”", 0, 150, 36, BLUE, 900))
    return problem(t, "누가 정하나?", BLUE, "#E3ECF7", "같은 국민 돈, 다른 임명 구조", body,
                   ["정부가 직접 챙기면", "더 안전한 거 아니에요?"], "정부 최고?")


def cut3(t): return twist(t, ["정치 주기가 운용 주기를 흔들어.", "그래서 둘 사이에 거리를 두는 거야."], "거리 두기!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "독립성의 네 차원", "운용 독립성(arm's length) — 정치와 운용 사이의 제도적 분리", head_size=100)
    rows = [(["법적 형태", "정부 기관 · 중앙은행 부서", "독립 법인"], [NAVY, RED, GREEN]),
            (["이사회 임명", "정부가 다수 직접 임명", "다단계 추천"], [NAVY, RED, GREEN]),
            (["운용 권한", "배분도 정부 승인", "이사회 · CIO 자율"], [NAVY, RED, GREEN]),
            (["개입 시계", "매년 · 사안별", "5년+ 장기 mandate"], [NAVY, RED, GREEN])]
    s.append(table(t, .5, 3, [175, 470, 810], ["차원", "낮음 (개입 쉬움)", "높음 (개입 차단)"], rows, y0=390, dy=60, size=26, head_size=26))
    a = ease_out(prog(t, 3.0, .4))
    Y = 790
    s.append(f'<g opacity="{a:.2f}"><line x1="130" y1="{Y}" x2="930" y2="{Y}" stroke="{NAVY}" stroke-width="6"/>'
             f'<polygon points="930,{Y-14} 958,{Y} 930,{Y+14}" fill="{NAVY}"/>'
             + label("독립성 낮음", 150, Y + 42, 22, RED, 900, anchor="start") + label("높음", 950, Y + 42, 22, GREEN, 900, anchor="end") + "</g>")
    for i, (nm, x) in enumerate((("NPS", 230), ("KIC", 450), ("GPFG", 670), ("CPPIB", 880))):
        g = back(prog(t, 3.3 + .35 * i, .35))
        if g <= 0: continue
        c = [RED, ORANGE, TEAL, GREEN][i]
        s.append(f'<g transform="translate({x},{Y}) scale({g:.3f})"><circle r="17" fill="{c}"/>' + label(nm, 0, -44, 32, c, 900) + "</g>")
    s += eqs(t, EQ, (870, 965), a0=4.8, scale=(.44, .44))
    s.append(f'<g opacity="{ease_out(prog(t, 6.2, .5)):.2f}">' + label("판정(케이스 덱): 4차원 중 3개 이상 충족 = 충분 · 1개 이하 = 낮음", 540, 1085, 26, GREY, 800) + "</g>")
    s.append(chip("거버넌스는 수익률의 함수가 아니라 선행 지표", 540, 1185, GOLD, back(prog(t, 6.8, .4)), w=840, size=32))
    s += explainer_tail(t, "독립성은 느낌이 아니라 차원 수로 잰다", "IC 제2호 예고 — KIC TPA 도입, 독립성이 핵심 논거",
                        ["‘독립적이다’는 말보다", "몇 개를 갖췄는지가 중요해."], a0=8.0, red_size=46)
    return s


def cut5(t): return relief(t, ["NPS는 몇 개를", "갖췄어요?"], ["4차원 중 0~1개 — ‘낮음’이야.", "그래서 대체 15%도 조건을 따져야 해."],
                           "0~1 / 4!", "체크: 법적 형태 · 이사회 임명 · 운용 권한 · 개입 시계", a_size=44, sfx_size=120, chip_size=32)


def cut6(t): return next_cut(t, BLUE, "IC 보너스", "NPS 대체투자 15% — 유지? 상향? 하향?", topic_size=180)


META = dict(
    episode="EP.17", title="정치와 운용 사이",
    concept="운용 독립성(arm's length) — 정치적 주인과 운용 결정 사이의 제도적 분리. 법적 형태 · 이사회 임명 · 운용 권한 · 개입 시계 네 차원으로 재며, 스펙트럼 위 상대 위치는 NPS < KIC < GPFG < CPPIB. 케이스 덱 판정 기준(3개 이상 충족 = 충분 · 1개 이하 = 낮음)으로 CPPIB 4/4는 충분, NPS 0~1/4는 낮음. 거버넌스는 수익률의 선행 지표",
    source="W01 강의본 37장(운용 독립성 4차원 — 법적 형태 · 이사회 임명 · 운용 권한 · 개입 시계의 낮음/높음, 스펙트럼 NPS < KIC < GPFG < CPPIB, IC 제2호 예고) · 36장(거버넌스 스펙트럼, 수익률의 선행 지표) · 케이스 2 · 4장(운용자율권 CPPIB 4/4 · NPS 0~1/4, 3개 이상 = 충분 · 1개 이하 = 낮음) · 11장(NPS 기금위원장 = 복지부 장관 · 위원 다수 정부 측, CPPIB 연방 + 9개 주정부 공동 · 전문가 이사회) · 기획표 EP.17",
    cuts=[{"n": 2, "notice": "같은 국민 돈, 다른 임명 구조 · NPS 기금위원장 = 복지부 장관(위원 다수 정부 측) · CPPIB 이사회 연방 + 9개 주(전문가 이사회) · 펭: “정부가 챙기면 든든하지!”", "bubble": ["정부가 직접 챙기면", "더 안전한 거 아니에요?"], "sfx": "정부 최고?"},
          {"n": 3, "bubble": ["정치 주기가 운용 주기를 흔들어.", "그래서 둘 사이에 거리를 두는 거야."], "sfx": "거리 두기!"},
          {"n": 4, "table": {"법적 형태": "정부 기관 · 중앙은행 부서 vs 독립 법인", "이사회 임명": "정부가 다수 직접 임명 vs 다단계 추천", "운용 권한": "배분도 정부 승인 vs 이사회 · CIO 자율", "개입 시계": "매년 · 사안별 vs 5년+ 장기 mandate"},
           "spectrum": ["NPS", "KIC", "GPFG", "CPPIB"], "latex": ["CPPIB: 4/4 ≥ 3 ⇒ sufficient", "NPS: 0~1/4 ≤ 1 ⇒ low"], "chip": "거버넌스는 수익률의 함수가 아니라 선행 지표",
           "summary": "독립성은 느낌이 아니라 차원 수로 잰다", "bubble": ["‘독립적이다’는 말보다", "몇 개를 갖췄는지가 중요해."]},
          {"n": 5, "bubbles": [["NPS는 몇 개를", "갖췄어요?"], ["4차원 중 0~1개 — ‘낮음’이야.", "그래서 대체 15%도 조건을 따져야 해."]], "sfx": "0~1 / 4!"},
          {"n": 6, "text": ["다음 화", "IC 보너스", "NPS 대체투자 15% — 유지? 상향? 하향?"]}],
    check={"cppib_dims": "4/4", "nps_dims": "0~1/4", "threshold_sufficient": 3, "threshold_low": 1},
    **{"fact-check": "강의본 37장의 4차원(법적 형태 · 이사회 임명 · 운용 권한 · 개입 시계)과 케이스 덱 2 · 4 · 11장의 운용자율권 4차원(임명 구조 · mandate 주기 · 정치 개입 사례 · 예산 · 인력 자율)은 이름이 다르다 — 화면 표는 강의본, 점수(CPPIB 4/4 · NPS 0~1/4)와 판정 임계는 케이스 덱 기준임을 화면에 밝혔다. KIC · GPFG의 점수는 덱에 없어 스펙트럼 위 상대 위치만 표시. 임명 구조(복지부 장관 · 연방 + 9개 주)는 케이스 11장 표기, 법령 원문은 직접 확인하지 않음."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "17", META)
