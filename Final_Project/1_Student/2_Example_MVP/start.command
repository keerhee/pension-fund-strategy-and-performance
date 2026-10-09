#!/bin/bash
# 맥: 이 파일을 더블클릭하면 채점 콘솔이 브라우저에 열린다.
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "처음 한 번만: 파이썬 환경을 만든다 (1~2분)…"
  python3 -m venv .venv && ./.venv/bin/pip install -q -r requirements.txt || { echo "python3 가 필요하다: https://www.python.org/downloads/"; read; exit 1; }
fi
./.venv/bin/python -m sdp serve
