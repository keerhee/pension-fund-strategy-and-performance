# W07 보너스(확장) 과제 — 계산 도구

| 폴더 | 과제 | 계산 도구 | 기본 실행 | 실행 시간 |
|---|---|---|---|---|
| bonusA_Regime_TDF | 보너스 A 국면전환 TDF | regime_tdf_tool.py | `python3 regime_tdf_tool.py` | 약 20초 |
| bonusB_RL_Validation | 보너스 B AI 리밸런싱 엔진 검증 | rl_validation_tool.py | `python3 rl_validation_tool.py` | 약 15초 |
| bonusC_Inverse_RL | 보너스 C 역강화학습 | irl_tool.py | `python3 irl_tool.py` | 수 초 |
| bonusD_Real_Data_Hedging | 보너스 D 실제 자료 재검증 | hedging_tool.py · fetch_real_data.py | `python3 fetch_real_data.py` → `python3 hedging_tool.py --panel real_panel.csv` | 수 초(인터넷 필요) |

- 필요 환경: Python 3, numpy, pandas, scipy (보너스 D는 yfinance도). Google Colab에서도 실행된다.
- 난수 시드가 고정되어 있어 누가 실행해도 같은 숫자가 나온다(보너스 D는 내려받는 시점에 따라 달라진다).
- 판정 기준값은 교육용 가정이며 모두 옵션으로 바꿀 수 있다. `python3 도구이름.py --help`로 옵션 목록을 본다.
