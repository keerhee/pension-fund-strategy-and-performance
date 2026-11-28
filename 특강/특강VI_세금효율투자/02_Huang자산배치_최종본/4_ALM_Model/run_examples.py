"""모델 실행 예제: 검증(김 교수 사례) → 4계좌 사례 → Z → 공동 최적화 프런티어 → 상장 위치 선택.

실행:  python run_examples.py      결과: outputs/results.md, outputs/*.png
"""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from model import Asset, Account, Problem, solve_location, solve_joint, fill_order, proportional, evaluate

os.makedirs("outputs", exist_ok=True)
for f in fm.findSystemFonts():                      # 한글 폰트 자동 탐색
    if "NotoSansCJK" in f or "NanumGothic" in f or "AppleGothic" in f or "malgun" in f.lower():
        fm.fontManager.addfont(f)
fam = [f.name for f in fm.fontManager.ttflist if any(k in f.name for k in ("Noto Sans CJK", "NanumGothic", "AppleGothic", "Malgun"))]
plt.rcParams.update({"font.family": fam[0] if fam else "sans-serif", "axes.unicode_minus": False, "font.size": 14,
                     "axes.spines.top": False, "axes.spines.right": False})
NAVY, BLUE, GREEN, MUTED, AMBER = "#1B2C5E", "#2E5BAA", "#3FA36F", "#6B7280", "#C77700"
md = []
def P_(s=""): md.append(s)
def fmt(v): return f"{v:,.0f}"
def table(tab, assets):
    rows = ["| 계좌 | " + " | ".join(assets) + " | 합계 |", "|---|" + "---:|" * (len(assets) + 1)]
    for acc, d in tab.items():
        rows.append(f"| {acc} | " + " | ".join(fmt(d[a]) if d[a] > 0.5 else "—" for a in assets) + f" | {fmt(sum(d.values()))} |")
    return "\n".join(rows)

KR, FXK, BD, FXU = "국내주식형 ETF", "국내상장 해외주식형 ETF", "채권 ETF", "해외상장 주식 ETF"
base_assets = [Asset(KR, 0.06, 0.0, 0.20), Asset(FXK, 0.07, 0.0, 0.17), Asset(BD, 0.0, 0.04, 0.05)]
corr3 = np.array([[1, .6, -.1], [.6, 1, -.1], [-.1, -.1, 1]])
names3 = [a.name for a in base_assets]

# ------------------------------------------------ 1. 검증: 김 교수 사례
P_("# 한국형 자산배분·자산배치 모델 — 실행 결과\n")
P_("금액 단위는 만 원, 투자 기간 10년, 기대 수익 경로 기준(결정론적)이다. 세법은 `tax_rules_2026.py`(2026년 11월 기준)를 따른다.\n")
P_("## 1. 검증 — 김 교수 사례 재현\n")
P_("일반계좌 1억·연금저축 1억, 국내주식 6,000·해외주식 8,000·채권 6,000(표시 잔액), 연금 평가상 인출세율 5.5%.\n")
tgt = {KR: 6000, FXK: 8000, BD: 6000}
rows = ["| 연금 인출세율 | 배치 A (채권부터 연금) | 배치 B (해외주식부터 연금) | LP 최적 | 최적해의 연금계좌 구성 |", "|---|---:|---:|---:|---|"]
taus = np.round(np.arange(0.0, 0.201, 0.005), 3)
sweep = []
for tau in taus:
    P = Problem(base_assets, [Account("일반", 10000), Account("연금저축", 10000, pension_tax=tau)])
    r = solve_location(P, tgt, "pretax")
    I = r["_index"]
    xA = np.array([6000, 4000, 0, 0, 4000, 6000]); xB = np.array([6000, 0, 4000, 0, 8000, 2000])
    vA, vB = I.value(xA)["value"], I.value(xB)["value"]
    sweep.append((tau, vB - vA, r["table"]["연금저축"][FXK]))
    if tau in (0.055, 0.13, 0.135, 0.165):
        pen = r["table"]["연금저축"]
        rows.append(f"| {tau*100:.1f}% | {fmt(vA)} | {fmt(vB)} | {fmt(r['value'])} | 해외주식 {fmt(pen[FXK])} · 채권 {fmt(pen[BD])} |")
