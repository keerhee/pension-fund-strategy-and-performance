// Das–Markowitz–Scheid–Statman(2010) 심리계정 포트폴리오 — 원 논문 예 중심 제로원 덱
// 실행: (assets.py 먼저) NODE_PATH=/Users/keerhee/Project/node_modules node build.js
process.chdir(__dirname);
const T = require("./template.js");
const R = require("./ratios.json");
const { C, M, CW } = T;
T.setBrand({ eyebrow: "BAF.60080 · W06 GBI 보충 · Das–Markowitz(2010)", wordmark: "" });
const OUT = process.argv[2] || "DMSS_Mental_Accounts_zeroone.pptx";

let P = 0;
const _warn = console.warn; console.warn = (...a) => _warn(`[p${P}]`, ...a);
const rr = k => { if (!(k in R)) throw new Error("ratio 없음: " + k); return R[k]; };
const img = k => k + ".png";
const FIG_BOT = 5.82;
const LW = 5.15, RX = M + LW + 0.40, RW = CW - LW - 0.40;

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
const PY = 5.98;
// 두 줄까지 허용하는 ※ 각주 (13pt, 앰버) — 원문 대조 결과를 밝히는 데 쓴다
function noteN(s, text, o) {
  T.txt(s, text, { x: M + 0.10, y: (o && o.y) || 5.56, w: CW - 0.10, h: 0.50, fontSize: 13, bold: true,
    color: C.amber, valign: "middle", lineSpacingMultiple: 1.05 });
}   // punch 시작

// =============================================================== 01 표지
{
  const s = T.slide();
  T.cover(s, { title: "심리계정 포트폴리오\nDas · Markowitz · Scheid · Statman (2010)", titleSize: 32,
    sub: "목표 언어 (H, α)를 위험회피도 γ로 번역합니다", org: "BAF.60080 · W06 GBI 보충 · 원 논문 읽기",
    chain: ["계정별 (H, α)", "분위수 조건", "내재 γ", "효율선 위 합산"] });
  ++P;
}
// =============================================================== 02 목차
{
  const s = T.slide();
  T.head(s, { title: "원 논문의 예 하나를 손계산에서 롱온리까지 따라갑니다", page: ++P,
    sub: "Portfolio Optimization with Mental Accounts · JFQA 45(2), 2010, pp. 311–334" });
  T.agenda(s, [
    { num: "01", title: "무엇을 풀려는가", kicker: "계정의 언어와 γ의 언어", desc: "BPT 심리계정 · MVT의 γ · 논문의 세 결과" },
    { num: "02", title: "계정 하나와 손계산", kicker: "확률 제약 → 분위수 조건", desc: "식 (5)–(6) · 60 · 30 · 10 검사 · 두 자산 w* 52.2%" },
    { num: "03", title: "행렬로 일반화", kicker: "최소분산 + 위험 방향", desc: "A · B · C · D · 식 (7)의 γ · 은퇴 계정 3.795" },
    { num: "04", title: "세 계정 · 합산 · 가능성", kicker: "합쳐도 효율, 단 가능한 목표만", desc: "표 1–2 · 합산 γ 2.174 · 가능성 −2.31%" },
    { num: "05", title: "롱온리와 강의 연결", kicker: "마찰은 수 bp", desc: "식 (20)–(29) · 손풀이 · 해 찾기 · 12bp · 표 3" },
  ], { y: 2.22, rowH: 0.73 });
  T.banner(s, "숫자는 모두 원문 식 (4)의 μ · Σ에서 numpy로 다시 계산했습니다", { y: 6.12 });
}
// =============================================================== D01
{ const s = T.slide(); T.divider(s, { num: "01", title: "무엇을 풀려는가", page: ++P,
  sub: "질문 — 목적별 계정의 사고와 평균-분산 최적화를 합칠 수 있는가 · 원문 I절" }); }
