# -*- coding: utf-8 -*-
"""rework_m7.py의 도구(수식 PNG·그림 배치)를 패치 스크립트가 같이 쓰도록 떼어 둔 것."""
import os
from pptx.util import Emu
from PIL import Image
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
EQ = os.path.join(HERE, "eq"); os.makedirs(EQ, exist_ok=True)
EMU = 9525
SCALE = 3.12

def render(tex, name, fontsize=30, color="#102027", bg="#F7F5F0"):
    bad = [c for c in tex if 0xAC00 <= ord(c) <= 0xD7A3]
    assert not bad, f"수식 안 한글: {name}"
    path = os.path.join(EQ, name)
    with plt.rc_context({"mathtext.fontset": "cm"}):
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, f"${tex}$", fontsize=fontsize, color=color)
        fig.savefig(path, dpi=220, bbox_inches="tight", pad_inches=0.12, facecolor=bg)
        plt.close(fig)
    Image.open(path).convert("RGB").save(path)
    return path

def size_px(path, maxw=None, maxh=None):
    w, h = Image.open(path).size
    w, h = w / SCALE, h / SCALE
    s = min(1.0, (maxw / w) if maxw else 1.0, (maxh / h) if maxh else 1.0)
    return w * s, h * s

def add_pic(slide, path, x, y, w, h, before=None):
    pic = slide.shapes.add_picture(path, Emu(int(x * EMU)), Emu(int(y * EMU)), Emu(int(w * EMU)), Emu(int(h * EMU)))
    if before is not None:   # z-순서: 지운 그림 자리에
        before.addprevious(pic._element)
    return pic

def remove(shape): shape._element.getparent().remove(shape._element)

def set_px(shape, x=None, y=None, w=None, h=None):
    if x is not None: shape.left = Emu(int(x * EMU))
    if y is not None: shape.top = Emu(int(y * EMU))
    if w is not None: shape.width = Emu(int(w * EMU))
    if h is not None: shape.height = Emu(int(h * EMU))

