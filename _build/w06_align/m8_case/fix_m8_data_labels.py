# -*- coding: utf-8 -*-
"""W06_M8_케이스데이터 의 라벨만 바꾼다(숫자 불변): 펀드오브펀드 → 재간접, 강의 N교시 → 단원. 원본은 _구판/W06_정합전_2026-10-05/W06_M8_케이스데이터/."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC = f"{R}/_구판/W06_정합전_2026-10-05/W06_M8_케이스데이터"; DST = f"{R}/W06_LDI와GBI/W06_M8_케이스데이터"
REP = [("펀드오브펀드·세컨더리", "재간접·세컨더리"), ("펀드오브펀드 · 세컨더리", "재간접 · 세컨더리"),
       ("펀드오브펀드 경유", "재간접 경유"), ("(Safety 버킷 — 강의 1교시)", "(Safety 버킷 — 강의 단원 ①)"),
       ("— 강의 2교시)", "— 강의 단원 ⑤⑥)")]
for f in sorted(os.listdir(SRC)):
    s = open(f"{SRC}/{f}", encoding="utf-8").read()
    for a, b in REP: s = s.replace(a, b)
    assert "펀드오브펀드" not in s and "교시" not in s, f
    open(f"{DST}/{f}", "w", encoding="utf-8").write(s); print("ok", f)
