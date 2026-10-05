// GBI 요약·기초 제로원 덱 — W06 M8 GBI를 문제 → 핵심 수식 → 논리 전개로 요약한다.
// 실행: (assets.py 먼저) NODE_PATH=/Users/keerhee/Project/node_modules node build.js
const path = require("path");
process.chdir(__dirname);
const T = require("./template.js");
const R = require("./ratios.json");
const { C, M, CW } = T;
T.setBrand({ eyebrow: "BAF.60080 · W06 LDI와 GBI · GBI 요약", wordmark: "" });
const OUT = process.argv[2] || "GBI_Summary_Basics_zeroone.pptx";

let P = 0;
const _warn = console.warn; console.warn = (...a) => _warn(`[p${P}]`, ...a);
const rr = k => R[k];
const img = k => k + ".png";
const FIG_BOT = 5.82;

// 수식 카드 열: items [{key, cap, kind}] 을 [y0, bot] 안에 균등 배치
function eqCol(s, items, x, w, y0, bot, gap) {
  gap = gap == null ? 0.22 : gap;
  const h = (bot - y0 - gap * (items.length - 1)) / items.length;
  let y = y0;
  items.forEach(it => {
    T.eqInCard(s, { x, w, y, h, kind: it.kind || "ghost", cap: it.cap, path: img(it.key), ratio: rr(it.key), pad: 0.30 });
    y += h + gap;
  });
}
function figAt(s, key, x, w, y, bot) {
  return T.figImg(s, img(key), rr(key), { y, bottom: bot, left: x, w, quiet: true });
}
// 텍스트 카드: cap + 줄들
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
const LW = 5.15, RX = M + LW + 0.40, RW = CW - LW - 0.40;   // 좌 수식 열 · 우 그림

// =============================================================== 01 표지
{
  const s = T.slide();
  T.cover(s, { title: "목표기반투자(GBI)\n무엇을 풀고, 어떻게 배분하는가", titleSize: 34,
    sub: "목표를 값으로 재고 두 바구니로 나눕니다", org: "BAF.60080 · W06 LDI와 GBI · GBI 요약",
    chain: ["목표 G", "Floor F", "쿠션 × 승수", "달성 확률"] });
  ++P;
}
// =============================================================== 02 목차
{
  const s = T.slide();
  T.head(s, { title: "여섯 부로 문제 정의에서 한국 적용까지 이어 갑니다", page: ++P,
    sub: "각 부는 무엇을 풀려는가 → 핵심 수식 → 해석 순서로 쓴다" });
  T.agenda(s, [
    { num: "01", title: "무엇을 풀려는가", kicker: "위험 = 목표에 지각할 확률", desc: "같은 65세·5억 · 미달 확률 · 3계층 버킷" },
    { num: "02", title: "목표를 값으로 재기", kicker: "필요 자본 K와 Floor", desc: "가장 싼 포트폴리오 · Retirement Bond · 목표의 자" },
    { num: "03", title: "두 바구니로 나누기", kicker: "GHP + PSP, 쿠션 × 승수", desc: "CPPI · 승수 m · Cash Trap · Flexicure" },
    { num: "04", title: "확률로 말하는 목표", kicker: "확률의 말을 비중으로", desc: "심리계정 · 디지털 해 · 필수 + 희망 목표" },
    { num: "05", title: "은퇴 이후", kicker: "잔고가 아니라 소득", desc: "β · 상각형 인출 · 사망률 크레딧 · 요양 보험" },
    { num: "06", title: "한국에 대입", kicker: "조건부 승인 두 건", desc: "원리금보장의 덫 · 디폴트옵션 · H대학기금" },
  ], { y: 2.22, rowH: 0.615 });
  T.banner(s, "앞 부의 답이 다음 부의 질문이 됩니다 — 수식 유도는 도출 III 덱이 맡습니다", { y: 6.12 });
}
// =============================================================== 03 LDI에서 이어받는 것
{
  const s = T.slide();
  const cy = T.head(s, { title: "LDI의 문법이 그대로 개인의 목표 문제로 옮겨 옵니다", page: ++P,
    sub: "M7 LDI에서 이어받는 것 — 기관의 부채 자리에 개인의 목표가 들어선다" });
  figAt(s, "fig/s_bridge", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "자산 100 · 부채 80 · 잉여금 20의 기금이, 자산 10억 · Floor 5억 · 쿠션 5억의 개인이 됩니다" },
    { text: "지킬 것을 먼저 안전자산으로 복제하고 남는 자금으로 수익을 좇습니다", color: C.red }], { y: 5.98 });
}
// =============================================================== 04 디바이더 01
{ const s = T.slide(); T.divider(s, { num: "01", title: "무엇을 풀려는가", page: ++P,
  sub: "질문 — 은퇴 투자의 ‘최적해’는 누구의 최적해인가 · 강의본 단원 ①" }); }
