// 한국형 자산배치 엔진 (alm_model/model.py의 배치 LP를 JS로 옮김). 금액 단위: 만 원
const TAX = {
  DIV: 0.154, FCGT: 0.22, FDED: 250, ISA_TAX: 0.099,
  ISA_ALLOW: { "일반형": 200, "서민형": 400 }, IRP_RISKY: 0.70,
};
const GROUPS = ["국내주식", "해외주식", "채권"];

// ---------- 단체법 (2단계, Bland 규칙)
function lpSolve(c, rows) {            // max c·x, rows: {a, b, t:'<='|'>='|'='}, x ≥ 0
  const n = c.length, R = rows.map(r => r.b < 0 ? { a: r.a.map(v => -v), b: -r.b, t: r.t === "<=" ? ">=" : r.t === ">=" ? "<=" : "=" } : r);
  const m = R.length; let ns = 0, na = 0;
  R.forEach(r => { if (r.t !== "=") ns++; if (r.t !== "<=") na++; });
  const N = n + ns + na, T = [], basis = [], art = new Array(N).fill(false);
  let si = n, ai = n + ns;
  R.forEach((r, i) => {
    const row = new Array(N + 1).fill(0); r.a.forEach((v, j) => row[j] = v); row[N] = r.b;
    if (r.t === "<=") { row[si] = 1; basis.push(si++); }
    else { if (r.t === ">=") row[si++] = -1; row[ai] = 1; art[ai] = true; basis.push(ai++); }
    T.push(row);
  });
  const run = (obj, allowed) => {
    T[m] = obj;
    for (let it = 0; it < 5000; it++) {
      let e = -1; for (let j = 0; j < N; j++) if (allowed[j] && T[m][j] < -1e-9) { e = j; break; }
      if (e < 0) return true;
      let r = -1, best = Infinity;
      for (let i = 0; i < m; i++) if (T[i][e] > 1e-9) {
        const q = T[i][N] / T[i][e];
        if (q < best - 1e-12 || (Math.abs(q - best) <= 1e-12 && basis[i] < basis[r])) { best = q; r = i; }
      }
      if (r < 0) throw new Error("unbounded");
      pivot(r, e);
    }
    throw new Error("iteration limit");
  };
  const pivot = (r, e) => {
    const p = T[r][e]; for (let j = 0; j <= N; j++) T[r][j] /= p;
    for (let i = 0; i <= m; i++) if (i !== r && Math.abs(T[i][e]) > 0) { const f = T[i][e]; if (f) for (let j = 0; j <= N; j++) T[i][j] -= f * T[r][j]; }
    basis[r] = e;
  };
  // 1단계
  if (na) {
    const o = new Array(N + 1).fill(0); for (let j = 0; j < N; j++) if (art[j]) o[j] = 1;
    for (let i = 0; i < m; i++) if (art[basis[i]]) for (let j = 0; j <= N; j++) o[j] -= T[i][j];
    run(o, new Array(N).fill(true));
    if (T[m][N] < -1e-6) throw new Error("infeasible");
    for (let i = 0; i < m; i++) if (art[basis[i]]) { const j = T[i].findIndex((v, k) => k < N && !art[k] && Math.abs(v) > 1e-9); if (j >= 0) pivot(i, j); }
  }
  // 2단계
  const o = new Array(N + 1).fill(0); c.forEach((v, j) => o[j] = -v);
  for (let i = 0; i < m; i++) { const f = o[basis[i]]; if (f) for (let j = 0; j <= N; j++) o[j] -= f * T[i][j]; }
  run(o, art.map(a => !a));
  const x = new Array(n).fill(0); basis.forEach((b, i) => { if (b < n) x[b] = T[i][N]; });
  return { x, value: T[m][N] };
}

// ---------- 1원당 계수
function unitCoef(acc, a, T) {
  const out = { net: 0, gfor: 0, gisa: 0, share: 1 };
  if (acc.kind === "taxable") {
    let V = 1, basis = 1;
    for (let t = 0; t < T; t++) { const d = V * a.d; V *= 1 + a.g; const af = d * (1 - TAX.DIV); V += af; basis += af; }
    const gain = V - basis;
    if (a.type === "kr_equity") out.net = V;
    else if (a.type === "kr_listed") out.net = V - TAX.DIV * gain;
    else { out.net = V; out.gfor = gain; }
  } else if (acc.kind === "isa") {
    const V = (1 + a.g + a.d) ** T; out.net = V; out.gisa = V - 1;
  } else {
    const V = (1 + a.g + a.d) ** T; out.net = V * (1 - acc.tau) + acc.tau * (acc.nd || 0); out.share = 1 - acc.tau;
  }
  return out;
}
const allowed = (acc, a) => !(a.type === "foreign" && acc.kind !== "taxable");

function index(P) {
  const pairs = [];
  P.accounts.forEach((acc, i) => P.assets.forEach((a, k) => { if (allowed(acc, a)) pairs.push([i, k]); }));
  const coef = pairs.map(([i, k]) => unitCoef(P.accounts[i], P.assets[k], P.T));
  return { pairs, coef };
}
function valueOf(P, I, x) {
  let net = 0, gf = 0, gi = 0, gross = 0;
  I.pairs.forEach(([i, k], j) => {
    const c = I.coef[j], a = P.assets[k]; net += c.net * x[j]; gf += c.gfor * x[j]; gi += c.gisa * x[j];
    gross += x[j] * (1 + a.g + a.d) ** P.T;
  });
  const tf = TAX.FCGT * Math.max(0, gf - TAX.FDED), ti = TAX.ISA_TAX * Math.max(0, gi - TAX.ISA_ALLOW[P.isaType]);
  const value = net - tf - ti;
  return { value, taxForeign: tf, taxIsa: ti, gross, leak: gross - value };
}
function tableOf(P, I, x) {
  const tab = P.accounts.map(() => P.assets.map(() => 0));
  I.pairs.forEach(([i, k], j) => tab[i][k] = x[j]); return tab;
}

