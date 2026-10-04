"""W01 EP.09 '석유를 주식으로' — 국부펀드(GPFG). 1969.12.23 북해 에코피스크 첫 분출 → 1970년대 '즉시 분배' 대 '네덜란드병 경계'
→ 1990 의회 결정(국외 투자 강제 + 지출 준칙 + NBIM 분리) → 재정 준칙 4% → 3%(2017) → 2025 ≈ $1.9조 세계 1위 · 1인당 약 $30만.
청구권자 없는 돈은 준칙이 지킨다: $1.9조 × 3% = 연 $570억까지만. (W01 강의본 18 · 29 · 40장 · 기획표 순서 9)"""
import os
from wkit import *

TEX = [r"\$1{,}900\,\mathrm{B} \times 3\% = \$57\,\mathrm{B}",
       r"\$300{,}000 \times 3\% = \$9{,}000"]
EQ = [f"eq/ep09_{i + 1}.png" for i in range(len(TEX))]
for _f, _t in zip(EQ, TEX):
    if not os.path.exists(_f) or (len(sys.argv) > 1 and sys.argv[1] == "stills"): latex_png(_t, _f)

MILES = [("1969", "북해 유전", "첫 분출", GREY), ("1990", "국외 투자 강제", "+ 지출 준칙", BLUE),
         ("2017", "준칙", "4% → 3%", RED), ("2025", "≈ $1.9조", "세계 1위", GREEN)]


def cut1(t): return title(t, "EP.09 · 석유를 주식으로", 860)


def cut2(t):
    body = (label("1969.12.23 북해 에코피스크 첫 분출", 0, -115, 32, "#555", 800)
            + label("“즉시 분배”", -190, -35, 40, RED, 900) + label("vs", 0, -35, 34, GREY, 900) + label("“네덜란드병 경계”", 190, -35, 36, BLUE, 900)
            + punch("석유 돈", 0, 60, 84, fill=GOLD, sw=10)
            + label("펭: “국민에게 바로 나눠 주자!”", 0, 170, 36, BLUE, 900))
    return problem(t, "다 나눠 주자!", BLUE, "#E3ECF6", "1970년대 노르웨이 논쟁", body, ["석유로 번 돈, 국민에게", "바로 나눠 주면 안 돼요?"], "다 쓰자!")


def cut3(t): return twist(t, ["주인은 아직 안 태어난 미래 세대야.", "청구할 사람이 없으니 준칙이 지키지."], "준칙이 지킨다!", size=44, sfx_size=130)


def cut4(t):
    s = explainer_frame(t, "3% 룰의 산수", "1990년의 제도 설계 — 국외 투자 강제 + 지출 준칙 + NBIM 분리")
    a = ease_out(prog(t, .4, .4))
    s.append(f'<line x1="150" y1="440" x2="930" y2="440" stroke="{NAVY}" stroke-width="6" opacity="{a:.2f}"/>')
    for i, (yr, l1, l2, c) in enumerate(MILES):
        g = back(prog(t, .6 + .45 * i, .4))
        if g <= 0: continue
        x = 180 + 240 * i
        s.append(f'<g transform="translate({x},440) scale({g:.3f})"><circle r="20" fill="{c}" stroke="{NAVY}" stroke-width="5"/>'
                 + label(yr, 0, -50, 36, c if c != GREY else NAVY, 900) + label(l1, 0, 58, 26, NAVY, 900) + label(l2, 0, 94, 26, c if c != GREY else "#555", 900) + "</g>")
    # 기금 막대: $1.9조 중 3%만 꺼낸다 (폭 비율 맞춤: 880px × 3% ≈ 26px)
    g = ease_out(prog(t, 2.6, .8))
    w = 880 * g
    s.append(label("기금 ≈ $1.9조", 540, 625, 32, NAVY, 900) if g > .1 else "")
    s.append(f'<rect x="100" y="660" width="{w:.0f}" height="90" rx="8" fill="{GOLD}"/>')
    if t > 3.4:
        b = ease_out(prog(t, 3.4, .5))
        s.append(f'<g opacity="{b:.2f}"><rect x="954" y="660" width="26" height="90" fill="{RED}"/>'
                 f'<line x1="967" y1="752" x2="967" y2="790" stroke="{RED}" stroke-width="4"/>'
                 + label("3%만 꺼내 쓴다 → 연 $570억", 640, 805, 30, RED, 900) + "</g>")
    s += eqs(t, EQ, (865, 1015), a0=4.2, scale=(.5, .5))
    s.append(f'<g opacity="{ease_out(prog(t, 4.6, .4)):.2f}">' + label("$1.9조 × 3% = 연 $570억까지만 인출", 540, 955, 28, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 5.4, .4)):.2f}">' + label("1인당 약 $30만 → 해마다 쓰는 몫은 1인당 약 $9천", 540, 1105, 28, GREY, 800) + "</g>")
    s.append(chip("전 세계 상장주식의 ~1.5% — 석유가 주식이 됐다", 540, 1250, NAVY, back(prog(t, 6.2, .4)), w=880, size=32))
    s += explainer_tail(t, "청구권자 없는 돈은 준칙이 지킨다", "정치적 분리가 장기 투자의 전제조건",
                        ["한 세대가 다 쓰지 못하게", "법으로 묶어 둔 거야."], a0=7.0)
    return s