P_("\n".join(rows))
be = next(t for t, d, _ in sweep if d < 0)
P_(f"\n강의 자료의 값(A 33,847 · B 33,995 · 손익분기 약 13.1%)과 일치한다. LP는 인출세율 약 {be*100-0.5:.1f}~{be*100:.1f}% 사이에서 최적 배치를 '해외주식 우선'에서 '채권 우선'으로 바꾼다.\n")
fig, ax = plt.subplots(figsize=(9.5, 4.2))
ax.plot([t * 100 for t, _, _ in sweep], [d for _, d, _ in sweep], color=NAVY, lw=2.6, label="배치 B − 배치 A (만 원)")
ax.axhline(0, color=MUTED, lw=1)
ax2 = ax.twinx(); ax2.step([t * 100 for t, _, _ in sweep], [f for _, _, f in sweep], color=AMBER, lw=2.2, where="mid", label="최적해의 연금 내 해외주식 (만 원)")
ax2.spines["top"].set_visible(False)
ax.set_xlabel("연금 평가상 인출세율 (%)"); ax.set_ylabel("배치 B − 배치 A (만 원)"); ax2.set_ylabel("연금 내 해외주식 (만 원)")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="lower left", frameon=False, fontsize=12)
fig.tight_layout(); fig.savefig("outputs/fig1_kim_tau_sweep.png", dpi=200); plt.close(fig)
P_("![인출세율에 따른 배치 전환](fig1_kim_tau_sweep.png)\n")

# ------------------------------------------------ 2. 4계좌 사례와 기준 전략
P_("## 2. 4계좌 2억 원 — 기준 전략과 최적 배치\n")
P_("일반 1억 · ISA(일반형) 4,000만 · 연금저축 3,000만 · IRP 3,000만. 목표는 표시 잔액 기준 국내주식 6,000 · 해외주식 8,000 · 채권 6,000. 연금 인출세율 5.5%, ISA는 10년 뒤 한 번 정산(200만 원 비과세, 초과 9.9%), IRP 위험자산 70% 한도.\n")
acc4 = [Account("일반", 10000), Account("ISA", 4000), Account("연금저축", 3000, pension_tax=0.055), Account("IRP", 3000, pension_tax=0.055)]
P4 = Problem(base_assets, acc4, horizon=10, isa_type="일반형")
opt = solve_location(P4, tgt, "pretax")
bench = {
    "계좌마다 같은 비중": proportional(P4, tgt),
    "채권부터 절세계좌": fill_order(P4, tgt, [BD, FXK, KR]),
    "해외주식부터 절세계좌": fill_order(P4, tgt, [FXK, BD, KR]),
}
rows = ["| 전략 | 10년 뒤 세후 가치 | 최적 대비 | ISA 세금 |", "|---|---:|---:|---:|"]
vals = {}
for k, x in bench.items():
    v = evaluate(P4, x); vals[k] = v["value"]
    rows.append(f"| {k} | {fmt(v['value'])} | {v['value']-opt['value']:+,.0f} | {fmt(v['tax_isa'])} |")
vals["LP 최적 배치"] = opt["value"]
rows.append(f"| **LP 최적 배치** | **{fmt(opt['value'])}** | 0 | {fmt(opt['tax_isa'])} |")
P_("\n".join(rows)); P_("")
P_("최적 배치(표시 잔액, 만 원):\n"); P_(table(opt["table"], names3)); P_("")
fig, ax = plt.subplots(figsize=(9.5, 3.8))
ks = list(vals); vs = [vals[k] for k in ks]
ax.barh(ks, vs, color=[MUTED, BLUE, BLUE, NAVY])
for i, v in enumerate(vs): ax.text(v + 40, i, f"{v:,.0f}", va="center", fontsize=13, fontweight="bold", color=NAVY)
ax.set_xlim(min(vs) - 600, max(vs) + 600); ax.set_xlabel("10년 뒤 세후 가치 (만 원)"); ax.invert_yaxis()
fig.tight_layout(); fig.savefig("outputs/fig2_benchmarks.png", dpi=200); plt.close(fig)
P_("![기준 전략 비교](fig2_benchmarks.png)\n")

