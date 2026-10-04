"""W01 EP.B2 'KIC TPA의 세 조건' — 케이스 IC 제2호. TPA 도입은 이미 결정(2026 시범 → 2027 정식) — 도입 '여부'가 아니라 '조건' 세 개를 표결한다.
(i) 비유동 상한: 회수 시나리오 연동 25~30% 출발, 5년 PME > 1.0 3년 연속 + 공동투자 20%면 +5%p · (ii) 비용: 내부 역량(직접 · 공동투자)에 한정, 외부 수수료 증가 불허
· (iii) 척도: RP 대비 순부가가치 5년 롤링, 사모는 평활화 보정. 'TPA 도입 = 30bp'는 인과 오류. (케이스 덱 4·5·28~32·38장)"""
from wkit import *

TEX = [r"25\% + 5\%\mathrm{p} = 30\% \qquad 30\% + 5\%\mathrm{p} = 35\%",
       r"\mathrm{premium} + \alpha_{\mathrm{access}} \;\geq\; \Delta c = 85\ \mathrm{bp}"]
EQ = [f"eq/epB2_{i}.png" for i in (1, 2)]
for _tex, _p in zip(TEX, EQ): latex_png(_tex, _p)

CONDS = [("(i) 비유동 상한", "회수 시나리오 연동 — 25~30%에서 출발", ORANGE),
         ("(ii) 비용 범위", "내부 역량(직접 · 공동투자)만 — 외부 수수료 증가 불허", BLUE),
         ("(iii) 성과 척도", "RP 대비 순부가가치 5년 롤링 — 사모는 평활화 보정", TEAL)]


