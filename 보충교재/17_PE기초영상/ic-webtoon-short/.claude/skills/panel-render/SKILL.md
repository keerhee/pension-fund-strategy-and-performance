---
name: panel-render
description: script.json의 컷을 패널로 그린다. backend=svg(기본, 오프라인·무료) 또는 backend=image(gpt-image 등 이미지 API, 일러스트 화풍).
---
# backend=svg (기본)
- `render/render_epNN.py` 에 컷 함수 `cutN(t)` 를 추가한다. 공통 부품: bg, burst, punch(효과 타이포), bubble(말풍선), panel_frame, owl, penguin.
- 검수용 정지 컷: `python3 render/render_epNN.py stills`

# backend=image
- 환경변수 `OPENAI_API_KEY` 필요. 레퍼런스 시트 PNG를 참조 이미지로 넣고, 프롬프트에 화풍·구도·말풍선 문구를 명시.
- 한글 말풍선은 이미지 생성에 맡기지 말고 생성 후 SVG 레이어로 덧입힌다(오탈자 방지).
- 컷당 2~3장 생성 → qa-reviewer가 1장 선택.
