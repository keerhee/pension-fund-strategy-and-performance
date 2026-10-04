"""W01 EP.12 'One Fund' — CPPIB, TPA의 원조. C$714.4B · FY2025 +9.3% · 내부 운용 80%+ · PE 30%+ · 비용 약 30bp(총비용 기준)
· Reference Portfolio(주식 85 / 채권 15의 단순 기준) 대비 상대 운용. One Fund 개편(Wiseman, 2012–16): 자산군 팀 해체 → 전략 팀 재편 —
TPA는 기법이 아니라 '조직 설계'. GPFG와 정반대의 답. (W01 강의본 30 · 31장 · 기획표 순서 12)"""
import os
from wkit import *

TEX = [r"r_{\mathrm{RP}} = 0.85 \times 7\% + 0.15 \times 4\% = 6.55\%",
       r"\mathrm{C}\$714\,\mathrm{B} \times 0.30\% \approx \mathrm{C}\$2.1\,\mathrm{B}",
       r"\Delta = r_{\mathrm{CPPIB}} - r_{\mathrm{RP}} > 0"]
EQ = [f"eq/ep12_{i + 1}.png" for i in range(len(TEX))]
for _f, _t in zip(EQ, TEX):
    if not os.path.exists(_f) or (len(sys.argv) > 1 and sys.argv[1] == "stills"): latex_png(_t, _f)

STATS = [("내부 운용", "80%+", TEAL), ("사모(PE)", "30%+", BLUE), ("총비용", "~30bp", RED), ("FY2025", "+9.3%", GREEN)]


def cut1(t): return title(t, "EP.12 · One Fund", 700)


def cut2(t):
    body = (label("CPPIB 조직 개편 (Wiseman, 2012–16)", 0, -115, 32, "#555", 800)
            + label("주식팀 · 채권팀 · 부동산팀", 0, -45, 38, NAVY, 900)
            + punch("해체!", 0, 50, 96, fill=GOLD, sw=11)
            + label("펭: “운용역은 다 어디로?”", 0, 165, 36, BLUE, 900))
    return problem(t, "팀이 사라졌다?", GOLD, "#F8EED8", "캐나다 연금 CPPIB 뉴스", body, ["자산군 팀을 없애면", "누가 운용해요?"], "해체?!")


def cut3(t): return twist(t, ["자산군 대신 ‘하나의 기금’으로 본 거야.", "TPA는 기법이 아니라 조직 설계지."], "One Fund!", size=44, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "One Fund의 산수", "기준 RP(주식 85 / 채권 15) 대비 상대 운용 · C$714.4B")
    # 왼쪽: RP 85/15 막대 (1% = 4.2px)
    base, k = 840, 4.2
    for i, (nm, v, c, a0) in enumerate([("주식", 85, NAVY, .5), ("채권", 15, ORANGE, 1.0)]):
        g = ease_out(prog(t, a0, .5)); h = v * k * g
        y0 = base - (0 if i == 0 else 85 * k)
        s.append(f'<rect x="130" y="{y0 - h:.0f}" width="230" height="{h:.0f}" fill="{c}"/>')
        if g > .8: s.append(label(f"{nm} {v}", 245, y0 - v * k / 2, 34, "#fff", 900))
    a = ease_out(prog(t, 1.5, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("기준 = RP", 245, 385, 34, RED, 900)
             + f'<line x1="110" y1="{base}" x2="380" y2="{base}" stroke="{NAVY}" stroke-width="5"/></g>')
    # 오른쪽: 실제 운용 네 칸
    for i, (nm, v, c) in enumerate(STATS):
        g = back(prog(t, 1.9 + .4 * i, .4))
        if g <= 0: continue
        y = 450 + 115 * i
        s.append(f'<g transform="translate(700,{y}) scale({g:.3f})"><rect x="-280" y="-48" width="560" height="96" rx="16" fill="{c}"/>'
                 + label(nm, -120, 0, 32, "#fff", 900) + label(v, 140, 0, 44, YELLOW, 900) + "</g>")
    s += eqs(t, EQ, (900, 1015, 1130), a0=4.0, scale=(.44, .46, .48))
    s.append(f'<g opacity="{ease_out(prog(t, 4.4, .4)):.2f}">' + label("가정: 주식 7% · 채권 4% 기대수익 → RP가 낼 몫", 540, 985, 26, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 5.2, .4)):.2f}">' + label("비용 ~30bp ≈ 연 C$21억 — RP보다 이만큼은 더 벌어야", 540, 1100, 26, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 6.0, .4)):.2f}">' + label("성적표 = RP 대비 순부가가치", 540, 1215, 26, GREY, 800) + "</g>")
    s.append(chip("자산군 팀 해체 → 전략 팀 재편", 540, 1300, NAVY, back(prog(t, 6.6, .4)), w=680, size=34))
    s += explainer_tail(t, "TPA는 기법이 아니라 조직 설계", "GPFG(베타를 싸게)와 정반대의 답",
                        ["기준은 단순하게,", "운용은 하나의 기금으로."], a0=7.4)
    return s


