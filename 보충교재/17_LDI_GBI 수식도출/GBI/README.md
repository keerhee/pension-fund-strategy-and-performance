# GBI — 요약·기초(03)와 Martellini 수식 도출 III(04 · 05), 참고 요약(06), Das 계열 원 논문 덱(08 · 13)

| 순서 | 파일 | 쪽 | 내용 |
|---|---|---:|---|
| 03 | [`03_GBI_Summary_Basics_zeroone.pdf`](03_GBI_Summary_Basics_zeroone.pdf) | 34 | **GBI 요약·기초 — 무엇을 풀고, 어떻게 배분하는가** — LDI에서 이어받는 것(부채 → 목표 · LHP → GHP · 적립비율 → 쿠션·Floor) → 위험 = 목표 미달 확률 → 목표를 값으로 재기(K · Floor = Retirement Bond) → 두 바구니(GHP · PSP · CPPI · Flexicure) → 확률로 말하는 목표 → 은퇴 이후 → 디폴트옵션 · 대학기금 케이스 · 기관 대 개인 한 장 요약 |
| 04 | [`04_Martellini_GBI_Derivations_III_zeroone.pdf`](04_Martellini_GBI_Derivations_III_zeroone.pdf) | 88 | **GBI 수식 도출 III — Martellini GBI** — 03의 식을 유도한다 — 기초 도구와 부채의 측정 · 두 블록 최적해와 CPPI · 확률로 말하는 목표 · 은퇴소득·인출·요양 · 방법들의 관계와 동치 |
| 05 | [`05_Martellini_GBI_Formula_Derivations_III.pdf`](05_Martellini_GBI_Formula_Derivations_III.pdf) | 41 | **GBI 수식 도출 III — 풀이 노트** — 04 덱의 문서판 — 절마다 풀려는 문제 → 답 → 단계별 풀이 → 이렇게 한다 → 숫자로 확인(md 수식 원문 포함) |
| 06 | [`06_Martellini_GBI_Summary.pdf`](06_Martellini_GBI_Summary.pdf) | 14 | **Martellini GBI 핵심 요약 (참고)** — 특강 II 마르텔리니 GBI 강의 덱 12종의 핵심 요약 |
| 07 | `07_Das_Markowitz_Scheid_Statman_2010_JFQA_원문.pdf` | 24 | 원문 — 저장소에 올리지 않음(.gitignore), 원문 링크 https://srdas.github.io/Papers/DMSS.pdf |
| 08 | [`08_Das_Markowitz_Mental_Accounts_zeroone.pdf`](08_Das_Markowitz_Mental_Accounts_zeroone.pdf) | 39 | **심리계정 포트폴리오 — Das · Markowitz · Scheid · Statman (2010)** — 원 논문 예 하나를 따라간다 — 확률 제약 → 분위수 조건 · 손계산(60 · 30 · 10 검사, 두 자산 w* 52.2%) · 행렬 일반화(A · B · C · D, g + v/γ, 은퇴 γ 3.795) · 세 계정과 합산(γ 2.174) · 가능성(−2.31%) · 롱온리 손풀이와 12bp · γ 오지정 손실 · M8 방법 1 · 2와의 연결. 원문 표와 재계산이 다른 곳은 장표 각주 |
| 09 | `09_Das_Ostrov_Radhakrishnan_Srivastav_2018_JOIM_GBWM_원문.pdf` | 27 | 원문 — 저장소에 올리지 않음(.gitignore), A New Approach to Goals-Based Wealth Management, JOIM 16(3) 2018, 원문 링크 https://srdas.github.io/Papers/GBWM.pdf |
| 10 | `10_Das_Ostrov_Radhakrishnan_Srivastav_2020_CMS_DynamicGBWM_원문.pdf` | 31 | 원문 — 저장소에 올리지 않음, Dynamic Portfolio Allocation in Goals-Based Wealth Management, CMS 17 2020 613–640(저자 사이트 판), 원문 링크 https://srdas.github.io/Papers/DP_Paper.pdf |
| 11 | `11_Das_Ostrov_Radhakrishnan_Srivastav_2022_JBF_MultiGoals_원문.pdf` | 47 | 원문 — 저장소에 올리지 않음, Dynamic Optimization for Multi-Goals Wealth Management, JBF 140 2022 106192, 원문 링크 https://srdas.github.io/Papers/MultWealthGoals.pdf |
| 12 | `12_Das_Ostrov_Radhakrishnan_Srivastav_EfficientGoalProbabilities_원문.pdf` | 17 | 원문 — 저장소에 올리지 않음, Efficient Goal Probabilities: A New Frontier, JOIM 21(3) 2023, 원문 링크 https://srdas.github.io/Papers/EGPF.pdf |
| 13 | [`13_GBWM_Series_DORS_zeroone.pdf`](13_GBWM_Series_DORS_zeroone.pdf) | 45 | **목표기반 자산관리(GBWM) 연작 — Das · Ostrov · Radhakrishnan · Srivastav 2018–2022** — 09~12 원문 요약과 활용법 — 계보(Roy → DMSS → DORS 네 편 · RL 후속) · 2018 효율선 위 목표 확률(3차식 · 원문 그림 점으로 역산한 효율선에서 86.6% 재현) · 2020 동적계획법(2기간 Bellman 손계산 · 10년 두 배 66.6% 대 원문 66.9% · 납입 · 인출 · 은퇴 DP 58.6% 대 TDF) · 2022 여러 목표(비용 · 효용 벡터 30 → 13 · 표 2 · 결정 구간 108~183 · 조합 폭발의 답) · EGP 확률 프런티어(최소 초기 자금 78.7 대 원문 79.9) · 비교표 · 흐름도 · M8 세 목표 DP 약 6.2억 · 디폴트옵션 · IRP · H대 대입 · Claude Code 프롬프트(gbwm_dp.py). 원문과 재계산이 다른 곳은 장표 각주 |

