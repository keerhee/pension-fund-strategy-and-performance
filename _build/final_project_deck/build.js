// XS 팀 프로젝트 안내서 — 제로원 덱
// 실행: cd _build/final_project_deck && NODE_PATH=/Users/keerhee/Project/node_modules node build.js
const fs = require("fs"), path = require("path");
const T = require("/Users/keerhee/Project/.claude/skills/zeroone-pitch-deck/scripts/template.js");
const { C, M, CW } = T;
const OUT = path.resolve(__dirname, "../../Final_Project/1_Student/2_Project_Guide/XS_Team_Project_Guide_Deck.pptx");
const V = f => path.join(__dirname, "viz", f), E = f => path.join(__dirname, "eq", f);
const ratio = p => { const b = fs.readFileSync(p); return b.readUInt32BE(16) / b.readUInt32BE(20); };

T.setBrand({ eyebrow: "BAF.60080 · XS 팀 프로젝트", wordmark: "" });
let P = 1;
const _w = console.warn; console.warn = (...a) => _w(`[p${P}]`, ...a);

// 왼쪽 수식 카드 + 확인 카드, 오른쪽 차트
function eqChart(s, cy, o) {
  const LW = o.lw || 5.0;
  const y2 = T.eqInCard(s, { y: cy, h: o.eqH || 1.85, w: LW, x: M, kind: "ghost", cap: o.cap,
    path: E(o.eq), ratio: ratio(E(o.eq)) });
  const by = y2 + 0.18, bh = 5.82 - by;
  T.card(s, M, by, LW, bh, "white");
  T.txt(s, o.boxCap, { x: M + 0.32, y: by + 0.18, w: LW - 0.64, h: 0.32, fontSize: 15, bold: true, color: C.teal, valign: "middle" });
  T.txt(s, o.lines.map(t => ({ text: t, options: { bullet: { code: "2022" }, breakLine: true } })),
    { x: M + 0.32, y: by + 0.56, w: LW - 0.60, h: bh - 0.70, fontSize: 17, color: C.body, valign: "top", ...T.lsp(17, 1.25) });
  T.figImg(s, V(o.chart), ratio(V(o.chart)), { x: undefined, left: M + LW + 0.35, w: CW - LW - 0.35, y: cy, bottom: 5.82, frame: true });
}

// ============================================================ 표지
let s = T.slide(true);
T.cover(s, { title: "XS 팀 프로젝트\n자율주행 포트폴리오", sub: "에이전트가 운용하고 사람은 CIO로서 감독합니다",
  org: "BAF.60080 · 기말 팀 프로젝트", chain: ["IPS", "에이전트 팀", "IC 보고서", "CIO 결정"] });

// ============================================================ 목차
s = T.slide();
T.head(s, { title: "안내서는 네 부분으로 구성됩니다", page: ++P });
T.agenda(s, [
  { num: "01", title: "과제와 배경", kicker: "무엇을 만들고 무엇을 결정하는가", desc: "일정 · 용어 · Ang의 여섯 층" },
  { num: "02", title: "출발점과 준비", kicker: "예시 MVP · 팀 · 데이터", desc: "예시 MVP 결과 · 역할 A~D · D1~D7 · 시점 잠금" },
  { num: "03", title: "필수 기능 M1~M10", kicker: "표준 시스템이 갖춰야 할 열 가지", desc: "분기 루프 · 각 기능의 [확인] · 아홉 단계" },
  { num: "04", title: "창의 트랙과 평가", kicker: "채점자는 MVP를 직접 돌린다", desc: "창의 메뉴 · 진행표 · T1~T8 · L1~L3 · 점수표" },
]);
T.banner(s, "평가의 중심은 보고서가 아니라 작동하는 MVP 저장소입니다", { y: 6.05 });

// ============================================================ 01
s = T.slide(true);
T.divider(s, { num: "01", title: "과제와 배경", sub: "무엇을 만들고, 매 분기 무엇을 결정하는가", page: ++P });

s = T.slide();
let cy = T.head(s, { title: "16주 동안 사람이 하던 IC를 이제 에이전트가 맡습니다", page: ++P,
  sub: "사람에게 남는 일은 감독이며, 무엇을 감독할지 설계하는 것이 과제의 절반이다" });
T.pairPanels(s,
  { cap: "HUMAN IC · 지금까지의 모의 IC", title: "사람이 계산하고 판단", bullets: ["애널리스트가 CMA 작성", "PM이 배분안 제출", "위원회가 심의·표결"], foot: "판단의 주체는 사람" },
  { kind: "dark", cap: "AGENT IC · 이번 프로젝트", title: "에이전트가 돌리는 운용", bullets: ["입력·배분안·심사 자동화", "상호 검토 후 표결", "CIO 한 명이 결정"], foot: "사람은 감독만 남는다" },
  { y: cy, h: 3.62, w: 5.2 });
T.punch(s, [{ text: "에이전트에게 맡길 일과 사람이 붙잡을 일을 나누는 것이 설계입니다", color: C.red }], { y: 6.06 });

s = T.slide();
cy = T.head(s, { title: "CIO는 매 분기 말과 프로젝트 끝에 결정합니다", page: ++P,
  sub: "분기마다 승인·조건부 승인·반려 중 하나와 사유, 끝에는 도입 의결문 — 예시 MVP의 실제 기록" });
