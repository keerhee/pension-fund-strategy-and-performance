# -*- coding: utf-8 -*-
"""‘FLAM’ 용어 정정 — W09 강의본 · W09 케이스1 · W12 강의본 · W12 케이스 (2026-09-30).
덱은 팩터 노출 통합(β_P = Σ w_i β_i)을 ‘FLAM’이라 불렀지만, FLAM은 Grinold의 Fundamental Law of Active Management
(IR = IC × √BR)를 가리킨다. 팩터 노출 통합은 ‘팩터 렌즈’로 바꾸고, W09 Grinold 장에 FLAM의 올바른 뜻을 적는다.
W15는 fix_qa_w15.py 가 같은 규칙(slidekit.flam_fix)으로 처리한다.
실행: .venv/bin/python _build/lecfix/fix_flam.py   (재실행 가능 — _구판/FLAM정정_구판_2026-09-30/ 에서 원본 복원)
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import *
from slidekit import flam_fix

R = os.path.dirname(os.path.dirname(HERE))
OLD = f"{R}/_구판/FLAM정정_구판_2026-09-30"; os.makedirs(OLD, exist_ok=True)
DECKS = ["W09_위험관리와성과평가/W09_위험관리와성과평가_강의본", "W09_위험관리와성과평가/W09_케이스1_국부펀드2022성과평가_IC",
         "W12_팩터투자/W12_팩터투자_강의본", "W12_팩터투자/W12_케이스_NPS국내주식팩터도입_IC"]


def backup(rel):
    for ext in (".pptx", ".pdf"):
        src, dst = f"{R}/{rel}{ext}", f"{OLD}/{os.path.basename(rel)}{ext}"
        if os.path.exists(dst): shutil.copy2(dst, src)
        elif os.path.exists(src): shutil.copy2(src, dst)


for rel in DECKS:
    backup(rel)
    prs = Presentation(f"{R}/{rel}.pptx")
    n = flam_fix(prs)
    if rel.endswith("W09_위험관리와성과평가_강의본"):
        assert replace_all(prs, "Grinold의 근본법칙 (1989)", "Grinold의 근본법칙 (1989) — FLAM") == 1
        assert replace_all(prs, "Grinold의 Fundamental Law (1989)", "Grinold의 Fundamental Law (1989) — 줄여서 FLAM") == 1
        assert replace_all(prs, "IR = IC√BR, 그리고 팩터 렌즈의 좌표", "IR = IC√BR(FLAM), 그리고 팩터 렌즈의 좌표") == 1
    left = grep(prs, "FLAM")
    prs.save(f"{R}/{rel}.pptx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(f"{R}/{rel}.pptx"), f"{R}/{rel}.pptx"],
                   check=True, capture_output=True)
    print(os.path.basename(rel), "치환", n, "· 남은 FLAM", left)
