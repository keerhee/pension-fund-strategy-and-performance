"""EP.18 '키맨 조항' — 9:16 웹툰 숏폼.
약정 1,000 펀드의 공동대표 2명 중 1명이 3년차에 떠나면 Key Person Event로 투자기간이 정지된다.
미투자 약정 400이 묶이고, 재개에는 약정 기준 2/3 동의가 필요한데 A 30% + B 25% = 55%라 정지가 유지된다.
정지 중 관리보수는 투자액 600 기준 12로 줄어든다(종전 약정 기준 20). (EP.13 '사람이 자산'과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep18_{i}.png" for i in (1, 2, 3)]
BASE = 820


def cut1(t): return title_cut(t, "EP.18 · 키맨 조항")


def cut2(t):
    return problem_cut(t, "#E3F1EF", "대표가 퇴사!", TEAL, "Key Person Event 통지", TEAL, "공동대표 2명 중 1명 퇴사 · 3년차",
                       ("남은 대표", "1명", NAVY, 90), ("투자기간", "정지", RED, 90), "별일 아니죠?",
                       ["한 명 나갔을 뿐인데,", "별일 아니죠?"], sfx_size=76, mood="happy", bubble_size=56, bubble_w=800)


def cut3(t):
    return twist_cut(t, ["LPA에 그 사람 이름이 박혀 있어.", "떠나면 투자기간이 자동으로 멈추지."], "투자 정지!", size=46, sfx_size=160)


def cut4(t):
    s = explain_frame(t, "무엇이 멈추나", "약정 1,000 · 3년차까지 600 투자 · 재개 정족수 2/3 (예시)")
    s.append(f'<line x1="100" y1="{BASE}" x2="980" y2="{BASE}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>')
    k = .4                                     # 약정 1 = 0.4px (1,000 → 400px)
    g = ease_out(prog(t, .6, .5)); h = 600 * k * g
    s.append(f'<rect x="170" y="{BASE-h:.0f}" width="220" height="{h:.0f}" fill="{NAVY}"/>')
    if g > .9: s.append(label("투자 600", 280, BASE - 120, 40, "#fff", 900))
    g2 = ease_out(prog(t, 1.4, .5)); h2 = 400 * k * g2
    s.append(f'<rect x="170" y="{BASE-600*k-h2:.0f}" width="220" height="{h2:.0f}" fill="{GREY}"/>')
    if g2 > .9:
        s.append(label("미투자 400", 280, BASE - 600 * k - 95, 36, "#fff", 900) + label("(정지)", 280, BASE - 600 * k - 45, 34, "#fff", 900))
        s.append(label("약정 1,000", 280, BASE - 1000 * k - 28, 36, NAVY, 900) + label("① 약정", 280, BASE + 42, 34, NAVY, 900))
    # ② 재개 투표: 55% vs 2/3
    kv = 4.6                                   # 1%p = 4.6px (100% → 460px)
    for i, (who, v, c, a0) in enumerate((("A 30%", 30, GREEN, 2.6), ("B 25%", 25, TEAL, 3.1))):
        lo = 0 if i == 0 else 30
        gv = ease_out(prog(t, a0, .45)); hv = v * kv * gv
        s.append(f'<rect x="650" y="{BASE-lo*kv-hv:.0f}" width="200" height="{hv:.0f}" fill="{c}"/>')
        if gv > .9: s.append(label(who, 750, BASE - (lo + v / 2) * kv, 34, "#fff", 900))
    if t > 3.7:
        a = ease_out(prog(t, 3.7, .4)); y = BASE - 66.7 * kv
        s.append(f'<line x1="610" y1="{y:.0f}" x2="{610 + 300*a:.0f}" y2="{y:.0f}" stroke="{RED}" stroke-width="6" stroke-dasharray="16 10"/>')
        if a > .9:
            s.append(label("재개 2/3", 750, y - 26, 32, RED, 900) + label("55% → 정지 유지", 750, BASE - 55 * kv - 26, 30, NAVY, 900))
    if t > 2.6: s.append(label("② 재개 투표", 750, BASE + 42, 34, NAVY, 900))
    s.append(chip("관리보수 20 → 12 (투자액 기준)", 540, 1000, TEAL, back(prog(t, 4.6, .4)), w=740, size=40))
    s += explain_tail(t, EQ, (1080, 1170, 1260), 5.6, "사람이 떠나면 돈도 멈춘다 — LP가 다시 고른다", 1470, 8.2,
                      ["EP.13에서 말했지.", "운용사의 자산은 사람이라고."], 9.0)
    return s


def cut5(t):
    return relief_cut(t, ["그럼 우리는", "뭘 해요?"], ["후임자를 보고 재개에 투표해.", "끝내 안 되면 펀드 해산까지 가지."], "의결권!",
                      "체크: 키맨 명단 · 시간 투입 조항 · 정지 범위 · 재개 정족수 · 보수 감액", chip_size=31, mood="happy")


def cut6(t): return next_cut(t, GOLD, "허들의 종류", "8%면 다 같은 8%?", topic_size=190)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep18.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
