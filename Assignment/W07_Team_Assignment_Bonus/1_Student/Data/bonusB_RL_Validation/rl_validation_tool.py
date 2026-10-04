#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""강화학습 리밸런싱 엔진 검증 도구 — W07 보너스 과제 B

정답이 알려진 합성시장(기하 브라운 운동)에서 벤더의 "RL 엔진"을 기준선과 같은 조건으로 시험한다.

사용법
  python3 rl_validation_tool.py              # 전체 검증 (수십 초)
  python3 rl_validation_tool.py --cost 10    # 편도 거래비용을 10bp로 바꿔 본다 (기본 25bp)
  python3 rl_validation_tool.py --gamma 5    # 위험회피 계수를 바꿔 본다 (기본 3)

출력
  [1] 합성시장과 Merton 비중 · 비용이 없을 때의 확실성등가(이론값)
  [2] 기준선 사다리 — 매수 후 보유 · 매일 Merton 비중 복원 · 무거래 구간(반폭 1~8%p)
  [3] 벤더 엔진의 학습 — 한 개의 10년 경로에서 설정 144개를 시도해 샤프 비율이 가장 높은 설정을 고른다
  [4] 다중 시도 보정 — Deflated Sharpe Ratio
  [5] 새 경로 검증 — 학습에 쓰지 않은 4,000개 경로에서 기준선과 비교
  [6] 시드 분포 — 학습 경로를 20개로 바꿔 다시 학습했을 때 고른 설정과 새 경로 성과
  [7] 분포 밖(OOD) 충격 — 첫해에 변동성이 두 배가 되고 주가가 40% 빠지는 시장
  [8] 정직한 강화학습 — Q-learning 에이전트가 시뮬레이터 경험만으로 리밸런싱 규칙을 배운다
  [9] 판정표 — 기준은 교육용 가정이다. 옵션으로 바꿔 결론이 바뀌는지 확인하라.
      --loss-max 2 (① 비용 손실 bp)  --oos-min -1 (② 새 경로 차이 bp)  --repro-min 80 (③ 재현 %)
      --ood-tol 0.05 (④ 충격 시 하위 5% 차이)  --dsr-min 0.95 (⑤ DSR)  --skip-q (8번 생략)
