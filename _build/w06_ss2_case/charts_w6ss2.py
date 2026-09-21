#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 SS2 케이스 v3 그림 — w6ss2_results.json · CSV 에서 그린다 (matplotlib, Noto Sans CJK KR). 출력 img/*.png + img/img_ratios.json"""
import json, os, math
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D, IMG = f"{ROOT}/data", f"{ROOT}/img"; os.makedirs(IMG, exist_ok=True)
fm.fontManager.addfont(os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc"))
plt.rcParams.update({"font.family": "Noto Sans CJK KR", "font.size": 15, "axes.titlesize": 17, "axes.labelsize": 15,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#6B7280", "axes.unicode_minus": False})
NAVY, BLUE, GREEN, ORANGE, GRAY, BODY, MUTED, HAIR, RED = "#1B2C5E", "#2E5BAA", "#3FA36F", "#E65100", "#F4F5F9", "#3B4252", "#6B7280", "#D6D6DB", "#B23A48"
R = json.load(open(f"{D}/w6ss2_results.json")); A1, A2 = R["agenda1"], R["agenda2"]
kospi = pd.read_csv(f"{D}/fml_w6ss2_kospi_2026.csv"); snap = pd.read_csv(f"{D}/fml_w6ss2_nps_snapshot.csv").set_index("nps_class")
inst = pd.read_csv(f"{D}/fml_w6ss2_institutions.csv")
RU = A1["rules"]; OPT = A1["options"]


def save(fig, name):
    fig.savefig(f"{IMG}/{name}.png", dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print("→", name)


# 1. 2026년 상반기 — 코스피와 국민연금 국내주식 비중 ----------------------------------
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.3), gridspec_kw={"width_ratios": [1.25, 1]}); fig.subplots_adjust(top=0.82, wspace=0.22)
kd = kospi.copy(); kd["d"] = pd.to_datetime(kd.date); k26 = kd[kd.d >= "2025-12-30"]
ax.plot(k26.d, k26.kospi_close, color=NAVY, lw=2.8, marker="o", ms=6)
for _, r in k26.iterrows():
    ax.annotate(f"{r.kospi_close:,.0f}", (r.d, r.kospi_close), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=12, color=BODY)
for d, lab, y, ha in [("2026-01-26", "1.26 유예", 4100, "left"), ("2026-05-28", "5.28 목표·밴드 확대", 9900, "right"), ("2026-06-30", "6.30 유예 종료", 4100, "left"), ("2026-07-02", "", 0, "left")]:
    ax.axvline(pd.Timestamp(d), color=ORANGE if "5.28" in lab else HAIR, lw=1.3, ls=":")
    if lab: ax.text(pd.Timestamp(d), y, " " + lab + " ", va="top" if y > 6000 else "bottom", ha=ha, fontsize=11.5, color=ORANGE if "5.28" in lab else MUTED)
ax.set_ylim(3800, 10200); ax.set_ylabel("코스피 종가"); ax.set_title("코스피 — 5,052 → 9,386(6.19 장중) → 6,259(7.7, −33%)", loc="left", color=NAVY, fontsize=14)
ax.grid(axis="y", color=HAIR, lw=0.8)
import matplotlib.dates as mdates
for a_ in (ax,): a_.xaxis.set_major_locator(mdates.MonthLocator(interval=2)); a_.xaxis.set_major_formatter(mdates.DateFormatter("%y.%m")); a_.tick_params(axis="x", labelsize=11)
pts = k26.dropna(subset=["nps_kr_eq_pct"])
bx.plot(pts.d, pts.nps_kr_eq_pct, color=NAVY, lw=2.8, marker="s", ms=7, label="국내주식 실제 비중")
for _, r in pts.iterrows(): bx.annotate(f"{r.nps_kr_eq_pct:.1f}%", (r.d, r.nps_kr_eq_pct), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=12, color=BODY)
t_old, t_new = snap.loc["eq_kr", "target_2026_jan_pct"], snap.loc["eq_kr", "target_2026_pct"]
bx.hlines(t_old, pd.Timestamp("2025-12-30"), pd.Timestamp("2026-05-28"), color=GREEN, lw=2, ls="--", label=f"목표 {t_old}% (1월)")
bx.hlines(t_new, pd.Timestamp("2026-05-28"), pd.Timestamp("2026-09-18"), color=GREEN, lw=2, label=f"목표 {t_new}% (5.28~)")
bx.fill_between([pd.Timestamp("2025-12-30"), pd.Timestamp("2026-05-28")], t_old - 3, t_old + 3, color=GREEN, alpha=0.12)
bx.fill_between([pd.Timestamp("2026-05-28"), pd.Timestamp("2026-09-18")], t_new - 6, t_new + 6, color=ORANGE, alpha=0.12)
bx.text(pd.Timestamp("2026-01-05"), t_old - 4.3, "SAA 밴드 ±3(지침)", fontsize=11, color=GREEN); bx.text(pd.Timestamp("2026-07-10"), t_new - 7.3, "한시 밴드 ±6", fontsize=11, color=ORANGE)
bx.set_ylim(6, 34); bx.set_ylabel("국내주식 비중 (%)"); bx.set_title("국민연금 국내주식 — 18.1 → 29.1%, 목표 위 8.3%p", loc="left", color=NAVY, fontsize=14)
bx.legend(loc="upper left", frameon=False, fontsize=11); bx.grid(axis="y", color=HAIR, lw=0.8); bx.xaxis.set_major_locator(mdates.MonthLocator(interval=2)); bx.xaxis.set_major_formatter(mdates.DateFormatter("%y.%m")); bx.tick_params(axis="x", labelsize=11)
fig.suptitle("2026년 상반기 — 규칙을 멈추자 비중이 달렸고, 규칙을 다시 켜기 전에 시장이 먼저 돌아섰다", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_kospi_2026")

# 2. 조건 ① — 자산군별 AR(1) φ · t ---------------------------------------------------
c1 = pd.DataFrame(A1["cond1"]); names = [n.split("(")[0] for n in c1.name]
fig, ax = plt.subplots(figsize=(12.5, 5.2))
cols = [GREEN if k == "평균회귀" else (ORANGE if k == "추세" else MUTED) for k in c1.kind]
ax.barh(names, c1.t, color=cols, height=0.58); ax.invert_yaxis()
ax.axvline(-2, color=NAVY, ls=":", lw=1.5); ax.axvline(2, color=NAVY, ls=":", lw=1.5); ax.axvline(0, color=HAIR, lw=1)
for i, r in c1.iterrows():
    ax.text(max(r.t, 0) + 0.15, i, f"t {r.t:+.2f} · φ {r.phi:+.2f} · VR(12) {r.vr12:.2f} → {r.kind} · 밴드 {r.band_hint}", va="center", ha="left", fontsize=12.5, color=BODY)
ax.set_xlim(-4.5, 9.5); ax.set_xlabel("월간 수익률 AR(1) φ 의 t값 (240개월) — 임계 ±2"); ax.grid(axis="x", color=HAIR, lw=0.8)
ax.set_title("조건 ① 평균회귀 — 신흥주식 · 상장 부동산은 평균회귀(좁은 밴드), 국고채는 추세(넓은 밴드), 국내 · 선진주식은 랜덤워크(지침 값 유지)", loc="left", color=NAVY, fontsize=15)
save(fig, "fig_ar1")

# 3. 빈도의 경제학 — DR · 비용 · 순 (NPS 규모 vs 소형) ---------------------------------
freq = [("cal_d", "일간"), ("cal_w", "주간"), ("cal_m", "월간"), ("cal_q", "분기"), ("cal_s", "반기"), ("cal_a", "연간")]
fig, ax = plt.subplots(figsize=(12.5, 5.3)); x = np.arange(len(freq)); wdt = 0.26
dr = [RU[k]["DR_bp"] for k, _ in freq]; cost = [RU[k]["cost_bp"] for k, _ in freq]; net = [RU[k]["net_bp"] for k, _ in freq]; net_s = [RU[k + "_small"]["net_bp"] for k, _ in freq]
ax.bar(x - wdt, dr, wdt, color=BLUE, label="분산수익 DR (gross)"); ax.bar(x, cost, wdt, color=RED, label="거래비용 — NPS 규모(스프레드 + 시장충격)"); ax.bar(x + wdt, net, wdt, color=GREEN, label="순 프리미엄 — NPS 규모")
ax.plot(x + wdt, net_s, color=NAVY, marker="D", ms=7, lw=0, label="순 프리미엄 — 소형 기관(스프레드만)")
for i in range(len(freq)):
    ax.text(x[i] - wdt, dr[i] + 1, f"{dr[i]:.0f}", ha="center", fontsize=12, color=BODY); ax.text(x[i], cost[i] + 1, f"{cost[i]:.1f}", ha="center", fontsize=12, color=BODY); ax.text(x[i] + wdt, net[i] + 1, f"{net[i]:.0f}", ha="center", fontsize=12, color=BODY, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels([n for _, n in freq]); ax.set_ylabel("bp / 년"); ax.set_ylim(0, 90)
best = A1["best_nps"]; ax.set_title(f"조건 ② 빈도의 경제학 — DR은 완만히 줄고 비용은 가파르게 준다 · NPS 규모 최적 {dict(freq)[best['rule']]} {best['net_bp']:+.0f}bp, 분기와 2bp 차이", loc="left", color=NAVY, fontsize=15)
ax.legend(loc="upper right", frameon=False, fontsize=12, ncol=2); ax.grid(axis="y", color=HAIR, lw=0.8)
save(fig, "fig_freq")

# 4. 밴드 폭 민감도(안 B 구조) + 세 안 -------------------------------------------------
sens = pd.DataFrame(A1["sens_band"])
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.2), gridspec_kw={"width_ratios": [1.15, 1]}); fig.subplots_adjust(top=0.82, wspace=0.25)
lab = [("월 복원(밴드 0)" if b == 0 else f"±{b}") for b in sens.band]
ax.bar(lab, sens.DR_bp, color=BLUE, width=0.55, label="DR"); ax.bar(lab, -sens.cost_bp, color=RED, width=0.55, label="비용(현물 + 선물)")
ax.plot(lab, sens.net_bp, color=GREEN, marker="o", ms=8, lw=2.5, label="순 프리미엄")
for i, r in sens.iterrows(): ax.text(i, r.net_bp + 2.5, f"{r.net_bp:+.0f}", ha="center", fontsize=12.5, color=GREEN, fontweight="bold"); ax.text(i, -r.cost_bp - 4.5, f"{r.max_trade_trn}조", ha="center", fontsize=11, color=BODY)
ax.axhline(0, color=HAIR, lw=1); ax.set_ylim(-14, 72); ax.set_ylabel("bp / 년"); ax.set_xlabel("자산군 밴드 폭 (월 점검 · 월 25bp 한도 · 총 위험 ±2 오버레이)")
ax.set_title("밴드가 넓을수록 DR을 버린다 (막대 아래 = 최대 단일거래)", loc="left", color=NAVY, fontsize=14); ax.legend(loc="upper right", frameon=False, fontsize=12); ax.grid(axis="y", color=HAIR, lw=0.8)
ks = ["A", "B", "C"]; xx = np.arange(3); wd = 0.26
bx.bar(xx - wd, [OPT[k]["net_bp"] for k in ks], wd, color=GREEN, label="순 프리미엄 bp")
bx.bar(xx, [OPT[k]["risk_dev_max_pp"] * 10 for k in ks], wd, color=ORANGE, label="위험 드리프트 최대 %p (×10)")
bx.bar(xx + wd, [OPT[k]["pct_days_over_cvar"] * 2 for k in ks], wd, color=RED, label="CVaR 한도 초과일 % (×2)")
for i, k in enumerate(ks):
    bx.text(xx[i] - wd, OPT[k]["net_bp"] + 1, f"{OPT[k]['net_bp']:+.0f}", ha="center", fontsize=12, color=BODY); bx.text(xx[i], OPT[k]["risk_dev_max_pp"] * 10 + 1, f"{OPT[k]['risk_dev_max_pp']:+.1f}", ha="center", fontsize=12, color=BODY); bx.text(xx[i] + wd, OPT[k]["pct_days_over_cvar"] * 2 + 1, f"{OPT[k]['pct_days_over_cvar']:.1f}%", ha="center", fontsize=12, color=BODY)
bx.set_xticks(xx); bx.set_xticklabels(["안 A\n분기 전량 복원", "안 B\n밴드 + 오버레이", "안 C\n±6 상시화"], fontsize=12); bx.set_ylim(0, 72)
bx.set_title("세 안을 같은 자로 — A는 크지만 못 지킨다", loc="left", color=NAVY, fontsize=14); bx.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False, fontsize=11, ncol=1); bx.grid(axis="y", color=HAIR, lw=0.8)
fig.suptitle("조건 ② 산수 — 안 B 의 밴드 폭 민감도와 세 안의 비교 (20년 모의 패널 · NPS 규모 비용)", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_band_sens")

# 5. 조건 ③ 시장충격 — 시나리오 × 실행 방법 (거래일, 로그축) ------------------------------
c3 = pd.DataFrame(A1["cond3"]); meta = A1["cond3_meta"]
fig, ax = plt.subplots(figsize=(12.5, 5.4)); y = np.arange(len(c3)); h = 0.26
ax.barh(y - h, c3.days_cap25bp, h, color=RED, label=f"현물 · 월 25bp 한도(일 {meta['cap_per_day_trn']}조)")
ax.barh(y, c3.days_cash5pct_2026, h, color=ORANGE, label=f"현물 · 거래대금 {meta['adv_2026']}조의 5% 참여")
ax.barh(y + h, c3.days_fut20pct, h, color=GREEN, label=f"지수선물 · 선물 거래대금 {meta['adv_fut']:.0f}조의 20% 참여")
for i, r in c3.iterrows():
    ax.text(r.days_cap25bp * 1.08, i - h, f"{r.days_cap25bp:.0f}일", va="center", fontsize=12, color=BODY); ax.text(r.days_cash5pct_2026 * 1.08, i, f"{r.days_cash5pct_2026:.0f}일", va="center", fontsize=12, color=BODY); ax.text(r.days_fut20pct * 1.08, i + h, f"{r.days_fut20pct:.0f}일", va="center", fontsize=12, color=BODY)
ax.set_yticks(y); ax.set_yticklabels([f"{r.scenario}\n{r.amount_trn:.0f}조" for _, r in c3.iterrows()], fontsize=12); ax.invert_yaxis()
ax.set_xscale("log"); ax.set_xlim(1, 3000); ax.axvline(20, color=NAVY, ls=":", lw=2); ax.text(21, 4.62, "임계 20 거래일", color=NAVY, fontsize=12.5, fontweight="bold")
ax.set_xlabel("복원 거래를 끝내는 데 걸리는 거래일 (로그축)"); ax.grid(axis="x", color=HAIR, lw=0.8)
ax.set_title("조건 ③ 시장충격 — 현물로는 한 달 안에 못 끝낸다, 선물 오버레이만 20일 안에 든다 (2026.6 말 공시 갭 기준)", loc="left", color=NAVY, fontsize=15)
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.14), frameon=False, fontsize=12, ncol=3)
save(fig, "fig_impact")

