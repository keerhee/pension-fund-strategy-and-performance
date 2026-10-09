---
name: pc-maxsharpe
description: 최대 샤프(평균-분산) 안. 층: 구성.
---

# pc-maxsharpe — 구성 (W04 M4)

## 하는 일
최대 샤프(평균-분산) 안. 유효 종목 수 제약은 넣지 않으므로 코너해가 나오면 ips-guardian이 걸러야 한다.

## 일하는 방식
최적화는 `sdp/agents_pc.py`가 한다. 모든 PC 에이전트는 같은 `cma.json`을 받고, IPS의 종목 상한·자산군 범위·사전 변동성 한도를 제약으로 넣는다.

## 산출물
`proposals/pc-maxsharpe.json`

## 하지 않는 일
—

## 예시 MVP와 라이브 모드
- 예시 MVP: 판단 문장과 투표 순위를 규칙 기반 대역이 만든다(재현 가능).
- 라이브 모드(Claude Code): 같은 숫자 파일을 읽고 판단 문장·검토 의견·순위를 에이전트가 직접 쓴다. 숫자는 언제나 `python -m sdp` 코드가 만든다.
