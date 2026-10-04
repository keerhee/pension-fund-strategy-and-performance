/* W06 LDI(M7) 요약·기초 — 제로원 덱
 * 실행(이 폴더에서): <python> assets.py && NODE_PATH=/Users/keerhee/Project/node_modules node build.js
 * 결과: ./LDI_Summary_Basics_zeroone.pptx (경로는 이 스크립트 기준 상대)
 */
const path = require("path");
const T = require("./template.js");
const { C, M, CW } = T;
const EQ = require("./eq/ratios.json"), FIG = require("./fig/ratios.json");
const eqp = k => ({ path: path.join(__dirname, "eq", k + ".png"), ratio: EQ[k] });
const fgp = k => ({ path: path.join(__dirname, "fig", k + ".png"), ratio: FIG[k] });

T.setBrand({ eyebrow: "BAF.60080 · W06 LDI와 GBI · LDI 요약", wordmark: "" });
let pg = 1;
const S = () => T.slide();
const H = (s, o) => T.head(s, Object.assign({ page: ++pg }, o));
const eqCard = (s, k, o) => T.eqInCard(s, Object.assign({ pad: 0.22 }, eqp(k), o));
const PUNCH_Y = 6.02;
const P = (s, lines) => T.punch(s, lines, { y: PUNCH_Y, gap: 0.44 });
const RED = t => ({ text: t, color: C.red });
const LW = 5.30, GAP = 0.36;                     // 좌 수식 열 · 우 차트
const RX = M + LW + GAP, RW = CW - LW - GAP;

/** 좌측 해설 카드: cap + 불릿 줄. 16pt 하한을 지키고 넘치면 경고한다. */
function info(s, x, y, w, h, cap, lines, o) {
  o = o || {};
  T.card(s, x, y, w, h, o.kind || "white");
  const dark = o.kind === "dark";
  let cy = y + 0.20;
  if (cap) {
    T.txt(s, cap, { x: x + 0.30, y: cy, w: w - 0.60, h: 0.30, fontSize: 14, bold: true,
      color: dark ? C.lime : C.teal, valign: "middle" });
    cy += 0.40;
  }
  const bw = w - 0.70, wrapW = bw - 0.40;
  let fs = 17;
  const nl = f => lines.reduce((a, b) => a + Math.max(1, Math.ceil(T.wUnits(b) * f / 72 / wrapW)), 0);
  const availH = y + h - 0.18 - cy;
  while (fs > 16 && nl(fs) * (fs / 72) * 1.40 > availH) fs -= 0.5;
  if (nl(fs) * (fs / 72) * 1.40 > availH)
    console.warn(`[info] "${cap}" ${nl(fs)}줄이 ${availH.toFixed(2)}in에 안 들어갑니다`);
  T.txt(s, lines.map(b => ({ text: b, options: { bullet: { code: "2022" }, breakLine: true } })),
    { x: x + 0.32, y: cy, w: bw, h: availH, fontSize: fs, color: dark ? C.white : C.body,
      valign: "top", lineSpacingMultiple: 1.22 });
  return y + h;
}
/** 좌 수식·해설 + 우 차트 */
function rightFig(s, k, top, bot) {
  const f = fgp(k);
  return T.figImg(s, f.path, f.ratio, { y: top, bottom: bot || 5.82, x: undefined, left: RX, w: RW });
}
/** 전체폭 그림 + punch */
function figBody(s, k, top, bot) {
  const f = fgp(k);
  return T.figImg(s, f.path, f.ratio, { y: top, bottom: bot || 5.98 });
}

/* 01 표지 */
T.cover(S(), {
  title: "부채연계투자(LDI)\n무엇을 풀고, 어떻게 막는가",
  sub: "부채를 재고, 막고, 남은 예산으로 번다",
  org: "BAF.60080 · W06 LDI와 GBI · 요약과 기초",
  chain: ["부채 측정", "듀레이션 갭", "헤지 세 가지", "위험 예산"],
});

