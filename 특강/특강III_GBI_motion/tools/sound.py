"""모던 빌드업 배경음 합성 — 장면 타이밍(src/data/<EP>.timing.json)에 맞춘 사운드 베드.

장면마다: 패드 → (+아르페지오) → (+서브 킥) → (+하이햇)이 차례로 쌓여 긴장이 오르고,
장면 끝 1.6초는 라이저(노이즈 스윕 + 상승음), 직전 0.2초 정적, 다음 장면 첫 박에 임팩트.
자막 문장이 시작될 때마다 작은 UI 블립. 나레이션이 있으면 문장 구간에서 음악을 덕킹한다.

사용: python3 tools/sound.py M7E03   → public/audio/<EP>_bed.mp3 (ffmpeg 없으면 .wav)
numpy만 사용. 외부 음원 없음(전부 합성) — 저작권 걱정 없음."""
import json, math, pathlib, subprocess, sys, wave
import numpy as np

SR = 44100
BPM = 100
BEAT = 60 / BPM
ROOT = pathlib.Path(__file__).resolve().parents[1]
rng = np.random.default_rng(7)

# A minor 계열 진행 (Am – F – C – G), 2마디씩
CHORDS = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
BASS = [45, 41, 48, 43]
hz = lambda n: 440.0 * 2 ** ((n - 69) / 12)


def env_adsr(n, a, d, s, r):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    e = np.full(n, s, dtype=np.float32)
    if a: e[:a] = np.linspace(0, 1, a)
    if d: e[a:a + d] = np.linspace(1, s, min(d, max(0, n - a)))[: max(0, min(d, n - a))]
    if r and n > r: e[-r:] *= np.linspace(1, 0, r)
    return e