# 6. 조건 ④ — CVaR 곡선과 드리프트 분포 ------------------------------------------------
c4 = A1["cond4"]; MU_R, MU_S, SG_R, SG_S, RHO = 8.0, 3.0, 15.0, 4.5, 0.10
def cvar(w):
    mu = w * MU_R + (1 - w) * MU_S; sg = math.sqrt((w * SG_R) ** 2 + ((1 - w) * SG_S) ** 2 + 2 * w * (1 - w) * SG_R * SG_S * RHO); return mu - 2.0627 * sg
ws = np.arange(0.50, 0.85, 0.005)
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.5, 5.2), gridspec_kw={"width_ratios": [1.15, 1]}); fig.subplots_adjust(top=0.82, wspace=0.22)
ax.plot(ws * 100, [cvar(w) for w in ws], color=NAVY, lw=3)
ax.axhline(-15, color=RED, ls=":", lw=2, label="위험한도 CVaR95 ≥ −15% (지침 제6조의2)")
for w, lab, col, off in [(65, f"기준포트폴리오 65% → {c4['cvar_65']}%", GREEN, (-14, 14)), (c4["w_max_pct"], f"상한 w_max {c4['w_max_pct']}% → −15.0%", ORANGE, (12, 10)), (c4["w_2026_06_pct"], f"2026.6 실제 {c4['w_2026_06_pct']}% → {c4['cvar_2026_06']}%", RED, (12, -16))]:
    ax.plot([w], [cvar(w / 100)], "o", color=col, ms=10); ax.annotate(lab, (w, cvar(w / 100)), textcoords="offset points", xytext=off, ha="right" if off[0] < 0 else "left", fontsize=12, color=col)
