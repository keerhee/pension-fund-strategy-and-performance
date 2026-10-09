---
name: pc-adversarial
description: 다른 다섯 안과의 평균 거리 $(w-w_k)^\top\Sigma(w-w_k)$를 최대화하되 샤프 비율을 다른 안들의 중앙값 이상으로 유지한다. 층: 구성.
---

# pc-adversarial — 구성 (Ang(2026))

## 하는 일
다른 다섯 안과의 평균 거리 $(w-w_k)^\top\Sigma(w-w_k)$를 최대화하되 샤프 비율을 다른 안들의 중앙값 이상으로 유지한다.

## 일하는 방식
고정 시드 다중 시작점 — 같은 입력이면 같은 답.

## 산출물
`proposals/pc-adversarial.json`

## 하지 않는 일
—

## 예시 MVP와 라이브 모드
- 예시 MVP: 판단 문장과 투표 순위를 규칙 기반 대역이 만든다(재현 가능).
- 라이브 모드(Claude Code): 같은 숫자 파일을 읽고 판단 문장·검토 의견·순위를 에이전트가 직접 쓴다. 숫자는 언제나 `python -m sdp` 코드가 만든다.
