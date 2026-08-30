// W05 사전학습 — M6 리스크 패리티와 HRP
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w05",
  out: "W05_리스크패리티와HRP/W05_0_프라이머_리스크패리티는왜주식을줄이나.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W05 사전학습",
  coverTitle: "리스크 패리티는 왜\n주식을 줄이나",
  coverSub: "W05 사전학습 · M6 리스크 패리티와 HRP",
  chain: ["돈으로 나누기", "위험으로 나누기", "2022년의 반례"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "겉과 속이 다르다", kicker: "60 대 40의 착시",
      desc: "돈의 비율 · 위험의 비율" },
    { num: "02", title: "위험을 재는 법", kicker: "누가 얼마나 지고 있나",
      desc: "위험기여도 · 수식 하나" },
    { num: "03", title: "위험으로 맞추면", kicker: "비중이 확 달라진다",
      desc: "주식을 줄인다 · 빌려서 채운다" },
    { num: "04", title: "그래도 한계는 있다", kicker: "2022년이 드러낸 것",
      desc: "함께 내릴 때 · 빌린 돈의 값" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "겉과 속이 다르다",
      sub: "가장 흔한 배분인 60 대 40부터 뜯어봅니다" },

    { type: "fig", file: "capital_vs_risk.png",
      title: "돈은 60 대 40인데 위험은 94 대 6입니다",
      punch: ["주식이 채권보다 훨씬 크게 출렁이기 때문입니다.",
              { text: "60/40은 균형 잡힌 배분이 아니라, 사실상 주식 포트폴리오입니다.", color: C.red }] },

    { type: "fig", file: "seesaw.png",
      title: "무게가 같아도 앉는 자리가 다르면 균형이 아닙니다",
      punch: ["시소는 무게와 거리의 곱으로 균형을 잡습니다.",
              { text: "포트폴리오도 비중과 변동성의 곱으로 봐야 합니다.", color: C.red }] },

    { type: "divider", num: "02", title: "위험을 재는 법",
      sub: "누가 얼마나 지고 있는지를 숫자로 적습니다" },

    { type: "eq", file: "equation.png", cap: "이 자산이 지는 위험의 몫",
      title: "각자가 진 위험을 한 줄로 적습니다",
      cards: [{ cap: "w", title: "얼마씩 담았나" },
              { cap: "(Σw)", title: "밀어 올린 몫" },
              { cap: "σₚ", title: "전체 변동성" },
              { kind: "lime", cap: "RC", title: "이 자산이 진 위험" }],
      punch: [{ text: "각자의 몫을 다 더하면 전체 변동성이 됩니다. 그래서 “나눈다”고 말합니다.", color: C.teal },
              { text: "비중이 작아도 많이 출렁이면 큰 몫을 집니다.", color: C.red }] },

    { type: "divider", num: "03", title: "위험으로 맞추면",
      sub: "위험을 반반으로 만들려면 돈은 반반이 아닙니다" },

    { type: "fig", file: "equalize.png",
      title: "위험을 반반으로 맞추려면 주식은 22%만 담아야 합니다",
      punch: ["주식이 크게 출렁이므로, 조금만 담아도 위험의 절반을 채웁니다.",
              { text: "이렇게 맞춘 것을 리스크 패리티라고 부릅니다.", color: C.red }] },

    { type: "cards", title: "그런데 그러면 수익이 너무 작아집니다",
      cards: [{ cap: "문제", title: "채권이 대부분",
                bullets: ["안전해졌지만", "기대수익도 낮아졌다"] },
              { cap: "해법", title: "빌려서 키운다",
                bullets: ["같은 비율 그대로", "규모만 늘린다"] },
              { kind: "dark", cap: "대가", title: "빌린 돈에는 값이 있다",
                bullets: ["이자를 내야 한다", "금리가 오르면 아프다"] }],
      punch: [{ text: "리스크 패리티는 위험을 고르게 나눈 뒤, 빌려서 규모를 키우는 방법입니다.", color: C.red }] },

    { type: "divider", num: "04", title: "그래도 한계는 있다",
      sub: "2022년은 이 방법의 전제를 정면으로 흔들었습니다" },

    { type: "fig", file: "y2022.png",
      title: "주식과 채권이 함께 내린 해에는 이 방법이 더 아팠습니다",
      punch: ["채권을 많이 담고 빌려서 키웠는데, 그 채권이 함께 내렸습니다.",
              { text: "“둘은 반대로 움직인다”는 전제가 깨지면 방법도 함께 무너집니다.", color: C.red }] },

    { type: "cards", title: "이 셋만 피하면 강의가 훨씬 쉬워집니다",
      cards: [{ cap: "오해 1", title: "60/40은 균형이다",
                bullets: ["돈으로만 반반이다", "위험은 94 대 6"] },
              { cap: "오해 2", title: "위험을 나누면 안전하다",
                bullets: ["빌려서 키우면", "위험도 함께 커진다"] },
              { kind: "dark", cap: "오해 3", title: "언제나 60/40보다 낫다",
                bullets: ["2022년엔 더 아팠다", "전제가 깨지면 무너진다"] }],
      punch: [{ text: "어떤 방법도 전제 위에 서 있습니다. 그 전제를 아는 것이 이 주차의 목적입니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["이 자산이 진 위험의 몫", "위험기여도", "risk contribution"],
             ["위험을 고르게 나누기", "리스크 패리티", "risk parity"],
             ["빌려서 규모를 키우기", "레버리지", "leverage"],
             ["비슷한 것끼리 묶어 내려가기", "계층적 위험 패리티", "hierarchical risk parity"],
             ["기대수익을 안 쓴다", "μ를 쓰지 않는 배분", "no expected-return input"]],
      widths: [4.60, 3.60, 3.59], emph: 1,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["60/40에서 주식의 위험 몫은?", "94%", "주식이 훨씬 크게 출렁이기 때문"],
             ["위험을 반반으로 하려면?", "주식 22%만", "적게 담아도 위험은 금방 찬다"],
             ["2022년에 왜 더 아팠나?", "둘이 함께 내려서", "반대로 움직인다는 전제가 깨졌다"]],
      widths: [4.30, 2.90, 4.59], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 이 덱의 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["돈으로 반반은 위험으로 반반이 아닙니다.",
                   "위험으로 맞추면 비중이 확 달라지고,",
                   "그 방법도 전제가 깨지면 무너집니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W05 · 리스크 패리티와 HRP", "W05 · 케이스 기대수익률 포기"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
