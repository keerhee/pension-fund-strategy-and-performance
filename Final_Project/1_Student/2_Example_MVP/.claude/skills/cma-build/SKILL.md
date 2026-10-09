---
name: cma-build
description: 자율주행 포트폴리오 예시 MVP — cma-build 절차
---

# cma-build

1. `data.returns(as_of)`로 직전 84개월을 읽는다(시점 잠금).
2. 기대수익률: $\hat\mu_i=(1-\delta)\bar r_i+\delta\,\bar r$, δ는 `config/params.json`(현재 0.5).
3. 공분산: Ledoit–Wolf 수축, 연율화 ×12.
4. `cma.json`에 as_of·추정 구간·δ·수축 강도·무위험 수익률(DGS3MO)을 기록한다.

이 파일은 하네스 보호 파일이다. 에이전트가 고치면 되돌려진다.