T.figImg(s, V("decisions.png"), ratio(V("decisions.png")), { y: cy + 0.02, bottom: 5.20 });
T.punch(s, ["예시 MVP의 CIO는 12번 중 승인 9 · 조건부 1 · 반려 2로 결정했습니다.",
  { text: "답의 형식은 작동하는 MVP 저장소이고, 결정문·보고서·덱을 함께 냅니다", color: C.red }], { y: 5.35 });

s = T.slide();
cy = T.head(s, { title: "중간고사 시간에 MVP v0, 기말고사 주에 MVP v1을 냅니다", page: ++P,
  sub: "중간 프로포절은 발표 10분 + 질의 5분, 최종 발표는 20분(라이브 시연 포함) + 질의 10분이다" });
T.dataTable(s, ["시점", "할 일", "제출물"], [
  ["팀 구성 직후", "기금 선택 · 역할 배정", "팀 명단 · 역할표 1쪽"],
  ["W08 중간고사", "프로포절 발표", "덱 10장 · PREREG.md · MVP v0"],
  ["W09~W15", "구축 → 루프 → 재실행", "주간 진행 로그 LOG.md"],
  ["W16 기말고사 주", "최종 발표 · 시연", "MVP v1 · 영상 · 보고서 · 덱"],
], { y: cy - 0.04, rowH: 0.72, widths: [2.6, 4.2, 4.99], emph: 3 });
T.note(s, "※ 최종 발표에서 교수·청중은 기금운용위원회 역할을 맡는다. 기여표(CONTRIB.md)도 함께 낸다", { y: 5.62 });
T.punch(s, [{ text: "MVP v0가 없으면 최종 점수에서 5점을 뺍니다", color: C.red }], { y: 6.02 });

s = T.slide();
cy = T.head(s, { title: "하네스는 에이전트를 운용 통제 체계 안에 묶는 바깥 틀입니다", page: ++P,
  sub: "Ang 발표의 용어를 그대로 쓰고, 운용 현장에서 무엇에 해당하는지 함께 적었다" });
T.dataTable(s, ["용어", "뜻", "운용 현장에서는"], [
  ["에이전트", "목표를 받아 단계·도구를 정해 일하는 AI", "애널리스트 · PM · 리스크 담당자"],
  ["스킬", "업무 순서를 적은 작업 명세 SKILL.md", "분석 절차서"],
  ["하네스", "지시·도구·가드레일·기록을 묶는 틀", "승인 관문 · 한도 점검 · 감사 기록"],
  ["킬스위치", "자기 수정을 사람 검토 전까지 막는 장치", "정책 변경의 이사회 승인"],
  ["감사 기록", "누가 무엇을 근거로 결론 냈는지의 기록", "투자 결정 기록 · 회의록"],
], { y: cy - 0.10, rowH: 0.62, widths: [1.9, 5.4, 4.49] });
T.note(s, "※ 컨텍스트 = IPS·운용지침·보유 포트폴리오 · 도구 = 리스크 모형·옵티마이저 · 오케스트레이터 = 운용 프로세스 그 자체", { y: 5.66 });
T.punch(s, ["킬스위치와 감사 기록이 감독 점수(20점)의 대상입니다"], { y: 6.08 });

s = T.slide();
cy = T.head(s, { title: "숫자는 코드가 계산하고, 에이전트는 판단과 추론을 맡습니다", page: ++P,
  sub: "Ang 발표에서 기억할 세 문장" });
T.cards(s, [
  { cap: "문장 1", title: "컨텍스트+스킬 우선", bullets: ["도구 > AI 모델", "기관 고유 자산"] },
  { cap: "문장 2", title: "계산은 코드", bullets: ["판단은 에이전트", "LLM 계산 금지"] },
  { kind: "dark", cap: "문장 3", title: "노력은 하네스에", bullets: ["연결과 평가", "모델은 교체 가능"] },
], { y: cy + 0.10, h: 2.40 });
T.punch(s, ["μ·Σ·최적화·점수 집계를 LLM에게 맡기면 계산 재현 점검(T6)에서 떨어집니다.",
  { text: "'계산은 코드'는 설계 원칙이자 채점 기준입니다", color: C.red }], { y: 5.30 });

s = T.slide();
T.figureSlide(s, { title: "논문의 여섯 층은 이 과정에서 배운 내용과 그대로 대응합니다", page: ++P,
  sub: "각 상자 아래 주차가 그 층을 배운 곳이고, 비평·투표 층은 16주 모의 IC가 에이전트의 일이 된 것이다",
  path: V("layers.png"), ratio: ratio(V("layers.png")), caption: "※ 논문은 참고 설계도일 뿐이다. 구조를 바꾸거나 새 에이전트를 발명해도 되며, 배점이 가장 큰 영역은 창의성이다" });

// ============================================================ 02
s = T.slide(true);
T.divider(s, { num: "02", title: "출발점과 준비", sub: "예시 MVP를 고쳐 쓰고, 역할을 나누고, 데이터를 갖춘다", page: ++P });

s = T.slide();
cy = T.head(s, { title: "예시 MVP 폴더 모양 그대로가 최종 제출물의 모양입니다", page: ++P,
  sub: "배포 묶음의 3_Example_MVP/ — 2022.8 말부터 3개월마다 12회 결정(평가 구간 2022.9~2025.7)" });
