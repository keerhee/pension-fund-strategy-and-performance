"""W01 EP.03 '기다릴 수 있는 돈' — 인내자본. "오래 투자하는 돈"이 아니라 남들이 못 기다릴 때 기다릴 수 있는 돈.
역추세 매수: 본질가치 100이 위기에 70 → 사서 기다리면 100 ÷ 70 − 1 ≈ +43%(예시). 인내자본 = 긴 시계 + 낮은 유동성 압력 + 안정된 거버넌스.
(W01 강의본 6 · 10 · 11장 · 기획표 순서 3 그대로)"""
from wkit import *

TEX = [r"\frac{100}{70} - 1 = 0.429",
       r"\left(\frac{100}{70}\right)^{1/5} - 1 = 0.074"]
EQ = [f"eq/ep03_{i}.png" for i in (1, 2)]
for f, tx in zip(EQ, TEX):
    if len(sys.argv) > 1 or not os.path.exists(f): latex_png(tx, f)


def cut1(t): return title(t, "EP.03 · 기다릴 수 있는 돈", 820)


def cut2(t):
    body = (label("인내자본(patient capital)이란?", 0, -110, 36, "#555", 800)
            + punch("오래 투자하는 돈", 0, 0, 70, fill=TEAL, sw=9)
            + label("펭: “10년 들고 있으면 인내자본!”", 0, 150, 38, BLUE, 900))
    return problem(t, "오래 = 인내?", TEAL, "#E2F0EF", "펭의 투자 메모", body, ["오래 들고 있으면", "인내자본 아닌가요?"], "장기 보유!")


def cut3(t): return twist(t, ["오래가 아니라 기다릴 수 있는 거야.", "남들이 팔 때 사서 버티는 돈이지."], "버티는 돈!", size=44, sfx_size=150)


X0, X1, Y100, KY = 160, 920, 440, 7          # 가격 100의 y, 1당 픽셀
PTS = [(0, 100), (.18, 100), (.32, 84), (.42, 70), (.55, 74), (.72, 86), (.88, 96), (1, 100)]


def y_of(v): return Y100 + (100 - v) * KY


def cut4(t):
    s = explainer_frame(t, "70에 사서 100까지", "역추세 매수 — 위기 때 매도 압력이 없는 돈만 살 수 있다 (예시)")
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><line x1="{X0}" y1="{Y100}" x2="{X1}" y2="{Y100}" stroke="{GREEN}" stroke-width="4" stroke-dasharray="14 10"/>'
             + label("본질가치 100", X0 + (X1 - X0) * .55, Y100 - 30, 28, GREEN, 900)
             + f'<line x1="{X0}" y1="{y_of(64)}" x2="{X1}" y2="{y_of(64)}" stroke="{NAVY}" stroke-width="4"/>'
             + label("시간 →", X1 - 40, y_of(64) + 30, 24, NAVY, 800) + "</g>")
    d = " ".join(("M" if i == 0 else "L") + f" {X0 + (X1 - X0) * u:.0f} {y_of(v):.0f}" for i, (u, v) in enumerate(PTS))
    L = 1400; g = ease_out(prog(t, .8, 1.6))
    s.append(f'<path d="{d}" fill="none" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round" stroke-dasharray="{L}" stroke-dashoffset="{L*(1-g):.0f}"/>')
    xb = X0 + (X1 - X0) * .42
    if t > 1.6:
        b = back(prog(t, 1.6, .4))
        s.append(f'<g transform="translate({xb:.0f},{y_of(70):.0f}) scale({b:.3f})"><circle r="16" fill="{RED}"/></g>')
        s.append(f'<g opacity="{ease_out(prog(t, 1.6, .4)):.2f}">' + label("위기 · 70에 매수", xb - 150, y_of(70) + 8, 28, RED, 900) + "</g>")
    if t > 2.5:
        b = back(prog(t, 2.5, .4))
        s.append(f'<g transform="translate({X1},{Y100}) scale({b:.3f})"><circle r="16" fill="{GREEN}"/></g>')
    s.append(eq_img(EQ[0], 540, 725, ease_out(prog(t, 3.0, .5)), scale=.6))
    s.append(f'<g opacity="{ease_out(prog(t, 3.4, .4)):.2f}">' + label("≈ +43% — 사서 기다린 대가 (예시)", 540, 870, 30, GREEN, 900) + "</g>")
    s.append(eq_img(EQ[1], 540, 905, ease_out(prog(t, 4.0, .5)), scale=.55))
    s.append(f'<g opacity="{ease_out(prog(t, 4.4, .4)):.2f}">' + label("회복에 5년이 걸려도 연 7.4% (가정)", 540, 1050, 30, NAVY, 900) + "</g>")
    for i, (txt, c) in enumerate([("① 긴 시계 — 지급 부담이 먼 미래 (CPPIB 75년)", NAVY),
                                  ("② 낮은 유동성 압력 — 당장 팔 이유가 없다", BLUE),
                                  ("③ 안정된 거버넌스 — 정치 압력 · 단기 평가 없음", TEAL)]):
        s.append(chip(txt, 540, 1130 + 85 * i, c, back(prog(t, 5.0 + .5 * i, .4)), w=900, size=30))
    s += explainer_tail(t, "세 조건이 함께 있어야 기다릴 수 있다", "하나만 빠져도 30년 기관이 5년을 못 기다린다",
                        ["오래 굴리는 돈이 아니라,", "남들이 못 기다릴 때 기다리는 돈."], a0=7.0, red_size=44, owl_size=40)
    return s


