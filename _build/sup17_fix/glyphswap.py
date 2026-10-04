"""그림 PNG(표) 안의 한 낱말(예: '돈')을 다른 낱말로 바꾼다 — 같은 칸에서 낱말 뒤 글자는 늘어난 폭만큼 오른쪽으로 민다.
swap_word(im, x_hint, y_hint, new, bold=False, right_limit=None, old="돈") -> (im, info)
  x_hint, y_hint : 바꿀 낱말 첫 글자 근처의 한 점   right_limit : 그 칸의 오른쪽 끝(이 안의 글자만 민다)
글꼴은 Noto Sans CJK KR(표 그림의 글꼴). 크기는 옛 낱말의 잉크 높이에 맞춰 고른다."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
TTC = os.path.expanduser("~/Library/Fonts/NotoSansCJK.ttc"); REG, BOLD = 26, 36

def swap_word(im, x_hint, y_hint, new, bold=False, right_limit=None, old="돈"):
    a = np.array(im.convert("RGB")); H, W, _ = a.shape
    bg = tuple(int(v) for v in np.median(a[y_hint, :].reshape(-1, 3), axis=0))
    ink = np.abs(a.astype(int) - np.array(bg)).sum(2) > 60
    # 행 띠: 가로 구분선(폭의 절반 넘게 잉크이거나 배경색이 바뀌는 줄)까지
    full = (np.abs(a.astype(int) - np.array(bg)).sum(2) > 12).mean(1) > 0.5
    y0 = y_hint
    while y0 > 0 and not full[y0 - 1]: y0 -= 1
    y1 = y_hint
    while y1 < H - 1 and not full[y1 + 1]: y1 += 1
    rl = right_limit or W
    band = ink[y0:y1 + 1]
    colink = band.any(0)
    # 낱말 첫 잉크 열: x_hint 왼쪽으로 띄어쓰기 폭만큼 빈 열이 나올 때까지
    x = x_hint   # x_hint는 첫 글자 잉크 안쪽 — 이어진 잉크 열을 따라 왼쪽 끝까지
    while not colink[x]: x += 1
    while x > 0 and colink[x - 1]: x -= 1
    while not colink[x]: x += 1
    gx0 = x
    # 첫 음절의 잉크 높이로 글꼴 크기 추정 → 옛 낱말 폭은 글꼴에서 계산
    probe = band[:, gx0:gx0 + 12]
    r = probe.any(1).nonzero()[0]
    fidx = BOLD if bold else REG
    # 옛 낱말 전체 폭 후보 크기마다: 잉크 높이(그 열 범위) 일치도를 본다
    best = None
    for fs in range(10, 130):
        f = ImageFont.truetype(TTC, fs, index=fidx); bb = f.getbbox(old)
        w = bb[2] - bb[0]
        cols = band[:, gx0:gx0 + max(1, int(w * 0.8))]
        rr = cols.any(1).nonzero()[0]
        if len(rr) == 0: continue
        err = abs((rr[-1] - rr[0] + 1) - (bb[3] - bb[1])) + abs(w - (bb[2] - bb[0]))
        # 낱말 오른쪽 바로 다음 열이 비어 있는지(글자 경계)도 점수에 넣는다
        if best is None or err < best[0]: best = (err, fs, w, rr[0] + y0, rr[-1] + y0)
    _, fs, old_w, wy0, wy1 = best
    f = ImageFont.truetype(TTC, fs, index=fidx)
    gx1 = gx0 + old_w - 1
    nb = f.getbbox(new); new_w = nb[2] - nb[0]
    delta = new_w - old_w
    after = colink[gx1 + 1:rl].nonzero()[0]
    rest_end = gx1 + 1 + after[-1] if len(after) else gx1
    sub = a[wy0:wy1 + 1, gx0:gx1 + 1].reshape(-1, 3).astype(int)
    color = tuple(int(v) for v in sub[np.abs(sub - np.array(bg)).sum(1).argmax()])
    out = a.copy(); Y = slice(y0 + 1, y1)
    seg = a[Y, gx1 + 1:rest_end + 1].copy()
    out[Y, gx0:rest_end + 1 + max(0, delta)] = bg
    if rest_end > gx1: out[Y, gx1 + 1 + delta:rest_end + 1 + delta] = seg
    img = Image.fromarray(out); dr = ImageDraw.Draw(img)
    ob = f.getbbox(old)   # 옛 낱말의 잉크 아래끝으로 기준선을 맞춘다
    dr.text((gx0 - nb[0], wy1 - ob[3]), new, font=f, fill=color)
    if rest_end + delta >= rl: raise ValueError(f"칸을 넘친다: {rest_end + delta} ≥ {rl}")
    return img, dict(bg=bg, color=color, row=(y0, y1), word=(gx0, gx1), fs=fs, delta=delta, rest_end=rest_end)