T.cards(s, [
  { cap: "구성", rows: [["에이전트", "13개", true], ["스킬", "7개"], ["결정", "분기 12회"]] },
  { cap: "하네스", rows: [["감사", "trace.jsonl", true], ["보호", "킬스위치"], ["시점", "as_of 잠금"]] },
  { kind: "dark", cap: "사람 · 채점", rows: [["CIO", "결정 12건", true], ["변경", "승인·반려 4건"], ["콘솔", "T1~T8 · L1~L3"]] },
], { y: cy + 0.06, h: 2.75 });
T.punch(s, ["start.command(맥) · start.bat(윈도)를 더블클릭하면 채점 콘솔이 브라우저에 열립니다.",
  { text: "무엇을 어떤 형태로 낼지는 이 폴더를 보고 맞춥니다", color: C.red }], { y: 5.40 });

s = T.slide();
T.figurePanelSlide(s, { title: "예시 MVP는 60/40에 뒤진 성과도 숨기지 않고 보고합니다", page: ++P,
  sub: "평가 구간 2022.9~2025.7 누적 수익률 · 오른쪽 숫자는 연율",
  panel: { cap: "예시 MVP 결과", title: "채택 경로 7.90%", bullets: ["60/40은 11.82%", "MVO 4개 분기 기각", "보유했다면 11.57%", "조건부 승인 의결"] },
  path: V("perf.png"), ratio: ratio(V("perf.png")), panelW: 3.9, bottom: 5.80 });
T.punch(s, [{ text: "성과 자체는 평가하지 않고, 감독 장치가 무엇을 막고 놓쳤는지 정직하게 분석했는지를 봅니다", color: C.red }], { y: 6.00 });

s = T.slide();
cy = T.head(s, { title: "예시의 판단 부분은 규칙 기반 대역이며, 팀이 바꿔야 합니다", page: ++P,
  sub: "매크로 해석·리서치 메모·검토 의견·투표 순위·IC 보고서 문장이 모두 코드 규칙으로 만들어졌다" });
T.cards(s, [
  { cap: "바꿀 것 1", title: "우리 기금의 IPS", bullets: ["가상 기금 KFP를 그대로 쓰지 않는다"] },
  { cap: "바꿀 것 2", title: "판단은 LLM으로", bullets: ["메모·검토·순위·보고서 중 셋 이상", "출력은 runs/에 녹화"] },
  { kind: "lime", cap: "바꿀 것 3", title: "창의 트랙 1개+", bullets: ["배점 35점의 창의성 영역"] },
], { y: cy + 0.10, h: 2.64, connect: true });
T.note(s, "※ README에 '예시 MVP와 달라진 점' 표(파일·에이전트·규칙 단위)를 반드시 둔다. 숫자는 계속 코드가 만든다", { y: 5.10 });
T.punch(s, ["특강 실습 폴더(self-driving-mvp/, 에이전트 7개·한 시점 결정)는 참고용입니다.",
  { text: "예시를 바꾸지 않고 낸 부분은 점수를 받지 못합니다", color: C.red }], { y: 5.40 });

s = T.slide();
cy = T.head(s, { title: "핵심 역할 넷을 한 명씩 맡고, CIO는 역할 A가 아닌 팀원이 겸합니다", page: ++P,
  sub: "팀은 4~6명 — 남는 인원은 통합·검증(E)이나 창의 확장(F)을 맡는다" });
T.cards(s, [
  { cap: "A · 거버넌스", title: "IPS·하네스", bullets: ["위반이 원천 불가한가"] },
  { cap: "B · 입력", title: "매크로·CMA", bullets: ["새 정보의 반영 경로"] },
  { cap: "C · 구성", title: "PC 4개 이상", bullets: ["충분히 다른 안인가"] },
  { kind: "dark", cap: "D · 심의·학습", title: "CRO·투표·IC", bullets: ["합의와 반대를 함께"] },
], { y: cy + 0.10, h: 2.22 });
T.note(s, "※ A가 CIO를 겸하면 규칙을 만든 사람이 그 규칙의 예외를 승인하게 된다", { y: 4.78 });
T.punch(s, ["보조 E는 '누가 돌려도 같은 숫자가 나오는가', 보조 F는 '우리 팀만의 새로운 점'을 책임집니다.",
  { text: "맡은 필수 기능이 동작하지 않으면 그 담당자의 개인 계수가 내려갑니다", color: C.red }], { y: 5.35 });

s = T.slide();
cy = T.head(s, { title: "D1~D4가 없으면 시스템이 돌지 않습니다", page: ++P,
  sub: "데이터는 배포하지 않는다 — 내려받기는 Claude Code에 맡기고 스크립트를 제출물에 넣는다" });
