# -*- coding: utf-8 -*-
from nbhelp import M, C, build, badge
import m7data as d

F = "02_할인율.ipynb"
yrs, _, _, net = d.cashflow()
END = int(float(d.params()["liab_end_year"]))
NET = [n for y, n in zip(yrs, net) if y <= END]
MATS, YLDS = d.curve()
PR = d.params()

title = M(f"""
# 02 · 할인율 — 같은 약속, 다른 숫자

{badge(F)}

**W06 M7 LDI 강의본 단원 ②(18~28장)** 의 숫자를 재현합니다. 할인율(부채를 재는 자)을 바꾸면 같은 약속이 다른 부채가 됩니다.

| 단계 | 강의 | 이 노트북에서 |
|---|---|---|
| 먼 약속일수록 흔들린다 | 19장 | 20년 뒤 100: 5% → 37.7 · 3% → 55.4 · 2%p 낮추면 +47% |
| 할인율의 두 눈금 — 국민연금 | 20 · 21 · 23장 | 자체 5.5% → 순부채 1,542조 · FR 95% / 국채 곡선 → 2,122조 · FR 69% · 1.4배 |
| 할인율 선택표 | 14 · 20장 | 예상수익률 7~8% · 국채 3~5% · AA 회사채(+100~150bp) — "두 배까지" |
| 공무원연금 · CalPERS | 21~23장 | 기금 16조 ÷ 부채 900조+ = 2% 미만 · CalPERS 7.5% → 6.8% |
| 영국 DB의 세 자 | 24 · 25장 | 잉여금 £273.7B · FR 130.8% → A ≈ £1,162B · L ≈ £889B / 바이아웃 114% → L ≈ £1,000B · 약 12% |

국민연금 숫자는 **케이스 데이터(교육용 추계)** 의 순유출(급여 − 보험료)을 노트북 안 상수로 옮겨 계산합니다(출처: `W06_M7_케이스데이터/fml_w6m7_cashflow.csv` · `fml_w6m7_curve.csv`, 계산 방식은 `w6m7_compute.py`와 같음).
""")

