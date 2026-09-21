# -*- coding: utf-8 -*-
"""배너 배경 막대에 글자가 중복으로 들어간 것을 지운다.

같은 자리(±6px)에 같은 문구를 담은 도형이 둘 있으면, 글이 두 겹으로 찍혀
한 줄로는 멀쩡해 보이다가 두 줄이 되는 순간 어긋나 보인다(W04 강의본 43쪽).
넓은 쪽(배경 막대)의 글자를 지우고, 두 줄이 되는 배너는 막대를 키운다.
실행: .venv/bin/python _build/lecfix/fix_dup_banner.py
"""
import glob, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import Presentation, px, set_text, set_size_px

R = os.path.dirname(os.path.dirname(HERE))
CH_PER_LINE = 45          # 20pt bold 배너의 한 줄 글자 수(대략)

fixed = 0
# 저장소 경로에 [2026] 이 들어 있다 — glob 은 대괄호를 문자클래스로 읽으므로 escape 한다.
for f in sorted(glob.glob(os.path.join(glob.escape(R), "W0*", "*.pptx"))):
    prs = Presentation(f); n = 0
    for s in prs.slides:
        shs = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
        for a in range(len(shs)):
            for b in range(a + 1, len(shs)):
                ta = " ".join(shs[a].text_frame.text.split())
                tb = " ".join(shs[b].text_frame.text.split())
                if ta != tb or len(ta) <= 12:
                    continue
                if abs(px(shs[a])[1] - px(shs[b])[1]) > 6:
                    continue
                wide, narrow = sorted((shs[a], shs[b]), key=lambda sh: -px(sh)[2])
                set_text(wide, "")                       # 배경 막대의 글자를 지운다
                lines = max(1, -(-len(ta) // CH_PER_LINE))
                if lines > 1:                            # 두 줄 이상이면 막대를 키운다
                    need = 30 + 34 * lines
                    for sh in (wide, narrow):
                        if px(sh)[3] < need:
                            set_size_px(sh, h=need)
                n += 1
    if n:
        prs.save(f)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                        os.path.dirname(f), f], check=True, capture_output=True)
        print(f"  {os.path.basename(f)[:50]:52s} {n}곳 정리 · PDF 갱신")
        fixed += n
print(f"총 {fixed}곳")