T.dataTable(s, ["#", "데이터", "최소 요건", "예시 MVP에서"], [
  ["D1", "총수익률 (월간)", "자산 8개+ · 학습 84개월", "ETF 11개 (yfinance)"],
  ["D2", "무위험 수익률", "기금 통화 단기 금리", "미국 3개월 국채"],
  ["D3", "정책 벤치마크", "기금 목적에 맞게", "60/40 · 동일가중"],
  ["D4", "국면 판정 매크로", "3개+, 발표 지연 명시", "금리·금리차·물가 등"],
], { y: cy - 0.04, rowH: 0.76, widths: [0.9, 3.3, 3.9, 3.69] });
T.note(s, "※ 총수익률은 배당·이자를 포함한다. 60/40이 기본 벤치마크는 아니다", { y: 5.60 });
T.punch(s, ["데이터 계획(D1~D7의 출처·기간·발표 지연표)은 중간 프로포절에 넣습니다"], { y: 6.02 });

s = T.slide();
T.figureSlide(s, { title: "결정 시점에 실제로 알 수 있었던 값만 씁니다", page: ++P,
  sub: "분기 말 as_of의 결정 — 늦게 발표되는 지표는 지연을 반영하고, 이후 행은 로더가 거부한다(T4)",
  path: V("timelock.png"), ratio: ratio(V("timelock.png")),
  caption: "※ LLM이 학습으로 이미 결과를 알 수 있다는 문제는 동질화·난독화 실험(M5)으로 따로 점검한다" });

s = T.slide();
cy = T.head(s, { title: "D5가 없으면 IPS 목표가 장식이 되고, D6이 없으면 감사할 수 없습니다", page: ++P,
  sub: "기금마다 달라지는 데이터 — 데이터 사전 data/DATA.md에 출처·단위·지연·결측 처리를 적는다" });
T.dataTable(s, ["#", "데이터", "쓰는 곳", "최소 요건"], [
  ["D5", "기금 고유 데이터", "IPS · 성과 · CIO", "부채·지출·납입·현금흐름 중 해당분"],
  ["D6", "리서치 자료 목록", "research-agent", "제목·공개일·출처 · 그 분기 이전만"],
  ["D7", "사람의 결정", "CIO · 하네스", "cio_decisions · approvals.csv"],
], { y: cy - 0.04, rowH: 0.80, widths: [0.9, 3.0, 3.0, 4.89] });
T.note(s, "※ 자산을 바꾼 팀도 기본 11개 자산으로 한 번 돌린 결과를 부록에 둔다 — 팀 간 비교용", { y: 5.00 });
T.punch(s, ["재배포가 금지된 데이터는 파일 대신 내려받기 스크립트만 넣습니다.",
  { text: "ETF를 지수로 대신하면 그 사실과 차이(보수·추적오차)를 데이터 사전에 적습니다", color: C.red }], { y: 5.45 });

// ============================================================ 03
s = T.slide(true);
T.divider(s, { num: "03", title: "필수 기능 M1~M10", sub: "열 가지가 모두 동작해야 표준 트랙을 통과한다 — [확인]이 채점 기준", page: ++P });

s = T.slide();
T.figureSlide(s, { title: "분기 말마다 열 가지 기능이 한 바퀴를 돕니다", page: ++P,
  sub: "모든 호출은 runs/{as_of}/trace.jsonl에 남고, 사람은 M9에서만 결정한다",
  path: V("loop.png"), ratio: ratio(V("loop.png")), caption: "※ 하네스(M2)는 루프 전체를 감싼다 — 감사 기록 · 보호 파일 · as_of 잠금" });

s = T.slide();
cy = T.head(s, { title: "M1 · IPS를 어기는 안은 표결 목록에 오르지 못합니다", page: ++P,
  sub: "역할 A — ips.md 본문과 함께 기계가 읽는 제약 표(YAML)를 둔다" });
eqChart(s, cy, { cap: "분산 요건 — 유효 종목 수", eq: "eq_neff.png", eqH: 1.62, lw: 5.4, boxCap: "검산과 [확인]",
  lines: ["예: 비중 40·30·20·10%", "하한 4.0이면 표결 제외", "[확인] 50%안은 사유와 함께 기각"],
  chart: "neff.png" });
T.punch(s, ["최소 항목: 목표 수익률 · 변동성 상한 · 최대낙폭 한도 · 자산군 범위 · 종목 상한 · 분산 요건"], { y: 6.02 });

s = T.slide();
T.figurePanelSlide(s, { title: "M2 · 어떤 에이전트도 규칙과 코드를 직접 고치지 못합니다", page: ++P,
  sub: "역할 A — 수정은 proposals/에 제안서로만 남고, CIO 승인이 있어야 반영된다",
  panel: { cap: "감사 기록 trace.jsonl", bullets: ["호출마다 한 줄", "입력·스킬·출력", "제약·근거 요약"], footCap: "[확인]", foot: "제안해도 파일은 그대로" },
  path: V("killswitch.png"), ratio: ratio(V("killswitch.png")), panelW: 3.7, bottom: 5.80 });
T.punch(s, [{ text: "CIO 승인 후 반영된 변경은 CHANGELOG.md에 날짜·사유·승인자를 남깁니다", color: C.red }], { y: 6.00 });

s = T.slide();
cy = T.head(s, { title: "M3 · M4 · 국면 라벨과 기대수익률은 코드가 정합니다", page: ++P,
  sub: "역할 B — 에이전트는 그 해석과 근거를 쓴다. 수축 강도 δ는 사전 등록한다" });
