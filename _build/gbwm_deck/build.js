// Das · Ostrov · Radhakrishnan · Srivastav(DORS) 목표기반 자산관리(GBWM) 연작 — 요약 · 재계산 · 활용 제로원 덱
// 실행: <python> compute.py → <python> assets.py → NODE_PATH=/Users/keerhee/Project/node_modules node build.js
process.chdir(__dirname);
const T = require("./template.js");
const R = require("./ratios.json");
const N = require("./numbers.json");
const { C, M, CW } = T;
T.setBrand({ eyebrow: "BAF.60080 · W06 GBI 보충 · GBWM 연작(DORS)", wordmark: "" });
const OUT = process.argv[2] || "GBWM_Series_DORS_zeroone.pptx";

let P = 0;
const _warn = console.warn; console.warn = (...a) => _warn(`[p${P}]`, ...a);
const rr = k => { if (!(k in R)) throw new Error("ratio 없음: " + k); return R[k]; };
const img = k => k + ".png";
const FIG_BOT = 5.82, PY = 5.98;
const LW = 5.15, RX = M + LW + 0.40, RW = CW - LW - 0.40;
const pc = (x, d = 1) => (100 * x).toFixed(d) + "%";
const f2 = (x, d = 2) => Number(x).toFixed(d);

function eqCol(s, items, x, w, y0, bot, gap) {
  gap = gap == null ? 0.20 : gap;
  const tot = items.reduce((a, it) => a + (it.wt || 1), 0);
  const unit = (bot - y0 - gap * (items.length - 1)) / tot;
  let y = y0;
  items.forEach(it => {
    const h = unit * (it.wt || 1);
    T.eqInCard(s, { x, w, y, h, kind: it.kind || "ghost", cap: it.cap, path: img(it.key), ratio: rr(it.key), pad: it.pad || (it.cap ? 0.26 : 0.16) });
    y += h + gap;
  });
}
function figAt(s, key, x, w, y, bot) {
  return T.figImg(s, img(key), rr(key), { y, bottom: bot, left: x, w, quiet: true });
}
function textCard(s, x, y, w, h, o) {
  T.card(s, x, y, w, h, o.kind || "white");
  const dark = o.kind === "dark";
  let cy = y + 0.24;
  if (o.cap) { T.txt(s, o.cap, { x: x + 0.30, y: cy, w: w - 0.60, h: 0.30, fontSize: 14, bold: true, color: dark ? C.lime : C.muted, valign: "middle" }); cy += 0.40; }
  const lh = (y + h - 0.20 - cy) / o.lines.length;
  o.lines.forEach((L, i) => {
    const t = typeof L === "string" ? { text: L } : L;
    T.txt(s, t.text, { x: x + 0.30, y: cy + i * lh, w: w - 0.60, h: lh, valign: "middle", bold: !!t.bold,
      fontSize: T.fitBody(t.text, w - 0.66, t.fs || 18, "textCard"), color: t.color || (dark ? C.white : C.body) });
  });
}
function noteN(s, text, o) {
  T.txt(s, text, { x: M + 0.10, y: (o && o.y) || 5.48, w: CW - 0.10, h: 0.50, fontSize: 13, bold: true,
    color: C.amber, valign: "middle", lineSpacingMultiple: 1.05 });
}
const fig2 = (s, kL, kR, cy, bot) => { const hw = (CW - 0.30) / 2; figAt(s, kL, M, hw, cy, bot); figAt(s, kR, M + hw + 0.30, hw, cy, bot); };

const Y18 = N.y2018, Y20 = N.y2020, H = N.hand, E = N.egp, M8 = N.m8, KO = N.korea;
const fixMax = Math.max(...Y20.fixed);
const ret15 = Y20.retire.find(r => r[0] === 15), pret15 = Y20.paper_retire.find(r => r[0] === 15);
const cfx = c => Y20.cashflow.find(r => r[0] === c);

// =============================================================== 01 표지
{
  const s = T.slide();
  T.cover(s, { title: "목표기반 자산관리(GBWM) 연작\nDas · Ostrov · Radhakrishnan · Srivastav 2018–2022", titleSize: 30,
    sub: "목표 확률을 효율선 · 동적계획법 · 여러 목표로 넓힙니다", org: "BAF.60080 · W06 GBI 보충 · 원 논문 연작 읽기",
    chain: ["2018 효율선 위 확률", "2020 동적계획법", "2022 여러 목표", "확률 프런티어"] });
  ++P;
}
// =============================================================== 02 목차
{
  const s = T.slide();
  T.head(s, { title: "네 편의 논문을 계보 · 재계산 · 활용 순서로 읽습니다", page: ++P,
    sub: "JOIM 16(3) 2018 · CMS 17 2020 · JBF 140 2022 · JOIM 21(3) 2023 — 원문 숫자는 numpy로 다시 계산했다" });
  T.agenda(s, [
    { num: "01", title: "계보와 문제", kicker: "위험 = 목표 미달 확률", desc: "Roy → Das–Markowitz → DORS 네 편 · RL 후속" },
    { num: "02", title: "2018 · 효율선 위 확률", kicker: "등고선 × 효율선의 접점", desc: "요건 아홉 · 3차식 · 86.6% · 좋은 · 나쁜 상태" },
    { num: "03", title: "2020 · 동적계획법", kicker: "자산 × 시점 격자를 거꾸로", desc: "Bellman 손계산 · 66.6% · 납입 · 인출 · TDF 대비" },
    { num: "04", title: "2022 · 여러 목표 · EGP", kicker: "살지 말지 + 포트폴리오", desc: "비용 · 효용 벡터 · 조합 폭발의 답 · 확률 프런티어" },
    { num: "05", title: "요약과 활용법", kicker: "언제 무엇을 · 어떻게 시키나", desc: "비교표 · 흐름도 · M8 · 한국 · 프롬프트" },
  ], { y: 2.22, rowH: 0.73 });
  T.banner(s, "원문 PDF는 저장소에 올리지 않는다 — 서지 · 저자 사이트 링크로만 인용", { y: 6.12 });
}
// =============================================================== D01
{ const s = T.slide(); T.divider(s, { num: "01", title: "계보와 문제", page: ++P,
  sub: "질문 — 이 연작은 앞 논문의 무엇을 풀고, 위험을 어떻게 다시 정의하는가 · 2018 1–2절 · 2020 1절 · 2022 1절" }); }
