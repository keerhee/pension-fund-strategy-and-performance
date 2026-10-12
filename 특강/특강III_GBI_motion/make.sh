#!/usr/bin/env bash
# 나레이션판 렌더 (맥)
#   bash make.sh               → 전 편 (LDI M7E00~M7E09 + GBI M8E00~M8E10)
#   bash make.sh M7            → LDI만 · bash make.sh M8 → GBI만
#   bash make.sh M7E03         → 한 편만
#   VOICE=ko-KR-InJoonNeural bash make.sh   → 남성 목소리
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${VOICE:-ko-KR-SunHiNeural}"
ALL_M7="M7E00 M7E01 M7E02 M7E03 M7E04 M7E05 M7E06 M7E07 M7E08 M7E09"
ALL_M8="M8E00 M8E01 M8E02 M8E03a M8E03b M8E03c M8E04 M8E05 M8E06 M8E07 M8E08 M8E09 M8E10"
if [ $# -eq 0 ]; then set -- $ALL_M7 $ALL_M8
elif [ "$1" = "M7" ]; then set -- $ALL_M7
elif [ "$1" = "M8" ]; then set -- $ALL_M8; fi
command -v node >/dev/null || { echo "Node.js가 필요합니다: brew install node"; exit 1; }
command -v ffprobe >/dev/null || { echo "ffmpeg가 필요합니다: brew install ffmpeg"; exit 1; }
[ -d node_modules ] || npm install
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q edge-tts numpy
echo "▶ 화면 숫자 계산"
.venv/bin/python tools/numbers_m7e03.py >/dev/null
.venv/bin/python tools/numbers_m7.py >/dev/null
.venv/bin/python tools/numbers_m8.py >/dev/null
mkdir -p out
for EP in "$@"; do
  echo "▶ $EP — 나레이션 생성 ($VOICE)"; .venv/bin/python tools/tts.py "$EP" "$VOICE"
  .venv/bin/python tools/timing.py "$EP"
  [ "${NOSOUND:-0}" = "1" ] || .venv/bin/python tools/sound.py "$EP"   # 빌드업 배경음 (NOSOUND=1이면 생략)
  OUT="out/W06_${EP:0:2}_${EP:2}_narrated.mp4"
  npx remotion render src/index.ts "$EP" "$OUT" --log=error
  echo "  완료: $OUT"
done