const EW = 5.4;
let yy = T.eqInCard(s, { y: cy, h: 1.50, w: 5.4, x: M + (CW - EW) / 2, kind: "ghost", cap: "M4 · 기대수익률 수축 (δ 사전 등록)",
  path: E("eq_mu.png"), ratio: ratio(E("eq_mu.png")) });
T.cards(s, [
  { cap: "M3 · 매크로", title: "국면 라벨은 규칙", bullets: ["금리차 × 물가 추세"] },
  { cap: "M4 · 공분산", title: "Ledoit–Wolf 수축", bullets: ["강도는 cma.json에"] },
  { kind: "dark", cap: "[확인]", title: "같은 as_of면 같다", bullets: ["라벨·cma.json 동일"] },
], { y: yy + 0.20, h: 1.90 });
T.punch(s, [{ text: "δ를 바꾸면 PC 안들이 얼마나 달라지는지가 3단계의 질문입니다", color: C.red }], { y: 6.02 });

s = T.slide();
cy = T.head(s, { title: "M5 · 리서치 메모는 '현행 유지' 아니면 변경 제안서로 끝납니다", page: ++P,
  sub: "역할 B — 분기마다 시황 요약이나 새 논문 하나를 읽는다" });
T.flow3(s, [
  { kind: "white", cap: "입력", lines: [{ text: "as_of 이전 공개 자료만", fs: 20 }, { text: "research_corpus.csv", fs: 16, color: C.muted }] },
  { kind: "dark", cap: "메모", lines: [{ text: "현행 유지 또는", fs: 20 }, { text: "IPS·스킬 변경 제안서", fs: 20 }] },
  { kind: "lime", cap: "처리", lines: [{ text: "M2 경로로만 반영", fs: 20 }, { text: "승인·반려와 사유 기록", fs: 16 }] },
], { y: cy + 0.05, h: 2.10 });
T.note(s, "※ 회사명·날짜를 가린 입력(동질화·난독화)으로 같은 메모를 한 번 더 써서 결론이 바뀌는지 기록한다", { y: 4.70 });
T.punch(s, ["LLM은 학습 과정에서 이미 미래를 알고 있을 수 있습니다(미래정보 편향).",
  { text: "[확인] 평가 구간 동안 변경 제안이 최소 1건 나오고 처리 결과가 남습니다", color: C.red }], { y: 5.35 });

s = T.slide();
cy = T.head(s, { title: "M6 · 적대적 분산자가 서로 비슷한 안끼리의 경쟁을 막습니다", page: ++P,
  sub: "역할 C — 같은 cma.json으로 PC 에이전트 4개 이상이 각자 배분안과 근거를 낸다" });
const AW = 8.8;
yy = T.eqInCard(s, { y: cy, h: 1.92, w: AW, x: M + (CW - AW) / 2, kind: "ghost", cap: "적대적 분산자 — 다른 PC 안들과의 차이를 최대화하되 샤프 하한을 지킨다",
  path: E("eq_adv.png"), ratio: ratio(E("eq_adv.png")) });
const LW6 = 5.7, ry = yy + 0.20;
T.eqInCard(s, { y: ry, h: 1.45, w: LW6, x: M, kind: "dark", cap: "[확인] 분기마다 안들 사이 추적오차 보고",
  path: E("eq_te.png"), ratio: ratio(E("eq_te.png")) });
T.card(s, M + LW6 + 0.30, ry, CW - LW6 - 0.30, 1.45, "white");
T.txt(s, "서로 다른 계열에서 셋 이상", { x: M + LW6 + 0.62, y: ry + 0.18, w: 5.2, h: 0.32, fontSize: 15, bold: true, color: C.teal, valign: "middle" });
T.txt(s, [{ text: "휴리스틱 · 수익 최적화", options: { breakLine: true } }, { text: "위험 구조 · 비전통(CVaR·TPA 등)" }],
  { x: M + LW6 + 0.62, y: ry + 0.54, w: 5.3, h: 0.86, fontSize: 18, bold: true, color: C.body, valign: "top", ...T.lsp(18, 1.25) });
T.punch(s, [{ text: "적대적 분산자를 넣었을 때 평균 추적오차가 커져야 합니다", color: C.red }], { y: 6.02 });

s = T.slide();
cy = T.head(s, { title: "M7 · 모든 안이 표결 전에 같은 양식의 리스크 보고서를 받습니다", page: ++P,
  sub: "역할 D — 예상 변동성 · 95% CVaR · 위험기여 · 스트레스 손실(2022년 금리 급등 재현 1개 이상)" });
eqChart(s, cy, { cap: "위험기여 — 합은 1", eq: "eq_rc.png", eqH: 1.58, lw: 5.4, boxCap: "읽는 법 (주식 16% · 채권 5% · 상관 0.2)",
  lines: ["60/40: 주식이 위험의 92%", "ERC 24/76이면 위험 반반", "[확인] 같은 보고서 수신(trace)"],
  chart: "rc.png" });
T.punch(s, [{ text: "비중이 분산되어 보여도 위험은 한 자산에 몰려 있을 수 있습니다", color: C.red }], { y: 6.02 });

s = T.slide();
cy = T.head(s, { title: "M8 · 득표와 정량 점수를 사전에 정한 비율 λ로 결합합니다", page: ++P,
  sub: "역할 D — 각 PC 에이전트는 자기를 뺀 다른 안 2건을 체크리스트로 검토한 뒤 투표한다" });
