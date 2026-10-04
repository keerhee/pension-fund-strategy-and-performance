# 17 · LDI · GBI 수식 도출

W06 「LDI와 GBI」를 강의 순서(M7 LDI → M8 GBI)대로 정리한 보충교재. 주제마다 **요약·기초 덱으로 큰 그림을 잡고, 도출 덱에서 같은 식을 유도한다.**

## 읽는 순서

| 순서 | 자료 | 형식 | 쪽 | 무엇을 다루나 |
|---|---|---|---:|---|
| 01 | [`01_LDI_Summary_Basics_zeroone.pdf`](LDI/01_LDI_Summary_Basics_zeroone.pdf) | 덱 | 34 | **LDI 요약·기초 — 무엇을 풀고, 어떻게 막는가** — 무엇을 풀려는가(성적표는 자산 대 부채) → 재는 도구(듀레이션 · 갭 · DV01) → 막는 방법(헤지 비율 · Redington · 실무 헤지 세 가지) → 깨지는 곳(2022 영국 · SVB) → 남은 예산(PSP/LHP · 위험 예산 · 트리거) → 국민연금 케이스 · GBI로 넘어가며 |
| 02 | [`02_LDI_Derivations_II_zeroone.pdf`](LDI/02_LDI_Derivations_II_zeroone.pdf) | 덱 | 74 | **LDI 수식 도출 II — 실무 헤지 세 가지** — 01의 식을 유도한다 — 부채 측정과 듀레이션 갭 · ① 현금흐름 매칭 ② 장기채 DV01 ③ 스왑 + 버퍼 · 헤지가 깨진 두 사건 · 헤지 비율과 위험 예산 · 최신 기법 |
| 03 | [`03_GBI_Summary_Basics_zeroone.pdf`](GBI/03_GBI_Summary_Basics_zeroone.pdf) | 덱 | 34 | **GBI 요약·기초 — 무엇을 풀고, 어떻게 배분하는가** — LDI에서 이어받는 것(부채 → 목표 · LHP → GHP · 적립비율 → 쿠션·Floor) → 위험 = 목표 미달 확률 → 목표를 값으로 재기(K · Floor = Retirement Bond) → 두 바구니(GHP · PSP · CPPI · Flexicure) → 확률로 말하는 목표 → 은퇴 이후 → 디폴트옵션 · 대학기금 케이스 · 기관 대 개인 한 장 요약 |
| 04 | [`04_Martellini_GBI_Derivations_III_zeroone.pdf`](GBI/04_Martellini_GBI_Derivations_III_zeroone.pdf) | 덱 | 84 | **GBI 수식 도출 III — Martellini GBI** — 03의 식을 유도한다 — 기초 도구와 부채의 측정 · 두 블록 최적해와 CPPI · 확률로 말하는 목표 · 은퇴소득·인출·요양 · 방법들의 관계와 동치 |
| 05 | [`05_Martellini_GBI_Formula_Derivations_III.pdf`](GBI/05_Martellini_GBI_Formula_Derivations_III.pdf) | 노트 | 39 | **GBI 수식 도출 III — 풀이 노트** — 04 덱의 문서판 — 절마다 풀려는 문제 → 답 → 단계별 풀이 → 이렇게 한다 → 숫자로 확인(md 수식 원문 포함) |
| 06 | [`06_Martellini_GBI_Summary.pdf`](GBI/06_Martellini_GBI_Summary.pdf) | 노트 | 14 | **Martellini GBI 핵심 요약 (참고)** — 특강 II 마르텔리니 GBI 강의 덱 12종의 핵심 요약 |

수업에서는 01 → 03으로 진행하고, 02 · 04 · 05는 수식 유도가 필요할 때(과제 · 보강) 본다. 06은 특강 II의 참고 요약이다.

- [`LDI/`](LDI/) — 01 · 02
- [`GBI/`](GBI/) — 03 ~ 06 (05 · 06은 md 수식 원문 포함)

PPTX · DOCX 편집 원본은 저장소에 올리지 않는다. 01 · 03 요약 덱의 빌드 스크립트는 `_build/ldi_summary/` · `_build/gbi_summary/`에 있다.
