# -*- coding: utf-8 -*-
from nbhelp import M, C, build, badge

F = "04_면역화_Redington.ipynb"
title = M(f"""
# 04 · 면역화와 Redington — 수학적 방패

{badge(F)}

**W06 M7 LDI 강의본 단원 ④(37~44장)** 와 부록 B-3(80 · 81장)을 재현합니다.

| 단계 | 강의 | 이 노트북에서 |
|---|---|---|
| 잉여금 전개식 · 세 조건(금액 꼴) | 38 · 39장 | ΔS ≈ −(D_A·A − D_L·L)Δy + ½(C_A·A − C_L·L)Δy² · A = L · D_A·A = D_L·L · C_A·A > C_L·L |
| 1차 효과 | 40장 | 지금 기금 금리 −1%p: −(300 − 1,600) × (−0.01) = −13 |
| 바벨 검증 | 39 · 41 · 81장 | 부채 10년 뒤 100(PV 60.65) · 바벨 5년 38.94 + 15년 64.20(D 10 · C 125) vs 불일치 5년 77.88(D 5) · −2%p에서 +0.37 vs −7.05 · 금리별 표 |
| 증명 | 80장(B-3) | a ≠ 0이면 반례 · a = 0이면 b ≥ 0 · S ≥ 0 |
| 한계 | 44장 | 큰 충격(3차 이상 항) · 시간이 지나면 다시 맞춘다 · 비평행 이동 · 30·50년 국고채 437조 vs 순부채 2,122조 |

계산은 강의와 같이 **연속복리 y = 5%** 입니다.
""")