"""
import argparse
import numpy as np
from math import erf, sqrt, log, e

ap = argparse.ArgumentParser()
ap.add_argument("--cost", type=float, default=25.0); ap.add_argument("--gamma", type=float, default=3.0)
ap.add_argument("--loss-max", type=float, default=2.0); ap.add_argument("--oos-min", type=float, default=-1.0)
ap.add_argument("--repro-min", type=float, default=80.0); ap.add_argument("--ood-tol", type=float, default=0.05)
ap.add_argument("--dsr-min", type=float, default=0.95); ap.add_argument("--skip-q", action="store_true")
a = ap.parse_args()
MU, SIG, RF, G, C = 0.07, 0.18, 0.02, a.gamma, a.cost / 1e4
YEARS, DAYS = 10, 252; N = YEARS * DAYS; DT = 1 / DAYS
WST = (MU - RF) / (G * SIG ** 2)
rf_d = np.exp(RF * DT) - 1

def paths(n, seed, ood=False):
    z = np.random.default_rng(seed).standard_normal((n, N))
    s = np.full(N, SIG); m = np.full(N, MU)
    if ood:
        s[:DAYS] = 2 * SIG; m[:DAYS] = log(0.6) + 0.5 * (2 * SIG) ** 2   # 첫해 기대 로그수익 ln 0.6 ≈ −40%
    return np.exp((m - 0.5 * s ** 2) * DT + s * np.sqrt(DT) * z) - 1

def simulate(R, band, tilt=None, look=None, daily=False, bh=False, cost=None):
    """R: (P, N) 수익률. 목표 = Merton 비중 (+ 모멘텀 기울기). band · tilt · look 은 숫자 또는 경로별 배열.
    반환: 최종 부, 일간 초과수익, 연 회전율(%)"""
    cost = C if cost is None else cost
    P = R.shape[0]; W = np.ones(P); w = np.full(P, WST); turn = np.zeros(P); dret = np.zeros((P, N))
    band = np.broadcast_to(np.asarray(band, float), (P,))
    if tilt is not None:
        tilt = np.broadcast_to(np.asarray(tilt, float), (P,)); look = np.broadcast_to(np.asarray(look, int), (P,))
        logp = np.concatenate([np.zeros((P, 1)), np.cumsum(np.log1p(R), axis=1)], axis=1); rows = np.arange(P)
    for t in range(N):
        Wb = W
        Wr = W * w * (1 + R[:, t]); Ws = W * (1 - w) * (1 + rf_d); W = Wr + Ws; w = Wr / W
        if bh:
            dret[:, t] = W / Wb - 1 - rf_d; continue
        tgt = np.full(P, WST)
        if tilt is not None:
            back = t + 1 - look; ok = back >= 0
            mom = np.where(ok, logp[rows, t + 1] - logp[rows, np.maximum(back, 0)], 0.0)
            tgt = np.clip(WST + tilt * np.sign(mom), 0, 1)
        new = tgt if daily else np.clip(w, tgt - band, tgt + band)
        tr = np.abs(new - w); W = W * (1 - cost * tr); turn += tr; w = new
        dret[:, t] = W / Wb - 1 - rf_d
    return W, dret, turn / YEARS * 100

def ce_bp(W):
    return ((np.mean(W ** (1 - G))) ** (1 / ((1 - G) * YEARS)) - 1) * 1e4
def sharpe(d):
    return d.mean(axis=-1) / d.std(axis=-1) * sqrt(DAYS)
Phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
def Phi_inv(p):
    lo, hi = -10.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Phi(mid) < p else (lo, mid)
    return (lo + hi) / 2

print(f"=== 강화학습 리밸런싱 엔진 검증 — 합성시장: 주식 기대수익 {MU:.0%} · 변동성 {SIG:.0%} · 무위험 {RF:.0%} · 위험회피 γ = {G:g} · 편도 거래비용 {C*1e4:.0f}bp ===")
print(f"[1] Merton 비중 w* = (μ − r) ÷ (γσ²) = {MU-RF:.2f} ÷ ({G:g} × {SIG**2:.4f}) = {WST:.1%} · 비용이 없을 때 확실성등가(이론) = r + (μ − r)² ÷ (2γσ²) = {(RF+(MU-RF)**2/(2*G*SIG**2))*1e4:.1f}bp")

R = paths(4000, 11)
Wf, _, _ = simulate(R, 0, daily=True, cost=0.0); CE0 = ce_bp(Wf)
print(f"[2] 기준선 사다리 — 10년 × 4,000개 경로 (같은 경로에서 비용 없는 Merton의 확실성등가 {CE0:.1f}bp를 기준으로 손실을 잰다)")
W, _, tu = simulate(R, 0, bh=True); print(f"    0 매수 후 보유 (리밸런싱 없음)          확실성등가 {ce_bp(W):6.1f}bp · 손실 {CE0-ce_bp(W):5.1f}bp · 회전율 0%")
W, _, tu = simulate(R, 0, daily=True); print(f"    1 매일 Merton 비중으로 복원             확실성등가 {ce_bp(W):6.1f}bp · 손실 {CE0-ce_bp(W):5.1f}bp · 회전율 {tu.mean():4.1f}%/년")
best = None
for h in [0.01, 0.02, 0.03, 0.04, 0.05, 0.08]:
    W, _, tu = simulate(R, h); ce = ce_bp(W)
    print(f"    2 무거래 구간 반폭 ±{h*100:.0f}%p                확실성등가 {ce:6.1f}bp · 손실 {CE0-ce:5.1f}bp · 회전율 {tu.mean():4.1f}%/년")
    if best is None or ce > best[1]: best = (h, ce)
print(f"    → 최적 반폭(이 경로 집합) ±{best[0]*100:.0f}%p · 점근 공식 반폭 ≈ (3/(2γ) × w*²(1−w*)² × c)^(1/3) = {((3/(2*G))*WST**2*(1-WST)**2*C)**(1/3)*100:.1f}%p")

TILTS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]; LOOKS = [20, 60, 120, 250]; BANDS = [0.005, 0.01, 0.02, 0.03, 0.05, 0.08]
GRID = [(k, L, h) for k in TILTS for L in LOOKS for h in BANDS]
GK = np.array([g[0] for g in GRID]); GL = np.array([g[1] for g in GRID]); GH = np.array([g[2] for g in GRID])
def train(seed):
    path = paths(1, seed)[0]
    _, d, _ = simulate(np.repeat(path[None, :], len(GRID), axis=0), GH, tilt=GK, look=GL)
    sr = sharpe(d); i = int(sr.argmax())
    return GRID[i], sr, path
TRAIN_SEED = 5008
(k0, L0, h0), SR, path0 = train(TRAIN_SEED)
_, d_band, _ = simulate(path0[None, :], 0.03)
print(f"[3] 벤더 엔진의 학습 — 학습 경로 1개(10년, 시드 {TRAIN_SEED})에서 설정 {len(GRID)}개 시도 (기울기 k × 신호 기간 L × 구간 반폭 h)")
print(f"    선택된 설정: 모멘텀 기울기 k = {k0:.1f} · 신호 기간 {L0}일 · 구간 반폭 ±{h0*100:.1f}%p → 학습 경로 샤프 {SR.max():.2f} (같은 경로에서 무거래 구간 ±3%p 샤프 {sharpe(d_band)[0]:.2f})")
print(f"    144개 시도 샤프의 분포: 평균 {SR.mean():.2f} · 표준편차 {SR.std():.2f} · 최댓값 {SR.max():.2f}")
# [4] DSR
_, d_sel, _ = simulate(path0[None, :], h0, tilt=k0, look=L0); x = d_sel[0]
srd = x.mean() / x.std(); sk = ((x - x.mean()) ** 3).mean() / x.std() ** 3; ku = ((x - x.mean()) ** 4).mean() / x.std() ** 4
var_sr = (SR / sqrt(DAYS)).var(); ge = 0.5772
sr0 = sqrt(var_sr) * ((1 - ge) * Phi_inv(1 - 1 / len(GRID)) + ge * Phi_inv(1 - 1 / (len(GRID) * e)))
dsr = Phi((srd - sr0) * sqrt(N - 1) / sqrt(1 - sk * srd + (ku - 1) / 4 * srd ** 2))
print(f"[4] 다중 시도 보정 — 시도 {len(GRID)}개에서 운으로 기대되는 최대 샤프(연율) {sr0*sqrt(DAYS):.2f} · Deflated Sharpe Ratio = {dsr:.2f} (0.95 이상이어야 유의)")
# [5] 새 경로
R2 = paths(4000, 777)
Wf2, _, _ = simulate(R2, 0, daily=True, cost=0.0); base2 = ce_bp(Wf2)
Wb, _, tub = simulate(R2, 0.03); Wv, _, tuv = simulate(R2, h0, tilt=k0, look=L0); Wd, _, tud = simulate(R2, 0, daily=True)
print(f"[5] 새 경로 검증 — 학습에 쓰지 않은 4,000개 경로 (비용 없는 Merton {base2:.1f}bp 기준)")
print(f"    매일 복원           확실성등가 {ce_bp(Wd):6.1f}bp · 손실 {base2-ce_bp(Wd):5.1f}bp · 회전율 {tud.mean():5.1f}%/년")
print(f"    무거래 구간 ±3%p    확실성등가 {ce_bp(Wb):6.1f}bp · 손실 {base2-ce_bp(Wb):5.1f}bp · 회전율 {tub.mean():5.1f}%/년")
print(f"    벤더 엔진           확실성등가 {ce_bp(Wv):6.1f}bp · 손실 {base2-ce_bp(Wv):5.1f}bp · 회전율 {tuv.mean():5.1f}%/년")
# [6] 시드 분포
print("[6] 시드 분포 — 학습 경로만 바꿔 20번 다시 학습 (새 경로 1,000개로 평가)")
R3 = R2[:1000]; Wb3, _, _ = simulate(R3, 0.03); ceb3 = ce_bp(Wb3); rows = []
for s in range(20):
    (k, L, h), sr, _ = train(5000 + s)
    Wv3, _, _ = simulate(R3, h, tilt=k, look=L); rows.append((k, L, h, sr.max(), ce_bp(Wv3) - ceb3))
for (k, L, h, s_in, dce) in rows:
    print(f"    k {k:.1f} · L {L:>3}일 · 반폭 ±{h*100:.1f}%p · 학습 샤프 {s_in:.2f} → 새 경로에서 무거래 구간 대비 {dce:+6.1f}bp")
wins = sum(1 for r in rows if r[4] > 0)
print(f"    → 20번 중 무거래 구간을 이긴 횟수 {wins}회 · 고른 기울기 k 분포 {sorted(set(r[0] for r in rows))} · 고른 신호 기간 {sorted(set(r[1] for r in rows))}")
# [7] OOD
R4 = paths(2000, 999, ood=True); Q5 = {}
for name, kw in [("무거래 구간 ±3%p", dict(band=0.03)), ("벤더 엔진", dict(band=h0, tilt=k0, look=L0)), ("매일 복원", dict(band=0, daily=True))]:
    W, _, tu = simulate(R4, **kw); Q5[name] = np.quantile(W, 0.05)
    print(f"[7] 분포 밖 충격(첫해 변동성 2배 · 약 −40%) — {name:<12} 10년 뒤 부 중앙값 {np.median(W):.2f} · 하위 5% {np.quantile(W, 0.05):.2f} · 회전율 {tu.mean():.1f}%/년")

# [8] 정직한 강화학습 — 표 형태 Q-learning
#   상태 = 목표 비중과의 괴리 d (0.5%p 간격 · −8~+8%p) · 행동 = 매매 후 괴리 d' · 주 단위
#   보상 = −(위험 비용 γ/2 · σ² · d'² · Δt) − (거래비용 c · |d' − d|)   ← 확실성등가 손실을 그대로 보상으로 쓴다
#   다음 상태 = d' + w*(1−w*) σ √Δt · ε  (주가가 움직이면 비중이 흘러간다)
def q_learn(samples, seed, step=0.005, lim=0.12, beta=0.995, K=20):
    rng = np.random.default_rng(seed); grid = np.round(np.arange(-lim, lim + 1e-9, step), 4); S = len(grid)
    dt = 5 / DAYS; sd = WST * (1 - WST) * SIG * sqrt(dt)
    risk = 0.5 * G * SIG ** 2 * grid ** 2 * dt; cost = C * np.abs(grid[None, :] - grid[:, None])
    rew = -(risk[None, :] + cost) * 1e4                                   # bp 단위 · (상태, 행동)
    Q = np.zeros((S, S)); sweeps = max(1, samples // (S * K))
    for it in range(sweeps):
        nxt = grid[:, None] + sd * rng.standard_normal((S, K))           # 행동(매매 후 괴리)마다 경험한 다음 상태 K개
        j = np.clip(np.rint((nxt + lim) / step).astype(int), 0, S - 1)
        alpha = 1 / (1 + it / 20) ** 0.6                                  # 학습률: 점점 줄인다
        Q = (1 - alpha) * Q + alpha * (rew + beta * Q.max(1)[j].mean(1)[None, :])
    stay = Q.argmax(1) == np.arange(S); lo = hi = S // 2                  # 0을 포함하는 '그대로 두기' 구간
    while lo > 0 and stay[lo - 1]: lo -= 1
    while hi < S - 1 and stay[hi + 1]: hi += 1
    return (grid[lo], grid[hi]), sweeps * S * K

if not a.skip_q:
    hth = ((3 / (2 * G)) * WST ** 2 * (1 - WST) ** 2 * C) ** (1 / 3)
    print(f"[8] 정직한 강화학습 — Q-learning이 배운 '아무것도 하지 않는 구간' (이론 반폭 ±{hth*100:.1f}%p)")
    for budget in (2_000, 20_000, 200_000, 2_000_000):
        outs = [q_learn(budget, s) for s in range(3)]
        txt = " · ".join(f"[{lo*100:+.1f}, {hi*100:+.1f}]%p" for (lo, hi), _ in outs)
        print(f"    경험 {budget:>9,}회(주 단위 전이 · 시드 3개): 배운 구간 {txt}")
    print(f"    참고: 실제 역사 10년은 주 단위 전이 약 {YEARS*52}회다.")
    (lo, hi), _ = q_learn(2_000_000, 0); hq = (hi - lo) / 2
    Wq, _, tuq = simulate(R2, hq)
    print(f"    배운 구간(반폭 ±{hq*100:.1f}%p)을 새 경로 4,000개에 적용: 확실성등가 {ce_bp(Wq):6.1f}bp (무거래 구간 ±3%p {ce_bp(Wb):6.1f}bp) · 회전율 {tuq.mean():.1f}%/년")

# [9] 판정표
lossA, lossB, lossC = base2 - ce_bp(Wd), base2 - ce_bp(Wb), base2 - ce_bp(Wv)
mk = lambda b: "통과" if b else "탈락"
print(f"[9] 판정표 — 기준(교육용 가정): ① 비용 손실 ≤ {a.loss_max:g}bp · ② 무거래 구간 대비 ≥ {a.oos_min:g}bp · ③ 재현 ≥ {a.repro_min:g}% · ④ 충격 하위 5% 차이 ≥ −{a.ood_tol:g} · ⑤ DSR ≥ {a.dsr_min:g}")
print(f"    A 매일 복원        ① {mk(lossA <= a.loss_max)}({lossA:.1f}bp) · ② {mk(ce_bp(Wd)-ce_bp(Wb) >= a.oos_min)}({ce_bp(Wd)-ce_bp(Wb):+.1f}bp) · ③ 해당 없음 · ④ {mk(Q5['매일 복원']-Q5['무거래 구간 ±3%p'] >= -a.ood_tol)} · ⑤ 해당 없음")
print(f"    B 무거래 구간 ±3%p ① {mk(lossB <= a.loss_max)}({lossB:.1f}bp) · ② 기준 · ③ 해당 없음 · ④ 기준 · ⑤ 해당 없음")
print(f"    C 벤더 엔진        ① {mk(lossC <= a.loss_max)}({lossC:.1f}bp) · ② {mk(ce_bp(Wv)-ce_bp(Wb) >= a.oos_min)}({ce_bp(Wv)-ce_bp(Wb):+.1f}bp) · ③ {mk(wins/20*100 >= a.repro_min)}({wins}/20)"
      f" · ④ {mk(Q5['벤더 엔진']-Q5['무거래 구간 ±3%p'] >= -a.ood_tol)}({Q5['벤더 엔진']-Q5['무거래 구간 ±3%p']:+.3f}) · ⑤ {mk(dsr >= a.dsr_min)}({dsr:.2f})")
