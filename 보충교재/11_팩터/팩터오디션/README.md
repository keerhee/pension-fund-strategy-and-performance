# 팩터 오디션 — 최종 세트

연기금 운용전략 과정의 팩터 오디션 실습 세트다. 아래 순서로 진행한다.

| 순서 | 폴더 | 파일 | 내용 |
|---|---|---|---|
| 1 | 1_Primer | Factor_Model_Intro_Primer_Navy_V.pptx | 비전공자용 팩터 모델 입문 사전학습 덱 (62장) — 수익률과 위험, CAPM, 팩터, 다중검정 보정(본페로니·홀름·BH·BY), 경험적 베이지안, 부록 A(Bryzgalova·Huang·Julliard 2023) |
| 2 | 2_Lecture | Factor_Audition_Lecture_Navy_II.pptx | 본 강의 덱 (45장) — 팩터 동물원, 계층적 베이지안 검정, 한국 재현율, 사전 등록과 시점 규칙, 드로다운 대응 규칙, SDAM 리서치 에이전트 |
| 3 | 3_QDL_Guide | QDL_Beginner_Guide.md | QDL 사용 가이드 — 설치, 데이터 배치, 함수 다섯 개, 처음 해 보는 연습 다섯 개 |
| 4 | 4_Lab | Factor_Audition_SDAM_Lab_III.md | 실습과제 — 0~6단계와 가산 단계, Claude Code 지시문 P0~P7, 부록 A 팩터 복제 연습 |
| 별도 | 5_Extra_APT_Lab | LopezLira_Roussanov_APT_Lab.md | BAF634용 별도 실습 — Lopez-Lira·Roussanov 베타중립 포트폴리오 구현 |

## 준비물
- BAF634 저장소: github.com/jaepil-choi/KAIST-BAF634-2025
- 강의 데이터(Google Drive): 저장소 루트의 data/ 폴더에 넣는다 (방법은 QDL 사용 가이드 2장)
- Claude Code — 수강생은 코드를 직접 짜지 않고 지시문으로 시킨다

## 알아 둘 점
- 덱의 그림 가운데 "시뮬레이션 예시"나 "교육용 예시"로 표시된 것은 실제 데이터가 아니다.
- 실습 코드와 지시문은 실제 JKP 데이터로 실행해 보지 않았다. 함수 이름이 바뀌었으면 Claude Code에게 qdl/facade.py를 읽고 정리하게 한다.
