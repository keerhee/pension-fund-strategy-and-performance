"""W01 EP.10 '너무 커서 액티브를 못 한다' — GPIF, 패시브의 제국. ¥277조 ≈ $1.87조(2025.9) · 국내 주식 · 국내 채권 · 해외 주식 · 해외 채권 4 × 25
대칭 배분 · 위탁 ~90% · 총비용 ~3bp · 알파 목표 사실상 없음(+20bp 한계). 규모의 역설 — 내가 사면 가격이 오르는 시장 충격이 알파를 잠식,
초대형 기금에게 패시브는 '선택'이 아니라 '귀결'. (W01 강의본 27 · 28장 · 기획표 순서 10)"""
import os
from wkit import *

TEX = [r"4 \times 25\% = 100\%",
       r"\mathrm{JPY}\;277\,\mathrm{T} \times 0.20\% \approx \mathrm{JPY}\;0.55\,\mathrm{T}",
       r"\mathrm{JPY}\;277\,\mathrm{T} \times 0.03\% \approx \mathrm{JPY}\;0.08\,\mathrm{T}"]
EQ = [f"eq/ep10_{i + 1}.png" for i in range(len(TEX))]
for _f, _t in zip(EQ, TEX):
    if not os.path.exists(_f) or (len(sys.argv) > 1 and sys.argv[1] == "stills"): latex_png(_t, _f)

QUAD = [("국내 주식", BLUE), ("해외 주식", TEAL), ("국내 채권", NAVY), ("해외 채권", GREY)]


def cut1(t): return title(t, "EP.10 · 너무 커서 액티브를 못 한다", 1000)


def cut2(t):
    body = (label("일본 공적연금 GPIF (2025.9)", 0, -110, 34, "#555", 800)
            + punch("¥277조", 0, -25, 90, fill=GREEN, sw=11)
            + label("4 × 25% 대칭 · 총비용 ~3bp", 0, 75, 36, NAVY, 900)
            + label("펭: “그냥 지수만 따라가네?”", 0, 165, 36, BLUE, 900))
    return problem(t, "왜 패시브만?", GREEN, "#E2F0E8", "펭의 해외 연기금 노트", body, ["세계 최대급 기금이", "왜 시장만 따라가요?"], "게을러?!")


def cut3(t): return twist(t, ["너무 커서 그래. 내가 사면", "가격이 먼저 올라 알파가 사라져."], "규모의 역설!", size=46, sfx_size=140)


def cut4(t):
    s = explainer_frame(t, "패시브는 귀결", "GPIF ¥277조 ≈ $1.87조 — 위탁 ~90% · 알파 목표 사실상 없음")
    # 왼쪽: 4 × 25 대칭 배분
    for i, (nm, c) in enumerate(QUAD):
        g = back(prog(t, .5 + .3 * i, .4))
        if g <= 0: continue
        x = 200 + 190 * (i % 2); y = 500 + 190 * (i // 2)
        s.append(f'<g transform="translate({x},{y}) scale({g:.3f})"><rect x="-88" y="-88" width="176" height="176" rx="14" fill="{c}"/>'
                 + label(nm, 0, -22, 28, "#fff", 900) + label("25%", 0, 26, 40, YELLOW, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 1.8, .4)):.2f}">' + label("대칭의 미학", 295, 820, 30, NAVY, 900) + "</g>")
    # 오른쪽: 비용 3bp vs 알파 한계 20bp (1bp = 15px)
    base = 760
    for i, (nm, v, c, x) in enumerate([("총비용", 3, NAVY, 660), ("알파 한계", 20, GREEN, 860)]):
        g = ease_out(prog(t, 2.2 + .5 * i, .6)); h = v * 15 * g
        s.append(f'<rect x="{x - 70}" y="{base - h:.0f}" width="140" height="{h:.0f}" fill="{c}"/>')
        if g > .8: s.append(label(f"{'~' if v == 3 else '+'}{v}bp", x, base - v * 15 - 32, 34, c, 900) + label(nm, x, base + 34, 28, NAVY, 900))
    s.append(f'<line x1="570" y1="{base}" x2="950" y2="{base}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, 2.2, .3)):.2f}"/>')
    s += eqs(t, EQ, (870, 975, 1090), a0=3.8, scale=(.5, .46, .46))
    s.append(f'<g opacity="{ease_out(prog(t, 4.8, .4)):.2f}">' + label("+20bp 알파 상한 ≈ ¥5,540억 — 시장 충격이 먼저 갉아먹는다", 540, 1055, 26, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 5.6, .4)):.2f}">' + label("총비용 3bp ≈ ¥831억 — 확실히 아끼는 돈", 540, 1170, 26, GREY, 800) + "</g>")
    s.append(chip("“We are too big to play active”", 540, 1270, NAVY, back(prog(t, 6.3, .4)), w=760, size=34))
    s += explainer_tail(t, "규모가 크면 패시브는 선택이 아니라 귀결", "위치는 취향이 아니다 — 규모 · 부채 · 거버넌스가 정한다",
                        ["큰 고래는 조용히", "헤엄칠 수가 없어."], a0=7.2, red_size=44)
    return s