def next2(t, color, l1, l2, question, size=150):
    s = [bg(color, "dotsW")]
    s.append(punch("다음 화", 540, 500, 120, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch(l1, 540, 760, size, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch(l2, 540, 940, size, fill=YELLOW, scale=back(prog(t, .7, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label(question, 540, 1140, 54, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s


def cut1(t): return title(t, "EP.B2 · KIC TPA의 세 조건", 880)


def cut2(t):
    body = (label("KIC 자산 (2025말)", 0, -110, 36, "#555", 800)
            + punch("$2,320억", 0, -20, 96, fill=TEAL, sw=12)
            + label("대체 21.9% · TPA 2026 시범 → 2027 정식", 0, 85, 32, NAVY, 900)
            + label("펭: “TPA 하면 비용 30bp래!”", 0, 155, 36, BLUE, 900))
    return problem(t, "TPA 찬반?", TEAL, "#DDEFEE", "IC 제2호 · KIC TPA 도입", body,
                   ["TPA를 할지 말지", "표결하는 거죠?"], "도입 찬반?")


def cut3(t): return twist(t, ["도입은 이미 정해졌어. 표결할 건", "얼마나 · 얼마에 · 무엇으로 재느냐야."], "조건 셋!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "TPA 하의 세 조건", "도입은 전제 — 상한 · 비용 · 척도를 표결한다", head_size=100)
    for i, (nm, d, c) in enumerate(CONDS):
        g = back(prog(t, .5 + .6 * i, .4))
        if g <= 0: continue
        y = 430 + 118 * i
        s.append(f'<g transform="translate(540,{y}) scale({g:.3f})"><rect x="-450" y="-50" width="900" height="100" rx="18" fill="{c}"/>'
                 + label(nm, 0, -20, 32, "#fff", 900) + label(d, 0, 22, 25, "#fff", 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 2.8, .4)):.2f}">' + label("(i)의 증거 연동 상향 — 5년 PME > 1.0이 3년 연속 + 공동투자 20%면 +5%p", 540, 815, 26, NAVY, 900) + "</g>")
    s += eqs(t, EQ, (845, 1000), a0=3.3, scale=(.44, .44))
    s.append(f'<g opacity="{ease_out(prog(t, 4.6, .4)):.2f}">' + label("(ii)의 비용 산수 — Δc = CPPIB 총비용 ~90bp − GPFG ~5bp", 540, 970, 26, NAVY, 900) + "</g>")
    s.append(chip("“TPA 도입 = 30bp”는 인과 오류 — 비용은 사모 · 내부 조직의 함수", 540, 1165, RED, back(prog(t, 5.6, .4)), w=960, size=27))
    s.append(chip("KIC 자율권: NPS보다 높고 CPPIB보다 낮다 → 상한도 그 사이", 540, 1265, NAVY, back(prog(t, 6.3, .4)), w=960, size=28))
    s += explainer_tail(t, "α는 사전에 증명할 수 없다", "그래서 상한을 α의 증거가 쌓이는 속도에 연동한다",
                        ["증거가 쌓이는 만큼만", "상한을 올려."], a0=8.0)
    return s


def cut5(t): return relief(t, ["국내 투자 불가는", "약점 아니에요?"], ["오히려 정치 개입 통로 하나를 막아 줘.", "법적 제약은 상한을 정하는 변수야."],
                           "제약 = 변수!", "체크: 비유동 상한 · 비용 범위 · 성과 척도", happy=True, a_size=44, sfx_size=120)


def cut6(t): return next2(t, TEAL, "어느 쪽이", "옳은가?", "두 기관의 공통 골격은?", size=160)


META = dict(
    episode="EP.B2", title="KIC TPA의 세 조건",
    concept="IC 제2호 — KIC의 TPA 도입은 이미 결정된 전제(2026 시범 → 2027 정식)이므로 도입 여부가 아니라 조건 셋을 표결한다: (i) 비유동 상한 — 위탁기관 회수 시나리오에 연동해 25~30%에서 출발, 5년 PME > 1.0이 3년 연속 + 공동투자 20%면 +5%p(25 → 30 → 35%) · (ii) 비용 — 접근권 α를 만드는 내부 역량에 한정, 외부 수수료 증가 불허(프리미엄 + α ≥ Δc 85bp) · (iii) 척도 — RP 대비 순부가가치 5년 롤링, 사모는 평활화 보정. 'TPA 도입 = 30bp'는 프레임과 비용의 혼동",
    source="W01 케이스 덱 4장(제2호 조건 ①~③ — 비유동 25~30% 출발 · PME > 1.0 3년 + 공동투자 20%면 +5%p, 외부 수수료 증가 불허, RP 대비 순부가가치 5년 롤링 · 평활화 보정) · 5장(TPA 도입 자체는 전제 — 승인 + 조건 3개) · 28장(KIC $2,320억 · 대체 21.9% · 2026 시범 → 2027 정식 · 자율권 NPS < KIC < CPPIB · 'TPA 도입 = 30bp'는 인과 오류) · 29장(표결 질문 [25/30/35]%) · 30장(국내 투자 불가가 정치 개입 통로를 막는다 · 법적 제약은 상한 변수) · 31장(프리미엄 + α ≥ 85bp) · 32장(상한의 논리 — α > 0은 사전에 증명할 수 없다) · 기획표 EP.B2",
    cuts=[{"n": 2, "notice": "IC 제2호 · KIC TPA 도입 · KIC 자산(2025말) $2,320억 · 대체 21.9% · TPA 2026 시범 → 2027 정식 · 펭: “TPA 하면 비용 30bp래!”", "bubble": ["TPA를 할지 말지", "표결하는 거죠?"], "sfx": "도입 찬반?"},
          {"n": 3, "bubble": ["도입은 이미 정해졌어. 표결할 건", "얼마나 · 얼마에 · 무엇으로 재느냐야."], "sfx": "조건 셋!"},
          {"n": 4, "conditions": [c[0] + " — " + c[1] for c in CONDS], "latex": ["25% + 5%p = 30%, 30% + 5%p = 35%", "premium + α_access ≥ Δc = 85 bp"],
           "chips": ["“TPA 도입 = 30bp”는 인과 오류 — 비용은 사모 · 내부 조직의 함수", "KIC 자율권: NPS보다 높고 CPPIB보다 낮다 → 상한도 그 사이"],
           "summary": "α는 사전에 증명할 수 없다", "bubble": ["증거가 쌓이는 만큼만", "상한을 올려."]},
          {"n": 5, "bubbles": [["국내 투자 불가는", "약점 아니에요?"], ["오히려 정치 개입 통로 하나를 막아 줘.", "법적 제약은 상한을 정하는 변수야."]], "sfx": "제약 = 변수!"},
          {"n": 6, "text": ["다음 화", "어느 쪽이 옳은가?", "두 기관의 공통 골격은?"]}],
    check={"cap_steps": [25, 30, 35], "delta_c": 85},
    **{"fact-check": "KIC 수치($2,320억 · 21.9%, 2025 실적 · 2026.2 발표)와 조건 3개는 케이스 덱 표기(KIC 공시 원문은 직접 확인 안 함). 상한 단계 25 → 30 → 35%는 덱 29장 표결 선택지[25/30/35]와 32장 '+5%p' 규칙을 이어 계산한 예시 — 덱은 몇 번까지 올릴 수 있는지 정하지 않았다. 덱 31장의 'α ≥ 30bp (중앙값 75bp에서 성립하려면)'은 85 − 75 = 10과 맞지 않아 화면에 넣지 않았다(부등식만 표기). 기획표의 'RP'는 Reference Portfolio."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "B2", META)
