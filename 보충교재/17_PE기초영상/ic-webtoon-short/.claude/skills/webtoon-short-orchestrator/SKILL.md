---
name: webtoon-short-orchestrator
description: "웹툰 숏폼 만들어줘", "IC 일기 다음 화", "강의 주제를 웹툰 영상으로" 요청 시 사용. 금융 강의 개념 하나를 6컷 30초 9:16 웹툰 숏폼 영상으로 만드는 에이전트 팀을 순서대로 지휘한다.
---
# 파이프라인
1. showrunner → `episodes/epNN/brief.md`
2. scenario-writer → `episodes/epNN/script.json`
3. character-designer → 레퍼런스 시트 확인(새 표정이 필요할 때만 갱신)
4. panel-artist → 컷별 정지 프레임 `output/still_N.png` (panel-render 스킬)
5. qa-reviewer → 정지 컷 검수, 실패 시 4로 (최대 2회)
6. motion-editor → `output/ic_webtoon_epNN.mp4` (motion-render 스킬)
7. qa-reviewer → MP4에서 컷별 프레임 추출 후 최종 검수

# 병렬화
- 4단계: 컷 6개를 panel-artist 서브에이전트 2~3개로 나눠 동시 작업
- 5단계 검수는 제작에 참여하지 않은 에이전트가 맡는다

# 진화
회차가 끝나면 사용자 피드백을 `/harness:evolve` 로 에이전트·스킬에 반영한다.
