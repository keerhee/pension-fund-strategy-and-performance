#!/bin/zsh
# swap_teams_guide.py 다음 — 바뀐 W06 과제 docx 세 개를 Pretendard 사본으로 바꿔 PDF로.
set -e
H=${0:A:h}; D="$H/../../Assignment/W06_Team_Assignment/1_Student"; T=$(mktemp -d)
for f in W06_Assignment_Guide W06_Team3_Default_Option W06_Team4_H_University; do
  /usr/bin/python3 "$H/../to_pretendard.py" "$D/$f.docx" "$T/$f.docx"
done
(cd "$T" && soffice --headless --convert-to pdf *.docx >/dev/null 2>&1)
for f in W06_Assignment_Guide W06_Team3_Default_Option W06_Team4_H_University; do cp "$T/$f.pdf" "$D/"; done
rm -rf "${T:?}"
