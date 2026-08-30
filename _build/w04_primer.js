// W04 사전학습 — M4 평균-분산 최적화 · M5 블랙-리터맨
const { build, C } = require("./primer_deck.js");

module.exports = {
  art: "w04",
  out: "W04_MVO와블랙리터맨/W04_0_프라이머_MVO와블랙리터맨은무엇을푸는가.pptx",
  eyebrow: "연기금 운용전략과 성과평가 · W04 사전학습",
  coverTitle: "MVO와 블랙-리터맨은\n무엇을 푸는가",
  coverSub: "W04 사전학습 · M4 평균-분산 최적화 · M5 블랙-리터맨",
  chain: ["변동성 σ", "상관계수 ρ", "섞은 뒤 σₚ"],

  agendaTitle: "네 구획이면 30분 안에 읽힙니다",
  agenda: [
    { num: "01", title: "준비물 셋", kicker: "강의가 전제하는 것",
      desc: "변동성 · 상관계수 · 섞기" },
    { num: "02", title: "수식 하나", kicker: "작아지는 만큼을 적는다",
      desc: "두 자산 분산식 · 기호 읽기 · ρ의 자리" },
    { num: "03", title: "M4의 답과 한계", kicker: "곡선 위에서 고른다",
      desc: "효율적 투자선 · 입력이 바뀔 때" },
    { num: "04", title: "M5의 전환", kicker: "방향을 거꾸로 돌린다",
      desc: "시장이 매긴 값 · 확신의 크기" },
  ],
  agendaBanner: "이 덱은 강의를 요약하지 않습니다. 강의 첫 장을 읽을 수 있게 만듭니다.",

  slides: [
    { type: "divider", num: "01", title: "준비물 셋",
      sub: "강의가 “다들 아시죠?” 하고 넘어가는 것만 모았습니다" },

    { type: "fig", file: "two_shops.png",
      title: "한쪽이 나쁠 때 다른 쪽이 좋으면 합은 얌전해집니다",
      punch: ["세 가게의 하루 평균은 모두 66만원으로 같습니다.",
              { text: "다른 것은 들쭉날쭉한 정도뿐입니다 — 39 · 38 그리고 2.", color: C.red }] },

    { type: "fig", file: "spread.png",
      title: "평균이 같아도 변동성이 다르면 다른 자산입니다",
      punch: ["투자에서 위험은 대개 “얼마나 들쭉날쭉한가”를 뜻합니다.",
              { text: "그 변동성을 재는 자가 표준편차 σ입니다.", color: C.red }] },

    { type: "fig", file: "corr3.png",
      title: "나눠 담기의 이득은 오직 상관계수 ρ가 정합니다",
      punch: ["상관계수 ρ는 둘이 같이 움직이는 정도를 −1과 +1 사이 숫자 하나로 나타낸 값입니다.",
              { text: "+1이면 이득이 없고, −1이면 이득이 가장 큽니다.", color: C.red }] },

    { type: "fig", file: "mix_smooth.png",
      title: "방향이 반대면 섞은 쪽이 둘 중 어느 것보다 얌전합니다",
      punch: ["가와 나는 매달 3% 안팎으로 출렁입니다.",
              { text: "반씩 섞으면 1%도 출렁이지 않습니다.", color: C.red }] },

    { type: "divider", num: "02", title: "수식 하나",
      sub: "이 덱에서 눈에 익혀 둘 것은 이 식 하나뿐입니다" },

    { type: "eq", file: "equation.png", cap: "두 자산을 섞었을 때의 변동성",
      title: "그 작아지는 만큼을 식 하나가 설명합니다",
      cards: [{ cap: "w₁, w₂", title: "얼마씩 담는가" },
              { cap: "σ₁, σ₂", title: "각각의 변동성" },
              { cap: "ρ", title: "상관계수" },
              { kind: "lime", cap: "σₚ", title: "섞은 뒤 변동성" }],
      punch: [{ text: "마지막 항에만 ρ가 있습니다. ρ가 음수면 이 항이 빠집니다.", color: C.teal },
              { text: "그래서 섞으면 변동성이 줄어듭니다.", color: C.red }] },

    { type: "fig", file: "rho_effect.png",
      title: "ρ 하나만 바꿔도 변동성이 15%에서 5%로 내려갑니다",
      punch: ["변동성 20%와 10%인 두 자산을 반씩 담은 결과입니다.",
              { text: "그냥 반씩 더한 15%에서 깎인 만큼이 나눠 담기의 이득입니다.", color: C.red }] },

    { type: "divider", num: "03", title: "M4의 답과 한계",
      sub: "곡선을 그리고 그 위에서 한 점을 고릅니다" },

    { type: "fig", file: "frontier.png",
      title: "비중을 0%부터 100%까지 다 해보면 고를 곡선이 나옵니다",
      punch: ["같은 변동성이면 더 버는 쪽, 같은 수익이면 덜 흔들리는 쪽을 고릅니다.",
              { text: "이 곡선 위에서 한 점을 고르는 일이 평균-분산 최적화입니다.", color: C.red }] },

    { type: "fig", file: "unstable.png",
      title: "예상 수익률을 1%p 올리면 답이 통째로 뒤집힙니다",
      punch: ["나 자산은 18%에서 100%로, 다 자산은 82%에서 0%로 갔습니다.",
              { text: "앞으로 벌 수익은 아무도 모르는데, 그 값이 답을 좌우합니다.", color: C.red }] },

    { type: "divider", num: "04", title: "M5의 전환",
      sub: "맞히기 어려운 것을 넣지 않고, 이미 있는 것에서 꺼냅니다" },

    { type: "fig", file: "bl_flow.png",
      title: "블랙-리터맨은 계산의 방향을 거꾸로 돌립니다",
      punch: ["시장에 이미 매겨진 비중은 누구나 볼 수 있습니다.",
              { text: "출발점을 “맞혀야 하는 값”에서 “이미 있는 값”으로 바꾼 것이 전부입니다.", color: C.red }] },

    { type: "fig", file: "confidence.png",
      title: "내 생각은 확신의 크기만큼만 반영됩니다",
      punch: ["시장은 30%라 하고 나는 70%라 합니다. 답은 그 사이입니다.",
              { text: "확신을 숫자로 적게 만든 것이 이 방법의 진짜 기여입니다.", color: C.red }] },

    { type: "cards", title: "이 셋만 피하면 강의가 훨씬 쉬워집니다",
      cards: [{ cap: "오해 1", title: "많이 나눌수록 안전",
                bullets: ["ρ가 정한다", "개수는 상관없다"] },
              { cap: "오해 2", title: "나온 비중이 정답",
                bullets: ["입력 바뀌면 답도 바뀐다", "얼마나 튼튼한지 본다"] },
              { kind: "dark", cap: "오해 3", title: "더 잘 맞히는 예측",
                bullets: ["예측이 아니다", "섞는 방법이다"] }],
      punch: [{ text: "셋 다 “섞는 방법”을 “맞히는 방법”으로 잘못 읽은 것입니다.", color: C.red }] },

    { type: "table", title: "이 덱의 말과 강의본의 말을 이어 둡니다",
      head: ["이 덱에서 쓴 말", "강의본이 쓰는 말", "영어"],
      rows: [["변동성을 재는 자", "표준편차", "standard deviation"],
             ["−1에서 +1 사이의 값 ρ", "상관계수", "correlation"],
             ["가장 덜 흔들리게 섞기", "평균-분산 최적화", "mean-variance optimization"],
             ["좋은 조합을 이은 선", "효율적 투자선", "efficient frontier"],
             ["시장이 매긴 수익률", "균형 수익률", "equilibrium return"]],
      widths: [4.10, 3.60, 4.09], emph: 2,
      banner: "강의본은 가운데 말을 씁니다. 이 표가 둘 사이의 다리입니다." },

    { type: "table", title: "답을 맞춰 보고 강의로 넘어가십시오",
      head: ["강의 전에 답해 볼 것", "답", "왜 그런가"],
      rows: [["ρ가 0이면 15%보다?", "작다 · 11.2%", "깎인 3.8%p가 나눠 담기의 이득"],
             ["ρ가 +1이면 이득은?", "없다 · 15% 그대로", "개수가 아니라 ρ가 정한다"],
             ["1%p로 답이 뒤집히면?", "믿기 어렵다", "M5가 바로 이 문제를 다룬다"]],
      widths: [3.90, 3.30, 4.59], rowH: 0.86, dy: 0.10,
      punch: [{ text: "세 개를 다 맞혔다면 강의본 첫 장이 그대로 읽힙니다.", color: C.red }],
      punchY: 5.86, note: "※ 이 덱의 숫자는 모두 수업용으로 지어낸 예시입니다." },

    { type: "closing",
      statements: ["강의는 이 준비물 위에서 시작합니다.",
                   "먼저 M4로 곡선을 그리고,",
                   "그다음 M5로 방향을 거꾸로 돌립니다."],
      message: "이제 강의본으로\n넘어가십시오",
      contacts: ["W04_M4 · MVO와 공분산 추정", "W04_M5 · 블랙-리터맨"],
      note: "※ 4교시는 모의 투자위원회입니다. 실제 시장 자료와 정확한 정의는 강의본과 실습데이터 덱에서 다룹니다." },
  ],
};

if (require.main === module) build(module.exports);