# ------------------------------------------------ 3. 계좌별 한계가치 Z
P_("## 3. 계좌별 한계가치 Z — 1원을 어느 계좌에 더 넣을까\n")
P_("세후 비중(국내 30 · 해외 40 · 채권 30)을 유지하면서 각 계좌에 1원을 더 넣었을 때 10년 뒤 세후 가치가 얼마나 늘어나는지(λ)를 LP의 쌍대가격으로 구하고, 일반계좌 대비 비율 Z = λ계좌 / λ일반을 계산한다. 새 납입의 세액공제는 포함하지 않는다.\n")
zres = {}
rows = ["| 연금 인출세율 | λ 일반 | λ ISA | λ 연금저축 | λ IRP | Z ISA | Z 연금저축 | Z IRP |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for tau in (0.033, 0.055, 0.165):
    P = Problem(base_assets, [Account("일반", 10000), Account("ISA", 4000), Account("연금저축", 3000, pension_tax=tau), Account("IRP", 3000, pension_tax=tau)])
    r = solve_location(P, {KR: .3, FXK: .4, BD: .3}, "aftertax")
    L, Z = r["lambda"], r["Z"]; zres[tau] = Z
    rows.append(f"| {tau*100:.1f}% | {L['일반']:.3f} | {L['ISA']:.3f} | {L['연금저축']:.3f} | {L['IRP']:.3f} | {Z['ISA']:.3f} | {Z['연금저축']:.3f} | {Z['IRP']:.3f} |")
P_("\n".join(rows))
P_("\nλ는 '지금 1원 → 10년 뒤 세후 몇 원'이다. ISA는 비과세 한도 200만 원을 이미 넘긴 상태라 한계 세율 9.9%가 적용된다. 인출세율이 오르면 연금계좌의 Z가 1 아래로 떨어질 수 있다. 일하는 은퇴자가 새로 넣는 돈은 여기에 세액공제 13.2~16.5%가 더해진다.\n")
fig, ax = plt.subplots(figsize=(9.5, 3.8))
labs = ["ISA", "연금저축", "IRP"]; w = 0.26
for j, (tau, col) in enumerate([(0.033, GREEN), (0.055, NAVY), (0.165, AMBER)]):
    ys = [zres[tau][l] for l in labs]
    ax.bar(np.arange(3) + (j - 1) * w, ys, w, color=col, label=f"인출세율 {tau*100:.1f}%")
    for i, y in enumerate(ys): ax.text(i + (j - 1) * w, y + 0.004, f"{y:.3f}", ha="center", fontsize=11.5)
ax.axhline(1, color=MUTED, lw=1.2, ls="--"); ax.set_xticks(range(3)); ax.set_xticklabels(labs)
lo = min(min(z.values()) for z in zres.values()); hi = max(max(z.values()) for z in zres.values())
ax.set_ylim(lo - 0.03, hi + 0.03); ax.set_ylabel("Z (일반계좌 = 1)"); ax.legend(frameon=False, ncol=3, fontsize=12, loc="upper center", bbox_to_anchor=(0.5, 1.18))
fig.tight_layout(); fig.savefig("outputs/fig3_Z.png", dpi=200); plt.close(fig)
P_("![계좌별 Z](fig3_Z.png)\n")

# ------------------------------------------------ 4. 공동 최적화 프런티어
P_("## 4. 배분과 배치를 함께 — 위험회피 계수별 해\n")
P_("목적함수는 '세후 기대 최종가치 − (γ/2)·세후 위험 벌점'이다. 위험은 세후 노출(연금은 0.945만 내 몫)로 잰다. 변동성 국내 20% · 해외 17% · 채권 5%, 주식 간 상관 0.6, 주식-채권 상관 −0.1 (예시 가정).\n")
Pj = Problem(base_assets, acc4, horizon=10, isa_type="일반형", corr=corr3)
gammas = [1, 1.5, 2, 3, 4, 6, 8, 12, 20]
fr = []
rows = ["| γ | 세후 주식 비중 | 국내 · 해외 · 채권 (세후 비중) | 연금·IRP 안의 주식 | ISA 구성 | 세후 기대가치 | 확실성 등가 |", "|---:|---:|---|---:|---|---:|---:|"]
for g in gammas:
    r = solve_joint(Pj, g)
    w = r["weights"]; t = r["table"]
    pen_eq = sum(t[a][n] for a in ("연금저축", "IRP") for n in (KR, FXK))
    isa = t["ISA"]
    fr.append((g, w[0] + w[1], pen_eq, r["value"], r["ce"], w))
    rows.append(f"| {g} | {(w[0]+w[1])*100:.0f}% | {w[0]*100:.0f} · {w[1]*100:.0f} · {w[2]*100:.0f} | {fmt(pen_eq)} | 국내 {fmt(isa[KR])} · 해외 {fmt(isa[FXK])} · 채권 {fmt(isa[BD])} | {fmt(r['value'])} | {fmt(r['ce'])} |")
P_("\n".join(rows))
P_("\n읽는 법은 세 가지다.\n")
P_("1. **세금 순위는 위험 성향과 관계없이 유지된다.** 해외주식형 ETF는 언제나 연금·IRP를 먼저 채우고 그다음 ISA로 가며, 국내주식형 ETF는 일반계좌에 남는다. 위험 성향이 바꾸는 것은 순위가 아니라 각 자산의 양이다(Huang의 분리).")
P_("2. **주식 수요가 줄면 빈자리를 채권이 채운다.** γ가 커져 해외주식 수요가 연금 용량(연금저축 3,000 + IRP 2,100)보다 작아지면, 연금에도 채권이 들어간다. 그래도 일반계좌에 채권이 남는 것은 해외주식이 채권보다 절세계좌를 쓸 가치가 크기 때문이다.")
P_("3. **제약이 걸리면 배치가 왜곡된다.** γ = 1(주식 94%)에서 투자자는 거의 전부 주식을 원하지만, IRP 위험자산 70% 한도 때문에 IRP에 채권 900만 원이 강제로 들어간다. 그만큼 해외주식 5,293만 원이 세금 내는 일반계좌로 밀려난다. 위험을 과세계좌에서 마음대로 되돌릴 수 없다는 Huang 전제 ①이 깨진 모습이다.\n")
for g in (1, 4, 12):
    P_(f"γ = {g}일 때 배치(표시 잔액, 만 원):\n")
    P_(table(solve_joint(Pj, g)["table"], names3)); P_("")
fig, ax = plt.subplots(figsize=(9.5, 4.0))
ax.plot([f[0] for f in fr], [f[1] * 100 for f in fr], "o-", color=NAVY, lw=2.4, label="세후 주식 비중 (%)")
ax.set_xscale("log"); ax.set_xlabel("위험회피 계수 γ (로그 눈금)"); ax.set_ylabel("세후 주식 비중 (%)")
ax2 = ax.twinx(); ax2.spines["top"].set_visible(False)
ax2.plot([f[0] for f in fr], [f[2] for f in fr], "s--", color=AMBER, lw=2.2, label="연금·IRP 안의 주식 (만 원)")
ax2.set_ylabel("연금·IRP 안의 주식 (만 원)")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=12, loc="upper right")
fig.tight_layout(); fig.savefig("outputs/fig4_frontier.png", dpi=200); plt.close(fig)
P_("![위험회피 계수별 배분과 배치](fig4_frontier.png)\n")

