---
title: "QDL 사용 가이드 — 처음 쓰는 사람을 위한 실행 매뉴얼"
course: BAF.60080 연기금 운용전략과 성과평가 · BAF634 고급금융계량분석
repo: github.com/jaepil-choi/KAIST-BAF634-2025
tags: [QDL, JKP, 가이드매뉴얼, ClaudeCode, 초보자]
---

# QDL 사용 가이드 — 처음 쓰는 사람을 위한 실행 매뉴얼

> [!abstract] 이 문서로 할 수 있게 되는 것
> 1. QDL을 내 컴퓨터에 설치하고 데이터를 제자리에 넣는다.
> 2. 팩터 수익률과 종목 특성을 불러와 표와 그림으로 확인한다.
> 3. 내가 만든 팩터가 정답 팩터와 얼마나 같은지 검증한다.
>
> **코드는 직접 짜지 않는다.** 모든 일은 Claude Code에게 지시문으로 시키고, 여러분은 결과를 확인한다. 이 문서의 코드는 Claude Code가 무엇을 할지 이해하기 위한 읽기용이다.

---

## 1. 기본 지식

### 1.1 QDL이란 무엇인가

QDL(Quant Data Library)은 KAIST BAF634 과목에서 만든 **데이터 창구**다. JKP 글로벌 팩터 데이터를 불러오고 검증하는 일을 함수 몇 개로 끝낼 수 있게 묶어 두었다. 내부가 복잡해도 사용자는 `QDL()`이라는 하나의 창구(퍼사드, facade)만 쓰면 된다.

### 1.2 JKP 데이터란 무엇인가

Jensen·Kelly·Pedersen(2023, *Journal of Finance*)이 만든 공개 데이터다. 93개국 주식에 대해 같은 방식으로 계산한 400여 개의 **종목 특성**과, 그 특성으로 만든 153개 **팩터 수익률**을 제공한다. 원자료는 jkpfactors.com에 있고, 이 과목에서는 미국(usa)과 한국(kor) 자료만 쓴다.

| 용어 | 뜻 | 예 |
|---|---|---|
| 특성(characteristic) | 종목마다 매월 하나씩 있는 숫자 | 장부가 대비 시가(`be_me`), 시가총액(`me`) |
| 팩터(factor) | 특성으로 종목을 정렬해 만든 롱숏 포트폴리오의 월 수익률 | 가치 팩터 = `be_me` 상위 3분의 1 매수, 하위 3분의 1 매도 |
| 테마(theme) | 비슷한 팩터를 묶은 13개 군집 | 가치(value), 모멘텀(momentum), 수익성(profitability) |

### 1.3 와이드 형식과 롱 형식

같은 데이터를 두 모양으로 담을 수 있다. QDL은 주로 **와이드 형식**을 돌려준다.

| 형식 | 모양 | 언제 편한가 |
|---|---|---|
| 와이드(wide) | 행은 날짜, 열은 종목(또는 팩터) | 시계열 그림, 날짜별 횡단면 계산 |
| 롱(long) | 한 행이 (날짜, 종목, 값) 하나 | 여러 특성을 한 표에 모을 때, 회귀 |

---

## 2. 설치 — Claude Code에게 맡긴다

### 2.1 준비물

- Claude Code가 설치된 컴퓨터 (Python 3.10 이상이면 좋다. 없어도 Claude Code가 설치해 준다)
- 인터넷 연결
- 데이터 폴더 링크: https://drive.google.com/drive/folders/1vRVfhTRU7YsaT1ndiqTEkxfSEfVIioVZ?usp=sharing

### 2.2 설치 지시문

> [!example] Claude Code 지시문 G1 — 저장소 내려받기와 환경 만들기
> ```
> 내 홈 폴더 아래 work/ 폴더를 만들고 그 안에서 다음을 해 줘.
> 1. github.com/jaepil-choi/KAIST-BAF634-2025 저장소를 git clone 한다.
> 2. 저장소 안에 파이썬 가상환경 .venv 를 만들고, 저장소에 requirements 파일이 있으면 그것으로,
>    없으면 pandas numpy pyarrow matplotlib scipy statsmodels 를 설치한다.
> 3. python -c "from qdl.facade import QDL; print('QDL OK')" 를 저장소 루트에서 실행해 결과를 보여 준다.
> 오류가 나면 원인을 찾아 고친 뒤 무엇을 고쳤는지 한 줄로 알려 줘.
> ```

