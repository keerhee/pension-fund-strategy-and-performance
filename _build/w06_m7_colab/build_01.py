# -*- coding: utf-8 -*-
from nbhelp import M, C, build, badge

F = "01_부채와_적립비율.ipynb"
title = M(f"""
# 01 · 부채와 적립비율 — 부채는 할인된 약속

{badge(F)}

**W06 M7 LDI 강의본 단원 ①(10~17장)** 과 도입의 메시지(5장)를 손계산 순서 그대로 재현합니다. 장 번호는 강의본 PDF 쪽번호(83장)입니다.

| 단계 | 강의 | 이 노트북에서 |
|---|---|---|
| 할인 = 복리를 거꾸로 | 12장 | 104 ÷ 1.04 = 100 · 108.16 ÷ 1.04² = 100 |
| 부채 = 할인된 약속 | 13장 | 3년간 매년 30, 할인율 4% → 28.85 · 27.74 · 26.67 · L = 83.25 · 연금현가 2.775 |
| 적립비율 · 잉여금 | 14 · 15장 | A 100 · L 80 → FR 125% · S 20 |
| 1년 뒤 적립비율 | 16장 | 자산 +7% · 부채 +10% → 107 ÷ 88 = 121.6%(정확) vs 121.25%(근사) · −3.4%p |
| 잉여금 수익률 | 17장 | R_S = r_A − (L/A) r_L = 7 − 8 = −1% · 잉여금 20 → 19 |
| "자산 +7.5%인데 나쁜 해" | 5 · 11장 | 자산 +7.5% · 부채 +15% → FR 하락 |

위에서부터 순서대로 실행하면 됩니다. 계산은 가벼워 몇 초 안에 끝납니다.
""")

