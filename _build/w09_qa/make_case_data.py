# -*- coding: utf-8 -*-
"""W09 케이스 데이터 팩 — 강의본 66·67장(케이스 준비)과 27·28·41장 예시의 숫자를 CSV로 만든다.
케이스 ① 국부펀드는 가상 기관이다. 2022 자산군 수익률(주식 −18 · 채권 −13)과 국제 비교는 공개 수치,
비중 · 운용 성과는 덱의 숫자(BM −9.2 · 실제 −8.6 · Brinson −0.2/+0.5/+0.3)를 재현하도록 지은 강의용 구성이다.
실행: .venv/bin/python _build/w09_qa/make_case_data.py
"""
import csv, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(R, "W09_위험관리와성과평가", "W09_케이스데이터")
C1, C2 = os.path.join(OUT, "케이스1_성과평가"), os.path.join(OUT, "케이스2_측정")
for d in (C1, C2): os.makedirs(d, exist_ok=True)
def w(path, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f: csv.writer(f).writerows(rows)

# ── 케이스 ① ─────────────────────────────────────────────────────────
A  = ["주식", "채권", "대체", "현금"]
wb = [0.40, 0.30, 0.25, 0.05]                 # 정책(벤치마크) 비중
rb = [-18.0, -13.0, 7.30, 1.50]               # 자산군 벤치마크 수익률 % (대체 BM은 합계 −9.2가 되도록)
wp = [0.45, 0.25, 0.26, 0.04]                 # 실제 비중
rp = [-15.00, -15.87, 7.93, 1.50]             # 실제 자산군 수익률 %
Rb = sum(a * b for a, b in zip(wb, rb)); Rp = sum(a * b for a, b in zip(wp, rp))
rows = [["자산군", "정책비중", "실제비중", "BM수익률(%)", "실제수익률(%)", "배분효과(%p)", "선택효과(%p)", "교차효과(%p)"]]
ta = ts = ti = 0
for i, a in enumerate(A):
    al = (wp[i] - wb[i]) * (rb[i] - Rb); se = wb[i] * (rp[i] - rb[i]); it = (wp[i] - wb[i]) * (rp[i] - rb[i])
    ta += al; ts += se; ti += it
    rows.append([a, wb[i], wp[i], rb[i], rp[i], round(al, 3), round(se, 3), round(it, 3)])
rows.append(["합계", 1.0, 1.0, round(Rb, 2), round(Rp, 2), round(ta, 3), round(ts, 3), round(ti, 3)])
w(f"{C1}/brinson_2022.csv", rows)
print(f"BM {Rb:.2f}  실제 {Rp:.2f}  초과 {Rp-Rb:+.2f} = 배분 {ta:+.2f} + 선택 {ts:+.2f} + 교차 {ti:+.2f}")
assert round(Rb, 1) == -9.2 and round(Rp, 1) == -8.6 and round(ta, 1) == -0.2 and round(ts, 1) == 0.5 and round(ti, 1) == 0.3

w(f"{C1}/factor_lens_2022.csv", [
    ["팩터", "기금 노출", "단위", "설명"],
    ["주식 베타", 0.65, "배", "세계 주식지수 1% 하락 → 기금 약 0.65% 하락"],
    ["금리 듀레이션", 5.2, "년", "채권 부분의 수정 듀레이션 — 금리 1%p 상승 시 채권 가치 약 5.2% 하락"],
    ["달러 비중", 0.70, "비율", "자산의 70%가 달러 표시"],
    ["출처", "", "", "케이스 ① 덱 9쪽 — 가상 기관의 강의용 값"]])

w(f"{C1}/peers_2022.csv", [
    ["기관", "2022 수익률(%)", "기준", "출처"],
    ["노르웨이 GPFG", -14.1, "역년", "NBIM 2022 연차보고서"],
    ["일본 GPIF", -4.8, "역년(1~12월)", "국민연금 2022 기금운용 성과 보도자료의 해외 비교(2023.3)"],
    ["캐나다 CPP", -5.0, "역년(1~12월)", "같은 비교자료"],
    ["네덜란드 ABP", -17.6, "역년", "같은 비교자료"],
    ["한국 국민연금", -8.22, "역년, 금액가중 잠정", "국민연금 기금운용본부(2023.3)"],
    ["한국 KIC", -14.36, "역년, USD", "KIC 2022 연차보고서"],
    ["케이스 국부펀드(가상)", -8.6, "역년", "케이스 ① 덱 — 실제 기관 아님"],
    ["참고: 세계 주식 / 채권 / 60:40", "−18 / −13 / 약 −16", "역년", "MSCI ACWI · Bloomberg Global Agg 2022 근사"]])

# ── 케이스 ② · 본문 27·28장 예시 ───────────────────────────────────
w(f"{C2}/twr_mwr_example.csv", [
    ["시점(년)", "그해 펀드 수익률", "투자자 현금흐름(투자자 기준)", "기말 잔고"],
    [0, "", -100, 100], [1, 0.50, -150, 300], [2, -0.20, 240, 0]])
twr = (1.5 * 0.8) ** 0.5 - 1
x = (-150 + (150 ** 2 + 4 * 100 * 240) ** 0.5) / (2 * 100); mwr = x - 1
cf = [(0, -100, 100), (3, 60, 130), (5, 120, 150)]
def npv(r): return sum(c / (1 + r) ** t for t, c, _ in cf)
lo, hi = 0.0, 1.0
for _ in range(100):
    mid = (lo + hi) / 2; (lo, hi) = (mid, hi) if npv(mid) > 0 else (lo, mid)
irr = (lo + hi) / 2
ks = sum(c / i for t, c, i in cf if c > 0) / sum(-c / i for t, c, i in cf if c < 0)
w(f"{C2}/ks_pme_example.csv", [
    ["시점(년)", "납입 C", "분배 D", "지수 I", "C/I", "D/I"],
    [0, 100, 0, 100, 1.0, 0], [3, 0, 60, 130, 0, round(60 / 130, 4)], [5, 0, 120, 150, 0, round(120 / 150, 4)],
    ["합계", 100, 180, "", 1.0, round(ks, 4)],
    ["결과", f"TVPI {180/100:.2f}", f"IRR {irr*100:.1f}%", f"KS-PME {ks:.2f}", "", ""]])
print(f"TWR {twr*100:.2f}%  MWR {mwr*100:.2f}%  IRR {irr*100:.2f}%  KS-PME {ks:.4f}")

open(f"{OUT}/README.md", "w", encoding="utf-8").write(f"""# W09 케이스 데이터

강의본(W09_위험관리와성과평가_강의본) 케이스 준비 장(66·67장)과 본문 예시 장의 숫자를 계산할 수 있게 모은 CSV다.
`_build/w09_qa/make_case_data.py`로 다시 만든다.

## 케이스1_성과평가 — 케이스 ① 국부펀드 2022

케이스의 국부펀드는 **가상 기관**이다(케이스 ① 덱 3쪽).
- 2022 자산군 수익률(주식 −18% · 채권 −13%)과 국제 비교 수치는 공개 자료다.
- 정책·실제 비중과 자산군별 운용 성과는 덱의 숫자를 정확히 재현하도록 지은 **강의용 구성**이다.

| 파일 | 내용 |
|---|---|
| `brinson_2022.csv` | 자산군 4개의 정책·실제 비중과 수익률, Brinson–Fachler 분해. BM {Rb:.2f}% · 실제 {Rp:.2f}% · 배분 {ta:+.2f} · 선택 {ts:+.2f} · 교차 {ti:+.2f}%p |
| `factor_lens_2022.csv` | 팩터 렌즈 노출(주식 β 0.65 · 듀레이션 5.2년 · 달러 70%) |
| `peers_2022.csv` | 국제 비교(GPFG · GPIF · CPP · ABP · 국민연금 · KIC)와 출처 |

배분효과는 (실제비중 − 정책비중) × (자산군 BM − 전체 BM)으로 계산했다(Brinson–Fachler). BHB식 (실제비중 − 정책비중) × 자산군 BM으로 계산해도 합계는 같다.

## 케이스2_측정 — 케이스 ② · 본문 27·28장

| 파일 | 내용 |
|---|---|
| `twr_mwr_example.csv` | 같은 펀드의 TWR {twr*100:.1f}%/년과 MWR(IRR) {mwr*100:.1f}%/년 |
| `ks_pme_example.csv` | 사모펀드 현금흐름 1개의 TVPI 1.80 · IRR {irr*100:.1f}% · KS-PME {ks:.2f} |

케이스 ② 덱의 Yale KS-PME 0.915와 VC KS-PME 1.81은 덱의 그림에 계산 과정이 있다. 원 현금흐름은 공개되지 않았다.
""")
