# -*- coding: utf-8 -*-
"""‘귀인’ → ‘성과요인분석’ — 다른 빌드 스크립트가 다루지 않는 덱·문서 (2026-09-30).
W09 강의본·케이스1 · W12 2편은 fix_flam.py, W15 제1부·케이스는 fix_qa_w15.py 가 같은 규칙(slidekit.attrib_fix)을 쓴다.
실행: .venv/bin/python _build/lecfix/fix_attrib.py   (재실행 가능 — _구판/성과요인분석_구판_2026-09-30/ 에서 원본 복원)"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import *
from slidekit import attrib_fix, ATTRIB_RULES

R = os.path.dirname(os.path.dirname(HERE))
OLD = f"{R}/_구판/성과요인분석_구판_2026-09-30"; os.makedirs(OLD, exist_ok=True)
DECKS = ["W09_위험관리와성과평가/W09_0_프라이머_성과평가는무엇을견주는가"]
DOCS = ["_과정운영/New_Lecture_with_New_Cases_요약정리.md"]


def backup(rel, exts):
    for ext in exts:
        src, dst = f"{R}/{rel}{ext}", f"{OLD}/{os.path.basename(rel)}{ext}"
        if os.path.exists(dst): shutil.copy2(dst, src)
        elif os.path.exists(src): shutil.copy2(src, dst)


for rel in DECKS:
    backup(rel, (".pptx", ".pdf"))
    prs = Presentation(f"{R}/{rel}.pptx")
    n = attrib_fix(prs)
    prs.save(f"{R}/{rel}.pptx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(f"{R}/{rel}.pptx"), f"{R}/{rel}.pptx"],
                   check=True, capture_output=True)
    print(os.path.basename(rel), n, "· 남은 귀인", grep(prs, "귀인"))
for rel in DOCS:
    stem, ext = os.path.splitext(rel)
    backup(stem, (ext,))
    t = open(f"{R}/{rel}", encoding="utf-8").read(); n = 0
    for a, b in ATTRIB_RULES:
        n += t.count(a); t = t.replace(a, b)
    open(f"{R}/{rel}", "w", encoding="utf-8").write(t)
    print(os.path.basename(rel), n)
