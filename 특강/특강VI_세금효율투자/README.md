# 특강 VI — 세금효율 투자

같은 자산이라도 어느 계좌에 담고 언제 팔며 누가 사느냐에 따라 손에 남는 돈이 달라진다. 교과서 강의로 전체 그림을 보고, Huang(2008) 모형으로 한국 계좌(ISA · 연금저축 · IRP)의 자산배치를 세후 기준으로 푼다. 세율 · 한도는 2026년 11월 기준이다.

## 01_세금과투자_교과서덱

| 자료 | 쪽 | 무엇을 다루나 |
|---|---:|---|
| [`Tax_Efficient_Investing_Navy_Deck.pdf`](01_세금과투자_교과서덱/Tax_Efficient_Investing_Navy_Deck.pdf) | 53 | **세금과 투자** — 세후 성과를 높이는 자산 배치 · 실현 시점 · 세금 고객층 (초보자~중급자) |

## 02_Huang자산배치_최종본 (2026-11-28 다운로드)

| 자료 | 쪽 | 무엇을 다루나 |
|---|---:|---|
| [`1_Deck/…Deck_V.pdf`](02_Huang자산배치_최종본/1_Deck/Huang_Asset_Location_Korea_Deck_V.pdf) | 73 | **Huang 모형과 한국형 자산배치 V** — 자산배분과 자산배치의 분리 → 한국 상품별 · 계좌별 과세 → 김 교수 사례 → 동적 최적화 → 2026 세제 개정 → Claude Code 구현 |
| [`2_Lecture_Notes/…Lecture_Notes_V.md`](02_Huang자산배치_최종본/2_Lecture_Notes/Huang_Asset_Location_Korea_Lecture_Notes_V.md) | — | 강의노트 V판(md · pdf, 플로우차트 `flowchart.png`) |
| [`3_Workbook/…Workbook_II.pdf`](02_Huang자산배치_최종본/3_Workbook/Huang_Asset_Location_Korea_Workbook_II.pdf) | 10 | **손계산 워크북** — 김 교수 사례를 복리계수 네 개로 따라 계산 |
| [`4_ALM_Model/`](02_Huang자산배치_최종본/4_ALM_Model/) | — | 자산배분 · 자산배치 모델 패키지(Python, `python run_examples.py`), 세법은 `tax_rules_2026.py`, 수식 명세 [`docs/ALM_Model_Specification.pdf`](02_Huang자산배치_최종본/4_ALM_Model/docs/ALM_Model_Specification.pdf)(5쪽, md · docx 함께, 흐름도 `flowchart.png`), 결과 `outputs/` |
| [`4_ALM_Model/lecture/…Deck.pdf`](02_Huang자산배치_최종본/4_ALM_Model/lecture/Korea_ALM_Model_Deck.pdf) | 50 | **한국형 자산배분 · 자산배치 모델** — 모델 해설 강의덱(pptx 함께), 손계산 워크북 [`…Workbook.pdf`](02_Huang자산배치_최종본/4_ALM_Model/lecture/Korea_ALM_Model_Workbook.pdf) 11장 |
| [`5_MVP_App/Tax_Location_Advisor.html`](02_Huang자산배치_최종본/5_MVP_App/Tax_Location_Advisor.html) | — | 고객 데이터를 넣으면 최적 절세 배치와 보고서를 내는 HTML 앱(브라우저로 열기) |

폴더 안 `README.md`가 받은 원본 안내다(앱의 IRP Z 계산 가정, 보고서 버튼 제약 포함).

## 그 밖

- `쇼릴_Huang자산배치_5분/` — 5분 쇼릴(원전은 이전판 강의노트 II)
- `_이전판/` — 덱 II판(50장, pptx · PDF)과 강의노트 II판. 최종본 V판으로 대체됨

## 이력

- 2026-11-28 `연기금후반부/`에서 옮겼다. Huang II판 세 편은 보충교재 `19_세금효율투자_자산배치/`에도 같은 파일이 있다.
- 2026-11-28 최종본 zip(`Huang_Asset_Location_Korea_Final`)을 `02_…최종본/`으로 풀어 넣고 재정리. 덱 V판 PDF는 Pretendard로 다시 변환(받은 PDF는 Noto Sans CJK), 워크북은 pptx가 기존과 같아 기존 Pretendard PDF를 쓰고 중복 사본 삭제. 덱 · 강의노트 II판은 `_이전판/`으로.
- 2026-11-28 다운로드에 따로 받은 `ALM_Model_Specification.pdf`는 `4_ALM_Model/docs/`의 것과 같은 파일(MD5 일치)이라 다운로드 사본만 삭제.
- 2026-11-28 ALM 모델 강의덱(50장) · 워크북(11장)을 받아 `4_ALM_Model/lecture/`에 넣음(다운로드 `_1` 중복 사본 삭제). PDF는 Pretendard로 다시 변환(받은 PDF는 Noto Sans CJK).
