"""한국형 자산배분·자산배치(Asset Allocation & Location) 모델.

Huang(2008)의 아이디어를 한국 계좌(일반·ISA·연금저축·IRP)와 2026년 세법으로 옮긴 결정론적 모델이다.

두 가지 문제를 푼다.
  1) 배치(location) 문제 — 목표 배분이 주어졌을 때 세후 최종가치를 최대화하는 선형계획(LP).
     계좌 잔액 제약의 쌍대가격(dual)으로 계좌별 한계가치 λ와 Z = λ_계좌 / λ_일반 을 얻는다.
  2) 배분·배치 공동(joint) 문제 — 세후 위험 노출에 평균-분산 벌점을 둔 2차계획(QP).
     위험회피 계수를 바꾸며 배분과 배치가 함께 어떻게 움직이는지 본다.

금액 단위는 만 원. 수익률은 연 기대값이며 기대 경로를 따라 세금을 계산한다(결정론적).
"""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import linprog
import tax_rules_2026 as TR


# ---------------------------------------------------------------- 입력 정의
@dataclass
class Asset:
    name: str            # tax_rules_2026.TAX_TYPE 의 키
    price_growth: float  # 연 가격 상승률
    distribution: float  # 연 분배(배당·이자) 수익률
    vol: float           # 연 변동성 (공동 최적화용)

    @property
    def total(self) -> float:
        return self.price_growth + self.distribution


@dataclass
class Account:
    name: str                 # "일반" | "ISA" | "연금저축" | "IRP"
    balance: float            # 만 원
    pension_tax: float = 0.055       # 연금계좌의 평가상 인출세율
    nondeductible_share: float = 0.0  # 연금계좌 중 세액공제받지 않은 원금 비중(인출 시 비과세)

    @property
    def kind(self) -> str:
        return "pension" if self.name in ("연금저축", "IRP") else ("isa" if self.name == "ISA" else "taxable")


@dataclass
class Problem:
    assets: list[Asset]
    accounts: list[Account]
    horizon: int = 10
    isa_type: str = "일반형"
    corr: np.ndarray | None = None   # 자산 간 상관행렬 (공동 최적화용)

    def allowed(self, acc: Account, a: Asset) -> bool:
        return a.name not in TR.NOT_ALLOWED.get(acc.name, set())


# ---------------------------------------------------------------- 1원당 계수
def unit_coefficients(acc: Account, a: Asset, T: int) -> dict:
    """계좌 acc에 자산 a를 1원 넣었을 때 T년 뒤의 계수.

    net   : 포트폴리오 단위 비선형 세금(해외 양도세 공제, ISA 한도)을 빼기 전 세후 가치
    g_for : 해외상장 양도차익 (22% · 250만 공제 대상)
    g_isa : ISA 순이익 (9.9% · 비과세 한도 대상)
    share : 세후 소유 지분 — 위험 노출 계산에 쓴다 (연금은 1 - 인출세율)
    """
    out = dict(net=0.0, g_for=0.0, g_isa=0.0, share=1.0)
    if acc.kind == "taxable":
        typ = TR.TAX_TYPE[a.name]
        V, basis = 1.0, 1.0
        for _ in range(T):
            dist = V * a.distribution
            V *= (1 + a.price_growth)
            after = dist * (1 - TR.DIVIDEND_TAX)      # 분배금은 매년 15.4% 원천징수 후 재투자
            V += after
            basis += after
        gain = V - basis
        if typ == "kr_equity":                       # 매매차익 비과세
            out["net"] = V
        elif typ in ("kr_listed", "interest"):       # 매도 시 차익 15.4%
            out["net"] = V - TR.DIVIDEND_TAX * gain
        elif typ == "foreign":                       # 22%는 포트폴리오 단위로 따로 계산
            out["net"], out["g_for"] = V, gain
    elif acc.kind == "isa":
        V = (1 + a.total) ** T
        out["net"], out["g_isa"] = V, V - 1.0
    else:  # pension
        V = (1 + a.total) ** T
        tau, nd = acc.pension_tax, acc.nondeductible_share
        out["net"] = V * (1 - tau) + tau * nd        # 공제받지 않은 원금은 인출 시 비과세
        out["share"] = 1 - tau
    return out