// 04 계정으로 생각한다
{
  const s = T.slide();
  const cy = T.head(s, { title: "사람들은 자금을 목적별 계정으로 나눠 생각합니다", page: ++P,
    sub: "Shefrin–Statman(2000) 행동 포트폴리오 이론(BPT) — 계정마다 문턱 H와 미달 확률 α를 둔다" });
  figAt(s, "fig/s_accounts", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "MVT는 전체 포트폴리오에 γ 하나를 묻지만, γ를 분산 단위로 정확히 말하는 투자자는 드뭅니다" },
    { text: "논문의 질문 — 계정별 목표 언어를 평균-분산 최적화와 합칠 수 있는가", color: C.red }], { y: PY });
}
// 05 MVT vs MA
{
  const s = T.slide();
  const cy = T.head(s, { title: "MVT는 γ를, 심리계정은 계정마다 (H, α)를 입력으로 받습니다", page: ++P,
    sub: "원문 식 (1)–(3)과 식 (5) — 같은 자산 μ · Σ 위에서 묻는 질문만 다르다" });
  const hw = (CW - 0.40) / 2;
  eqCol(s, [{ key: "eq/mvt", cap: "MVT — 식 (1)·(2) 위험 조정 기대수익 최대" },
            { key: "eq/w3", cap: "닫힌 해 — 식 (3), 공매도 허용", kind: "dark" }], M, hw, cy + 0.04, FIG_BOT);
  eqCol(s, [{ key: "eq/ma", cap: "심리계정 — 식 (5) 미달 확률 한도 안에서 기대수익 최대" }], M + hw + 0.40, hw, cy + 0.04, cy + 1.66);
  textCard(s, M + hw + 0.40, cy + 1.86, hw, FIG_BOT - cy - 1.86, { kind: "white", cap: "투자자가 실제로 말하는 것",
    lines: ["은퇴 — 5% 확률로도 −10% 아래는 안 된다", "교육 — 15% 확률까지 −5% 아래 허용", { text: "γ 대신 문턱과 확률을 말한다", bold: true, color: C.teal }] });
  T.punch(s, [{ text: "MVT에서는 γ를 정하면 효율선 위 한 점이 정해지고, 심리계정에서는 (H, α)가 그 일을 합니다" },
    { text: "둘이 같은 점을 고른다면 계정의 언어를 그대로 최적화에 쓸 수 있습니다", color: C.red }], { y: PY });
}
// 06 세 결과
{
  const s = T.slide();
  const cy = T.head(s, { title: "논문은 문제 동치 · 합산 효율 · 작은 마찰 세 가지를 보입니다", page: ++P,
    sub: "원문 I절 주요 결과 i)–ii) · 가정: 투자자는 γ보다 문턱 · 확률을, 전체보다 계정 단위로 잘 말한다" });
  figAt(s, "fig/s_claims", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "①과 ②는 정규분포(또는 2차 효용)와 공매도 허용이 전제이고, ③은 공매도를 막았을 때의 비용입니다" },
    { text: "목표를 계정별로 말하게 해도 효율을 거의 잃지 않는다는 것이 결론입니다", color: C.red }], { y: PY });
}
// =============================================================== D02
{ const s = T.slide(); T.divider(s, { num: "02", title: "계정 하나와 손계산", page: ++P,
  sub: "질문 — 확률 제약을 평균 · 표준편차의 조건으로 어떻게 바꾸나 · 원문 III절 식 (5)–(6) · 강의본 34–36장" }); }
// 08 확률 → 분위수
{
  const s = T.slide();
  const cy = T.head(s, { title: "정규분포 아래 미달 확률 한도는 하위 분위수 조건이 됩니다", page: ++P,
    sub: "원문 식 (5)→(6) · 강의 표기 z는 −Φ⁻¹(α)로 양수 — α 5%면 1.645, 15%면 1.036, 20%면 0.842" });
  eqCol(s, [{ key: "eq/ineq6", cap: "식 (6) — 원문 표기, Φ는 표준정규 누적분포" },
            { key: "eq/zform", cap: "강의 표기 — 하위 α 분위수가 H 이상", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_ztail", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "하위 5% 수익률은 95% VaR의 경계이므로, (H, α) 제약은 ‘VaR가 −H 이하’와 같은 말입니다" },
    { text: "확률의 언어가 평균과 표준편차, 두 숫자의 부등식 하나로 줄어듭니다", color: C.red }], { y: PY });
}
// 09 자산 셋
{
  const s = T.slide();
  const cy = T.head(s, { title: "원 논문의 예는 가상 자산 셋으로 시작합니다", page: ++P,
    sub: "원문 식 (4) · 채권형 · 저위험 주식형 · 고위험 주식형 — 무위험 자산 없음, 공매도 허용" });
  figAt(s, "fig/s_data", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "계정 셋 — 은퇴 (−10%, 5%) · 교육 (−5%, 15%) · 상속 (−15%, 20%)을 모두 이 자산으로 풉니다" },
    { text: "이후의 모든 숫자는 이 μ와 Σ에서 다시 계산한 값입니다", color: C.red }], { y: PY });
}
// 10 손계산 ① 60·30·10
{
  const s = T.slide();
  const cy = T.head(s, { title: "채권 60 · 저위험 30 · 고위험 10은 은퇴 계정 조건을 통과합니다", page: ++P,
    sub: "은퇴 계정 H = −10%, α = 5% — 보충교재 4-2 단계 1 · 강의본 35장과 같은 손계산" });
  const w = 6.95;
  eqCol(s, [{ key: "eq/m60" }, { key: "eq/v60" }, { key: "eq/q60", kind: "dark" }, { key: "eq/p60" }], M, w, cy + 0.04, FIG_BOT, 0.14);
  figAt(s, "fig/c_check", M + w + 0.30, CW - w - 0.30, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "분산의 넷째 항 0.0012가 두 주식의 공분산 몫 — 그래서 표준편차는 9.06%입니다" },
    { text: "통과는 하지만 여유가 남습니다 — 기대수익을 더 올릴 수 있습니다", color: C.red }], { y: PY });
}
// 11 손계산 ② 두 자산
{
  const s = T.slide();
  const cy = T.head(s, { title: "두 자산이면 비중 하나를 조건에 딱 맞추면 됩니다", page: ++P,
    sub: "교육용 축소 — 채권형(5% · 5%)과 저위험 주식형(10% · 20%), 상관 0 · 은퇴 계정 (−10%, 5%)" });
  const w = 6.95;
  eqCol(s, [{ key: "eq/m2" }, { key: "eq/q2" }, { key: "eq/poly2" }, { key: "eq/root2", kind: "dark", wt: 1.5 }], M, w, cy + 0.04, FIG_BOT, 0.14);
  figAt(s, "fig/c_two", M + w + 0.30, CW - w - 0.30, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "w 0.5는 −9.46%로 통과, 0.6은 −12.01%로 위반 — 답은 52.2% (m 7.61% · σ 10.70%)" },
    { text: "음수 근 −26.8%는 버립니다 — 자산이 셋이면 같은 일을 행렬로 합니다", color: C.red }], { y: PY });
}
// =============================================================== D03
{ const s = T.slide(); T.divider(s, { num: "03", title: "행렬로 일반화", page: ++P,
  sub: "질문 — 자산이 n개일 때 (H, α)를 지키는 최선의 비중은 · 원문 II–III절 식 (1)–(8) · 부록 (A-1)–(A-8) · 강의본 37장" }); }
