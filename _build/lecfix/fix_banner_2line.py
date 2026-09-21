# -*- coding: utf-8 -*-
"""아래 문장과 겹치는 두 줄 배너를 한 줄로 줄인다(20pt bold 는 약 45자가 한 줄).
실행: .venv/bin/python _build/lecfix/fix_banner_2line.py
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import Presentation, px, set_text, set_size_px, find

R = os.path.dirname(os.path.dirname(HERE))
JOBS = [
    (f"{R}/W04_MVO와블랙리터맨/W04_M4_MVO와공분산추정_강의본.pptx", 43,
     "강건최적화결과는", "강건최적화결과는 “근거 없음”까지만 말한다 — 수치는 조건 ②와 조건 ③이 정한다"),
    (f"{R}/W04_MVO와블랙리터맨/W04_M4_MVO와공분산추정_강의본.pptx", 47,
     "핵심 체험", "핵심 체험 — γ는 “정치적 협상물”이다 : 합의도 판정 조건 ①~④를 통과해야 한다"),
    (f"{R}/W05_리스크패리티와HRP/W05_리스크패리티와HRP_강의본.pptx", 49,
     "정상기엔 현행", "정상기엔 현행, 위기엔 ERC · HRP — 허들 5.5%와 CVaR −15%가 고른다"),
]
touched = set()
for path, page, prefix, new in JOBS:
    prs = Presentation(path)
    sh = find(prs.slides[page - 1], prefix)
    assert sh is not None, (path, page, prefix)
    set_text(sh, new); set_size_px(sh, h=63)
    # 같은 자리의 배경 막대도 높이를 되돌린다
    y0 = px(sh)[1]
    for o in prs.slides[page - 1].shapes:
        if o is not sh and abs(px(o)[1] - y0) <= 6 and px(o)[2] > 1000:
            set_size_px(o, h=63)
    prs.save(path); touched.add(path)
    print(f"  {os.path.basename(path)[:44]:46s} {page}쪽 배너 {len(new)}자로")
for p in touched:
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    os.path.dirname(p), p], check=True, capture_output=True)
print("PDF 갱신", len(touched))