yy = T.eqInCard(s, { y: cy, h: 2.05, kind: "dark", cap: "수정 보르다 득표 S → 정규화 Ŝ → 정량 점수 M과 결합",
  path: E("eq_score.png"), ratio: ratio(E("eq_score.png")) });
T.cards(s, [
  { cap: "득표", title: "상위 5개 5~1점" },
  { cap: "반대 표시", title: "최하위 1개 −2점" },
  { cap: "사전 등록 (W08)", title: "λ · M · 줄인 규칙" },
], { y: yy + 0.20, h: 1.15 });
T.punch(s, [{ text: "PC 에이전트가 6개 미만이면 '상위 2개 +2·+1, 최하위 −2'처럼 줄인 규칙을 미리 등록합니다", color: C.red }], { y: 6.02 });

s = T.slide();
T.figurePanelSlide(s, { title: "검산 예제에서는 C가 채택되고 정량 1위 D는 탈락합니다", page: ++P,
  sub: "PC 4개 · 줄인 규칙(+2 · +1 · −2) · M = (0.40, 0.70, 0.80, 0.90) · λ = 0.5",
  panel: { cap: "투표자 → 1위 · 2위 · 최하위", bullets: ["A → B · C · D", "B → C · A · D", "C → B · A · D", "D → C · B · A"], foot: "득표 A 0 · B 5 · C 5 · D −6" },
  path: V("vote.png"), ratio: ratio(V("vote.png")), panelW: 3.9, bottom: 5.80 });
T.punch(s, [{ text: "득표 동점(B·C)은 정량 점수가 갈랐고, D는 세 명 모두에게 최하위로 지목되었습니다", color: C.red }], { y: 6.00 });

s = T.slide();
cy = T.head(s, { title: "M9 · CIO는 세 가지 중 하나로 결정하고 안을 직접 고치지 않습니다", page: ++P,
  sub: "역할 D + CIO — ic_report.md(1~2쪽)에는 권고안·차점안·반대 의견·CRO 핵심 숫자·기각 사유가 들어간다" });
T.dataTable(s, ["결정", "의미", "기록할 것"], [
  ["승인", "권고안을 그대로 집행(가상)", "한 줄 사유"],
  ["조건부 승인", "조건을 붙여 집행", "조건과 사유"],
  ["반려", "직전 분기 포트폴리오 유지", "사유와 다음 분기 요구사항"],
], { y: cy - 0.04, rowH: 0.80, widths: [2.6, 4.6, 4.59], emph: 1 });
T.note(s, "※ 개입 횟수와 사유는 모두 INTERVENTIONS.md에 적는다. 승인 사유가 매번 '권고대로'뿐이면 감독이 작동했다고 보기 어렵다", { y: 5.02 });
T.punch(s, ["개입이 적을수록 좋은 것은 아닙니다.", { text: "필요한 순간에 근거를 갖고 개입했는지가 평가 대상입니다", color: C.red }], { y: 5.45 });

s = T.slide();
cy = T.head(s, { title: "M10 · 변경은 테스트에서 나아진 경우에만 승격합니다", page: ++P,
  sub: "역할 D — 분기가 지나면 meta-reviewer가 직전 예측을 실현과 대조한다" });
const MW = 6.4;
yy = T.eqInCard(s, { y: cy, h: 1.95, w: MW, x: M + (CW - MW) / 2, kind: "ghost", cap: "예측 오차 — 기각된 안도 함께 평가한다",
  path: E("eq_mae.png"), ratio: ratio(E("eq_mae.png")) });
T.pipeline(s, ["오차 패턴에서\n변경 제안", "킬스위치 경유\nCIO 승인", "같은 과거 구간\n전후 비교", "승격 또는\n롤백"], { y: yy + 0.22, h: 1.15 });
T.punch(s, [{ text: "[확인] 제안 → 승인 → 테스트 → 승격·롤백 기록이 최소 1회 남아야 합니다", color: C.red }], { y: 6.02 });

s = T.slide();
T.figureSlide(s, { title: "표준 트랙은 아홉 단계로 진행하고, 각 답이 보고서의 절이 됩니다", page: ++P,
  sub: "2단계 질문: 평가 구간 첫 분기의 결정을 2026년에 학습된 LLM으로 내리는 것은 공정한가",
  path: V("steps.png"), ratio: ratio(V("steps.png")),
  caption: "※ 7단계: 같은 설정으로 3회 재실행 — 코드 계산은 매번 같고, 달라지는 것은 판단 부분뿐이어야 한다" });

// ============================================================ 04
s = T.slide(true);
T.divider(s, { num: "04", title: "창의 트랙과 평가", sub: "배점이 가장 큰 창의성, 그리고 채점자가 직접 돌리는 평가 절차", page: ++P });

s = T.slide();
cy = T.head(s, { title: "창의 트랙은 표준 시스템 위에 우리 팀만의 개선을 얹습니다", page: ++P,
  sub: "메뉴에서 하나 이상을 깊게 파거나, 메뉴에 없는 것을 새로 만든다" });