def lowpass(x, cutoff):
    """FFT 기반 부드러운 로우패스."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)


def highpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (cutoff / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)


def add(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def saw_pad(freq, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t, dtype=np.float32)
    for det in (-0.12, 0.0, 0.11):          # 디튠 3겹
        f0 = freq * 2 ** (det / 12)
        for k in range(1, 9):               # 대역 제한 톱니
            s += (np.sin(2 * np.pi * f0 * k * t + det * 7) / k).astype(np.float32)
    return s * env_adsr(len(t), 0.6, 0.4, 0.8, 0.8) / 9


def pluck(freq, dur=0.32):
    t = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2 * t) + 0.15 * np.sin(2 * np.pi * freq * 3 * t)
    return (s * np.exp(-t * 11)).astype(np.float32)


def kick(dur=0.45):
    t = np.arange(int(dur * SR)) / SR
    f = 42 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 7)).astype(np.float32)


def hat(dur=0.06):
    n = int(dur * SR)
    s = highpass(rng.standard_normal(n).astype(np.float32), 7000)
    return s * np.exp(-np.arange(n) / SR * 60)


def blip():
    t = np.arange(int(0.09 * SR)) / SR
    return (np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 45) + 0.5 * np.sin(2 * np.pi * 2640 * t) * np.exp(-t * 60)).astype(np.float32)


def riser(dur=1.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    # 시간에 따라 열리는 필터: 구간별 하이패스 컷을 올린다
    out = np.zeros(n, dtype=np.float32)
    seg = n // 8
    for k in range(8):
        a, b = k * seg, (k + 1) * seg if k < 7 else n
        out[a:b] = highpass(noise[a:b], 400 + k * 900)
    f = 220 * 2 ** (t / dur * 2)                     # 2옥타브 상승
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR).astype(np.float32)
    amp = (t / dur) ** 2
    return (0.55 * out + 0.25 * tone) * amp


def impact(dur=2.2):
    t = np.arange(int(dur * SR)) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 9)) / SR) * np.exp(-t * 2.2)
    n = rng.standard_normal(len(t)).astype(np.float32)
    crash = lowpass(n, 6000) * np.exp(-t * 3.5) * 0.35
    return (boom * 0.9 + crash).astype(np.float32)


def reverb(x, sec=1.8, mix=0.25):
    n = int(sec * SR)
    ir = rng.standard_normal(n).astype(np.float32) * np.exp(-np.arange(n) / SR * 3.2)
    ir = lowpass(ir, 5000); ir /= np.sqrt((ir**2).sum())
    L = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[: len(x)].astype(np.float32)
    return x * (1 - mix) + y * mix


def build(ep):
    T = json.load(open(ROOT / f"src/data/{ep}.timing.json"))
    fps = T["fps"]; total = T["total"] / fps + 2.5
    N = int(total * SR)
    pad = np.zeros(N, np.float32); arp = np.zeros(N, np.float32); drm = np.zeros(N, np.float32)
    fx = np.zeros(N, np.float32); bas = np.zeros(N, np.float32)
    duck = np.ones(N, np.float32)
    bar = 4 * BEAT
    for si, sc in enumerate(T["scenes"]):
        s0 = sc["from_"] / fps; D = sc["dur"] / fps; s1 = s0 + D
        last = si == len(T["scenes"]) - 1
        # 패드 · 베이스 — 2마디마다 코드 변경
        t = s0
        while t < s1 - 0.05:
            ci = int(t / (2 * bar)) % 4
            seg = min(2 * bar, s1 - t)
            for n_ in CHORDS[ci]:
                add(pad, saw_pad(hz(n_), seg + 0.6), t)
            # 베이스 펄스: 장면 30%부터 8분음표
            k = 0
            while k * BEAT / 2 < seg:
                tt = t + k * BEAT / 2
                if (tt - s0) / D > 0.3 and tt < s1 - 0.25:
                    b = pluck(hz(BASS[ci]), 0.25) * 0.9
                    add(bas, b, tt)
                k += 1
            t += seg
        # 아르페지오 16분 — 장면 15%부터, 점점 커짐
        k = 0
        while s0 + k * BEAT / 4 < s1 - 0.25:
            tt = s0 + k * BEAT / 4; r = (tt - s0) / D
            if r > 0.15:
                ci = int(tt / (2 * bar)) % 4
                notes = CHORDS[ci] + [CHORDS[ci][0] + 12]
                add(arp, pluck(hz(notes[k % 4] + 12)) * (0.25 + 0.75 * min(1, (r - 0.15) / 0.6)), tt)
            k += 1
        # 킥(4분) 35%부터 · 하이햇(8분) 55%부터
        k = 0
        while s0 + k * BEAT / 2 < s1 - 0.25:
            tt = s0 + k * BEAT / 2; r = (tt - s0) / D
            if r > 0.35 and k % 2 == 0: add(drm, kick() * 0.9, tt)
            if r > 0.55: add(drm, hat() * (0.35 if k % 2 else 0.2), tt)
            k += 1
        # 장면 끝 라이저 → 임팩트
        if not last and D > 4:
            add(fx, riser(1.6) * 0.8, s1 - 1.6)
            add(fx, impact() * 0.9, s1)
        # 문장 시작 블립 · 나레이션 덕킹
        for ln in sc["lines"]:
            lt = s0 + ln["start"] / fps
            add(fx, blip() * 0.18, lt)
            if ln.get("audio"):
                a = int(lt * SR); b = int((lt + ln["dur"] / fps) * SR)
                duck[a:b] = 0.4
    # 첫 장면 임팩트 · 끝 페이드
    add(fx, impact() * 0.9, 0.0)
    # 장면 경계 직전 0.2초 정적 (드롭 전 숨 고르기)
    for sc in T["scenes"][:-1]:
        b = (sc["from_"] + sc["dur"]) / fps
        i, j = int((b - 0.2) * SR), int(b * SR)
        for layer in (arp, drm, bas):
            layer[i:j] *= np.linspace(1, 0, j - i)
    # 덕킹 부드럽게 (50ms)
    kk = int(0.05 * SR); duck = np.convolve(duck, np.ones(kk) / kk, mode="same").astype(np.float32)
    music = reverb(lowpass(pad, 2500) * 0.30 + bas * 0.42, 2.2, 0.22) + reverb(arp * 0.16, 1.4, 0.35) + drm * 0.5
    mix = highpass(music * duck + reverb(fx, 1.6, 0.2) * 0.8, 32)
    # 끝 2초 페이드아웃
    f2 = int(2.0 * SR); mix[-f2:] *= np.linspace(1, 0, f2)
    # 정규화 + 소프트 리미터
    mix = np.tanh(mix / (np.percentile(np.abs(mix), 99.5) + 1e-9) * 0.9) * 0.7
    st = np.stack([mix, np.roll(mix, int(0.012 * SR)) * 0.97], 1)   # 살짝 넓힌 스테레오
    out = ROOT / "public/audio"; out.mkdir(parents=True, exist_ok=True)
    wav = out / f"{ep}_bed.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
    mp3 = out / f"{ep}_bed.mp3"
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-b:a", "192k", str(mp3)], check=True)
        wav.unlink(); name = mp3.name
    except Exception:
        name = wav.name
    T["bed"] = f"audio/{name}"
    json.dump(T, open(ROOT / f"src/data/{ep}.timing.json", "w"), ensure_ascii=False, indent=1)
    print(ep, "bed →", name, f"{total:.1f}s")


if __name__ == "__main__":
    for ep in sys.argv[1:]:
        build(ep)
