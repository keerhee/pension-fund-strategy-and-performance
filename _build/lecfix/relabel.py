"""Repaint a text label inside a flat-colour figure PNG.

find the label's ink box inside a search region, calibrate the font size on a reference label
drawn in the same style, cover the old label with its background and draw the new text centred
on the same spot."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

TTC = '/Users/keerhee/Library/Fonts/NotoSansCJK.ttc'
FACE = {'Bold': 36, 'Medium': 16, 'Regular': 26}


def ink_box(im, region, thresh=60):
    a = np.asarray(im.crop(region)).astype(int)
    bg = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
    d = np.abs(a - bg).sum(axis=2)
    ys, xs = np.where(d > thresh)
    if len(xs) == 0:
        return None, bg
    x0, y0 = region[0], region[1]
    # darkest ink colour = text colour
    idx = d[ys, xs].argmax()
    col = tuple(int(v) for v in a[ys[idx], xs[idx]])
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1), tuple(int(v) for v in bg), col


def text_box(text, size, face):
    f = ImageFont.truetype(TTC, size, index=FACE[face])
    im = Image.new('L', (size * len(text) * 2, size * 3), 0)
    ImageDraw.Draw(im).text((size, size), text, font=f, fill=255)
    bb = im.getbbox()
    return bb[2] - bb[0], bb[3] - bb[1], f, bb


def calibrate(ref_w, ref_h, ref_text, face):
    """font size whose ink width matches the reference label."""
    best = None
    for s in range(10, 80):
        w, h, _, _ = text_box(ref_text, s, face)
        err = abs(w - ref_w) + abs(h - ref_h)
        if best is None or err < best[0]:
            best = (err, s)
    return best[1]


def repaint(im, box, bg, col, text, size, face, pad=3, align='center'):
    d = ImageDraw.Draw(im)
    d.rectangle([box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad], fill=bg)
    w, h, f, bb = text_box(text, size, face)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    x = (box[0] - bb[0] + size) if align == 'left' else cx - w / 2 - bb[0] + size
    # keep the same ink top as the old label so baselines line up
    y = box[1] - bb[1] + size
    d.text((x, y), text, font=f, fill=col)
