#!/bin/sh
# pptx → pdf → 50dpi PNG → 3×3 콘택트 시트 (sheets/sheet-N.png)
cd "$(dirname "$0")"
soffice --headless --convert-to pdf DMSS_Mental_Accounts_zeroone.pptx --outdir . >/dev/null 2>&1
rm -rf rp && mkdir rp sheets 2>/dev/null; mkdir -p rp sheets
pdftoppm -r 50 -png DMSS_Mental_Accounts_zeroone.pdf rp/p
/private/tmp/claude-501/-Users-keerhee-Project/43976b5b-172f-482e-9ca0-d96d85d71590/scratchpad/wt/bin/python - <<'PY'
from PIL import Image
import glob
fs=sorted(glob.glob("rp/p-*.png"))
w,h=Image.open(fs[0]).size
for k in range(0,len(fs),9):
    S=Image.new("RGB",(w*3+20,h*3+20),"black")
    for i,f in enumerate(fs[k:k+9]):
        S.paste(Image.open(f),((i%3)*(w+10),(i//3)*(h+10)))
    S.save(f"sheets/sheet-{k//9+1}.png")
print(len(fs),w,h)
PY
