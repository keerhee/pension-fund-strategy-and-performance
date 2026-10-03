"""시즌 2 「지킬 것부터 사라」 EP.B1 '3% · 5% · 30%' — 9:16 웹툰 숏폼. (IC 보너스 1 — W06 M7 케이스 제1호)
국민연금 LDI: 안 A 현행 헤지 3%(지표 없음) · 안 B 현물 30년물 131조 → 4.9%(시장 상한 ~5%) · 안 C IRS 명목 1,223조 → 30%.
부채 DV01 = 35년 × 2,122조 × 0.0001 = 7.43조/bp. C의 ΔDV01 = (0.30 − 0.03) × 7.43 = 2.01 → 3일 +200bp 증거금 401조 > 유동자산 123조.
판정 조건 ①~⑤: A ① 탈락 · B 전부 통과 · C ②③⑤ 탈락 → 기본 답 B 조건부. (케이스 덱 2~3장 · 판정표 그대로 — 학생 배포 덱에 공개된 결론)"""
from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/epB1_{i}.png" for i in (1, 2, 3)]   # latex_png()로 미리 생성


def cut1(t):
    s = title_cut(t, "EP.B1 · 3% · 5% · 30%", chip_w=720)
    s.insert(2, punch("시즌 2 · IC 보너스", 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def cut2(t):   # 문제: 하느냐 마느냐로 표결?
    s = [bg("#E6ECF7")]
    s.append(punch("LDI 할까 말까?", 540, 170, 110, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{NAVY}"/><rect x="-390" y="-180" width="780" height="26" fill="{NAVY}"/>'
                 + label("IC 제1호 · 국민연금 기금의 LDI", 0, -202, 42, "#fff", 900)
                 + label("부채 2,122조 · 듀레이션 35년 · 적립비율 69%", 0, -105, 34, NAVY, 800)
                 + f'<rect x="-330" y="-40" width="300" height="160" rx="18" fill="{GREEN}"/><rect x="30" y="-40" width="300" height="160" rx="18" fill="{RED}"/>'
                 + label("찬성", -180, 40, 64, "#fff", 900) + label("반대", 180, 40, 64, "#fff", 900)
                 + label("펭이 만든 투표 용지", 0, 170, 34, GREY, 800)
                 + '</g>')
    if t > 2.0:
        inner.append(punch("둘 중 하나!", 770, 975, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    inner.append(penguin(380, 1290, .7, "happy" if t < 2.6 else "worry"))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["LDI를 하자, 말자로", "표결하면 되는 거죠?"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s


def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["‘하느냐’가 아니라 몇 %를, 무엇으로,", "얼마의 버퍼로 하느냐를 표결하는 거야."], 540, 330, 1030, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=42))
    if t > 3.2:
        s.append(punch("몇 % · 무엇 · 버퍼!", 540, 1650, 106, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


COLX = [215, 450, 670, 890]
HEAD = [("", NAVY), ("안 A 현행", GREY), ("안 B 시장 상한", GREEN), ("안 C 오버레이", RED)]
ROWS = [("헤지 비율", ["3%", "4.9%", "30%"]),
        ("수단", ["추가 없음", "30년물 131조", "IRS 1,223조"]),
        ("3일 +200bp 증거금", ["0", "0", "401조 > 123조"]),
        ("판정 ①~⑤", ["① 탈락", "전부 통과", "②③⑤ 탈락"])]


def cut4(t):   # 해설: 안 A·B·C 표 → 조건 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("세 안 비교", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("국민연금 LDI 모의 IC · 기준일 2026.9.21 (케이스)", 540, 275, 34, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    a = ease_out(prog(t, .5, .4))
    s.append(f'<g opacity="{a:.2f}">' + "".join(label(h, x, 390, 28, c, 900) for (h, c), x in zip(HEAD, COLX))
             + f'<line x1="80" y1="420" x2="1000" y2="420" stroke="{NAVY}" stroke-width="3"/></g>')
    for r, (name, vals) in enumerate(ROWS):
        y = 465 + 68 * r
        g = ease_out(prog(t, 1.0 + .7 * r, .4))
        o = label(name, COLX[0], y, 26, NAVY, 900)
        for j, v in enumerate(vals):
            c = [GREY, GREEN, RED][j] if r in (0, 3) or (r == 2 and j == 2) else NAVY
            o += label(v, COLX[j + 1], y, 26 if r == 1 else 30, c, 900 if r != 1 else 800)
        s.append(f'<g opacity="{g:.2f}">{o}</g>')
    s.append(f'<g opacity="{ease_out(prog(t, 3.8, .4)):.2f}">' + label("(123조 = 유동자산)", COLX[3], 760 - 42, 20, GREY, 800) + "</g>")
    s.append(chip("① 갭 실재 ② 시장 수용 ③ 유동성 버퍼 ④ 허들 5.5% ⑤ 지침", 540, 790, NAVY, back(prog(t, 4.2, .4)), w=920, size=30))
    for i, (y, sc) in enumerate(((855, .46), (950, .46), (1045, .48))):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.0 + .8 * i, .5)), scale=sc))
    s.append(chip("기본 답: 안 B 조건부 (케이스 덱)", 540, 1200, GREEN, back(prog(t, 7.4, .4)), w=640, size=34))
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .5))}">' + label("‘하느냐’가 아니라 몇 %·무엇으로·얼마의 버퍼로", 540, 1400, 42, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("헤지 못 한 95%의 금리 위험은 누가 지나 — 의결문에 적는다", 540, 1480, 30, NAVY, 800) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)))
    s.append(bubble(["EP.04의 DV01과 EP.06의 버퍼가", "그대로 판정 조건이 돼."], 650, 1710, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=44))
    return s


def cut5(t):   # 후속 질문 + 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 헤지 비율 · 수단 · 시장 상한 · 증거금 ÷ 유동자산 · 지침", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=940, size=32)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["30%로 크게 하면", "더 좋은 거 아니에요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["증거금 401조를 유동자산 123조로", "못 내. EP.06 영국과 같은 길이야."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.6:
        s.append(punch("버퍼가 먼저!", 330, 740, 110, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def cut6(t): return next_cut(t, GREEN, "Flexicure 표결", "디폴트옵션에 넣어도 될까?", topic_size=130)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_s2_epB1.mp4",
        [2.8, 9.9, 16.5, 30.5, 37.5, 41.0])