cells = [
M("""
## 1. 먼 약속일수록 흔들린다 (강의 19장)
20년 뒤 100을 한 번 지급하는 약속. 할인은 분모의 (1 + r)ᵗ로 하니 **r의 차이가 t번 곱해집니다.**
"""),
C("""
def pv(cf, r, t):
    return cf / (1 + r) ** t

v5, v3 = pv(100, 0.05, 20), pv(100, 0.03, 20)
print(f"5%: 100 ÷ 1.05²⁰ = {v5:.1f} · 3%: 100 ÷ 1.03²⁰ = {v3:.1f} → 할인율 2%p 낮추면 부채 {v3 / v5 - 1:+.0%}")
check("20년 뒤 100 · 5%", v5, 37.7, 0.05, ".1f")
check("20년 뒤 100 · 3%", v3, 55.4, 0.05, ".1f")
check("2%p 낮출 때 부채 증가 (%)", 100 * (v3 / v5 - 1), 47, 0.5, ".1f")
"""),
C("""
rs = np.linspace(0.01, 0.08, 200)
fig, ax = plt.subplots(figsize=(7.5, 4))
for t, c in [(5, GRAY), (10, OLIVE), (20, TEAL), (35, INK)]:
    ax.plot(rs * 100, pv(100, rs, t), color=c, lw=2.2 if t == 20 else 1.4, label=f"{t}년 뒤 100")
for r_, v in [(3, v3), (5, v5)]:
    ax.scatter(r_, v, s=70, color=RED if r_ == 3 else TEAL, zorder=5)
    ax.annotate(f"{r_}% → {v:.1f}", (r_, v), textcoords="offset points", xytext=(8, 6), color=RED if r_ == 3 else TEAL)
ax.set_xlabel("할인율 (%)"); ax.set_ylabel("오늘 가치 (현재가치)")
ax.set_title("할인율이 2%p 낮아지면 20년 약속은 +47% — 먼 약속일수록 기울기가 가파르다")
ax.legend()
plt.show()
"""),
M(f"""
## 2. 할인율의 두 눈금 — 국민연금 순부채 (강의 20 · 21 · 23장)
2026~{END}년 순유출(급여 − 보험료)의 현재가치를 두 자로 잽니다(2025년 말 기준, 연말 현금흐름).
- **자체 할인율 5.5%** (연금개혁 전제 기금수익률)
- **국채 곡선** — 국고채 3 · 10 · 30 · 50년 공시 수익률(2026-09-18) + 교육용 보간, 만기 t년 현금흐름은 t년 금리로 할인

적립금 F = {float(PR['fund_2025_trn']):,.0f}조(2025년 말)로 나누면 적립비율 두 개가 나옵니다. **우리 계산** 값이며, 국민연금이 공시하는 지표는 적립배율(적립금 ÷ 그해 지출)입니다.
"""),
C(f"""
# 케이스 데이터 상수 (교육용 추계 · 조원) — 출처: W06_M7_케이스데이터/fml_w6m7_cashflow.csv (net_outflow_trn_krw, 2026~{END})
YEARS = np.arange(2026, {END + 1})
NET = np.array({d.fmt_list(NET)})          # 순유출 = 급여 − 보험료 (음수 = 보험료가 더 많은 해)
MATS = np.array({MATS})                    # 국고채 곡선 만기(년) — fml_w6m7_curve.csv
YLDS = np.array({YLDS})   # 수익률(%) — 3 · 10 · 30 · 50년 공시, 나머지 교육용 보간
F0 = {float(PR['fund_2025_trn'])}          # 2025년 말 적립금(조)
HURDLE = {float(PR['hurdle_pct'])}         # 자체 할인율 = 허들(%)

def z(t, shift_bp=0.0):
    \"\"\"만기 t년 금리(%) — 곡선 점을 선형 보간, 50년 뒤는 평탄\"\"\"
    return np.interp(t, MATS, YLDS) + shift_bp / 100

def pv_flows(flows, years, rate=None, shift_bp=0.0):
    \"\"\"연말 현금흐름의 2025년 말 현재가치 — rate(%)가 있으면 평탄 할인, 없으면 곡선\"\"\"
    t = np.asarray(years) - 2025
    r = np.full(t.shape, rate, dtype=float) if rate is not None else z(t, shift_bp)
    return float(np.sum(flows / (1 + r / 100) ** t))

L_h = pv_flows(NET, YEARS, rate=HURDLE)
L_g = pv_flows(NET, YEARS)
print(f"곡선: 3년 {{z(3):.2f}} · 10년 {{z(10):.2f}} · 30년 {{z(30):.2f}}%")
print(f"순부채 — 자체 {{HURDLE}}%: {{L_h:,.0f}}조 · 국채 곡선: {{L_g:,.0f}}조 (×{{L_g / L_h:.2f}})")
print(f"적립비율 — 자체 FR_h = {{F0 / L_h:.0%}} · 국채 FR_g = {{F0 / L_g:.0%}}")
check("순부채 자체 5.5% (조)", L_h, 1542, 0.5, ",.0f")
check("순부채 국채 곡선 (조)", L_g, 2122, 0.5, ",.0f")
check("FR 자체 눈금 (%)", 100 * F0 / L_h, 95, 0.5, ".1f")
check("FR 국채 눈금 (%)", 100 * F0 / L_g, 69, 0.5, ".1f")
check("두 눈금의 비 (배)", L_g / L_h, 1.4, 0.05, ".2f")
"""),
M("""
**그래프 — 평탄 할인율을 바꿔 가며 잰 순부채와 적립비율.** 할인율 하나가 적립비율을 50%대에서 100% 위까지 옮깁니다.
국채 곡선(4% 중반)은 평탄 할인율로 치면 어디쯤인지도 찾아 봅니다(곡선 부채와 같은 값을 주는 평탄 할인율).
"""),
C("""
from scipy.optimize import brentq
flat = np.linspace(3.0, 8.0, 101)
Ls = np.array([pv_flows(NET, YEARS, rate=x) for x in flat])
r_equiv = brentq(lambda x: pv_flows(NET, YEARS, rate=x) - L_g, 2, 8)
print(f"국채 곡선 부채 {L_g:,.0f}조 = 평탄 할인율 {r_equiv:.2f}%와 같다")

fig, ax1 = plt.subplots(figsize=(8.5, 4.4))
ax1.plot(flat, Ls, color=INK, lw=2.2, label="순부채 (왼쪽 축)")
ax1.set_xlabel("평탄 할인율 (%)"); ax1.set_ylabel("순부채 현재가치 (조)")
ax2 = ax1.twinx()
ax2.plot(flat, 100 * F0 / Ls, color=TEAL, lw=2, ls="--", label="적립비율 FR (오른쪽 축)")
ax2.axhline(100, color=GRAY, lw=0.8, ls=":")
ax2.set_ylabel("적립비율 (%)"); ax2.spines["right"].set_visible(True); ax2.grid(False)
for x, L_, lab, c in [(HURDLE, L_h, f"자체 5.5%\\n{L_h:,.0f}조 · FR {F0 / L_h:.0%}", TEAL), (r_equiv, L_g, f"국채 곡선(≈{r_equiv:.2f}%)\\n{L_g:,.0f}조 · FR {F0 / L_g:.0%}", RED)]:
    ax1.scatter(x, L_, s=80, color=LIME, edgecolor=c, lw=2, zorder=6)
    ax1.annotate(lab, (x, L_), textcoords="offset points", xytext=(10, 10), color=c, fontsize=9)
ax1.set_title("같은 약속, 다른 숫자 — 할인율 하나가 국민연금 순부채를 1.4배 바꾼다 (교육용 추계)")
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper right")
plt.show()
"""),
M("""
## 3. 할인율 선택표 — "두 배까지 차이" (강의 14 · 20장)
| 할인율 | 사용 주체 | 특징 |
|---|---|---|
| 예상 자산수익률 7~8% | 미국 공적연금 전통 | 부채가 작아 보인다 — "많이 벌 테니 부채가 작다"는 순환 논리 |
| 국채 수익률 3~5% | 민간 연금(ERISA · IAS 19) | 시장 가격 반영 — 부채가 크고 금리에 따라 크게 변한다 |
| AA 회사채 | 미국 GAAP | 국채 + 스프레드 100~150bp |

같은 국민연금 순유출에 이 눈금들을 대 봅니다(평탄 할인율로 단순화한 비교).
"""),
C("""
scales = [("국채 3%", 3.0), ("국채 곡선", None), ("AA 회사채 = 곡선 + 125bp", "aa"), ("자체 5.5%", 5.5), ("예상수익률 7.5%", 7.5)]
vals = []
for name, x in scales:
    if x is None: v = L_g
    elif x == "aa": v = pv_flows(NET, YEARS, shift_bp=125)
    else: v = pv_flows(NET, YEARS, rate=x)
    vals.append(v)
    print(f"{name:22s} 순부채 {v:7,.0f}조 · FR {F0 / v:5.0%}")
print(f"가장 낮은 자(3%) ÷ 가장 높은 자(7.5%) = {vals[0] / vals[-1]:.1f}배")
print("강의 14장은 일반 연금 기준 '두 배까지'. 국민연금 순유출은 앞쪽이 보험료 유입(음수)이고 지급이 먼 뒤에 몰려(듀레이션 35년)")
print("같은 눈금 차이에도 배수가 훨씬 크다 — 부채가 길수록 '자'의 선택이 더 큰 숫자를 만든다")
check("국채 3% vs 예상수익률 7.5% — 두 배 이상", float(vals[0] / vals[-1] >= 2), 1, 0, ".0f")
"""),
M("""
## 4. 공무원연금 · CalPERS (강의 21 · 22 · 23장)
- 공무원연금: 기금 16조 · 연금충당부채 900조+ → 적립비율 **2% 미만**(우리 계산). 2015 개혁: 기여율 7% → 9%, 지급률 1.9% → 1.7%.
- CalPERS: 할인율 7.5% → 6.8%(2016년 단계적 하향), 적립비율 약 75%(FY2024, 공시).

CalPERS의 0.7%p 하향이 어느 정도의 부채 증가인지, 같은 국민연금 순유출로 감을 잡아 봅니다(교육용 비교 — 강의 숫자 아님).
"""),
C("""
gepf = 16 / 900
print(f"공무원연금 적립비율 ≈ 16 ÷ 900 = {gepf:.1%} (부채가 900조보다 크면 더 낮다)")
check("공무원연금 적립비율 2% 미만", float(gepf < 0.02), 1, 0, ".0f")
L75, L68 = pv_flows(NET, YEARS, rate=7.5), pv_flows(NET, YEARS, rate=6.8)
print(f"(참고) 같은 순유출을 7.5% → 6.8%로 재면 부채 {L75:,.0f} → {L68:,.0f}조 ({L68 / L75 - 1:+.0%}) — 할인율 0.7%p가 부채 수십 %")
"""),
M("""
## 5. 영국 DB의 세 자 (강의 24 · 25장)
2026년 2월 PPF 7800: 영국 DB 연금 전체 잉여금 £273.7B. 자산은 같고 부채를 재는 자만 다릅니다.
FR = A/L, S = A − L에서 **A = S · FR ÷ (FR − 1), L = A − S** 로 역산합니다.
- PPF(s179) 기준 FR 130.8% · 저의존 123% · 바이아웃 114%(바이아웃 잉여금 약 £140B)
"""),
C("""
def back_out(S, FR):
    A = S * FR / (FR - 1)
    return A, A - S

A_ppf, L_ppf = back_out(273.7, 1.308)
A_bo, L_bo = back_out(140, 1.14)
print(f"PPF s179: 273.7 × 1.308 ÷ 0.308 → A ≈ £{A_ppf:,.0f}B · L ≈ £{L_ppf:,.0f}B")
print(f"바이아웃: 140 × 1.14 ÷ 0.14 → A ≈ £{A_bo:,.0f}B · L ≈ £{L_bo:,.0f}B")
print(f"자산 차이 {A_bo / A_ppf - 1:+.1%} (비슷) · 부채 차이 {L_bo / L_ppf - 1:+.1%}")
check("PPF 자산 (£B)", A_ppf, 1162, 0.5, ",.0f")
check("PPF 부채 (£B)", L_ppf, 889, 0.5, ",.0f")
check("바이아웃 자산 (£B)", A_bo, 1140, 0.5, ",.0f")
check("바이아웃 부채 (£B)", L_bo, 1000, 0.5, ",.0f")
check("부채 차이 약 12% (%)", 100 * (L_bo / L_ppf - 1), 12, 1.0, ".1f")
"""),
C("""
fig, ax = plt.subplots(figsize=(7.5, 4.2))
names = ["PPF (s179)", "저의존", "바이아웃"]; frs = [130.8, 123, 114]
bars = ax.bar(names, frs, 0.6, color=["#DDE3E3", TEAL, INK], edgecolor=INK)
for b, v in zip(bars, frs):
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v}%", ha="center", fontweight="bold")
ax.text(0, 93, f"부채 ≈ £{L_ppf:,.0f}B", ha="center", fontsize=9)
ax.text(2, 93, f"부채 ≈ £{L_bo:,.0f}B", ha="center", fontsize=9, color="white")
ax.axhline(100, color=RED, ls="--", lw=1); ax.text(2.35, 101, "FR 100%", color=RED, fontsize=9, ha="right")
ax.set_ylim(90, 140); ax.set_ylabel("적립비율 (%)")
ax.set_title("같은 영국 DB 연금(2026.2), 자에 따라 130.8% ~ 114%")
plt.show()
"""),
M("""
## 6. 정리
- 부채는 할인율로 **추정**되는 숫자입니다. 국민연금 순부채는 자체 5.5%로 1,542조, 국채 곡선으로 2,122조 — 오후 IC 조건 ① "어느 눈금의 적립비율인가"의 출발점입니다.
- 같은 할인율 문제가 금리 **변화**에 대해 생기면 그것이 금리 위험입니다 → 03 노트북(듀레이션 · DV01).
"""),
]

ex = [
    "국채 곡선 전체를 −100bp 내리면(`pv_flows(NET, YEARS, shift_bp=-100)`) 순부채와 FR_g는? (07 노트북의 '69% → 49%'와 비교)",
    "자체 할인율이 4.5%라면(소진 2064 시나리오의 수익률) 순부채와 FR은 얼마인가?",
    "영국 DB의 저의존 기준(FR 123%) 부채를 자산 £1,150B로 가정해 역산하라. 바이아웃 부채와 몇 % 차이인가?",
]

if __name__ == "__main__":
    build(F, title, cells, ex)
