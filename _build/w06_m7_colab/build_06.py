# -*- coding: utf-8 -*-
from nbhelp import M, C, build, badge
import m7data as d

F = "06_실무헤지_2022영국_SVB.ipynb"
_, PAY = d.liability_lab()

title = M(f"""
# 06 · 실무 헤지 · 2022 영국 LDI · 2023 SVB — 레버리지 헤지는 현금 시험이다

{badge(F)}

**W06 M7 LDI 강의본 단원 ⑥ · ⑦ · ⑧(50~70장)** 의 숫자와 **실습데이터 덱**(`W06_M7_실습데이터_LDI부채연계투자.pdf` 단계 2~4)의 기대 결과를 재현합니다.

| 단계 | 강의 | 이 노트북에서 |
|---|---|---|
| 현물 · 스왑 · 증거금 | 51 · 53장 | Margin ≈ DV01_swap × Δy_bp · 안 C 사흘 +200bp 증거금 401조 vs 유동자산 123조 · TPR 버퍼 250bp |
| 2022 영국 | 56~61장 | £45B 감세(GDP 1.5%) · BOE £65B 발표 vs 실매입 £19.3B · 담보 현금 1~2% → 5~10% |
| 실습 B — 가상 부채 | 68장 · 실습 덱 12장 | PV 20,465억 · D 18.56 / 17.96년 · DV01 36.76억/bp · ±100bp −15.7% / +20.7% |
| 실습 C — 헤지 0 · 50 · 100% | 68장 · 실습 덱 13장 | 출발 FR 90% · ±100bp ΔFR −15.5/+16.8 · −6.9/+7.5 · +1.7/−1.9 |
| 실습 D — 레버리지 LDI 위기 | 69 · 70장 · 실습 덱 15 · 16장 | 버퍼 100bp → 3일차 고갈 · 강제매도 8.7% · 헤지 89% · FR −2.7%p / 250bp → 매도 0% · FR −0.9%p · 5배 · 7배 |
| 2023 SVB | 62 · 63 · 64장 | −6 × 117 × 0.025 ≈ −17.6(USD bn) ≈ 공시 평가손실 150억 달러+ |

가상 부채는 `W06_LDI와GBI/fml_w7_liability.csv`(**가상 데이터 — 강의용**, 실제 기관 자료 아님)의 연간 지급액을 노트북 안 상수로 옮겼습니다.
실습 덱 끝장이 가리키는 `lab_sim.py`는 저장소에 없어, 실습 덱 14장의 가정(현물 · 스왑 · 현금 버퍼 세 칸, 투매 할인 3%)으로 시뮬레이터를 다시 짰고 기대 결과가 그대로 나옵니다.
""")

