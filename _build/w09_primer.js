// W09 사전학습 — M10 위험관리와 성과평가
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w09",
  out: "W09_위험관리와성과평가/W09_0_프라이머_성과평가는무엇을견주는가.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W09 사전학습",
  coverTitle: "성과평가는\n무엇을 견주는가",
  coverSub: "W09 사전학습 · M10 위험관리와 성과평가",
  chain: ["변동성을 잰다", "잣대와 견준다", "실력인지 가린다"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "위험을 재는 법", kicker: "나쁠 때 얼마나 나쁜가",
      desc: "왼쪽 꼬리 · 흔한 일과 드문 일" },
    { num: "02", title: "값을 매기는 법", kicker: "수익만으로는 모른다",
      desc: "변동성 한 단위당 번 몫 · 수식 하나" },
    { num: "03", title: "무엇과 견줄까", kicker: "잣대를 먼저 정한다",
      desc: "잣대 없는 성적 · 어디서 갈렸나" },
    { num: "04", title: "실력인가 운인가", kicker: "짧은 기록은 못 가른다",
      desc: "필요한 햇수 · 필요한 폭" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "위험을 재는 법",
      sub: "“얼마나 흔들리나”보다 “나쁠 때 얼마나 나쁜가”를 봅니다" },

    { type: "fig", file: "var_tail.png",
      title: "위험은 분포의 왼쪽 꼬리에 있습니다",
      punch: ["가운데가 두툼한 것은 흔한 일이고, 왼쪽 끝이 드물지만 아픈 일입니다.",
              { text: "“백 번 중 다섯 번은 이보다 나쁘다”가 위험을 재는 한 방식입니다.", color: C.red }] },

    { type: "cards", title: "그런데 그 한 줄만으로는 부족합니다",
      cards: [{ cap: "묻는 것", title: "얼마나 나쁠 수 있나",
                bullets: ["백 번 중 다섯 번의 문턱", "그 선을 넘는 손실"] },
              { cap: "빠진 것", title: "넘어간 뒤가 문제다",
                bullets: ["문턱만 알려 준다", "그 너머는 말이 없다"] },
              { kind: "lime", cap: "그래서", title: "꼬리의 평균도 본다",
                bullets: ["나쁠 때의 평균 손실", "이쪽이 더 정직하다"] }],
      punch: [{ text: "문턱을 아는 것과 그 너머를 아는 것은 다릅니다. 2008년이 그 차이를 가르쳤습니다.", color: C.red }] },

    { type: "divider", num: "02", title: "값을 매기는 법",
      sub: "같은 수익이라도 얼마나 조마조마했는지가 다릅니다" },

    { type: "fig", file: "two_funds.png",
      title: "끝값이 같아도 두 펀드의 값은 다릅니다",
      punch: ["가 펀드는 얌전히, 나 펀드는 크게 출렁이며 같은 곳에 닿았습니다.",
              { text: "변동성 한 단위당 얼마나 벌었는지로 견주면 차이가 드러납니다.", color: C.red }] },

    { type: "eq", file: "equation.png", cap: "변동성 한 단위당 번 몫",
      title: "그 비교를 한 줄로 적습니다",
      cards: [{ cap: "rp", title: "내가 번 몫" },
              { cap: "rf", title: "안 굴려도 받는 몫" },
              { cap: "σp", title: "얼마나 출렁였나" },
              { kind: "lime", cap: "SR", title: "변동성당 번 몫" }],
      punch: [{ text: "위험을 더 져서 번 것인지, 잘해서 번 것인지를 가르는 첫 자입니다.", color: C.teal },
              { text: "다만 크게 무너진 적이 있는지는 이 숫자 하나로 알 수 없습니다.", color: C.red }] },

    { type: "divider", num: "03", title: "무엇과 견줄까",
      sub: "잣대를 나중에 고르면 언제나 이겨 보이게 만들 수 있습니다" },

    { type: "fig", file: "benchmark.png",
      title: "잣대를 정하기 전에는 +8%가 좋은지 나쁜지 알 수 없습니다",
      punch: ["시장이 +12%였다면 뒤진 것이고, +3%였다면 앞선 것입니다.",
              { text: "그래서 잣대는 돈을 넣기 전에 정해 문서로 남깁니다.", color: C.red }] },

    { type: "fig", file: "attribution.png",
      title: "앞선 몫이 어디서 나왔는지를 갈라 놓습니다",
      punch: ["큰 덩어리를 잘 나눠서 번 것과, 그 안에서 잘 골라서 번 것은 다른 일입니다.",
              { text: "갈라 놓아야 다음에 무엇을 고칠지 알 수 있습니다.", color: C.red }] },

    { type: "divider", num: "04", title: "실력인가 운인가",
      sub: "가장 답하기 어려운 질문입니다" },

    { type: "fig", file: "luck.png",
      title: "짧은 기록으로는 실력과 운을 가를 수 없습니다",
      punch: ["1년치로 판단하려면 해마다 4%p는 앞서야 운이 아니라고 말할 수 있습니다.",
              { text: "대부분의 펀드 평가가 이 문턱을 넘지 못한 채 이뤄집니다.", color: C.red }] },

    { type: "cards", title: "이 셋만 피하면 강의가 훨씬 쉬워집니다",
      cards: [{ cap: "오해 1", title: "수익률이 성적표",
                bullets: ["얼마나 졌는지 모른다", "잣대도 없다"] },
              { cap: "오해 2", title: "위험은 변동성뿐",
                bullets: ["꼬리가 더 아프다", "평균은 조용하다"] },
              { kind: "dark", cap: "오해 3", title: "3년 성적이면 안다",
                bullets: ["운으로도 나온다", "햇수가 짧으면 못 가른다"] }],
      punch: [{ text: "좋은 평가는 “얼마 벌었나”가 아니라 “무엇을 견주었나”에서 시작합니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["백 번 중 다섯 번의 문턱", "VaR", "value at risk"],
             ["나쁠 때의 평균 손실", "CVaR · 기대손실", "expected shortfall"],
             ["변동성 한 단위당 번 몫", "샤프비율", "Sharpe ratio"],
             ["견줄 잣대", "벤치마크", "benchmark"],
             ["어디서 갈렸나", "성과 귀인", "performance attribution"]],
      widths: [4.30, 3.60, 3.89], emph: 2,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["끝값이 같은 두 펀드는?", "값이 다르다", "얼마나 조마조마했는지가 다르다"],
             ["잣대는 언제 정하나?", "돈을 넣기 전에", "나중에 고르면 늘 이겨 보인다"],
             ["3년 성적으로 실력을 아나?", "어렵다", "그 정도는 운으로도 나온다"]],
      widths: [4.30, 2.90, 4.59], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 이 덱의 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["위험은 평균이 아니라 꼬리에 있습니다.",
                   "성적은 잣대가 있어야 뜻이 생기고,",
                   "실력은 충분한 햇수가 있어야 보입니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W09 · 위험관리와 성과평가", "W09 · 케이스 국부펀드 2022 평가"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
