# W06 LDI·GBI 모션그래픽

BAF.60080 6주차 강의본(M7 LDI, M8 GBI)을 장별 모션그래픽으로 만드는 Remotion 프로젝트.

## 나레이션판 만들기 (맥)

```bash
bash make.sh                              # 전 편 23편 (여성 목소리 SunHi)
bash make.sh M8                           # GBI 13편만
bash make.sh M7E03                        # 한 편만
VOICE=ko-KR-InJoonNeural bash make.sh     # 남성 목소리
```

## 편 목록 (M7 LDI)

| 편 | 내용 | 강의본 |
| --- | --- | --- |
| M7E00 | 도입 — 자산이 아니라 자산 대 부채 | pp.1–9 |
| M7E01 | ① 부채와 적립비율 | pp.10–17 |
| M7E02 | ② 할인율 — 같은 약속, 다른 숫자 | pp.18–28 |
| M7E03 | ③ 듀레이션 · DV01 · 볼록성 | pp.29–36 |
| M7E04 | ④ 면역화와 Redington | pp.37–44 |
| M7E05 | ⑤ 잉여금 최적화와 두 블록 | pp.45–49 |
| M7E06 | ⑥ 실무 헤지 수단 | pp.50–54 |
| M7E07 | ⑦ 2022 영국 · 2023 SVB | pp.55–64 |
| M7E08 | ⑨ 모의 IC 복습 (기본 답 공개) | pp.71–75 |
| M7E09 | ⑧ 실습 · LDI 미니 시뮬레이터 | pp.65–70 |

## 편 목록 (M8 GBI)

| 편 | 내용 | 강의본 |
| --- | --- | --- |
| M8E00 | 도입 — 개인의 생활비 약속 = 연금의 부채 | pp.1–7 |
| M8E01 | ① 목표와 위험 — σ가 아니라 확률 | pp.8–13 |
| M8E02 | ② 심리계정 — Thaler · BPT · Das–Markowitz | pp.14–20 |
| M8E03a | ③ 필요 자본 기초 · 방법 1 가장 싼 K | pp.21–33 |
| M8E03b | ③ 방법 2 Das–Markowitz | pp.34–41 |
| M8E03c | ③ 방법 3 몬테카를로 · 세 방법 비교 | pp.42–63 |
| M8E04 | ④ Floor 만들기 — RB에서 GHP로 | pp.64–72 |
| M8E05 | ⑤ 쿠션과 승수 — CPPI에서 Flexicure로 | pp.73–85 |
| M8E06 | ⑥ Floor 운용 규칙과 한계 | pp.86–92 |
| M8E07 | ⑦ GBI와 현실 세계 — 한국 제도 | pp.93–109 |
| M8E08 | ⑧ 기관의 GBI — H대 기금의 세 숫자 | pp.110–117 |
| M8E09 | ⑩ 모의 IC 복습 (기본 답 공개) | pp.123–127 |
| M8E10 | ⑨ 실습 · GBI 설계기 | pp.118–122 |

필요한 것: Node.js 20+, ffmpeg, Python 3 (`brew install node ffmpeg`).
첫 실행 때 npm 패키지와 edge-tts를 설치하고 렌더용 Chrome을 내려받는다.

## 음향 (모던 빌드업)

`tools/sound.py`가 장면 타이밍에 맞춰 배경음을 합성한다(외부 음원 없음). 장면 안에서 패드 → 아르페지오 → 베이스 → 킥 → 하이햇이 차례로 쌓이고, 장면 끝 라이저 → 다음 장면 첫 박 임팩트, 문장마다 블립. 나레이션 구간은 음악을 약 8dB 덕킹한다.

- 음향 없이: `NOSOUND=1 bash make.sh`
- 템포 · 코드 · 레이어 진입 시점은 `tools/sound.py` 상단과 `build()`에서 바꾼다

## 구조

| 경로 | 내용 |
| --- | --- |
| `script/M7E0N.json` | 편별 대본 — `cap`은 화면 자막, `say`는 읽는 문장 |
| `tools/numbers_m7e03.py`, `numbers_m7.py`, `numbers_m8.py` | 화면에 나오는 숫자를 강의본 가정으로 계산 (M8은 gbi_mc.py와 같은 seed·식) |
| `tools/gen_root.py` | `src/episodes/*.tsx`를 Root에 등록 |
| `tools/tts.py` | edge-tts로 문장별 mp3 생성 → `public/audio/` |
| `tools/timing.py` | 음성 길이(없으면 추정)로 장면 타이밍 → `src/data/*.timing.json` |
| `src/episodes/M7E0N.tsx` | 편별 장면 컴포넌트 |
| `tools/stills.sh` | 장면별 스틸 + 컨택트 시트 (점검용) |
| `src/lib/` | 공용 틀(Scene)·애니메이션·KaTeX 수식·카드 |

## 고치는 법

- 문장을 바꾸면 해당 `script/*.json`만 고치고 `bash make.sh M7E0N`을 다시 실행한다. 바뀐 문장의 mp3는 지워야 새로 만든다.
- 미리보기: `npx remotion studio`
- 자막을 끄려면 `Scene`의 `captions` 기본값을 `false`로.