ax.set_xlabel("위험자산 비중 (%) — 기준포트폴리오 척도"); ax.set_ylabel("CVaR95 (연, %)"); ax.set_ylim(-21, -10); ax.grid(color=HAIR, lw=0.8)
ax.set_title(f"CVaR 곡선 — 65%에서 −14.4%, 여유는 ±{c4['band_max_pp']}%p 뿐이다", loc="left", color=NAVY, fontsize=14); ax.legend(loc="lower left", frameon=False, fontsize=11)
d12 = c4["drift_12m"]; d3 = c4["drift_3m"]
bx.bar(["3M σ", "3M 95%", "3M 최대", "12M σ", "12M 95%", "12M 최대", "2026 상반기\n(공시)"], [d3["std"], d3["p95"], d3["max"], d12["std"], d12["p95"], d12["max"], c4["drift_2026_06_pp"]],
       color=[MUTED, MUTED, ORANGE, MUTED, MUTED, ORANGE, RED], width=0.6)
for i, v in enumerate([d3["std"], d3["p95"], d3["max"], d12["std"], d12["p95"], d12["max"], c4["drift_2026_06_pp"]]): bx.text(i, v + 0.15, f"{v:+.1f}", ha="center", fontsize=12, color=BODY)
bx.axhline(c4["band_max_pp"], color=RED, ls=":", lw=2, label=f"허용 드리프트 +{c4['band_max_pp']}%p (CVaR 상한)")
bx.axhline(2.0, color=GREEN, ls="--", lw=1.5, label="안 B 총 위험 밴드 ±2"); bx.legend(loc="upper left", frameon=False, fontsize=11)
bx.set_ylabel("위험자산 비중 드리프트 (%p, 리밸런싱 없이)"); bx.set_ylim(0, 10.5); bx.tick_params(axis="x", labelsize=11); bx.grid(axis="y", color=HAIR, lw=0.8)
bx.set_title("드리프트 — 분기 규칙(A)도 3개월 최대 4.5%p, 2026 형은 9%p", loc="left", color=NAVY, fontsize=14)
fig.suptitle("조건 ④ 위험 이탈 — 리밸런싱은 수익 장치이기 전에 위험한도를 지키는 장치다", x=0.01, y=0.97, ha="left", color=NAVY, fontsize=17)
save(fig, "fig_cvar")

