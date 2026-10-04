# W07 팀 발표 과제 IV — 계산 도구

| 폴더 | 팀 | 계산 도구 | 기본 실행 | 실행 시간 |
|---|---|---|---|---|
| team1_NPS_Glidepath | 1팀 | glidepath_tool.py | `python3 glidepath_tool.py` | 수 초 |
| team2_KIC_Hedging | 2팀 | hedging_tool.py | `python3 hedging_tool.py` | 수 초 |
| team3_4_Rebalancing | 3팀 · 4팀 | rebal_tool.py | 3팀 `python3 rebal_tool.py --inst NPS` · 4팀 `python3 rebal_tool.py --inst ALL` | 수 초 |

- 필요 환경: Python 3, numpy, pandas, scipy. Google Colab에서도 실행된다 — 폴더를 올린 뒤 `!python3 도구이름.py`.
- 난수 시드가 고정되어 있어 누가 실행해도 같은 숫자가 나온다. 가정과 데이터 출처는 각 폴더의 `DATA.md`에 있다. `is_assumed = 1`은 교육용 가정, `0`은 공시 사실이다.
- 판정 기준값은 공시 사실(바꿀 수 없음)과 교육용 가정(위원회가 정할 값)으로 나뉜다. 모두 옵션으로 바꿀 수 있다. `python3 도구이름.py --help`로 옵션 목록을 본다.
- 실행 결과를 텍스트 파일로 저장해 제출한다. 예: `python3 rebal_tool.py --inst ALL > log_all.txt`
