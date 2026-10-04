"""python sheet.py NN → 정지 컷 렌더 + 콘택트 시트(scratchpad)."""
import sys, subprocess, os
from PIL import Image
ep = sys.argv[1]; S = os.environ.get('SHEET_DIR', '/private/tmp/claude-501/-Users-keerhee-Project/43976b5b-172f-482e-9ca0-d96d85d71590/scratchpad/w01sheets/'); os.makedirs(S, exist_ok=True)
subprocess.run([sys.executable, f'render_ep{ep}.py', 'stills'], check=True)
ims = [Image.open(f'../output/ic_webtoon_w01_ep{ep}_still_{i}.png').resize((360, 640)) for i in range(1, 7)]
c = Image.new('RGB', (360 * 6, 640), 'white')
for i, im in enumerate(ims): c.paste(im, (360 * i, 0))
c.save(S + f'w01_{ep}_sheet.png')
Image.open(f'../output/ic_webtoon_w01_ep{ep}_still_4.png').resize((540, 960)).save(S + f'w01_{ep}_c4.png')
