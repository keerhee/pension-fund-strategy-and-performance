"""M7 E03 화면 숫자 계산 — 강의본 pp.29–36의 예시 기금과 같은 가정."""
import json, math, pathlib
A, DA, L, DL = 100.0, 3.0, 80.0, 20.0
dy = -0.01
A1, L1 = A * (1 - DA * dy), L * (1 - DL * dy)
S0, S1 = A - L, A1 - L1
# 기본 지식: 20년 뒤 100
pv5, pv6 = 100 / 1.05**20, 100 / 1.06**20
# DV01
dv_a, dv_l = DA * A * 1e-4, DL * L * 1e-4
# 볼록성: 10년 뒤 100, 연속복리 5%
V = 100 * math.exp(-0.5); D, C = 10.0, 100.0
conv = []
for d in (0.01, -0.01, 0.02):
    exact = 100 * math.exp(-10 * (0.05 + d)) - V
    first = -D * V * d
    conv.append(dict(dy=d, exact=exact, first=first, second=first + 0.5 * C * V * d * d))
curve = [dict(y=y / 1000, v=100 * math.exp(-10 * y / 1000)) for y in range(10, 91, 2)]
# 헤지비율: 강의본 p.36 포트폴리오별 자산 DV01
ports = [("전부 D=3", 0.03), ("50을 30년물로", 0.115), ("80은 30년물 + 20은 주식", 0.16)]
hedge = [dict(label=k, dv=v, h=v / dv_l) for k, v in ports]
out = dict(A=A, DA=DA, L=L, DL=DL, A1=A1, L1=L1, S0=S0, S1=S1,
           FR0=A / L, FR1=A1 / L1, surplus_chg=S1 / S0 - 1, gap=DA - DL,
           pv5=pv5, pv6=pv6, pv_chg=pv6 / pv5 - 1,
           dv_a=dv_a, dv_l=dv_l, dv_gap=dv_a - dv_l,
           V=V, D=D, C=C, conv=conv, curve=curve, hedge=hedge,
           nps_gap=-34, nps_h=0.021, nps_h_2027=0.03)
p = pathlib.Path(__file__).resolve().parents[1] / "src/data/M7E03.numbers.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"surplus {S0:.1f}->{S1:.1f} ({out['surplus_chg']:.1%}), FR {out['FR0']:.1%}->{out['FR1']:.1%}, pv {pv5:.1f}->{pv6:.1f} ({out['pv_chg']:.1%})")
for c in conv: print({k: round(v, 3) for k, v in c.items()})
for h in hedge: print(h['label'], f"{h['h']:.1%}")
