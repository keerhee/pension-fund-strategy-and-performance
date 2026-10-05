# 미국 주식 포트폴리오·팩터 데이터 (W02 · W10 실습, W12 팀 프로젝트 공용)

KAIST BAF634 고급금융계량분석(2025) 과제 2의 `Problem_Set_2.xls`(github.com/jaepil-choi/KAIST-BAF634-2025)를 시트별 CSV로 옮겼다. 원자료는 Kenneth French Data Library. 모든 값은 **월간 %**, 첫 열 `yyyymm`.

| 파일 | 내용 | 기간 |
|---|---|---|
| `baf_ind30_vw.csv` | 30개 산업 가치가중 포트폴리오, **총수익률** | 1926.07~2015.07 |
| `baf_mom10.csv` | 과거수익률(t−12~t−2) 10분위, **총수익률** (`D01_Loser` … `D10_Winner`) | 1927.01~2015.07 |
| `baf_size_bm25.csv` | 규모 5 × BE/ME 5 가치가중, **총수익률**. `S1`=최소형 … `S5`=최대형, `B1`=최저 BE/ME … `B5`=최고 | 1926.07~2015.11 |
| `baf_mkt_rf.csv` | `MKT_RF` 시장 초과수익률(CRSP 가치가중), `RF` 무위험수익률 | 1926.07~2015.11 |

계산 도구 `factor_lab.py` (Python 3 + numpy · pandas · scipy, Colab 가능)는 포트폴리오에서 `RF`를 빼 초과수익률로 바꾸고, 팩터를 다음과 같이 만든다(간이판 — 공식 Fama-French 2×3 팩터보다 변동성이 크다).

- `SMB` = S1 행 평균 − S5 행 평균 · `HML` = B5 열 평균 − B1 열 평균 · `UMD` = D10 − D01

| 명령 | 하는 일 |
|---|---|
| `summary --set ind30\|mom10\|sb25` | 평균 · 표준편차 · 연 샤프 |
| `grs --set … --model capm\|ff3\|ff3mom\|mom` | 시계열 회귀표 + GRS F · p |
| `factors` | 팩터 프리미엄 · t · 상관 |
| `rolling --factor HML --window 120` | 롤링 연 프리미엄 |
| `combo --w HML=0.5,UMD=0.5` | 팩터 결합의 샤프 · 최대 낙폭 · 최악 12개월(복리) |
| `manager --port S1B5` | 25개 중 한 포트폴리오를 가상 운용사로 보고 CAPM · FF3 · FF3+UMD 알파 |
| `jkp --file <JKP CSV> --factors be_me,ret_12_1,market_equity` | jkpfactors.com에서 내려받은 팩터 요약 + 이 자료와 겹치는 기간의 상관(부호 확인) |

모든 명령에 `--start yyyymm` · `--end yyyymm` 으로 기간을 자를 수 있다. 출력은 `>> log.txt` 로 저장해 제출한다.

**주의.** 이 자료는 2015년에서 끝난다. 그 뒤의 미국 자료와 한국 자료는 JKP 데이터(jkpfactors.com)를 각자 내려받아 `jkp` 명령으로 읽는다. 데이터의 판단용 숫자(슬리브 한도·보수 등)는 각 과제 문서에서 교육용 가정으로 명시했다.
