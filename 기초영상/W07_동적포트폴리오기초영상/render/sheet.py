"""python sheet.py NN → 정지 컷 렌더 + 콘택트 시트(scratchpad)."""
import sys, subprocess, os
from PIL import Image
ep = sys.argv[1]; S = '/private/tmp/claude-501/-Users-keerhee-Project/45cf510c-41f3-413b-9e76-668085e86931/scratchpad/'
subprocess.run([sys.executable, f'render_ep{ep}.py', 'stills'], check=True)
ims = [Image.open(f'../output/ic_webtoon_s3_ep{ep}_still_{i}.png').resize((360, 640)) for i in range(1, 7)]
c = Image.new('RGB', (360 * 6, 640), 'white')
for i, im in enumerate(ims): c.paste(im, (360 * i, 0))
c.save(S + f's3_{ep}_sheet.png')
Image.open(f'../output/ic_webtoon_s3_ep{ep}_still_4.png').resize((540, 960)).save(S + f's3_{ep}_c4.png')
