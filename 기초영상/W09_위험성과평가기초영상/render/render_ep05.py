"""시즌 4 EP.05 '노벨상 펀드의 5주' — LTCM의 VaR 신화 붕괴(1998). Scholes · Merton 참여 · 4년 연 40%+ · 일일 VaR 약 $45M을 자신 →
1998 러시아 디폴트로 5주 만에 $4.6B 손실(VaR의 약 100배). 실패 이유: 정규분포 가정(꼬리 과소) · 위기 때 모든 상관 = 1 · 유동성 위험 부재 · 평온기(1994~98) 백테스트.
CVaR였어도 같은 정규 가정이면 같이 틀렸다 → 스트레스 테스트. (W09 강의본 13·39장 그대로)"""
from s4kit import *

EQ = [f"eq/ep05_{i}.png" for i in (1, 2, 3)]
REASONS = [("정규분포 가정", "꼬리를 과소평가"), ("위기 땐 상관 → 1", "분산이 사라진다"), ("유동성 위험 없음", "팔 수가 없었다"), ("평온기 백테스트", "1994~98만 학습")]


def cut1(t): return title(t, "EP.05 · 노벨상 펀드의 5주", 840)


def cut2(t):
    body = (label("운용진: 노벨상 수상자 2명 (Scholes · Merton)", 0, -105, 32, "#555", 800)
            + label("4년 연평균", -190, -30, 34, "#555", 800) + punch("40%+", -190, 40, 70, fill=GREEN, sw=9)
            + label("일일 VaR", 190, -30, 34, "#555", 800) + punch("$45M", 190, 40, 70, fill=BLUE, sw=9)
            + label("펭: “이 정도면 절대 안 망한다”", 0, 150, 38, NAVY, 900))
    return problem(t, "천재들의 펀드", BLUE, "#E6ECF7", "1998년 봄 · LTCM 투자 설명서", body, ["노벨상 수상자가 만든 모델이니", "틀릴 리 없죠?"], "무적!")


def cut3(t): return twist(t, ["러시아가 디폴트하자 5주 만에 $4.6B.", "모델이 ‘거의 없다’던 일이 일어났어."], "VaR의 100배!", size=44, sfx_size=140)


def cut4(t):
    s = explainer_frame(t, "VaR 신화의 붕괴", "LTCM 1998 — 일일 VaR 약 $45M · 5주 손실 $4.6B")
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}"><rect x="120" y="{720-12}" width="160" height="12" fill="{BLUE}"/>' + label("일일 VaR $45M", 200, 680, 28, BLUE, 900) + "</g>")
    g = ease_out(prog(t, 1.0, 1.0)); h = 330 * g
    s.append(f'<rect x="360" y="{720-h:.0f}" width="160" height="{h:.0f}" fill="{RED}"/>')
    if g > .9: s.append(label("5주 손실 $4.6B", 440, 370, 30, RED, 900))
    s.append(f'<line x1="100" y1="720" x2="560" y2="720" stroke="{NAVY}" stroke-width="4" opacity="{a:.2f}"/>')
    for i, (h1, h2) in enumerate(REASONS):
        g = back(prog(t, 1.8 + .4 * i, .4))
        if g <= 0: continue
        y = 425 + 86 * i
        s.append(f'<g transform="translate(790,{y}) scale({g:.3f})"><rect x="-190" y="-38" width="380" height="76" rx="14" fill="{NAVY}"/>'
                 + label(h1, 0, -13, 26, YELLOW, 900) + label(h2, 0, 20, 22, "#fff", 800) + "</g>")
    s.append(chip("CVaR였어도 같은 정규 가정이면 같이 틀렸다 → 스트레스 테스트", 540, 800, RED, back(prog(t, 3.6, .4)), w=920, size=28))
    s += eqs(t, EQ, (870, 975, 1080), a0=4.2, scale=(.4, .44, .46))
    s += explainer_tail(t, "모델이 알 수 없는 것을 인정하라", "1987 · 2008 · 2020 · 2022 영국 +300bp — 모델 밖 시나리오를 넣는다",
                        ["평온한 날만 배운 모델은", "폭풍을 상상하지 못해."])
    return s