T.cards(s, [
  { kind: "lime", cap: "7.1 강력 권장", title: "자기 목적 IPS", bullets: ["목적이 IPS를 바꾸고", "IPS가 에이전트를 바꾼다"] },
  { cap: "7.2 구조 개선", title: "투표·방법·뷰", bullets: ["토론 후 집계", "새 PC 방법 발굴", "LLM 뷰 블랙-리터만"] },
  { cap: "7.3 감독 개선", title: "함정 대응", bullets: ["국면 전환 감지", "거짓 합의 탐지", "CIO 대시보드"] },
], { y: cy + 0.05, h: 2.85 });
T.punch(s, ["특강 MVP가 대응하지 못한 함정은 국면 민감성입니다(금 예측 오차 18.2%p).",
  { text: "새 기능의 효과를 비교 실험으로 보여야 창의성 점수가 됩니다", color: C.red }], { y: 5.40 });

s = T.slide();
cy = T.head(s, { title: "기금의 목적이 바뀌면 IPS와 필요한 데이터가 함께 바뀝니다", page: ++P,
  sub: "기본 가상 기금 KFP 대신 목적이 분명한 기금을 정한다 — D5의 예" });
T.dataTable(s, ["기금 유형", "달라지는 점", "추가 데이터"], [
  ["대학 발전기금", "지출 규칙 · 실질 원금 보전", "지출률 · 기부 유입 · 비용 물가"],
  ["퇴직연금 디폴트옵션", "연령별 글라이드패스 · 수수료", "연령 분포 · 납입률 · 원화 자산"],
  ["DB형 연기금", "부채 듀레이션 헤지(LDI)", "부채 현금흐름 · 할인율 곡선"],
  ["국부펀드", "초장기 시계 · 통화 노출", "환율 · 국내 시장 시가총액"],
  ["보험 일반계정", "자본 규제 · 신용등급 제약", "K-ICS 위험계수 · 부채 듀레이션"],
], { y: cy - 0.08, rowH: 0.64, widths: [3.0, 4.3, 4.49] });
T.punch(s, [{ text: "원화 기준 기금이면 해외 자산 수익률을 환율로 환산하고 환헤지 여부를 IPS에 적습니다", color: C.red }], { y: 5.98 });

s = T.slide();
T.figureSlide(s, { title: "W08에 프로포절과 MVP v0, W16에 MVP v1을 냅니다", page: ++P,
  sub: "권장 진행표 — 주차별 완료 기준을 넘겨야 다음 주차로 간다",
  path: V("schedule.png"), ratio: ratio(V("schedule.png")),
  caption: "※ W15에 자가 점검(P9)으로 reports/selfcheck.md 8개 통과를 확인한다" });

s = T.slide();
cy = T.head(s, { title: "W08 중간 프로포절은 사전 등록표와 MVP v0가 핵심입니다", page: ++P });
T.dataTable(s, ["항목", "담을 내용"], [
  ["IPS 초안 · 구조도 · 역할", "숫자마다 근거 · 시스템 구조도 한 장 · CIO 지정"],
  ["사전 등록표 PREREG.md", "λ · 정량 점수 M · 수축 강도 δ · 평가 지표 · 비교 기준"],
  ["감독 설계 · 창의 · 위험", "자동 기각 · 킬스위치 · 사람 승인 지점 · 성공 기준"],
  ["데이터 계획", "D1~D7의 출처 · 기간 · 발표 지연, D5 확보처"],
  ["MVP v0", "우리 IPS로 첫 분기(2022-08)를 끝까지 돌린 저장소"],
], { y: cy - 0.06, rowH: 0.66, widths: [4.0, 7.79], emph: 4 });
T.punch(s, ["덱 10장 이내 · 사전 등록값을 나중에 바꾸면 사유를 CHANGELOG.md에 남깁니다.", { text: "MVP v0는 점수에 들어가지 않지만, 없으면 최종 점수에서 5점을 뺍니다", color: C.red }], { y: 5.94, gap: 0.40 });

s = T.slide();
cy = T.head(s, { title: "채점자는 파이썬과 브라우저만으로 MVP를 돌립니다", page: ++P,
  sub: "Claude Code·터미널·API 키를 쓰지 않는다 — 버튼은 모두 임시 복사본에서 돈다" });
yy = T.pipeline(s, ["zip 풀기", "start 파일\n더블클릭", "개요 탭\n성과·결정", "공개 점검\nT1~T8", "분기 다시\n계산", "문서 탭\n점수표"], { y: cy + 0.10, h: 1.20, gap: 0.30 });
T.dataTable(s, ["부분", "채점 콘솔에서"], [
  ["CMA · 최적화 · 적격 · 투표 · 성과", "다시 계산 — 소수 6자리까지 일치"],
  ["CIO 결정 · 변경 승인", "입력으로 재생 — csv 파일"],
  ["LLM 판단(메모·검토·순위·보고서)", "녹화본 재생 — 양식과 근거만 본다"],
], { y: yy + 0.22, rowH: 0.56, widths: [5.6, 6.19] });
T.punch(s, [{ text: "콘솔이 뜨지 않으면 실행 점수(T1)는 0점입니다", color: C.red }], { y: 6.02 });