// 05 같은 65세
{
  const s = T.slide();
  const cy = T.head(s, { title: "같은 65세·같은 5억이라도 목표가 다르면 답이 다릅니다", page: ++P,
    sub: "이순자 씨와 김영수 씨(가상 인물) — TDF·MVO라면 두 사람에게 같은 포트폴리오를 준다" });
  T.pairPanels(s,
    { kind: "white", cap: "이순자 씨 · 65세 · 5억 · 안정 최우선",
      bullets: ["국민연금 월 150만", "생활비 월 300만은 필수", "손주 교육은 여유가 되면"], foot: "Safety 목표가 먼저" },
    { kind: "dark", cap: "김영수 씨 · 65세 · 5억 · 성장 지향",
      bullets: ["임대 소득 월 200만", "기본 생활은 임대로 충분", "자녀 증여 · 세계여행"], foot: "Aspirational 목표가 크다" },
    { y: cy + 0.05, h: 3.50, w: 5.15, arrow: false });
  T.punch(s, [{ text: "DC 가입자에게 부채가 없는 것이 아니라 각자의 부채가 다릅니다" },
    { text: "GBI는 목표를 먼저 정의하고 그 목표에서 배분을 거꾸로 계산합니다", color: C.red }], { y: 5.98 });
}
// 06 위험 = 미달 확률
{
  const s = T.slide();
  const cy = T.head(s, { title: "위험은 변동성이 아니라 목표 미달 확률과 그 깊이로 잽니다", page: ++P,
    sub: "예 — 3억 목표에 균형형(연 4.5%·변동성 9%)으로 2.22억, 10년 뒤 자산의 분포" });
  eqCol(s, [{ key: "eq/risk1", cap: "미달 확률 — 얼마나 자주 지각하나" },
            { key: "eq/es", cap: "기대 부족분 — 지각하면 얼마나 모자라나", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_risk", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "변동성 9%는 이 목표를 이룰지 말해 주지 않고, 미달 확률 30% · 부족분 약 0.47억이 말해 줍니다" },
    { text: "실무는 몬테카를로 1,000회로 같은 확률을 셉니다", color: C.red }], { y: 5.98 });
}
// 07 3계층 버킷 + BPT
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표에 위계를 두고 계층마다 달성 확률을 따로 정합니다", page: ++P,
    sub: "행동 포트폴리오 이론(BPT) — Shefrin-Statman(2000), Thaler의 마음속 계좌(1985)" });
  eqCol(s, [{ key: "eq/bpt", cap: "계좌별 만족의 합 최대 · 계좌마다 확률 제약" }], M, LW, cy + 0.04, cy + 1.60);
  textCard(s, M, cy + 1.80, LW, FIG_BOT - cy - 1.80, { kind: "white", cap: "확률 한도 = 1 − 달성 확률",
    lines: ["Safety 5% · Market 30%", "Aspirational 70%", { text: "숫자는 비중이 아니라 확률이다", bold: true, color: C.teal }] });
  figAt(s, "fig/s_bucket", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "자금에 꼬리표를 붙이는 습관을 GBI는 계좌별 확률 제약으로 공학화합니다" },
    { text: "다음 — 확률 p로 목표를 이루려면 오늘 얼마를 떼어 둬야 하나", color: C.red }], { y: 5.98 });
}
// =============================================================== 디바이더 02
{ const s = T.slide(); T.divider(s, { num: "02", title: "목표를 값으로 재기", page: ++P,
  sub: "질문 — 목표 하나를 이루는 데 오늘 얼마가 드는가 · 강의본 단원 ③ · 도출 III 5-1·6-1" }); }
