#!/bin/sh
# pptx → pdf → 50dpi PNG → 3×3 contact sheets (src/sheet-N.png)
cd "$(dirname "$0")"
soffice --headless --convert-to pdf LDI_Summary_Basics_zeroone.pptx --outdir . >/dev/null 2>&1
rm -rf rp && mkdir rp && pdftoppm -r 50 -png LDI_Summary_Basics_zeroone.pdf rp/p
../wt/bin/python - <<'PY'
from PIL import Image, ImageDraw
import glob
fs=sorted(glob.glob("rp/p-*.png"))
w,h=Image.open(fs[0]).size
for k in range(0,len(fs),9):
    S=Image.new("RGB",(w*3+20,h*3+20),"black")
    for i,f in enumerate(fs[k:k+9]):
        S.paste(Image.open(f),((i%3)*(w+10),(i//3)*(h+10)))
    S.save(f"src/sheet-{k//9+1}.png")
print(len(fs),w,h)
PY
