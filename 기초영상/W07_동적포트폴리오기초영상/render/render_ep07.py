"""시즌 3 EP.07 'To vs Through' — 글라이드패스의 두 축(공격성 · 형태). 공격적(Vanguard형) 90 → 30% Through(은퇴 후에도 감소),
보수적(한국형) 70 → 20% To(은퇴 시점에 안정화). 형태의 선택이 2022년 성과를 갈랐다(2022 TDF −14~20%).
Babbel(1985) 제안 25세 80% → 85세 20% = 연 1%p. (W07 M9 2교시 21·22장 · 에피소드 2(50장) 그대로)"""
from s3kit import *

EQ = [f"eq/ep07_{i}.png" for i in (1, 2, 3)]
THRU = [(25, 90), (35, 82), (45, 70), (55, 52), (65, 30), (75, 22), (85, 18)]
TO = [(25, 70), (35, 65), (45, 55), (55, 38), (65, 20), (75, 20), (85, 20)]


def cut1(t): return title(t, "EP.07 · To vs Through", 700)


def cut2(t):
    body = (f'<rect x="-350" y="-130" width="330" height="190" rx="18" fill="#E9F1E4"/><rect x="20" y="-130" width="330" height="190" rx="18" fill="#E6ECF7"/>'
            + label("TDF A", -185, -85, 40, GREEN, 900) + label("2065 · Through", -185, -20, 34, NAVY, 800)
            + label("TDF B", 185, -85, 40, BLUE, 900) + label("2065 · To", 185, -20, 34, NAVY, 800)
            + label("이름은 둘 다 ‘TDF 2065’", 0, 130, 42, NAVY, 900))
    return problem(t, "TDF는 다 같다?", GREEN, "#E9F1E4", "펭의 디폴트옵션 상품 비교", body, ["이름이 둘 다 TDF니까", "같은 상품 아니에요?"], "똑같은 TDF!")


def cut3(t): return twist(t, ["출발점 · 도착점 · 은퇴 뒤 모양이 달라.", "형태의 선택이 2022년을 갈랐어."], "모양이 위험!", size=44, sfx_size=140)


X0, X1, Y0, Y1 = 150, 930, 420, 790


def px(a, w): return X0 + (X1 - X0) * (a - 25) / 60, Y1 - (Y1 - Y0) * w / 100


def path(t, a0, pts, c, dash=""):
    g = ease_out(prog(t, a0, 1.4)); n = max(2, int(round(1 + (len(pts) - 1) * g)))
    xy = [px(*p) for p in pts[:n]]
    return f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in xy)}" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" {dash}/>'


def cut4(t):
    s = explainer_frame(t, "두 개의 글라이드패스", "주식 비중 — 시작점 · 은퇴 시점(65세) · 은퇴 후 모양")
    a = ease_out(prog(t, .4, .4))
    rx = px(65, 0)[0]
    s.append(f'<g opacity="{a:.2f}"><line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{NAVY}" stroke-width="4"/>'
             f'<line x1="{rx}" y1="{Y0-10}" x2="{rx}" y2="{Y1}" stroke="{RED}" stroke-width="3" stroke-dasharray="10 8"/>'
             + label("은퇴 65세", rx, Y0 - 30, 26, RED, 900)
             + "".join(label(f"{g}세", px(g, 0)[0], Y1 + 30, 24, NAVY, 800) for g in (25, 45, 65, 85)) + "</g>")
    s.append(path(t, .8, THRU, GREEN))
    s.append(path(t, 2.2, TO, BLUE, 'stroke-dasharray="18 10"'))
    if t > 2.4:
        o = ease_out(prog(t, 2.4, .4))
        s.append(f'<g opacity="{o:.2f}">' + label("90%", px(25, 90)[0] + 40, px(25, 90)[1] - 26, 30, GREEN, 900)
                 + label("30%", px(65, 30)[0] + 44, px(65, 30)[1] - 24, 30, GREEN, 900) + "</g>")
    if t > 3.6:
        o = ease_out(prog(t, 3.6, .4))
        s.append(f'<g opacity="{o:.2f}">' + label("70%", px(25, 70)[0] + 40, px(25, 70)[1] + 30, 30, BLUE, 900)
                 + label("20%", px(65, 20)[0] - 40, px(65, 20)[1] + 30, 30, BLUE, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 3.8, .4)):.2f}"><rect x="715" y="450" width="34" height="10" fill="{GREEN}"/>' + label("Through (공격적)", 759, 456, 26, GREEN, 900, anchor="start")
             + f'<rect x="715" y="490" width="34" height="10" fill="{BLUE}"/>' + label("To (한국형)", 759, 496, 26, BLUE, 900, anchor="start") + "</g>")
    s.append(chip("2022년 미국 TDF −14~20% → 은퇴 연기 · 소송", 540, 900, RED, back(prog(t, 4.4, .4)), w=820, size=32))
    s += eqs(t, EQ, (965, 1060, 1155), a0=5.0, scale=.46)
    s += explainer_tail(t, "같은 ‘TDF’ 아래 전혀 다른 위험", "공격성(시작 비중)과 형태(To · Through) 두 축이 상품을 정한다",
                        ["은퇴 직전 주식이 얼마냐가", "2022년 같은 해의 성적표야."], red_size=46)
    return s


