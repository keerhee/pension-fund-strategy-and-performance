"""시즌 3 EP.10 'Shannon's Demon' — 리밸런싱은 제자리 자산에서도 번다. 현금 50 + 자산 50(예시), 자산 가격 ×2 → ×½(제자리).
그냥 두면 100 → 150 → 100, 매기 50/50 리밸런싱하면 100 → 150 → 112.5. 오른 것을 팔고 내린 것을 사는 규율.
(W07 SS2 6·7장 · 프라이머 12·13장 — 수치는 교육용 예시)"""
from s3kit import *

EQ = [f"eq/ep10_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.10 · Shannon's Demon", 780)


def cut2(t):
    body = (label("현금 50 + 자산 X 50 (예시)", 0, -110, 38, NAVY, 900)
            + label("1년차", -190, -45, 34, "#555", 800) + punch("×2", -190, 25, 80, fill=GREEN, sw=10)
            + label("2년차", 190, -45, 34, "#555", 800) + punch("×½", 190, 25, 80, fill=RED, sw=10)
            + label("자산 X 가격은 결국 제자리", 0, 150, 38, BLUE, 900))
    return problem(t, "제자리걸음", TEAL, "#DDF0EE", "펭의 계좌 · 2년 기록", body, ["가격이 제자리니까", "내 돈도 제자리죠?"], "본전!")


def cut3(t): return twist(t, ["매년 50/50으로 맞춰 왔다면 112.5야.", "오르면 팔고 내리면 산 덕분이지."], "출렁임이 돈!", size=44, sfx_size=140)


BASE, K = 790, 2.0
GROUPS = [("시작", 100, 100), ("1년차 ×2", 150, 150), ("2년차 ×½", 100, 112.5)]


def cut4(t):
    s = explainer_frame(t, "그냥 두기 vs 리밸런싱", "현금 50 + 자산 50 · 자산 ×2 → ×½ · 매년 50/50으로 복원 (예시)", head_size=92)
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    for i, (name, hold, reb) in enumerate(GROUPS):
        cx = 250 + 290 * i
        for j, (v, c) in enumerate(((hold, GREY), (reb, TEAL))):
            g = ease_out(prog(t, .7 + .9 * i + .3 * j, .5))
            if g <= 0: continue
            x = cx - 60 + 120 * j; h = v * K * g
            s.append(f'<rect x="{x-52}" y="{BASE-h:.0f}" width="104" height="{h:.0f}" fill="{c}" rx="6"/>')
            if g > .9: s.append(label(f"{v:g}", x, BASE - v * K - 26, 34, RED if (i == 2 and j == 1) else c, 900))
        s.append(f'<g opacity="{ease_out(prog(t, .7 + .9 * i, .4)):.2f}">' + label(name, cx, BASE + 36, 30, NAVY, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 3.6, .4)):.2f}"><rect x="110" y="410" width="30" height="22" fill="{GREY}"/>' + label("그냥 두기", 150, 421, 26, GREY, 900, anchor="start")
             + f'<rect x="300" y="410" width="30" height="22" fill="{TEAL}"/>' + label("50/50 리밸런싱", 340, 421, 26, TEAL, 900, anchor="start") + "</g>")
    s.append(chip("자산은 제자리 · 리밸런싱은 +12.5", 540, 895, TEAL, back(prog(t, 4.0, .4)), w=640, size=34))
    s += eqs(t, EQ, (960, 1060, 1160), a0=4.6, scale=(.46, .46, .44))
    s += explainer_tail(t, "싸게 사고 비싸게 파는 규율", "오른 쪽을 덜어 내린 쪽을 채운다 — 감정이 아니라 규칙으로",
                        ["150일 때 75를 팔아 둔 게", "반토막에서 살 돈이 됐지."])
    return s


def cut5(t): return relief(t, ["그럼 무조건 자주", "맞추면 되겠네요?"], ["거래비용과 평균회귀를 봐야 해.", "얼마나 자주는 몇 화 뒤에 숫자로 보자."],
                           "공짜는 아니야!", "체크: 목표 비중 · 비중 드리프트 · 리밸런싱 횟수", a_size=42, sfx_size=110)


def cut6(t): return next_cut(t, TEAL, "분산수익 DR", "리밸런싱 수익은 어디서 오나?", topic_size=160)


META = dict(
    episode="EP.10", title="Shannon's Demon",
    concept="리밸런싱은 변동성을 수익으로 바꾸는 규율 — 고정 비중을 유지하면 오른 자산을 팔고 내린 자산을 사게 된다. 횡보장(자산 ×2 → ×½)에서도 50/50 리밸런싱은 수익을 낸다(Shannon's Demon). 그냥 두면 비중이 오른 쪽으로 흘러가 분산이 사라진다",
    source="W07 SS2 6·7장(Shannon's Demon — 자산은 제자리인데 50/50 리밸런싱은 수익, B&H는 오른 자산으로 쏠린다) · 프라이머 12·13장(그냥 두면 비중이 틀어진다, 되돌리면 결과가 달라진다)",
    cuts=[{"n": 2, "notice": "펭의 계좌 · 2년 기록 · 현금 50 + 자산 X 50(예시) · 1년차 ×2 · 2년차 ×½ · 자산 X 가격은 결국 제자리", "bubble": ["가격이 제자리니까", "내 돈도 제자리죠?"], "sfx": "본전!"},
          {"n": 3, "bubble": ["매년 50/50으로 맞춰 왔다면 112.5야.", "오르면 팔고 내리면 산 덕분이지."], "sfx": "출렁임이 돈!"},
          {"n": 4, "bars": {"그냥 두기": [100, 150, 100], "50/50 리밸런싱": [100, 150, 112.5]}, "latex": ["asset: 1 × 2 × ½ = 1 (flat)", "hold: 50 + 50 × 2 × ½ = 100", "rebalance: 150 → (75, 75) → 75 + 75 × ½ = 112.5"],
           "summary": "싸게 사고 비싸게 파는 규율", "bubble": ["150일 때 75를 팔아 둔 게", "반토막에서 살 돈이 됐지."]},
          {"n": 5, "bubbles": [["그럼 무조건 자주", "맞추면 되겠네요?"], ["거래비용과 평균회귀를 봐야 해.", "얼마나 자주는 몇 화 뒤에 숫자로 보자."]], "sfx": "공짜는 아니야!"},
          {"n": 6, "text": ["다음 화", "분산수익 DR", "리밸런싱 수익은 어디서 오나?"]}],
    check={"hold": 100, "rebalance": 112.5},
    **{"fact-check": "현금 50 + 자산 50, ×2 → ×½는 Shannon's Demon을 보여 주는 교육용 예시(강의본 6장은 그림만 있다). 현금 수익 0, 거래비용 0 가정. 극단적 변동(±100%/−50%)이라 효과가 크게 보인다 — 실제 크기는 EP.11~12의 분산수익 · 순 프리미엄(bp 단위)으로 잰다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "10", META)
