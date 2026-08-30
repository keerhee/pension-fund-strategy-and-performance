// W07 사전학습 — M8 부채연계투자(LDI) · M9 목표기반투자(GBI)
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w07",
  out: "W07_LDI와GBI/W07_0_프라이머_LDI와GBI는왜부채와목표에서시작하나.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W07 사전학습",
  coverTitle: "LDI와 GBI는 왜\n부채와 목표에서 시작하나",
  coverSub: "W07 사전학습 · M8 부채연계투자 · M9 목표기반투자",
  chain: ["부채를 본다", "금리가 흔든다", "목표에서 시작한다"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "성적표가 다르다", kicker: "자산만 보면 틀린다",
      desc: "부채까지 함께 · 적립비율" },
    { num: "02", title: "금리가 흔든다", kicker: "부채도 값이 변한다",
      desc: "듀레이션 · 수식 하나" },
    { num: "03", title: "2022년 영국", kicker: "닷새의 사건",
      desc: "금리 급등 · 무엇이 문제였나" },
    { num: "04", title: "개인의 경우", kicker: "목표에서 시작한다",
      desc: "세 개의 통 · 이룰 확률" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "성적표가 다르다",
      sub: "연기금은 번 돈이 아니라 부채으로 평가받습니다" },

    { type: "fig", file: "funding.png",
      title: "자산만 보면 좋아 보이는 해가 실제로는 나쁜 해입니다",
      punch: ["연기금에는 언젠가 내줘야 할 돈이 정해져 있습니다.",
              { text: "그 부채이 더 빨리 늘면, 자산이 늘어도 형편은 나빠집니다.", color: C.red }] },

    { type: "cards", title: "그래서 보는 숫자가 하나 더 있습니다",
      cards: [{ cap: "가진 것", title: "모아 둔 돈",
                bullets: ["지금까지 쌓은 자산", "매년 수익으로 늘어난다"] },
              { cap: "갚을 것", title: "부채",
                bullets: ["앞으로 내줘야 할 연금", "이것도 값이 변한다"] },
              { kind: "lime", cap: "나눠 보면", title: "부채를 갚을 수 있는 비율",
                bullets: ["100%를 넘으면 여유", "밑돌면 채워야 한다"] }],
      punch: [{ text: "이 비율 하나가 연기금 이사회에서 가장 자주 불리는 숫자입니다.", color: C.red }] },

    { type: "divider", num: "02", title: "금리가 흔든다",
      sub: "부채도 시장 가치가 있고, 금리에 따라 움직입니다" },

    { type: "fig", file: "duration.png",
      title: "금리가 내리면 부채이 자산보다 훨씬 크게 불어납니다",
      punch: ["멀리 있는 돈일수록 금리에 크게 흔들립니다. 연금은 수십 년 뒤에 나갑니다.",
              { text: "그래서 금리가 내린 해에 연기금 형편이 나빠집니다.", color: C.red }] },

    { type: "eq", file: "equation.png", cap: "금리가 움직일 때 값이 변하는 폭",
      title: "그 변동성을 한 줄로 적습니다",
      cards: [{ cap: "D", title: "듀레이션" },
              { cap: "Δy", title: "금리가 움직인 폭" },
              { cap: "−", title: "방향은 반대" },
              { kind: "lime", cap: "ΔP / P", title: "값이 변한 폭" }],
      punch: [{ text: "듀레이션이 18년이면, 금리 1%p에 값이 18% 움직입니다.", color: C.teal },
              { text: "자산과 부채의 듀레이션을 맞추는 일이 부채연계투자입니다.", color: C.red }] },

    { type: "divider", num: "03", title: "2022년 영국",
      sub: "이 방법이 어떻게 위기가 되었는지를 봅니다" },

    { type: "fig", file: "uk2022.png",
      title: "닷새 만에 30년 금리가 1.2%p 뛰었습니다",
      punch: ["연기금들은 기간을 맞추려고 빌린 돈으로 국채를 들고 있었습니다.",
              { text: "값이 떨어지자 담보를 더 내라는 요구가 몰렸고, 국채를 팔 수밖에 없었습니다.", color: C.red }] },

    { type: "cards", title: "방법이 틀린 게 아니라 빌린 돈이 문제였습니다",
      cards: [{ cap: "맞았던 것", title: "기간을 맞춘 판단",
                bullets: ["금리에 덜 흔들리게 했다", "방향은 옳았다"] },
              { cap: "빠뜨린 것", title: "빌린 돈의 대가",
                bullets: ["담보를 더 내야 한다", "급할 때 팔아야 한다"] },
              { kind: "dark", cap: "교훈", title: "현금을 얼마나 둘까",
                bullets: ["평소엔 낭비로 보인다", "그날 하루가 갈랐다"] }],
      punch: [{ text: "위험은 자산에만 있는 게 아니라 급하게 팔아야 하는 상황에도 있습니다.", color: C.red }] },

    { type: "divider", num: "04", title: "개인의 경우",
      sub: "기관의 “부채”은 개인에게 “목표”입니다" },

    { type: "fig", file: "buckets.png",
      title: "목표마다 다른 통에 담으면 굴리는 법이 달라집니다",
      punch: ["반드시 써야 할 돈과 되면 좋은 돈을 한 통에 담으면 구분이 사라집니다.",
              { text: "통을 나누면 “얼마 벌까”가 아니라 “무엇을 지킬까”에서 시작할 수 있습니다.", color: C.red }] },

    { type: "fig", file: "goal_prob.png",
      title: "성적표도 수익률이 아니라 목표를 이룰 확률입니다",
      punch: ["더 모으면 확률이 오릅니다. 더 위험하게 굴려도 확률이 항상 오르지는 않습니다.",
              { text: "“몇 % 벌었나”가 아니라 “목표에 닿을 확률이 얼마나 올랐나”를 봅니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["앞으로 내줘야 할 연금", "부채", "liability"],
             ["부채를 갚을 수 있는 비율", "적립비율", "funded ratio"],
             ["돈이 얼마나 멀리 있나", "듀레이션", "duration"],
             ["부채에 맞춰 굴리기", "부채연계투자", "liability-driven investing"],
             ["목표에서 시작하기", "목표기반투자", "goal-based investing"]],
      widths: [4.30, 3.60, 3.89], emph: 1,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["자산이 5% 늘면 좋은 해인가?", "부채를 봐야 안다", "부채이 더 늘면 나빠진 것이다"],
             ["금리 1%p에 18년짜리는?", "약 18% 움직인다", "듀레이션만큼 흔들린다"],
             ["2022년 영국의 진짜 문제는?", "빌린 돈과 담보", "방향이 아니라 버티는 힘이었다"]],
      widths: [4.30, 3.20, 4.29], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 이 덱의 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["연기금의 성적표는 부채이 정합니다.",
                   "그 부채은 금리에 크게 흔들리고,",
                   "개인에게는 그 자리를 목표가 대신합니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W07_M8 · LDI 부채연계투자", "W07_M9 · GBI 목표기반투자"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
