// W02 사전학습 — M2 자산배분과 CAPM
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w02",
  out: "W02_자산배분과CAPM/W02_0_프라이머_자산배분은왜종목보다중요한가.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W02 사전학습",
  coverTitle: "자산배분은 왜\n종목보다 중요한가",
  coverSub: "W02 사전학습 · M2 자산배분과 CAPM",
  chain: ["큰 덩어리 나누기", "남는 위험 β", "그만큼의 보상"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "무엇이 결과를 가르나", kicker: "종목이 아니다",
      desc: "결정의 순서 · 91.5%라는 숫자" },
    { num: "02", title: "사라지는 위험", kicker: "나눠 담으면 없어진다",
      desc: "종목 수를 늘릴 때 · 끝내 남는 것" },
    { num: "03", title: "남는 위험의 값", kicker: "시장을 얼마나 따라가나",
      desc: "β 읽는 법 · 보상받는 위험" },
    { num: "04", title: "수식 하나", kicker: "그 보상을 적는다",
      desc: "CAPM 한 줄 · 기호 읽기" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "무엇이 결과를 가르나",
      sub: "종목을 잘 고르는 일이 아닙니다" },

    { type: "fig", file: "order.png",
      title: "연기금은 종목보다 큰 덩어리를 먼저 정합니다",
      punch: ["주식과 채권을 몇 대 몇으로 나눌지가 첫 결정입니다.",
              { text: "그다음에야 무엇을 담을지를 정합니다.", color: C.red }] },

    { type: "fig", file: "bhb.png",
      title: "수익이 오르내린 이유의 91.5%가 그 첫 결정에서 나옵니다",
      punch: ["미국 연기금 91곳을 10년간 뜯어본 결과입니다.",
              { text: "종목 고르기와 매매 시점은 다 합쳐도 8.5%였습니다.", color: C.red }] },

    { type: "divider", num: "02", title: "사라지는 위험",
      sub: "나눠 담으면 없어지는 위험과, 끝내 남는 위험이 있습니다" },

    { type: "fig", file: "diversify.png",
      title: "종목을 늘리면 위험이 줄지만 어느 선에서 멈춥니다",
      punch: ["한 종목만 가지면 26%씩 출렁이지만, 여러 개로 나누면 빠르게 줄어듭니다.",
              { text: "그러나 12.5% 아래로는 내려가지 않습니다. 시장 전체가 흔들리기 때문입니다.", color: C.red }] },

    { type: "cards", title: "그래서 위험은 두 종류로 나뉩니다",
      cards: [{ cap: "나눠 담으면 사라진다", title: "그 회사만의 사정",
                bullets: ["공장에 불이 났다", "신제품이 실패했다", "여럿에 나누면 상쇄된다"] },
              { kind: "dark", cap: "아무리 나눠도 남는다", title: "모두가 함께 겪는 일",
                bullets: ["금리가 올랐다", "경기가 꺾였다", "피할 곳이 없다"] },
              { kind: "lime", cap: "그래서", title: "남는 위험만 보상받는다",
                bullets: ["피할 수 있는 위험에", "값을 쳐줄 이유가 없다"] }],
      punch: [{ text: "피할 수 있었는데 피하지 않은 위험에는 아무도 값을 쳐주지 않습니다.", color: C.red }] },

    { type: "divider", num: "03", title: "남는 위험의 값",
      sub: "그 남는 위험을 얼마나 짊어졌는지를 재는 자가 β입니다" },

    { type: "fig", file: "beta_scatter.png",
      title: "β는 시장이 1% 움직일 때 따라 움직이는 폭입니다",
      punch: ["점을 뿌리고 직선을 하나 그으면, 그 기울기가 β입니다.",
              { text: "1보다 크면 시장보다 더 출렁이고, 작으면 덜 출렁입니다.", color: C.red }] },

    { type: "fig", file: "sml.png",
      title: "β가 클수록 더 많은 수익을 요구해야 합니다",
      punch: ["더 많이 짊어졌으면 더 받아야 합니다. 선 위의 점들이 그 값입니다.",
              { text: "선 아래에 있다면 위험에 비해 덜 주는 것입니다.", color: C.red }] },

    { type: "divider", num: "04", title: "수식 하나",
      sub: "지금까지의 이야기가 한 줄로 적힙니다" },

    { type: "eq", file: "equation.png", cap: "이 자산에 요구할 수익",
      title: "요구할 수익은 두 조각의 합입니다",
      cards: [{ cap: "rf", title: "안 굴려도 주는 것" },
              { cap: "E[rm] − rf", title: "시장에 준 웃돈" },
              { cap: "β", title: "얼마나 짊어졌나" },
              { kind: "lime", cap: "E[ri]", title: "요구할 수익" }],
      punch: [{ text: "가만히 둬도 받는 몫에, 짊어진 만큼의 웃돈을 더한 값입니다.", color: C.teal },
              { text: "β가 0이면 웃돈이 없습니다. 위험을 안 졌으니 보상도 없습니다.", color: C.red }] },

    { type: "cards", title: "이 셋만 피하면 강의가 훨씬 쉬워집니다",
      cards: [{ cap: "오해 1", title: "위험한 만큼 번다",
                bullets: ["피할 수 있는 위험은", "값을 쳐주지 않는다"] },
              { cap: "오해 2", title: "종목 고르기가 핵심",
                bullets: ["결과의 91.5%는", "큰 덩어리에서 갈린다"] },
              { kind: "dark", cap: "오해 3", title: "β가 크면 좋은 자산",
                bullets: ["좋고 나쁨이 아니다", "많이 짊어졌다는 뜻"] }],
      punch: [{ text: "CAPM은 좋은 자산을 고르는 법이 아니라, 값이 맞는지 재는 자입니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["큰 덩어리 나누기", "전략적 자산배분", "strategic asset allocation"],
             ["나눠 담으면 사라지는 위험", "고유위험", "idiosyncratic risk"],
             ["아무리 나눠도 남는 위험", "체계적 위험", "systematic risk"],
             ["시장을 따라 움직이는 폭", "베타", "beta"],
             ["시장에 준 웃돈", "시장위험 프리미엄", "market risk premium"]],
      widths: [4.10, 3.60, 4.09], emph: 2,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["종목을 50개로 늘리면?", "12.5%에서 멈춘다", "시장 전체가 흔들리는 몫은 안 사라진다"],
             ["β가 0인 자산의 요구수익은?", "rf 그대로", "짊어진 위험이 없으니 웃돈도 없다"],
             ["결과를 가장 크게 가르는 결정은?", "큰 덩어리 나누기", "오르내림의 91.5%가 여기서 갈린다"]],
      widths: [4.30, 3.10, 4.39], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 91.5%를 뺀 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["결과는 종목이 아니라 큰 덩어리에서 갈립니다.",
                   "피할 수 있는 위험에는 값이 붙지 않고,",
                   "남는 위험만 그 크기만큼 보상받습니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W02 · 자산배분과 CAPM", "W02 · 케이스 GPFG 알파의 진위"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