def cut5(t): return relief(t, ["비용 30bp면", "비싼 거 아니에요?"], ["RP를 그보다 더 이기면 남는 장사야.", "그 판단을 맡길 조직이 있느냐가 핵심이지."],
                           "조직이 답!", "체크: RP 85/15 · 내부 운용 80%+ · PE 30%+ · ~30bp", a_size=42, sfx_size=120, chip_size=32)


def cut6(t): return next_cut(t, GOLD, "수익률 1%p = 7년", "한국의 답은?", topic_size=124)


META = dict(
    episode="EP.12", title="One Fund",
    concept="CPPIB의 답 — 자산군별 목표 비중 대신 '주식 85 / 채권 15'의 단순한 Reference Portfolio(RP)를 기준으로 두고, 기금 전체를 하나로(One Fund) 보며 그 기준을 이기려 한다(TPA). 내부 운용 80%+, 사모 30%+, 비용 약 30bp. 2012–16 Wiseman의 개편으로 자산군 팀을 해체하고 전략 팀으로 재편했다 — TPA는 기법이 아니라 조직 설계다. 비용 30bp(연 약 C$21억)를 넘는 순부가가치를 내느냐가 성적표",
    source="W01 강의본 30장(CPPIB — TPA의 원조: C$714.4B · FY2025 +9.3% · 10년 연환산 9%대 · 주식 ~55 · 채권 ~22 · 실물 ~23 · 내부 운용 80%+ · PE 30%+ · Reference Portfolio 주식 85 / 채권 15 대비 상대 운용 · One Fund 개편(Wiseman, 2012–16) 자산군 팀 해체 → 전략 팀 재편, TPA는 기법이 아니라 조직 설계) · 31장(GPFG vs CPPIB — 비유동 30%+, 운용 비용 약 30bp 총비용 기준) · 기획표 순서 12",
    cuts=[{"n": 2, "notice": "캐나다 연금 CPPIB 뉴스 · CPPIB 조직 개편 (Wiseman, 2012–16) · 주식팀 · 채권팀 · 부동산팀 해체! · 펭: “운용역은 다 어디로?”", "bubble": ["자산군 팀을 없애면", "누가 운용해요?"], "sfx": "해체?!"},
          {"n": 3, "bubble": ["자산군 대신 ‘하나의 기금’으로 본 거야.", "TPA는 기법이 아니라 조직 설계지."], "sfx": "One Fund!"},
          {"n": 4, "bar": {"RP 주식": 85, "RP 채권": 15}, "stats": {a: b for a, b, _ in STATS},
           "latex": ["r_RP = 0.85 × 7% + 0.15 × 4% = 6.55% (가정 기대수익)", "C$714B × 0.30% ≈ C$2.1B (비용 ~30bp ≈ 연 C$21억)", "Δ = r_CPPIB − r_RP > 0 (RP 대비 순부가가치)"],
           "chip": "자산군 팀 해체 → 전략 팀 재편", "summary": "TPA는 기법이 아니라 조직 설계", "bubble": ["기준은 단순하게,", "운용은 하나의 기금으로."]},
          {"n": 5, "bubbles": [["비용 30bp면", "비싼 거 아니에요?"], ["RP를 그보다 더 이기면 남는 장사야.", "그 판단을 맡길 조직이 있느냐가 핵심이지."]], "sfx": "조직이 답!"},
          {"n": 6, "text": ["다음 화", "수익률 1%p = 7년", "한국의 답은?"]}],
    check={"rp_return": 6.55, "cost_cad_100m": 21.4},
    **{"fact-check": "C$714.4B · FY2025 +9.3% · 내부 운용 80%+ · PE 30%+ · RP 85/15는 강의본 30장, 비용 약 30bp는 31장 표기(CPPIB 연차보고서 원자료는 직접 확인하지 않음). 기획표는 '사모 30%+'로, 30장은 'PE 30%+', 31장은 '비유동 30%+(사모 · 인프라 · 실물)'로 적어 표기가 조금씩 다르다 — 화면은 '사모(PE) 30%+'. 주식 7% · 채권 4% 기대수익은 가정(덱에 없음). C$21억은 C$714.4B × 0.30%의 단순 환산. CPPIB가 RP 대비 성과를 비용 차감 후(순) 부가가치로 보고한다는 점은 기억 기반. RP의 실제 구성은 시기별로 조정돼 왔고 덱의 85/15를 따랐다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "12", META)