// mode "pretax": target = 그룹별 금액 / "aftertax": target = 그룹별 세후 비중
function solveLocation(P, target, mode = "pretax") {
  const I = index(P), n = I.pairs.length, nv = n + 2, rows = [];
  const c = new Array(nv).fill(0); I.coef.forEach((k, j) => c[j] = k.net); c[n] = -1; c[n + 1] = -1;
  P.accounts.forEach((acc, i) => { const a = new Array(nv).fill(0); I.pairs.forEach(([ii], j) => { if (ii === i) a[j] = 1; }); rows.push({ a, b: acc.bal, t: "=" }); });
  if (mode === "pretax") {
    GROUPS.forEach((g, gi) => { const a = new Array(nv).fill(0); I.pairs.forEach(([, k], j) => { if (P.assets[k].group === gi) a[j] = 1; }); rows.push({ a, b: target[gi], t: "=" }); });
  } else {
    const s = target.reduce((p, v) => p + v, 0), w = target.map(v => v / s);
    for (let gi = 0; gi < GROUPS.length - 1; gi++) {
      const a = new Array(nv).fill(0);
      I.pairs.forEach(([, k], j) => a[j] = I.coef[j].share * ((P.assets[k].group === gi ? 1 : 0) - w[gi]));
      rows.push({ a, b: 0, t: "=" });
    }
  }
  P.accounts.forEach((acc, i) => { if (acc.name === "IRP") { const a = new Array(nv).fill(0); I.pairs.forEach(([ii, k], j) => { if (ii === i && P.assets[k].risky) a[j] = 1; }); rows.push({ a, b: TAX.IRP_RISKY * acc.bal, t: "<=" }); } });
  let a = new Array(nv).fill(0); I.coef.forEach((k, j) => a[j] = TAX.FCGT * k.gfor); a[n] = -1; rows.push({ a, b: TAX.FCGT * TAX.FDED, t: "<=" });
  a = new Array(nv).fill(0); I.coef.forEach((k, j) => a[j] = TAX.ISA_TAX * k.gisa); a[n + 1] = -1; rows.push({ a, b: TAX.ISA_TAX * TAX.ISA_ALLOW[P.isaType], t: "<=" });
  const r = lpSolve(c, rows), x = r.x.slice(0, n).map(v => Math.max(0, v));
  return { x, I, table: tableOf(P, I, x), ...valueOf(P, I, x) };
}

// 계좌별 한계가치 Z: 세후 비중을 유지하며 계좌에 δ를 더했을 때 가치 증가 ÷ 일반계좌의 같은 값
function marginalZ(P, weights, delta = 10) {
  const base = solveLocation(P, weights, "aftertax").value, lam = {};
  P.accounts.forEach((acc, i) => {
    const Q = { ...P, accounts: P.accounts.map((b, j) => j === i ? { ...b, bal: b.bal + delta } : b) };
    lam[acc.name] = (solveLocation(Q, weights, "aftertax").value - base) / delta;
  });
  const Z = {}; Object.keys(lam).forEach(k => Z[k] = lam[k] / lam["일반"]);
  return { lam, Z };
}

// 기준 전략 (그룹 목표를 각 그룹의 기본 상품으로 담는다)
function defaultAsset(P, gi) { return P.assets.findIndex(a => a.group === gi && a.type !== "foreign"); }
function xFromTable(P, I, tab) { return I.pairs.map(([i, k]) => tab[i][k]); }
function proportional(P, target) {
  const I = index(P), tot = target.reduce((p, v) => p + v, 0), tab = P.accounts.map(() => P.assets.map(() => 0));
  P.accounts.forEach((acc, i) => GROUPS.forEach((g, gi) => tab[i][defaultAsset(P, gi)] = acc.bal * target[gi] / tot));
  return xFromTable(P, I, tab);
}
function fillOrder(P, target, orderGroups) {
  const I = index(P), left = [...target], tab = P.accounts.map(() => P.assets.map(() => 0));
  for (const name of ["IRP", "연금저축", "ISA"]) {
    const i = P.accounts.findIndex(a => a.name === name); if (i < 0) continue;
    const acc = P.accounts[i]; let room = acc.bal, rr = name === "IRP" ? TAX.IRP_RISKY * acc.bal : Infinity;
    const put = gi => { const k = defaultAsset(P, gi), risky = P.assets[k].risky; const cap = Math.max(0, Math.min(room, left[gi], risky ? rr : Infinity)); tab[i][k] += cap; left[gi] -= cap; room -= cap; if (risky) rr -= cap; };
    orderGroups.forEach(put); if (room > 1e-9) GROUPS.forEach((g, gi) => put(gi));
  }
  const g = P.accounts.findIndex(a => a.kind === "taxable");
  GROUPS.forEach((_, gi) => tab[g][defaultAsset(P, gi)] += left[gi]);
  return xFromTable(P, I, tab);
}
function evaluate(P, x) { const I = index(P); return { x, I, table: tableOf(P, I, x), ...valueOf(P, I, x) }; }

if (typeof module !== "undefined") module.exports = { TAX, GROUPS, lpSolve, solveLocation, marginalZ, proportional, fillOrder, evaluate, index, tableOf };