// 계보 지도
{
  const s = T.slide();
  const cy = T.head(s, { title: "여섯 단계의 계보는 앞 논문의 한계를 하나씩 풉니다", page: ++P,
    sub: "Roy 안전우선에서 DORS 2023 목표 확률 프런티어까지 — 아래 줄은 각 논문이 푸는 것" });
  figAt(s, "fig/s_lineage", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "2018은 한 번 정하는 접점, 2020은 해마다 고르는 DP, 2022는 살 목표까지 고릅니다" },
    { text: "같은 효율선 위에서 묻는 질문이 정적 → 동적 → 여러 목표 → 상담 언어로 넓어집니다", color: C.red }], { y: PY });
}
// 위험 = 미달 확률
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표 확률로 보면 변동성을 줄이는 것이 늘 안전하지는 않습니다", page: ++P,
    sub: "2018 원문 예 — 40만 → 10년 뒤 50만 달러, 효율선은 원문 그림의 점 여덟 개로 역산(강의 재계산)" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "DORS의 위험 정의",
    lines: ["업계 — 위험 = 변동성 σ", "투자자 — 위험 = 목표 미달 확률", "자금이 모자란 투자자가 σ를 줄이면", { text: "미달 확률이 오히려 커진다", bold: true, color: C.teal }] });
  figAt(s, "fig/c_risk", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: `σ를 0 쪽으로 내리면 목표 확률은 ${pc(Y18.ogpp[2])}에서 급히 떨어지고, 지나치게 올려도 서서히 떨어집니다` },
    { text: "효율선 위 어딘가에 목표 확률을 가장 크게 하는 점이 하나 있습니다", color: C.red }], { y: PY });
}
// =============================================================== D02
{ const s = T.slide(); T.divider(s, { num: "02", title: "2018 · 효율선 위의 목표 확률", page: ++P,
  sub: "A New Approach to Goals-Based Wealth Management · JOIM 16(3), 1–27 · 2018 Markowitz 상 — 정적 · 목표 하나 · 한 기간" }); }
// 요건 아홉 · 정보 여덟
{
  const s = T.slide();
  const cy = T.head(s, { title: "2018 논문은 GBWM의 요건 아홉과 고객에게 물을 정보 여덟을 정합니다", page: ++P,
    sub: "원문 3절 — 자문사 설문(투자자 503명 · 자문사 300명): '90% 확률로 목표 달성'은 92%가 이해한다" });
  figAt(s, "fig/s_props", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "고객은 γ나 σ가 아니라 기간 · 금액 · 확률 · 손실 문턱, 그리고 좋은 · 나쁜 상태의 선호 둘만 말합니다" },
    { text: "나머지(어느 포트폴리오인가)는 계산이 정합니다 — 강의 M8 '입력은 개인, 출력은 계산'과 같은 분업", color: C.red }], { y: PY });
}
// GPLC
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표 확률 등고선은 (σ, μ) 평면의 볼록한 포물선입니다", page: ++P,
    sub: "원문 식 (1)–(3) · 그림 4 재현 — 기하 브라운 운동, z₀는 Φ(z₀) = 목표 확률인 값" });
  eqCol(s, [{ key: "eq/gbm", cap: "식 (1) — 자산의 기하 브라운 운동" }, { key: "eq/gplc", cap: "식 (2) — 목표 확률 등고선(GPLC)", kind: "dark" }],
    M, 6.4, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_gplc", M + 6.7, CW - 6.7, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: `변동성 0이면 모든 등고선이 필요 성장률 ${pc(Y18.intercept, 2)}(40만 → 50만)에서 만나고, 확률을 높이면 위로 휩니다` },
    { text: "등고선 위쪽 = 목표 영역 — 효율선이 그 영역에 닿는 구간만 목표를 지킵니다", color: C.red }], { y: PY });
}
// 접점 · 3차식
{
  const s = T.slide();
  const cy = T.head(s, { title: "최적점은 등고선이 효율선에 접하는 한 점이고 3차식의 근입니다", page: ++P,
    sub: "원문 식 (5) z · 식 (4) 효율선 · 식 (8) 3차식 — z를 효율선 위에서 라그랑주 승수로 최대화한다" });
  eqCol(s, [{ key: "eq/zfun" }, { key: "eq/ef" }, { key: "eq/cubic", kind: "dark" }, { key: "eq/znum" }], M, 6.7, cy + 0.04, FIG_BOT, 0.12);
  figAt(s, "fig/c_tangent", M + 7.0, CW - 7.0, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: `세 근 ${f2(Y18.roots[0], 4)} · ${f2(Y18.roots[1], 4)} · ${f2(Y18.roots[2], 4)} 중 꼭짓점 위의 근은 하나뿐입니다` },
    { text: `그 점 (σ ${f2(Y18.ogpp[0], 3)}, μ ${f2(Y18.ogpp[1], 4)})에서 목표 확률이 ${pc(Y18.ogpp[2])}로 최대입니다`, color: C.red }], { y: PY });
}
// 재계산 표
{
  const s = T.slide();
  const cy = T.head(s, { title: "원문 그림의 점 여덟 개로 효율선을 되살리면 86.6%가 그대로 나옵니다", page: ++P,
    sub: "원문은 자산 셋의 μ · Σ를 주지 않는다 — 그림 9–13의 (σ, μ) 여덟 점으로 a · b · c를 최소제곱 역산(강의 재계산)" });
  T.dataTable(s, ["점 (원문 그림)", "원문 (σ, μ)", "재계산 (σ, μ)", "확률 기준", "판정"], [
    ["최적점 (그림 9)", "0.158 · 0.0902", `${f2(Y18.ogpp[0], 3)} · ${f2(Y18.ogpp[1], 4)}`, `최대 ${pc(Y18.ogpp[2])}`, "일치"],
    ["상단 목표점 (그림 10)", "0.424 · 0.225", `${f2(Y18.ugp[0], 3)} · ${f2(Y18.ugp[1], 3)}`, "80% 등고선", "일치"],
    ["다른 접점 (그림 13)", "μ .0083 · −.0669", `μ ${f2(Y18.roots[1], 4).replace("0.", ".")} · ${f2(Y18.roots[2], 4).replace("0.", ".")}`, "아래 절반", "근사"],
    ["중간점 (그림 10)", "0.291 · 0.158", `${f2(Y18.half[0], 3)} · ${f2(Y18.half[1], 3)}`, "σ 평균", "일치"],
    ["손실 문턱점 (그림 11)", "0.249 · 0.136", `${f2(Y18.ltp[0], 3)} · ${f2(Y18.ltp[1], 3)}`, "30만 · 95%", "다름"],
  ], { y: cy + 0.0, rowH: 0.52, widths: [2.75, 2.55, 2.55, 2.04, 1.90], emph: 0 });
  noteN(s, `※ 원문 손실 문턱점 (0.249, 0.136)은 30만 달러 95% 문턱선이 아니라 ${pc(Y18.p_at_paper_ltp)} 선 위에 있다 — 재계산은 (${f2(Y18.ltp[0], 3)}, ${f2(Y18.ltp[1], 3)}). 효율선을 점으로 역산했으므로 셋째 자리 차이는 반올림 오차`, { y: 5.34 });
  T.punch(s, [{ text: `역산 효율선은 여덟 점을 σ 오차 0.0011 안에서 지나고, 상단 목표점은 ${pc(Y18.p_at_paper_ugp, 2)} 선 위입니다` },
    { text: "닫힌 꼴 3차식 하나로 원문의 최적점과 확률이 재현됩니다", color: C.red }], { y: PY });
}
// 좋은 · 나쁜 상태
{
  const s = T.slide();
  const cy = T.head(s, { title: "좋은 상태와 나쁜 상태에서 고르는 점이 다릅니다", page: ++P,
    sub: "원문 4.3.2–4.3.3절 · 그림 10–12 — 고객이 미리 고른 선택 1 · 2 · 3이 효율선 위 점을 정한다" });
  figAt(s, "fig/s_options", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "좋은 상태는 확률과 기대수익 사이를, 나쁜 상태는 목표와 손실 문턱 사이를 고릅니다" },
    { text: "최적점보다 왼쪽은 위험도 확률도 나빠 어느 선택에서도 쓰지 않습니다", color: C.red }], { y: PY });
}
// W(0) 민감도
{
  const s = T.slide();
  const cy = T.head(s, { title: "자산이 줄면 최적점이 더 공격적인 쪽으로 옮겨 갑니다", page: ++P,
    sub: "원문 4.4절 — 약세장에서 W(0)이 줄면 등고선 전체가 위로 평행 이동한다 · 숫자는 역산 효율선의 재계산" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "원문의 관찰 (4.4절)",
    lines: ["W(0)↓ → 절편 r↑ → 등고선 위로", "선택 1이면 더 위험한 점으로", "약세장에 주식을 산다", { text: "TDF는 같은 점에 머문다", bold: true, color: C.teal }] });
  figAt(s, "fig/c_w0", RX, RW, cy + 0.04, FIG_BOT);
  const s30 = Y18.w0_sens[0], s45 = Y18.w0_sens[15];
  T.punch(s, [{ text: `W(0) 40만이면 σ* ${pc(Y18.ogpp[0])}, 30만이면 ${pc(s30[1])}, 45만이면 ${pc(s45[1])} — 앞서면 줄이고 뒤처지면 늘립니다` },
    { text: "정적 모형이지만 매년 다시 풀면 이미 '자산에 따라 움직이는' 전략이 됩니다 — 2020 DP의 예고", color: C.red }], { y: PY });
}
// =============================================================== D03
{ const s = T.slide(); T.divider(s, { num: "03", title: "2020 · 동적계획법", page: ++P,
  sub: "Dynamic Portfolio Allocation in Goals-Based Wealth Management · CMS 17, 613–640 — 2018의 확장 과제 '동적 · 납입 · 인출'을 푼다" }); }
