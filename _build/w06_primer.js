// W06 사전학습 — M7 동적 자산배분 · SS2 재균형 프리미엄
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w06",
  out: "W06_동적포트폴리오와장기투자/W06_0_프라이머_글라이드패스와재균형은무엇을바꾸나.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W06 사전학습",
  coverTitle: "글라이드패스와 재균형은\n무엇을 바꾸나",
  coverSub: "W06 사전학습 · M7 동적 자산배분 · SS2 재균형 프리미엄",
  chain: ["나이가 든다", "비중이 틀어진다", "되돌린다"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "사람도 자산이다", kicker: "앞으로 벌 월급",
      desc: "젊음이라는 재산 · 월급은 채권을 닮았다" },
    { num: "02", title: "나이 따라 바꾼다", kicker: "글라이드패스",
      desc: "젊을 때 많이 · 은퇴가 가까우면 줄인다" },
    { num: "03", title: "출렁임의 값", kicker: "평균이 다가 아니다",
      desc: "오르고 내리면 제자리가 아니다 · 수식 하나" },
    { num: "04", title: "되돌리기", kicker: "틀어진 비중을 제자리로",
      desc: "저절로 틀어진다 · 되돌리면 생기는 몫" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "사람도 자산이다",
      sub: "통장에 든 돈만 재산이 아닙니다" },

    { type: "fig", file: "human_capital.png",
      title: "젊을 때 가장 큰 재산은 앞으로 벌 월급입니다",
      punch: ["스물다섯에는 재산의 대부분이 아직 벌지 않은 월급입니다.",
              { text: "월급은 꼬박꼬박 들어오니 채권을 닮았습니다.", color: C.red }] },

    { type: "cards", title: "그래서 나이에 따라 답이 달라집니다",
      cards: [{ cap: "젊을 때", title: "채권을 이미 많이 가진 셈",
                bullets: ["월급이 채권 노릇을 한다", "그래서 주식을 더 담아도 된다"] },
              { cap: "나이 들면", title: "그 채권이 줄어든다",
                bullets: ["앞으로 받을 월급이 적다", "돈으로 채워야 한다"] },
              { kind: "lime", cap: "그래서", title: "비중을 서서히 옮긴다",
                bullets: ["한 번 정하고 끝이 아니다", "시간이 답을 바꾼다"] }],
      punch: [{ text: "같은 사람에게도 나이에 따라 다른 답이 맞습니다.", color: C.red }] },

    { type: "divider", num: "02", title: "나이 따라 바꾼다",
      sub: "미리 정해 둔 경로를 따라 서서히 옮깁니다" },

    { type: "fig", file: "glide.png",
      title: "비행기가 내려앉듯 주식 비중을 서서히 낮춥니다",
      punch: ["언제 얼마로 바꿀지를 미리 정해 두고 그대로 따릅니다.",
              { text: "시장을 보고 그때그때 정하지 않는 것이 핵심입니다.", color: C.red }] },

    { type: "divider", num: "03", title: "출렁임의 값",
      sub: "평균만 보면 놓치는 것이 있습니다" },

    { type: "fig", file: "arith_geo.png",
      title: "오르고 같은 폭으로 내리면 제자리가 아닙니다",
      punch: ["+50% 뒤 −50%면 평균은 0%인데 내 돈은 75가 됩니다.",
              { text: "출렁일수록 더 깎입니다. 그래서 변동성을 줄이는 일이 곧 버는 일입니다.", color: C.red }] },

    { type: "eq", file: "equation.png", cap: "실제로 손에 남는 수익",
      title: "그 깎이는 몫을 한 줄로 적습니다",
      cards: [{ cap: "μ", title: "해마다의 평균" },
              { cap: "σ", title: "얼마나 출렁이나" },
              { cap: "σ² / 2", title: "깎이는 몫" },
              { kind: "lime", cap: "g", title: "손에 남는 수익" }],
      punch: [{ text: "변동성이 20%면 해마다 2%p씩 깎입니다. 35%면 6%p입니다.", color: C.teal },
              { text: "출렁임은 불편함이 아니라 실제로 돈을 깎는 비용입니다.", color: C.red }] },

    { type: "divider", num: "04", title: "되돌리기",
      sub: "정해 둔 비중은 가만히 두면 저절로 틀어집니다" },

    { type: "fig", file: "drift.png",
      title: "그냥 두면 비중이 정해 둔 값에서 멀어집니다",
      punch: ["더 오른 쪽이 저절로 커지고 덜 오른 쪽이 작아집니다.",
              { text: "아무것도 안 했는데 내가 정한 적 없는 배분이 되어 있습니다.", color: C.red }] },

    { type: "fig", file: "rebalance.png",
      title: "같은 배분이라도 되돌리면 결과가 달라집니다",
      punch: ["오른 것을 조금 팔고 내린 것을 조금 사는 일을 해마다 반복합니다.",
              { text: "그것만으로 생긴 몫이 있습니다. 이것을 재균형 프리미엄이라 부릅니다.", color: C.red }] },

    { type: "cards", title: "이 셋만 피하면 강의가 훨씬 쉬워집니다",
      cards: [{ cap: "오해 1", title: "한 번 정하면 끝",
                bullets: ["나이가 답을 바꾼다", "비중도 저절로 틀어진다"] },
              { cap: "오해 2", title: "평균 수익이 내 수익",
                bullets: ["출렁일수록 깎인다", "평균과 손에 남는 건 다르다"] },
              { kind: "dark", cap: "오해 3", title: "되돌리기는 시장 예측",
                bullets: ["맞히는 게 아니다", "정해 둔 규칙을 지킬 뿐"] }],
      punch: [{ text: "되돌리기는 예측이 아니라 규율입니다. 오를 때 팔고 내릴 때 사게 만듭니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["앞으로 벌 월급", "인적자본", "human capital"],
             ["나이 따라 바꾸는 경로", "글라이드패스", "glide path"],
             ["손에 남는 수익", "기하평균 수익률", "geometric return"],
             ["틀어진 비중을 되돌리기", "재균형", "rebalancing"],
             ["되돌려서 생긴 몫", "재균형 프리미엄", "rebalancing premium"]],
      widths: [4.10, 3.90, 3.79], emph: 4,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["+50% 뒤 −50%면?", "75가 된다", "평균 0%여도 25%가 사라진다"],
             ["변동성 20%의 값은?", "해마다 2%p", "σ² ÷ 2 만큼 깎인다"],
             ["되돌리기는 예측인가?", "아니다", "정해 둔 규칙을 지키는 일이다"]],
      widths: [3.90, 3.10, 4.79], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 이 덱의 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["시간은 답을 바꿉니다.",
                   "출렁임은 실제로 돈을 깎고,",
                   "되돌리기는 그 깎인 몫을 조금 되찾습니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W06 · 동적 포트폴리오와 장기투자", "W06 · 특별세션 SS2 재균형 프리미엄"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
