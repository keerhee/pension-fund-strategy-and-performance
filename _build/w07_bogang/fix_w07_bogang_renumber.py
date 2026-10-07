# -*- coding: utf-8 -*-
"""W07 강의본 — 보강 번호 바꿈 반영 (2026-10-03).

보강 1 = 「처음 배우는 TDF」(새로 추가, w07_tdf_basics.js)
보강 2 = 「처음 배우는 강화학습」(기존 보강 1, w06_rl_basics.js)

강의본에서 RL 보강을 가리키는 두 곳을 '보강 2'로 고친다.
  3쪽  먼저 읽는 용어 ② — "3교시 · 기초는 보강 1"
  31쪽 3교시 · 상태 — "기초(…)는 W07 보강 1 ‘처음 배우는 강화학습’"
실행: .venv/bin/python _build/lecfix/fix_w07_bogang_renumber.py   (재실행 가능 — 이미 고쳐졌으면 0건)
그다음 강의본 PDF를 다시 내보낸다(Keynote/PowerPoint 또는 soffice).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import Presentation, replace_all

R = os.path.dirname(os.path.dirname(HERE))
P = f"{R}/W07_동적포트폴리오와장기투자/W07_동적포트폴리오와장기투자_강의본.pptx"

prs = Presentation(P)
pairs = [("기초는 보강 1", "기초는 보강 2"),
         ("W07 보강 1 ‘처음 배우는 강화학습’", "W07 보강 2 ‘처음 배우는 강화학습’")]
total = 0
for old, new in pairs:
    n = replace_all(prs, old, new)
    print(f"{n}건  {old} → {new}")
    total += n
if total:
    prs.save(P)
    print("저장:", os.path.basename(P))
else:
    print("바꿀 곳이 없습니다 — 이미 반영됐습니다.")