// 09 K 공식
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표의 값은 확률 p로 이루려고 오늘 떼어 둘 자금 K입니다", page: ++P,
    sub: "로그정규 가정 · m은 연 로그 성장률, z는 달성 확률의 표준정규 값 — 강의본 부록 B-1" });
  const w = 7.6;
  T.eqInCard(s, { x: M + (CW - w) / 2, w, y: cy + 0.04, h: 1.75, kind: "ghost",
    cap: "성장할 몫만큼 할인 · 확률 조건만큼 안전마진", path: img("eq/K"), ratio: rr("eq/K") });
  T.statCards(s, [{ cap: "Safety 6억 · 95% · GHP", value: "4.91억" }, { cap: "Market 3억 · 70% · GHP + 주식 67%", value: "2.24억" },
    { cap: "Aspirational 5억 · 30% · 주식", value: "1.97억" }], { y: cy + 2.00, h: 1.05 });
  T.note(s, "※ z값 — 95% → 1.645 · 70% → 0.524 · 30% → −0.524. p가 50% 미만이면 z가 음수라 변동성이 오히려 필요 자본을 줄인다",
    { y: cy + 3.22, color: C.amber });
  T.punch(s, [{ text: "55세 · 금융자산 10억 · 10년 뒤 은퇴 — 세 목표를 같은 공식 하나로 값을 매깁니다" },
    { text: "목표 금액과 확률은 개인이 정하고, 떼어 둘 자금은 계산이 정합니다", color: C.red }], { y: 5.98 });
}
// 10 아홉 칸
{
  const s = T.slide();
  const cy = T.head(s, { title: "확률 높은 목표는 GHP가, 낮은 목표는 주식이 가장 쌉니다", page: ++P,
    sub: "목표 × 포트폴리오 아홉 칸의 필요 자본 K(억, 실질) — GHP 2%·균형형 4.5%/9%·주식 6%/20%" });
  figAt(s, "fig/c_nine", M, CW, cy + 0.02, 5.46);
  T.note(s, "※ Market의 균형형 2.22억은 후보 비교 — 본문 계산은 공식 비중(GHP + 주식 67%) 2.24억 · 합쳐 보면 주식 43% · 채권·GHP 57%",
    { y: 5.56, color: C.amber });
  T.punch(s, [{ text: "목표마다 공식 비중으로 사면 4.91 + 2.24 + 1.97 = 9.13억, 남는 0.87억은 꿈의 계좌로 갑니다" },
    { text: "배분 49 / 22 / 28은 입력이 아니라 결과입니다", color: C.red }], { y: 5.98 });
}
// 11 최적 비중
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표별 주식 비중은 Merton 비중에서 확률 안전마진을 뺀 값입니다", page: ++P,
    sub: "GHP와 주식을 섞는다 — 초과수익 6%·변동성 20%·10년, 미분 유도는 강의본 부록 B-5" });
  eqCol(s, [{ key: "eq/gp", cap: "필요 자본 최소 = 확률 조정 성장률 최대" },
            { key: "eq/wstar", cap: "1계 조건 — 교과서 비중 − 확률 조정", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_wstar", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "95%는 0%(전액 GHP), 70%는 67%(GHP와 혼합, K 2.24억), 30%는 100%(전액 주식)입니다" },
    { text: "앞 장의 ‘가장 싼 포트폴리오’와 같은 답이 미분으로도 나옵니다", color: C.red }], { y: 5.98 });
}
// 12 Floor = RB 가격
{
  const s = T.slide();
  const cy = T.head(s, { title: "Floor는 필수 소득을 오늘 시장에서 사는 값, 곧 Retirement Bond 가격입니다", page: ++P,
    sub: "실질 연 2,400만 원 × 25년을 물가연동국채 금리로 할인한다 — 도출 III 6-1" });
  eqCol(s, [{ key: "eq/floorRB", cap: "Floor = 필수 소득의 연금현가" },
            { key: "eq/rb45", cap: "젊을수록 싸다 — 연 2,400만 원 × 20년, 실질 2%", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_floor", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "금리가 오르면 Floor가 내려가 쿠션이 저절로 늘어납니다 (1.5% 4.97억 → 2.5% 4.42억)" },
    { text: "낙관 할인율 3.5%를 쓰면 Floor가 1억 작아 보여 위험을 더 삽니다", color: C.red }], { y: 5.98 });
}
// 13 목표의 자
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표의 자로 재면 현금이 흔들리고 목표 채권(GHP)이 고정됩니다", page: ++P,
    sub: "10년 뒤 1억 목표 · 금리 4%에서 목표 가격 6,756만 · 가진 자금 5,000만 — 도출 III 5-3·5-4" });
  eqCol(s, [{ key: "eq/atilde", cap: "목표 확보율 — 목표의 몇 %를 확실히 사나" }], M, LW, cy + 0.04, cy + 1.85);
  textCard(s, M, cy + 2.05, LW, FIG_BOT - cy - 2.05, { kind: "dark", cap: "명목 원금보장의 함정 (5-4)",
    lines: ["15년 목표, 금리 5% → 2%", { text: "현금의 확보율 100% → 65%", bold: true, color: C.lime }] });
  figAt(s, "fig/c_numeraire", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "원화로 재면 현금이 안전해 보이지만 목표로 재면 GHP만이 무위험 자산입니다" },
    { text: "보장의 기준은 원금이 아니라 목표입니다", color: C.red }], { y: 5.98 });
}
// =============================================================== 디바이더 03
{ const s = T.slide(); T.divider(s, { num: "03", title: "두 바구니로 나누기", page: ++P,
  sub: "질문 — Floor를 지키면서 위험은 얼마나 질 수 있는가 · 강의본 단원 ④⑤ · 도출 III 3절" }); }