def cut5(t): return relief(t, ["그럼 남는 돈은", "어디로 가요?"], ["원금은 미래 세대 몫으로 남아.", "1990년의 설계가 2025년의 1위를 만든 거지."],
                           "세대 저축!", "체크: 청구권자 없음 · 3% 준칙 · 국외 투자 · NBIM 분리", a_size=42, sfx_size=120, chip_size=30)


def next_two(t, color, l1, l2, question, size=150):
    """예고 — 제목이 길어 두 줄로 나눈다(next_cut과 같은 배치)."""
    s = [bg(color, "dotsW")]
    s.append(punch("다음 화", 540, 470, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch(l1, 540, 720, size, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch(l2, 540, 900, size, fill=YELLOW, scale=back(prog(t, .7, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label(question, 540, 1090, 54, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s


def cut6(t): return next_two(t, BLUE, "너무 커서", "액티브를 못 한다", "너무 크면 어떻게?", size=130)


META = dict(
    episode="EP.09", title="석유를 주식으로",
    concept="노르웨이 GPFG — 북해 석유 수입을 국외 주식 · 채권으로 바꿔 미래 세대에게 넘기는 국부펀드. 주인이 아직 태어나지 않은 미래 세대라 '청구권자'가 없으므로, 정치가 다 써 버리지 못하게 준칙이 지킨다: 1990 의회 결정(국외 투자 강제 + 지출 준칙 + NBIM 분리), 재정 준칙 4% → 3%(2017). $1.9조 × 3% = 연 $570억까지만 인출. 1990년의 제도 설계가 2025년의 세계 1위를 만들었다",
    source="W01 강의본 40장(노르웨이 — 석유를 주식으로: 1969.12.23 에코피스크 첫 분출 · 1970년대 '즉시 분배' 대 '네덜란드병 경계' · 1990 의회 결정 국외 투자 강제 + 지출 준칙 + NBIM 분리 · ≈ $1.9조 2025년 세계 1위 · 1인당 약 $30만 · 전 세계 상장주식 ~1.5% · 준칙 4% → 3% (2017) — 한 세대가 다 쓰지 못하게) · 29장(GPFG 표 — 재정 준칙 4% → 3% · TE 한도 1.25%) · 18장(국부펀드 — 청구권자 없는 돈의 운용, 영구 지평) · 기획표 순서 9 · 손계산 검산표",
    cuts=[{"n": 2, "notice": "1970년대 노르웨이 논쟁 · 1969.12.23 북해 에코피스크 첫 분출 · “즉시 분배” vs “네덜란드병 경계” · 석유 돈 · 펭: “국민에게 바로 나눠 주자!”", "bubble": ["석유로 번 돈, 국민에게", "바로 나눠 주면 안 돼요?"], "sfx": "다 쓰자!"},
          {"n": 3, "bubble": ["주인은 아직 안 태어난 미래 세대야.", "청구할 사람이 없으니 준칙이 지키지."], "sfx": "준칙이 지킨다!"},
          {"n": 4, "timeline": [f"{a} — {b} {c}" for a, b, c, _ in MILES], "bar": "기금 ≈ $1.9조 중 3%만 꺼내 쓴다 → 연 $570억",
           "latex": ["$1,900B × 3% = $57B (= 연 $570억)", "$300,000 × 3% = $9,000 (1인당 약 $30만 → 연 약 $9천)"],
           "chip": "전 세계 상장주식의 ~1.5% — 석유가 주식이 됐다", "summary": "청구권자 없는 돈은 준칙이 지킨다", "bubble": ["한 세대가 다 쓰지 못하게", "법으로 묶어 둔 거야."]},
          {"n": 5, "bubbles": [["그럼 남는 돈은", "어디로 가요?"], ["원금은 미래 세대 몫으로 남아.", "1990년의 설계가 2025년의 1위를 만든 거지."]], "sfx": "세대 저축!"},
          {"n": 6, "text": ["다음 화", "너무 커서 액티브를 못 한다", "너무 크면 어떻게?"]}],
    check={"withdraw_usd_100m": 570, "per_capita_usd": 9000},
    **{"fact-check": "$1.9조 · 1인당 약 $30만 · 상장주식 ~1.5% · 준칙 4% → 3%(2017) · 1969.12.23 · 1990 의회 결정은 강의본 40 · 29장 표기(NBIM 공시 원자료는 직접 확인하지 않음). '$1.9조 × 3% = $570억'은 기획표 손계산 — 실제 준칙은 '구조적 비석유 재정적자 ≤ 기금의 기대 실질수익 3%'로 연도 초 기금 가치에 적용하며, 실제 인출액은 연도마다 다르다(기억 기반). 1인당 $9천은 덱의 1인당 $30만에 3%를 곱한 단순 환산(실제 1인 배분 제도는 없음). 막대의 3% 조각 폭은 비율을 맞춤. 1990 '지출 준칙'과 2001 재정 준칙 도입 연도 구분은 덱 표기를 따름."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "09", META)