# ---------------------------------------------------------------- 공통 구조
class _Index:
    def __init__(self, P: Problem):
        self.P = P
        self.pairs = [(ai, ki) for ai, acc in enumerate(P.accounts) for ki, a in enumerate(P.assets) if P.allowed(acc, a)]
        self.n = len(self.pairs)
        self.coef = [unit_coefficients(P.accounts[ai], P.assets[ki], P.horizon) for ai, ki in self.pairs]
        self.net = np.array([c["net"] for c in self.coef])
        self.gfor = np.array([c["g_for"] for c in self.coef])
        self.gisa = np.array([c["g_isa"] for c in self.coef])
        self.share = np.array([c["share"] for c in self.coef])

    def table(self, x: np.ndarray) -> dict:
        P = self.P
        tab = {acc.name: {a.name: 0.0 for a in P.assets} for acc in P.accounts}
        for (ai, ki), v in zip(self.pairs, x):
            tab[P.accounts[ai].name][P.assets[ki].name] = float(v)
        return tab

    def exposure(self, x: np.ndarray) -> np.ndarray:
        e = np.zeros(len(self.P.assets))
        for (ai, ki), s, v in zip(self.pairs, self.share, x):
            e[ki] += s * v
        return e

    def value(self, x: np.ndarray) -> dict:
        """주어진 배치 x의 세후 최종가치 (비선형 세금 포함)."""
        allow = TR.ISA_ALLOWANCE[self.P.isa_type]
        tax_for = TR.FOREIGN_CGT * max(0.0, float(self.gfor @ x) - TR.FOREIGN_CGT_DEDUCTION)
        tax_isa = TR.ISA_TAX * max(0.0, float(self.gisa @ x) - allow)
        return dict(value=float(self.net @ x) - tax_for - tax_isa, tax_foreign=tax_for, tax_isa=tax_isa)


# ---------------------------------------------------------------- 1) 배치 LP
def solve_location(P: Problem, target: dict, mode: str = "pretax") -> dict:
    """목표 배분 아래 세후 최종가치를 최대화하는 배치.

    mode="pretax"  : target = {자산: 표시 잔액(만 원)}  — 김 교수 사례 방식
    mode="aftertax": target = {자산: 세후 비중}         — Huang 방식, 계좌별 Z 도출 가능
    """
    I = _Index(P)
    n, nA = I.n, len(P.assets)
    nv = n + 2                                   # x..., 해외 양도세, ISA 세금
    c = np.zeros(nv); c[:n] = -I.net; c[n] = 1.0; c[n + 1] = 1.0

    A_eq, b_eq, A_ub, b_ub = [], [], [], []
    bal_rows = {}
    for ai, acc in enumerate(P.accounts):         # 계좌 잔액
        row = np.zeros(nv)
        for k, (aj, _) in enumerate(I.pairs):
            if aj == ai: row[k] = 1.0
        bal_rows[acc.name] = len(A_eq); A_eq.append(row); b_eq.append(acc.balance)

    names = [a.name for a in P.assets]
    if mode == "pretax":
        for key, amt in target.items():           # 키가 튜플이면 여러 상품의 합계를 맞춘다 (예: 해외주식 국내상장+해외상장)
            group = set(key) if isinstance(key, tuple) else {key}
            row = np.zeros(nv)
            for k, (_, kj) in enumerate(I.pairs):
                if names[kj] in group: row[k] = 1.0
            A_eq.append(row); b_eq.append(amt)
    else:
        w = np.array([target[nm] for nm in names]); w = w / w.sum()
        for ki in range(nA - 1):                  # 마지막 식은 나머지로부터 자동 성립
            row = np.zeros(nv)
            for k, (_, kj) in enumerate(I.pairs):
                row[k] = I.share[k] * ((1.0 if kj == ki else 0.0) - w[ki])
            A_eq.append(row); b_eq.append(0.0)

    for ai, acc in enumerate(P.accounts):         # IRP 위험자산 70%
        if acc.name == "IRP":
            row = np.zeros(nv)
            for k, (aj, kj) in enumerate(I.pairs):
                if aj == ai and P.assets[kj].name in TR.RISKY: row[k] = 1.0
            A_ub.append(row); b_ub.append(TR.IRP_RISKY_LIMIT * acc.balance)

    row = np.zeros(nv); row[:n] = TR.FOREIGN_CGT * I.gfor; row[n] = -1.0      # 해외 양도세 ≥ 22%(차익-250)
    A_ub.append(row); b_ub.append(TR.FOREIGN_CGT * TR.FOREIGN_CGT_DEDUCTION)
    row = np.zeros(nv); row[:n] = TR.ISA_TAX * I.gisa; row[n + 1] = -1.0      # ISA 세금 ≥ 9.9%(이익-한도)
    A_ub.append(row); b_ub.append(TR.ISA_TAX * TR.ISA_ALLOWANCE[P.isa_type])

    res = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq,
                  bounds=[(0, None)] * nv, method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    x = res.x[:n]
    out = dict(x=x, table=I.table(x), exposure=I.exposure(x), **I.value(x))
    lam = {nm: -res.eqlin.marginals[r] for nm, r in bal_rows.items()}   # 1원 추가 시 세후가치 증가
    out["lambda"] = lam
    if mode == "aftertax" and "일반" in lam and lam["일반"] > 0:
        out["Z"] = {nm: v / lam["일반"] for nm, v in lam.items()}
    out["_index"] = I
    return out