// 문제
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표 확률 극대화를 시점 × 자산 격자 위의 최적 제어로 씁니다", page: ++P,
    sub: "원문 1–2절 — 상태 (t, W) · 행동 = 효율선 위 μ 하나 · 전이 = 로그정규 · 효용함수는 정하지 않는다" });
  T.eqInCard(s, { x: M + (CW - 6.2) / 2, w: 6.2, y: cy + 0.02, h: 1.05, kind: "dark", path: img("eq/obj20"), ratio: rr("eq/obj20"), pad: 0.14 });
  figAt(s, "fig/s_state", M, CW, cy + 1.20, FIG_BOT);
  T.punch(s, [{ text: "2018은 '지금 한 번' 최적이라 근시안적 — DP는 앞으로 다시 고를 수 있다는 사실까지 넣어 고릅니다" },
    { text: "끝에서 목표 달성 여부(0 · 1)를 정하고, 그 가치를 한 해씩 앞으로 옮기면 해마다의 최적 행동이 나옵니다", color: C.red }], { y: PY });
}
// 효율선 · 격자
{
  const s = T.slide();
  const cy = T.head(s, { title: "세 펀드 효율선에서 포트폴리오 15개를 고르고 자산 격자를 로그 간격으로 깝니다", page: ++P,
    sub: "원문 표 1(1998–2017 미국 채권 · 해외 주식 · 미국 주식) · 그림 1 · 식 (1)–(4) · 2.3절" });
  eqCol(s, [{ key: "eq/imax", cap: "격자 칸 수 — ln W를 σmin/ρ 간격으로(ρ = 3)" }], M, 6.4, cy + 0.04, cy + 1.62);
  textCard(s, M, cy + 1.80, 6.4, FIG_BOT - cy - 1.80, { kind: "white", cap: "원문 대 재계산 (W(0) 100 · G 200 · T 10)",
    lines: [`σ ${f2(Y20.sigs[0], 4)} ~ ${f2(Y20.sigs[14], 4)} (원문 .0374 ~ .1954)`,
      `격자 ${Y20.nodes}칸 (327) · ${f2(Y20.Wmin, 1)} ~ ${Y20.Wmax.toFixed(0)}`,
      { text: "W(0) 100이 격자점이 되게 아래로 민다", bold: true, color: C.teal }] });
  figAt(s, "fig/c_ef20", M + 6.7, CW - 6.7, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "0번은 채권 91%, 14번은 미국 주식 117% · 해외 −25% — 원문 그림 1 비중과 같습니다" },
    { text: "σmin이 원문보다 0.0003 작아 칸이 넷 많습니다 — 원문 표 1이 반올림된 탓입니다", color: C.red }], { y: PY });
}
// 전이 · Bellman
{
  const s = T.slide();
  const cy = T.head(s, { title: "전이확률은 정규화한 로그정규 밀도이고 Bellman 식은 그 기댓값의 최댓값입니다", page: ++P,
    sub: "위부터 원문 식 (6) 전이확률(칸들의 합이 1이 되게 나눈다) · 식 (5)(7) Bellman 역산 · 식 (8) 앞으로 전파" });
  eqCol(s, [{ key: "eq/trans" }, { key: "eq/bell", kind: "dark", wt: 1.1 }], M, CW, cy + 0.04, 4.62, 0.16);
  T.eqInCard(s, { x: M + (CW - 7.2) / 2, w: 7.2, y: 4.78, h: 1.04, kind: "ghost", path: img("eq/fwd"), ratio: rr("eq/fwd"), pad: 0.14 });
  T.punch(s, [{ text: "C(t)는 미리 정한 납입(+) · 인출(−) — 인출 뒤 0 이하면 파산, 가치 0 (3.2절)" },
    { text: "칸마다 μ 15개 중 기댓값이 가장 큰 것을 고를 뿐 — 효용함수도 모의도 필요 없습니다", color: C.red }], { y: PY });
}
// 손계산 ①
{
  const s = T.slide();
  const cy = T.head(s, { title: "손계산 ① — 자산 100에서 공격형을 고르면 다섯 칸으로 이렇게 퍼집니다", page: ++P,
    sub: "강의 축소 예 — 2기간 · 5칸(ln 간격 0.15) · A = 0번(보수) · B = 14번(공격) · 목표 110" });
  T.eqInCard(s, { x: M + (CW - 7.4) / 2, w: 7.4, y: cy + 0.02, h: 1.00, kind: "ghost", path: img("eq/hz"), ratio: rr("eq/hz"), pad: 0.12 });
  figAt(s, "fig/s_hand1", M, CW, cy + 1.14, FIG_BOT);
  T.punch(s, [{ text: "보수형 A는 거의 100에 머물러 목표 칸에 7.7%만, 공격형 B는 46.4%가 닿습니다" },
    { text: "5칸이라 끝에서 잘린 확률을 나눠 1로 맞춥니다 — 원문은 Z ±3까지 칸을 깔아 막습니다", color: C.red }], { y: PY });
}
// 손계산 ②
{
  const s = T.slide();
  const cy = T.head(s, { title: "손계산 ② — 거꾸로 풀면 뒤처진 칸은 공격형, 앞선 칸은 보수형을 고릅니다", page: ++P,
    sub: "시점 2의 가치 V = 1{W ≥ 110} → 시점 1의 칸마다 A · B의 기댓값 비교 → 시점 0의 자산 100" });
  figAt(s, "fig/s_hand2", M, CW, cy + 0.02, 4.86);
  T.eqInCard(s, { x: M + (CW - 7.0) / 2, w: 7.0, y: 4.96, h: 0.86, kind: "dark", path: img("eq/hv0"), ratio: rr("eq/hv0"), pad: 0.12 });
  T.punch(s, [{ text: `목표 위 칸은 A로 지키고 100 이하는 B로 노립니다 — 고정 A ${f2(H.fixedA, 3)} · 고정 B ${f2(H.fixedB, 3)}` },
    { text: `해마다 다시 고르는 DP가 ${f2(Math.max(...H.E0), 3)}로 가장 높습니다 — 원문 그림 4의 원리입니다`, color: C.red }], { y: PY });
}
// 가치함수 · 전략 지도
{
  const s = T.slide();
  const cy = T.head(s, { title: "뒤처지면 공격적으로, 앞서면 보수적으로 — 전략은 시점과 자산 둘 다에 달립니다", page: ++P,
    sub: "원문 그림 3 · 4 재현 — 왼쪽 목표 확률 V(t, W), 오른쪽 최적 포트폴리오 번호(0 보수 ~ 14 공격) · 자산 37~226" });
  fig2(s, "fig/c_value", "fig/c_policy", cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: `시작은 ${Y20.l0}번 μ ${f2(Y20.mu0, 4)} · σ ${f2(Y20.sig0, 4)} (원문 .0835 · .1686) — 공격형 경계는 목표 쪽으로 오릅니다` },
    { text: "TDF는 시점만 보지만 DP는 지금 자산이 목표에 얼마나 가까운지도 봅니다", color: C.red }], { y: PY });
}
// 66.6%
{
  const s = T.slide();
  const cy = T.head(s, { title: "같은 15개 포트폴리오로 DP는 10년 두 배 확률을 66.6%까지 올립니다", page: ++P,
    sub: "W(0) 100 → G 200 · T 10 · 연 재조정 — 원문 66.9%, 고정 · 정적과의 비교는 강의 재계산" });
  figAt(s, "fig/c_compare", M, CW, cy + 0.02, 5.36);
  const sr = Y20.sens_rho.map(r => r[3]);
  noteN(s, `※ 격자 밀도 ρ 1~6에서 재계산 ${pc(Math.min(...sr))} ~ ${pc(Math.max(...sr))} (원문 표 3: 66.2 ~ 67.6%) — 두 값의 차 0.3%p는 격자 잡음 안. 포트폴리오 5 → 40개면 ${pc(Y20.sens_m[0][3])} → ${pc(Y20.sens_m[4][3])} (원문 66.5 → 66.9%), 기본 예 계산 ${f2(Y20.runtime, 2)}초`, { y: 5.42 });
  T.punch(s, [{ text: `고정 최고 ${pc(fixMax)}, 2018 정적 해를 매년 다시 풀면 ${pc(Y20.repeated_static)} — 원문 5절의 관찰 그대로입니다` },
    { text: `DP는 고정보다 ${((Y20.P200 - fixMax) * 100).toFixed(1)}%p 높고, 납입 · 인출이 끼면 정적 해로는 못 풉니다`, color: C.red }], { y: 6.02 });
}
// 분포
{
  const s = T.slide();
  const cy = T.head(s, { title: "DP는 목표 바로 위에 확률 질량을 모아 끝 분포를 왼쪽으로 기울입니다", page: ++P,
    sub: "원문 그림 2 재현 — 해마다 P[W(t) ≥ W], 위쪽에 있을수록 좋다" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "읽는 법",
    lines: ["초기에는 로그정규처럼 오른쪽 꼬리", "목표에 가까워지면 위험을 줄여", "G = 200 바로 위에 혹이 생긴다", { text: `P[W(10) ≥ 150] = ${pc(Y20.P150)} (원문 77.7%)`, bold: true, color: C.teal }] });
  figAt(s, "fig/c_dist", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "목표를 넘는 자산은 쓸모가 없으므로 위쪽 꼬리를 팔아 G 근처의 확률을 삽니다 — 디지털 옵션의 수익 구조" },
    { text: "그래서 DP는 '평균 수익'이 아니라 '목표에 닿을 확률'만 최대로 만든다는 것을 기억해야 합니다", color: C.red }], { y: PY });
}
// 납입 · 인출
{
  const s = T.slide();
  const cy = T.head(s, { title: "해마다 1씩만 넣어도 확률이 6%p 오르고, 10씩 빼면 파산 확률이 12%가 됩니다", page: ++P,
    sub: "원문 표 5 · 6 재현 — 기본 예에 t = 1 … 9 동안 매년 C를 넣거나(+) 뺀다(−), 파산 = 인출 뒤 0 이하" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "재계산 (원문)",
    lines: [`C +1 → ${pc(cfx(1)[3])} (73.0%)`, `C +5 → ${pc(cfx(5)[3])} (94.4%)`, `C −10 → 파산 ${pc(cfx(-10)[1])} (12.4%)`,
      `C −15 → 파산 ${pc(cfx(-15)[1])} (49.2%)`, { text: "계산 시간은 그대로", bold: true, color: C.teal }] });
  figAt(s, "fig/c_cash", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "현금흐름이 있어도 격자 범위만 넓어질 뿐 같은 Bellman 식이고, 파산 확률이 부산물로 나옵니다" },
    { text: "작은 납입이 확률을 크게 올린다 — 저축을 설득하는 숫자가 고객의 목표 언어로 나옵니다", color: C.red }], { y: PY });
}
// 은퇴 · TDF
{
  const s = T.slide();
  const cy = T.head(s, { title: "같은 세 펀드로도 자산 수준을 보는 DP가 TDF보다 30%p 넘게 높습니다", page: ++P,
    sub: "원문 표 7–8 — 50세 10만, 65세까지 연 c 납입, 66~80세 연 5만(실질) 인출, 80세 지급 능력" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "c = 15일 때 재계산 (원문)",
    lines: [`DP ${pc(ret15[1])} (${pc(pret15[1])})`, `TDF ${pc(ret15[2])} (${pc(pret15[2])})`, "TDF = 표 8 비중 · 모의 20만",
      { text: "차이 = 자산 의존 + 효율선 + 목표", bold: true, color: C.teal }] });
  figAt(s, "fig/c_retire", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "DP 숫자는 원문 표 7과 소수 첫째 자리까지 같고, TDF는 모의 방식 차이로 1%p 안쪽만 다릅니다" },
    { text: "TDF로 같은 58.6%에 닿으려면 연 납입을 15에서 약 24로 늘려야 합니다 — DP는 같은 목표를 더 싸게 삽니다", color: C.red }], { y: PY });
}
// =============================================================== D04
{ const s = T.slide(); T.divider(s, { num: "04", title: "2022 · 여러 목표와 확률 프런티어", page: ++P,
  sub: "Dynamic Optimization for Multi-Goals Wealth Management · JBF 140, 106192 · Efficient Goal Probabilities · JOIM 21(3), 2023" }); }
