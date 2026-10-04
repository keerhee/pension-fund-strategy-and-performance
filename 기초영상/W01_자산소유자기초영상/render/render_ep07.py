"""W01 EP.07 '약속이 이자를 넘을 때' — 보험사는 디폴트 LDI 운용자. Float의 축복과 역마진의 저주.
예정이율 7% 확정형(1990년대 중반~2000년대 초 6~8%) · 운용수익 4%(예시) → 해마다 −3%p = 이차역마진. 버크셔 float $1,470억(2024).
보험사의 운용은 수익률 게임이 아니라 부채와의 정렬 게임. (W01 강의본 19장 · 기획표 순서 7 그대로)"""
from wkit import *

TEX = [r"4\% - 7\% = -3\%\mathrm{p}",
       r"10{,}000 \times 0.03 = 300",
       r"300 \times 10 = 3{,}000"]
EQ = [f"eq/ep07_{i}.png" for i in (1, 2, 3)]
for f, tx in zip(EQ, TEX):
    if len(sys.argv) > 1 or not os.path.exists(f): latex_png(tx, f)


def cut1(t): return title(t, "EP.07 · 약속이 이자를 넘을 때", 940)


def cut2(t):
    body = (label("1990년대 확정형 연금보험", 0, -110, 36, "#555", 800)
            + punch("예정이율 7%", 0, 0, 90, fill=GOLD, sw=11)
            + label("펭: “평생 7% 보장이래요!”", 0, 150, 38, BLUE, 900))
    return problem(t, "평생 7%!", GOLD, "#FBF1DD", "펭이 찾은 옛날 광고", body, ["7% 보장이면 보험사가", "엄청 버는 거죠?"], "대박 상품!")


def cut3(t): return twist(t, ["금리가 떨어지면 그 약속이 독이야.", "4%밖에 못 벌면 해마다 −3%p지."], "이차역마진!", size=44, sfx_size=130)


BASE, K = 660, 36


def bar(t, a0, x, v, c, name):
    g = ease_out(prog(t, a0, .6))
    if g <= 0: return ""
    h = v * K * g
    return (f'<rect x="{x-75}" y="{BASE-h:.0f}" width="150" height="{h:.0f}" rx="8" fill="{c}"/>'
            + label(name, x, BASE + 34, 28, NAVY, 900)
            + (label(f"{v}%", x, BASE - v * K - 30, 40, c, 900) if g > .9 else ""))