# 7. 제2호 — 4기관 지도 (실행일수 × 현금흐름 용량) ------------------------------------
ins = pd.DataFrame(A2["institutions"]); sd = A2["drift_12m_sd"]
fig, ax = plt.subplots(figsize=(12.5, 5.4))
xs = [];
for _, r in ins.iterrows():
    x = r.days_3pp if pd.notna(r.days_3pp) and r.days_3pp is not None else 3000
    x = max(x, 0.01); xs.append(x)
    col = {"NPS": NAVY, "KIC": BLUE, "SWF": RED, "UNIV": GREEN}[r.code]
    ax.scatter([x], [abs(r.net_flow_pct)], s=max(220, math.sqrt(r.aum_trn_krw) * 40), color=col, alpha=0.75, edgecolor="white", lw=1.5)
    lab = {"NPS": f"국민연금 1,866조 · 3%p = {r.days_3pp:.0f}일 · 흐름 +0.75%\n→ 밴드 ±3 + 오버레이 · 월 · 한도",
           "KIC": f"KIC 333조(2,320억 달러) · 3%p = 0.2일 · 흐름 0\n→ 월말 목표 복원 · 현물 즉시",
           "SWF": "전략형 국부펀드 20조(2027 계획) · 비상장 95% → ∞\n→ 밴드 부적용 · 집중 한도 · 유동성 하한",
           "UNIV": "H대 발전기금 5,000억(가상)\n3%p = 0일 · 흐름 −3%/년 · 비유동 10%\n→ 현금흐름 우선 · 월 점검 · 잔여 현물"}[r.code]
    off = {"NPS": (0, 30), "KIC": (26, -44), "SWF": (0, -62), "UNIV": (26, -10)}[r.code]; ha = {"NPS": "center", "KIC": "left", "SWF": "right", "UNIV": "left"}[r.code]
    ax.annotate(lab, (x, abs(r.net_flow_pct)), textcoords="offset points", xytext=off, ha=ha, fontsize=11.5, color=col)
