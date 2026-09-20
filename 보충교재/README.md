# 보충교재

16주 과정 밖에서 읽는 자료다. **주차 진도에 묶이지 않는다** — 특정 주차를 더 파고들고
싶을 때, 또는 학기 시작 전에 감을 잡고 싶을 때 꺼내 본다.

본 과정 덱과 달리 여기 있는 것은 **한 주제를 끝까지 따라가는 단독 덱**이다.
케이스도 실습데이터도 붙지 않는다. 읽고 끝내는 자료다.

---

## 무엇이 있나

| 자료 | 쪽 | 무엇을 다루나 | 함께 보면 좋은 주차 |
|---|---:|---|---|
| [`quant_investing_motivation.pdf`](quant_investing_motivation.pdf) | 50 | 퀀트 인베스팅 전반 — 정의 · 팩터 · 포트폴리오 구축 · FLAM · 주요 운용사 | 과정 시작 전 · W10 · W12 |
| [`W03_BuildingBlock_CMA_ZeroOne.pdf`](W03_BuildingBlock_CMA_ZeroOne.pdf) | 45 | Building Block CMA — 28개 자산군의 수익률을 여덟 개 블록으로 분해한다 | **W03 연기금모델과CMA** |
| [`BlackRock_Boracay_LongTerm_CMA.pdf`](BlackRock_Boracay_LongTerm_CMA.pdf) | 42 | 장기 자본시장가정(CMA) — 미국 ERP, 주식·채권 기대수익 추정 (BlackRock Boracay Phase 1 · Topic 5) | **W03 연기금모델과CMA** |
| [`W03_Macro_First_CMA_ZeroOne.pdf`](W03_Macro_First_CMA_ZeroOne.pdf) | 42 | Macro-first Building Block — GDP·인플레이션에서 시작해 모든 자산군으로 내려온다 | **W03 연기금모델과CMA** |
| [`stock-data-architecture-review.pdf`](stock-data-architecture-review.pdf) | 40 | 주식 데이터 아키텍처 검토와 제안 — CRSP·Compustat·WRDS 구독 범위, 회사-종목 연결, PIT 재무, 상장폐지 처리 | W10 주식퀀트모델 · XS · [실습 데이터 가이드](../_%EA%B3%BC%EC%A0%95%EC%9A%B4%EC%98%81/) |
| [`Moskowitz_Quality_Defensive_Investing.pdf`](Moskowitz_Quality_Defensive_Investing.pdf) | 36 | Quality·Defensive 투자 — 좋은 기업을 합리적 가격에, 안전한 자산에 레버리지를 (Yale SOM Master Class) | **W12 팩터투자** |
| [`13F_Predatory_Trading_3Agent_MBA_Deck.pdf`](13F_Predatory_Trading_3Agent_MBA_Deck.pdf) | 36 | 13F 전략적 공시와 포식적 거래 — 3-Agent 동적 게임 | **W15 TPA** · W10 |
| [`FamaFrench_Model_ZeroOne.pdf`](FamaFrench_Model_ZeroOne.pdf) | 29 | Fama-French 3요인 모델 — 이상현상에서 팩터로, 25 포트폴리오 구성법 | **W12 팩터투자** |
| [`TPA_Framework_Brief_Deck_v01.pdf`](TPA_Framework_Brief_Deck_v01.pdf) | 28 | TPA 설계 프레임 v0.1 — 밖의 자산·부채 → 헤지 가능성 R² → 딜 심사 → 거버넌스 세 조건, 5단계 절차와 명제 7개 | **W15 TPA** · W07 LDI |
| [`0. Stylized Facts and SDF.pdf`](0.%20Stylized%20Facts%20and%20SDF.pdf) | 21 | 수익률의 세 가지 정형화된 사실과 확률할인요인(SDF) | 과정 시작 전 · W02 |
| [`Barberis_PE_Habit_Extrapolation_deck.pdf`](Barberis_PE_Habit_Extrapolation_deck.pdf) | 18 | 시장 P/E는 왜 한 세기 동안 출렁였는가 — Habit Formation과 과잉 외삽 | W06 동적포트폴리오와장기투자 |

11개 · 387쪽. CMA만 세 편이라 W03은 따로 묶어 본다.

---

## 어떻게 쓰나

**학기 전에** — `quant_investing_motivation`과 `0. Stylized Facts and SDF`를 먼저 본다.
이 과정이 무엇을 다루는지, 왜 팩터라는 말이 계속 나오는지가 잡힌다.

**W03 CMA는 세 편이 한 묶음이다.** `Macro_First`가 GDP·인플레이션에서 출발하는 틀을 세우고,
`BuildingBlock`이 그 틀로 28개 자산군을 분해하며, `BlackRock_Boracay`가 실제 운용사의
적용 사례를 보여 준다. 이 순서로 읽으면 본 강의가 결론만 쓰는 대목의 근거가 메워진다.

**주차 중에** — 위 표의 오른쪽 열을 따라간다. 해당 주차 강의본을 보고 나서 읽으면
그 주의 개념이 원전에서 어떻게 나왔는지 이어진다. 특히 W03의 CMA와 W12의 팩터는
본 강의가 결론만 쓰는 대목이라, 근거를 보려면 여기를 봐야 한다.

**IC 케이스를 준비할 때** — `13F_Predatory_Trading`은 W15 TPA 케이스에서 다루는
"공시가 전략을 노출시킨다"는 문제를 게임이론으로 푼다. 의결문에 쓸 반론을 찾을 때 쓴다.

**W15 TPA는 두 편이 짝이다.** `TPA_Framework_Brief_Deck`이 "TPA를 도입할지"가 아니라
"어느 기능에 얼마짜리 가치가 있는지"를 재는 5단계 절차를 세우고(리밸런싱 0~6bp 대 딜 심사
227bp), `13F_Predatory_Trading`이 그 심사 결과가 공시로 새어 나갈 때의 문제를 다룬다.
강의본을 본 뒤 프레임 → 13F 순서로 읽는다.

**실습 데이터를 직접 만들 때** — `stock-data-architecture-review`는 백테스트·라이브트레이딩용
주가·재무 DB를 어떻게 쌓았고 무엇이 막혔는지 검토한 자료다. CRSP·Compustat·TAQ가 어디까지
구독돼 있는지, 회사-종목 연결이 왜 절반에서 끊기는지, PIT 재무를 무료로 확보하는 길(SEC EDGAR
XBRL)이 정리돼 있다. W10 퀀트 모델과 XS 자율주행 포트폴리오에서 yfinance 밖의 데이터를
쓰려 할 때 먼저 본다.

---

## 알아둘 것

- **본 과정 덱이 아니다.** 시험 범위에 들어가지 않는다. 배치표
  ([`_과정운영/16주_커리큘럼_배치표.md`](../_%EA%B3%BC%EC%A0%95%EC%9A%B4%EC%98%81/16%EC%A3%BC_%EC%BB%A4%EB%A6%AC%ED%81%98%EB%9F%BC_%EB%B0%B0%EC%B9%98%ED%91%9C.md))에도 없다.
- 일부는 **외부 원전을 정리한 것**이다(BlackRock Boracay, Yale SOM Master Class).
  `stock-data-architecture-review`는 내부 데이터 구축 보고서를 검토한 것이라(작성자·이슈 번호는 지웠다)
  구독 범위·일정은 2026년 9월 시점 기준이다.
  인용할 때는 표지에 적힌 출처를 그대로 쓴다.
- 여기에는 **PDF만 둔다.** 저장소 규칙대로 편집 원본 PPTX는 올리지 않는다.