/* 02 목차 */
{ const s = S(); const cy = H(s, { title: "여섯 부로 문제에서 한국 적용까지 이어 갑니다",
    sub: "앞 부의 답이 다음 부의 질문이 된다 — 유도는 옆의 도출 II 덱이 맡는다" });
  const rows = [
    ["01", "무엇을 풀려는가", "성적표는 자산 대 부채", "적립비율 · 잉여금 · 현재가치"],
    ["02", "재는 도구", "금리 1%p에 얼마나", "듀레이션 · DV01 · 갭 · 볼록성"],
    ["03", "막는 방법", "면역화와 헤지 세 가지", "사다리 · 장기채 · 스왑"],
    ["04", "막다가 깨지는 곳", "가치와 현금은 따로", "2022 영국 · 2023 SVB"],
    ["05", "남은 예산으로 수익을", "두 블록과 위험 예산", "PSP·LHP · 한도 · 트리거"],
    ["06", "한국에 대입", "국민연금 LDI 케이스", "두 눈금 · 안 A/B/C · GBI로"],
  ];
  const y0 = cy + 0.06, rh = 0.58;
  rows.forEach(([n, t, k, d], i) => {
    const y = y0 + i * rh;
    T.txt(s, n, { x: M, y, w: 0.7, h: rh - 0.08, fontSize: 20, bold: true, color: C.muted, valign: "middle" });
    T.hline(s, M + 0.75, y + (rh - 0.08) / 2, 0.80, i === rows.length - 1 ? C.lime : C.hair, 2.5);
    T.txt(s, t, { x: M + 1.80, y, w: 3.40, h: rh - 0.08, fontSize: 20, bold: true, color: C.body, valign: "middle" });
    T.txt(s, k, { x: M + 5.30, y, w: 3.20, h: rh - 0.08, fontSize: 16, bold: true, color: C.teal, valign: "middle" });
    T.txt(s, d, { x: M + 8.55, y, w: 3.24, h: rh - 0.08, fontSize: T.fitFs(d, 3.18, 15, 13), color: C.muted, valign: "middle" });
    if (i < rows.length - 1) T.hline(s, M, y + rh - 0.04, CW, C.hair, 1);
  }); }

/* ===== 1부 ===== */
T.divider(S(), { num: "01", title: "무엇을 풀려는가", page: ++pg,
  sub: "연기금의 성적표는 자산 수익률이 아니라 자산 대 부채다" });

{ const s = S(); const cy = H(s, { title: "자산이 7.5% 올랐는데도 나쁜 해가 될 수 있습니다",
    sub: "할인율이 3%에서 2%로 내려 부채가 15% 늘어난 해의 회의실이다" });
  T.pairPanels(s,
    { cap: "운용역의 보고", title: "자산 +7.5%", bullets: ["모든 자산군 상승", "벤치마크 초과", "수익률 표로는 좋은 해"],
      foot: "자산 수익률의 언어" },
    { kind: "dark", cap: "이사회의 질문", title: "부채는 +15%", bullets: ["할인율 3% → 2%", "같은 약속이 더 무거움", "적립비율은 하락"],
      foot: "자산 대 부채의 언어" },
    { y: cy, h: 3.62, w: 4.90, centerLabel: "같은 해" });
  P(s, ["같은 해의 잉여금 수익률은 −4.5%입니다 (도출 II 2-1).",
        RED("연기금의 성적표는 수익률이 아니라 자산 대 부채입니다.")]); }

{ const s = S(); const cy = H(s, { title: "부채는 앞으로 줄 금액을 오늘 값으로 할인해 더한 값입니다",
    sub: "자산은 매일 관찰되지만 부채는 할인율로 추정될 뿐이다" });
  const y1 = eqCard(s, "pv", { y: cy, h: 1.45, w: LW, x: M, kind: "ghost", cap: "부채의 현재가치 (도출 II 1-1)" });
  info(s, M, y1 + 0.16, LW, 5.82 - y1 - 0.16, "숫자로 확인", [
    "3년간 매년 30, 할인율 4% → 83.25",
    "20년 뒤 100: 5%면 37.7, 3%면 55.4",
    "할인율 2%p 차이에 부채 1.47배",
  ]);
  rightFig(s, "c_pv", cy);
  P(s, ["먼 약속일수록 할인율에 크게 흔들립니다 — 연금은 아주 먼 약속입니다.",
        RED("어떤 할인율(자)을 쓰느냐가 부채의 크기를 정합니다.")]); }