# ---------------------------------------------------------------- 2) 공동 QP
def solve_joint(P: Problem, gamma: float, ref_return: float = 0.05) -> dict:
    """배분과 배치를 함께 고른다.

    목적: 세후 기대 최종가치 - (γ/2)·G·T·(e'Σe)/W  (e = 세후 위험 노출, G = (1+기준수익률)^T, W = 세후 재산)
    확실성 등가 CE ≈ E[W_T] - (γ/2)·Var(W_T)/E[W_T] 를 선형화한 근사다.
    """
    import cvxpy as cp
    I = _Index(P)
    nA = len(P.assets)
    vol = np.array([a.vol for a in P.assets])
    C = P.corr if P.corr is not None else np.eye(nA)
    Sigma = np.outer(vol, vol) * C
    Sigma = (Sigma + Sigma.T) / 2 + 1e-10 * np.eye(nA)

    x = cp.Variable(I.n, nonneg=True); tf = cp.Variable(nonneg=True); ti = cp.Variable(nonneg=True)
    M = np.zeros((nA, I.n))                       # 노출 행렬: e = M x
    for k, (_, kj) in enumerate(I.pairs):
        M[kj, k] = I.share[k]
    e = M @ x
    W_at = sum(acc.balance * (1 - acc.pension_tax if acc.kind == "pension" else 1) for acc in P.accounts)
    G = (1 + ref_return) ** P.horizon
    pen = 0.5 * gamma * G * P.horizon / W_at

    cons = [tf >= TR.FOREIGN_CGT * (I.gfor @ x - TR.FOREIGN_CGT_DEDUCTION),
            ti >= TR.ISA_TAX * (I.gisa @ x - TR.ISA_ALLOWANCE[P.isa_type])]
    for ai, acc in enumerate(P.accounts):
        idx = [k for k, (aj, _) in enumerate(I.pairs) if aj == ai]
        cons.append(cp.sum(x[idx]) == acc.balance)
        if acc.name == "IRP":
            risky = [k for k in idx if P.assets[I.pairs[k][1]].name in TR.RISKY]
            cons.append(cp.sum(x[risky]) <= TR.IRP_RISKY_LIMIT * acc.balance)
    obj = cp.Maximize(I.net @ x - tf - ti - pen * cp.quad_form(e, Sigma))
    cp.Problem(obj, cons).solve(solver="CLARABEL")
    xv = np.maximum(np.asarray(x.value).ravel(), 0)
    ev = I.exposure(xv)
    val = I.value(xv)
    return dict(x=xv, table=I.table(xv), exposure=ev, weights=ev / ev.sum(),
                risk_penalty=float(pen * ev @ Sigma @ ev), ce=val["value"] - float(pen * ev @ Sigma @ ev), **val)


# ---------------------------------------------------------------- 기준 전략
def fill_order(P: Problem, target: dict, order: list[str]) -> np.ndarray:
    """절세계좌(IRP → 연금저축 → ISA)를 자산 순서대로 채우고 나머지는 일반계좌에 둔다 (표시 잔액 목표)."""
    I = _Index(P)
    left = dict(target)
    tab = {acc.name: {a.name: 0.0 for a in P.assets} for acc in P.accounts}
    for accname in ["IRP", "연금저축", "ISA"]:
        acc = next((a for a in P.accounts if a.name == accname), None)
        if acc is None: continue
        room, risky_room = acc.balance, (TR.IRP_RISKY_LIMIT * acc.balance if accname == "IRP" else np.inf)
        for nm in order:
            if not P.allowed(acc, next(a for a in P.assets if a.name == nm)): continue
            cap = min(room, left[nm], risky_room if nm in TR.RISKY else np.inf)
            tab[accname][nm] += cap; left[nm] -= cap; room -= cap
            if nm in TR.RISKY: risky_room -= cap
        if room > 1e-9:                                  # 남은 자리는 남은 자산으로
            for nm in left:
                cap = min(room, left[nm], risky_room if nm in TR.RISKY else np.inf)
                tab[accname][nm] += cap; left[nm] -= cap; room -= cap
                if nm in TR.RISKY: risky_room -= cap
    for nm in left:
        tab["일반"][nm] += left[nm]
    return np.array([tab[P.accounts[ai].name][P.assets[ki].name] for ai, ki in I.pairs])


def proportional(P: Problem, target: dict) -> np.ndarray:
    """모든 계좌에 같은 비중으로 담는다 (담을 수 없는 상품은 일반계좌로)."""
    I = _Index(P)
    tot = sum(target.values())
    tab = {acc.name: {a.name: 0.0 for a in P.assets} for acc in P.accounts}
    for acc in P.accounts:
        for a in P.assets:
            tab[acc.name][a.name] = acc.balance * target[a.name] / tot
    for acc in P.accounts:                               # 담을 수 없는 상품은 일반계좌의 다른 자산과 맞바꿈
        for a in P.assets:
            if not P.allowed(acc, a) and tab[acc.name][a.name] > 0:
                amt = tab[acc.name][a.name]; tab[acc.name][a.name] = 0
                tab["일반"][a.name] += amt
                alt = next(b for b in P.assets if P.allowed(acc, b))
                tab[acc.name][alt.name] += amt; tab["일반"][alt.name] -= amt
    return np.array([tab[P.accounts[ai].name][P.assets[ki].name] for ai, ki in I.pairs])


def evaluate(P: Problem, x: np.ndarray) -> dict:
    I = _Index(P)
    return dict(table=I.table(x), exposure=I.exposure(x), **I.value(x))
