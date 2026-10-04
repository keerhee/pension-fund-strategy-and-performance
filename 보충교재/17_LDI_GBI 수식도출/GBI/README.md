# GBI — 요약·기초(03)와 Martellini 수식 도출 III(04 · 05), 참고 요약(06)

| 순서 | 파일 | 쪽 | 내용 |
|---|---|---:|---|
| 03 | [`03_GBI_Summary_Basics_zeroone.pdf`](03_GBI_Summary_Basics_zeroone.pdf) | 34 | **GBI 요약·기초 — 무엇을 풀고, 어떻게 배분하는가** — LDI에서 이어받는 것(부채 → 목표 · LHP → GHP · 적립비율 → 쿠션·Floor) → 위험 = 목표 미달 확률 → 목표를 값으로 재기(K · Floor = Retirement Bond) → 두 바구니(GHP · PSP · CPPI · Flexicure) → 확률로 말하는 목표 → 은퇴 이후 → 디폴트옵션 · 대학기금 케이스 · 기관 대 개인 한 장 요약 |
| 04 | [`04_Martellini_GBI_Derivations_III_zeroone.pdf`](04_Martellini_GBI_Derivations_III_zeroone.pdf) | 84 | **GBI 수식 도출 III — Martellini GBI** — 03의 식을 유도한다 — 기초 도구와 부채의 측정 · 두 블록 최적해와 CPPI · 확률로 말하는 목표 · 은퇴소득·인출·요양 · 방법들의 관계와 동치 |
| 05 | [`05_Martellini_GBI_Formula_Derivations_III.pdf`](05_Martellini_GBI_Formula_Derivations_III.pdf) | 39 | **GBI 수식 도출 III — 풀이 노트** — 04 덱의 문서판 — 절마다 풀려는 문제 → 답 → 단계별 풀이 → 이렇게 한다 → 숫자로 확인(md 수식 원문 포함) |
| 06 | [`06_Martellini_GBI_Summary.pdf`](06_Martellini_GBI_Summary.pdf) | 14 | **Martellini GBI 핵심 요약 (참고)** — 특강 II 마르텔리니 GBI 강의 덱 12종의 핵심 요약 |

03은 LDI(01 · 02)를 들은 뒤 이어 본다. 04 덱과 05 노트는 같은 도출의 덱판 · 문서판이다. md는 $$ 수식(옵시디언 등).

## 도출 III에서 바뀐 점 (2026-10-04)

- 0-2 기호표에 금액·비율 구분 추가: k_ess·k_asp는 목표 G에 대한 비율, c·c_ess는 연소득 금액(원/년).
- 기호 충돌 정리: PSP 비중 α → w_PSP, 부채 반영 비율 k → κ, 보험 비용률 λ → θ, 요양 필요 금액 → X(h), 확률 극대화 문턱 c → ξ̄.
- 5절 재구성: 5-1 k_ess·k_asp 정의와 숫자 예시, 5-5 "전부 아니면 전무"(모양)와 "시장이 오르면 달성"(위치)이 같은 해임을 명시, 5-6 디지털 옵션 델타 복제 매매, 5-7 필수+희망 목표 실무 해와 승수별 확률표.
- 3-5 CPPI 운용 순서, 4-2 Das-Markowitz 운용 순서, 6-4 Flexicure 금액 계산 추가.
- 9절 방법들의 관계와 동치 종합.

md는 $$ 수식(옵시디언 등), docx는 수식 이미지. 이전 판(II)은 별도 보관.

- 3-6 신설: 고정 비중·CPPI·VaR 예산의 관계 (floor 먼저, GHP < floor, VaR로 m 상한, VaR 7.9% = 2절 해, 첫날 같고 다음 날부터 갈림)
- 3-7 신설: m을 파생상품으로 구현하면 (선물 오버레이 · OBPI 실질 승수 Ω · 갭 보험)
