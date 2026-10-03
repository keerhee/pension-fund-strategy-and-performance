"""시즌 2 「지킬 것부터 사라」 EP.B3 'Yale을 흉내 낼 수 있나?' — 9:16 웹툰 숏폼. (IC 보너스 3 · 시즌 마지막 — W06 M8 케이스 2부)
H대학교 발전기금(가상): 5,000억 · 지출 200억(4.0%) · 3년차 건축 목돈 600억 · 대체 전담 1명. 실질 잠식 3 − 2 − 4 = −3%/년.
좌표 (x 비유동 상한, y 안전 유동 하한, z 지출률): Yale형 (60,15,5.25) 생존 2년 → 부결 · GPFG형 (0,35,4.0) 통과 · 여유 없음 · 기본 답 (20,30,4.5) 13년 → 조건부 승인.
y 하한 (620 + 600) ÷ 0.88 ≈ 1,386억 → 28% → 격자 30%. z 5.25% 실질가치 유지 46% vs 4.5% 59%. Yale도 2025년 PE 세컨더리 약 25억 달러 매각.
(케이스 덱 2부 2~3·9·23장 그대로 — 결론은 학생 덱 2장에 공개, 기획표 B3_Cuts 시트 구성)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/epB3_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성
PURPLE = "#6B3FA0"


def cut1(t):
    s = title_cut(t, "EP.B3 · Yale을 흉내 낼 수 있나?", chip_w=960)
    s.insert(2, punch("시즌 2 · IC 보너스", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 이사회 결의 "Yale처럼"
    s = [bg("#EEE7F6")]
    s.append(punch("Yale처럼!", 540, 170, 120, fill=PURPLE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{PURPLE}"/><rect x="-390" y="-180" width="780" height="26" fill="{PURPLE}"/>'
                 + label("H대학교 발전기금 이사회 결의 (가상)", 0, -202, 40, "#fff", 900)
                 + label("“Yale처럼 운용하라”", 0, -100, 52, PURPLE, 900)
                 + label("“지출 200억은 유지한다”", 0, -25, 44, NAVY, 900)
                 + f'<rect x="-340" y="45" width="680" height="130" rx="18" fill="#F4E9DC"/>'
                 + label("기금 5,000억 · 3년차 건축 목돈 600억", 0, 85, 32, "#555", 800)
                 + label("대체투자 전담 인력 1명", 0, 135, 32, "#555", 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("대체 60%!", 770, 975, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["대체투자를 60%로 올리면", "Yale처럼 벌겠네요!"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["Yale 모델은 대체 60%가 아니라", "지평 · 지출 · 접근권의 규율이야."], 540, 330, 1010, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=46))
    if t > 3.2:
        s.append(punch("세 숫자 (x, y, z)!", 540, 1650, 110, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


COLX = [200, 420, 640, 870]
ROWS = [("Yale형", "(60, 15, 5.25)", "2년", "부결", RED),
        ("GPFG형", "(0, 35, 4.0)", "22년", "통과 · 여유 없음", GOLD),
        ("기본 답", "(20, 30, 4.5)", "13년", "조건부 승인", GREEN)]


def cut4(t):   # 해설: 좌표표 → 결과 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("좌표로 재기", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("x 비유동 상한 · y 안전 유동 하한 · z 지출률 (%) · H대는 가상", 540, 275, 32, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}">' + label("이름", COLX[0], 390, 28, NAVY, 900) + label("(x, y, z)", COLX[1], 390, 28, NAVY, 900)
             + label("생존 연수 ≥ 10", COLX[2], 390, 28, NAVY, 900) + label("판정", COLX[3], 390, 28, NAVY, 900)
             + f'<line x1="80" y1="420" x2="1000" y2="420" stroke="{NAVY}" stroke-width="3"/></g>')
    for r, (name, xyz, yrs, verdict, c) in enumerate(ROWS):
        y = 470 + 72 * r
        g = ease_out(prog(t, 1.0 + .9 * r, .4))
        s.append(f'<g opacity="{g:.2f}">' + label(name, COLX[0], y, 32, c, 900) + label(xyz, COLX[1], y, 30, NAVY, 800)
                 + label(yrs, COLX[2], y, 34, c, 900) + "</g>")
        s.append(f'<g opacity="{ease_out(prog(t, 1.4 + .9 * r, .4)):.2f}">' + label(verdict, COLX[3], y, 28 if r == 1 else 32, c, 900) + "</g>")
    s.append(chip("Yale 441억 달러 · 지출률 5.25% · 2025 PE 세컨더리 약 25억 달러 매각", 540, 720, PURPLE, back(prog(t, 4.0, .4)), w=940, size=26))
    for i, (y, sc) in enumerate(((790, .46), (885, .48), (1000, .48))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.8 + .8 * i, .5)), scale=sc))
    s.append(f'<g opacity="{ease_out(prog(t, 7.2, .4))}">' + label("① 예금 − 물가 − 지출 = 실질 잠식  ② 지출 3년 + 목돈 ÷ 국채 −12%  ③ 실질가치 유지 확률", 540, 1120, 22, GREY, 800) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("영구 기관도 버틸 수 있는 연수까지만", 540, 1360, 46, RED, 900)
             + label("비유동을 담는다", 540, 1425, 46, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("철학의 이름이 아니라 세 숫자를 표결한다", 540, 1500, 34, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["목돈 600억이 3년 뒤에 나가.", "10년 묶이는 돈을 60%나 못 담지."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=40))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 분모 효과 시 신규 약정 중단 · 연 1회 재계산", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=35)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["Yale처럼 5.25%를", "쓰면 왜 안 돼요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["x 20에서 실질가치를 지킬 확률이 46%야.", "4.5%면 59%. Yale도 2025년엔 팔았어."], 540, 1720, 1020, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=42))
    if t > 3.6:
        s.append(punch("Yale도 팔았다!", 540, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def cut6(t):   # 시즌 종료 + W07 예고
    s = [bg(NAVY, "dotsW")]
    s.append(punch("시즌 2 끝!", 540, 520, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("지킬 것부터 사라", 540, 800, 110, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("다음 시즌: W07 동적 포트폴리오와 장기투자", 540, 1020, 44, "#fff", 800) + "</g>")
    s.append(penguin(380, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .6, "happy"))
    s.append(owl(720, 1610 + (1 - ease_out(prog(t, 1.6, .6))) * 400, .6, blink=(2.6 < t < 2.75)))
    return s


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_epB3.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