// 15 두 바구니
{
  const s = T.slide();
  const cy = T.head(s, { title: "목표를 복제하는 GHP와 수익을 좇는 PSP, 두 바구니로 나눕니다", page: ++P,
    sub: "Retirement Bond는 발행하는 나라가 거의 없어 GHP로 복제하고 그 값을 Floor로 쓴다" });
  const yEnd = figAt(s, "fig/s_chain", M, CW, cy + 0.02, cy + 1.85);
  const w = 6.8;
  T.eqInCard(s, { x: M + (CW - w) / 2, w, y: yEnd + 0.20, h: FIG_BOT - yEnd - 0.20, kind: "ghost",
    cap: "목표 확보율을 흔드는 것은 PSP 대 GHP 하나뿐 (도출 III 5-2)", path: img("eq/dA"), ratio: rr("eq/dA"), pad: 0.28 });
  T.punch(s, [{ text: "GHP만 들면 확보율은 금리와 무관하게 고정되고, 남는 위험은 PSP의 초과 성과뿐입니다" },
    { text: "다음 — PSP에는 쿠션의 몇 배를 넣어야 하나", color: C.red }], { y: 5.98 });
}
// 16 CPPI
{
  const s = T.slide();
  const cy = T.head(s, { title: "위험자산을 쿠션의 m배로 두면 1/m 미만의 급락에는 Floor가 지켜집니다", page: ++P,
    sub: "Black-Jones(1987) CPPI와 같은 식 · F = 5억, 레버리지 금지로 상한 100% — 도출 III 3-1~3-4" });
  eqCol(s, [{ key: "eq/cppi", cap: "쿠션 공식 — 금액 E와 비중" },
            { key: "eq/cppicond", cap: "위험자산이 x만큼 떨어질 때 Floor가 지켜지는 조건", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_cppi", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "자산이 Floor에 가까워질수록 위험자산은 규칙에 따라 자동으로 줄어듭니다" },
    { text: "쿠션은 ‘잃어도 되는 자금’ — 예측도 감정도 필요 없습니다", color: C.red }], { y: 5.98 });
}
// 17 m 정하기
{
  const s = T.slide();
  const cy = T.head(s, { title: "승수 m은 급락 상한과 효용 기준 중 작은 값으로 정합니다", page: ++P,
    sub: "‘자산의 80%’처럼 임의로 잡지 않는다 — 견딜 손실 L과 위험회피도로 정한다 · 도출 III 3-5" });
  const w = 6.2;
  T.eqInCard(s, { x: M, w, y: cy + 0.04, h: FIG_BOT - cy - 0.04, kind: "ghost", cap: "두 상한 중 작은 값",
    path: img("eq/mrule"), ratio: rr("eq/mrule") });
  const x2 = M + w + 0.40, w2 = CW - w - 0.40;
  textCard(s, x2, cy + 0.04, w2, 1.80, { kind: "white", cap: "① 급락 상한 — 견딜 손실 L",
    lines: ["월 99% VaR 약 12% → m 8", "하루 −20%(1987) → m 5", { text: "−25% 급락 → m 4", bold: true }] });
  textCard(s, x2, cy + 2.00, w2, FIG_BOT - cy - 2.00, { kind: "dark", cap: "② 효용 기준 (Merton)",
    lines: ["초과수익 4% · 변동성 18% · γ 0.5", { text: "→ m 약 2.5", bold: true, color: C.lime }] });
  T.punch(s, [{ text: "작은 값을 고른 뒤 마지막은 몬테카를로로 Safety ≥ 95% · Market ≥ 70%를 맞춥니다" },
    { text: "m은 철학의 숫자가 아니라 산수의 숫자입니다", color: C.red }], { y: 5.98 });
}
// 18 m 민감도
{
  const s = T.slide();
  const cy = T.head(s, { title: "m이 크면 중위 자산은 늘지만 최악은 나빠지고 Cash Trap에 갇힙니다", page: ++P,
    sub: "실습 Step 5 — 이순자 씨 65→75세 · 1,000 경로 · 출발 Floor 3.50억 → 75세 2.13억" });
  figAt(s, "fig/c_msens", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "m 3이면 Cash Trap 1.4% · Floor 위반 0%, m 6이면 Cash Trap 20.7% · 위반 1.9%" },
    { text: "갇힐 확률이 m의 진짜 비용입니다", color: C.red }], { y: 5.98 });
}
// 19 Flexicure
{
  const s = T.slide();
  const cy = T.head(s, { title: "Flexicure는 Floor를 매년 다시 잡아 Cash Trap을 피합니다", page: ++P,
    sub: "EDHEC(2018) — 매년 초 Floor를 자산의 80%로, 승수는 나이별 TDF 주식 비중 ÷ 0.2" });
  const w = 6.6;
  T.eqInCard(s, { x: M + (CW - w) / 2, w, y: cy + 0.04, h: 1.60, kind: "ghost",
    cap: "재설정 직후 쿠션 = 자산의 20% → 비중 = 승수 × 0.2", path: img("eq/flexi"), ratio: rr("eq/flexi") });
  T.dataTable(s, ["1년 뒤 (자산 10 · Floor 8 · m 3, PSP 60% 출발)", "재설정 Floor", "재설정 후 PSP", "재설정 안 하면"],
    [["벌었을 때 자산 11.5", "9.2 (이익 잠금)", "60%", "91%"], ["잃었을 때 자산 8.5", "6.8", "60%", "18% — Cash Trap 근접"]],
    { y: cy + 1.78, rowH: 0.66, widths: [4.2, 2.2, 1.9, 3.49], emph: 1 });
  T.punch(s, [{ text: "45세 m 3, 65세 m 1 · 대가는 보호 수준이 해마다 움직인다는 것입니다" },
    { text: "보호하는 것은 절대 금액이 아니라 ‘한 해 손실 20% 이내’입니다", color: C.red }], { y: 5.98 });
}
// =============================================================== 디바이더 04
{ const s = T.slide(); T.divider(s, { num: "04", title: "확률로 말하는 목표", page: ++P,
  sub: "질문 — 지금 자금으로 확보할 수 없는 희망 목표는 무엇으로 관리하나 · 도출 III 4–5절" }); }