// 2022 문제
{
  const s = T.slide();
  const cy = T.head(s, { title: "여러 목표는 해마다 '살지 말지'와 포트폴리오를 함께 고르는 문제입니다", page: ++P,
    sub: "원문 식 (4) — 목표 칸 k와 포트폴리오 l을 함께 고른다 · 아래는 표 2 둘째 줄의 기대 효용 분해" });
  eqCol(s, [{ key: "eq/bell22", kind: "dark", wt: 1.2 }, { key: "eq/eu" }], M, CW, cy + 0.04, 4.45, 0.16);
  T.cards(s, [{ kind: "white", cap: "효용", title: "상대 비율만 중요" }, { kind: "white", cap: "출력", title: "목표별 달성 확률" },
    { kind: "dark", cap: "고객", title: "확률 보고 효용 수정" }], { y: 4.62, h: 1.20 });
  T.punch(s, [{ text: "효용은 연속 함수가 아니라 목표마다 숫자 하나 — 비용이 같아도 중요도가 다를 수 있습니다" },
    { text: "고객은 효용은 몰라도 그 결과인 목표별 확률표는 읽습니다 — 사람이 고리 안에 남습니다", color: C.red }], { y: PY });
}
// 비용 · 효용 벡터
{
  const s = T.slide();
  const cy = T.head(s, { title: "같은 해 목표 조합 30개는 정렬과 지배 제거로 13칸이 됩니다", page: ++P,
    sub: "원문 2.3절 예 — 목표 1(전부 아니면 전무) · 목표 2 · 3(부분 달성 가능), 재계산이 원문 벡터와 같다" });
  figAt(s, "fig/s_combine", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "같은 비용이면 효용 큰 칸만, 더 싼 칸보다 효용이 작으면 버립니다 — 둘이 함께 오릅니다" },
    { text: "해마다 고를 것은 이 벡터의 몇 번째 칸인가 하나 — 목표가 늘어도 한 줄입니다", color: C.red }], { y: PY });
}
// 표 2
{
  const s = T.slide();
  const cy = T.head(s, { title: "효용 비율이 바뀌면 5년 목표의 확률이 90%에서 1%까지 움직입니다", page: ++P,
    sub: "원문 표 2 패널 A 재계산 — W(0) 100, 5년 뒤 비용 100 · 10년 뒤 비용 150, 격자 475칸" });
  const tb = N.y2022_tab2, tp = N.y2022_tab2_paper;
  const row = (u5, u10) => { const r = tb.find(x => x[0] === 100 && x[2] === u5 && x[3] === u10), p = tp.find(x => x[0] === 100 && x[2] === u5 && x[3] === u10);
    return [`${u5} : ${u10}`, `${r[4].toFixed(0)} (${p[4]})`, `${pc(r[6])} (${pc(p[6])})`, `${pc(r[7])} (${pc(p[7])})`]; };
  T.dataTable(s, ["효용 u(5) : u(10)", "E*[u] 재계산 (원문)", "5년 목표 확률", "10년 목표 확률"],
    [row(1000, 1000), row(1000, 2000), row(1000, 3000), row(2000, 3000), row(3000, 1000)],
    { y: cy + 0.02, rowH: 0.58, widths: [2.90, 2.96, 2.96, 2.97], emph: 2 });
  T.punch(s, [{ text: `격자 상한 ${N.y2022_grid.Wmax.toFixed(0)}(원문 1,834) · 확률 차 1%p 안팎 — u(5) ≥ u(10)이면 자금이 있을 때 늘 삽니다` },
    { text: "1 : 3이면 자금이 있어도(97.6%) 1.3%만 삽니다 — 10년 목표를 지키려 참는 것이 최적", color: C.red }], { y: PY });
}
// 결정 구간
{
  const s = T.slide();
  const sw = N.y2022_switch.filter(x => x >= 80 && x <= 260);
  const cy = T.head(s, { title: `5년 뒤 자산이 ${sw[1].toFixed(0)}~${sw[2].toFixed(0)}이면 앞 목표를 건너뛰는 것이 최적입니다`, page: ++P,
    sub: "원문 4.1.3절 — 휴가(5년 · 100 · 효용 2000)와 차(10년 · 150 · 효용 3000), 시점 5의 두 선택의 가치" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "재계산 (원문 100 · 108 · 182)",
    lines: [`100 ~ ${sw[1].toFixed(0)} — 산다 (차는 어차피 멀다)`, `${sw[1].toFixed(0)} ~ ${sw[2].toFixed(0)} — 건너뛴다 (차를 노린다)`, `${sw[2].toFixed(0)} 이상 — 산다 (둘 다 가능)`,
      { text: "결정이 자산에 따라 두 번 뒤집힌다", bold: true, color: C.teal }] });
  figAt(s, "fig/c_switch", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "몬테카를로는 '자금이 있으면 산다'는 규칙만 시험하고, DP는 뒤집힘 경계를 계산합니다" },
    { text: "원문 서론의 질문 '휴가를 갈까'의 답 — 애매하면 참고, 아주 적거나 많으면 간다", color: C.red }], { y: PY });
}
// 일곱 목표
{
  const s = T.slide();
  const S7 = N.y2022_seven;
  const cy = T.head(s, { title: "일곱 목표의 확률은 효용 · 초기 자금 · 납입을 고쳐 가며 원하는 수준에 맞춥니다", page: ++P,
    sub: "원문 표 3 · 4 — Run 1(W(0) 30) → Run 7(W(0) 50 · 첫 6년 연 3, 이후 연 2 납입 · 효용 조정), 25년 · 556칸" });
  figAt(s, "fig/c_seven", M, CW, cy + 0.02, 5.36);
  noteN(s, `※ Run 1 재계산 E*[u] ${S7.V.toFixed(0)} (원문 5,415) · 효용 비율 ${pc(S7.frac)} (원문 50.1%) · 격자 상한 ${S7.Wmax.toFixed(0)} (원문 5,026) — 확률 차 0.4%p 안 · 원문 표 3과 표 11 첫 줄도 서로 0.1%p 다르다`, { y: 5.42 });
  T.punch(s, [{ text: "빨간 선에 못 미치면 효용을 올리고, 넘치면 내리고, 모두 모자라면 자금을 더합니다" },
    { text: "Run 7에서 일곱 목표가 모두 선을 넘습니다 — 효용은 확률을 맞추는 손잡이일 뿐입니다", color: C.red }], { y: 6.02 });
}
// 조합 폭발
{
  const s = T.slide();
  const cy = T.head(s, { title: "상태 공간 DP는 목표 조합을 세지 않아 계산이 목표 수에 선형으로 늘어납니다", page: ++P,
    sub: "M8 51장의 질문 '목표가 여럿이면 조합이 폭발한다'에 대한 원문 3.2절의 답 — 상태는 (t, W) 둘뿐" });
  eqCol(s, [{ key: "eq/cplx", cap: "원문 3.2절 계산량 (분할)", kind: "dark" }], M, LW, cy + 0.04, cy + 1.62);
  textCard(s, M, cy + 1.80, LW, FIG_BOT - cy - 1.80, { kind: "white", cap: "원문 4.5절 큰 예",
    lines: ["60년 · 목표 301 + 부분 138", "분할 전 13분 → 17초", { text: "목표는 행동, 상태가 아니다", bold: true, color: C.teal }] });
  figAt(s, "fig/c_scal", RX, RW, cy + 0.04, FIG_BOT);
  const sc = N.scaling;
  T.punch(s, [{ text: `목표는 해마다의 행동 칸으로만 들어가 1 → 24개에도 ${f2(sc[0][1])} → ${f2(sc[sc.length - 1][1])}초입니다` },
    { text: "한계는 반대쪽 — 상태(세금 · 사망 · 목표 미루기)가 늘면 격자가 곱으로 커집니다", color: C.red }], { y: PY });
}
// TDF · MC 비교
{
  const s = T.slide();
  const R8 = N.y2022_retire;
  const cy = T.head(s, { title: "목표가 셋인 60년 은퇴 설계에서도 DP가 TDF보다 20%p 넘게 앞섭니다", page: ++P,
    sub: "원문 표 8 — 35세 10만 · 연 1만 납입 · 연금 250만(70세) · 300만(85세) · 증여 400만(95세)" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "95세까지 세 목표 모두 (재계산 · 원문)",
    lines: [`DP ${pc(R8.dp[2])} · ${pc(R8.paper_dp[2])}`, `TDF ${pc(R8.tdf[2])} · ${pc(R8.paper_tdf[2])}`, "원문 4.5.2절 MC: 포트폴리오 고정이면", { text: "301개 목표 모두 7%뿐", bold: true, color: C.teal }] });
  figAt(s, "fig/c_ret22", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "'앞 목표를 모두 낸 경로 비율'로 읽어야 원문 표가 재현됩니다(강의 해석)" },
    { text: `DP 우위는 재계산 ${((R8.dp[2] - R8.tdf[2]) * 100).toFixed(0)}%p · 원문 ${((R8.paper_dp[2] - R8.paper_tdf[2]) * 100).toFixed(0)}%p — 숫자는 다르지만 방향과 크기는 같습니다`, color: C.red }], { y: PY });
}
// EGPF
{
  const s = T.slide();
  const st = N.static20.cases;
  const cy = T.head(s, { title: "효용 비율을 0에서 무한대까지 돌리면 목표 확률의 효율 프런티어가 생깁니다", page: ++P,
    sub: "EGP 3절 — W(0) 5만, 10년 뒤 차 10만 · 20년 뒤 학자금 15만 · 포트폴리오 15개" });
  textCard(s, M, cy + 0.04, LW, 4.98 - cy - 0.04, { kind: "white", cap: "한 목표면 점 하나 — 10만에서 (2절)",
    lines: [`5년 12.5만: ${pc(st[0][5], 0)} (원문 72%)`, `6년 15만: ${pc(st[1][5], 0)} (원문 51%)`,
      `σ ${pc(st[0][4], 1)} · ${pc(st[1][4], 1)} (4.7 · 18.1%)`, { text: "목표 n개면 n − 1차원 곡면", bold: true, color: C.teal }] });
  figAt(s, "fig/c_egpf", RX, RW, cy + 0.04, 4.98);
  noteN(s, `※ 끝점 재계산 ${pc(Math.max(...E.fr50.map(r => r[2])))} · ${pc(Math.max(...E.fr50.map(r => r[1])))} (원문 87.5 · 70.9%). 원문 70.9%는 2020 표가 보인 '10년 두 배 최대 66.9%'보다 높아, 목표 시점을 한 해 늦게 셈한 것으로 보인다(11년이면 ${pc(E.single[2][2])})`, { y: 5.10 });
  T.punch(s, [{ text: "프런티어 위쪽은 불가능, 아래쪽은 가능하지만 비효율 — 마코위츠 효율선과 같은 읽는 법입니다" }], { y: 6.02 });
}
// 근접점 · 최소 자금
{
  const s = T.slide();
  const cy = T.head(s, { title: `원하는 확률 점에 닿는 최소 초기 자금은 할선법으로 찾습니다 — ${f2(E.minW, 1)} 대 원문 79.9`, page: ++P,
    sub: "EGP 식 (9)–(11) 근접점(효용을 d − p 쪽으로) · 4.2절 할선법 — 원하는 점 d = (70%, 80%)" });
  eqCol(s, [{ key: "eq/upd", kind: "dark" }, { key: "eq/sec" }], M, 6.4, cy + 0.04, 4.30, 0.16);
  textCard(s, M, 4.46, 6.4, FIG_BOT - 4.46, { kind: "white", cap: "재계산 (원문)",
    lines: [`근접점 ${pc(E.prox50[0])} · ${pc(E.prox50[1])} (48.9 · 58.3%)`, `최소 ${f2(E.minW, 1)} · 효용 100 : ${f2(E.U_min[1], 1)} (79.9 · 108.5)`] });
  figAt(s, "fig/c_egpmin", M + 6.7, CW - 6.7, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: `할선 ${E.secant.map(x => f2(x[0], 1)).join(" → ")} — 다섯 번에 수렴, 원문 시점 관례 차이만큼 낮게 나옵니다` },
    { text: "원문 부분 목표 예 — 기대수익 +1%p면 39.4 → 33.6, 공분산 ×1.5면 42.9", color: C.red }], { y: PY });
}
// =============================================================== D05
{ const s = T.slide(); T.divider(s, { num: "05", title: "요약과 활용법", page: ++P,
  sub: "비교표 · 언제 무엇을 쓰나 · 실무 절차 · M8 · 한국 대입 · Claude Code로 2020 DP 구현 · 한계" }); }