// 13 역행렬과 상수
{
  const s = T.slide();
  const cy = T.head(s, { title: "역행렬 하나에서 상수 A · B · C · D가 나옵니다", page: ++P,
    sub: "원문 각주 6의 기호 — 강의본 37장의 a · c와 같고, 강의의 K(= d)는 D를 C로 나눈 0.18399" });
  const yEnd = figAt(s, "fig/s_inv", M, CW, cy + 0.02, 4.62);
  const hw = (CW - 0.30) / 2;
  T.eqInCard(s, { x: M, w: hw + 0.6, y: 4.74, h: 1.08, kind: "ghost", path: img("eq/abcd"), ratio: rr("eq/abcd"), pad: 0.16 });
  T.eqInCard(s, { x: M + hw + 0.9, w: hw - 0.6, y: 4.74, h: 1.08, kind: "dark", path: img("eq/abcdn"), ratio: rr("eq/abcdn"), pad: 0.16 });
  T.punch(s, [{ text: "공분산이 블록 대각이라 역행렬도 채권 1/0.0025 = 400과 주식 2 × 2 블록으로 나뉩니다" },
    { text: "이 네 숫자만 있으면 효율선 전체를 식으로 쓸 수 있습니다", color: C.red }], { y: PY });
}
// 14 g + v/γ
{
  const s = T.slide();
  const cy = T.head(s, { title: "효율선의 해는 최소분산 g에 위험 방향 v를 1/γ만큼 더한 것입니다", page: ++P,
    sub: "원문 부록 (A-1) 라그랑주 함수 → (A-2)–(A-8) 1계 조건과 λ → 식 (3)을 두 조각으로(보충교재 4-2 단계 2)" });
  const w = 7.25;
  eqCol(s, [{ key: "eq/lag" }, { key: "eq/foc" }, { key: "eq/gv", kind: "dark" }], M, w, cy + 0.04, FIG_BOT, 0.16);
  textCard(s, M + w + 0.30, cy + 0.04, CW - w - 0.30, FIG_BOT - cy - 0.04, { kind: "white", cap: "두 재료 (채권 · 저위험 · 고위험)",
    lines: ["g — 93.9 · 5.6 · 0.5%", "v — −151.6 · 79.5 · 72.1%", "v의 성분 합은 0", { text: "γ가 작을수록 v를 더 섞는다", bold: true, color: C.teal }] });
  T.punch(s, [{ text: "g는 위험이 가장 작은 포트폴리오, v는 채권을 팔아 주식을 사는 ‘위험을 더 지는 방향’입니다" },
    { text: "모든 효율 포트폴리오가 같은 두 재료를 비율만 달리 섞습니다", color: C.red }], { y: PY });
}
// 15 m(γ), σ(γ)
{
  const s = T.slide();
  const cy = T.head(s, { title: "평균과 분산이 γ 하나의 함수로 정리됩니다", page: ++P,
    sub: "식 (3)을 대입한 효율선의 매개변수 표시 — 강의 표기 K는 원문 D를 C로 나눈 값" });
  eqCol(s, [{ key: "eq/msig", cap: "효율선을 γ로 쓰면" },
            { key: "eq/msign", cap: "이 예의 숫자", kind: "dark" }], M, 7.0, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_fgamma", M + 7.3, CW - 7.3, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "γ가 무한대면 최소분산(4.84%, 5.38%), γ가 작아질수록 효율선을 따라 오른쪽 위로 올라갑니다" },
    { text: "남은 일은 (H, α)가 고르는 γ를 찾는 것입니다", color: C.red }], { y: PY });
}
// 16 γ 방정식
{
  const s = T.slide();
  const cy = T.head(s, { title: "확률 제약을 등호로 거는 γ가 계정의 내재 위험회피도입니다", page: ++P,
    sub: "원문 식 (7)–(8) — 최적점에서 제약은 등호 · x를 1/γ로 두고 제곱(z 1.645) · 은퇴 계정 (−10%, 5%)" });
  eqCol(s, [{ key: "eq/eq7" }, { key: "eq/xform" }, { key: "eq/xroot", kind: "dark" }], M, 6.3, cy + 0.04, FIG_BOT, 0.16);
  figAt(s, "fig/c_vline", M + 6.6, CW - 6.6, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "제약 직선과 효율선이 만나는 점이 답이고, 효율선을 그보다 더 올라가면 조건을 어깁니다" },
    { text: "제곱으로 생긴 음수 근 −0.1415는 원래 식을 만족하지 않아 버립니다", color: C.red }], { y: PY });
}
// 17 은퇴 비중
{
  const s = T.slide();
  const cy = T.head(s, { title: "은퇴 계정은 채권 53.9 · 저위험 26.6 · 고위험 19.5%입니다", page: ++P,
    sub: "γ = 3.795를 식 (3)에 넣고 검산한다 — 원문 표 1 첫 열(0.53943 · 0.26562 · 0.19495)과 일치" });
  eqCol(s, [{ key: "eq/wret", cap: "비중 = 최소분산 + 0.2635 × 위험 방향" },
            { key: "eq/chkret", cap: "검산 — 하위 5%가 정확히 H", kind: "dark" }], M, 6.5, cy + 0.04, 5.40);
  figAt(s, "fig/c_wgamma", M + 6.8, CW - 6.8, cy + 0.04, 5.40);
  noteN(s, "※ 원문 p.320 본문의 γ₁ = 3.9750은 오기 — p.317과 표 1 · 2는 3.7950. 3.975를 넣으면 하위 5%가 −9.45%로 H = −10%를 맞추지 못한다", { y: 5.48 });
  T.punch(s, [{ text: "“5% 확률로도 −10% 아래는 안 된다”는 목표 언어가 γ = 3.795와 같은 말입니다", color: C.red }], { y: 6.10 });
}
// =============================================================== D04
{ const s = T.slide(); T.divider(s, { num: "04", title: "세 계정 · 합산 · 가능성", page: ++P,
  sub: "질문 — 계정마다 다른 γ를 합치면 효율을 잃는가, 목표는 애초에 가능한가 · 원문 III절 · 표 1–2 · 식 (9)–(19)" }); }