def cut5(t): return relief(t, ["한국은 왜", "보수적인 To예요?"], ["퇴직금 손실 회피 · 단기 평가 · 디폴트옵션", "설계가 곡선을 그렇게 만들었어."],
                           "시장이 곡선을!", "체크: 시작 비중 · 은퇴 시 비중 · To/Through · 은퇴 후 경로", a_size=42, chip_size=32)


def cut6(t): return next_cut(t, "#B8462E", "월급의 베타", "월급은 정말 채권인가?", topic_size=170)


META = dict(
    episode="EP.07", title="To vs Through",
    concept="글라이드패스의 두 축 — 공격성(시작 비중)과 형태(To: 은퇴 시점에 안정화, Through: 은퇴 후에도 감소). 공격적(Vanguard형) 90 → 30% Through와 보수적(한국형) 70 → 20% To는 같은 'TDF' 이름 아래 전혀 다른 위험을 진다. 한국이 To인 이유는 시장 구조(퇴직금 전환 자금의 손실 회피 · 단기 평가 관행 · 디폴트옵션의 보수적 설계)",
    source="W07 M9 2교시 21·22장(공격적(Vanguard형) 90 → 30% Through, 보수적(한국형) 70 → 20% To, 시작·은퇴 시 비중 표, 형태의 선택이 2022년 성과를 갈랐다) · 에피소드 2(50장 — Babbel 1985 TIAA-CREF 제안 25세 80% → 85세 20%, 1994 첫 TDF, 2006 PPA, 2022 −14~20% 손실 → 은퇴 연기 · 소송)",
    cuts=[{"n": 2, "notice": "펭의 디폴트옵션 상품 비교 · TDF A 2065 · Through / TDF B 2065 · To · 이름은 둘 다 ‘TDF 2065’", "bubble": ["이름이 둘 다 TDF니까", "같은 상품 아니에요?"], "sfx": "똑같은 TDF!"},
          {"n": 3, "bubble": ["출발점 · 도착점 · 은퇴 뒤 모양이 달라.", "형태의 선택이 2022년을 갈랐어."], "sfx": "모양이 위험!"},
          {"n": 4, "paths": {"Through": "90 → 30% (65) → 계속 감소", "To": "70 → 20% (65) → 평탄"}, "latex": ["Through: 90% → 30% (65), then lower", "To: 70% → 20% (65), then flat", "Babbel 1985: (80 − 20)/(85 − 25) = 1%p/yr"],
           "summary": "같은 ‘TDF’ 아래 전혀 다른 위험", "bubble": ["은퇴 직전 주식이 얼마냐가", "2022년 같은 해의 성적표야."]},
          {"n": 5, "bubbles": [["한국은 왜", "보수적인 To예요?"], ["퇴직금 손실 회피 · 단기 평가 · 디폴트옵션", "설계가 곡선을 그렇게 만들었어."]], "sfx": "시장이 곡선을!"},
          {"n": 6, "text": ["다음 화", "월급의 베타", "월급은 정말 채권인가?"]}],
    check={"babbel_slope_pp_per_yr": 1.0},
    **{"fact-check": "두 곡선의 중간 점과 은퇴 후 Through 경로(65세 이후 30 → 18%)는 강의본의 시작·은퇴 시 비중(90 → 30, 70 → 20)을 잇는 개념도이며 특정 상품의 실제 글라이드패스가 아니다. 2022 −14~20%는 강의본 95장의 미국 TDF 손실 범위. 'TDF 2065'는 연출용 상품명."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "07", META)