> [!example] Claude Code 지시문 G2 — 데이터 내려받기
> ```
> 아래 Google Drive 폴더를 저장소 루트의 data/ 폴더로 내려받아 줘.
> https://drive.google.com/drive/folders/1vRVfhTRU7YsaT1ndiqTEkxfSEfVIioVZ?usp=sharing
> gdown 을 설치해 gdown --folder 로 시도하고, 안 되면 실패 이유를 알려 줘.
> 다 받으면 data/factors/ 와 data/chars/ 의 파일 목록과 각 파일 크기를 표로 보여 주고,
> data/ 가 .gitignore 에 들어 있는지 확인해 줘.
> ```

> [!warning] 자동 내려받기가 안 될 때
> Google Drive는 큰 파일이나 많은 파일을 자동으로 받지 못하게 막을 때가 있다. 그때는 브라우저로 링크를 열어 폴더를 직접 내려받고, 압축을 풀어 다운로드 폴더에 둔 뒤 Claude Code에게 "다운로드 폴더의 파일을 저장소 data/ 구조에 맞게 옮겨 줘"라고 시킨다.

### 2.3 폴더가 이렇게 되어 있어야 한다

```
KAIST-BAF634-2025/
├── qdl/                  ← QDL 코드 (손대지 않는다)
├── tutorial.ipynb        ← 공식 튜토리얼
├── data/                 ← 내려받은 데이터 (저장소에 올리지 않는다)
│   ├── factors/          ← 팩터 수익률 CSV
│   │   ├── [usa]_[all_factors]_[monthly]_[vw_cap].csv
│   │   ├── [usa]_[all_themes]_[monthly]_[vw_cap].csv
│   │   ├── [usa]_[mkt]_[monthly]_[vw_cap].csv
│   │   └── [kor]_… (같은 구성)
│   └── chars/            ← 종목 특성 parquet
│       ├── jkp_1972-_usa.parquet   (가장 크다)
│       ├── jkp_2000-_usa.parquet
│       ├── jkp_2020-_usa.parquet   (가장 작다)
│       └── jkp_…_kor.parquet
└── (여러분의 과제 폴더)
```

| 파일 이름의 부분 | 뜻 | 가능한 값 |
|---|---|---|
| `[usa]` | 국가 | `usa`, `kor` |
| `[all_factors]` | 데이터 종류 | `all_factors`(153개 팩터), `all_themes`(13개 테마), `mkt`(시장) |
| `[vw_cap]` | 가중 방식 | `ew`(동일가중), `vw`(시가총액가중), `vw_cap`(상한을 둔 시가총액가중) |
| `jkp_2000-` | 특성 데이터의 시작 연도 | `1972-`, `2000-`, `2020-` |

> [!tip] 메모리가 부족하면
> `jkp_1972-_usa.parquet`는 수백 MB이고, 불러오면 메모리를 몇 GB 쓴다. 노트북이 느려지거나 멈추면 `2000-`나 `2020-` 파일부터 쓴다. 팩터 수익률 CSV는 몇 MB라 걱정하지 않아도 된다.

---

## 3. QDL의 함수 다섯 개

모든 함수는 `q = QDL()`로 창구를 연 뒤 `q.함수이름(...)`으로 부른다. 저장소 루트에서 실행해야 `data/`를 찾는다.

| 함수 | 하는 일 | 돌려주는 것 |
|---|---|---|
| `load_factors(country, dataset, weighting, factors, strict)` | 팩터 수익률을 불러온다 | 와이드 표 (행 날짜, 열 팩터) |
| `load_factor_dataset(country, dataset, weighting, columns)` | 팩터 원자료를 그대로 불러온다 | 롱 표 |
| `load_char(country, vintage, char)` | 특성 **하나**를 불러온다 | 와이드 표 (행 날짜, 열 종목 `id`) |
| `load_chars(country, vintage, columns)` / `load_char_dataset(country, vintage)` | 여러 특성을 한꺼번에 불러온다 | 롱 표 |
| `validate_factor(user, weighting, return_plot, plot_title, ...)` | 내가 만든 팩터를 정답과 비교한다 | 검증 리포트 |