{ const s = S(); const cy = H(s, { title: "부채는 장기채를 공매도한 것과 같은 음(−)의 포지션입니다",
    sub: "가상 기금 — 자산 100 · 부채 80 · 적립비율 125%, 이후 계산은 모두 이 기금으로 한다" });
  figBody(s, "s_balance", cy);
  P(s, [RED("부채를 무시하는 것은 거대한 공매도 포지션을 무시하는 것입니다.")]); }

{ const s = S(); const cy = H(s, { title: "성적표는 적립비율과 잉여금 수익률 두 숫자입니다",
    sub: "자산 100 · 부채 80에서 자산 +7%, 부채 +10%인 해 (강의본 1교시)" });
  const g = T.grid(3, 0.30);
  eqCard(s, "fr", { y: cy, h: 1.70, x: g[0].x, w: g[0].w, kind: "ghost", cap: "적립비율 · 잉여금" });
  eqCard(s, "dfr", { y: cy, h: 1.70, x: g[1].x, w: g[1].w, kind: "ghost", cap: "1년 뒤 적립비율의 변화" });
  eqCard(s, "rs", { y: cy, h: 1.70, x: g[2].x, w: g[2].w, kind: "dark", cap: "잉여금 수익률" });
  T.statCards(s, [
    { cap: "새 적립비율 (정확)", value: "121.6%" },
    { cap: "근사식", value: "121.25%" },
    { cap: "잉여금", value: "20 → 19" },
    { cap: "잉여금 수익률", value: "−1%" },
  ], { y: cy + 1.98, h: 1.10 });
  P(s, ["7%를 벌고도 적립비율은 125%에서 121.6%로 내려갔습니다.",
        RED("좋은 해는 부채보다 많이 번 해입니다.")]); }

/* ===== 2부 ===== */
T.divider(S(), { num: "02", title: "재는 도구", page: ++pg,
  sub: "듀레이션 · DV01 · 듀레이션 갭 · 볼록성 — 금리가 움직일 때 무엇이 얼마나 움직이나" });

{ const s = S(); const cy = H(s, { title: "듀레이션은 금리 1%p에 가치가 몇 % 변하는지를 잽니다",
    sub: "현재가치로 가중한 평균 지급 시점이다 (도출 II 1-2)" });
  const y1 = eqCard(s, "dur", { y: cy, h: 1.50, w: 8.4, x: M + (CW - 8.4) / 2, kind: "ghost", cap: "듀레이션과 금리 민감도" });
  T.cards(s, [
    { cap: "가상 기금 자산", title: "약 3년", sub: "주식 · 채권 · 대체 혼합" },
    { cap: "가상 기금 부채", title: "약 20년", sub: "지급이 5~40년에 분산" },
    { kind: "dark", cap: "국민연금 순부채", title: "35년", sub: "원화 자산은 0.85년" },
  ], { y: y1 + 0.22, h: 1.66, gap: 0.30 });
  P(s, ["부채 세 덩어리(5년 20 · 20년 30 · 30년 30)의 가중평균 지급 시점이 20년입니다.",
        RED("자산과 부채의 듀레이션 차이, 갭이 위험의 원천입니다.")]); }

{ const s = S(); const cy = H(s, { title: "금리가 1%p 내리면 잉여금 20 중 13이 사라집니다",
    sub: "듀레이션 공식을 자산과 부채에 따로 쓰고 뺀다 (도출 II 2-2)" });
  const y1 = eqCard(s, "gap", { y: cy, h: 1.25, w: LW, x: M, kind: "dark", cap: "잉여금 변화 — 금액 듀레이션 갭" });
  info(s, M, y1 + 0.16, LW, 5.82 - y1 - 0.16, "가상 기금, 금리 1%p 하락", [
    "자산 100 → 103 (듀레이션 3)",
    "부채 80 → 96 (듀레이션 20)",
    "괄호 300 − 1,600 = −1,300",
    "적립비율 125% → 107%",
  ]);
  rightFig(s, "c_gap", cy);
  P(s, ["잉여금이 65% 줄었습니다 — 이 차이를 듀레이션 갭 −17년이 만듭니다.",
        RED("금리 하락은 숨은 공매도의 손실로 돌아옵니다.")]); }