// 19 세 계정 표
{
  const s = T.slide();
  const cy = T.head(s, { title: "세 계정의 (H, α)는 γ 3.795 · 2.706 · 0.877로 번역됩니다", page: ++P,
    sub: "원문 표 1 재계산 — 비중은 채권 · 저위험 · 고위험 순, 계정마다 식 (7)을 따로 푼다" });
  T.dataTable(s, ["계정 (H, α)", "내재 γ", "비중 (%)", "기대수익률", "표준편차"], [
    ["은퇴 (−10%, 5%)", "3.795", "53.9 · 26.6 · 19.5", "10.23%", "12.30%"],
    ["교육 (−5%, 15%)", "2.706", "37.9 · 35.0 · 27.1", "12.18%", "16.57%"],
    ["상속 (−15%, 20%)", "0.877", "−78.9 · 96.2 · 82.7", "26.35%", "49.13%"],
  ], { y: cy + 0.05, rowH: 0.86, widths: [3.30, 1.70, 3.39, 1.70, 1.70], emph: 0 });
  T.note(s, "※ 원문 표 1 · 2와 소수 넷째 자리까지 일치(교육 고위험 0.27141 → 27.1%) · 상속의 채권 −78.9%는 공매도, 곧 차입이다", { y: 5.30, color: C.amber });
  T.punch(s, [{ text: "미달 기준이 느슨할수록(α가 크거나 H가 낮을수록) γ가 작아지고 주식이 늘어납니다" },
    { text: "상속 계정은 자기자금 100으로 주식 178.9를 삽니다 — 이름만 보고 안전하다고 판단하면 안 됩니다", color: C.red }], { y: PY });
}
// 20 효율선 위 세 계정 + 합산
{
  const s = T.slide();
  const cy = T.head(s, { title: "세 계정과 합산 포트폴리오가 모두 효율선 위에 있습니다", page: ++P,
    sub: "원문 그림 1 재현 — 계정 배분 은퇴 60 · 교육 20 · 상속 20%, 공매도 허용" });
  figAt(s, "fig/c_frontier3", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "합산 비중은 채권 24.2 · 저위험 42.2 · 고위험 33.7% — 기대수익률 13.84%, 표준편차 20.32%" },
    { text: "계정마다 따로 풀어도 합친 결과가 효율선에서 벗어나지 않습니다", color: C.red }], { y: PY });
}
// 21 γ 지도
{
  const s = T.slide();
  const cy = T.head(s, { title: "기준이 느슨할수록 내재 γ가 작아집니다", page: ++P,
    sub: "(H, α) 격자마다 식 (7)을 푼 내재 γ — 위로(α↑) · 왼쪽으로(H↓) 갈수록 γ가 작다" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "읽는 법",
    lines: ["α를 키우거나 H를 낮추면 γ가 작아진다", "γ가 작으면 v를 더 섞어 주식이 는다", "오른쪽 아래 빈칸은 불가능한 목표", { text: "같은 등고선 = 같은 포트폴리오", bold: true, color: C.teal }] });
  figAt(s, "fig/c_gmap", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "은퇴 3.795 → 교육 2.706 → 상속 0.877 — 목표가 느슨해지는 순서와 γ가 줄어드는 순서가 같습니다" },
    { text: "투자자는 γ를 말하지 않고 (H, α)를 말해도 효율선 위 한 점을 고릅니다", color: C.red }], { y: PY });
}
// 22 표 2 — 다대일
{
  const s = T.slide();
  const cy = T.head(s, { title: "같은 포트폴리오에 여러 (H, α)가 대응합니다", page: ++P,
    sub: "원문 표 2 재현 — 은퇴 계정은 (−10%, 5%)이면서 동시에 (0%, 20.3%)이다" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "손실 확률 (H = 0%) — 원문 20 · 23 · 30 · 25%",
    lines: ["은퇴 20.3% · 교육 23.1%", "상속 29.6% · 합산 24.8%", { text: "10% 넘게 잃을 확률 5%와", bold: true, color: C.teal }, { text: "손실 확률 5%는 전혀 다른 조건", bold: true, color: C.teal }] });
  figAt(s, "fig/c_table2", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "MVT 효율선의 점 하나가 여러 심리계정 효율선 위에 동시에 놓입니다 — 원문의 다대일 대응" },
    { text: "계정을 정한 뒤에는 다른 기준의 미달 확률도 함께 보고합니다", color: C.red }], { y: PY });
}
// 23 합산 γ
{
  const s = T.slide();
  const cy = T.head(s, { title: "합산 위험회피도는 γ의 산술평균이 아니라 역수의 가중평균입니다", page: ++P,
    sub: "각 계정이 g + v/γ 꼴이므로 합쳐도 같은 꼴 — 역수 가중은 강의 도출, 원문은 ‘가중평균과 다르다’고만 쓴다" });
  eqCol(s, [{ key: "eq/agg", cap: "계정 배분 a로 합치면" },
            { key: "eq/gtot", cap: "은퇴 60 · 교육 20 · 상속 20%", kind: "dark" }], M, 6.3, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_aggsd", M + 6.6, CW - 6.6, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "γ는 산술평균 2.994가 아닌 2.174, 표준편차는 가중평균 20.52%가 아닌 20.32%입니다" },
    { text: "합산 효율은 공매도 허용이 전제입니다 (원문 p.315 ii-b, pp.320–321)", color: C.red }], { y: PY });
}
// 24 Q max
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표가 가능한지는 하위 분위수의 최댓값으로 먼저 점검합니다", page: ++P,
    sub: "원문 식 (9)–(19) — 원문은 수치로 푼다, 닫힌 해와 −2.31%는 강의 계산(보충교재 4-2 단계 6)" });
  eqCol(s, [{ key: "eq/q10", cap: "식 (10)–(11) — 하위 분위수를 가장 높이는 포트폴리오" },
            { key: "eq/qclosed", cap: "효율선 위에서 미분하면 (α 5%)", kind: "dark" }], M, 6.0, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_qmax", M + 6.3, CW - 6.3, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "α 5%에서 만들 수 있는 하위 5% 수익률은 최대 −2.31%입니다 (채권 89.3 · 저위험 8.0 · 고위험 2.7%)" },
    { text: "H가 이보다 높으면 어떤 비중으로도 목표를 지킬 수 없습니다", color: C.red }], { y: PY });
}
// 25 대안
{
  const s = T.slide();
  const cy = T.head(s, { title: "원금 손실 확률 5% 이하는 이 자산들로는 불가능합니다", page: ++P,
    sub: "H = 0%, α = 5%는 0 > −2.31%라 불가능 — H · α · 자산 · 목표 가운데 하나를 고친다" });
  textCard(s, M, cy + 0.04, LW, FIG_BOT - cy - 0.04, { kind: "white", cap: "대안 넷 (재계산)",
    lines: ["H를 −3%로 — γ 11.94 · 기대 6.92%", "α를 11.7% 이상으로 — Roy 해", "현금 같은 안정 자산을 추가", "목표 금액 · 기간 · 저축을 조정"] });
  figAt(s, "fig/c_feas", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "H 0%를 지키는 가장 작은 α는 11.7% — 평균 대비 표준편차 배수가 가장 큰 Roy(1952) 포트폴리오의 값입니다" },
    { text: "목표가 불가능하면 비중이 아니라 질문을 다시 합니다", color: C.red }], { y: PY });
}
// =============================================================== D05
{ const s = T.slide(); T.divider(s, { num: "05", title: "롱온리와 강의 연결", page: ++P,
  sub: "질문 — 공매도를 막으면 얼마를 잃는가, 논문은 그 밖에 무엇을 보였나 · 원문 IV–VI절 · M8 단원 ③" }); }