def cut4(t):
    s = explainer_frame(t, "7% 약속, 4% 수익", "보험사 — 부채(보증금리)가 먼저 정해진 디폴트 LDI 운용자")
    s.append(f'<line x1="140" y1="{BASE}" x2="940" y2="{BASE}" stroke="{NAVY}" stroke-width="4" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    s.append(bar(t, .6, 300, 7, RED, "예정이율 (약속)"))
    s.append(bar(t, 1.2, 580, 4, GREEN, "운용수익 (예시)"))
    if t > 2.0:
        a = ease_out(prog(t, 2.0, .4)); y7, y4 = BASE - 7 * K, BASE - 4 * K
        s.append(f'<g opacity="{a:.2f}"><line x1="300" y1="{y7}" x2="780" y2="{y7}" stroke="{RED}" stroke-width="4" stroke-dasharray="12 8"/>'
                 f'<line x1="660" y1="{y4}" x2="780" y2="{y4}" stroke="{GREEN}" stroke-width="4" stroke-dasharray="12 8"/>'
                 f'<path d="M 780 {y7} h 20 v {y4-y7} h -20" fill="none" stroke="{RED}" stroke-width="5"/>'
                 + label("−3%p", 880, (y7 + y4) / 2 - 20, 44, RED, 900) + label("이차역마진", 880, (y7 + y4) / 2 + 26, 28, RED, 900) + "</g>")
    s.append(chip("책임준비금 1조 원(가정)이라면?", 540, 790, NAVY, back(prog(t, 2.8, .4)), w=700, size=32))
    s.append(eq_img(EQ[0], 540, 840, ease_out(prog(t, 3.4, .5)), scale=.58))
    s.append(eq_img(EQ[1], 540, 930, ease_out(prog(t, 4.0, .5)), scale=.58))
    s.append(f'<g opacity="{ease_out(prog(t, 4.4, .4)):.2f}">' + label("억 원 — 해마다 300억 원씩 메워야 한다 (예시)", 540, 1030, 30, RED, 900) + "</g>")
    s.append(eq_img(EQ[2], 540, 1070, ease_out(prog(t, 5.0, .5)), scale=.58))
    s.append(f'<g opacity="{ease_out(prog(t, 5.4, .4)):.2f}">' + label("10년이면 3,000억 원 — 부채 듀레이션은 20~40년", 540, 1170, 30, NAVY, 900) + "</g>")
    s.append(chip("반대편: 버크셔 float $1,470억(2024) — 저비용 자본", 540, 1260, GOLD, back(prog(t, 6.0, .4)), w=900, size=31))
    s += explainer_tail(t, "수익률 게임이 아니라 부채와의 정렬 게임", "IFRS 17(2022) 부채 시가평가 → 해외채권 · LDI 도입",
                        ["운용이 약속을 못 따라가면,", "그 차이가 해마다 구멍이야."], a0=7.0, red_size=44, owl_size=42)
    return s


def cut5(t): return relief(t, ["처음부터 약속을", "작게 했어야죠?"], ["당시엔 시장금리도 높았어. 문제는", "듀레이션 · 재투자 위험의 방치였지."],
                           "정렬이 답!", "체크: 예정이율 · 운용수익률 · 듀레이션 정렬", a_size=44, chip_size=32, sfx_size=120)


def cut6(t): return next_cut(t, "#3D4F7A", "Yale의 산수", "부채 없는 부족은?", topic_size=170)


META = dict(
    episode="EP.07", title="약속이 이자를 넘을 때",
    concept="보험사는 디폴트 LDI 운용자 — 부채(보증금리)가 먼저 정해진다. 1990년대 중반~2000년대 초 예정이율 6~8% 확정형을 대량 판매했는데 시장금리가 급락하자 자산수익률 < 부채부담이율, 즉 이차역마진이 생겼다. 예정이율 7% · 운용수익 4%(예시)면 해마다 −3%p, 책임준비금 1조 원(가정)이면 연 300억 원 · 10년 3,000억 원. 반대로 잘 정렬된 float는 저비용 자본(버크셔 $1,470억, 2024). 보험사의 운용은 수익률 게임이 아니라 부채와의 정렬 게임 — W6 LDI의 원형",
    source="W01 강의본 19장(보험사 — 디폴트 LDI 운용자, Float 보험료 수입 → 보험금 지급까지의 자금 · 버크셔 float $1,470억(2024) · 부채 듀레이션 20~40년 + 엄격한 규제 → 채권 중심, 한국의 역마진 위기 — 1990년대 중반~2000년대 초 예정이율 6~8% 확정형 대량 판매 · 자산수익률 < 부채부담이율 = 이차역마진 · IFRS 17(2022) 부채 시가평가 → 해외채권 · LDI 도입, “수익률 게임이 아니라 부채와의 정렬 게임”, 당시엔 시장금리도 높았다 — 문제는 듀레이션 · 재투자 위험의 방치) · 기획표 순서 7",
    cuts=[{"n": 2, "notice": "펭이 찾은 옛날 광고 · 1990년대 확정형 연금보험 · 예정이율 7% · 펭: “평생 7% 보장이래요!”", "bubble": ["7% 보장이면 보험사가", "엄청 버는 거죠?"], "sfx": "대박 상품!"},
          {"n": 3, "bubble": ["금리가 떨어지면 그 약속이 독이야.", "4%밖에 못 벌면 해마다 −3%p지."], "sfx": "이차역마진!"},
          {"n": 4, "bars(%)": {"예정이율 (약속)": 7, "운용수익 (예시)": 4}, "gap": "−3%p 이차역마진", "latex": TEX,
           "labels": ["억 원 — 해마다 300억 원씩 메워야 한다 (예시)", "10년이면 3,000억 원 — 부채 듀레이션은 20~40년"],
           "chips": ["책임준비금 1조 원(가정)이라면?", "반대편: 버크셔 float $1,470억(2024) — 저비용 자본"],
           "summary": "수익률 게임이 아니라 부채와의 정렬 게임", "bubble": ["운용이 약속을 못 따라가면,", "그 차이가 해마다 구멍이야."]},
          {"n": 5, "bubbles": [["처음부터 약속을", "작게 했어야죠?"], ["당시엔 시장금리도 높았어. 문제는", "듀레이션 · 재투자 위험의 방치였지."]], "sfx": "정렬이 답!"},
          {"n": 6, "text": ["다음 화", "Yale의 산수", "부채 없는 부족은?"]}],
    check={"gap_pp": -3, "1조x3%(억원)": 300, "10년(억원)": 3000},
    **{"fact-check": "예정이율 7%는 강의본 19장 범위(6~8%) 안의 예시값, 운용수익 4%는 기획표 예시(실제 특정 회사 수치 아님). 책임준비금 1조 원 · 10년 누적 3,000억 원은 이 화에서 덧붙인 가정 계산(단순 합, 준비금 증감 · 할인 무시). 부채 듀레이션 20~40년은 19장 표기(잔존 보증 기간과 같은 개념은 아니며, 손실이 오래 이어질 수 있다는 뜻으로만 썼다). 버크셔 float $1,470억(2024)·IFRS 17(2022)은 강의본 19장 표기(버크셔 연차보고서 원자료 직접 확인 안 함 — 덱 표기, 원자료 미확인)."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "07", META)
