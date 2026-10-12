"""M7 LDI 에피소드별 화면 숫자 계산 (강의본과 같은 가정). 사용: python3 tools/numbers_m7.py"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parents[1] / "src/data"
def save(ep, d):
    (root / f"{ep}.numbers.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(ep, "ok")

# E01 부채와 적립비율 (pp.10–17)
A, L = 100.0, 80.0
hook = dict(A1=A * 1.075, L1=L * 1.15)
hook["FR1"] = hook["A1"] / hook["L1"]
pv = [30 / 1.04**t for t in (1, 2, 3)]
yr = dict(A1=A * 1.07, L1=L * 1.10)
yr.update(FR1=yr["A1"] / yr["L1"], approx=A / L * (0.07 - 0.10), RS=0.07 - L / A * 0.10)
save("M7E01", dict(A=A, L=L, FR0=A / L, S0=A - L, hook=hook, pv=pv, Lsum=sum(pv), yr=yr))

# E02 할인율 (pp.18–28)
p5, p3 = 100 / 1.05**20, 100 / 1.03**20
uk_A, uk_L_ppf = 273.7 * 1.308 / 0.308, 273.7 / 0.308
uk_L_bo = 140 / 0.14
save("M7E02", dict(p5=p5, p3=p3, chg=p3 / p5 - 1,
     nps=dict(own=dict(r=5.5, L=1542, FR=0.95), gov=dict(L=2122, FR=0.69)),
     uk=dict(S=273.7, FR_ppf=1.308, FR_bo=1.14, A=uk_A, L_ppf=uk_L_ppf, L_bo=uk_L_bo, diff=uk_L_bo / uk_L_ppf - 1),
     funds=[dict(k="공무원연금", fr=0.02, note="2% 미만 (우리 계산)"), dict(k="CalPERS", fr=0.75, note="약 75% (FY2024 공시)"),
            dict(k="국민연금 · 자체 5.5%", fr=0.95, note="95% (우리 계산)"), dict(k="국민연금 · 국채 눈금", fr=0.69, note="69% (우리 계산)")]))

# E04 Redington (pp.37–44) — 부채: 10년 뒤 100, y = 5% 연속복리
import math
y0 = 0.05; Lpv = 100 * math.exp(-10 * y0)
half = Lpv / 2
f5, f15 = half * math.exp(5 * y0), half * math.exp(15 * y0)   # 바벨 액면
fm = Lpv * math.exp(5 * y0)                                    # 불일치(5년물) 액면
def S(port, d):
    y = y0 + d; L = 100 * math.exp(-10 * y)
    A = sum(F * math.exp(-t * y) for F, t in port)
    return A - L
bar, mis = [(f5, 5), (f15, 15)], [(fm, 5)]
grid = [round(-0.03 + i * 0.001, 3) for i in range(61)]
save("M7E04", dict(Lpv=Lpv, f5=f5, f15=f15, fm=fm, C_bar=0.5 * 25 + 0.5 * 225,
     s_bar_m2=S(bar, -0.02), s_mis_m2=S(mis, -0.02), s_bar_p2=S(bar, 0.02), s_mis_p2=S(mis, 0.02),
     curve=[dict(d=d, bar=S(bar, d), mis=S(mis, d)) for d in grid],
     dd_A=3 * 100, dd_L=20 * 80, first=-(3 * 100 - 20 * 80) * -0.01))

# E05 두 블록 (pp.45–49)
lam, sig, gam = 0.04, 0.15, 3.6
psp = lam / (gam * sig**2); lhp = (1 / 1.25) * (20 / 20)
frs = [round(0.7 + i * 0.01, 2) for i in range(81)]
psp_r = round(psp, 1)  # 강의본: ≈ 50%
save("M7E05", dict(psp=psp, psp_r=psp_r, lhp=lhp, total=psp_r + lhp, swap=psp_r + lhp - 1,
     vol=[dict(k="헤지 19%", v=0.128), dict(k="헤지 100%", v=0.075)],
     hedge_curve=[dict(fr=fr, h=1 / fr) for fr in frs],
     pts=[dict(fr=1.25, h=1 / 1.25), dict(fr=1.20, h=1 / 1.20), dict(fr=0.80, h=1 / 0.80)]))

# E06 헤지 수단 (pp.50–54)
save("M7E06", dict(vm=401, liquid=123, buffer_bp=250, refill_days=5, notional=1223, market_cap=299,
     issue=87, pimco=600))

# E07 2022 영국 · SVB (pp.55–64)
svb_bonds, svb_D, svb_dy = 1170, 6, 0.025      # 억 달러, 년, 가정치(강의본)
save("M7E07", dict(boe_cap=65, boe_bought=19.3, budget=45, loss=150, aum2021=1.5,
     days_to_resign=32, tenure=49,
     svb=dict(assets=2090, deposits=1755, uninsured=0.86, bonds=svb_bonds, D=svb_D, dy=svb_dy,
              loss_calc=svb_bonds * svb_D * svb_dy, loss_disc=150, run=420, swap_closed=110, sale_loss=18)))
# E09 실습 결과 (p.69 실습 출력)
save("M7E09", dict(b100=dict(fire=0.087, hedge=0.89, dfr=-2.7), b250=dict(fire=0.0, hedge=1.0, dfr=-0.9)))
