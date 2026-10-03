---
name: motion-render
description: 패널을 애니메이션 MP4로 렌더한다. SVG 프레임을 cairosvg로 래스터화해 ffmpeg로 인코딩하고, 코드 진행 패드 BGM과 컷 전환 효과음을 합성한다.
---
- 준비: `pip install cairosvg numpy pillow`, ffmpeg, Noto Sans CJK 폰트
- 실행: `python3 render/render_epNN.py` → `output/ic_webtoon_epNN.mp4` (32초 기준 약 1~2분)
- 애니메이션 함수: back(팝), ease_out(슬라이드), prog(t, 시작, 길이)
- Remotion으로 옮기려면 컷 함수를 React 컴포넌트로 1:1 변환(useCurrentFrame → t).
