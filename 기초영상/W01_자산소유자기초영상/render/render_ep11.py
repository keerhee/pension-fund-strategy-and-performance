"""W01 EP.11 '베타를 싸게 수확하라' — GPFG의 답. 주식 ~70 · 채권 ~27 · 부동산 등 ~3(대체 의도적 최소) · 액티브 기대 알파 −5~+10bp로 평가
· 운용 비용 5~7bp · TE 한도 1.25% 법정(지수 이탈 허용폭) · 재정 준칙 4% → 3%(2017) · 보유 전 종목 공개.
준칙과 한도 — 정치로부터 기금을 지키는 두 법조문. (W01 강의본 29 · 31장 · 기획표 순서 11)"""
import os, math
from wkit import *

TEX = [r"\sigma\,(r_{\mathrm{GPFG}} - r_{\mathrm{index}}) \leq 1.25\%",
       r"\$1{,}900\,\mathrm{B} \times 0.06\% \approx \$1.1\,\mathrm{B}",
       r"\$1{,}900\,\mathrm{B} \times 0.30\% = \$5.7\,\mathrm{B}"]
EQ = [f"eq/ep11_{i + 1}.png" for i in range(len(TEX))]
for _f, _t in zip(EQ, TEX):
    if not os.path.exists(_f) or (len(sys.argv) > 1 and sys.argv[1] == "stills"): latex_png(_t, _f)


def wiggle(x):
    return 34 * math.sin(x / 47) + 16 * math.sin(x / 13 + 1) + 8 * math.sin(x / 7)


def cut1(t): return title(t, "EP.11 · 베타를 싸게 수확하라", 920)


def cut2(t):
    body = (label("노르웨이 GPFG ≈ $1.9조", 0, -115, 34, "#555", 800)
            + label("주식 ~70 · 채권 ~27 · 부동산 등 ~3", 0, -50, 34, NAVY, 900)
            + label("액티브 기대 알파", 0, 15, 32, "#555", 800) + punch("−5~+10bp", 0, 85, 74, fill="#A23E48", sw=9)
            + label("펭: “이게 다예요?”", 0, 175, 34, BLUE, 900))
    return problem(t, "알파는 포기?", "#A23E48", "#F3E3E5", "GPFG 운용 방침 요약", body, ["$1.9조를 굴리면서", "알파는 안 노려요?"], "의욕 0?!")


def cut3(t): return twist(t, ["알파 대신 비용을 줄였어.", "지수에서 1.25% 넘게는 못 벗어나."], "법정 한도!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "베타를 싸게", "GPFG — 비용 5~7bp · TE 한도 1.25% 법정 · 대체 ~3%")
    cy, x0, x1 = 530, 210, 960
    a = ease_out(prog(t, .4, .4))
    s.append(f'<g opacity="{a:.2f}"><rect x="{x0}" y="{cy - 80}" width="{x1 - x0}" height="160" fill="{BLUE}" opacity=".16"/>'
             f'<line x1="{x0}" y1="{cy - 80}" x2="{x1}" y2="{cy - 80}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 8"/>'
             f'<line x1="{x0}" y1="{cy + 80}" x2="{x1}" y2="{cy + 80}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 8"/>'
             f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{NAVY}" stroke-width="6"/>'
             + label("지수", 140, cy, 32, NAVY, 900) + label("+1.25%", 140, cy - 80, 26, BLUE, 900) + label("−1.25%", 140, cy + 80, 26, BLUE, 900) + "</g>")
    g = ease_out(prog(t, 1.0, 1.6))
    xe = x0 + (x1 - x0) * g
    if g > 0:
        pts = " ".join(f"{x},{cy + wiggle(x - x0):.1f}" for x in range(x0, int(xe) + 1, 6))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linejoin="round"/>')
    if g > .9:
        s.append(label("GPFG — 지수 곁을 바짝 따라간다", 585, cy - 125, 30, ORANGE, 900))
        s.append(label("TE 한도 1.25% = 지수 이탈 허용폭 (법정)", 585, cy + 125, 28, BLUE, 900))
    s += eqs(t, EQ, (720, 850, 980), a0=3.2, scale=(.5, .48, .48))
    s.append(f'<g opacity="{ease_out(prog(t, 4.0, .4)):.2f}">' + label("TE(추적오차) = 지수와의 수익률 차이의 표준편차", 540, 815, 26, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 4.8, .4)):.2f}">' + label("비용 6bp(5~7bp의 중간) → 연 약 $11억", 540, 945, 26, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 5.6, .4)):.2f}">' + label("같은 돈을 30bp로 굴린다면(가정) → 연 $57억", 540, 1075, 26, GREY, 800) + "</g>")
    s.append(chip("준칙 3% + TE 한도 1.25% = 정치로부터 지키는 두 법조문", 540, 1190, NAVY, back(prog(t, 6.3, .4)), w=940, size=30))
    s.append(f'<g opacity="{ease_out(prog(t, 6.8, .4)):.2f}">' + label("부동산 등 대체 ~3% · 보유 전 종목 공개", 540, 1290, 30, TEAL, 900) + "</g>")
    s += explainer_tail(t, "알파를 사지 말고 베타를 싸게 사라", "액티브 기대 알파 −5~+10bp — 비용 차이가 더 확실하다",
                        ["싸게 · 넓게 · 오래.", "이게 GPFG의 답이야."], a0=7.4)
    return s


