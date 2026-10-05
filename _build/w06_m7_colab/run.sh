#!/bin/bash
# usage: run.sh 01   → build_01.py로 노트북을 만들고 실행해 출력까지 저장 (run.sh readme → README.md)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../../W06_LDI와GBI/W06_M7_실습_Colab"
UV="uv run -q --with numpy --with scipy --with matplotlib --with nbconvert --with ipykernel --with nbformat"
cd "$HERE"
if [ "$1" = "readme" ]; then $UV python build_readme.py; exit; fi
f=$($UV python build_$1.py | sed -n 's/^wrote .*\/\([^/]*\.ipynb\) [0-9]* cells$/\1/p')
echo "built: $f"
cd "$OUT"
s=$(python3 -c 'import time;print(time.time())')
$UV jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 "$f" 2>&1 | grep -v "^\[NbConvertApp\] Writing" | tail -25
python3 -c "import time;print('elapsed %.1f s' % (time.time()-$s))"
