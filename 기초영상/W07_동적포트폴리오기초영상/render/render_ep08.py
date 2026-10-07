"""시즌 3 EP.08 '월급도 주식일 수 있다' — 생애주기 배분의 비판 ①②. 금융업 종사자의 인적자본은 주식 베타 0.3~0.5 — 채권이 아니다.
같은 35세 · 인적자본 12억 · 금융 2억(EP.05)이라도 β 0.4면 주식 4.8억 상당을 이미 쥔 셈 → 통장 2억을 주식에 넣으면 총 부의 주식 노출 14% vs 49%.
(W07 M9 2교시 23장 · 에피소드 4(52장, Merton SmartNest) — β 0.4와 4.8억은 교육용 예시)"""
from s3kit import *

EQ = [f"eq/ep08_{i}.png" for i in (1, 2, 3)]


def cut1(t): return title(t, "EP.08 · 월급도 주식일 수 있다", 900)


def cut2(t):
    body = (f'<rect x="-350" y="-135" width="330" height="200" rx="18" fill="#E6ECF7"/><rect x="20" y="-135" width="330" height="200" rx="18" fill="#FBE9E9"/>'
            + label("A · 공무원", -185, -90, 38, BLUE, 900) + label("35세 · 연봉 6천", -185, -30, 32, NAVY, 800) + label("통장 2억", -185, 20, 32, NAVY, 800)
            + label("B · 증권사", 185, -90, 38, RED, 900) + label("35세 · 연봉 6천", 185, -30, 32, NAVY, 800) + label("통장 2억", 185, 20, 32, NAVY, 800)
            + label("펭의 추천: 둘 다 같은 비중", 0, 140, 40, NAVY, 900))
    return problem(t, "같은 35세?", RED, "#F5E1E1", "펭의 상담 노트 · 두 고객", body, ["나이도 연봉도 같으니까", "같은 비중이면 되죠?"], "똑같이!")


def cut3(t): return twist(t, ["증권사 월급은 시장이 나쁘면 같이 흔들려.", "그 월급은 채권이 아니라 주식을 닮았어."], "월급의 베타!", size=42, sfx_size=140)


X0, W = 110, 860


def wealth(t, a0, y, title_, segs):
    o = [f'<g opacity="{ease_out(prog(t, a0, .4)):.2f}">' + label(title_, X0, y - 72, 30, NAVY, 900, anchor="start") + "</g>"]
    x = X0
    for i, (v, c, txt) in enumerate(segs):
        g = ease_out(prog(t, a0 + .2 + .4 * i, .5)); w = W * v / 14
        if g > 0:
            o.append(f'<rect x="{x:.0f}" y="{y-40}" width="{w*g:.0f}" height="80" fill="{c}" stroke="#fff" stroke-width="3"/>')
            if g > .9: o.append(label(txt, x + w / 2, y, 26 if w < 200 else 30, "#fff", 900))
        x += w
    return "".join(o)


def cut4(t):
    s = explainer_frame(t, "월급 속의 주식", "같은 35세 · 인적자본 H 12억 · 통장 F 2억(EP.05) · β 0.4는 예시")
    s.append(wealth(t, .5, 470, "A 공무원 — 월급은 채권", [(12, NAVY, "채권 같은 H 12억"), (2, GOLD, "F 2")]))
    s.append(wealth(t, 2.0, 640, "B 증권사 — 월급에 주식이 섞였다", [(4.8, RED, "주식 같은 H 4.8"), (7.2, NAVY, "채권 같은 H 7.2"), (2, GOLD, "F 2")]))
    s.append(chip("통장 2억을 다 주식에: A는 총 부의 14% · B는 49%", 540, 760, RED, back(prog(t, 3.6, .4)), w=900, size=32))
    s.append(chip("B는 통장을 채권 쪽으로 기울여야 균형", 540, 845, TEAL, back(prog(t, 4.1, .4)), w=720, size=32))
    s += eqs(t, EQ, (910, 1010, 1120), a0=4.8, scale=.48)
    s += explainer_tail(t, "인적자본이 늘 채권은 아니다", "SmartNest(2013) — TDF는 모두를 같은 사람으로 본다",
                        ["나이만 같다고 같은 답을", "주면 안 되는 이유야."])
    return s