def cut5(t): return relief(t, ["다른 거대 기금도", "다 이렇게 해요?"], ["캐나다 CPPIB는 정반대야.", "사모 · 내부 운용으로 갔지."],
                           "정반대!", "체크: 비용 5~7bp · TE 1.25% · 대체 ~3% · 준칙 3%", a_size=46, sfx_size=130, chip_size=32)


def cut6(t): return next_cut(t, "#A23E48", "One Fund", "정반대의 답은?", topic_size=170)


META = dict(
    episode="EP.11", title="베타를 싸게 수확하라",
    concept="GPFG의 답 — 액티브 기대 알파를 −5~+10bp로 낮게 보고, 대신 시장 수익(베타)을 싸게 수확한다. 운용 비용 5~7bp, 지수 이탈 허용폭인 TE(추적오차) 한도 1.25%를 법으로 정하고, 대체는 ~3%로 의도적 최소, 보유 전 종목을 공개한다. 재정 준칙(4% → 3%, 2017)과 TE 한도가 정치로부터 기금을 지키는 두 법조문이다. $1.9조에 6bp면 연 약 $11억, 30bp라면 연 $57억",
    source="W01 강의본 29장(GPFG 표 — ≈ $1.9조 · 주식 ~70% · 채권 ~27% · 부동산 등 ~3% 대체 의도적 최소 · '베타를 싸게 수확하라' 액티브 기대 알파 −5~+10bp · 재정 준칙 4% → 3%(2017) · TE 한도 1.25% 법정 · 보유 전 종목 공개 · 준칙과 한도 — 정치로부터 기금을 지키는 두 법조문) · 31장(GPFG vs CPPIB — GPFG 운용 비용 5~7bp · 비유동 약 2.5% · CPPIB 약 30bp) · 27장(스펙트럼 — GPFG 비용 5bp · 대체 ~3%) · 기획표 순서 11",
    cuts=[{"n": 2, "notice": "GPFG 운용 방침 요약 · 노르웨이 GPFG ≈ $1.9조 · 주식 ~70 · 채권 ~27 · 부동산 등 ~3 · 액티브 기대 알파 −5~+10bp · 펭: “이게 다예요?”", "bubble": ["$1.9조를 굴리면서", "알파는 안 노려요?"], "sfx": "의욕 0?!"},
          {"n": 3, "bubble": ["알파 대신 비용을 줄였어.", "지수에서 1.25% 넘게는 못 벗어나."], "sfx": "법정 한도!"},
          {"n": 4, "band": "지수 곁을 바짝 따라가는 GPFG — ±1.25% 띠는 TE 한도 (개념도)",
           "latex": ["σ(r_GPFG − r_index) ≤ 1.25%", "$1,900B × 0.06% ≈ $1.1B (비용 6bp → 연 약 $11억)", "$1,900B × 0.30% = $5.7B (같은 돈을 30bp로, 가정)"],
           "chip": "준칙 3% + TE 한도 1.25% = 정치로부터 지키는 두 법조문", "note": "부동산 등 대체 ~3% · 보유 전 종목 공개",
           "summary": "알파를 사지 말고 베타를 싸게 사라", "bubble": ["싸게 · 넓게 · 오래.", "이게 GPFG의 답이야."]},
          {"n": 5, "bubbles": [["다른 거대 기금도", "다 이렇게 해요?"], ["캐나다 CPPIB는 정반대야.", "사모 · 내부 운용으로 갔지."]], "sfx": "정반대!"},
          {"n": 6, "text": ["다음 화", "One Fund", "정반대의 답은?"]}],
    check={"cost_6bp_usd_B": 1.14, "cost_30bp_usd_B": 5.7},
    **{"fact-check": "주식 ~70 · 채권 ~27 · 부동산 등 ~3 · 알파 −5~+10bp · TE 1.25% · 준칙 4% → 3%(2017)는 강의본 29장 표기(NBIM · 노르웨이 재무부 원자료는 직접 확인하지 않음). 비용은 덱 안에서 표기가 갈린다 — 31장 '5~7bp', 27장 '5bp'. 화면은 기획표 · 31장의 5~7bp를 쓰고 계산은 중간값 6bp(가정). 30bp는 CPPIB 수준(31장)을 빌린 가정 비교. TE 한도 1.25%는 기대 추적오차 기준이라는 점은 기억 기반. 띠 그림의 GPFG 경로는 개념도(실제 데이터 아님)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "11", META)