{ const s = S(); const cy = H(s, { title: "DV01은 금리 1bp에 몇 원이 움직이는지를 금액으로 보여 줍니다",
    sub: "크기가 다른 자산과 부채를 같은 단위(원)로 비교하는 도구다" });
  const y1 = eqCard(s, "dv01", { y: cy, h: 1.45, w: 7.4, x: M + (CW - 7.4) / 2, kind: "ghost", cap: "금리 1bp당 가치 변화" });
  T.statCards(s, [
    { cap: "자산 DV01 (3 × 100)", value: "0.03" },
    { cap: "부채 DV01 (20 × 80)", value: "0.16" },
    { cap: "1bp당 잉여금 변화", value: "−0.13" },
    { cap: "국민연금 부채 DV01", value: "7.4조/bp" },
  ], { y: y1 + 0.30, h: 1.20 });
  P(s, ["금리가 1bp 내릴 때마다 잉여금이 0.13씩, 100bp면 13 줄어듭니다.",
        RED("부채 DV01이 자산의 다섯 배가 넘는 것이 이 기금의 문제입니다.")]); }

{ const s = S(); const cy = H(s, { title: "금리가 크게 움직이면 볼록성이 두 번째 항으로 끼어듭니다",
    sub: "10년 뒤 100을 주는 부채, 금리 5% 연속복리 — 가치 60.65 · D 10 · C 100" });
  const y1 = eqCard(s, "conv", { y: cy, h: 1.35, w: LW, x: M, kind: "ghost", cap: "기울기(듀레이션) + 휘어짐(볼록성)" });
  info(s, M, y1 + 0.16, LW, 5.82 - y1 - 0.16, "읽는 법", [
    "1차만 쓰면 오를 때 손실은 과대",
    "내릴 때 이익은 과소평가",
    "부채는 근사보다 더 오른다",
  ]);
  rightFig(s, "c_conv", cy);
  P(s, ["부채 D 20에 금리 −2%p면 듀레이션만으로는 약 10%p를 놓칩니다 (도출 II 1-3).",
        "그래서 면역화 조건에는 볼록성 항이 들어갑니다."]); }

/* ===== 3부 ===== */
T.divider(S(), { num: "03", title: "막는 방법", page: ++pg,
  sub: "헤지 비율 · Redington 면역화 · 실무 헤지 세 가지(현금흐름 매칭 · 장기채 · 스왑과 버퍼)" });

{ const s = S(); const cy = H(s, { title: "헤지 비율은 부채의 금리 민감도를 얼마나 덮었는지 보여 줍니다",
    sub: "헤지 비율 100%면 금리가 움직여도 잉여금이 거의 변하지 않는다" });
  const y1 = eqCard(s, "h", { y: cy, h: 1.80, w: LW, x: M, kind: "dark", cap: "헤지 비율 (도출 II 3-0)" });
  eqCard(s, "hnps", { y: y1 + 0.16, h: 5.82 - y1 - 0.16, w: LW, x: M, kind: "ghost", cap: "국민연금 — 자산 DV01 ÷ 부채 DV01 (조/bp)" });
  rightFig(s, "c_hedge", cy);
  P(s, ["가상 기금은 19%, 국민연금은 2.1%만 덮고 있습니다.",
        RED("막는다는 것은 자산 DV01을 부채 DV01까지 올리는 일입니다.")]); }

{ const s = S(); const cy = H(s, { title: "Redington 세 조건은 잉여금 곡선의 골짜기 바닥 조건입니다",
    sub: "Redington(1952) 면역화 — 증명은 도출 II 3-2 · 강의본 부록 B-3" });
  [["red1", "① 지급 능력", "출발선 맞추기", "ghost"],
   ["red2", "② 1차 항 = 0", "금액 듀레이션 일치", "ghost"],
   ["red3", "③ 2차 항 ≥ 0", "볼록성 우위", "dark"]].forEach(([k, a, b, kind], i) => {
    const y = cy + i * 1.20, h = 1.10, dk = kind === "dark";
    T.card(s, M, y, LW, h, kind);
    T.txt(s, a, { x: M + 0.26, y: y + 0.16, w: 2.40, h: 0.38, fontSize: 17, bold: true, color: dk ? C.lime : C.teal, valign: "middle" });
    T.txt(s, b, { x: M + 0.26, y: y + 0.56, w: 2.40, h: 0.36, fontSize: 16, color: dk ? C.white : C.muted, valign: "middle" });
    const e = eqp(k);
    T.figImg(s, e.path, e.ratio, { y: y + 0.12, bottom: y + h - 0.12, left: M + 2.70, w: LW - 2.85, quiet: true });
  });
  rightFig(s, "c_red", cy);
  P(s, ["같은 현재가치 60.65로 금리 −2%p: 바벨은 +0.37, 5년물 하나는 −7.05입니다.",
        RED("자산 현금흐름이 부채보다 시간상 더 퍼져 있어야 합니다.")]); }