// 21 Das-Markowitz
{
  const s = T.slide();
  const cy = T.head(s, { title: "확률의 말 (H, α)는 위험회피도 γ로 그대로 번역됩니다", page: ++P,
    sub: "Das-Markowitz-Scheid-Statman(2010) — 계정마다 최소 수익률 H와 확률 한도 α만 묻는다" });
  T.eqInCard(s, { x: M, w: 7.6, y: cy + 0.04, h: 1.25, kind: "ghost", cap: "정규분포에서 확률 제약 = 하위 α 분위수가 H 이상",
    path: img("eq/dm"), ratio: rr("eq/dm"), pad: 0.26 });
  textCard(s, M + 8.0, cy + 0.04, CW - 8.0, 1.25, { kind: "dark", cap: "공매도 허용 · 60 · 20 · 20 합산",
    lines: [{ text: "전체 γ 2.174 (역수 가중)", bold: true, color: C.lime }] });
  T.dataTable(s, ["계정", "최소 수익률 · 확률 한도", "γ", "채권 · 저위험 · 고위험 주식"],
    [["은퇴", "−10% · 5%", "3.795", "53.9 · 26.6 · 19.5%"], ["교육", "−5% · 15%", "2.706", "37.9 · 35.0 · 27.1%"],
     ["상속", "−15% · 20%", "0.877", "−78.9 · 96.2 · 82.7%"]],
    { y: cy + 1.36, rowH: 0.50, widths: [1.9, 3.6, 1.9, 4.39], emph: 0 });
  T.note(s, "※ 롱온리면 상속만 0 · 8.9 · 91.1%(기대 23.67%) — 계정별로 막으면 합산 연 12bp 손실, 합산 수준에서만 막으면 0 (도출 III 4-2)",
    { y: 5.56, color: C.amber });
  T.punch(s, [{ text: "기준이 느슨할수록 γ가 작고 주식이 많으며, 공매도 허용 시 합쳐도 γ 2.174의 효율적 해입니다" },
    { text: "계정을 나눠 관리해도 효율은 거의 잃지 않습니다", color: C.red }], { y: 5.98 });
}
// 22 디지털 해
{
  const s = T.slide();
  const cy = T.head(s, { title: "희망 목표만 보면 최적해는 ‘시장이 좋으면 전액, 아니면 0’입니다", page: ++P,
    sub: "미래 4상황(확률 25%씩) · 예산 50 · 희망 목표 100 — 도출 III 5-5·5-6" });
  eqCol(s, [{ key: "eq/digital", cap: "확률 극대화의 해 — 디지털 콜옵션" },
            { key: "eq/browne", cap: "최대 달성 확률 — Browne(1999)", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_digital", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "같은 확률이면 싼 상황의 쿠폰부터 사고, 목표에 못 미치는 금액은 확률을 올리지 못합니다" },
    { text: "대가 — 자금이 가장 필요한 폭락 때 0을 받습니다", color: C.red }], { y: 5.98 });
}
// 23 필수 + 희망
{
  const s = T.slide();
  const cy = T.head(s, { title: "필수 목표는 Floor로 지키고 희망 목표는 승수 m으로 조절합니다", page: ++P,
    sub: "학자금 1억(10년 뒤) · 필수 0.6 · 희망 1.2 · 자산 5,000만 · 금리 4% — 도출 III 5-7" });
  eqCol(s, [{ key: "eq/ess", cap: "Floor = 필수 목표의 가격 (만 원)" },
            { key: "eq/cppiA", cap: "확보율로 쓴 CPPI — m 3이면 PSP 57%", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_essasp", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "바닥을 지키는 대가로 희망 목표 확률은 82%에서 약 14%로 내려가고, m 3–4에서 가장 높습니다" },
    { text: "확률을 더 올리려면 m이 아니라 바닥·저축·기간을 고칩니다", color: C.red }], { y: 5.98 });
}
// =============================================================== 디바이더 05
{ const s = T.slide(); T.divider(s, { num: "05", title: "은퇴 이후 — 소득·인출·요양", page: ++P,
  sub: "질문 — 은퇴 뒤에는 무엇을 지키고 얼마씩 꺼내 쓰나 · 도출 III 6–8절" }); }
// 25 소득과 β
{
  const s = T.slide();
  const cy = T.head(s, { title: "은퇴자의 목표는 잔고가 아니라 평생 소득이며 그 값은 β로 잽니다", page: ++P,
    sub: "45세 · 20년 뒤 은퇴 · 20년 지급 · 자산 3억 · 목표 연 1,800만 원 — 도출 III 6-1·6-2·8-4" });
  eqCol(s, [{ key: "eq/beta", cap: "β = 매년 1원 소득의 가격 · 개인 적립비율" }], M, LW, cy + 0.04, cy + 1.85);
  textCard(s, M, cy + 2.05, LW, FIG_BOT - cy - 2.05, { kind: "dark", cap: "실질금리 2% → 1% (β 11.22 → 14.94)",
    lines: ["현금 보유자 적립비율 149% → 112%", { text: "RB 보유자 149% → 149%", bold: true, color: C.lime }] });
  figAt(s, "fig/c_income", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "금리가 1%로 내리면 현금 3억의 잔고는 그대로지만 살 수 있는 소득은 25% 줄어듭니다" },
    { text: "소득 기준의 안전자산은 현금이 아니라 Retirement Bond입니다", color: C.red }], { y: 5.98 });
}
// 26 인출
{
  const s = T.slide();
  const cy = T.head(s, { title: "남은 자산을 β로 나눠 꺼내 쓰면 파산 대신 소득이 줄어듭니다", page: ++P,
    sub: "시퀀스 리스크 — 자산 100, 매년 30 인출, −50%와 +50%가 한 번씩 · 도출 III 7-1·7-2" });
  eqCol(s, [{ key: "eq/seq", cap: "인출기의 자산 — 빼기가 끼어 순서가 결과를 가른다" },
            { key: "eq/amort", cap: "상각형 인출 · 필수 소득은 RB 사다리로 확정", kind: "dark" }], M, LW, cy + 0.04, FIG_BOT);
  figAt(s, "fig/c_seq", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "같은 수익률이라도 불황이 먼저 오면 고정 인출은 2년 만에 파산합니다" },
    { text: "필수 소득은 확정하고 나머지만 상각형으로 쓰면 변동은 하한 위에서만 생깁니다", color: C.red }], { y: 5.98 });
}
// 27 장수·요양
{
  const s = T.slide();
  const cy = T.head(s, { title: "장수 꼬리는 늦게 시작하는 연금, 요양 꼬리는 보험으로 싸게 덮습니다", page: ++P,
    sub: "사망률 크레딧과 보험료 비교 — 숫자는 예시 · 도출 III 7-3·8-1~8-3" });
  const g = T.grid(2, 0.41);
  T.eqInCard(s, { x: g[0].x, w: g[0].w, y: cy + 0.04, h: 1.85, kind: "ghost", cap: "생존자 1인당 수익 — 사망률 q만큼 더 받는다",
    path: img("eq/mort"), ratio: rr("eq/mort") });
  T.eqInCard(s, { x: g[1].x, w: g[1].w, y: cy + 0.04, h: 1.85, kind: "ghost", cap: "요양 꼬리의 보험료 (억) — 비용률 θ 30%",
    path: img("eq/ltc"), ratio: rr("eq/ltc") });
  textCard(s, g[0].x, cy + 2.08, g[0].w, FIG_BOT - cy - 2.08, { kind: "white", cap: "시장금리 2%일 때 생존자 수익률",
    lines: ["65세 개시 (q 0.6%) → 2.6%", { text: "85세 개시 (q 4.5%) → 6.8%", bold: true, color: C.teal }] });
  textCard(s, g[1].x, cy + 2.08, g[1].w, FIG_BOT - cy - 2.08, { kind: "dark", cap: "5년 이상 요양 3억 · 확률 8%",
    lines: ["현금 버퍼 3억을 묶어 둔다", { text: "보험료 약 0.31억으로 덮는다", bold: true, color: C.lime }] });
  T.punch(s, [{ text: "연금화는 소액·후기·꼬리 전용으로, 요양은 꼬리만 보험·나머지는 목표화된 예비 자산으로 둡니다" },
    { text: "확률은 낮고 금액이 큰 꼬리는 쌓기보다 사는 편이 쌉니다", color: C.red }], { y: 5.98 });
}
// =============================================================== 디바이더 06
{ const s = T.slide(); T.divider(s, { num: "06", title: "한국에 대입", page: ++P,
  sub: "질문 — 이 언어로 한국의 두 안건에 어떻게 표결하나 · 강의본 단원 ⑦⑧⑩ · 케이스 1·2부" }); }
