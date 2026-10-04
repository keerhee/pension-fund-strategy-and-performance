#!/usr/bin/env python3
"""
zeroone-pitch-deck 수식 렌더러 — 로컬판 (pdflatex 없음 → matplotlib mathtext).

원본 render_eq.py와 같은 API: render(tex, filename, fontsize, color, bg) → (경로, ratio).
  * mathtext.fontset="cm" (Computer Modern 외관), dpi 300
  * 배경색을 카드 색으로 굽는다 (투명 금지 — 아이보리 위 흰 사각형 방지)
  * 한글 금지 (mathtext도 한글 글리프가 없어 □로 깨진다)
  * mathtext 제약: \\le·\\ge 대신 \\leq·\\geq, \\tfrac·cases 금지, \\text{} 대신 \\mathrm{}
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq")

INK, PAPER, WHITE = "102027", "F7F5F0", "FFFFFF"
LIME, TEAL, DARK, RED = "B7F34A", "0B6B68", "071A1D", "C00000"

plt.rcParams["mathtext.fontset"] = "cm"


def _check(latex, filename):
    bad = sorted({ch for ch in latex if 0xAC00 <= ord(ch) <= 0xD7A3 or 0x3130 <= ord(ch) <= 0x318F})
    if bad:
        raise ValueError(f"[render_eq] '{filename}': 수식 안에 한글 → {''.join(bad)}")
    for tok in (r"\le ", r"\ge ", r"\tfrac", r"\begin{cases}", r"\text{"):
        if tok in latex + " ":
            raise ValueError(f"[render_eq] '{filename}': mathtext 미지원 토큰 {tok.strip()}")


def render(latex, filename, fontsize=30, color=INK, bg=PAPER, dpi=300, pad=0.14):
    _check(latex, filename)
    os.makedirs(OUT, exist_ok=True)
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_facecolor("#" + bg)
    fig.text(0, 0, f"${latex}$", fontsize=fontsize, color="#" + color)
    path = os.path.join(OUT, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=pad,
                facecolor="#" + bg, transparent=False)
    plt.close(fig)
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.save(path)
    ratio = im.width / im.height
    print(f"  o {filename}  {im.width}x{im.height}  ratio={ratio:.3f}")
    return path, ratio
