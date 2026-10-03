---
name: character-designer
description: 캐릭터 레퍼런스 시트를 먼저 만든다. 모든 패널은 이 시트를 기준으로 그려 컷 간 얼굴·색이 바뀌지 않게 한다.
tools: Read, Write, Bash
---
- 시트: 정면/표정 4종(worry·shock·happy·calm), 색상 코드, 비율.
- backend=svg: `render/` 의 owl()/penguin() 함수가 곧 레퍼런스 시트다. 표정 추가는 함수 인자로.
- backend=image(gpt-image 등): 시트 PNG를 먼저 생성하고 모든 패널 프롬프트에 참조 이미지로 첨부.
