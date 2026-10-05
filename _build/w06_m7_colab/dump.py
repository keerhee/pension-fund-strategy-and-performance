# usage: python dump.py 01_xxx.ipynb [img_dir] — 실행된 노트북의 출력 텍스트를 보이고 그림을 PNG로 뽑는다(검수용)
import json, sys, base64, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "W06_LDI와GBI", "W06_M7_실습_Colab")
f = sys.argv[1]; nb = json.load(open(os.path.join(OUT, f)))
d = sys.argv[2] if len(sys.argv) > 2 else "img_" + f[:2]; os.makedirs(d, exist_ok=True); k = 0
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code": continue
    for o in c.get("outputs", []):
        if o.get("output_type") == "stream": print(f"[{i}]", "".join(o["text"])[:3000])
        elif o.get("output_type") == "error": print(f"[{i}] ERROR", o["ename"], o["evalue"])
        elif "data" in o:
            if "image/png" in o["data"]:
                k += 1; p = f"{d}/c{i:02d}_{k}.png"; open(p, "wb").write(base64.b64decode(o["data"]["image/png"])); print(f"[{i}] image -> {p}")
            elif "text/plain" in o["data"]: print(f"[{i}]", "".join(o["data"]["text/plain"])[:500])