> [!note] 함수 이름이 다르면
> 위 표는 저장소의 `tutorial.py`와 `test_qdl.py`에서 확인한 것이다. 저장소가 갱신되어 이름이나 인자가 바뀌었을 수 있다. 오류가 나면 Claude Code에게 "qdl/facade.py 를 읽고 공개 함수 목록과 인자를 표로 정리해 줘"라고 시킨다.

### 3.1 팩터 수익률 불러오기 (읽기용)

```python
from qdl.facade import QDL
q = QDL()

F = q.load_factors(
    country="usa",            # 국가
    dataset="factor",         # 개별 팩터
    weighting="vw_cap",       # 가중 방식
    factors=["be_me", "ret_12_1", "ope_be"],   # 원하는 팩터 이름
    strict=False,             # 없는 이름이 있어도 멈추지 않는다
)
print(F.tail())               # 행: 날짜, 열: 팩터, 값: 월 수익률(소수, 0.01 = 1%)
```

### 3.2 특성 하나 불러오기 (읽기용)

```python
ME = q.load_char(country="usa", vintage="2020-", char="me")   # 시가총액
print(ME.shape)                # (날짜 수, 종목 수)
print(ME.iloc[-1].dropna().sort_values().tail())   # 마지막 달 시가총액 상위 종목
```

### 3.3 검증하기 (읽기용)

```python
report = q.validate_factor(user=my_factor, weighting="vw_cap",
                           return_plot=True, plot_title="내 팩터 vs 정답")
print(report.corr, report.rmse, report.n_obs, report.date_start, report.date_end)
report.per_factor_metrics      # 팩터별 mse·rmse·mae·corr·ic
report.figure                  # 누적수익률 비교 그림
```

| 리포트 항목 | 뜻 | 좋은 값 |
|---|---|---|
| `corr` | 내 팩터와 정답 팩터의 상관 | 1에 가까울수록 좋다 |
| `rmse` | 월 수익률 차이의 크기 | 0에 가까울수록 좋다 |
| `n_obs` | 겹치는 달의 수 | 기간이 맞는지 확인용 |
| `ic` | 순위 상관 | 1에 가까울수록 좋다 |

---

## 4. 자주 쓰는 특성 사전

| 특성 이름 | 뜻 | 쓰임 |
|---|---|---|
| `id` | 종목 식별자 | 열 이름 |
| `eom` | 월말 날짜(end of month) | 행 이름 |
| `me` | 시가총액 | 가치가중 비중 |
| `size_grp` | NYSE 기준 규모 그룹 (`mega`, `large`, `small`, `micro`, `nano`) | 소형주 제외, 브레이크포인트 |
| `ret_exc` | 그 달의 초과수익률 | 시계열 분석 |
| `ret_exc_lead1m` | **다음 달** 초과수익률 | 포트폴리오 성과 측정 |
| `market_equity` | 규모 특성 | 규모(SMB) 팩터 |
| `be_me` | 장부가 대비 시가 | 가치(HML) 팩터 |
| `ope_be` | 자기자본 대비 영업이익 | 수익성(RMW) 팩터 |
| `at_gr1` | 총자산 증가율 | 투자(CMA) 팩터 |
| `ret_12_1` | 직전 12개월~1개월 누적수익률 | 모멘텀 팩터 |
| `ret_1_0` | 직전 1개월 수익률 | 단기 반전 팩터 |

> [!warning] 날짜 맞추기 — 초보자가 가장 많이 틀리는 곳
> $t$월 말의 특성으로 종목을 고르면, 성과는 $t+1$월 수익률로 재야 한다. 방법은 둘이다.
> - `ret_exc_lead1m`을 쓰면 같은 행에 다음 달 수익률이 이미 들어 있다.
> - `ret_exc`를 쓰면 특성 표를 한 달 밀어(`shift(1)`) 맞춘다.
>
> 이것을 어기면 미래 정보를 쓴 셈이 되어 성과가 비현실적으로 좋게 나온다. 결과가 너무 좋으면 가장 먼저 날짜 맞춤을 의심한다.

---

## 5. 처음 해 보는 연습 다섯 개

모두 Claude Code에게 시킨다. 각 연습 끝의 **확인할 것**만 직접 본다.