cells = [
M("""
## 1. 변동증거금 — 스왑의 DV01 × 금리 변동 bp (강의 51 · 53장)
LBP(부채 벤치마크)는 성과의 기준, IRS 오버레이는 현금을 거의 쓰지 않고 듀레이션을 늘리는 지렛대입니다.
대가는 **변동증거금**: 금리가 오르면 고정금리 수취 스왑의 손실만큼 현금을 냅니다. **Margin ≈ DV01_swap × Δy_bp**.

국민연금 안 C(07 노트북): 30년 고정금리 수취 스왑 명목 1,223조, 30년 IRS 고정금리 4.45%(국고채 4.60% − 스프레드 0.15%p)의 수정 듀레이션 16.4년.
"""),
C("""
def par_mod_duration(T, y_pct):
    \"\"\"만기 T년, 연 이표 = 수익률인 액면가 채권(= 스왑 고정 다리)의 수정 듀레이션\"\"\"
    c = y_pct / 100; t = np.arange(1, T + 1)
    pv = c / (1 + c) ** t; pv[-1] += 1 / (1 + c) ** T
    return float(np.sum(t * pv) / (1 + c))

D_irs = par_mod_duration(30, 4.60 - 0.15)
notional_C = 1223.0
dv01_swap = notional_C * D_irs * 1e-4           # 조원/bp
margin_3d = dv01_swap * 200                      # 사흘 +200bp
buffer_250 = dv01_swap * 250
LIQUID = 4.6 + 118.6                             # 단기자금 + 국고채 보유(조) — 케이스 데이터 fml_w6m7_assets.csv
print(f"IRS 30년 수정 듀레이션 {D_irs:.1f}년 · 스왑 DV01 = 1,223 × {D_irs:.1f} × 0.0001 = {dv01_swap:.2f}조/bp")
print(f"사흘 +200bp 증거금 ≈ {margin_3d:.0f}조 · TPR 250bp 버퍼 {buffer_250:.0f}조 vs 담보 적격 유동자산 {LIQUID:.1f}조 (×{margin_3d / LIQUID:.1f})")
check("IRS 30년 수정 듀레이션 (년)", D_irs, 16.4, 0.05, ".2f")
check("안 C 사흘 +200bp 증거금 (조)", margin_3d, 401, 0.5, ".1f")
check("NPS 유동자산 (조)", LIQUID, 123, 0.5, ".1f")
"""),
M("""
## 2. 2022 영국 LDI — 숫자로 읽는 32일 (강의 56~61장)
| 날짜 | 사건 |
|---|---|
| 9/23 | 미니예산 — £45B 감세(GDP 1.5%), 파운드 −3.6% |
| 9/26 | 파운드 역대 최저(1.03) · LDI 증거금 경보 |
| 9/27 | 30년 Gilt 나흘 새 +1%p 이상 · Gilt 대량 매각 |
| 9/28 | BOE £65B 매입 발표 — 13일 한정 (실매입 £19.3B) |
| 10/25 | Truss 사임 — 재임 49일 |

손실 추정 £150B, 2021년 레버리지 LDI 약 £1.5조, 담보 현금 1~2% 보유 → 위기 시 5~10% 필요(61장 교훈 ③).
"""),
C("""
gdp = 45 / 0.015
print(f"£45B = GDP의 1.5% → 영국 GDP ≈ £{gdp / 1000:.1f}조")
print(f"BOE: 발표 £65B 중 실매입 £19.3B = {19.3 / 65:.0%} — '무제한 의지'의 신호가 핵심")
print(f"LDI £1.5조에 담보 현금 1~2% = £{1500 * 0.01:.0f}~{1500 * 0.02:.0f}B · 위기 때 5~10% = £{1500 * 0.05:.0f}~{1500 * 0.10:.0f}B 필요")
# 30년 Gilt 나흘 +1%p: 레버리지 3배 LDI(헤지 100%, 부채 D 20 가정)의 담보 수요 — 자산 대비
for lev in [3, 5, 7]:
    q = 1 - 1 / lev
    print(f"  레버리지 {lev}배: 스왑 몫 {q:.0%} × D 20 × 1%p = 부채 대비 {q * 20 * 0.01:.0%}의 현금")
check("BOE 실매입 비율 (%)", 100 * 19.3 / 65, 30, 0.5, ".1f")
"""),
C("""
fig, ax = plt.subplots(figsize=(10, 2.8))
ev = [(0, 0, 0.25, "9/23\\n미니예산\\n£45B 감세", INK), (3, 1.2, -0.25, "9/26\\n파운드 1.03\\n증거금 경보", INK),
      (4, 4, 0.25, "9/27\\n30년 Gilt\\n나흘 +1%p↑", RED), (5, 8.5, -0.25, "9/28 BOE £65B 발표\\n(실매입 £19.3B)", OLIVE),
      (32, 32, 0.25, "10/25\\nTruss 사임\\n재임 49일", INK)]
ax.axhline(0, color=GRAY, lw=2)
for x, lx, ly, lab, c in ev:
    ax.scatter(x, 0, s=120, color=LIME if c == OLIVE else c, edgecolor=INK, zorder=5)
    ax.annotate(lab, (x, 0), xytext=(lx, ly), ha="center", va="bottom" if ly > 0 else "top", fontsize=9, color=c,
                arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6) if lx != x else None)
ax.axvspan(5, 18, color=LIME, alpha=0.25); ax.text(15, 0.55, "BOE 매입 13일 한정", ha="center", color=OLIVE, fontsize=9)
ax.set_ylim(-1, 1); ax.set_yticks([]); ax.set_xlim(-2, 35); ax.set_xlabel("미니예산 후 경과일"); ax.grid(False)
ax.set_title("2022 영국 LDI 위기 — 미니예산에서 Truss 사임까지 32일")
plt.show()
"""),
M(f"""
## 3. 실습 B — 가상 DB 부채의 PV · 듀레이션 · DV01 (강의 68장 · 실습 덱 5 · 12장)
가상 DB 연금(가입자 10,000명), 2026~2076년 51개 연도 **연초 지급**(t = 0부터 할인), 물가연동 2%가 반영된 명목액(억원). 단일 할인율 3.3%.
"""),
C(f"""
# 가상 데이터 — 강의용 (실제 기관 · 개인의 자료가 아니다) · 출처: W06_LDI와GBI/fml_w7_liability.csv '연간지급액_억원'
PAY = np.array({d.fmt_list(PAY)})
t = np.arange(len(PAY)); YEARS = 2026 + t

def L_pv(y, start=0):
    \"\"\"연초 지급 — t = start부터 할인(start=1은 흔한 오류)\"\"\"
    return float(np.sum(PAY / (1 + y) ** (t + start)))

y0 = 0.033
L0 = L_pv(y0)
mac = float(np.sum(t * PAY / (1 + y0) ** t)) / L0
mod = mac / (1 + y0)
DV01_L = mod * L0 * 1e-4
up, dn = L_pv(y0 + 0.01) / L0 - 1, L_pv(y0 - 0.01) / L0 - 1
print("가상 데이터 — 강의용")
print(f"부채 PV {{L0:,.0f}}억 · Macaulay D {{mac:.2f}}년 · 수정 D {{mod:.2f}}년 · DV01 {{DV01_L:.2f}}억/bp")
print(f"금리 +100bp: PV {{up:+.1%}} · −100bp: PV {{dn:+.1%}} — 볼록성 때문에 하락 쪽 충격이 더 크다")
print(f"할인율 3.5%면 {{L_pv(0.035):,.0f}}억 · 정점 지급 {{YEARS[PAY.argmax()]}}년 {{PAY.max():,.0f}}억 · (오류) t = 1부터 할인하면 {{L_pv(y0, 1):,.0f}}억")
check("부채 PV (억)", L0, 20465, 0.5, ",.0f")
check("Macaulay 듀레이션 (년)", mac, 18.56, 0.005, ".3f")
check("수정 듀레이션 (년)", mod, 17.96, 0.005, ".3f")
check("DV01 (억/bp)", DV01_L, 36.76, 0.005, ".3f")
check("+100bp PV 변화 (%)", 100 * up, -15.7, 0.05, ".2f")
check("−100bp PV 변화 (%)", 100 * dn, 20.7, 0.05, ".2f")
check("할인율 3.5% PV (억)", L_pv(0.035), 19749, 0.5, ",.0f")
check("정점 지급 (억)", PAY.max(), 1132, 0.5, ",.0f")
check("t = 1부터 할인한 PV (억, 오류 예)", L_pv(y0, 1), 19811, 0.5, ",.0f")
"""),
C("""
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.bar(YEARS, PAY, color=TEAL, edgecolor="none", label="연간 지급액 (명목, 억원)")
ax.bar(YEARS, PAY / (1 + y0) ** t, color=LIME, edgecolor="none", alpha=0.9, label="현재가치 (3.3%)")
ax.annotate(f"정점 {YEARS[PAY.argmax()]} · {PAY.max():,.0f}억", (YEARS[PAY.argmax()], PAY.max()), textcoords="offset points", xytext=(10, 5), color=INK)
ax.axvline(2026 + mac, color=RED, ls="--", lw=1.2); ax.text(2026 + mac + 0.5, 1180, f"Macaulay D {mac:.1f}년", color=RED, fontsize=9)
ax.set_ylim(0, 1300); ax.set_xlabel("지급 연도"); ax.set_ylabel("억원")
ax.set_title("가상 DB 부채 — 은퇴자가 앞쪽, 현직 가입자의 은퇴 물결이 2056년 정점을 만든다 (가상 데이터)")
ax.legend(loc="upper left", ncol=2)
plt.show()
"""),
M("""
## 4. 실습 C — 헤지비율 0 · 50 · 100%의 적립비율 (강의 68장 · 실습 덱 13장)
출발 FR 90%(자산 = 0.9 × 부채 PV). 헤지 자산이 부채를 복제한다고 보면 금리 변화 시 자산은 h × (L₁ − L₀)만큼 움직입니다.
FR₁ = (A₀ + h·(L₁ − L₀)) ÷ L₁, 금리 ±100bp 평행 이동(부채는 다시 할인 — 볼록성 포함).
"""),
C("""
A0 = 0.9 * L0
LECT_C = {0.0: (-15.5, 16.8), 0.5: (-6.9, 7.5), 1.0: (1.7, -1.9)}
print(f"{'헤지':>6s} {'−100bp ΔFR':>12s} {'+100bp ΔFR':>12s}")
for h, (l_dn, l_up) in LECT_C.items():
    out = []
    for s in (-0.01, 0.01):
        L1 = L_pv(y0 + s)
        out.append(100 * ((A0 + h * (L1 - L0)) / L1 - 0.9))
    print(f"{h:6.0%} {out[0]:+11.1f}%p {out[1]:+11.1f}%p")
    check(f"헤지 {h:.0%} · −100bp ΔFR (%p)", out[0], l_dn, 0.05, "+.2f")
    check(f"헤지 {h:.0%} · +100bp ΔFR (%p)", out[1], l_up, 0.05, "+.2f")
"""),
C("""
shifts = np.linspace(-200, 200, 81)
fig, ax = plt.subplots(figsize=(8, 4.2))
for h, c in [(0.0, RED), (0.5, TEAL), (1.0, OLIVE)]:
    fr = [100 * (A0 + h * (L_pv(y0 + s / 1e4) - L0)) / L_pv(y0 + s / 1e4) for s in shifts]
    ax.plot(shifts, fr, color=c, lw=2.2, label=f"헤지 {h:.0%}")
ax.axhline(90, color=GRAY, ls=":", lw=1); ax.axvline(0, color=GRAY, lw=0.6)
ax.set_xlabel("금리 평행 이동 (bp)"); ax.set_ylabel("적립비율 (%)")
ax.set_title("헤지 100%면 금리가 어느 쪽으로 움직여도 FR은 2%p 안 — 헤지는 대칭이다")
ax.legend()
plt.show()
"""),
M("""
## 5. 실습 D — 레버리지 LDI 위기 시뮬레이터 (강의 69 · 70장 · 실습 덱 14~17장)
**가정(실습 덱 10 · 14장)** — 단일 기금 모형, 시장 가격 충격(Doom Loop)은 넣지 않는다.
- 출발 FR 90% · 헤지 100% = 현물 p + 스왑 q, 레버리지 3배면 p = 1/3 · q = 2/3 (부채 대비 비중)
- 현금 버퍼 = 스왑 DV01 × 버퍼(bp), 나머지 자산은 성장자산(금리 무관)
- 금리 +50bp × 3일 → 매일 변동증거금 납부(부채를 다시 할인한 정확한 손익 — 볼록성 때문에 하루 증거금은 50bp × DV01보다 조금 작다)
- 버퍼가 바닥나면 현물을 **3% 할인**으로 팔아 메우고, 레버리지 3배를 지키려 스왑을 현물의 2배로 줄인다
- 4일차 −100bp 되돌림(중앙은행 개입)
- 강제 매도 비율 = 판 현물(장부가) ÷ 출발 현물, 남은 헤지 = 현물 + 스왑(부채 대비)
"""),
C("""
def ldi_crisis(buffer_bp, path_bp=(50, 50, 50, -100), lev=3, FR0=0.9, haircut=0.03):
    p0 = 1 / lev; q0 = 1 - p0
    p, q = p0, q0
    cash = q0 * DV01_L * buffer_bp                     # 현금 버퍼(억)
    growth = FR0 * L0 - p0 * L0 - cash                 # 금리와 무관한 성장자산
    y, L_prev = y0, L0
    sold, short_day, cash_path = 0.0, None, [cash]
    for day, dy in enumerate(path_bp, 1):
        y += dy / 1e4; L_new = L_pv(y)
        cash += q * (L_new - L_prev)                   # 수취 스왑 손익 = 변동증거금(+면 받음)
        if cash < 0:                                   # 버퍼 고갈 → 현물 투매
            need = -cash; sell = need / (1 - haircut)
            p -= sell / L_new; q = (lev - 1) * p
            sold += sell; cash = 0.0
            short_day = short_day or day
        cash_path.append(cash); L_prev = L_new
    A_end = growth + p * L_prev + cash
    return {"부족일": short_day, "강제매도": sold / (p0 * L0), "남은헤지": p + q, "최종FR": A_end / L_prev,
            "ΔFR": A_end / L_prev - FR0, "버퍼경로": cash_path}

SCEN = [("버퍼 100bp · 균등 +50×3", dict(buffer_bp=100), (3, 8.7, 89, 87.3, -2.7)),
        ("버퍼 150bp · 균등", dict(buffer_bp=150), (None, 0, 100, 89.1, -0.9)),
        ("버퍼 250bp · 균등", dict(buffer_bp=250), (None, 0, 100, 89.1, -0.9)),
        ("버퍼 100bp · 전방 +100, +50", dict(buffer_bp=100, path_bp=(100, 50, -100)), (2, 8.7, 89, 87.3, -2.7)),
        ("버퍼 100bp · 레버리지 5배", dict(buffer_bp=100, lev=5), (3, 17.4, 78, 85.6, -4.4)),
        ("버퍼 100bp · 레버리지 7배", dict(buffer_bp=100, lev=7), (3, 26.1, 67, 83.9, -6.1))]
RES = {}
print("가상 데이터 — 강의용 · 단일 기금 · 가격 충격 미포함 모형")
print(f"{'시나리오':28s} {'버퍼 부족':>8s} {'강제 매도':>9s} {'남은 헤지':>9s} {'최종 FR':>8s} {'ΔFR':>7s}")
for name, kw, lec in SCEN:
    r = ldi_crisis(**kw); RES[name] = r
    sd = f"{r['부족일']}일차" if r["부족일"] else "없음"
    print(f"{name:28s} {sd:>8s} {r['강제매도']:9.1%} {r['남은헤지']:9.0%} {r['최종FR']:8.1%} {100 * r['ΔFR']:+6.1f}%p")
    check(f"{name} 부족일", r["부족일"] or 0, lec[0] or 0, 0, ".0f")
    check(f"{name} 강제 매도 (%)", 100 * r["강제매도"], lec[1], 0.05, ".2f")
    check(f"{name} 남은 헤지 (%)", 100 * r["남은헤지"], lec[2], 0.5, ".1f")
    check(f"{name} 최종 FR (%)", 100 * r["최종FR"], lec[3], 0.05, ".2f")
    check(f"{name} ΔFR (%p)", 100 * r["ΔFR"], lec[4], 0.05, ".2f")
left250 = RES["버퍼 250bp · 균등"]["버퍼경로"][3]
print(f"250bp 버퍼는 3일차에 {left250:,.0f}억 남음 · 하루 증거금(1일차) {-(RES['버퍼 250bp · 균등']['버퍼경로'][1] - RES['버퍼 250bp · 균등']['버퍼경로'][0]):,.0f}억 < 50bp × 스왑 DV01 {50 * DV01_L * 2 / 3:,.0f}억")
check("250bp 버퍼 3일차 잔액 (억)", left250, 3102, 0.5, ",.0f")
"""),
C("""
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.3))
for name, c in [("버퍼 100bp · 균등 +50×3", RED), ("버퍼 150bp · 균등", GRAY), ("버퍼 250bp · 균등", TEAL)]:
    ax1.plot(range(5), RES[name]["버퍼경로"], marker="o", color=c, lw=2, label=name.split(" · ")[0])
ax1.axhline(0, color=INK, lw=0.8)
ax1.annotate("3일차 고갈 → 현물 8.7% 투매", (3, 0), textcoords="offset points", xytext=(15, 40), color=RED, fontsize=9, arrowprops=dict(arrowstyle="->", color=RED))
ax1.set_xticks(range(5), ["출발", "1일 +50", "2일 +50", "3일 +50", "4일 −100"])
ax1.set_ylabel("남은 현금 버퍼 (억)"); ax1.set_title("날마다 남은 현금 버퍼 — 100bp는 사흘째 바닥"); ax1.legend()
names = ["버퍼 100bp · 균등 +50×3", "버퍼 250bp · 균등", "버퍼 100bp · 레버리지 5배", "버퍼 100bp · 레버리지 7배"]
labs = ["100bp · 3배", "250bp · 3배", "100bp · 5배", "100bp · 7배"]
vals = [100 * RES[n]["ΔFR"] for n in names]
bars = ax2.bar(labs, vals, color=[RED, TEAL, RED, RED], edgecolor=INK)
for b, n, v in zip(bars, names, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v - 0.25, f"{v:+.1f}%p\\n헤지 {RES[n]['남은헤지']:.0%}", ha="center", va="top", fontsize=9)
ax2.set_ylim(-8, 0.5); ax2.set_ylabel("4일차 뒤 ΔFR (%p)")
ax2.set_title("레버리지가 클수록 더 많이 팔고 더 많은 헤지를 잃는다")
fig.tight_layout(); plt.show()
"""),
M("""
**재현되지 않는 것 — "일부 기금 FR −30%p"(강의 58 · 69장, 실습 덱 17장).** 이 모형은 한 기금의 산수라 7배여도 −6.1%p입니다.
붕괴의 크기는 1,000개 기금의 동시 매도가 Gilt 가격을 떨어뜨려 금리를 다시 올리는 **시장 전체의 가격 충격(Doom Loop)** 에서 나옵니다.
발언할 때는 "단일 기금 · 가격 충격 미포함 모형 기준"이라고 가정을 함께 말합니다.

## 6. 2023 SVB — 반대 방향의 갭, 같은 현금 시험 (강의 62 · 63 · 64장)
2022년 말 SVB: 총자산 2,090억 · 예금 1,755억(비보호 약 86%) · 채권 1,170억 달러. **듀레이션 6년 · 금리 +2.5%p는 손계산용 가정치.**
"""),
C("""
D_svb, V_svb, dy_svb = 6, 117, 0.025
loss = -D_svb * V_svb * dy_svb
print(f"ΔV ≈ −D·V·Δy = −6 × 117 × 0.025 = {loss:.1f} (USD bn, 약 {-loss * 10:.0f}억 달러) ≈ 공시 평가손실 150억 달러+ (자기자본과 비슷한 규모)")
print(f"비보호 예금 ≈ 1,755억 × 86% = {1755 * 0.86:,.0f}억 달러 · 3/9 하루 인출 420억 = 예금의 {420 / 1755:.0%}")
check("SVB 평가손실 손계산 (USD bn)", loss, -17.6, 0.05, ".2f")
check("손계산 ≥ 공시 150억 달러", float(-loss >= 15), 1, 0, ".0f")
"""),
C("""
dys = np.linspace(0, 0.04, 41)
fig, ax = plt.subplots(figsize=(7.5, 4))
for D_, c in [(4, GRAY), (6, RED), (8, INK)]:
    ax.plot(dys * 100, D_ * V_svb * dys, color=c, lw=2.2 if D_ == 6 else 1.3, label=f"듀레이션 {D_}년")
ax.axhline(15, color=TEAL, ls="--", lw=1.2); ax.text(0.1, 15.6, "공시 평가손실 150억 달러+", color=TEAL, fontsize=9)
ax.scatter(2.5, -loss, s=90, color=LIME, edgecolor=RED, zorder=5)
ax.annotate(f"손계산 {-loss:.1f}", (2.5, -loss), textcoords="offset points", xytext=(8, -14), color=RED)
ax.set_xlabel("금리 상승 (%p)"); ax.set_ylabel("채권 평가손실 (USD bn, 1차 근사)")
ax.set_title("SVB — 단원 ③의 −D·V·Δy 한 줄이 공시 손실과 거의 같다")
ax.legend()
plt.show()
"""),
M("""
## 7. 정리
- 2022 영국 연기금: 짧은 자산을 **스왑으로 늘려** 헤지 → 금리가 빠르게 오르자 **증거금**에서 무너짐.
- 2023 SVB: 짧은 예금 앞에 긴 채권을 들고 **헤지하지 않음** → 금리 상승의 평가손실이 **인출**에서 터짐.
- 갭의 방향은 달라도 시험은 현금. 버퍼 150bp의 차이가 강제매도 여부를 가른다 — 영국 규제 250bp의 근거. 국민연금 안 C는 사흘 +200bp 증거금 401조 vs 유동자산 123조 → 07 노트북.
"""),
]

ex = [
    "`ldi_crisis(100, lev=3, haircut=0.10)` — 투매 할인을 3% → 10%로 키우면 강제 매도와 ΔFR은? (가격 충격을 넣은 아주 간단한 흉내)",
    "금리 경로를 +80bp × 3일 → −100bp로 바꾸면 버퍼 250bp도 고갈되는가? 고갈되지 않는 최소 버퍼(bp)를 찾아보라.",
    "실습 C에서 출발 FR을 90% → 110%로 바꾸면 헤지 0%일 때 ±100bp의 ΔFR은? 왜 적립이 좋은 기금도 금리 하락에 FR이 떨어지는가?",
]

if __name__ == "__main__":
    build(F, title, cells, ex)
