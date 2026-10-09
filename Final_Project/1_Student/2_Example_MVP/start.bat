@echo off
chcp 65001 >nul
REM 윈도: 이 파일을 더블클릭하면 채점 콘솔이 브라우저에 열린다.
cd /d "%~dp0"
if not exist .venv (
  echo 처음 한 번만: 파이썬 환경을 만든다 (1~2분)...
  py -3 -m venv .venv || python -m venv .venv
  .venv\Scripts\pip install -q -r requirements.txt
)
.venv\Scripts\python -m sdp serve
pause