{ const s = S(); const cy = H(s, { title: "실무 헤지는 현금흐름 매칭, 장기채, 스왑 순서로 DV01을 채웁니다",
    sub: "가상 기금이 헤지 비율 100%를 목표로 할 때, 주식 50은 수익 추구로 남긴다 (도출 II 3-4)" });
  figBody(s, "s_three", cy);
  P(s, ["0.01 + 0.06 + 0.09 = 부채 DV01 0.16 — 앞 단계가 모자랄 때만 다음 단계로 갑니다.",
        RED("순서가 곧 안전장치입니다.")]); }

{ const s = S(); const cy = H(s, { title: "가까운 지급은 사다리로, 긴 구간은 장기채로 덮습니다",
    sub: "방법 ① 현금흐름 매칭과 방법 ② 장기채 DV01 매칭 (도출 II 3-1 · 3-2)" });
  T.txt(s, "헤지 100%에 필요한 금액 (자산 100 대비)", { x: M, y: cy, w: 5.9, h: 0.36, fontSize: 16, bold: true, color: C.teal, valign: "middle" });
  T.barsH(s, [
    { label: "중기채 D 7", value: 229, shown: "229", color: C.red },
    { label: "30년 국채 D 20", value: 80, shown: "80", color: C.teal },
    { label: "50년 국채 D 30", value: 53, shown: "53", color: C.teal },
  ], { y: cy + 0.42, rowH: 0.52, barX: M + 2.10, barW: 2.70, valueW: 0.90 });
  info(s, M, cy + 2.04, 5.70, 5.82 - cy - 2.04, "한계 — 공급", [
    "30·50년 국고채 잔액 437조",
    "국민연금 순부채 2,122조",
  ]);
  const ex = M + 6.10, ew = CW - 6.10;
  const y1 = eqCard(s, "cf", { y: cy, h: 1.55, w: ew, x: ex, kind: "ghost", cap: "① 그 해 지급액만큼 그 해 만기 국채" });
  eqCard(s, "whedge", { y: y1 + 0.16, h: 5.82 - y1 - 0.16, w: ew, x: ex, kind: "ghost", cap: "② 필요 헤지 비중 — 아래첨자 H는 헤지 채권" });
  P(s, ["중기채로는 자산의 두 배가 넘게 필요해 불가능합니다.",
        RED("현물로 모자라는 몫을 채우는 것이 방법 ③ 스왑입니다.")]); }

{ const s = S(); const cy = H(s, { title: "스왑은 자금 없이 듀레이션을 빌리고 대가로 현금 증거금을 냅니다",
    sub: "고정금리 수취 스왑 — 헤지 노출 80 · 듀레이션 20 · 헤지 자본 K (도출 II 3-3)" });
  const y1 = eqCard(s, "margin", { y: cy, h: 1.45, w: LW, x: M, kind: "ghost", cap: "변동증거금" });
  eqCard(s, "buffer", { y: y1 + 0.16, h: 5.82 - y1 - 0.16, w: LW, x: M, kind: "dark", cap: "버틸 수 있는 금리 상승폭과 레버리지 상한" });
  rightFig(s, "c_buffer", cy);
  P(s, ["레버리지 2배면 250bp, 3배면 약 167bp에서 헤지 자본이 바닥납니다.",
        RED("듀레이션 20이면 250bp 기준의 레버리지 상한은 2배입니다.")]); }

/* ===== 4부 ===== */
T.divider(S(), { num: "04", title: "막다가 깨지는 곳", page: ++pg,
  sub: "2022 영국 LDI는 버퍼를, 2023 SVB는 DV01 매칭을 빠뜨렸다" });