s = T.slide();
T.figureSlide(s, { title: "공개 점검 T1~T8은 제출 전에 팀이 직접 돌려 볼 수 있습니다", page: ++P,
  sub: "티일 = 완성도·재현성(25점) · 파랑 = 감독·하네스(20점) — 채점자도 똑같이 돌린다",
  path: V("tests.png"), ratio: ratio(V("tests.png")),
  caption: "※ T6·T8은 코드로 계산한 숫자만 정확히 일치를 요구한다. 판단 부분은 양식과 근거 기록만 본다" });

s = T.slide();
cy = T.head(s, { title: "라이브 점검은 코드를 고치지 않고 IPS와 입력만 바꿔 대응합니다", page: ++P,
  sub: "발표 당일 교수가 주는 시험 — 미리 알려 주지 않으며, 발표 20분 중 7분 안에 시연한다" });
T.cards(s, [
  { cap: "L1 · IPS 조항 변경", title: "변동성 상한 7%", bullets: ["ips.md만 고쳐 한 분기 재실행"] },
  { cap: "L2 · 가상 시장 상황", title: "금리 +150bp", bullets: ["IC 보고서·CIO 결정까지 진행"] },
  { kind: "dark", cap: "L3 · 숨은 결함", title: "비중 합 1.03", bullets: ["잡아내거나 trace로 위치를 찾는다"] },
], { y: cy + 0.10, h: 2.28 });
T.note(s, "※ L2 예: 금리 +150bp와 함께 주식 −15% 한 달 · L3 예: 리서치 메모에 평가 구간 뒤의 사건이 섞임", { y: 4.82 });
T.banner(s, "L1~L3 대응은 감독·하네스 점수 중 6점입니다", { y: 5.45 });

s = T.slide();
T.figurePanelSlide(s, { title: "창의성이 35점으로 가장 크고, 미래정보 사용은 10점을 뺍니다", page: ++P,
  sub: "개인 점수 = 팀 점수 × 개인 계수(0.8~1.1) — 기여표·커밋 기록·동료 평가로 정한다",
  panel: { kind: "dark", cap: "감점", title: "미래정보 −10", bullets: ["MVP v0 미제출 −5", "사전 등록값 무단 변경 −5", "불리한 결과 누락 −5"] },
  path: V("score.png"), ratio: ratio(V("score.png")), panelW: 3.9, bottom: 5.80 });
T.punch(s, [{ text: "완성도 25 = T1 7 · T5 3 · T6 5 · T8 5 · 재실행 5  /  감독 20 = T2·T3·T4·T7 각 3 · L 6 · CIO 2" }], { y: 6.00 });

s = T.slide();
cy = T.head(s, { title: "터미널 명령 대신 Claude Code에게 순서대로 말합니다", page: ++P,
  sub: "시작 키트 P1~P9 — 각 단계는 [어디] [입력] [출력] [확인] 네 칸으로 적혀 있다" });
T.cards(s, [
  { cap: "출발", rows: [["P1", "콘솔·T1~T8", true], ["P1-2", "판단→에이전트"], ["P2", "데이터·잠금"]] },
  { cap: "구축", rows: [["P3", "하네스 확장", true], ["P4", "팀 구성"], ["P5", "투표 검산"]] },
  { kind: "dark", cap: "실행 · 점검", rows: [["P6", "분기 루프", true], ["P7·P8", "재실행·CIO"], ["P9", "자가 점검"]] },
], { y: cy + 0.06, h: 2.75 });
T.punch(s, ["프로그램은 Claude Code가 쓰고, 팀은 무엇을 만들지 말하고 [확인]으로 점검합니다.",
  { text: "숫자가 맞는지는 반드시 사람이 확인합니다 — M8 검산 예제가 그 연습입니다", color: C.red }], { y: 5.40 });

s = T.slide();
cy = T.head(s, { title: "성과가 60/40보다 나빠도 감점하지 않습니다", page: ++P, sub: "자주 묻는 질문" });
T.cards(s, [
  { cap: "Q · 성과가 나쁘면?", title: "감점 아님", bullets: ["왜 그랬는지 분석", "막은 것·놓친 것"] },
  { cap: "Q · LLM에 μ를 물으면?", title: "전망으로만", bullets: ["μ·Σ는 코드 계산", "BL 뷰 + 확신도 상한"] },
  { kind: "dark", cap: "Q · 구조를 바꾸면?", title: "바꿔도 된다", bullets: ["바꾼 이유를 제시", "결과가 창의성 점수"] },
], { y: cy + 0.06, h: 2.70 });
T.punch(s, ["채점자가 돌릴 때 LLM 결과가 달라도 녹화본을 재생하므로 문제없습니다.",
  { text: "발표 때 라이브로 돌려 결과가 달라지는 것은 정상입니다", color: C.red }], { y: 5.30 });

// ============================================================ 마감
s = T.slide(true);
T.closing(s, {
  statements: ["IPS가 전 과정을 제약하고", "에이전트가 분기마다 운용하며", "사람은 CIO로서 감독합니다"],
  message: "작동하는 MVP와 정직한 해석,\n그리고 근거 있는 CIO 결정",
  note: "참고: Ang, Azimbayev & Kim (2026), The Self Driving Portfolio, arXiv:2604.02279 · CFA Institute (2026) · 예시 MVP: 배포 묶음 3_Example_MVP/",
});

T.save(OUT).then(f => console.log("saved", f, "slides", P));
