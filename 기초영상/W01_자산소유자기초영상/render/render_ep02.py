"""W01 EP.02 '1bp의 무게' — 자본시장 생태계의 경제학. 1bp(베이시스포인트) = 0.01%p.
운용사는 AUM × 보수율로 번다(액티브 70~150bp · ETF 3~20bp). 작은 보수도 큰 돈 위에선 크다 — NPS 1,610조 × 1bp = 1,610억 원.
(W01 강의본 7장 · 8장 · 기획표 순서 2 그대로)"""
from wkit import *

TEX = [r"1\,\mathrm{bp} = 0.01\%\mathrm{p} = 0.0001",
       r"1{,}610 \times 0.0001 = 0.161",
       r"(70 - 20) \times 0.0001 \times 1{,}610 = 8.05"]
EQ = [f"eq/ep02_{i}.png" for i in (1, 2, 3)]
for f, tx in zip(EQ, TEX):
    if len(sys.argv) > 1 or not os.path.exists(f): latex_png(tx, f)


def cut1(t): return title(t, "EP.02 · 1bp의 무게", 700)


def cut2(t):
    body = (label("액티브 펀드 운용보수", 0, -110, 36, "#555", 800)
            + label("연 0.01%p 차이", 0, -40, 40, NAVY, 900) + punch("1bp", 0, 50, 104, fill=GREEN, sw=12)
            + label("펭: “반올림하면 0 아닌가요?”", 0, 165, 38, BLUE, 900))
    return problem(t, "0.01%쯤이야?", GREEN, "#E3F1E8", "펭의 보수 비교표", body, ["1bp면 0.01%p잖아요.", "거의 공짜 아니에요?"], "티끌!")


def cut3(t): return twist(t, ["작은 보수도 큰 돈 위에선 커.", "NPS에 1bp면 해마다 1,610억 원이야."], "1,610억!", size=44, sfx_size=150)


AX0, PX = 140, 5          # 0bp의 x, bp당 픽셀


def rng_bar(t, a0, name, lo, hi, y, c):
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    x0 = AX0 + lo * PX; w = (hi - lo) * PX * g
    return (f'<g opacity="{min(1, g * 1.5):.2f}">' + label(name, AX0, y - 42, 30, c, 900, "start")
            + f'<rect x="{x0}" y="{y-24}" width="{max(w, 4):.0f}" height="48" rx="10" fill="{c}"/>'
            + (label(f"{lo}", x0 - 6, y + 52, 24, c, 900) + label(f"{hi}bp", x0 + (hi - lo) * PX + 10, y + 52, 24, c, 900) if g > .9 else "") + "</g>")


def eq_line(t, f, y, a, scale=.46):
    return eq_img(f, 540, y, ease_out(prog(t, a, .5)), scale=scale)


def cut4(t):
    s = explainer_frame(t, "1bp × 1,610조", "1bp(베이시스포인트) = 0.01%p — 운용사는 AUM × 보수율로 번다")
    a = ease_out(prog(t, .4, .4))
    ax = f'<g opacity="{a:.2f}"><line x1="{AX0}" y1="720" x2="{AX0+160*PX}" y2="720" stroke="{NAVY}" stroke-width="4"/>'
    for v in (0, 50, 100, 150):
        ax += f'<line x1="{AX0+v*PX}" y1="712" x2="{AX0+v*PX}" y2="728" stroke="{NAVY}" stroke-width="4"/>' + label(v, AX0 + v * PX, 750, 22, GREY, 800)
    ax += label("연 보수 (bp)", AX0 + 160 * PX - 40, 690, 22, NAVY, 800) + "</g>"
    s.append(ax)
    s.append(rng_bar(t, .7, "액티브 펀드 70~150bp", 70, 150, 480, RED))
    s.append(rng_bar(t, 1.3, "ETF 3~20bp", 3, 20, 630, GREEN))
    s.append(chip("NPS 1,610조 원(2026.2) 위에 얹으면?", 540, 830, NAVY, back(prog(t, 2.2, .4)), w=760, size=34))
    s.append(eq_line(t, EQ[0], 885, 2.9, .6))
    s.append(eq_line(t, EQ[1], 975, 3.6, .6))
    s.append(f'<g opacity="{ease_out(prog(t, 4.0, .4)):.2f}">' + label("조 원 → 0.161조 = 1bp당 해마다 1,610억 원", 540, 1090, 30, GREEN, 900) + "</g>")
    s.append(eq_line(t, EQ[2], 1130, 4.8, scale=.56))
    s.append(f'<g opacity="{ease_out(prog(t, 5.2, .4)):.2f}">' + label("액티브 하단 − ETF 상단 = 50bp 차이(예시) → 연 8.05조 원", 540, 1240, 30, RED, 900) + "</g>")
    s += explainer_tail(t, "작은 보수도 큰 돈 위에선 크다", "보수 구조를 알아야 위임 계약을 설계한다 — W9 · W15 복선",
                        ["돈이 크면 bp 하나가", "해마다 1,610억 원이야."], a0=6.6)
    return s