03은 LDI(01 · 02)를 들은 뒤 이어 본다. 04 덱과 05 노트는 같은 도출의 덱판 · 문서판이다. md는 $$ 수식(옵시디언 등).

## 도출 III에서 바뀐 점 (2026-10-04)

- 0-2 기호표에 금액·비율 구분 추가: k_ess·k_asp는 목표 G에 대한 비율, c·c_ess는 연소득 금액(원/년).
- 기호 충돌 정리: PSP 비중 α → w_PSP, 부채 반영 비율 k → κ, 보험 비용률 λ → θ, 요양 필요 금액 → X(h), 확률 극대화 문턱 c → ξ̄.
- 5절 재구성: 5-1 k_ess·k_asp 정의와 숫자 예시, 5-5 "전부 아니면 전무"(모양)와 "시장이 오르면 달성"(위치)이 같은 해임을 명시, 5-6 디지털 옵션 델타 복제 매매, 5-7 필수+희망 목표 실무 해와 승수별 확률표.
- 3-5 CPPI 운용 순서, 4-2 Das-Markowitz 운용 순서, 6-4 Flexicure 금액 계산 추가.
- 9절 방법들의 관계와 동치 종합.

md는 $$ 수식(옵시디언 등), docx는 수식 이미지. 이전 판(II)은 별도 보관.

- 3-6 신설: 고정 비중·CPPI·VaR 예산의 관계 (floor 먼저, GHP < floor, VaR로 m 상한, VaR 7.9% = 2절 해, 첫날 같고 다음 날부터 갈림)
- 4-2 엑셀 해 찾기로 풀기 추가(2026-10-05): 롱온리 상속 계정을 해 찾기 대화창(‘음이 아닌 수’ 체크 · GRG 비선형)과 scipy SLSQP로 · 08 덱에 같은 장 1장(39쪽)
- 4-2 원문 대조 감사 반영(2026-10-05): 합산 효율은 공매도 허용 시 · 12bp는 계정별 롱온리(합산 수준 제약이면 0) · 원문 각주 6의 A·B·C·D와 강의 K 구분 · 원문 p.328 σ 19.89%는 19.38%의 오기로 보임 · 3.9750 위치(p.320) · 인용 범위 · 표 3(위험회피도 오지정 2.5–44bp) · 롱온리로 푸는 법(상속 계정 예). 06 요약 122행 표현 수정
- 4-2 단계 1-2 신설(2026-10-05): 두 자산으로 손으로 풀기(w* = 52.2%) — 행렬(단계 2) 앞의 다리 · 한계에 롱온리 영향(은퇴 · 교육 0, 합산 연 12bp) 추가
- 3-6(c) 신설(2026-10-05): VaR로 floor를 움직이는 위험 자본 방식 — 위험이 오르면 floor↑ · 쿠션↓ · 노출↓, VaR 손실은 손실 예산 L로 고정(9-6 표에 한 줄)
- 3-7 신설: m을 파생상품으로 구현하면 (선물 오버레이 · OBPI 실질 승수 Ω · 갭 보험)
- 04 덱을 05 노트에 맞춤(2026-10-05, 84 → 88장): 31장 3-6(c) 위험 자본 방식(σ 15/20/25% → floor 71.2/80/84.7, 노출 86.4/60/46.0) · 40장 4-2 단계 1-2 두 자산 손풀이(w* 52.2%) · 47장 롱온리 풀이(상속 0 · 8.9 · 91.1%, 계정별 연 12bp, 합산 수준 0) · 48장 엑셀 해 찾기 · SLSQP 신설. 41장 원문 A · B · C · D와 강의 K = D/C, 42장 3.9750 위치(p.320), 44장 '공매도 허용 시' 합산 효율, 84장 12bp, 87장 3-6(c) 한 줄, 7장 기호 각주의 장 번호. 패치 `_build/w06_align/sup17/patch_04.py`
- 03 덱을 W06 M8 강의본에 맞춤(2026-10-05): 방법 1 Market = GHP + 주식 67% 2.24억(균형형 2.22억은 후보 비교) → 합 9.13억 · 남는 0.87억 · 49/22/28, Das–Markowitz 합산 효율은 공매도 허용 시 · 롱온리 12bp, H대 기본 답 = 과제 B안과 Flexicure 승수(1.42 → 충격 뒤 1.53, C안 2.41 → 4.2), '교시' → 단원, 화면의 '돈' → 자금


- 13 덱 신설(2026-10-05): DORS GBWM 연작(09~12 원문) 요약 · 재계산 · 활용 45장. 빌드 `_build/gbwm_deck/`(compute.py → assets.py → build.js, DP 코어 gbwm_core.py, 실습 정답 gbwm_dp.py)
