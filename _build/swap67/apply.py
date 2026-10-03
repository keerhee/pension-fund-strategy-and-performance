# -*- coding: utf-8 -*-
"""W06 ↔ W07 맞바꾸기 — PPTX 텍스트(본문·표·그룹·노트)에 적용. --apply 없으면 dry run.
예외: 강의 주차가 아닌 숫자(M7=Magnificent 7, 다른 과정의 n주차, 문제 번호 W1~W12), 제출 마감(달력 기준), 집합 표기.
원본은 _구판/W06W07교환_구판_2026-10-03/ 에 같은 상대경로로 보관(이미 있으면 거기서 되돌려 재실행을 결정적으로)."""
import glob, os, sys, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import swap, TOK
from pptx import Presentation
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
APPLY = "--apply" in sys.argv
BK = "_구판/W06W07교환_구판_2026-10-03"
SKIP_FILES = ("Risk_Based_Allocation_Main_VIII", "Cerberus_Global_NPL", "Direct_Lending_Course", "Residential_Credit_ABS_Course",
              "04_RL_Workbook_zeroone_II")
NO_WEEKWORD = ("Self_Driving_AM_Course_Based_Proposal", "W14_대체투자와비유동성_강의본")   # 'n주'만 끈다
KEEP_PARA = ("제출 —", "제출 —", "두 단위를 함께 쓰는 주차는")
PRE = [("W1~W6은 자산", "W1~W5는 자산"), ("W1~W6은 자산 중심", "W1~W5는 자산 중심"), ("자산 중심 (W1~W6)", "자산 중심 (W1~W5)")]

def tfs(sh):
    if sh.has_text_frame: yield sh.text_frame
    if getattr(sh, "has_table", False) and sh.has_table:
        for r in sh.table.rows:
            for c in r.cells: yield c.text_frame
    if sh.shape_type == 6:
        for s in sh.shapes: yield from tfs(s)

def swap_para(p, noweek):
    t = p.text
    if not TOK.search(t) or any(k in t for k in KEEP_PARA):
        return 0
    new = t
    for a, b in PRE:
        new = new.replace(a, b)
    if noweek:
        # 'n주' 표기는 건드리지 않는다: 임시로 가린다
        new = re.sub(r"(?<![0-9])([67])(주)", lambda m: m.group(1) + "" + m.group(2), new)
    new = swap(new)
    new = new.replace("", "")
    if new == t:
        return 0
    runs = p.runs
    # run 단위로 먼저 시도 — 서식 보존
    joined = "".join(r.text for r in runs)
    if joined == t and len(runs) > 1:
        # 각 run 을 독립 치환해 같은 결과가 나오면 run 서식 그대로
        cand = [r.text for r in runs]
        cand2 = []
        for c in cand:
            c2 = c
            for a, b in PRE: c2 = c2.replace(a, b)
            if noweek:
                c2 = re.sub(r"(?<![0-9])([67])(주)", lambda m: m.group(1) + "" + m.group(2), c2)
            c2 = swap(c2).replace("", "")
            cand2.append(c2)
        if "".join(cand2) == new:
            for r, c2 in zip(runs, cand2): r.text = c2
            return 1
    if runs:
        runs[0].text = new
        for r in runs[1:]: r.text = ""
    return 1

files = sorted(f for f in glob.glob("**/*.pptx", recursive=True) if not f.startswith(("_구판", "_build", "site")))
total = 0; touched = []
for f in files:
    if any(k in f for k in SKIP_FILES): continue
    if APPLY:
        b = os.path.join(BK, f)
        if os.path.exists(b): shutil.copy2(b, f)
    prs = Presentation(f); n = 0
    noweek = any(k in f for k in NO_WEEKWORD)
    for s in prs.slides:
        srcs = [tf for sh in s.shapes for tf in tfs(sh)]
        if s.has_notes_slide: srcs.append(s.notes_slide.notes_text_frame)
        for tf in srcs:
            for p in tf.paragraphs:
                n += swap_para(p, noweek)
    if n:
        touched.append((f, n)); total += n
        if APPLY:
            b = os.path.join(BK, f)
            if not os.path.exists(b):
                os.makedirs(os.path.dirname(b), exist_ok=True); shutil.copy2(f, b)
                pdf = f[:-5] + ".pdf"
                if os.path.exists(pdf): shutil.copy2(pdf, b[:-5] + ".pdf")
            prs.save(f)
for f, n in touched: print(f"{n:4d}  {f}")
print("files", len(touched), "paragraphs", total, "(APPLIED)" if APPLY else "(dry run)")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "touched.txt"), "w").write("\n".join(f for f, _ in touched))