// 27 롱온리 문제
{
  const s = T.slide();
  const cy = T.head(s, { title: "공매도를 막으면 닫힌 해 대신 γ 탐색과 QP로 풉니다", page: ++P,
    sub: "위 식 (20)–(24) 확률 제약 + 비중 하한 L · 상한 U → 아래 식 (25), w(γ)는 식 (26)–(29)의 선형 제약 QP 해" });
  eqCol(s, [{ key: "eq/lo20", pad: 0.12 }, { key: "eq/lo25", kind: "dark", pad: 0.12 }], M, CW, cy + 0.04, cy + 2.12, 0.14);
  figAt(s, "fig/s_qp", M, CW, cy + 2.24, FIG_BOT);
  T.punch(s, [{ text: "③이 아니면 γ를 옮겨 ②로 — 원문은 R의 quadprog, 수렴하지 않으면 그 (H, α)는 불가능입니다" },
    { text: "닫힌 해 g + v/γ는 공매도 허용일 때만 성립합니다", color: C.red }], { y: PY });
}
// 28 롱온리 손풀이
{
  const s = T.slide();
  const cy = T.head(s, { title: "롱온리 해는 음수 자산을 0에 묶고 남은 자산으로 다시 풉니다", page: ++P,
    sub: "상속 계정 (−15%, 20%), z 0.8416 — 무제약 해의 채권 −78.9% 위반 → 채권 0에 묶고 저위험 1 − w · 고위험 w로" });
  const w = 7.0;
  eqCol(s, [{ key: "eq/lo_m", pad: 0.10 }, { key: "eq/lo_q", pad: 0.10 }, { key: "eq/lo_poly", pad: 0.10 }, { key: "eq/lo_root", kind: "dark", wt: 1.4, pad: 0.12 }], M, w, cy + 0.04, 5.40, 0.12);
  figAt(s, "fig/c_lohand", M + w + 0.30, CW - w - 0.30, cy + 0.04, 5.40);
  noteN(s, "※ 음수 근 −24.3%는 범위 밖 · 등호 해가 100%를 넘으면 경계(w = 100%)가 조건을 지키는지 본다 · 계정별 롱온리 해는 원문에 없는 재계산(scipy 검산)", { y: 5.48 });
  T.punch(s, [{ text: "w 0.9는 −14.75% 통과, 1.0은 −17.08% 위반 → 0 · 8.9 · 91.1% (기대 23.67%, σ 45.94%)" },
    { text: "남은 비중이 모두 0 이상이면 끝, 아니면 묶기를 반복 — 자산이 많으면 SLSQP · 엑셀 해 찾기로 풉니다", color: C.red }], { y: 6.02 });
}
// 28b 롱온리 — 엑셀 해 찾기 · scipy
{
  const s = T.slide();
  const cy = T.head(s, { title: "롱온리는 엑셀 ‘해 찾기’ 대화창 하나로도 풉니다", page: ++P,
    sub: "같은 상속 계정 — ‘음이 아닌 수’ 체크 하나가 공매도 금지 · 같은 문제를 SLSQP로도 · 강의본 40장" });
  figAt(s, "fig/s_solver", M, CW, cy + 0.02, 5.40);
  noteN(s, "※ 한국어판 엑셀 · B8 행렬 곱은 365에서 그대로 Enter(구버전은 Ctrl + Shift + Enter) · 해법 GRG 비선형 · scipy 검산 0 · 8.893 · 91.107%, 하위 20% 경계 −15.00%", { y: 5.48 });
  T.punch(s, [{ text: "체크를 끄면 −78.9 · 96.2 · 82.7%(26.35%), 켜면 0 · 8.9 · 91.1%(23.67%)" },
    { text: "bounds = (0, 1)이 엑셀의 ‘음이 아닌 수’ 체크와 같습니다 — 자산이 많아도 같은 설정으로 풉니다", color: C.red }], { y: 6.02 });
}
// 29 롱온리 결과
{
  const s = T.slide();
  const cy = T.head(s, { title: "롱온리는 상속 계정만 바꾸고, 합산은 효율선보다 연 12bp 낮습니다", page: ++P,
    sub: "원문 그림 6 재현 — 은퇴 · 교육은 해가 원래 전부 양수라 그대로, 상속만 26.35% → 23.67%" });
  figAt(s, "fig/c_longonly", M, CW, cy + 0.02, 5.40);
  noteN(s, "※ 원문 p.328은 합산 13.31% · σ 19.89%로 쓰지만 재계산은 13.30% · 19.38% — σ 19.89%면 같은 σ의 효율선이 13.65%라 손실 12bp와 맞지 않아 오기로 보인다", { y: 5.48 });
  T.punch(s, [{ text: "합산 13.30% 대 같은 표준편차의 롱온리 효율선 13.43% → 손실 12bp (원문도 12bp)" },
    { text: "제약은 있지만 현실적으로 크지 않습니다", color: C.red }], { y: 6.02 });
}
// 30 합산 수준 vs 계정 수준
{
  const s = T.slide();
  const cy = T.head(s, { title: "공매도 금지를 합산 수준에만 걸면 이 예의 손실은 0입니다", page: ++P,
    sub: "원문 p.329 — 합산 포트폴리오에 공매도가 남을 때만 비효율이 생긴다" });
  T.pairPanels(s,
    { kind: "white", cap: "합산 수준에만 제약", bullets: ["무제약 합산 24 · 42 · 34%", "이미 모두 0 이상", "계정 해 그대로 사용"], foot: "손실 0" },
    { kind: "dark", cap: "계정마다 제약", bullets: ["상속만 0 · 8.9 · 91.1%", "합산 13.30% · σ 19.38%", "효율선 13.43%"], foot: "손실 12bp" },
    { y: cy + 0.05, h: 3.45, w: 5.40, arrow: false });
  T.punch(s, [{ text: "원문 두 단계 — ① 공매도 없는 계정은 그대로 둔다 ② 남은 한도 안에서 공매도 계정만 다시 최적화한다" },
    { text: "제약은 계정이 아니라 합산에 거는 것이 원문의 실무 권고입니다", color: C.red }], { y: PY });
}
// 31 오지정 손실
{
  const s = T.slide();
  const cy = T.head(s, { title: "γ를 잘못 말하는 손실이 공매도 제약 손실보다 큽니다", page: ++P,
    sub: "원문 IV절 표 3 — γ를 10 · 20 · 30% 위아래로 잘못 말할 때 확실성 등가 손실(bp, 두 방향 평균)" });
  eqCol(s, [{ key: "eq/loss", cap: "손실 — 확실성 등가의 차(강의 도출)" }], M, LW, cy + 0.04, cy + 1.40);
  textCard(s, M, cy + 1.56, LW, 5.40 - cy - 1.56, { kind: "white", cap: "원문 강건성 — 그림 7–9 · 각주 9",
    lines: ["샤프비율 손실 최악 약 6% · 평균 1% 미만", "실데이터 0.25% · Brunel(2006) 8bp"] });
  figAt(s, "fig/c_misspec", RX, RW, cy + 0.04, 5.40);
  noteN(s, "※ 표 3의 γ 0.877 행(5.29 · 23.15 · 44.22)은 재계산과 다르다 — 손실은 1/γ에 비례해 은퇴 행의 4.33배인 10.81 · 47.33 · 124.22가 맞다. 은퇴 · 교육 행은 일치", { y: 5.48 });
  T.punch(s, [{ text: "γ를 20%만 틀려도 11~47bp — 롱온리 마찰 12bp보다 크고, γ가 낮을수록 더 큽니다" },
    { text: "목표 언어로 γ를 정확히 끌어내는 이득이 마찰보다 큽니다 — 심리계정 방식의 핵심 근거", color: C.red }], { y: 6.02 });
}
// 32 심리계정 효율선 · 그림 3
{
  const s = T.slide();
  const cy = T.head(s, { title: "심리계정 효율선은 α에 볼록하고, H가 높으면 γ의 역할이 뒤집힙니다", page: ++P,
    sub: "왼쪽 원문 그림 2 · 4 재현(H 고정, α를 바꾼 효율선) · 오른쪽 원문 그림 3 재현(γ에 따른 미달 확률)" });
  const hw = (CW - 0.30) / 2;
  figAt(s, "fig/c_mafront", M, hw, cy + 0.04, 5.40);
  figAt(s, "fig/c_fig3", M + hw + 0.30, hw, cy + 0.04, 5.40);
  noteN(s, "※ 원문 그림 4 캡션은 H를 −5 · −10 · −20%로 적지만 상속 점 (−15%, 20%)은 −15% 선 위에 있어 −15%로 그렸다", { y: 5.48 });
  T.punch(s, [{ text: "H +5%는 γ↑에 미달 확률이 줄다 늘고, H +10%는 계속 늘어 효율 포트폴리오가 하나뿐입니다" },
    { text: "문턱이 최소분산 수익률 5.38%보다 높으면 안전 쪽으로 갈수록 목표에서 멀어집니다", color: C.red }], { y: 6.02 });
}
// 33 VaR · 가정 · BPT
{
  const s = T.slide();
  const cy = T.head(s, { title: "논문은 VaR 문헌과 BPT 사이에 이 틀을 놓습니다", page: ++P,
    sub: "원문 pp.312–315, 318–319, 331–332 — 연결 · 가정 · 제외한 것" });
  T.cards(s, [
    { kind: "white", cap: "VaR와의 관계", title: "같은 제약, 다른 표현",
      bullets: ["Alexander 외(2007): 효율선이 안쪽으로", "이 논문: 더 높은 내재 γ로", "Telser(1956) 안전우선과 동치"] },
    { kind: "white", cap: "두 가정", title: "말하기 쉬운 쪽으로 묻는다",
      bullets: ["γ보다 문턱 · 확률을", "전체보다 계정 단위로", "그래서 오지정이 준다"] },
    { kind: "dark", cap: "BPT와 다른 점", title: "위험추구는 뺐다",
      bullets: ["BPT의 복권형 계정 제외", "모든 계정이 위험회피", "후속 연구 과제로 남김"] },
  ], { y: cy + 0.05, h: 3.45 });
  T.punch(s, [{ text: "VaR 제약을 효율선의 손실로 보지 않고 위험회피도의 이동으로 읽는 것이 이 논문의 관점입니다" },
    { text: "그래서 목표 언어 · VaR · 평균-분산이 한 지도 위에 놓입니다", color: C.red }], { y: PY });
}
// 34 계보
{
  const s = T.slide();
  const cy = T.head(s, { title: "M8 방법 1과 방법 2는 Roy 안전우선의 쌍둥이입니다", page: ++P,
    sub: "강의본 60장 — 방법 1은 Kataoka(1963)형, 방법 2(이 논문)는 Telser(1956)형" });
  figAt(s, "fig/s_lineage", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "방법 1은 T년 뒤 자산으로 떼어 둘 자금 K를, 방법 2는 한 해 수익률로 계정 비중을 정합니다" },
    { text: "다른 것은 기간과 목적이고, 확률을 평균 · 변동성 조건으로 바꾸는 방식은 같습니다", color: C.red }], { y: PY });
}
// 35 공통 언어
{
  const s = T.slide();
  const cy = T.head(s, { title: "VaR · CPPI floor · 심리계정은 같은 ‘평균 − z × 변동성’ 언어를 씁니다", page: ++P,
    sub: "은퇴 계정 하나를 네 가지로 말한다 — 보충교재 9-3 · 정규분포 · 한 기간" });
  const w = 9.4;
  T.eqInCard(s, { x: M + (CW - w) / 2, w, y: cy + 0.04, h: 1.40, kind: "ghost", cap: "위험을 말하는 네 언어", path: img("eq/four"), ratio: rr("eq/four"), pad: 0.24 });
  T.statCards(s, [{ cap: "위험회피도 γ", value: "3.795" }, { cap: "변동성", value: "12.30%" },
    { cap: "1년 95% VaR", value: "10.0%" }, { cap: "목표 언어 (H, α)", value: "(−10%, 5%)" }], { y: cy + 1.70, h: 1.30 });
  T.punch(s, [{ text: "CPPI는 floor 위 쿠션으로, VaR 예산은 손실 한도로, 심리계정은 (H, α)로 같은 조건을 겁니다" },
    { text: "이사회에는 VaR 10%, 개인에게는 ‘5% 확률로도 −10% 아래는 안 된다’ — 같은 포트폴리오입니다", color: C.red }], { y: PY });
}
// 36 한계
{
  const s = T.slide();
  const cy = T.head(s, { title: "정규분포 · 한 기간 · 빈도 제약이라는 한계를 함께 읽습니다", page: ++P,
    sub: "원문 VI절의 확장 과제와 보충교재 4-2의 한계" });
  T.cards(s, [
    { kind: "white", cap: "분포와 기간", title: "정규 · 한 기간",
      bullets: ["꼬리가 두꺼우면 미달↑", "H는 1년 수익률 기준", "10년 목표는 따로 평가"] },
    { kind: "white", cap: "제약의 성격", title: "빈도만 막는다",
      bullets: ["미달의 크기는 무제한", "기대 부족분은 별도", "동적 전략은 틀 밖"] },
    { kind: "dark", cap: "원문의 확장 과제", title: "남은 질문",
      bullets: ["비정규 다변량 분포", "옵션형 상품", "노동 · 부동산 배경위험"] },
  ], { y: cy + 0.05, h: 3.45 });
  T.punch(s, [{ text: "바닥(필수 목표)은 floor · CPPI로, 그 위의 계정은 Das–Markowitz로 지키는 것이 M8의 조합입니다" },
    { text: "확률 제약은 빈도의 약속이지 크기의 약속이 아닙니다", color: C.red }], { y: PY });
}
// 37 한 장 요약
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표 언어에서 합산까지 다섯 단계와 점검 셋으로 정리됩니다", page: ++P,
    sub: "한 장 요약 — 숫자는 원 논문 예(가상 자산 셋 · 세 계정)의 재계산" });
  figAt(s, "fig/s_summary", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "은퇴 3.795 · 교육 2.706 · 상속 0.877 → 합산 2.174, 효율선 위 13.84% · 20.32%" },
    { text: "계정별로 묻고, 합산에서 점검합니다", color: C.red }], { y: PY });
}
// 38 마감
{
  const s = T.slide();
  T.closing(s, {
    statements: ["(H, α)는 γ와 같은 말입니다", "계정을 나눠도 효율선 위에 남습니다", "마찰은 수 bp, 오지정은 수십 bp입니다"],
    message: "목표는 계정별로 묻고\n비중은 계산이 정합니다",
    note: "출처: Das, Markowitz, Scheid, Statman (2010), Portfolio Optimization with Mental Accounts, JFQA 45(2), 311–334 · 수치는 원문 식 (4)의 μ · Σ에서 재계산(_build/dmss_deck)",
  });
  ++P;
}

T.save(OUT).then(f => console.log("saved", f, "slides", P));