// 비교표 1
{
  const s = T.slide();
  const cy = T.head(s, { title: "다섯 편은 푸는 문제 · 시간 구조 · 목표 수에서 한 칸씩 넓어집니다", page: ++P,
    sub: "한 장 비교표 ① — 무엇을 어떻게 푸나" });
  T.dataTable(s, ["논문", "푸는 문제", "정적 · 동적", "목표 수", "해법"], [
    ["DMSS 2010", "계정별 (H, α) → γ", "정적", "계정 여럿", "닫힌 해 · QP"],
    ["DORS 2018", "목표 확률 최대 점", "정적 · 매년", "하나 + 문턱", "3차식"],
    ["DORS 2020", "끝 시점 목표 확률", "동적", "하나", "격자 DP"],
    ["DORS 2022", "목표 효용 합 최대", "동적 · 살지 말지", "여럿 · 부분", "격자 DP 분할"],
    ["DORS 2023", "확률 프런티어 · 최소 자금", "동적", "여럿", "DP + 할선법"],
  ], { y: cy + 0.02, rowH: 0.62, widths: [2.05, 3.55, 2.30, 1.84, 2.05], emph: 2 });
  T.punch(s, [{ text: "2010 · 2018은 한 번 푸는 정적 해, 2020부터는 자산 × 시점 격자를 거꾸로 푸는 동적 해입니다" },
    { text: "모두 같은 효율선(평균-분산) 위에서 고르고, 위험을 목표 미달 확률로 잽니다", color: C.red }], { y: PY });
}
// 비교표 2
{
  const s = T.slide();
  const cy = T.head(s, { title: "계산은 모두 1분 안이고, 한계는 정규 · 고정 가정과 상태 차원입니다", page: ++P,
    sub: "한 장 비교표 ② — 계산량 · 강점 · 한계 (계산 시간은 이 덱의 numpy 재계산 기준)" });
  T.dataTable(s, ["논문", "계산량", "강점", "한계"], [
    ["DMSS 2010", "역행렬 하나", "목표 언어 = γ", "한 기간 · 빈도만"],
    ["DORS 2018", "3차식 하나", "고객 언어 · 선택 규칙", "근시안 · 현금흐름 불가"],
    ["DORS 2020", `${f2(Y20.runtime, 2)}초 (${Y20.nodes}칸)`, "자산 따라 전략 · 파산", "목표 하나 · μΣ 고정"],
    ["DORS 2022", "수 초 (분할)", "조합 대신 행동 칸", "목표 미루기 불가"],
    ["DORS 2023", "DP 수십 번 · 수 분", "효용 없이 확률 상담", "n ≥ 4면 그림 불가"],
  ], { y: cy + 0.02, rowH: 0.62, widths: [2.05, 2.75, 3.50, 3.49], emph: 2 });
  T.punch(s, [{ text: "2020 원문도 '정적 해를 매년 다시 풀면 DP와 비슷하다'고 쓴다 — 갈림은 현금흐름 · 여러 목표" },
    { text: "격자 DP의 적은 상태 차원 — 그래서 저자들의 다음 연구가 강화학습입니다", color: C.red }], { y: PY });
}
// 흐름도
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표 수 · 기간 · 상담 방식에 따라 쓸 도구가 정해집니다", page: ++P,
    sub: "강의 정리 — 바닥 보장은 규칙(CPPI · Flexicure), 확률 최적화는 DP, 검증은 몬테카를로" });
  figAt(s, "fig/s_flow", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "마지막은 늘 몬테카를로 검증 — 두꺼운 꼬리 · 세금 · 수수료는 경로로 확인합니다(M8 방법 3)" },
    { text: "바닥은 규칙으로 지키고, 그 위의 목표 확률은 DP로 최대화하는 조합이 현실적입니다", color: C.red }], { y: PY });
}
// 실무 절차
{
  const s = T.slide();
  const cy = T.head(s, { title: "실무에서는 다섯 단계를 해마다 다시 돌립니다", page: ++P,
    sub: "원문 2018 4.5절(매년 재실행 권고) · 2020 2.6절 · 2022 4.2.1절(사람이 고리 안에) — 강의 정리" });
  figAt(s, "fig/s_pipeline", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "고객에게는 목표별 확률만 보이고, 모자라면 납입 · 목표 · 효용을 고칩니다" },
    { text: "결과는 '이 자산이면 이 포트폴리오'라는 전략 표 — 매년 자산을 넣어 찾아 쓰면 됩니다", color: C.red }], { y: PY });
}
// M8 대입
{
  const s = T.slide();
  const cy = T.head(s, { title: `M8의 세 목표를 DP로 풀면 필요 자본이 9.13억에서 약 ${f2(M8.minW, 1)}억으로 줄어듭니다`, page: ++P,
    sub: "강의 재계산 — 55세 · 10년 뒤 6 · 9 · 14억을 95 · 70 · 30%로 · GHP 2% · 주식 λ 6% σ 20%" });
  T.barsH(s, [{ label: "방법 1 · 계좌 분리", value: 9.13, shown: "9.13억", color: C.hair },
    { label: "방법 3 · 한 계좌 고정 비중", value: 7.1, shown: "7.1억", color: C.blue },
    { label: "2022 DP · 해마다 비중", value: M8.minW, shown: `${f2(M8.minW, 2)}억`, color: C.teal }],
    { y: cy + 0.10, rowH: 0.80, barX: M + 3.2, barW: 2.0, max: 9.5 });
  figAt(s, "fig/c_m8", M + 6.7, CW - 6.7, cy + 0.04, 4.90);
  noteN(s, `※ 확률 ${M8.p.map(x => pc(x)).join(" · ")}, 효용 1 : ${f2(M8.U[1], 2)} : ${f2(M8.U[2], 2)} · 시작 주식 ${pc(M8.w0_choice, 0)} — Safety가 GHP 확정이 아니라 95% 확률로 바뀐다. 위험자산 70% 한도면 같은 자금에서 ${M8.cap70_at_minW.map(x => pc(x)).join(" · ")}로 약간 모자란다`, { y: 5.00 });
  T.punch(s, [{ text: "방법 1 · 2는 목표마다 따로, 방법 3은 한 번 정한 비중 — DP는 자산이 Safety 근처면 줄이고 멀면 늘립니다" },
    { text: "Safety를 확정으로 둘지(방법 1) 확률로 둘지(DP)가 3억 차이의 대가 — IC가 정할 정책입니다", color: C.red }], { y: 6.02 });
}
// 한국 대입
{
  const s = T.slide();
  const cy = T.head(s, { title: "디폴트옵션 · IRP · H대 기금에는 각각 다른 논문을 대입합니다", page: ++P,
    sub: "M8 단원 ⑦⑧⑩ — 위험자산 70% 한도는 2020 효율선 위 μmax를 자른다(공매도 허용 효율선 · 강의 재계산)" });
  figAt(s, "fig/s_korea", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: `70% 한도면 μmax ${pc(0.0886, 2)} → ${pc(KO.mu_cap, 2)}, 10년 두 배 확률 ${pc(Y20.P200)} → ${pc(KO.P200_cap)} — 한도의 비용을 확률로 말할 수 있습니다` },
    { text: "H대 지출 4.5% · 3.5%는 2022의 완전 · 부분 목표 — Flexicure와 같은 언어가 됩니다", color: C.red }], { y: PY });
}
// 프롬프트
{
  const s = T.slide();
  const cy = T.head(s, { title: "2020 DP는 Claude Code에게 이렇게 시킵니다", page: ++P });
  figAt(s, "fig/s_prompt", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "빈 폴더에 붙여 넣는다 — 가정은 숫자로, 할 일은 식 번호로, 검증은 원문 값으로" },
    { text: "'안 맞으면 스스로 고쳐줘'까지 적어야 Claude Code가 원문과 대조하며 끝까지 갑니다", color: C.red }], { y: PY });
}
// 실행 결과
{
  const s = T.slide();
  const cy = T.head(s, { title: "그 프롬프트가 만든 gbwm_dp.py는 0.5초에 원문 숫자를 냅니다", page: ++P });
  figAt(s, "fig/s_output", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: `검증 넷 — 격자 ${Y20.nodes}칸 · P ${f2(Y20.P200, 3)}(원문 0.669) · 시작 μ ${f2(Y20.mu0, 4)} · C −10 파산 ${pc(cfx(-10)[1])}(원문 12.4%)` },
    { text: "확장 과제 — --G를 바꿔 목표 확률 곡선을, C에 은퇴 인출을 넣어 원문 표 7을 직접 재현해 본다", color: C.red }], { y: PY });
}
// 한계
{
  const s = T.slide();
  const cy = T.head(s, { title: "기하 브라운 운동 · 고정된 μ · Σ · 미루지 못하는 목표라는 한계를 함께 읽습니다", page: ++P,
    sub: "원문 2018 5절 · 2020 5절 · 2022 5절 · EGP 5절이 스스로 적은 확장 과제" });
  T.cards(s, [
    { kind: "white", cap: "모형", title: "분포와 가정",
      bullets: ["GBM · 정규 꼬리", "μ · Σ가 수십 년 고정", "t분포 5면 효용 −0.07%"] },
    { kind: "white", cap: "목표", title: "정해진 시점",
      bullets: ["목표를 미룰 수 없다", "효용은 사람이 정한다", "확률만 최대 · 꼬리 무시"] },
    { kind: "dark", cap: "계산", title: "상태의 차원",
      bullets: ["세금 · 사망 · 금리 상태", "격자가 곱으로 커진다", "그래서 RL 후속 연구"] },
  ], { y: cy + 0.05, h: 3.45 });
  T.punch(s, [{ text: "확률 최대화는 미달의 크기를 보지 않습니다 — 손실 문턱 · floor를 함께 둡니다" },
    { text: "격자 DP는 '목표 시점과 금액이 정해진' 문제에서 가장 강합니다", color: C.red }], { y: PY });
}
// 한 장 요약
{
  const s = T.slide();
  const cy = T.head(s, { title: "정적 접점 → 동적 격자 → 여러 목표 → 확률 프런티어로 정리됩니다", page: ++P,
    sub: "한 장 요약 — 숫자는 원문 예의 numpy 재계산" });
  figAt(s, "fig/s_summary", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: `86.6% (2018) · 66.6% vs 고정 ${pc(fixMax)} (2020) · 1 : 3이면 5년 목표 1% (2022) · 최소 자금 ${f2(E.minW, 1)} (2023)` },
    { text: "고객에게는 확률로 묻고 확률로 보여 주고, 포트폴리오는 계산이 매년 다시 고릅니다", color: C.red }], { y: PY });
}
// 마감
{
  const s = T.slide();
  T.closing(s, {
    statements: ["위험은 목표에 못 미칠 확률입니다", "자산에 따라 해마다 다시 고릅니다", "목표가 많아도 조합은 세지 않습니다"],
    message: "확률로 묻고 확률로 답하고\n포트폴리오는 계산이 고릅니다",
    note: "출처: Das · Ostrov · Radhakrishnan · Srivastav — JOIM 16(3) 2018, 1–27 · CMS 17 2020, 613–640 · JBF 140 2022, 106192 · JOIM 21(3) 2023 (srdas.github.io/Papers: GBWM · DP_Paper · MultWealthGoals · EGPF.pdf) · 재계산 _build/gbwm_deck",
  });
  ++P;
}

T.save(OUT).then(f => console.log("saved", f, "slides", P));
