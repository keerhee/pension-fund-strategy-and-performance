# Huang 모형과 한국형 자산배치 — 최종본 (2026년 11월)

| 폴더 | 내용 |
|---|---|
| 1_Deck | 강의덱 V판 (73장, pptx·pdf) |
| 2_Lecture_Notes | 강의노트 V판 (md·pdf). md의 플로우차트 그림은 같은 폴더의 flowchart.png를 쓴다 |
| 3_Workbook | 손계산 워크북 II판 (pptx·pdf) |
| 4_ALM_Model | 자산배분·자산배치 모델 패키지 (Python). `python run_examples.py`로 실행하고, 수식 명세는 docs/에 있다 |
| 5_MVP_App | 고객 데이터를 넣으면 최적 절세 배치와 보고서를 내는 HTML 앱. 브라우저로 Tax_Location_Advisor.html을 연다. engine.js는 계산 엔진 원본이며 앱 안에 이미 들어 있다 |

- 세법은 2026년 11월 기준이며 4_ALM_Model/tax_rules_2026.py에 모여 있다.
- 앱의 IRP Z는 납입하면 70% 한도도 함께 늘어난다고 보고 계산한다. 모델 패키지와 덱의 값(0.993)은 한도를 고정한 값이다.
- 내려받은 HTML 앱에서는 '보고서 내려받기' 버튼이 동작하지 않으므로 '요약 복사'나 브라우저 인쇄(PDF 저장)를 쓴다.

> 정리 메모(2026-11-28): 덱 V판 PDF와 워크북 PDF는 Pretendard 글꼴판으로 바꿔 두었다(받은 원본 PDF는 Noto Sans CJK).
