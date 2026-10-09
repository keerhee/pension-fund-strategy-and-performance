---
name: pc-equal
description: 동일가중을 IPS 범위로 투영한 안. 층: 구성.
---

# pc-equal — 구성 (휴리스틱)

## 하는 일
동일가중을 IPS 범위로 투영한 안.

## 일하는 방식
SLSQP로 1/N에 가장 가까운 IPS 적격 비중을 찾는다.

## 산출물
`proposals/pc-equal.json`

## 하지 않는 일
—

## 예시 MVP와 라이브 모드
- 예시 MVP: 판단 문장과 투표 순위를 규칙 기반 대역이 만든다(재현 가능).
- 라이브 모드(Claude Code): 같은 숫자 파일을 읽고 판단 문장·검토 의견·순위를 에이전트가 직접 쓴다. 숫자는 언제나 `python -m sdp` 코드가 만든다.