cells = [
M("""
## 1. 잉여금 전개식과 세 조건 (강의 38 · 39장)
자산 · 부채를 각각 테일러 전개(03 노트북)해 빼면

**ΔS = ΔA − ΔL ≈ −(D_A·A − D_L·L)·Δy + ½·(C_A·A − C_L·L)·(Δy)²**

Redington(1952): 1차 항을 0으로, 2차 항을 양수로. 세 조건은 모두 **금액(×A, ×L) 꼴**입니다.

| 조건 | 식 | 막는 것 |
|---|---|---|
| 1 현재가치 일치 | A = L (실무: A ≥ L) | 출발선 부족 |
| 2 듀레이션 일치 | D_A·A = D_L·L | 1차 항(방향) |
| 3 볼록성 우위 | C_A·A > C_L·L | 2차 항(휘어짐) |

A = L일 때만 A · L이 약분되어 '자산 D = 부채 D · 자산 C > 부채 C'로 줄어듭니다.
"""),
C("""
def dS_approx(A, DA, CA, L, DL, CL, dy):
    \"\"\"잉여금 변화의 2차 근사 — 첫 항(1차, 방향) + 둘째 항(2차, 휘어짐)\"\"\"
    first = -(DA * A - DL * L) * dy
    second = 0.5 * (CA * A - CL * L) * dy**2
    return first, second

# 강의 40장 — 지금 기금(A 100 · D_A 3, L 80 · D_L 20), 금리 −1%p, 1차 항만
first, _ = dS_approx(100, 3, 0, 80, 20, 0, -0.01)
print(f"자산 금액 듀레이션 {3 * 100} · 부채 금액 듀레이션 {20 * 80}")
print(f"첫 항 = −(300 − 1,600) × (−0.01) = {first:+.0f}  ← 03 노트북의 DV01 차이 −0.13 × 100bp와 같다")
check("지금 기금 1차 효과 (금리 −1%p)", first, -13, 0.5, ".1f")
"""),
M("""
## 2. 바벨 검증 — 같은 PV 60.65의 두 자산 (강의 39 · 41 · 81장)
부채: 10년 뒤 100, y = 5% 연속복리 → L = 100·e^(−0.5) = 60.65, D_L = 10, C_L = 100.
- **바벨**: 5년물과 15년물에 현재가치를 반반(30.33씩) → 액면 5년 38.94 + 15년 64.20, D = 10, C = 10² + 5² = 125
- **불일치**: 5년물 하나에 전부 → 액면 77.88, D = 5 (조건 2 위반)
"""),
C("""
y0 = 0.05
L_face, L_t = 100.0, 10
def price(flows, y):
    \"\"\"[(만기, 액면), ...]의 연속복리 현재가치\"\"\"
    return sum(f * np.exp(-y * t) for t, f in flows)

L0 = price([(L_t, L_face)], y0)
half = L0 / 2
barbell = [(5, half * np.exp(y0 * 5)), (15, half * np.exp(y0 * 15))]
mismatch = [(5, L0 * np.exp(y0 * 5))]

def dur_conv(flows, y):
    V = price(flows, y)
    D = sum(t * f * np.exp(-y * t) for t, f in flows) / V
    Cx = sum(t * t * f * np.exp(-y * t) for t, f in flows) / V
    return V, D, Cx

for name, fl in [("부채 10년 불릿", [(L_t, L_face)]), ("바벨 5 + 15년", barbell), ("불일치 5년", mismatch)]:
    V, D, Cx = dur_conv(fl, y0)
    print(f"{name:12s} 액면 {' + '.join(f'{t}년 {f:.2f}' for t, f in fl):24s} PV {V:.2f} · D {D:.1f} · C {Cx:.0f}")
check("부채 PV", L0, 60.65, 0.005, ".2f")
check("바벨 5년 액면", barbell[0][1], 38.94, 0.005, ".2f")
check("바벨 15년 액면", barbell[1][1], 64.20, 0.005, ".2f")
check("바벨 D", dur_conv(barbell, y0)[1], 10, 0.05, ".2f")
check("바벨 C", dur_conv(barbell, y0)[2], 125, 0.5, ".1f")
check("불일치 5년 액면", mismatch[0][1], 77.88, 0.005, ".2f")
check("불일치 D", dur_conv(mismatch, y0)[1], 5, 0.05, ".2f")
"""),
M("""
**세 조건 확인.** 바벨은 조건 1 · 2 · 3을 모두 지키고, 불일치는 조건 2를 어깁니다.
"""),
C("""
for name, fl in [("바벨", barbell), ("불일치", mismatch)]:
    A, DA, CA = dur_conv(fl, y0)
    c1 = abs(A - L0) < 1e-9; c2 = abs(DA * A - 10 * L0) < 1e-6; c3 = CA * A > 100 * L0
    print(f"{name:4s} 조건 1 A = L: {'✓' if c1 else '✗'} · 조건 2 D_A·A = D_L·L ({DA * A:.1f} vs {10 * L0:.1f}): {'✓' if c2 else '✗'} · "
          f"조건 3 C_A·A > C_L·L ({CA * A:.0f} vs {100 * L0:.0f}): {'✓' if c3 else '✗'}")
"""),
M("""
**금리별 표 (강의 81장).** 금리가 평행 이동한 뒤 다시 할인해 잉여금 S = A − L(출발 0)을 구하고, 2차 근사 ΔS = ½ × 25 × 60.65 × Δy²와 비교합니다.
"""),
C("""
LECT = {-0.02: (74.08, 74.45, 0.37, 0.30, -7.05), -0.01: (67.03, 67.12, 0.08, 0.08, -3.27),
        +0.01: (54.88, 54.95, 0.07, 0.08, 2.81), +0.02: (49.66, 49.91, 0.25, 0.30, 5.22)}
print(f"{'Δy':>6s} {'부채 L':>8s} {'바벨 A':>8s} {'바벨 S':>8s} {'근사 ΔS':>8s} {'불일치 S':>9s}")
for dy, lec in LECT.items():
    Ld = price([(L_t, L_face)], y0 + dy); Ab = price(barbell, y0 + dy); Am = price(mismatch, y0 + dy)
    approx = 0.5 * (125 - 100) * L0 * dy**2
    row = (Ld, Ab, Ab - Ld, approx, Am - Ld)
    print(f"{dy * 100:+5.0f}%p {row[0]:8.2f} {row[1]:8.2f} {row[2]:+8.2f} {row[3]:+8.2f} {row[4]:+9.2f}")
    for lab, v, l in zip(["부채 L", "바벨 A", "바벨 S", "근사 ΔS", "불일치 S"], row, lec):
        check(f"Δy {dy * 100:+.0f}%p {lab}", v, l, 0.005, "+.2f")
"""),
C("""
dys = np.linspace(-0.03, 0.03, 121)
Sb = np.array([price(barbell, y0 + d) - price([(L_t, L_face)], y0 + d) for d in dys])
Sm = np.array([price(mismatch, y0 + d) - price([(L_t, L_face)], y0 + d) for d in dys])
fig, ax = plt.subplots(figsize=(8.5, 4.4))
ax.plot(dys * 100, Sb, color=TEAL, lw=2.4, label="바벨 (5년 + 15년, D = 10, C = 125)")
ax.plot(dys * 100, Sm, color=RED, lw=2, ls="--", label="불일치 (5년 한 번, D = 5)")
ax.axhline(0, color=GRAY, lw=0.8)
ax.annotate("어느 쪽으로 움직여도 ≥ 0", (0, 0.05), textcoords="offset points", xytext=(-80, 18), color=TEAL, fontweight="bold")
for d in [-0.02, 0.02]:
    i = np.argmin(abs(dys - d))
    ax.scatter(d * 100, Sb[i], color=LIME, edgecolor=TEAL, zorder=5)
    ax.scatter(d * 100, Sm[i], color=LIME, edgecolor=RED, zorder=5)
ax.annotate(f"−2%p: 바벨 {Sb[np.argmin(abs(dys + 0.02))]:+.2f}\\n불일치 {Sm[np.argmin(abs(dys + 0.02))]:+.2f}", (-2, Sm[np.argmin(abs(dys + 0.02))]),
            textcoords="offset points", xytext=(15, -5), fontsize=9, color=INK)
ax.set_ylim(-9, 6)
ax.set_xlabel("금리 변화 Δy (%p)"); ax.set_ylabel("잉여금 변화 ΔS")
ax.set_title("부채를 양쪽에서 감싸는 바벨은 면역되고, 짧은 자산은 금리 하락에 무너진다")
ax.legend(loc="lower right")
plt.show()
"""),
M("""
## 3. 부록 B-3 — 왜 세 조건인가 (강의 80장)
ΔS ≈ −a·Δy + ½·b·Δy², a = D_A·A − D_L·L, b = C_A·A − C_L·L.
- a ≠ 0이면 Δy가 작을 때 −a·Δy가 Δy²항을 이겨 **한쪽 방향에서 ΔS < 0** (반례). 불일치 자산은 a = (5 − 10) × 60.65 < 0 → 금리가 내리면 손실.
- a = 0이면 ΔS ≈ ½·b·Δy² → b ≥ 0이어야 어느 쪽에서도 손실이 없다.
- 출발점 S ≥ 0(A ≥ L)이면 S(y + Δy) = S + ΔS ≥ S ≥ 0 — 미분 언어로 S′(y) = 0, S″(y) ≥ 0, 골짜기 바닥.

아래에서 아주 작은 Δy(±1bp)로 반례를 확인합니다.
"""),
C("""
for name, fl in [("바벨", barbell), ("불일치", mismatch)]:
    A, DA, CA = dur_conv(fl, y0)
    a = round(DA * A - 10 * L0, 6) + 0.0; b = CA * A - 100 * L0
    s_dn = price(fl, y0 - 1e-4) - price([(L_t, L_face)], y0 - 1e-4)
    s_up = price(fl, y0 + 1e-4) - price([(L_t, L_face)], y0 + 1e-4)
    print(f"{name:4s} a = {a:+8.2f} · b = {b:+8.1f} · −1bp ΔS = {s_dn:+.5f} · +1bp ΔS = {s_up:+.5f}")
"""),
M("""
## 4. 면역화의 한계 (강의 44장)
| 한계 | 무엇이 문제인가 | 아래에서 |
|---|---|---|
| 큰 충격 | 테일러 근사의 3차 이상 항 | 표의 바벨 S(+0.37)와 근사(+0.30)의 차이 |
| 시간 · 금리 변화 | D · C가 변한다 → 다시 맞춘다 | 금리가 움직인 뒤 바벨 D가 10에서 벗어남 |
| 비평행 이동(비틀림) | 듀레이션 매칭은 평행 이동만 막는다 | 5년 · 15년 금리가 반대로 움직이면 바벨도 손실 |
| 공급 | 현금흐름 매칭할 장기채가 모자람 | 30 · 50년 국고채 437조 vs 순부채 2,122조 |
"""),
C("""
# (1) 금리가 움직인 뒤 듀레이션 — 다시 맞춰야 한다
for dy in [-0.02, 0.0, 0.02]:
    _, DA, _ = dur_conv(barbell, y0 + dy)
    print(f"금리 {dy * 100:+.0f}%p 뒤 바벨 D = {DA:.2f}년 (부채 D는 10년 그대로) → 갭 {DA - 10:+.2f}년")

# (2) 비평행 이동 — 10년을 축으로 비틀기: Δy(t) = k × (t − 10)  (교육용 예시, 강의 숫자 아님)
def S_twist(fl, k):
    A = sum(f * np.exp(-(y0 + k * (t - 10)) * t) for t, f in fl)
    return A - price([(L_t, L_face)], y0)
for k in [-0.001, 0.001]:
    print(f"비틀기 k = {k * 1e4:+.0f}bp/년 (5년 {-5 * k * 1e4:+.0f}bp · 15년 {5 * k * 1e4:+.0f}bp): 바벨 잉여금 {S_twist(barbell, k):+.2f}")

# (3) 공급 — 현금흐름 매칭으로 덮을 수 있는 몫
print(f"30 · 50년 국고채 잔액 437조 ÷ 국민연금 순부채 2,122조 = {437 / 2122:.0%} — 전부 사도 순부채의 5분의 1")
"""),
C("""
ks = np.linspace(-0.002, 0.002, 81)
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.plot(ks * 1e4, [S_twist(barbell, k) for k in ks], color=TEAL, lw=2.2, label="바벨")
ax.plot(ks * 1e4, [S_twist(mismatch, k) for k in ks], color=RED, lw=1.8, ls="--", label="불일치 (5년)")
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_xlabel("비틀기 k (bp/년) — 양수: 단기 ↓ · 장기 ↑ (가팔라짐)"); ax.set_ylabel("잉여금 변화")
ax.set_title("비평행 이동에서는 바벨도 손실 — 면역화는 평행 이동에 대한 보장")
ax.legend()
plt.show()
"""),
M("""
## 5. 정리
- 면역화 = 1차 항 0(금액 DV01 일치, h = 100%) + 2차 항 ≥ 0(금액 볼록성 우위).
- 평행 · 작은 이동에 대한 보장이며 계속 다시 맞춰야 합니다. 실무는 듀레이션 매칭 + 일부 초과수익 → 05 노트북의 두 블록.
- (TDF 글라이드패스 · 국면민감형 TDF(42 · 43장)는 계산 예제가 없는 개념 장이라 이 노트북에서는 다루지 않습니다.)
"""),
]

ex = [
    "바벨을 3년물 + 17년물(현재가치 반반)로 바꾸면 D · C는? −2%p에서 잉여금은 5년 + 15년 바벨보다 큰가?",
    "부채가 A = 100 · L = 80(지금 기금)일 때 조건 2를 맞추려면 자산 D_A가 몇 년이어야 하나? (D_A·A = D_L·L)",
    "`S_twist` 대신 5년 금리만 +1%p 오르고 15년 금리는 그대로인 경우를 직접 계산해 보라. 바벨과 불일치 중 누가 이기나?",
]

if __name__ == "__main__":
    build(F, title, cells, ex)
