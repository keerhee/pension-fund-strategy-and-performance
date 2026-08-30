// W03 사전학습 — M3 연기금 3대 모델과 CMA
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w03",
  out: "W03_연기금모델과CMA/W03_0_프라이머_자본시장가정은어떻게세우나.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W03 사전학습",
  coverTitle: "자본시장 가정은\n어떻게 세우나",
  coverSub: "W03 사전학습 · M3 연기금 3대 모델과 자본시장 가정",
  chain: ["세 가지 길", "가정 세우기", "그 가정의 무게"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "세 가지 길", kicker: "정답은 하나가 아니다",
      desc: "노르웨이 · 캐나다 · 예일" },
    { num: "02", title: "가정을 세운다", kicker: "예측이 아니라 가정이다",
      desc: "조각을 쌓는 법 · 10년이라는 기간" },
    { num: "03", title: "기관마다 다르다", kicker: "같은 자산, 다른 숫자",
      desc: "여섯 기관 비교 · 왜 갈리나" },
    { num: "04", title: "가정의 무게", kicker: "1%p가 30년을 바꾼다",
      desc: "복리로 벌어지는 격차" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "세 가지 길",
      sub: "“우리 돈을 누가, 어떻게 굴릴 것인가”에 대한 세 답" },

    { type: "fig", file: "models.png",
      title: "같은 질문에 세 기관이 서로 다른 답을 냈습니다",
      punch: ["지수를 사거나, 직접 굴리거나, 잘 고르는 사람에게 맡기거나입니다.",
              { text: "셋 다 성공했습니다. 정답이 하나가 아니라는 뜻입니다.", color: C.red }] },

    { type: "cards", title: "무엇을 고르든 먼저 답해야 할 것은 같습니다",
      cards: [{ cap: "사람", title: "누가 굴리나",
                bullets: ["안에서 뽑을까", "밖에 맡길까"] },
              { cap: "방식", title: "지수인가 선택인가",
                bullets: ["시장을 그대로 살까", "고르는 값을 낼까"] },
              { kind: "lime", cap: "그전에", title: "무엇을 기대하나",
                bullets: ["어느 길이든", "숫자를 먼저 정해야 한다"] }],
      punch: [{ text: "어느 길로 가든 “앞으로 얼마 벌 것으로 볼까”를 먼저 적어야 합니다.", color: C.red }] },

    { type: "divider", num: "02", title: "가정을 세운다",
      sub: "맞히는 일이 아니라, 근거를 적어 두는 일입니다" },

    { type: "fig", file: "blocks.png",
      title: "기대수익은 조각을 쌓아서 만듭니다",
      punch: ["배당으로 받는 몫, 기업이 더 벌어 오르는 몫, 사람들이 더 쳐줘서 오르는 몫입니다.",
              { text: "세 조각을 각각 근거와 함께 적으면, 어디서 틀렸는지 나중에 알 수 있습니다.", color: C.red }] },

    { type: "eq", file: "equation.png", cap: "10년 기대수익을 쌓는 법",
      title: "그 세 조각을 한 줄로 적습니다",
      cards: [{ cap: "D / P", title: "배당으로 받는 몫" },
              { cap: "g", title: "이익이 늘어서" },
              { cap: "Δ(P/E)", title: "값을 더 쳐줘서" },
              { kind: "lime", cap: "E[r]", title: "10년 기대수익" }],
      punch: [{ text: "앞의 두 조각은 기업이 만들고, 마지막 조각은 사람들의 마음이 만듭니다.", color: C.teal },
              { text: "마지막 조각이 가장 못 미더워서, 대개 0에 가깝게 둡니다.", color: C.red }] },

    { type: "divider", num: "03", title: "기관마다 다르다",
      sub: "같은 자산을 놓고도 숫자가 갈립니다" },

    { type: "fig", file: "cma_spread.png",
      title: "여섯 기관이 같은 주식에 다른 숫자를 적었습니다",
      punch: ["가장 낮은 곳과 높은 곳의 차이가 2.3%p입니다.",
              { text: "틀린 곳이 있어서가 아니라, 근거로 삼은 조각이 달라서입니다.", color: C.red }] },

    { type: "divider", num: "04", title: "가정의 무게",
      sub: "적어 둔 숫자 하나가 수십 년을 가릅니다" },

    { type: "fig", file: "sensitivity.png",
      title: "가정 1%p 차이가 30년 뒤에는 두 배 가까운 격차가 됩니다",
      punch: ["복리로 불어나기 때문에, 처음의 작은 차이가 끝에서 크게 벌어집니다.",
              { text: "그래서 가정을 정하는 회의가 종목을 고르는 회의보다 중요합니다.", color: C.red }] },

    { type: "cards", title: "이 셋만 피하면 강의가 훨씬 쉬워집니다",
      cards: [{ cap: "오해 1", title: "가정은 예측이다",
                bullets: ["맞히려는 게 아니다", "근거를 적어 두는 일"] },
              { cap: "오해 2", title: "기관마다 다르면 틀린 것",
                bullets: ["근거가 다를 뿐이다", "다름 자체가 정보다"] },
              { kind: "dark", cap: "오해 3", title: "모델 중 정답이 있다",
                bullets: ["셋 다 성공했다", "제약이 다를 뿐이다"] }],
      punch: [{ text: "가정은 맞히는 것이 아니라, 나중에 검증할 수 있게 적어 두는 것입니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["앞으로 얼마 벌 것으로 볼까", "자본시장 가정", "capital market assumptions"],
             ["조각을 쌓는 법", "빌딩 블록 접근", "building block approach"],
             ["더 벌어서 오르는 몫", "이익 성장", "earnings growth"],
             ["더 쳐줘서 오르는 몫", "밸류에이션 변화", "valuation change"],
             ["직접 굴린다", "내부 운용", "internal management"]],
      widths: [4.60, 3.30, 3.89], emph: 0,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["기대수익의 세 조각은?", "배당 · 이익성장 · 가격변화", "앞 둘은 기업이, 끝은 마음이"],
             ["기관마다 숫자가 다르면?", "근거가 다른 것", "틀림이 아니라 가정의 차이다"],
             ["가정 1%p의 무게는?", "30년 뒤 큰 격차", "복리로 벌어지기 때문이다"]],
      widths: [4.00, 3.90, 3.89], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 이 덱의 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["길은 하나가 아닙니다.",
                   "어느 길이든 숫자를 먼저 적어야 하고,",
                   "그 숫자 하나가 수십 년을 가릅니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W03 · 연기금 모델과 CMA", "W03 · 케이스 6개 기관 메타분석"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
