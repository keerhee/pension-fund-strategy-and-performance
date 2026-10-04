"""시즌 4 EP.01 '위험이 얼마예요?' — 위험의 네 정의. σ는 흩어짐(상승도 벌점) · VaR는 경계선 · CVaR는 그 너머 꼬리의 평균 · MDD는 고점 대비 낙폭.
비유: 홍수 경계선 · 넘친 뒤의 수심 · 최저점의 상처. (W09 강의본 7·8·9장 · 프라이머 4·5장 · 기획표 EP01_Cuts 그대로)"""
from s4kit import *
from math import exp

EQ = [f"eq/ep01_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.01 · 위험이 얼마예요?", 820)


def cut2(t):
    body = (label("글로벌 주식형 펀드 · 연간 보고", 0, -110, 36, "#555", 800)
            + label("연 변동성 σ", 0, -40, 40, NAVY, 900) + punch("12%", 0, 40, 84, fill=GREEN, sw=10)
            + label("위험 등급: 낮음 ✓", 0, 155, 40, GREEN, 900))
    return problem(t, "위험 낮음!", GREEN, "#E9F1E4", "펭의 펀드 보고서", body, ["σ가 12%면", "위험은 다 잰 거죠?"], "다 쟀다!")


def cut3(t): return twist(t, ["‘위험이 얼마냐’는 질문이 덜 끝났어.", "무엇을 재느냐에 따라 답이 넷이야."], "질문이 넷!", size=44, sfx_size=160)


def cut4(t):
    s = explainer_frame(t, "위험의 네 얼굴", "같은 펀드도 무엇을 재느냐에 따라 위험이 달라진다")
    # 왼쪽: 분포 + VaR 선 + 꼬리
    X0, X1, YB = 100, 560, 700
    pts = [(X0 + (X1 - X0) * k / 60, YB - 230 * exp(-((k - 33) / 10.0) ** 2 / 2)) for k in range(61)]
    g = ease_out(prog(t, .5, .8)); n = max(2, int(61 * g))
    s.append(f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts[:n])}" fill="none" stroke="{NAVY}" stroke-width="6"/>')
    s.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{NAVY}" stroke-width="3" opacity="{g:.2f}"/>')
    if t > 1.5:
        a = ease_out(prog(t, 1.5, .4)); vx = X0 + (X1 - X0) * 16.5 / 60
        tail = [p for p in pts if p[0] <= vx]
        s.append(f'<g opacity="{a:.2f}"><polygon points="{X0},{YB} {" ".join(f"{x:.0f},{y:.0f}" for x, y in tail)} {vx:.0f},{YB}" fill="{RED}" opacity=".35"/>'
                 f'<line x1="{vx:.0f}" y1="{YB-200}" x2="{vx:.0f}" y2="{YB}" stroke="{RED}" stroke-width="5"/>'
                 + label("VaR", vx + 8, YB - 215, 30, RED, 900, anchor="start") + label("CVaR = 꼬리 평균", X0 + 10, YB + 30, 26, RED, 900, anchor="start")
                 + f'<line x1="{X0+(X1-X0)*23/60:.0f}" y1="{YB-120}" x2="{X0+(X1-X0)*43/60:.0f}" y2="{YB-120}" stroke="{TEAL}" stroke-width="5"/>'
                 + label("σ 흩어짐", X0 + (X1 - X0) * 33 / 60, YB - 145, 28, TEAL, 900) + "</g>")
    # 오른쪽: 낙폭
    PX = [(600, 600), (660, 520), (720, 470), (780, 560), (840, 650), (900, 590), (960, 500)]
    g2 = ease_out(prog(t, 2.2, .8)); m = max(2, int(len(PX) * g2))
    s.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in PX[:m])}" fill="none" stroke="{ORANGE}" stroke-width="6"/>')
    if t > 3.0:
        a = ease_out(prog(t, 3.0, .4))
        s.append(f'<g opacity="{a:.2f}"><line x1="720" y1="470" x2="840" y2="470" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 6"/>'
                 f'<line x1="840" y1="470" x2="840" y2="650" stroke="{ORANGE}" stroke-width="5"/>' + label("MDD", 885, 560, 30, ORANGE, 900) + label("고점 → 최저점", 780, 700, 26, ORANGE, 900) + "</g>")
    for i, (txt, c, x) in enumerate((("VaR = 홍수 경계선", RED, 210), ("CVaR = 넘친 뒤 수심", RED, 540), ("MDD = 최저점의 상처", ORANGE, 870))):
        s.append(chip(txt, x, 800, c, back(prog(t, 3.6 + .3 * i, .4)), w=310, size=26))
    s += eqs(t, EQ, (850, 995, 1100), a0=4.8, scale=(.5, .42, .46))
    s += explainer_tail(t, "위험은 평균이 아니라 꼬리에 있다", "σ 흩어짐 · VaR 경계 · CVaR 꼬리 · MDD 낙폭 — 네 질문, 네 답",
                        ["σ는 오를 때 흔들림까지", "위험으로 세거든."])
    return s


