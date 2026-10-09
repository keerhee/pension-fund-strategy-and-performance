---
name: portfolio-construct
description: 자율주행 포트폴리오 예시 MVP — portfolio-construct 절차
---

# portfolio-construct

1. 6개 PC 에이전트가 같은 `cma.json`을 받는다.
2. 제약: 비중 합 1, 종목 ≤ 30%, 자산군 범위, 사전 변동성 ≤ 10%. 유효 종목 수는 넣지 않는다.
3. 적대적 분산자는 다른 다섯 안이 나온 뒤 마지막에 만든다.
4. 각 안을 `proposals/{agent}.json`에 저장한다.

이 파일은 하네스 보호 파일이다. 에이전트가 고치면 되돌려진다.
