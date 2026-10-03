# IC Webtoon Short — 금융 강의 웹툰 숏폼 하네스

revfactory/harness 방식(에이전트 팀 + 스킬)으로 구성한 Claude Code 하네스.
강의 개념 하나 → 6컷 30초 9:16 웹툰 숏폼 MP4.

## 사용
1. 이 폴더를 프로젝트 루트로 두고 Claude Code 실행
2. "IC 일기 다음 화 만들어줘 — 주제: 캐피털 콜" 처럼 요청
3. 결과: `output/ic_webtoon_epNN.mp4`

## 팀
showrunner → scenario-writer → character-designer → panel-artist → qa-reviewer → motion-editor → qa-reviewer

## 구조
.claude/agents/   에이전트 6종
.claude/skills/   오케스트레이터 · panel-render · motion-render
episodes/ep01/    script.json + 검수 정지 컷
render/           render_ep01.py (SVG 작화 + 애니메이션 + BGM)

## 화풍 업그레이드
panel-render 스킬의 backend=image 로 바꾸고 OPENAI_API_KEY 를 설정하면 일러스트 화풍 패널로 교체된다.
