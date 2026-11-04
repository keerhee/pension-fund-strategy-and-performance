# 과제 (Assignment)

주차별 개인 실습과 팀 과제. 과제 폴더마다 `1_Student/`(학생 배포용)와 `2_Instructor/`(교수용 모범답안 — 저장소에 올리지 않음)로 나뉜다.

| 주차 | 폴더 | 형식 | 내용 |
|---|---|---|---|
| W02 | `W02_Lab_CAPM_GRS/` | 개인 실습 | CAPM 시계열 회귀와 GRS 검정 (산업 30 · 모멘텀 10 · 규모×BE/ME 25) |
| W06 | `W06_Team_Assignment/` | 팀 과제 | LDI·GBI — 1팀 국민연금 금리 인하 · 2팀 금리 인상 · 3팀 디폴트옵션 · 4팀 H대학 기금 |
| W07 | `W07_Team_Assignment/` | 팀 과제 | 동적 포트폴리오 — 1팀 글라이드패스 · 2팀 KIC 헤징 · 3팀 국민연금 리밸런싱 · 4팀 기관 리밸런싱 규칙 |
| W07 | `W07_Team_Assignment_Bonus/` | 보너스 과제 | 확장 과제 — A 국면 TDF · B RL 검증 · C 역강화학습 · D 실데이터 헤징 |
| W10 | `W10_Lab_Factor_Models/` | 개인 실습 | SMB·HML·UMD 직접 구성, CAPM→FF3→4팩터 GRS, 위탁운용사 알파 재측정 |
| W11 | `W11_Final_Assignment_Factor_Audition/` | 파이널 과제 | 팩터 오디션 — `1_Easy/`(5단계) 먼저, `2_Advanced/`(6단계 검정 엔진) 심화. 153개 팩터 중 최대 10개를 Claude Code로 판정, 단순 t값 vs JKP 계층 베이지안, IC 안건서 결재 |
| W12 | `W12_Team_Project_Factor_Adoption/` | 팀 프로젝트 | 국내주식 팩터 도입 — 1팀 가치 · 2팀 모멘텀 · 3팀 규모 · 4팀 결합 (미국 90년 + JKP 표본 밖·한국 검증) |
| 공용 | `BAF634_Factor_Data/` | 데이터·도구 | W02·W10·W12 공용 데이터와 계산 도구 `factor_lab.py` — KAIST BAF634(2025) `Problem_Set_2.xls` 기반. 초보자용 실행 가이드(`Lab_Run_Guide_Beginner.pdf`)와 Colab 노트북 포함 |

## 폴더 안 구성

| 위치 | 들어 있는 것 |
|---|---|
| `1_Student/*_Guide.pdf` | 과제 전체 가이드 — 먼저 읽는다 |
| `1_Student/*_TeamN_*.pdf` | 팀별 과제지 (W06·W07은 편집 원본 `.docx`가 옆에 있다 — 저장소 제외) |
| `1_Student/Data/<팀 폴더>/` | 팀별 데이터와 계산 도구. 폴더마다 단독 실행되도록 같은 패널 파일을 따로 넣어 두었다(W06 3·4팀 패널, W07 2팀·보너스 D 헤징 데이터) |
| `1_Student/Videos/` | 과제 설명 영상 — W06 5편(가이드 10분 + 팀별 13~17분, 약 1.1GB), W11 팩터 오디션 소개 영상 1편. 저장소 제외 |
| `2_Instructor/` | W06·W07·W07 보너스 모범답안 `.docx` |

계산 도구는 `Data/` 아래 팀 폴더에서 `python3 <도구>.py`로 실행한다. W02·W10·W12는 `BAF634_Factor_Data/factor_lab.py` 하나를 함께 쓴다. 최종 프로젝트는 상위 폴더의 `Final_Project/`에 따로 있다.