ax.axvline(20, color=NAVY, ls=":", lw=2); ax.text(23, 4.6, "조건 ③ 임계 20일 — 오른쪽은 현물로 못 끝냄", color=NAVY, fontsize=11.5)
ax.axhline(0.5 * sd, color=GREEN, ls="--", lw=1.5); ax.text(0.25, 0.5 * sd + 0.1, f"현금흐름 용량 임계 ½σ = {0.5*sd:.1f}%/년", color=GREEN, fontsize=11.5)
ax.set_xscale("log"); ax.set_xlim(0.004, 20000); ax.set_ylim(-0.6, 5.2)
ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000, 3000]); ax.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1,000", "∞(비상장)"])
ax.set_xlabel("3%p 복원 거래를 끝내는 거래일 (현물 5% 참여, 로그축)"); ax.set_ylabel("|연간 순현금흐름| ÷ 자산 (%)"); ax.grid(color=HAIR, lw=0.8)
ax.set_title("네 기관은 같은 좌표에 있지 않다 — 실행일수와 현금흐름 용량이 규칙을 정한다 (원의 크기 = 자산)", loc="left", color=NAVY, fontsize=15)
save(fig, "fig_inst_map")

# 8. 제2호 — NPS 규칙을 그대로 쓰면 vs 자기 규칙 ------------------------------------
rows = [r for r in A2["institutions"] if r["cands"]]
fig, ax = plt.subplots(figsize=(12.5, 5.0)); x = np.arange(len(rows)); wd = 0.3
nps_net = [r["rule_nps_net"] for r in rows]; best_net = [r["rule_best_net"] for r in rows]
ax.bar(x - wd / 2, nps_net, wd, color=MUTED, label="안 A — 국민연금 규칙(밴드 ±3 · 월 25bp 한도 · 오버레이)을 그대로")
ax.bar(x + wd / 2, best_net, wd, color=GREEN, label="안 B — 자기 지표로 도출한 규칙")
for i, r in enumerate(rows):
    ax.text(x[i] - wd / 2, nps_net[i] + 1, f"{nps_net[i]:+.0f}", ha="center", fontsize=12.5, color=BODY); ax.text(x[i] + wd / 2, best_net[i] + 1, f"{best_net[i]:+.0f}", ha="center", fontsize=12.5, color=BODY, fontweight="bold")
    note = {"NPS": "같은 규칙\n(제1호 결과)", "KIC": f"격차 {best_net[i]-nps_net[i]:.0f}bp ≈ 연 {(best_net[i]-nps_net[i])/1e4*r['aum_trn_krw']*1e4:,.0f}억\n시장충격 없는 곳에 한도 · 밴드", "UNIV": f"한도 12억/월 · 오버레이 없음\n→ CVaR 초과일 {[c for c in r['cands'] if c['rule']=='nps_rule'][0]['pct_days_over_cvar']}%"}[r["code"]]
    ax.text(x[i], -7, note, ha="center", va="top", fontsize=11.5, color=RED if r["code"] != "NPS" else MUTED)
ax.set_xticks(x); ax.set_xticklabels([{"NPS": "국민연금 1,866조", "KIC": "KIC 333조", "UNIV": "H대 발전기금 5,000억"}[r["code"]] for r in rows]); ax.set_ylim(-20, 68); ax.axhline(0, color=HAIR, lw=1)
ax.set_ylabel("순 프리미엄 bp / 년"); ax.legend(loc="upper right", frameon=False, fontsize=12); ax.grid(axis="y", color=HAIR, lw=0.8)
ax.set_title("같은 규칙은 KIC에서 DR을 버리고 H대에서 위험을 못 지킨다 — 국부펀드에는 적용 자체가 안 된다", loc="left", color=NAVY, fontsize=14)
save(fig, "fig_inst_rules")

# 비율 사전 — 덱 빌드에서 그림 크기 계산용 -------------------------------------------------
ratios = {}
for fn in sorted(os.listdir(IMG)):
    if fn.endswith(".png"):
        w, h = Image.open(f"{IMG}/{fn}").size; ratios[fn[:-4]] = round(w / h, 4)
json.dump(ratios, open(f"{IMG}/img_ratios.json", "w"), indent=1)
print("charts done · ratios:", len(ratios))