def cut5(t): return relief(t, ["운용사는 그래서", "덩치를 키우는 거군요?"], ["맞아. 같은 인력으로 AUM이 커지면", "보수가 늘어 — 고정비 레버리지야."],
                           "규모의 힘!", "체크: bp · AUM × 보수율 · 고정비 레버리지", happy=True, a_size=44, sfx_size=120)


def cut6(t): return next_cut(t, "#6B3FA0", "기다릴 수 있는 돈", "시간은 무엇을 사나?", topic_size=140)


META = dict(
    episode="EP.02", title="1bp의 무게",
    concept="자본시장 참여자의 경제학 — 1bp(베이시스포인트) = 0.01%p. 자산운용사는 AUM × 보수율로 번다(액티브 70~150bp · ETF 3~20bp). 비율로는 작아 보여도 큰 돈 위에선 크다: NPS 1,610조 원 × 1bp = 해마다 1,610억 원. 보수의 구조를 알아야 위임 계약을 설계할 수 있다(W9 성과평가 · W15 TPA의 복선)",
    source="W01 강의본 7장(각 참여자의 경제학 — 1bp = 0.01%p, 운용사 AUM × 보수율 · 고정비 레버리지, 액티브 70~150bp · ETF 3~20bp, 보수의 구조를 알아야 위임 계약을 설계 — W9 · W15 복선) · 8장(NPS 단독 1,610조 원, 2026.2) · 기획표 순서 2",
    cuts=[{"n": 2, "notice": "펭의 보수 비교표 · 액티브 펀드 운용보수 · 연 0.01%p 차이 · 1bp · 펭: “반올림하면 0 아닌가요?”", "bubble": ["1bp면 0.01%p잖아요.", "거의 공짜 아니에요?"], "sfx": "티끌!"},
          {"n": 3, "bubble": ["작은 보수도 큰 돈 위에선 커.", "NPS에 1bp면 해마다 1,610억 원이야."], "sfx": "1,610억!"},
          {"n": 4, "ranges_bp": {"액티브 펀드": [70, 150], "ETF": [3, 20]}, "chip": "NPS 1,610조 원(2026.2) 위에 얹으면?",
           "latex": TEX, "labels": ["조 원 → 0.161조 = 1bp당 해마다 1,610억 원", "액티브 하단 − ETF 상단 = 50bp 차이(예시) → 연 8.05조 원"],
           "summary": "작은 보수도 큰 돈 위에선 크다", "bubble": ["돈이 크면 bp 하나가", "해마다 1,610억 원이야."]},
          {"n": 5, "bubbles": [["운용사는 그래서", "덩치를 키우는 거군요?"], ["맞아. 같은 인력으로 AUM이 커지면", "보수가 늘어 — 고정비 레버리지야."]], "sfx": "규모의 힘!"},
          {"n": 6, "text": ["다음 화", "기다릴 수 있는 돈", "시간은 무엇을 사나?"]}],
    check={"1bp_x_1610조(조원)": 0.161, "50bp_x_1610조(조원)": 8.05},
    **{"fact-check": "1bp 정의 · 보수 범위(액티브 70~150bp · ETF 3~20bp) · 고정비 레버리지는 강의본 7장, NPS 1,610조 원(2026.2)은 강의본 8장 표기(공시 원자료 직접 확인 안 함). 50bp 차이(액티브 하단 70 − ETF 상단 20)와 연 8.05조 원은 설명용 계산 예시이며, 실제 NPS 보수 지출이 아니다(NPS는 직접 · 위탁 운용을 섞어 쓰고 위탁 보수율은 자산군마다 다르다). 1,610억 원은 기금 전체에 1bp를 일률 적용한 단순 곱."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "02", META)
