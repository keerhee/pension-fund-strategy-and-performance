import math, subprocess, wave, os, base64, sys
import numpy as np, cairosvg
from PIL import Image

W, H, FPS = 1080, 1920, 24
FONT = "Noto Sans CJK KR"
NAVY, ORANGE, YELLOW, CREAM, RED = "#1B2A4A", "#F05A28", "#F6B22B", "#F4E9DC", "#D7263D"
GREEN, GREY, GOLD, BLUE, TEAL = "#1E7F4F", "#8A94A6", "#9A6B00", "#2F6FB0", "#0B6B68"

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def back(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def prog(t, a, d): return clamp((t - a) / d)

DEFS = '''<defs>
<pattern id="dots" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="4.5" fill="#000" opacity=".10"/></pattern>
<pattern id="dotsW" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="4" fill="#fff" opacity=".10"/></pattern>
</defs>'''

def bg(color, pat="dots"):
    return f'<rect width="{W}" height="{H}" fill="{color}"/><rect width="{W}" height="{H}" fill="url(#{pat})"/>'

def burst(cx, cy, t, n=18, colors=(ORANGE, NAVY)):
    s = []
    for i in range(n):
        a0 = math.radians(t * 6 + i * 360 / n); a1 = a0 + math.radians(4 + (i % 3) * 2); R = 1600
        s.append(f'<polygon points="{cx},{cy} {cx+R*math.cos(a0):.0f},{cy+R*math.sin(a0):.0f} {cx+R*math.cos(a1):.0f},{cy+R*math.sin(a1):.0f}" fill="{colors[i%2]}" opacity=".88"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="430" fill="{YELLOW}"/><circle cx="{cx}" cy="{cy}" r="430" fill="url(#dots)"/>')
    return "".join(s)

def punch(text, x, y, size, fill=ORANGE, stroke=NAVY, scale=1.0, rot=0, sw=None):
    sw = sw or size * 0.16
    t = f'font-family="{FONT}" font-weight="900" font-size="{size}" text-anchor="middle" dominant-baseline="central"'
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">'
            f'<text x="10" y="12" {t} fill="{stroke}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{text}</text>'
            f'<text x="0" y="0" {t} fill="{stroke}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{text}</text>'
            f'<text x="0" y="0" {t} fill="{fill}">{text}</text></g>')

def label(text, x, y, size, fill=NAVY, weight=700, anchor="middle"):
    text = str(text).replace("&lt;", "<").replace("&amp;", "&").replace("&", "&amp;").replace("<", "&lt;")   # [시즌 3·4] < · & 자동 이스케이프
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" dominant-baseline="central" fill="{fill}">{text}</text>')

def bubble(lines, x, y, w, h, tail=(0, 1), scale=1.0, size=52, fill="#fff"):
    tx, ty = tail; bx, by = tx * w * 0.25, ty * h / 2 - 6
    body = (f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{h/2.2}" fill="{fill}" stroke="{NAVY}" stroke-width="8"/>'
            f'<polygon points="{bx-34},{by} {bx+34},{by} {bx+tx*60+10},{by+ty*90}" fill="{fill}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="{bx-30}" y="{by-14}" width="60" height="18" fill="{fill}"/>')
    n = len(lines); lh = size * 1.35
    txt = "".join(label(l, 0, (i - (n - 1) / 2) * lh, size, NAVY, 800) for i, l in enumerate(lines))
    return f'<g transform="translate({x},{y}) scale({scale})">{body}{txt}</g>'

def chip(txt, x, y, c, sc, w=420, size=40):
    if sc <= 0: return ""
    return (f'<g transform="translate({x},{y}) scale({sc})"><rect x="{-w/2}" y="-40" width="{w}" height="80" rx="20" fill="{c}"/>'
            + label(txt, 0, 0, size, "#fff", 900) + "</g>")

