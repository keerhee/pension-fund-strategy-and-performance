#!/usr/bin/env bash
# 자막판(추정 타이밍) 렌더. 사용: bash tools/render_captions.sh M7E00 M7E01 ...
cd "$(dirname "$0")/.."
BX=${BX:+--browser-executable=$BX}
for EP in "$@"; do
  python3 tools/timing.py "$EP"
  [ "${NOSOUND:-0}" = "1" ] || python3 tools/sound.py "$EP"
  npx remotion render src/index.ts "$EP" "out/W06_${EP:0:2}_${EP:2}_${SUFFIX:-sound}.mp4" $BX --concurrency=2 --log=error && echo "done $EP"
done
