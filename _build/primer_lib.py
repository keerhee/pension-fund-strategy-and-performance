# -*- coding: utf-8 -*-
"""프라이머 그림의 공용 뼈대.

zeroone-pitch-deck 룰북 §7.1·§7.2를 따른다.
 · 배경은 투명이 아니라 아이보리(#F7F5F0) — 투명이면 아이보리 위에서 흰 사각형으로 뜬다
 · figSlide 가용 영역에 맞춰 가로:세로 ≈ 2.5 로 통일한다
 · 그림 안 글씨는 슬라이드에서 16pt 아래로 내려가지 않게 크게 그린다
주차별 스크립트는 이 모듈을 불러 fig()/save()만 쓴다.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager as fm, pyplot as plt

FONTFILE = "/Users/keerhee/Library/Fonts/NotoSansCJK.ttc"
fm.fontManager.addfont(FONTFILE)
KO = fm.FontProperties(fname=FONTFILE).get_name()

# ZeroOne 토큰 (룰북 §1.1)
INK, PAPER, WHITE = "#102027", "#F7F5F0", "#FFFFFF"
LIME, TEAL, RED = "#B7F34A", "#0B6B68", "#C00000"
BLUE, AMBER, MUTED, HAIR = "#4677F5", "#F3A33C", "#64757D", "#DDE3E2"
DARK = "#071A1D"

plt.rcParams.update({
    "font.family": KO, "axes.unicode_minus": False, "mathtext.fontset": "cm",
    "figure.dpi": 170, "savefig.dpi": 170,
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": HAIR,
})

WIDE = (12.9, 5.0)          # 2.58 — figSlide 가용 영역에 맞춘 비율
_OUT = None


def out_dir(week):
    """_art/<week>/ 를 만들고 이후 save()의 기본 목적지로 삼는다."""
    global _OUT
    _OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_art", week)
    os.makedirs(_OUT, exist_ok=True)
    print(f"[{week}] →", _OUT)
    return _OUT


def clean(ax, grid="y"):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=HAIR, lw=1)
        ax.set_axisbelow(True)
    ax.tick_params(labelsize=13)


def fig(size=WIDE, ncol=1, **kw):
    return plt.subplots(1, ncol, figsize=size, **kw) if ncol > 1 else plt.subplots(figsize=size)


def save(f, name, note=None):
    """note는 그림 우하단의 작은 단서 — 지어낸 숫자임을 밝히는 자리."""
    if note:
        f.text(0.995, 0.006, note, ha="right", va="bottom", fontsize=9, color=MUTED)
    p = os.path.join(_OUT, name)
    f.savefig(p, bbox_inches="tight", facecolor=PAPER, pad_inches=0.18)
    plt.close(f)
    from PIL import Image
    w, h = Image.open(p).size
    print(f"   {name:26s} {w}x{h}  ratio={w/h:.3f}")
    return p


def equation(tex, name="equation.png", fontsize=42, width=11.4):
    r"""수식 PNG. 이 환경에 pdflatex이 없어 matplotlib의 Computer Modern으로 굽는다.
    글자꼴은 LaTeX 기본과 같은 CM이다. 배경은 얹을 카드 색(PAPER)을 구워 넣는다 — 룰북 §7.5.
    LaTeX 문자열 안에 한글을 넣지 않는다(라벨은 슬라이드 텍스트로).
    mathtext가 모르는 명령이 있다 — \bigl·\bigr·\underbrace·\text 는 쓰지 말고
    \left(·\right)·\mathrm 을 쓴다."""
    assert not any('가' <= c <= '힣' for c in tex), "수식 안에 한글이 있습니다"
    f = plt.figure(figsize=(width, 1.9), facecolor=PAPER)
    f.text(.5, .5, tex, ha="center", va="center", fontsize=fontsize, color=INK)
    p = os.path.join(_OUT, name)
    f.savefig(p, bbox_inches="tight", facecolor=PAPER, pad_inches=0.26)
    plt.close(f)
    from PIL import Image
    w, h = Image.open(p).size
    print(f"   {name:26s} {w}x{h}  ratio={w/h:.3f}")
    return p


# ── SVG 개념 도해 ────────────────────────────────────────────────
def svg(name, body, w=1600, h=620):
    import cairosvg
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{PAPER}"/>'
           f'<style>text{{font-family:"Noto Sans CJK KR","Noto Sans CJK JP",sans-serif}}</style>'
           f'<defs>'
           f'<marker id="aT" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">'
           f'<path d="M0,0 L9,4 L0,8 z" fill="{TEAL}"/></marker>'
           f'<marker id="aR" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">'
           f'<path d="M0,0 L9,4 L0,8 z" fill="{RED}"/></marker>'
           f'<marker id="aM" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">'
           f'<path d="M0,0 L9,4 L0,8 z" fill="{MUTED}"/></marker>'
           f'</defs>{body}</svg>')
    p = os.path.join(_OUT, name)
    cairosvg.svg2png(bytestring=doc.encode("utf-8"), write_to=p, output_width=w * 2)
    print(f"   {name:26s} {w*2}x{h*2}  ratio={w/h:.3f}")
    return p


def box(x, y, w, h, title, sub=(), fill=WHITE, stroke=HAIR, tc=INK, sc=MUTED, ts=34, ss=26):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="2"/>'
         f'<text x="{x+w/2}" y="{y+46}" font-size="{ts}" font-weight="700" fill="{tc}" '
         f'text-anchor="middle">{title}</text>')
    for i, ln in enumerate(sub):
        s += (f'<text x="{x+w/2}" y="{y+86+i*34}" font-size="{ss}" fill="{sc}" '
              f'text-anchor="middle">{ln}</text>')
    return s


def limebox(x, y, w, h, title, sub=()):
    """도착점 — 라임은 슬라이드(그림)당 한 블록만 (룰북 §1.1)."""
    return box(x, y, w, h, title, sub, fill=LIME, stroke=INK, tc=DARK, sc=DARK)


def darkbox(x, y, w, h, title, sub=()):
    return box(x, y, w, h, title, sub, fill=DARK, stroke=DARK, tc=LIME, sc="#9FB0B2")


def arrow(x1, y1, x2, y2, color=TEAL, mk="aT", wt=5, label=None, lc=None):
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
         f'stroke-width="{wt}" marker-end="url(#{mk})"/>')
    if label:
        s += (f'<text x="{(x1+x2)/2}" y="{min(y1,y2)-14}" font-size="26" '
              f'fill="{lc or color}" text-anchor="middle">{label}</text>')
    return s


def text(x, y, t, size=27, color=INK, anchor="middle", bold=False):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
            + (' font-weight="700"' if bold else '') + f'>{t}</text>')


def hrule(x1, x2, y, color=HAIR, wt=2):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{wt}"/>'


def vrule(x, y1, y2, color=HAIR, wt=2):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="{wt}"/>'