def panel_frame(x, y, w, h, inner, fill=CREAM, scale=1.0, rot=0):
    cx, cy = x + w / 2, y + h / 2
    return (f'<g transform="translate({cx},{cy}) rotate({rot}) scale({scale}) translate({-cx},{-cy})">'
            f'<rect x="{x+16}" y="{y+16}" width="{w}" height="{h}" fill="{NAVY}"/>'
            f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>{inner}</svg>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{NAVY}" stroke-width="12"/></g>')

def owl(x, y, s=1.0, blink=False, point=False):
    eye = (lambda ex: f'<line x1="{ex-28}" y1="-60" x2="{ex+28}" y2="-60" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>') if blink else \
          (lambda ex: f'<circle cx="{ex}" cy="-60" r="50" fill="#fff"/><circle cx="{ex+6}" cy="-56" r="22" fill="{NAVY}"/><circle cx="{ex+12}" cy="-64" r="7" fill="#fff"/>')
    wingR = ('<ellipse cx="185" cy="-20" rx="45" ry="105" fill="#7A4E2D" stroke="#1B2A4A" stroke-width="8" transform="rotate(-55 150 30)"/>' if point
             else '<ellipse cx="160" cy="40" rx="45" ry="110" fill="#7A4E2D" stroke="#1B2A4A" stroke-width="8" transform="rotate(-12 160 40)"/>')
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="250" rx="190" ry="26" fill="#000" opacity=".15"/>
<polygon points="-140,-150 -100,-275 -45,-190" fill="#7A4E2D" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>
<polygon points="140,-150 100,-275 45,-190" fill="#7A4E2D" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>
<ellipse cx="0" cy="20" rx="175" ry="225" fill="#9A6A43" stroke="{NAVY}" stroke-width="9"/>
<ellipse cx="0" cy="85" rx="112" ry="140" fill="#F3E3C3"/>
<path d="M -60 60 q 15 14 30 0 M 0 60 q 15 14 30 0 M -30 100 q 15 14 30 0 M 30 100 q 15 14 30 0" stroke="#C9A97A" stroke-width="5" fill="none"/>
<ellipse cx="-160" cy="40" rx="45" ry="110" fill="#7A4E2D" stroke="{NAVY}" stroke-width="8" transform="rotate(12 -160 40)"/>
{wingR}{eye(-62)}{eye(62)}
<circle cx="-62" cy="-60" r="62" fill="none" stroke="{NAVY}" stroke-width="10"/><circle cx="62" cy="-60" r="62" fill="none" stroke="{NAVY}" stroke-width="10"/>
<line x1="-2" y1="-62" x2="2" y2="-62" stroke="{NAVY}" stroke-width="10"/>
<polygon points="-20,-8 20,-8 0,26" fill="#F2A33A" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/>
<path d="M -22 40 Q 0 58 22 40" stroke="#1B2A4A" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M -60 240 l -20 22 M -60 240 l 0 26 M -60 240 l 20 22 M 60 240 l -20 22 M 60 240 l 0 26 M 60 240 l 20 22" stroke="#F2A33A" stroke-width="12" stroke-linecap="round"/>
</g>'''

def penguin(x, y, s=1.0, mood="worry", sweat=0.0, flap=0.0):
    """mood: worry | shock | happy"""
    brow = '<path d="M -80 -95 L -30 -80 M 80 -95 L 30 -80" stroke="#fff" stroke-width="9" stroke-linecap="round"/>' if mood == "worry" else ""
    if mood == "happy":
        eyes = ('<path d="M -78 -48 Q -55 -75 -32 -48" stroke="#1B2A4A" stroke-width="10" fill="none" stroke-linecap="round"/>'
                '<path d="M 32 -48 Q 55 -75 78 -48" stroke="#1B2A4A" stroke-width="10" fill="none" stroke-linecap="round"/>')
        mouth = '<path d="M -26 22 Q 0 52 26 22 Z" fill="#D7263D" stroke="#1B2A4A" stroke-width="5"/>'
    else:
        r = 30 if mood == "shock" else 24
        eyes = (f'<circle cx="-55" cy="-48" r="{r+12}" fill="#fff" stroke="#1B2A4A" stroke-width="5"/><circle cx="-52" cy="-44" r="{r-6}" fill="{NAVY}"/>'
                f'<circle cx="55" cy="-48" r="{r+12}" fill="#fff" stroke="#1B2A4A" stroke-width="5"/><circle cx="52" cy="-44" r="{r-6}" fill="{NAVY}"/>')
        mouth = ('<ellipse cx="0" cy="34" rx="16" ry="20" fill="#1B2A4A"/>' if mood == "shock"
                 else '<path d="M -22 36 Q 0 22 22 36" stroke="#1B2A4A" stroke-width="7" fill="none" stroke-linecap="round"/>')
    fa = 25 * math.sin(flap * math.pi * 6) if flap else 0
    sw = f'<path d="M 140 -150 q 22 40 0 58 q -22 -18 0 -58 z" fill="#5AB4E8" opacity="{sweat}"/>' if sweat > 0 else ""
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="250" rx="170" ry="24" fill="#000" opacity=".15"/>
<ellipse cx="0" cy="10" rx="160" ry="235" fill="#24407A" stroke="{NAVY}" stroke-width="9"/>
<ellipse cx="0" cy="60" rx="110" ry="175" fill="#FFFFFF"/><ellipse cx="0" cy="-60" rx="125" ry="95" fill="#FFFFFF"/>
<g transform="rotate({-fa} -150 0)"><ellipse cx="-165" cy="40" rx="38" ry="115" fill="#24407A" stroke="{NAVY}" stroke-width="8" transform="rotate(18 -165 40)"/></g>
<g transform="rotate({fa} 150 0)"><ellipse cx="165" cy="40" rx="38" ry="115" fill="#24407A" stroke="{NAVY}" stroke-width="8" transform="rotate(-18 165 40)"/></g>
{brow}{eyes}
<polygon points="-26,-8 26,-8 0,18" fill="#F2A33A" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>{mouth}
<polygon points="-30,118 30,118 0,140" fill="{RED}" stroke="{NAVY}" stroke-width="5"/>
<polygon points="0,135 -22,215 0,235 22,215" fill="{RED}" stroke="{NAVY}" stroke-width="5"/>
<ellipse cx="-60" cy="245" rx="55" ry="20" fill="#F2A33A" stroke="{NAVY}" stroke-width="6"/>
<ellipse cx="60" cy="245" rx="55" ry="20" fill="#F2A33A" stroke="{NAVY}" stroke-width="6"/>{sw}</g>'''

# ---------- 공통 컷: 타이틀 / 예고 ----------
def title_cut(t, ep_label, chip_w=780):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    a = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{a}" transform="translate(0,{(1-a)*60})"><rect x="{540-chip_w/2}" y="1360" width="{chip_w}" height="130" rx="26" fill="{NAVY}"/>'
             + label(ep_label, 540, 1425, 54, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def next_cut(t, color, topic, question, topic_size=220):
    s = [bg(color, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch(topic, 540, 860, topic_size, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label(question, 540, 1090, 54, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s

# ---------- LaTeX 수식 ----------
def _latex_png_mathtext(tex, path):
    """[로컬 패치] pdflatex가 없는 맥에서 matplotlib mathtext(Computer Modern)로 굽는다. 600dpi · 흰 배경 · 같은 색."""
    import re, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    s = tex.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\displaystyle", "")
    s = re.sub(r"\\(?:textrm|mbox)\{", r"\\text{", s)
    s = re.sub(r"\\[Bb]igg?[lr]?(?![a-zA-Z])", "", s)
    with plt.rc_context({"mathtext.fontset": "cm"}):
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, "$" + s + "$", fontsize=11, color="#1B2A4A")
        fig.savefig(path, dpi=600, bbox_inches="tight", pad_inches=4 / 72, facecolor="white")
        plt.close(fig)

def latex_png(tex, path):
    """tex: 디스플레이 수식 본문. 600dpi PNG 생성."""
    import shutil
    if shutil.which("pdflatex") is None:          # [로컬 패치] 이 맥에는 TeX가 없다
        return _latex_png_mathtext(tex, path)
    base = os.path.splitext(path)[0]
    open(base + ".tex", "w").write('\\documentclass[border=4pt]{standalone}\\usepackage{amsmath,xcolor}'
                                   '\\begin{document}\\color[HTML]{1B2A4A}$\\displaystyle ' + tex + '$\\end{document}')
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", os.path.dirname(path) or ".", base + ".tex"],
                   stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["pdftoppm", "-png", "-r", "600", "-singlefile", base + ".pdf", base], check=True)
    for ext in (".tex", ".aux", ".log", ".pdf"):
        if os.path.exists(base + ext): os.remove(base + ext)

def eq_img(path, x, y, a, scale=.5):
    w, h = Image.open(path).size; w, h = w * scale, h * scale
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})"><image x="{x-w/2:.0f}" y="{y:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" xlink:href="data:image/png;base64,{b64}"/></g>')

# ---------- 오디오 + 렌더 ----------
def make_audio(path, cuts, dur, sr=44100):
    n = int(dur * sr); tt = np.arange(n) / sr; y = np.zeros(n)
    chords = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    for k in range(int(dur // 2) + 1):
        a, b = k * 2 * sr, min(n, (k + 1) * 2 * sr)
        if a >= n: break
        seg = tt[a:b] - k * 2; env = np.minimum(1, seg / .05) * np.exp(-seg * 1.1)
        for f in chords[k % 4]:
            y[a:b] += .06 * env * (np.sin(2 * np.pi * f * seg) + .3 * np.sin(4 * np.pi * f * seg))
        for j in range(4):
            h0 = a + int(j * .5 * sr); h1 = min(n, h0 + int(.04 * sr))
            if h0 < n: y[h0:h1] += .05 * np.random.randn(h1 - h0) * np.linspace(1, 0, h1 - h0)
    for a, _ in cuts:
        p0 = int(a * sr); L = min(int(.18 * sr), n - p0); s = np.arange(L) / sr
        y[p0:p0 + L] += .35 * np.sin(2 * np.pi * (900 - 2500 * s) * s) * np.exp(-s * 25)
    y = np.clip(y / max(1e-9, np.abs(y).max()) * .8, -1, 1)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y * 32767).astype(np.int16).tobytes())

def frame_svg(T, funcs, cuts):
    for i, (a, b) in enumerate(cuts):
        if a <= T < b or (i == len(cuts) - 1 and T >= a):
            t = T - a; body = "".join(funcs[i](t))
            fl = 1 - prog(t, 0, .18) if i > 0 else 0          # 컷 전환 흰 플래시
            if fl > 0: body += f'<rect width="{W}" height="{H}" fill="#fff" opacity="{fl:.2f}"/>'
            return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                    f'width="{W}" height="{H}">{DEFS}{body}</svg>')

def run(funcs, cuts, dur, out_mp4, still_times):
    """python3 render_epNN.py stills → 정지 컷 PNG / 인자 없으면 MP4"""
    out_dir = os.path.dirname(out_mp4) or "."; os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(out_mp4))[0]
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for i, T in enumerate(still_times):
            cairosvg.svg2png(bytestring=frame_svg(T, funcs, cuts).encode(), write_to=f"{out_dir}/{stem}_still_{i+1}.png")
        return
    wav = f"{out_dir}/{stem}.wav"; make_audio(wav, cuts, dur)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    for f in range(int(dur * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS, funcs, cuts).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", out_mp4)
