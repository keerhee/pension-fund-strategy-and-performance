# -*- coding: utf-8 -*-
"""dry run: 모든 PPTX(텍스트·표·그룹·노트)와 md 에서 바뀔 표기를 문맥과 함께 뽑는다."""
import glob, os, sys, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import swap, TOK
from pptx import Presentation
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
files = sorted(f for f in glob.glob("**/*.pptx", recursive=True) if not f.startswith(("_구판", "_build", "site")))
def tfs(sh):
    if sh.has_text_frame: yield sh.text_frame
    if getattr(sh, "has_table", False) and sh.has_table:
        for r in sh.table.rows:
            for c in r.cells: yield c.text_frame
    if sh.shape_type == 6:
        for s in sh.shapes: yield from tfs(s)
rep = open(os.path.join(os.path.dirname(__file__), "scan_report.md"), "w")
tot = collections.Counter(); kinds = collections.Counter()
for f in files:
    prs = Presentation(f); hits = []
    for i, s in enumerate(prs.slides, 1):
        srcs = [tf for sh in s.shapes for tf in tfs(sh)]
        if s.has_notes_slide: srcs.append(s.notes_slide.notes_text_frame)
        for tf in srcs:
            for p in tf.paragraphs:
                t = p.text
                if TOK.search(t):
                    log = []; new = swap(t, log)
                    for a, b in log:
                        kinds[(a, b)] += 1
                    hits.append((i, t.strip()[:110], new.strip()[:110], [l for l in log if l[0].startswith("범위")]))
    if hits:
        tot[f] = len(hits)
        rep.write(f"\n## {f} ({len(hits)})\n")
        for i, t, n, r in hits:
            rep.write(f"- s{i}: {t}\n    → {n}{'   ⚠ '+str(r) if r else ''}\n")
rep.close()
print(len(files), "pptx ·", len(tot), "files with hits ·", sum(tot.values()), "paragraphs")
for k, v in sorted(kinds.items(), key=lambda x: -x[1])[:60]: print(v, k)