// 29 원리금보장의 덫
{
  const s = T.slide();
  const cy = T.head(s, { title: "한국 퇴직연금의 덫은 원리금보장 쏠림과 목표 인식의 부재입니다", page: ++P,
    sub: "2025년 말 공시 — 금감원 투자백서 · 고용노동부 (케이스 1부 브리핑)" });
  T.txt(s, "2025년 수익률", { x: M, y: cy + 0.02, w: 6, h: 0.34, fontSize: 16, bold: true, color: C.muted });
  T.barsH(s, [{ label: "원리금보장", value: 3.09, shown: "3.09%", color: C.muted },
    { label: "퇴직연금 전체", value: 6.47, shown: "6.47%", color: C.blue },
    { label: "실적배당", value: 16.8, shown: "16.80%", color: C.teal }], { y: cy + 0.50, rowH: 0.80, barW: 3.9, max: 16.8 });
  T.insightBox(s, { x: M + CW - 4.5, y: cy + 0.04, w: 4.5, h: FIG_BOT - cy - 0.04, cap: "적립금 501조 원의 쏠림",
    blocks: [{ title: "원리금보장 비중 75.4%", desc: "퇴직연금 전체 · 디폴트옵션 안정형은 85.4%" },
             { title: "안정형 583만 명", desc: "디폴트옵션 지정 가입자의 79.4%" }] });
  T.punch(s, [{ text: "가입자 열에 여덟이 3.09%를 고르고, 은퇴 목표액을 묻는 질문 자체가 없습니다" },
    { text: "GBI의 한국적 가치는 ‘목표를 묻는 것’에서 시작합니다", color: C.red }], { y: 5.98 });
}
// 30 케이스 1
{
  const s = T.slide();
  const cy = T.head(s, { title: "디폴트옵션 Flexicure는 세 조건을 붙여 조건부 승인합니다", page: ++P,
    sub: "케이스 1부 — Floor 90% · m ≤ 2 · 총보수 ≤ 0.5% · 표준 가입자 55→65세 · 4,000 경로" });
  eqCol(s, [{ key: "eq/case1", cap: "결정 규칙 — Floor는 GHP 가격(금리 연동)" }], M, LW, cy + 0.04, cy + 1.75);
  textCard(s, M, cy + 1.95, LW, FIG_BOT - cy - 1.95, { kind: "dark", cap: "조건 ③ 수수료 후 Market 달성 (임계 70%)",
    lines: ["총보수 0.5% → 73% · 0.8% → 67%", { text: "1.5% → 51% — 수수료가 판을 가른다", bold: true, color: C.lime }] });
  figAt(s, "fig/c_case1", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "m 3은 Safety 미달 10.0%로, Floor 100%는 쿠션이 얇아 Market 70%를 못 넘겨 탈락합니다" },
    { text: "총보수를 0.5% 이하로 못 만들면 답은 부결입니다", color: C.red }], { y: 5.98 });
}
// 31 케이스 2
{
  const s = T.slide();
  const cy = T.head(s, { title: "H대학기금은 Yale 모델 대신 비유동 20%로 조건부 승인합니다", page: ++P,
    sub: "케이스 2부 · 4팀 과제 — 기본 답(비유동 20 · 유동 30 · 지출 4.5%) = B안 주식 50 · 국채 25 · 현금 5 · 사모 20" });
  eqCol(s, [{ key: "eq/case2", cap: "지출 규칙 — 80/20 평활" }], M, LW, cy + 0.04, cy + 1.75);
  textCard(s, M, cy + 1.95, LW, FIG_BOT - cy - 1.95, { kind: "dark", cap: "Flexicure — (주식 + 사모) ÷ 쿠션 ≤ 2",
    lines: ["B안 m 1.42 → 2008형 충격 뒤 1.53 통과", "C안 m 2.41 → 충격 뒤 4.2 탈락",
      { text: "x = 충격 뒤에도 m ≤ 2인 최대치", bold: true, color: C.lime }] });
  figAt(s, "fig/c_case2", RX, RW, cy + 0.04, FIG_BOT);
  T.punch(s, [{ text: "Yale형(비유동 60%)은 충격 아래 2년 만에 팔 수 없는 자산을 팔아야 하고 인력도 1명뿐입니다" },
    { text: "시간지평이 배분을 정합니다 — 영구 지평은 현금흐름이 받칠 때만 영구입니다", color: C.red }], { y: 5.98 });
}
// 32 방법 지도
{
  const s = T.slide();
  const cy = T.head(s, { title: "무엇을 위험으로 보느냐가 쓸 방법과 손잡이를 정합니다", page: ++P,
    sub: "방법 지도 — 이 덱의 각 부와 도출 III의 절을 잇는다 (도출 III 9-6)" });
  figAt(s, "fig/s_map", M, CW, cy + 0.02, FIG_BOT);
  T.punch(s, [{ text: "변동성이면 고정 비중, 확률이면 심리계정, 바닥이면 CPPI, 소득이면 Flexicure입니다" },
    { text: "유도가 필요하면 오른쪽 열의 도출 III 절로 갑니다", color: C.red }], { y: 5.98 });
}
// 33 한 장 요약
{
  const s = T.slide();
  const cy = T.head(s, { title: "기관은 부채를, 개인은 목표를 같은 두 바구니로 지킵니다", page: ++P,
    sub: "한 장 요약 — 위는 기관(LDI)과 개인(GBI)의 대비, 아래는 GBI의 핵심 식 세 줄" });
  const yS = figAt(s, "fig/s_summary", M, CW, cy + 0.02, cy + 2.45);
  const g3 = T.grid(3, 0.30), yE = yS + 0.14;
  ["eq/s_K", "eq/s_cppi", "eq/s_inc"].forEach((k, i) =>
    T.eqInCard(s, { x: g3[i].x, w: g3[i].w, y: yE, h: FIG_BOT - yE, kind: "white", path: img(k), ratio: rr(k), pad: 0.14 }));
  T.punch(s, [{ text: "목표의 값 K로 재고, 쿠션의 m배를 PSP에 두고, 소득은 개인 적립비율로 봅니다" },
    { text: "IC에서는 수익률이 아니라 Floor · 쿠션 · 달성 확률로 말합니다", color: C.red }], { y: 5.98 });
}
// =============================================================== 마감
{
  const s = T.slide();
  T.closing(s, { statements: ["목표가 다르면 포트폴리오도 다르다.", "Floor는 필수 목표의 시장가, 쿠션만큼 위험을 진다.",
    "확률과 소득의 언어로 표결한다."], message: "수식 유도는\n도출 III 덱으로",
    note: "※ 숫자는 강의본·케이스·도출 III의 교육용 가상 예시(이순자 씨·H대 등)이며, 한국 퇴직연금 수치는 2025년 말 공시를 따른다" });
  ++P;
}
T.save(OUT).then(f => console.log("saved", f, "slides", P));
