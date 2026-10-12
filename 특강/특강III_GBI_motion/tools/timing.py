"""문장별 길이(음성 파일이 있으면 실제 길이, 없으면 추정)로 장면 타이밍 JSON 생성."""
import json, sys, subprocess, pathlib
FPS = 30; HEAD, GAP, TAIL = 0.6, 0.45, 1.0
ep = sys.argv[1]
root = pathlib.Path(__file__).resolve().parents[1]
script = json.loads((root / f"script/{ep}.json").read_text())
adir = root / f"public/audio/{ep}"
def dur(f, text):
    if f.exists() and f.stat().st_size > 0:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
        return float(r.stdout.strip()), True
    return len(text.replace(" ", "")) / 6.2, False   # 추정: 초당 약 6.2자
scenes, t, has_audio = [], 0, True
for si, s in enumerate(script["scenes"]):
    lines, cur = [], HEAD
    for li, ln in enumerate(s["lines"]):
        d, real = dur(adir / f"s{si}_{li}.mp3", ln["say"]); has_audio &= real
        lines.append(dict(start=round(cur * FPS), dur=round(d * FPS), cap=ln["cap"],
                          audio=f"audio/{ep}/s{si}_{li}.mp3" if real else None))
        cur += d + GAP
    sd = round((cur - GAP + TAIL) * FPS)
    scenes.append(dict(id=s["id"], from_=t, dur=sd, lines=lines)); t += sd
json.dump(dict(fps=FPS, total=t, hasAudio=has_audio, scenes=scenes),
          open(root / f"src/data/{ep}.timing.json", "w"), ensure_ascii=False, indent=1)
print(f"{ep}: {t/FPS:.1f}s, audio={'real' if has_audio else 'estimated'}")
