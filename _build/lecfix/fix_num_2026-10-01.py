# -*- coding: utf-8 -*-
"""수치 정정 2건 (2026-10-01, 중간고사 문항 검산 중 발견).
  W04 M4 강의본 11쪽: 60/40 변동성 약 10.16% → 10.19%  (0.36·0.0256 + 0.16·0.0025 + 2·0.6·0.4·0.2·0.16·0.05 = 0.010384, √ = 10.19%)
  W06 강의본 19쪽: 인적자본 12억 · 금융자산 2억 → 총 부의 83% → 86%  (12 ÷ 14 = 85.7%)
실행: .venv/bin/python _build/lecfix/fix_num_2026-10-01.py  (재실행 가능 — _구판/수치정정_구판_2026-10-01/ 에서 원본 복원)
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import *
R = os.path.dirname(os.path.dirname(HERE))
OLD = f"{R}/_구판/수치정정_구판_2026-10-01"; os.makedirs(OLD, exist_ok=True)
JOBS = [("W04_MVO와블랙리터맨/W04_M4_MVO와공분산추정_강의본", [("약 10.16%", "약 10.19%")]),
        ("W06_동적포트폴리오와장기투자/W06_동적포트폴리오와장기투자_강의본", [("총 부의 83%", "총 부의 86%")])]
for rel, rules in JOBS:
    for ext in (".pptx", ".pdf"):
        src, dst = f"{R}/{rel}{ext}", f"{OLD}/{os.path.basename(rel)}{ext}"
        if os.path.exists(dst): shutil.copy2(dst, src)
        elif os.path.exists(src): shutil.copy2(src, dst)
    prs = Presentation(f"{R}/{rel}.pptx")
    for a, b in rules:
        n = replace_all(prs, a, b); assert n == 1, (rel, a, n)
    prs.save(f"{R}/{rel}.pptx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(f"{R}/{rel}"), f"{R}/{rel}.pptx"],
                   check=True, capture_output=True)
    print("고침:", os.path.basename(rel))