{ const s = S(); const cy = H(s, { title: "2022년 영국에서는 마진콜이 매도를, 매도가 마진콜을 불렀습니다",
    sub: "레버리지 LDI의 악순환(doom loop) — 유도는 도출 II 4-1" });
  const y1 = eqCard(s, "loop", { y: cy, h: 1.22, w: LW, x: M, kind: "dark", cap: "판 만큼 금리가 더 오른다" });
  info(s, M, y1 + 0.16, LW, 5.82 - y1 - 0.16, "경과 (강의본 3교시)", [
    "9/23 미니예산 — £45B 감세",
    "30년 Gilt 나흘 새 +1%p 이상",
    "9/28 BOE £65B 매입 발표",
    "실매입 £19.3B · 손실 추정 £150B",
  ]);
  rightFig(s, "s_loop", cy);
  P(s, ["개별적으로 합리적인 매도가 모이면 시장이 무너집니다.",
        RED("이후 기준은 250bp 버퍼와 5영업일 재충전입니다.")]); }

{ const s = S(); const cy = H(s, { title: "SVB는 반대 방향의 갭으로 같은 현금 시험에서 무너졌습니다",
    sub: "2022년 말 채권 1,170억 달러 — 듀레이션 6년 · 금리 +2.5%p는 손계산용 가정치" });
  const y1 = eqCard(s, "svb", { y: cy, h: 1.45, w: 6.6, x: M + (CW - 6.6) / 2, kind: "ghost", cap: "예금 듀레이션 ≈ 0이면 자산 듀레이션이 그대로 갭" });
  T.statCards(s, [
    { cap: "장기 국채 · MBS", value: "1,170억 달러" },
    { cap: "듀레이션 (가정)", value: "6년" },
    { cap: "금리 상승 (가정)", value: "+2.5%p" },
    { cap: "손계산 평가손실", value: "약 176억 달러" },
  ], { y: y1 + 0.30, h: 1.20 });
  P(s, ["공시 평가손실 150억 달러 이상과 거의 같고, 자기자본에 맞먹는 규모였습니다.",
        RED("듀레이션 갭은 어느 쪽으로 열려도 위험합니다.")]); }

{ const s = S(); const cy = H(s, { title: "금리 위험은 가치와 현금으로 두 번 잽니다",
    sub: "너무 열심히 헤지한 연금과 헤지하지 않은 은행 — 거울상의 두 사건 (도출 II 4-3)" });
  figBody(s, "s_mirror", cy);
  P(s, [RED("매달 DV01 갭(가치)과 금리 +250bp 시 필요 현금(유동성)을 함께 보고합니다.")]); }

/* ===== 5부 ===== */
T.divider(S(), { num: "05", title: "남은 예산으로 수익을", page: ++pg,
  sub: "두 블록 최적해 · 위험 예산 · 적립비율 트리거 — 헤지 비율을 감이 아니라 규칙으로 정한다" });

{ const s = S(); const cy = H(s, { title: "잉여금 최적화의 해는 PSP와 LHP 두 블록으로 갈라집니다",
    sub: "Sharpe–Tint(1990) 잉여금 평균-분산 — 유도는 도출 II 5-1 · 5-2" });
  const y1 = eqCard(s, "obj", { y: cy, h: 1.40, w: 7.2, x: M + (CW - 7.2) / 2, kind: "ghost", cap: "목적 — 자산이 아니라 잉여금의 평균-분산" });
  eqCard(s, "wstar", { y: y1 + 0.18, h: 1.90, w: 9.6, x: M + (CW - 9.6) / 2, kind: "dark", cap: "최적 비중 = 투기적 수요(PSP) + 헤지 수요(LHP)" });
  P(s, ["PSP 몫에는 부채가 없고, LHP 몫에는 기대수익도 위험회피도 없습니다.",
        RED("운용팀은 두 블록을 만들고, 이사회는 섞는 비율 하나를 정합니다.")]); }

