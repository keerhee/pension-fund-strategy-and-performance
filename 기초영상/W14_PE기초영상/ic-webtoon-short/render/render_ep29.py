"""EP.29 '테일엔드' — 9:16 웹툰 숏폼.
12년차, 잔여 NAV 30 중 우리 몫 3(10%). 3년 더 들고 가면 가치 10% 상승 3.3에서 관리 비용 0.3 × 3 = 0.9를 빼 2.4,
테일엔드 세컨더리에 85%로 팔면 2.55. 작은 잔여 지분은 관리비가 수익을 먹는다 — 정리도 운용이다. (EP.07 · EP.28과 연결)"""
from pe_common import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 30), (30, 37), (37, 40.5)]
DUR = 40.5
EQ = [f"eq/ep29_{i}.png" for i in (1, 2, 3)]
BASE, K = 840, 110          # 1 = 110px (3.3 → 363px)


def cut1(t): return title_cut(t, "EP.29 · 테일엔드")


def cut2(t):
    return problem_cut(t, "#ECEEF2", "조금 남았는데?", ORANGE, "12년차 보고서 · 펀드 1호", NAVY, "잔여 회사 5개 · 남은 NAV 30",
                       ("우리 몫", "3", GREEN, 100), ("남은 기간", "3년+", GOLD, 80), "끝까지!",
                       ["조금 남았으니", "끝까지 들고 가죠!"], sfx_size=90, mood="happy", bubble_size=56, bubble_w=760, title_size=100)


def cut3(t):
    return twist_cut(t, ["남은 게 작아도 보고서·감사·관리 비용은", "그대로 들어. 꼬리가 몸통을 흔들지."], "꼬리가 무겁다!", size=42, sfx_size=130)


def cut4(t):
    s = explain_frame(t, "들고 갈까, 팔까", "우리 몫 3 · 3년 보유 시 +10% · 관리 비용 연 0.3 (예시)")
    s.append(baseline(t, BASE))
    s.append(vbar(t, .6, 230, 3.3, K, BASE, GREY, "3.3", ("가치 +10%",), w=170))
    s.append(vbar(t, 1.4, 540, 2.4, K, BASE, ORANGE, "2.4", ("① 3년 보유", "− 비용 0.9"), w=170))
    s.append(vbar(t, 2.2, 850, 2.55, K, BASE, GREEN, "2.55", ("② 지금 매각", "85%"), w=170))
    if t > 3.0:
        a = ease_out(prog(t, 3.0, .4))
        s.append(f'<g opacity="{a:.2f}">' + label("비용 −0.9", 385, BASE - 3.0 * K, 32, RED, 900) + "</g>")
    s.append(chip("작은 꼬리는 관리비가 수익을 먹는다", 540, 1020, NAVY, back(prog(t, 3.8, .4)), w=780, size=40))
    s += explain_tail(t, EQ, (1095, 1185, 1275), 4.8, "정리도 운용이다 — 테일엔드는 묶어서 판다", 1480, 7.6,
                      ["EP.28 연장의 끝에서", "흔히 만나는 선택이지."], 8.4)
    return s


def cut5(t):
    return relief_cut(t, ["누가 이런 걸", "사요?"], ["테일엔드 전문 세컨더리 펀드가 있어.", "여러 펀드 꼬리를 할인해서 묶어 사지."], "묶어서 판다!",
                      "체크: 잔여 NAV · 관리 비용 · 할인율 · 남은 기간 · GP 동의", chip_size=34, mood="happy", sfx_size=96)


def cut6(t): return next_cut(t, BLUE, "공정가치 평가", "PE 회사 값은 누가 매기나?", topic_size=170)


if __name__ == "__main__":
    run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "../output/ic_webtoon_ep29.mp4",
        [2.8, 9.9, 16.5, 29.5, 36.5, 40.0])
