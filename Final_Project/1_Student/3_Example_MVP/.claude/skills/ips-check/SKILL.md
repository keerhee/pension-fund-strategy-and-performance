---
name: ips-check
description: 자율주행 포트폴리오 예시 MVP — ips-check 절차
---

# ips-check

1. `ips.md` 부록 A의 yaml을 읽는다.
2. 비중 합·공매도·종목 상한·자산군 범위·유효 종목 수 $N_{\text{eff}}=1/\sum w_i^2\ge4$·사전 변동성을 판정한다.
3. 위반 사유를 문장으로 남기고 표결 목록에서 뺀다.

이 파일은 하네스 보호 파일이다. 에이전트가 고치면 되돌려진다.