def cut5(t): return relief(t, ["그럼 넷 중", "뭘 봐야 해요?"], ["목적이 정해. 연기금은", "꼬리와 낙폭을 먼저 봐."],
                           "목적이 정한다!", "체크: σ · VaR · CVaR · MDD — 무엇을 묻는가", happy=True, a_size=48, sfx_size=110)


def cut6(t): return next_cut(t, RED, "최악 5개월", "경계선 너머는 얼마나 깊나?", topic_size=170)


META = dict(
    episode="EP.01", title="위험이 얼마예요?",
    concept="위험의 네 수학적 정의 — 표준편차 σ(흩어짐, 상승도 위험으로 셈) · VaR(신뢰수준의 최대 예상 손실, 경계선) · CVaR(VaR 너머 꼬리의 평균 손실) · MDD(고점 대비 최대 낙폭). 네 척도가 네 가지 다른 질문에 답한다 — '위험이 얼마냐'는 질문 자체가 미완성",
    source="W09 강의본 7·8·9장(네 정의 · 한 장의 수식 · 비유 — VaR = 홍수 경계선 · CVaR = 넘친 후의 수심 · MDD = 최저점의 상처) · 프라이머 4·5장(위험은 분포의 왼쪽 꼬리에) · 기획표 EP01_Cuts",
    cuts=[{"n": 2, "notice": "펭의 펀드 보고서 · 글로벌 주식형 펀드 · 연 변동성 σ 12% · 위험 등급: 낮음 ✓", "bubble": ["σ가 12%면", "위험은 다 잰 거죠?"], "sfx": "다 쟀다!"},
          {"n": 3, "bubble": ["‘위험이 얼마냐’는 질문이 덜 끝났어.", "무엇을 재느냐에 따라 답이 넷이야."], "sfx": "질문이 넷!"},
          {"n": 4, "figure": "분포(σ · VaR 선 · 꼬리 CVaR) + 낙폭 곡선(MDD)", "chips": ["VaR = 홍수 경계선", "CVaR = 넘친 뒤 수심", "MDD = 최저점의 상처"],
           "latex": ["σ = √E[(r − μ)²]", "P(L > VaR95) = 5%, CVaR = E[L | L > VaR]", "MDD = max_t (1 − V_t / max_{s≤t} V_s)"],
           "summary": "위험은 평균이 아니라 꼬리에 있다", "bubble": ["σ는 오를 때 흔들림까지", "위험으로 세거든."]},
          {"n": 5, "bubbles": [["그럼 넷 중", "뭘 봐야 해요?"], ["목적이 정해. 연기금은", "꼬리와 낙폭을 먼저 봐."]], "sfx": "목적이 정한다!"},
          {"n": 6, "text": ["다음 화", "최악 5개월", "경계선 너머는 얼마나 깊나?"]}],
    **{"fact-check": "분포와 낙폭 곡선은 개념도이며 특정 펀드의 데이터가 아니다. 'σ 12%' 보고서는 연출용(강의본 22장 예제 펀드의 σ와 같은 값). '연기금은 꼬리와 낙폭을 먼저 본다'는 강의본 15장(기관 — 적립비율 · 유동성 위기와 직결)의 요약."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "01", META)