def cut5(t): return relief(t, ["그 뒤엔", "어떻게 됐어요?"], ["Fed가 주도해 은행들이 구제했어.", "한 펀드가 시스템을 흔든 거지."],
                           "겸손이 위험관리!", "체크: 분포 가정 · 위기 상관 · 유동성 · 스트레스 시나리오", a_size=46, sfx_size=96)


def cut6(t): return next_cut(t, GREEN, "Sharpe", "값은 어떻게 매기나?", topic_size=200)


META = dict(
    episode="EP.05", title="노벨상 펀드의 5주",
    concept="LTCM의 VaR 신화 붕괴(1998) — 노벨상 수상자가 참여한 펀드가 정규분포 · 평온기 백테스트에 기댄 VaR(일일 약 $45M)를 믿다가 러시아 디폴트로 5주 만에 $4.6B를 잃었다. 위기에는 상관이 1로 가고 유동성이 사라진다. CVaR도 같은 가정이면 같이 틀린다 — 모델 밖 시나리오(스트레스 테스트)가 필요하다",
    source="W09 강의본 39장(LTCM — Scholes · Merton 참여, 4년 연 40%+, 일일 VaR 약 $45M, 1998 러시아 디폴트 → 5주 만에 $4.6B 손실, 정규분포 가정 · 위기 시 모든 상관 = 1 · 유동성 위험 부재, Fed 주도 구제, 평온기(1994–98) 백테스트의 함정, CVaR였어도 같은 정규 가정이면 같이 틀렸다) · 13장(스트레스 테스트 — 1987 · 2008 · 2020 · 2022 영국 +300bp)",
    cuts=[{"n": 2, "notice": "1998년 봄 · LTCM 투자 설명서 · 운용진 노벨상 수상자 2명(Scholes · Merton) · 4년 연평균 40%+ · 일일 VaR $45M · 펭: “이 정도면 절대 안 망한다”", "bubble": ["노벨상 수상자가 만든 모델이니", "틀릴 리 없죠?"], "sfx": "무적!"},
          {"n": 3, "bubble": ["러시아가 디폴트하자 5주 만에 $4.6B.", "모델이 ‘거의 없다’던 일이 일어났어."], "sfx": "VaR의 100배!"},
          {"n": 4, "bars": {"일일 VaR": "$45M", "5주 손실": "$4.6B"}, "reasons": dict(REASONS), "latex": ["daily VaR ≈ $45M (normal, 1994–98 calm data)", "$4.6B/$45M ≈ 100× in 5 weeks", "crisis: ρ → 1, liquidity → 0"],
           "summary": "모델이 알 수 없는 것을 인정하라", "bubble": ["평온한 날만 배운 모델은", "폭풍을 상상하지 못해."]},
          {"n": 5, "bubbles": [["그 뒤엔", "어떻게 됐어요?"], ["Fed가 주도해 은행들이 구제했어.", "한 펀드가 시스템을 흔든 거지."]], "sfx": "겸손이 위험관리!"},
          {"n": 6, "text": ["다음 화", "Sharpe", "값은 어떻게 매기나?"]}],
    check={"ratio": 102},
    **{"fact-check": "$45M · $4.6B · 5주 · 연 40%+는 강의본 39장 표기(널리 인용되는 수치이나 원자료는 직접 확인하지 않음). 막대 높이는 비율을 맞추지 않은 개념도(실제 비율 약 100배는 수식으로 표시). '약 100배'는 일일 VaR와 5주 누적 손실을 단순 비교한 것으로 기간이 다르다. 두 사람의 노벨상은 1997년 수상."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "05", META)