def cut5(t): return relief(t, ["그럼 증권사 B는", "어떻게 해요?"], ["이미 주식 4.8억을 쥔 셈이니", "통장은 채권 쪽으로 기울여."],
                           "직업이 비중을!", "체크: 직업 · 소득과 주가의 상관 · 인적자본 베타", happy=True, a_size=46, sfx_size=110)


def cut6(t): return next_cut(t, NAVY, "기금의 나이", "기관에도 나이가 있나?", topic_size=180)


META = dict(
    episode="EP.08", title="월급도 주식일 수 있다",
    concept="생애주기 배분의 비판 — 인적자본도 안전하지 않다(금융업 종사자의 인적자본은 주식 베타 0.3~0.5)와 개인차 무시(공무원과 창업자의 인적자본은 전혀 다르다). 같은 나이라도 월급이 주가와 함께 움직이면 이미 주식을 쥔 셈이라 금융자산은 채권 쪽으로 기울여야 한다. 개인화의 문제의식이 Merton SmartNest(2013)",
    source="W07 M9 2교시 23장(생애주기 배분의 네 가지 비판 — ① 인적자본도 안전하지 않다: 금융업 종사자의 인적자본은 주식 베타 0.3–0.5, ② 개인차 무시: 공무원과 창업자) · 에피소드 4(52장, Merton SmartNest 2013 “TDF는 모두를 같은 사람으로 취급한다”) · EP.05의 35세 예시(H 12억 · F 2억)",
    cuts=[{"n": 2, "notice": "펭의 상담 노트 · A 공무원 / B 증권사 · 둘 다 35세 · 연봉 6천 · 통장 2억 · 펭의 추천: 둘 다 같은 비중", "bubble": ["나이도 연봉도 같으니까", "같은 비중이면 되죠?"], "sfx": "똑같이!"},
          {"n": 3, "bubble": ["증권사 월급은 시장이 나쁘면 같이 흔들려.", "그 월급은 채권이 아니라 주식을 닮았어."], "sfx": "월급의 베타!"},
          {"n": 4, "stacks": {"A 공무원": {"채권 같은 H": 12, "F": 2}, "B 증권사": {"주식 같은 H": 4.8, "채권 같은 H": 7.2, "F": 2}}, "latex": ["H_equity = β_H × H = 0.4 × 12 = 4.8", "2/14 ≈ 14% vs (4.8 + 2)/14 ≈ 49%", "β_H ≈ 0.3 ~ 0.5 (finance jobs)"],
           "summary": "인적자본이 늘 채권은 아니다", "bubble": ["나이만 같다고 같은 답을", "주면 안 되는 이유야."]},
          {"n": 5, "bubbles": [["그럼 증권사 B는", "어떻게 해요?"], ["이미 주식 4.8억을 쥔 셈이니", "통장은 채권 쪽으로 기울여."]], "sfx": "직업이 비중을!"},
          {"n": 6, "text": ["다음 화", "기금의 나이", "기관에도 나이가 있나?"]}],
    check={"H_equity": 4.8, "share_A": 0.143, "share_B": 0.486},
    **{"fact-check": "β 0.4(강의본 범위 0.3~0.5의 가운데)와 4.8억, 14% · 49%는 교육용 예시 계산이다 — 인적자본의 베타를 금액에 곱해 '주식 상당'으로 보는 것은 단순화. 공무원 인적자본 β ≈ 0도 가정. 고객 A·B는 연출용. SmartNest는 강의본 98장 표기를 따랐다."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "08", META)