cells = [
M("""
## 1. 할인 — 복리로 불리기를 거꾸로 (강의 12장)
오늘 P를 금리 r로 t년 맡기면 P(1 + r)ᵗ. 거꾸로 t년 뒤의 금액 CF를 오늘 값으로 바꾸면 **PV = CF ÷ (1 + r)ᵗ** 입니다.
강의 숫자: 금리 4%에서 104 ÷ 1.04 = 100, 108.16 ÷ 1.04² = 100.
"""),
C("""
def pv(cf, r, t):
    \"\"\"t년 뒤 cf의 현재가치 — 이산복리\"\"\"
    return cf / (1 + r) ** t

r = 0.04
print(f"100을 1년 맡기면 {100 * (1 + r):.2f} · 2년 맡기면 {100 * (1 + r)**2:.2f}")
print(f"거꾸로: 104 ÷ 1.04 = {pv(104, r, 1):.2f} · 108.16 ÷ 1.04² = {pv(108.16, r, 2):.2f}")
check("104 ÷ 1.04", pv(104, r, 1), 100, 0.005, ".2f")
check("108.16 ÷ 1.04²", pv(108.16, r, 2), 100, 0.005, ".2f")
"""),
M("""
## 2. 연금 부채 = 해마다 줄 금액을 각각 할인해 더한 값 (강의 13장)
3년간 매년 30을 지급하고 할인율이 4%이면 L = 30/1.04 + 30/1.04² + 30/1.04³.
같은 금액이 반복되면 **연금현가 공식** L = CF × (1 − (1 + r)⁻ᵀ) ÷ r 로 한 번에 계산합니다.
"""),
C("""
CF, T = 30.0, 3
rows = [(t, CF, pv(CF, r, t)) for t in range(1, T + 1)]
print(f"{'시점':>6s} {'지급':>6s} {'현재가치':>9s}")
for t, c, v in rows:
    print(f"{t:>4d}년 {c:6.0f} {v:9.2f}")
L3 = sum(v for *_, v in rows)
annuity = (1 - (1 + r) ** -T) / r
print(f"합계 지급 {CF * T:.0f} → L = {L3:.2f} · 연금현가 계수 {annuity:.3f} × 30 = {CF * annuity:.2f}")
print(f"이자가 채우는 몫 = {CF * T - L3:.2f}")
for (t, _, v), lec in zip(rows, [28.85, 27.74, 26.67]):
    check(f"{t}년 뒤 30의 현재가치", v, lec, 0.005, ".2f")
check("부채 L (3년 연금)", L3, 83.25, 0.005, ".2f")
check("연금현가 계수", annuity, 2.775, 0.0005, ".3f")
check("이자가 채우는 몫", CF * T - L3, 6.75, 0.005, ".2f")
"""),
M("""
**그래프 — 줄 금액과 그 현재가치.** 같은 30이라도 멀수록 오늘 값이 작습니다(막대의 빈 부분 = 이자가 채우는 몫).
"""),
C("""
fig, ax = plt.subplots(figsize=(7, 3.8))
ts = [t for t, *_ in rows]; pvs = [v for *_, v in rows]
ax.bar(ts, [CF] * T, 0.55, color="white", edgecolor=INK, lw=1.2, label="줄 금액 30")
ax.bar(ts, pvs, 0.55, color=TEAL, edgecolor=INK, label="현재가치 (할인율 4%)")
for t, v in zip(ts, pvs):
    ax.text(t, v / 2, f"{v:.2f}", ha="center", va="center", color="white", fontweight="bold")
    ax.text(t, CF + 0.6, f"이자 몫 {CF - v:.2f}", ha="center", fontsize=9, color=RED)
ax.set_xticks(ts, [f"{t}년 뒤" for t in ts]); ax.set_ylim(0, 42)
ax.set_ylabel("금액"); ax.set_xlabel("지급 시점")
ax.set_title(f"3년 연금 — 줄 금액 90, 오늘 필요한 금액 L = {L3:.2f}")
ax.legend(loc="upper right", ncol=2)
plt.show()
"""),
M("""
## 3. 적립비율과 잉여금 (강의 14 · 15장)
**적립비율 FR = A / L** (줄 금액의 몇 배를 가졌나), **잉여금 S = A − L** (버틸 여유). 강의 기금: 자산 A = 100, 부채 L = 80.
FR ≥ 100%면 적립, 미만이면 미적립입니다. ※ 국민연금이 공시하는 **적립배율**(적립금 ÷ 그해 지출)은 적립비율과 다른 지표입니다.
"""),
C("""
A0, L0 = 100.0, 80.0
FR0, S0 = A0 / L0, A0 - L0
print(f"A = {A0:.0f} · L = {L0:.0f} → FR = {FR0:.0%} · S = {S0:.0f} → {'적립' if FR0 >= 1 else '미적립'}")
check("적립비율 FR (%)", 100 * FR0, 125, 0.5, ".1f")
check("잉여금 S", S0, 20, 0.5, ".1f")
"""),
M("""
## 4. 1년 뒤 적립비율 — 자산 수익률에서 부채 수익률을 뺀 만큼 (강의 16장)
FR₁ = A(1 + r_A) ÷ L(1 + r_L) ≈ FR(1 + r_A − r_L), 즉 **ΔFR ≈ FR × (r_A − r_L)**.
r_L은 시간 이자와 금리 변화에 따른 재평가를 합친 부채의 변화율입니다. 자산 +7%, 부채 +10%이면?
"""),
C("""
rA, rL = 0.07, 0.10
A1, L1 = A0 * (1 + rA), L0 * (1 + rL)
FR1_exact = A1 / L1
FR1_approx = FR0 + FR0 * (rA - rL)
print(f"새 자산 {A1:.0f} · 새 부채 {L1:.0f}")
print(f"새 적립비율 (정확) {A1:.0f} ÷ {L1:.0f} = {FR1_exact:.1%}")
print(f"근사식 125% × (7% − 10%) = {FR0 * (rA - rL) * 100:+.2f}%p → {FR1_approx:.2%}")
print(f"7%를 벌고도 적립비율이 {100 * (FR0 - FR1_exact):.1f}%p 떨어졌다")
check("새 자산", A1, 107, 0.5, ".1f")
check("새 부채", L1, 88, 0.5, ".1f")
check("새 적립비율 정확 (%)", 100 * FR1_exact, 121.6, 0.05, ".2f")
check("근사 ΔFR (%p)", 100 * FR0 * (rA - rL), -3.75, 0.005, ".2f")
check("근사 적립비율 (%)", 100 * FR1_approx, 121.25, 0.005, ".2f")
check("적립비율 하락 (%p)", 100 * (FR0 - FR1_exact), 3.4, 0.05, ".2f")
"""),
M("""
## 5. 성적표 한 숫자 — 잉여금 수익률 R_S (강의 17장)
잉여금 변화 = 자산이 번 금액 − 부채가 늘어난 금액. 이를 자산으로 나누면

**R_S = ΔS / A = r_A − (L/A) · r_L**

연기금의 성적표는 r_A가 아니라 R_S입니다.
"""),
C("""
def surplus_return(rA, rL, A, L):
    return rA - (L / A) * rL

RS = surplus_return(rA, rL, A0, L0)
S1 = A1 - L1
print(f"R_S = {rA:.0%} − ({L0 / A0:.1f}) × {rL:.0%} = {RS:+.1%}")
print(f"검산: 잉여금 {S0:.0f} → {S1:.0f} (= {A1:.0f} − {L1:.0f}), 변화 {S1 - S0:+.0f} = R_S × A {RS * A0:+.0f}")
check("L/A", L0 / A0, 0.8, 0.05, ".2f")
check("잉여금 수익률 R_S (%)", 100 * RS, -1, 0.5, ".2f")
check("1년 뒤 잉여금", S1, 19, 0.5, ".1f")
"""),
M("""
## 6. "자산 +7.5%인데 나쁜 해" (강의 5 · 11장)
할인율이 3% → 2%로 내려 부채가 +15% 늘어난 해. 운용역은 "자산 +7.5%"를 보고하고, 이사회는 "부채는 +15%"를 묻습니다.
같은 기금(A 100 · L 80)에 넣어 보면 적립비율과 잉여금 수익률은?

부채가 +15% 늘려면 듀레이션이 얼마여야 하나도 함께 봅니다 — 할인율 3% → 2%에서 t년 뒤 한 번 지급하는 약속은 (1.03/1.02)ᵗ배가 됩니다.
"""),
C("""
rA, rL = 0.075, 0.15
FR_b = A0 * (1 + rA) / (L0 * (1 + rL))
RS_b = surplus_return(rA, rL, A0, L0)
print(f"자산 +7.5% · 부채 +15% → FR {FR0:.0%} → {FR_b:.1%} ({100 * (FR_b - FR0):+.1f}%p) · R_S = {RS_b:+.1%}")
t15 = math.log(1.15) / math.log(1.03 / 1.02)
print(f"할인율 3% → 2%에 부채 +15%가 되는 단일 지급 시점 ≈ {t15:.1f}년 — 강의(5장)가 말하는 부채 듀레이션 15~25년의 아래쪽 끝")
check("자산 +7.5%여도 FR 하락", float(FR_b < FR0), 1, 0, ".0f")
"""),
M("""
## 7. 그래프 — 자산 수익률 · 부채 수익률 평면의 적립비율 변화
가로축 자산 수익률, 세로축 부채 수익률. 대각선(r_A = r_L) 위쪽은 적립비율이 나빠지는 영역입니다.
강의의 두 점(16장 · 11장)이 모두 "벌었지만 나쁜 해" 쪽에 있습니다.
"""),
C("""
ra = np.linspace(-0.10, 0.20, 200); rl = np.linspace(-0.10, 0.20, 200)
RA, RL = np.meshgrid(ra, rl)
dFR = 100 * (A0 * (1 + RA) / (L0 * (1 + RL)) - FR0)
fig, ax = plt.subplots(figsize=(7.5, 5.2))
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("lec", [RED, "#F2C4C4", IVORY, "#BFE3DF", TEAL])
cs = ax.contourf(RA * 100, RL * 100, dFR, levels=np.arange(-40, 41, 5), cmap=cmap, alpha=0.85)
ax.contour(RA * 100, RL * 100, dFR, levels=[0], colors=INK, linewidths=1.5)
cb = fig.colorbar(cs, ax=ax); cb.set_label("적립비율 변화 (%p)")
for (x, y, lab) in [(7, 10, "16장: +7% / +10%\\n→ 121.6% (−3.4%p)"), (7.5, 15, "11장: +7.5% / +15%\\n→ " + f"{FR_b:.1%}")]:
    ax.scatter(x, y, s=90, color=LIME, edgecolor=INK, zorder=5, lw=1.5)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(10, 6), fontsize=9, color=INK)
ax.text(-8, 16, "부채가 더 많이 늘어난 해\\n= 적립비율 하락", color=RED, fontsize=10, fontweight="bold")
ax.text(9, -7, "부채보다 많이 번 해\\n= 적립비율 상승", color=TEAL, fontsize=10, fontweight="bold")
ax.set_xlabel("자산 수익률 r_A (%)"); ax.set_ylabel("부채 수익률 r_L (%)")
ax.set_title("좋은 해는 '부채보다 많이 번 해' — 출발 FR 125%")
plt.show()
"""),
M("""
## 8. 정리
- 부채는 관찰되지 않고 **할인율로 추정되는 할인된 약속**입니다. 같은 약속도 할인율에 따라 크기가 달라집니다 → 02 노트북.
- 성적표는 r_A가 아니라 **R_S = r_A − (L/A) r_L**. 부채 수익률 r_L의 대부분은 금리 변화에서 옵니다 → 03 노트북의 듀레이션.
"""),
]

ex = [
    "3년 연금(매년 30)을 할인율 3% · 5%로 다시 계산해 보라. 할인율 1%p가 부채를 몇 % 바꾸나? (`pv(30, 0.03, t)`)",
    "출발 FR이 80%(A 64 · L 80)인 기금이 자산 +7% · 부채 +10%를 겪으면 적립비율은 몇 %p 바뀌나? FR 125%일 때(−3.4%p)와 비교하라.",
    "잉여금 수익률이 0이 되려면 부채 +10%인 해에 자산이 몇 % 벌어야 하나? (`surplus_return(rA, 0.10, 100, 80) = 0`을 rA로 풀기)",
]

if __name__ == "__main__":
    build(F, title, cells, ex)