{ const s = S(); const cy = H(s, { title: "헤지 몫은 DV01 매칭과 정확히 같습니다",
    sub: "한 요인 모형 — 주식 기대초과수익 4% · 변동성 15% · 위험회피 3.6, 30년 국채 D 20 (도출 II 5-2)" });
  const y1 = eqCard(s, "wb", { y: cy, h: 1.45, w: 9.0, x: M + (CW - 9.0) / 2, kind: "ghost", cap: "헤지 몫 — 장기채 DV01 = 부채 DV01" });
  T.dataTable(s, ["몫", "계산", "자산 대비"], [
    ["주식 (PSP)", "4% ÷ (3.6 × 0.0225)", "49% ≈ 50%"],
    ["30년 국채 (LHP)", "20 ÷ (1.25 × 20)", "80%"],
    ["합계", "모자라는 30%는 스왑", "130%"],
  ], { y: y1 + 0.08, rowH: 0.50, widths: [3.0, 5.6, 3.19], emph: 2 });
  P(s, ["주식 50 · 30년 국채 50 · 스왑 명목 30이 이 최적해의 실무 구현입니다 (도출 II 3-3).",
        RED("감으로 정한 듯한 '헤지 100%'는 최적화의 답입니다.")]); }

{ const s = S(); const cy = H(s, { title: "헤지 비율을 올리면 같은 위험 예산에서 주식 한도가 늘어납니다",
    sub: "주식 변동성 15% · 금리 변동성 0.8%p · 이사회의 잉여금 변동성 한도 9% (도출 II 6-1 · 6-2)" });
  const y1 = eqCard(s, "sigs", { y: cy, h: 1.30, w: LW, x: M, kind: "dark", cap: "잉여금 변동성 — 주식 몫과 헤지 안 된 금리 몫" });
  info(s, M, y1 + 0.16, LW, 5.82 - y1 - 0.16, "숫자로 확인 (주식 50%)", [
    "헤지 19% → 100%: 변동성 12.8% → 7.5%",
    "한도 9%: 헤지 44%면 주식 36%",
    "헤지 100%면 주식 60%",
  ]);
  rightFig(s, "c_budget", cy);
  P(s, ["보상 없이 지던 금리 위험을 지우면 그 예산을 주식에 쓸 수 있습니다.",
        RED("LDI는 보상 없는 위험을 보상 있는 위험으로 바꾸는 기술입니다.")]); }

{ const s = S(); const cy = H(s, { title: "트리거는 적립비율이 오를 때마다 헤지를 계단식으로 올립니다",
    sub: "좋아진 만큼 잠근다 — 미리 정하고, 넘으면 자동 실행한다 (도출 II 7-1)" });
  T.dataTable(s, ["적립비율", "헤지", "주식", "방법"], [
    ["100% 미만", "50%", "60%", "① + ②"],
    ["110%", "70%", "55%", "② 확대"],
    ["120%", "90%", "50%", "③ + 버퍼"],
    ["135% 이상", "100%", "35%", "지키기"],
  ], { y: cy, rowH: 0.74, widths: [1.75, 1.05, 1.05, 1.45], emph: 3 });
  rightFig(s, "c_trigger", cy);
  P(s, ["지금 125%인 가상 기금은 헤지 90% · 주식 50% 계단에 있습니다.",
        RED("헤지를 올리는 단계마다 스왑 버퍼 점검을 다시 합니다.")]); }

/* ===== 6부 ===== */
T.divider(S(), { num: "06", title: "한국에 대입", page: ++pg,
  sub: "국민연금 LDI 케이스 — 적립비율의 두 눈금 · 안 A/B/C · 기본 답, 그리고 GBI로" });

{ const s = S(); const cy = H(s, { title: "국민연금 적립비율은 어느 자로 재느냐에 따라 95%와 69%로 갈립니다",
    sub: "2026~2071년 순유출(급여 − 보험료)의 현재가치를 부채로 본다 (W06 M7 케이스)" });
  info(s, M, cy, LW, 5.82 - cy, "케이스 숫자 (교육용 추계)", [
    "순부채 2,122조 (국채 곡선 기준)",
    "부채 수정 듀레이션 35년",
    "원화 자산 듀레이션 0.85년",
    "갭 약 −34년 · 부채 DV01 7.4조/bp",
    "현행 헤지 비율 2.1%",
  ]);
  rightFig(s, "c_nps", cy);
  P(s, ["금리가 100bp 내리면 국채 눈금 적립비율은 69%에서 49%로 떨어집니다.",
        RED("판정 조건 ① — 갭은 실재합니다.")]); }

