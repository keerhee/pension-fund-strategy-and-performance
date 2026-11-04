# W11 파이널 과제 — 팩터 오디션

기금의 해외주식 팩터 슬리브(10조 원)에 넣을 팩터를 153개 후보 가운데 최대 10개 고른다. 판정은 Claude Code가 하고, 수강생은 지시하고 검증하고 결재한다. 단순 t값 기준과 JKP(2023) 계층 베이지안 기준(군집 13개로 보정)을 비교한다.

두 판이 있다. **Easy판으로 먼저 하고, 고급판은 심화 과제로 한다.**

| | Easy판 (`1_Student/1_Easy/`) | 고급판 (`1_Student/2_Advanced/`) |
|---|---|---|
| 단계 | 지시문 5개 · 5단계 | 6단계 검정 엔진 (배점 100 + 가산 10) |
| 기본 지식 | 팩터 슬리브 · 다중 검정 · 계층 베이지안 · 드로다운 4가지 | + 경험적 베이지안 수축 · 군집 계층 모형 식 · 사전 등록(규칙 잠금) |
| 오디션 | 2010년 한 번 → 이후 10년 채점 | 2000~2020년 5년마다 리뷰, 세 규칙(단순 t · HLZ · JKP 베이지안) 비교 |
| 드로다운 | Value 겨울 한 구간 | 3단계 대응 규칙을 Value 겨울에 테스트 |
| 파일 | 과제지 `Factor_Audition_Lab_Easy.pdf`(6쪽, 원본 md·docx) · 설명 덱 `Factor_Audition_Lab_Deck_Easy_II.pdf`(19장) | 실습 덱 `Factor_Audition_Lab_Deck_Advanced.pdf`(22장) |

- `1_Student/Videos/Factor_Audition_Lecture_Motion.mp4` — 과제 소개 모션 영상 2분 35초 (저장소 제외)
- 편집 원본 `.pptx`·`.docx`는 저장소에 올리지 않는다.

데이터는 따로 동봉하지 않는다. 코드는 GitHub `jaepil-choi/KAIST-BAF634-2025`(QDL), JKP 팩터 수익률 CSV는 과제지에 적힌 Google Drive 폴더에서 받아 저장소 `data/`에 넣는다. 원본 SDAM 랩은 `보충교재/11_팩터/팩터오디션/`에 있다.
