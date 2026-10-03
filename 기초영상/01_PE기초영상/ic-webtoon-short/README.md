# 연기금 IC 일기 · 시즌 1 — PE 기초 (33화 완결)

부엉이 CIO '부장님'과 펭귄 신입 '펭'이 PE(사모펀드) 개념 하나를 6컷 · 9:16(1080×1920) · 32~43초 웹툰 숏폼으로 푼다.
회차별 주제와 손계산 숫자는 바깥 [`기초영상/README.md`](../../README.md)에 표로 있다.

## 폴더

| 경로 | 내용 | 저장소 |
|---|---|---|
| `episodes/epNN_script.json` | 회차 대본 — 컷별 시간 · 대사 · 손계산 가정과 결과 · LaTeX · fact-check | 추적 |
| `episodes/epNN/` | 검수용 정지 컷 6장 `ic_webtoon_epNN_still_1~6.png` (33화 모두) | 추적 |
| `render/render_epNN.py` | 회차 렌더 스크립트 (SVG 작화 · 애니메이션 · BGM) | 추적 |
| `render/webtoon_lib.py` | 공통 라이브러리 — 캐릭터 · 말풍선 · 컷 · 수식 · 렌더 (EP.12~) | 추적 |
| `render/pe_common.py` | 공통 컷 — 문제 · 반전 · 해설 틀 · 후속 · 막대 (EP.18~) | 추적 |
| `render/eq/` | 회차별 수식 PNG | 추적 |
| `output/ic_webtoon_epNN.mp4` | 완성 영상 33편 | **비추적**(mp4 규칙) — 로컬에만 |
| `.claude/` | 처음 받은 하네스의 에이전트 6종 · 스킬 (참고용) | 추적 |

EP.01~11은 처음 받은 하네스 코드라 공통 부품을 `render_ep01.py`에서 가져온다. EP.12부터는 `webtoon_lib`를,
EP.18부터는 `pe_common`까지 쓴다. 지금 새 회차는 Claude Code 스킬 `ic-webtoon-short`로 만든다.

## 다시 렌더하기

```bash
cd render
PY=".../New_Lecture_with_New_Cases/.venv/bin/python"   # cairosvg · numpy · matplotlib · pillow
$PY render_ep12.py stills   # 정지 컷 6장 → ../output/ (EP.01~11은 ../output/epNN_still_k.png)
$PY render_ep12.py          # MP4 → ../output/ic_webtoon_ep12.mp4 (약 40초 렌더)
```

이 맥에는 pdflatex가 없어 수식 PNG는 matplotlib mathtext로 굽는다(`webtoon_lib.latex_png`가 자동 대체).

## 유튜브

NeoAsset 채널 재생목록 **연기금 운용전략과 성과평가 · PE 기초 IC 일기 (Shorts)**에 하루 4편씩 올린다
(2026-10-03 EP.01~04, 10-04 ~ 10-11 예약으로 EP.33까지). 업로드 메모·자막은 저장소 밖
`lectures/_youtube_pension/pe_shorts/`에서 대본 JSON으로 만든다.
