# -*- coding: utf-8 -*-
"""보충교재 15 — FLAM 일반화 식 문서의 빠진 수식 그림 3개(‘[image: 수식]’ 자리)를 채운다. 자리가 없으면 아무것도 안 한다.
실행: uv run --with python-docx --with matplotlib python _build/lecfix/patch_flam_doc.py"""
import os, glob, subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(R, "보충교재", "15_적극적운용의기본법칙")
DOC = glob.glob(os.path.join(glob.escape(D), "*.docx"))[0]
TEX = [r"\mathrm{Cov}(\varepsilon, z)=\mathrm{Cov}(r,z)-b\,\mathrm{Var}(z)=0",
       r"E[r\mid z]=\mu_r+b\,(z-\mu_z)+E[\varepsilon\mid z]=\mu_r+\frac{\mathrm{Cov}(r,z)}{\mathrm{Var}(z)}\,(z-\mu_z)",
       r"IR^{2}=IC^{2}\cdot BR,\qquad IR_{\mathrm{total}}^{2}=\sum_k IR_k^{2}"]
matplotlib.rcParams["mathtext.fontset"] = "cm"
doc = Document(DOC)
slots = [p for p in doc.paragraphs if p.text.strip() == "[image: 수식]"]
print("빈 자리", len(slots))
for i, (p, tex) in enumerate(zip(slots, TEX)):
    png = os.path.join(HERE, "_art", f"flam_doc_eq{i+1}.png")
    fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, f"${tex}$", fontsize=14, color="black")
    fig.savefig(png, dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="white"); plt.close(fig)
    from PIL import Image
    w, h = Image.open(png).size
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    p.add_run().add_picture(png, width=Emu(int(w / 300 * 914400)))
if slots:
    doc.save(DOC)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", D, DOC], check=True, capture_output=True)
print("저장", DOC)
