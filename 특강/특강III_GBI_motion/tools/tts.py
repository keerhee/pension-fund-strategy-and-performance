"""edge-tts로 문장별 나레이션 mp3 생성. 사용: python3 tools/tts.py M7E03 [voice]"""
import asyncio, json, sys, pathlib
import edge_tts
ep = sys.argv[1]; voice = sys.argv[2] if len(sys.argv) > 2 else "ko-KR-SunHiNeural"
root = pathlib.Path(__file__).resolve().parents[1]
script = json.loads((root / f"script/{ep}.json").read_text())
out = root / f"public/audio/{ep}"; out.mkdir(parents=True, exist_ok=True)
async def main():
    for si, s in enumerate(script["scenes"]):
        for li, ln in enumerate(s["lines"]):
            f = out / f"s{si}_{li}.mp3"
            if f.exists() and f.stat().st_size > 0: continue
            await edge_tts.Communicate(ln["say"], voice, rate="+0%").save(str(f))
            print("tts", f.name)
asyncio.run(main())
