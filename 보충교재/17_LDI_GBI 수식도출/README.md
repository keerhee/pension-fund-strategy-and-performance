# 17 · LDI · GBI 수식 도출

W06 「LDI와 GBI」를 강의 순서(M7 LDI → M8 GBI)대로 정리한 보충교재. 주제마다 **요약·기초 덱으로 큰 그림을 잡고, 도출 덱에서 같은 식을 유도한다.**

## 읽는 순서

| 순서 | 자료 | 형식 | 쪽 | 무엇을 다루나 |
|---|---|---|---:|---|
| 01 | [`01_LDI_Summary_Basics_zeroone.pdf`](LDI/01_LDI_Summary_Basics_zeroone.pdf) | 덱 | 34 | **LDI 요약·기초 — 무엇을 풀고, 어떻게 막는가** — 무엇을 풀려는가(성적표는 자산 대 부채) → 재는 도구(듀레이션 · 갭 · DV01) → 막는 방법(헤지 비율 · Redington · 실무 헤지 세 가지) → 깨지는 곳(2022 영국 · SVB) → 남은 예산(PSP/LHP · 위험 예산 · 트리거) → 국민연금 케이스 · GBI로 넘어가며 |
| 02 | [`02_LDI_Derivations_II_zeroone.pdf`](LDI/02_LDI_Derivations_II_zeroone.pdf) | 덱 | 74 | **LDI 수식 도출 II — 실무 헤지 세 가지** — 01의 식을 유도한다 — 부채 측정과 듀레이션 갭 · ① 현금흐름 매칭 ② 장기채 DV01 ③ 스왑 + 버퍼 · 헤지가 깨진 두 사건 · 헤지 비율과 위험 예산 · 최신 기법 |
| 03 | [`03_GBI_Summary_Basics_zeroone.pdf`](GBI/03_GBI_Summary_Basics_zeroone.pdf) | 덱 | 34 | **GBI 요약·기초 — 무엇을 풀고, 어떻게 배분하는가** — LDI에서 이어받는 것(부채 → 목표 · LHP → GHP · 적립비율 → 쿠션·Floor) → 위험 = 목표 미달 확률 → 목표를 값으로 재기(K · Floor = Retirement Bond) → 두 바구니(GHP · PSP · CPPI · Flexicure) → 확률로 말하는 목표 → 은퇴 이후 → 디폴트옵션 · 대학기금 케이스 · 기관 대 개인 한 장 요약 |
| 04 | [`04_Martellini_GBI_Derivations_III_zeroone.pdf`](GBI/04_Martellini_GBI_Derivations_III_zeroone.pdf) | 덱 | 88 | **GBI 수식 도출 III — Martellini GBI** — 03의 식을 유도한다 — 기초 도구와 부채의 측정 · 두 블록 최적해와 CPPI · 확률로 말하는 목표 · 은퇴소득·인출·요양 · 방법들의 관계와 동치 |
| 05 | [`05_Martellini_GBI_Formula_Derivations_III.pdf`](GBI/05_Martellini_GBI_Formula_Derivations_III.pdf) | 노트 | 41 | **GBI 수식 도출 III — 풀이 노트** — 04 덱의 문서판 — 절마다 풀려는 문제 → 답 → 단계별 풀이 → 이렇게 한다 → 숫자로 확인(md 수식 원문 포함) |
| 06 | [`06_Martellini_GBI_Summary.pdf`](GBI/06_Martellini_GBI_Summary.pdf) | 노트 | 14 | **Martellini GBI 핵심 요약 (참고)** — 특강 II 마르텔리니 GBI 강의 덱 12종의 핵심 요약 |
| 08 | [`08_Das_Markowitz_Mental_Accounts_zeroone.pdf`](GBI/08_Das_Markowitz_Mental_Accounts_zeroone.pdf) | 덱 | 39 | **심리계정 포트폴리오 — Das · Markowitz · Scheid · Statman (2010)** — 원 논문 예 하나를 따라가는 손풀이 덱(07 원문은 저장소에 올리지 않음) |
| 13 | [`13_GBWM_Series_DORS_zeroone.pdf`](GBI/13_GBWM_Series_DORS_zeroone.pdf) | 덱 | 45 | **목표기반 자산관리(GBWM) 연작 — Das · Ostrov · Radhakrishnan · Srivastav 2018–2022** — 2018 효율선 위 목표 확률 → 2020 동적계획법 → 2022 여러 목표 → 2023 확률 프런티어를 원문 예 재계산으로 따라가고, 언제 무엇을 쓰나 · M8 · 한국 대입 · Claude Code 프롬프트로 정리(09~12 원문은 저장소에 올리지 않음 · 저자 사이트 링크) |

수업에서는 01 → 03으로 진행하고, 02 · 04 · 05는 수식 유도가 필요할 때(과제 · 보강) 본다. 06은 특강 II의 참고 요약이다.

- [`LDI/`](LDI/) — 01 · 02
- [`GBI/`](GBI/) — 03 ~ 08 · 13 (05 · 06은 md 수식 원문 포함, 07 · 09~12 원문 PDF는 저장소 미포함)

PPTX · DOCX 편집 원본은 저장소에 올리지 않는다. 01 · 03 요약 덱의 빌드 스크립트는 `_build/ldi_summary/` · `_build/gbi_summary/`에 있다.

## 변경 이력

- 2026-10-05 — 13 DORS GBWM 연작 덱 추가(45장, `_build/gbwm_deck/`). 원문 09~12는 .gitignore — 링크 https://srdas.github.io/Papers/GBWM.pdf · DP_Paper.pdf · MultWealthGoals.pdf · EGPF.pdf

- 2026-10-05 — W06 강의본(M7 · M8) 개정에 맞춰 정합: 01(Redington 전개식 전체 · 금액 꼴 조건 A = L · C_A A > C_L L, 국민연금 적립비율 95% · 69%는 우리 계산 · 공시 지표는 적립배율, 안 A 현행 유지 · 안 B 30년 국고채 교체 · 안 C IRS 오버레이, '교시' → 단원), 02(25장 Redington · 29장 안 B), 03(방법 1 합 9.13억 · 0.87억 · 49/22/28, Market = GHP + 주식 67% 2.24억, Das–Markowitz 합산 효율은 공매도 허용 시 · 롱온리 12bp, H대 Flexicure m 1.42 → 1.53 · C안 4.2), 04(84 → 88장: 3-6(c) 위험 자본 방식 · 4-2 단계 1-2 두 자산 손풀이 · 롱온리 풀이 · 해 찾기 4장 추가). 01 · 03은 `_build/ldi_summary/` · `_build/gbi_summary/`로, 02 · 04는 `_build/w06_align/sup17/patch_02.py` · `patch_04.py`로 다시 만든다.