def cut5(t): return relief(t, ["그럼 덩치 큰 기금은", "할 게 없어요?"], ["비용을 아끼는 것도 운용이야.", "3bp면 1조 원에 3억 원이지."],
                           "싸게가 실력!", "체크: 규모 · 시장 충격 · 총비용 3bp · 알파 한계 20bp", a_size=44, sfx_size=110, chip_size=32)


def cut6(t): return next_cut(t, GREEN, "베타를 싸게 수확하라", "싸게 베타를 사면?", topic_size=100)


META = dict(
    episode="EP.10", title="너무 커서 액티브를 못 한다",
    concept="GPIF(일본, ¥277조 ≈ $1.87조)는 국내 · 해외 주식 · 채권 4 × 25% 대칭 배분, 위탁 ~90%, 총비용 ~3bp로 운용하며 알파 목표가 사실상 없다(+20bp 한계). 규모의 역설: 이만한 기금이 사고팔면 가격이 먼저 움직여(시장 충격) 알파가 잠식된다. 초대형 기금에게 패시브는 '선택'이 아니라 '귀결'이고, 비용을 아끼는 것 자체가 운용 성과다",
    source="W01 강의본 28장(GPIF — 패시브의 제국: “We are too big to play active” · ¥277조 ≈ $1.87조 (2025.9) · 2025년 GPFG에 1위 자리를 내주다 · 4 × 25 대칭 · 위탁 ~90% · 총비용 ~3bp · 알파 목표 사실상 없음 (+20bp 한계) · 규모의 역설 — 시장 충격이 알파를 잠식, 패시브는 선택이 아니라 귀결) · 27장(운용 모델의 스펙트럼 — GPIF 비용 3bp · 위탁 90% · 4 × 25% 대칭, 위치는 규모 · 부채 · 거버넌스가 정한다) · 기획표 순서 10",
    cuts=[{"n": 2, "notice": "펭의 해외 연기금 노트 · 일본 공적연금 GPIF (2025.9) · ¥277조 · 4 × 25% 대칭 · 총비용 ~3bp · 펭: “그냥 지수만 따라가네?”", "bubble": ["세계 최대급 기금이", "왜 시장만 따라가요?"], "sfx": "게을러?!"},
          {"n": 3, "bubble": ["너무 커서 그래. 내가 사면", "가격이 먼저 올라 알파가 사라져."], "sfx": "규모의 역설!"},
          {"n": 4, "grid": [q[0] + " 25%" for q in QUAD], "bars": {"총비용": "~3bp", "알파 한계": "+20bp"},
           "latex": ["4 × 25% = 100%", "JPY 277T × 0.20% ≈ JPY 0.55T (+20bp 알파 상한 ≈ ¥5,540억)", "JPY 277T × 0.03% ≈ JPY 0.08T (총비용 3bp ≈ ¥831억)"],
           "chip": "“We are too big to play active”", "summary": "규모가 크면 패시브는 선택이 아니라 귀결", "bubble": ["큰 고래는 조용히", "헤엄칠 수가 없어."]},
          {"n": 5, "bubbles": [["그럼 덩치 큰 기금은", "할 게 없어요?"], ["비용을 아끼는 것도 운용이야.", "3bp면 1조 원에 3억 원이지."]], "sfx": "싸게가 실력!"},
          {"n": 6, "text": ["다음 화", "베타를 싸게 수확하라", "싸게 베타를 사면?"]}],
    check={"alpha_cap_jpy_100m": 5540, "cost_jpy_100m": 831, "krw_1T_3bp_100m": 3},
    **{"fact-check": "¥277조 ≈ $1.87조(2025.9) · 4 × 25 · 위탁 ~90% · 총비용 ~3bp · +20bp 한계는 강의본 28장 표기(GPIF 연차보고서 원자료는 직접 확인하지 않음). 4 × 25는 기본 포트폴리오 목표 비중이며 실제 비중은 허용 범위 안에서 움직인다(기억 기반). ¥5,540억 · ¥831억은 덱 수치를 곱한 단순 환산 — 실제 알파 · 비용 금액이 아니다. 막대 높이는 bp 비율을 맞춤(1bp = 15px). 'We are too big to play active'는 덱 인용구 그대로."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "10", META)