{ const s = S(); const cy = H(s, { title: "안 C는 시장·버퍼·지침에서, 안 A는 갭 측정에서 탈락합니다",
    sub: "판정 조건 ① 갭 실재 ② 시장 수용 ③ 버퍼 ④ 허들 5.5% ⑤ 지침 (모범답안)" });
  T.dataTable(s, ["안", "헤지 · 수단", "시장 수용", "증거금 · 유동자산", "판정"], [
    ["안 A · 현행", "3% · 현 보유 채권", "해당 없음", "해당 없음", "탈락 ①"],
    ["안 B · 현물", "5% · 30년물 131조", "상한 131조 이내", "증거금 0", "조건부 승인"],
    ["안 C · IRS", "30% · 명목 1,223조", "상한의 4.1배", "401조 vs 123조", "탈락 ②③⑤"],
  ], { y: cy, rowH: 0.98, widths: [2.05, 2.95, 2.45, 2.45, 1.89], emph: 1 });
  P(s, ["안 B도 갭을 −34년에서 −33년으로 1년 줄일 뿐입니다.",
        RED("의결문에는 남는 갭 95%를 보험료와 재정이 진다고 적습니다.")]); }

{ const s = S(); const cy = H(s, { title: "식 여덟 줄이 LDI의 문제 여덟 개를 풉니다",
    sub: "식은 결과만 둔다 — 유도는 도출 II의 해당 절에서 한다" });
  const items = [
    ["pv", "부채의 크기", "1-1"], ["rs", "성적표", "2-1"],
    ["gap", "금리 위험의 크기", "2-2"], ["h", "헤지 비율", "3-0"],
    ["red2", "면역화 1차 조건", "3-2"], ["buffer", "버퍼와 레버리지", "3-3"],
    ["wstar", "두 블록 최적해", "5-2"], ["sigs", "위험 예산", "6-1"],
  ];
  const g = T.grid(2, 0.25), rh = 0.84, gp = 0.06;
  items.forEach(([k, name, sec], i) => {
    const x = g[i % 2].x, w = g[i % 2].w, y = cy + Math.floor(i / 2) * (rh + gp);
    T.card(s, x, y, w, rh, "ghost");
    T.txt(s, name, { x: x + 0.20, y: y + 0.08, w: 2.10, h: 0.40, fontSize: 16, bold: true, color: C.body, valign: "middle" });
    T.txt(s, "도출 II " + sec, { x: x + 0.20, y: y + 0.46, w: 2.10, h: 0.30, fontSize: 14, color: C.teal, valign: "middle" });
    const e = eqp("sm_" + k);
    T.figImg(s, e.path, e.ratio, { y: y + 0.06, bottom: y + rh - 0.06, left: x + 2.35, w: w - 2.50, quiet: true });
  });
  P(s, [RED("모든 식은 '부채 대비'라는 같은 뼈대 위에 있습니다.")]); }

{ const s = S(); const cy = H(s, { title: "이 덱의 각 부는 도출 II의 절로, 다시 M8 GBI로 이어집니다",
    sub: "막히면 도출 II의 해당 절로 가고, 다 읽었으면 GBI로 간다" });
  figBody(s, "s_map", cy);
  P(s, ["요약 → 유도 → 개인 버전 순서로 읽습니다."]); }

{ const s = S(); const cy = H(s, { title: "GBI로 넘어가면 기관의 부채가 개인의 목표가 됩니다",
    sub: "같은 골격, 다른 단위 — M8 GBI 요약 덱도 이 대응표로 시작한다" });
  figBody(s, "s_bridge", cy);
  P(s, ["LHP는 GHP로, 잉여금과 적립비율은 쿠션과 바닥으로 바뀝니다.",
        RED("부채를 존중하라는 말은 개인에게 목표를 먼저 지키라는 말이 됩니다.")]); }

/* 마감 */
T.closing(S(), {
  statements: ["부채는 숨어 있는 거대한 공매도 포지션이다.",
               "면역화는 방패, 두 블록은 실무의 문법이다.",
               "부채를 존중하라, 레버리지를 두려워하라."],
  message: "다음 — GBI(목표기반투자)\nLDI의 개인 버전",
  note: "출처: W06 M7 강의본 · 프라이머 · 국민연금 LDI 케이스와 모범답안 · LDI 수식 도출 II. 숫자는 별도 표시가 없으면 강의용 가상 예시(자산 100 · 부채 80)다.",
});

T.save(path.join(__dirname, "LDI_Summary_Basics_zeroone.pptx")).then(f => console.log("saved", f, "slides", pg + 1));