> [!example] 연습 1 — 팩터 데이터 둘러보기
> ```
> 저장소 루트에서 QDL 로 미국 all_factors vw_cap 팩터를 모두 불러와 줘.
> 팩터 개수, 시작월, 마지막월을 알려 주고, be_me, ret_12_1, ope_be 세 팩터의
> 연 평균수익률, 연 변동성, 샤프 비율을 표로 만들어 줘.
> 세 팩터의 누적수익률 그림을 results/ex1.png 로 저장해 줘.
> ```
> **확인할 것.** 팩터 수가 150개 안팎인가? 그림에서 2018~2020년 `be_me`가 내려가는 구간(Value 겨울)이 보이는가?

> [!example] 연습 2 — 미국과 한국 비교
> ```
> 연습 1과 같은 세 팩터를 한국(kor)으로도 불러와, 두 나라의 샤프 비율을 나란히 표로 만들어 줘.
> 한국 자료가 언제 시작하는지도 알려 줘.
> ```
> **확인할 것.** 한국 표본이 미국보다 얼마나 짧은가? 같은 팩터인데 부호가 반대인 것이 있는가?

> [!example] 연습 3 — 특성 하나 들여다보기
> ```
> 미국 2020- 특성에서 me 와 size_grp 를 불러와, 가장 최근 달의 size_grp 별 종목 수와
> 시가총액 합계 비중을 표로 보여 줘.
> ```
> **확인할 것.** micro와 nano 종목은 종목 수로는 많지만 시가총액 비중은 몇 %인가? 이것이 팩터를 만들 때 소형주를 빼는 이유와 어떻게 연결되는가?

> [!example] 연습 4 — 테마 13개 보기
> ```
> 미국 all_themes vw_cap 을 불러와 13개 테마의 이름과 샤프 비율을 큰 순서로 보여 주고,
> 테마끼리 상관행렬을 히트맵으로 results/ex4.png 에 저장해 줘.
> ```
> **확인할 것.** 상관이 가장 높은 두 테마는 무엇인가? 서로 음(−)의 상관인 테마 쌍이 있는가?

> [!example] 연습 5 — 검증 함수 써 보기
> ```
> tutorial.py 의 검증 예시처럼, 정답 팩터 be_me 에 작은 잡음을 더한 가짜 팩터를 만들고
> validate_factor 로 정답과 비교해 corr 와 rmse 를 보여 줘. 잡음 크기를 0.01, 0.02, 0.05 로
> 바꿔 corr 가 어떻게 변하는지 표로 정리해 줘.
> ```
> **확인할 것.** 잡음이 커질수록 corr가 떨어지는가? 부록 A의 팩터 복제 연습에서 corr가 몇 이상이면 "잘 복제했다"고 볼지 감을 잡는다.

---

## 6. 막혔을 때

| 증상 | 흔한 원인 | Claude Code에게 할 말 |
|---|---|---|
| `ModuleNotFoundError: qdl` | 저장소 루트가 아닌 곳에서 실행했다 | "저장소 루트에서 다시 실행해 줘" |
| `FileNotFoundError` | `data/` 위치나 파일 이름이 다르다 | "data/ 구조를 가이드 2.3절과 비교해 맞게 옮겨 줘" |
| 컴퓨터가 멈춘다 | `1972-` parquet가 너무 크다 | "2000- 빈티지로 바꿔서 다시 해 줘" |
| 결과가 비현실적으로 좋다 | 날짜를 맞추지 않아 미래 정보가 들어갔다 | "특성 날짜와 수익률 날짜가 한 달 어긋나게 맞춰졌는지 코드로 보여 줘" |
| 팩터 이름이 없다는 오류 | 이름 철자가 다르다 | "all_factors 파일의 name 열에서 비슷한 이름을 찾아 줘" |

> [!tip] 좋은 지시문의 세 가지 조건
> 1. **어디서**: 저장소 루트에서, 어떤 폴더에 저장할지 적는다.
> 2. **무엇을**: 국가, 빈티지, 가중 방식, 팩터 이름을 구체적으로 적는다.
> 3. **어떻게 확인할지**: 표, 그림, 숫자 중 무엇으로 보여 줄지 적는다.

## 참고
- 저장소 README, `tutorial.py`, `test_qdl.py`, `factor_construction_demo.py` — github.com/jaepil-choi/KAIST-BAF634-2025
- Jensen, T. I., Kelly, B., & Pedersen, L. H. (2023). Is there a replication crisis in finance? *Journal of Finance*, 78(5).
- JKP 데이터 웹사이트 — jkpfactors.com