def cut5(t): return relief(t, ["오래 굴리는 기관은", "다 할 수 있죠?"], ["조건 하나만 빠져도 못 버텨.", "CPPIB 사모 30%는 구조의 결과야."],
                           "구조가 먼저!", "체크: 긴 시계 · 낮은 유동성 압력 · 안정된 거버넌스", a_size=44, chip_size=32, sfx_size=110)


def cut6(t): return next_cut(t, GREEN, "GDP의 60%를 쥔 기관", "한국의 주인은 누구?", topic_size=110)


META = dict(
    episode="EP.03", title="기다릴 수 있는 돈",
    concept="인내자본 — “오래 투자하는 돈”이 아니라 남들이 못 기다릴 때 기다릴 수 있는 돈. 역추세 매수: 본질가치 100이 위기에 70이 될 때 사서 기다리면 100 ÷ 70 − 1 ≈ +43%(예시), 회복에 5년이 걸려도 연 7.4%(가정). 긴 시계 · 낮은 유동성 압력 · 안정된 거버넌스 세 조건이 함께 있어야 하며, 하나만 빠져도 30년 기관이 5년을 못 기다린다",
    source="W01 강의본 6장(정점인 세 이유 — 초장기 시간 지평, CPPIB “Time horizon is a competitive advantage”) · 10장(장기 자산소유자의 비교우위 여섯 후보 — ③ 역추세 매수 능력) · 11장(인내자본 — 본질가치 100이 위기에 70, 세 조건: 긴 시계(CPPIB 75년) · 낮은 유동성 압력 · 안정된 거버넌스, 하나만 빠져도 30년 기관이 5년을 못 기다린다, CPPIB 사모 30%는 구조의 결과) · 기획표 순서 3",
    cuts=[{"n": 2, "notice": "펭의 투자 메모 · 인내자본(patient capital)이란? · 오래 투자하는 돈 · 펭: “10년 들고 있으면 인내자본!”", "bubble": ["오래 들고 있으면", "인내자본 아닌가요?"], "sfx": "장기 보유!"},
          {"n": 3, "bubble": ["오래가 아니라 기다릴 수 있는 거야.", "남들이 팔 때 사서 버티는 돈이지."], "sfx": "버티는 돈!"},
          {"n": 4, "price_path(예시)": PTS, "latex": TEX, "labels": ["≈ +43% — 사서 기다린 대가 (예시)", "회복에 5년이 걸려도 연 7.4% (가정)"],
           "chips": ["① 긴 시계 — 지급 부담이 먼 미래 (CPPIB 75년)", "② 낮은 유동성 압력 — 당장 팔 이유가 없다", "③ 안정된 거버넌스 — 정치 압력 · 단기 평가 없음"],
           "summary": "세 조건이 함께 있어야 기다릴 수 있다", "bubble": ["오래 굴리는 돈이 아니라,", "남들이 못 기다릴 때 기다리는 돈."]},
          {"n": 5, "bubbles": [["오래 굴리는 기관은", "다 할 수 있죠?"], ["조건 하나만 빠져도 못 버텨.", "CPPIB 사모 30%는 구조의 결과야."]], "sfx": "구조가 먼저!"},
          {"n": 6, "text": ["다음 화", "GDP의 60%를 쥔 기관", "한국의 주인은 누구?"]}],
    check={"100/70-1": 0.4286, "(100/70)^(1/5)-1": 0.0739},
    **{"fact-check": "본질가치 100 → 위기 70은 강의본 11장의 예시 숫자(실제 자산 사례 아님). +43%는 100/70 − 1 = 42.9%의 반올림. '회복 5년 · 연 7.4%'는 이 화에서 덧붙인 가정 계산(강의본에 없음 — 사모 · 인프라는 5~10년 뒤 결과가 나온다는 11장 서술에 맞춘 설명용). CPPIB 75년 시계 · 사모 30%는 강의본 11장 표기(CPPIB 공시 원자료 직접 확인 안 함). 그래프 경로는 개념도."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "03", META)
