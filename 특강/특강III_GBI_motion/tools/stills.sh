#!/usr/bin/env bash
# 장면 끝 직전 프레임 스틸 + 컨택트 시트. 사용: bash tools/stills.sh M7E01
set -e; EP=$1; cd "$(dirname "$0")/.."
BX=${BX:+--browser-executable=$BX}
mkdir -p out/stills/$EP
FR=$(python3 -c "import json;T=json.load(open('src/data/$EP.timing.json'));print(' '.join(str(s['from_']+s['dur']-20) for s in T['scenes']))")
for fr in $FR; do npx remotion still src/index.ts $EP out/stills/$EP/f$fr.png --frame=$fr $BX --log=error; done
python3 - "$EP" $FR <<'PY'
import sys; from PIL import Image
ep, frs = sys.argv[1], sys.argv[2:]
ims=[Image.open(f'out/stills/{ep}/f{f}.png').resize((960,540)) for f in frs]
rows=(len(ims)+1)//2; s=Image.new('RGB',(1920,540*rows))
for i,im in enumerate(ims): s.paste(im,((i%2)*960,(i//2)*540))
s.save(f'out/stills/{ep}/sheet.png')
PY
echo out/stills/$EP/sheet.png
