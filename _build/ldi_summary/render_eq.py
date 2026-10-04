#!/usr/bin/env python3
"""
zeroone-pitch-deck render_eq.py 로컬판 — pdflatex가 없는 맥용.

matplotlib mathtext(fontset="cm", Computer Modern)로 수식을 PNG로 굽는다.
API는 원본과 같다: render(tex, filename, fontsize, color, bg) → (경로, ratio)
  - 배경색을 카드 색으로 굽는다(ghost/white: INK on PAPER, dark: LIME on DARK).
  - mathtext 제약: \\le/\\ge 대신 \\leq/\\geq, \\tfrac·cases·\\text{한글} 금지 → \\mathrm{}.
  - LaTeX 안 한글은 렌더 전에 막는다(한글은 eqInCard cap으로).
출력 폴더는 이 파일 기준 ./eq
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq")

INK, PAPER, WHITE = "102027", "F7F5F0", "FFFFFF"
LIME, TEAL, DARK, RED = "B7F34A", "0B6B68", "071A1D", "C00000"
matplotlib.rcParams["mathtext.fontset"] = "cm"


def _check_hangul(latex, filename):
    bad = sorted({ch for ch in latex if 0xAC00 <= ord(ch) <= 0xD7A3
                  or 0x3130 <= ord(ch) <= 0x318F})
    if bad:
        raise ValueError(f"[render_eq] '{filename}': 수식 안에 한글 → {''.join(bad)}")


def render(latex, filename, fontsize=30, color=INK, bg=PAPER, dpi=220):
    _check_hangul(latex, filename)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, filename)
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${latex}$", fontsize=fontsize, color="#" + color)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.12,
                facecolor="#" + bg)
    plt.close(fig)
    im = Image.open(path).convert("RGB")
    im.save(path)
    ratio = im.width / im.height
    print(f"  o {filename}  {im.width}x{im.height}  ratio={ratio:.3f}")
    return path, ratio