# ------------------------------------------------ 5. 상장 위치 선택 (국내상장 vs 해외상장)
P_("## 5. 같은 해외주식, 국내상장과 해외상장 중 어디로?\n")
P_("해외주식 8,000만 원을 국내상장 ETF(15.4%, 절세계좌 가능)와 해외상장 ETF(22%, 연 250만 원 공제, 일반계좌만 가능) 중 어떻게 나눌지도 모델이 고르게 한다. 두 상품의 기대수익은 같다고 둔다.\n")
assets4 = base_assets + [Asset(FXU, 0.07, 0.0, 0.17)]
P5 = Problem(assets4, acc4, horizon=10)
rows = ["| 투자 기간 | 해외상장 ETF (일반계좌) | 국내상장 해외 ETF | 세후 가치 | 해외 양도세 |", "|---|---:|---:|---:|---:|"]
for T in (3, 10, 20):
    P5.horizon = T
    r = solve_location(P5, {KR: 6000, (FXK, FXU): 8000, BD: 6000}, "pretax")
    t = r["table"]
    fxu = sum(t[a][FXU] for a in t); fxk = sum(t[a][FXK] for a in t)
    rows.append(f"| {T}년 | {fmt(fxu)} | {fmt(fxk)} | {fmt(r['value'])} | {fmt(r['tax_foreign'])} |")
P_("\n".join(rows))
P_("\n해외상장 ETF는 연 250만 원 공제가 있지만 모델은 투자 기간 전체에 한 번만 공제를 쓴다(매도를 마지막에 몰아서 하는 가정). 해마다 이익을 250만 원씩 실현해 공제를 반복해 쓰는 전략은 이 모델에 들어 있지 않으므로, 실제로는 해외상장 쪽이 더 유리할 수 있다.\n")

P_("## 6. 모델의 가정과 한계\n")
P_("- 기대 수익 경로를 따라 세금을 계산한다(결정론적). 시나리오별 위험은 4절의 평균-분산 근사로만 반영한다.")
P_("- 국내상장 ETF는 과표기준가 상승분을 실제 매매차익과 같다고 둔다. 해외 원천징수, 금융소득종합과세(연 2,000만 원 초과), 거래비용, 수수료는 넣지 않았다.")
P_("- ISA는 투자 기간 끝에 한 번 정산하고, 연금은 계좌 전체에 평가상 인출세율 하나를 곱한다(연금수령한도·연 1,500만 원 기준은 별도 확인).")
P_("- 위험 노출에서 일반계좌·ISA는 세금의 위험 분담을 무시하고(지분 1), 연금계좌만 1 − 인출세율로 잡는다.")
P_("- 수치는 2026년 11월 세법 기준의 예시이며 투자 권유가 아니다.")
open("outputs/results.md", "w", encoding="utf-8").write("\n".join(md))
print("done")
