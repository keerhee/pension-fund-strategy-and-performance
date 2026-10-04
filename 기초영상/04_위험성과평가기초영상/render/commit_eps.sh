#!/bin/zsh
# 사용: commit_eps.sh 02 03 … — 정지 컷을 episodes/epNN로 옮기고 회차 파일을 커밋 대상에 올린다
cd "${0:A:h}/.."
for e in "$@"; do
  mkdir -p episodes/ep$e
  mv output/ic_webtoon_s4_ep${e}_still_*.png episodes/ep$e/ 2>/dev/null
  git add episodes/ep$e episodes/ep${e}_script.json render/render_ep$e.py render/eq/ep${e}_*.png
done
git add render/s4kit.py render/sheet.py render/commit_eps.sh
