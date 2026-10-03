"""EP.01 'J-커브는 정상입니다' — 9:16 웹툰 숏폼 렌더러 (SVG 프레임 → ffmpeg).
컷 구성은 ../episodes/ep01/script.json 과 같다. 패널 아트는 SVG 직접 작화(backend=svg).
"""
import math, subprocess, wave, struct, json, os
import numpy as np, cairosvg

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")
os.makedirs(OUT, exist_ok=True)
FONT = "Noto Sans CJK KR"
NAVY, ORANGE, YELLOW, CREAM, RED = "#1B2A4A", "#F05A28", "#F6B22B", "#F4E9DC", "#D7263D"

CUTS = [  # (start, end)
    (0, 4), (4, 10), (10, 15), (15, 23), (23, 28), (28, 32)]
DUR = CUTS[-1][1]

# ---------- easing ----------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def back(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def prog(t, a, d): return clamp((t - a) / d)

# ---------- primitives ----------
DEFS = f'''<defs>
<pattern id="dots" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="4.5" fill="#000" opacity=".10"/></pattern>
<pattern id="dotsW" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="4" fill="#fff" opacity=".10"/></pattern>
</defs>'''

def bg(color, pat="dots"):
    return f'<rect width="{W}" height="{H}" fill="{color}"/><rect width="{W}" height="{H}" fill="url(#{pat})"/>'

def burst(cx, cy, t, n=18, colors=(ORANGE, NAVY)):
    s = []
    rot = t * 6
    for i in range(n):
        a0 = math.radians(rot + i * 360 / n)
        a1 = a0 + math.radians(4 + (i % 3) * 2)
        R = 1600
        pts = f"{cx},{cy} {cx+R*math.cos(a0):.0f},{cy+R*math.sin(a0):.0f} {cx+R*math.cos(a1):.0f},{cy+R*math.sin(a1):.0f}"
        s.append(f'<polygon points="{pts}" fill="{colors[i%2]}" opacity="{0.85 if i%2 else 0.9}"/>')
    # 중앙을 비워 '방사선' 느낌
    s.append(f'<circle cx="{cx}" cy="{cy}" r="430" fill="{YELLOW}"/><circle cx="{cx}" cy="{cy}" r="430" fill="url(#dots)"/>')
    return "".join(s)

def punch(text, x, y, size, fill=ORANGE, stroke=NAVY, scale=1.0, rot=0, sw=None):
    sw = sw or size * 0.16
    t = (f'font-family="{FONT}" font-weight="900" font-size="{size}" text-anchor="middle" dominant-baseline="central"')
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">'
            f'<text x="10" y="12" {t} fill="{stroke}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{text}</text>'
            f'<text x="0" y="0" {t} fill="{stroke}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{text}</text>'
            f'<text x="0" y="0" {t} fill="{fill}">{text}</text></g>')

def label(text, x, y, size, fill=NAVY, weight=700, anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" dominant-baseline="central" fill="{fill}">{text}</text>')

def bubble(lines, x, y, w, h, tail=(0, 1), scale=1.0, size=52, fill="#fff"):
    """x,y = 말풍선 중심. tail = 꼬리 방향 (dx,dy) 단위."""
    tx, ty = tail
    bx, by = tx * w * 0.25, ty * h / 2 - 6
    tail_pts = f"{bx-34},{by} {bx+34},{by} {bx + tx*60 + 10},{by + ty*90}"
    body = (f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{h/2.2}" fill="{fill}" stroke="{NAVY}" stroke-width="8"/>'
            f'<polygon points="{tail_pts}" fill="{fill}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="{bx-30}" y="{by-14}" width="60" height="18" fill="{fill}"/>')
    n = len(lines); lh = size * 1.35
    txt = "".join(label(l, 0, (i - (n - 1) / 2) * lh, size, NAVY, 800) for i, l in enumerate(lines))
    return f'<g transform="translate({x},{y}) scale({scale})">{body}{txt}</g>'

# ---------- characters (오리지널: 부엉이 CIO '부장님', 펭귄 신입 '펭') ----------
def owl(x, y, s=1.0, blink=False, point=False, smile=True):
    eye = (lambda ex: f'<line x1="{ex-28}" y1="-60" x2="{ex+28}" y2="-60" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>') if blink else \
          (lambda ex: f'<circle cx="{ex}" cy="-60" r="50" fill="#fff"/><circle cx="{ex+6}" cy="-56" r="22" fill="{NAVY}"/><circle cx="{ex+12}" cy="-64" r="7" fill="#fff"/>')
    wingR = ('<ellipse cx="185" cy="-20" rx="45" ry="105" fill="#7A4E2D" stroke="#1B2A4A" stroke-width="8" transform="rotate(-55 150 30)"/>'
             if point else '<ellipse cx="160" cy="40" rx="45" ry="110" fill="#7A4E2D" stroke="#1B2A4A" stroke-width="8" transform="rotate(-12 160 40)"/>')
    mouth = ('<path d="M -22 40 Q 0 58 22 40" stroke="#1B2A4A" stroke-width="7" fill="none" stroke-linecap="round"/>' if smile else "")
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="250" rx="190" ry="26" fill="#000" opacity=".15"/>
<polygon points="-140,-150 -100,-275 -45,-190" fill="#7A4E2D" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>
<polygon points="140,-150 100,-275 45,-190" fill="#7A4E2D" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>
<ellipse cx="0" cy="20" rx="175" ry="225" fill="#9A6A43" stroke="{NAVY}" stroke-width="9"/>
<ellipse cx="0" cy="85" rx="112" ry="140" fill="#F3E3C3"/>
<path d="M -60 60 q 15 14 30 0 M 0 60 q 15 14 30 0 M -30 100 q 15 14 30 0 M 30 100 q 15 14 30 0" stroke="#C9A97A" stroke-width="5" fill="none"/>
<ellipse cx="-160" cy="40" rx="45" ry="110" fill="#7A4E2D" stroke="{NAVY}" stroke-width="8" transform="rotate(12 -160 40)"/>
{wingR}
{eye(-62)}{eye(62)}
<circle cx="-62" cy="-60" r="62" fill="none" stroke="{NAVY}" stroke-width="10"/>
<circle cx="62" cy="-60" r="62" fill="none" stroke="{NAVY}" stroke-width="10"/>
<line x1="-2" y1="-62" x2="2" y2="-62" stroke="{NAVY}" stroke-width="10"/>
<polygon points="-20,-8 20,-8 0,26" fill="#F2A33A" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/>
{mouth}
<path d="M -60 240 l -20 22 M -60 240 l 0 26 M -60 240 l 20 22 M 60 240 l -20 22 M 60 240 l 0 26 M 60 240 l 20 22" stroke="#F2A33A" stroke-width="12" stroke-linecap="round"/>
</g>'''

def penguin(x, y, s=1.0, mood="worry", sweat=0.0, flap=0.0):
    brow = {"worry": '<path d="M -80 -95 L -30 -80 M 80 -95 L 30 -80" stroke="#fff" stroke-width="9" stroke-linecap="round"/>',
            "happy": "", "shock": ""}[mood]
    if mood == "happy":
        eyes = ('<path d="M -78 -48 Q -55 -75 -32 -48" stroke="#1B2A4A" stroke-width="10" fill="none" stroke-linecap="round"/>'
                '<path d="M 32 -48 Q 55 -75 78 -48" stroke="#1B2A4A" stroke-width="10" fill="none" stroke-linecap="round"/>')
        mouth = '<path d="M -26 22 Q 0 52 26 22 Z" fill="#D7263D" stroke="#1B2A4A" stroke-width="5"/>'
    else:
        r = 30 if mood == "shock" else 24
        eyes = (f'<circle cx="-55" cy="-48" r="{r+12}" fill="#fff" stroke="#1B2A4A" stroke-width="5"/><circle cx="-52" cy="-44" r="{r-6}" fill="{NAVY}"/>'
                f'<circle cx="55" cy="-48" r="{r+12}" fill="#fff" stroke="#1B2A4A" stroke-width="5"/><circle cx="52" cy="-44" r="{r-6}" fill="{NAVY}"/>')
        mouth = '<ellipse cx="0" cy="34" rx="16" ry="20" fill="#1B2A4A"/>' if mood == "shock" else \
                '<path d="M -22 36 Q 0 22 22 36" stroke="#1B2A4A" stroke-width="7" fill="none" stroke-linecap="round"/>'
    fa = 25 * math.sin(flap * math.pi * 6) if flap else 0
    sw = ""
    if sweat > 0:
        sw = f'<path d="M 140 -150 q 22 40 0 58 q -22 -18 0 -58 z" fill="#5AB4E8" opacity="{sweat}"/>'
    return f'''<g transform="translate({x},{y}) scale({s})">
<ellipse cx="0" cy="250" rx="170" ry="24" fill="#000" opacity=".15"/>
<ellipse cx="0" cy="10" rx="160" ry="235" fill="#24407A" stroke="{NAVY}" stroke-width="9"/>
<ellipse cx="0" cy="60" rx="110" ry="175" fill="#FFFFFF"/>
<ellipse cx="0" cy="-60" rx="125" ry="95" fill="#FFFFFF"/>
<g transform="rotate({-fa} -150 0)"><ellipse cx="-165" cy="40" rx="38" ry="115" fill="#24407A" stroke="{NAVY}" stroke-width="8" transform="rotate(18 -165 40)"/></g>
<g transform="rotate({fa} 150 0)"><ellipse cx="165" cy="40" rx="38" ry="115" fill="#24407A" stroke="{NAVY}" stroke-width="8" transform="rotate(-18 165 40)"/></g>
{brow}{eyes}
<polygon points="-26,-8 26,-8 0,18" fill="#F2A33A" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>
{mouth}
<polygon points="-30,118 30,118 0,140" fill="{RED}" stroke="{NAVY}" stroke-width="5"/>
<polygon points="0,135 -22,215 0,235 22,215" fill="{RED}" stroke="{NAVY}" stroke-width="5"/>
<ellipse cx="-60" cy="245" rx="55" ry="20" fill="#F2A33A" stroke="{NAVY}" stroke-width="6"/>
<ellipse cx="60" cy="245" rx="55" ry="20" fill="#F2A33A" stroke="{NAVY}" stroke-width="6"/>
{sw}</g>'''

def panel_frame(x, y, w, h, inner, fill=CREAM, scale=1.0, rot=0):
    cx, cy = x + w / 2, y + h / 2
    return (f'<g transform="translate({cx},{cy}) rotate({rot}) scale({scale}) translate({-cx},{-cy})">'
            f'<rect x="{x+16}" y="{y+16}" width="{w}" height="{h}" fill="{NAVY}"/>'
            f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>{inner}</svg>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{NAVY}" stroke-width="12"/></g>')

def jcurve(t):  # 누적 순수익(%) — 연차 t(0~10)
    if t <= 4: return -12 * math.sin(math.pi * t / 4)
    return min(60, 5.5 * (t - 4) ** 1.35)

# ---------- cuts ----------
def cut1(t):  # 타이틀
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, 0.1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="170" y="1360" width="740" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.01 · J-커브는 정상입니다", 540, 1425, 54, "#fff", 800) + '</g>')
    p = ease_out(prog(t, 1.8, .7))
    s.append(penguin(300, 1720 + (1 - p) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):  # 펭: 첫해 -8%
    s = [bg("#FBE3CF")]
    s.append(punch("투자위원회 D-day", 540, 170, 96, fill=ORANGE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="330" width="920" height="1150" fill="#2B3A5C"/>',
             '<rect x="80" y="330" width="920" height="1150" fill="url(#dotsW)"/>',
             # 모니터
             '<rect x="150" y="410" width="780" height="470" rx="18" fill="#fff" stroke="#1B2A4A" stroke-width="10"/>',
             label("PE 펀드 1년차 수익률", 540, 470, 46, NAVY, 800)]
    pd = prog(t, .6, 1.4)
    pts = [(220 + i * 70, 560 + (i * 32 if i < 9 else 288) * 0.95) for i in range(10)]
    k = max(2, int(2 + pd * 8))
    path = " ".join(f"{'M' if i == 0 else 'L'} {x:.0f} {y:.0f}" for i, (x, y) in enumerate(pts[:k]))
    inner.append(f'<path d="{path}" stroke="{RED}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if pd >= 1:
        sc = back(prog(t, 2.0, .4))
        inner.append(punch("-8%", 790, 610, 130, fill=RED, stroke=NAVY, scale=sc, rot=-8))
    inner.append(penguin(560, 1200, .95, "shock" if t > 2.2 else "worry", sweat=prog(t, 2.4, .5), flap=prog(t, 2.2, .8) if t < 3 else 0))
    s.append(panel_frame(80, 330, 920, 1150, "".join(inner), scale=back(prog(t, 0.05, .45))))
    b = back(prog(t, 3.0, .45))
    s.append(bubble(["부장님… 첫해 수익률이", "−8%예요… 망했어요 ㅠㅠ"], 540, 1700, 900, 230, tail=(-0.3, -1), scale=b, size=56))
    return s

def cut3(t):  # 부엉이: J-커브, 정상
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 2.4))
    b = back(prog(t, .7, .45))
    s.append(bubble(["침착해. 그건 J-커브야.", "PE 첫 몇 해는 원래 마이너스지."], 540, 330, 960, 250, tail=(0, 1), scale=b, size=54))
    if t > 2.4:
        s.append(punch("정상!", 540, 1650, 230, fill=YELLOW, scale=back(prog(t, 2.4, .45)), rot=-6))
    return s

def cut4(t):  # J-커브 해설
    s = [bg(CREAM)]
    s.append(punch("J-커브란?", 540, 160, 120, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t,.3,.5))}">' +
             label("Private Equity 펀드의 누적 순수익 경로", 540, 290, 46, NAVY, 700) + "</g>")
    X0, X1, Y0 = 130, 990, 980   # Y0 = 0% 기준선
    ys = lambda v: Y0 - v * 9.0
    xs = lambda yr: X0 + (X1 - X0) * yr / 10
    s.append(f'<rect x="70" y="380" width="960" height="1030" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{NAVY}" stroke-width="6"/>')
    s.append(f'<line x1="{X0}" y1="420" x2="{X0}" y2="1300" stroke="{NAVY}" stroke-width="6"/>')
    for yr in range(0, 11, 2):
        s.append(label(str(yr), xs(yr), 1340, 36, "#555", 700))
    s.append(label("연차", X1 - 10, 1385, 34, "#555", 700, "end"))
    s.append(label("0%", X0 - 18, Y0, 34, "#555", 700, "end"))
    s.append(f'<rect x="{X0}" y="{Y0}" width="{xs(4)-X0}" height="{ys(-14)-Y0}" fill="{RED}" opacity=".08"/>')
    pd = prog(t, .8, 4.2)
    N = 120; end = max(2, int(N * pd))
    pts = [(xs(10 * i / N), ys(jcurve(10 * i / N))) for i in range(end + 1)]
    d = " ".join(f"{'M' if i == 0 else 'L'} {x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    s.append(f'<path d="{d}" stroke="{ORANGE}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    hx, hy = pts[-1]; s.append(f'<circle cx="{hx}" cy="{hy}" r="18" fill="{NAVY}"/>')
    notes = [(1.5, "① 관리보수·초기비용", xs(2.0), ys(-12) + 95, RED),
             (3.0, "② 가치 창출", 430, 760, NAVY),
             (4.6, "③ 회수 (Exit)", 680, 470, "#1E7F4F")]
    for a, txt, x, y, c in notes:
        sc = back(prog(t, a, .4))
        if sc > 0:
            s.append(f'<g transform="translate({x},{y}) scale({sc})"><rect x="-190" y="-42" width="380" height="84" rx="20" fill="{c}"/>'
                     + label(txt, 0, 0, 40, "#fff", 800) + "</g>")
    s.append(owl(190, 1690, .5, point=True, blink=(5.6 < t < 5.75)))
    b = back(prog(t, 5.2, .45))
    s.append(bubble(["IRR은 펀드 만기까지", "보고 판단하는 거야."], 640, 1600, 720, 220, tail=(-1.6, 1), scale=b, size=50))
    return s

def cut5(t):  # 펭 안도
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1150, .9, "happy" if t > 2.4 else "worry", flap=prog(t, 2.4, 1.2))
    inner += owl(780, 1180, .78, blink=(1.2 < t < 1.35))
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 회복은 언제쯤…?"], 380, 330, 640, 150, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["보통 4~5년차부터.", "조급하면 지는 게임이야."], 560, 1720, 840, 230, tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=52))
    if t > 2.6:
        s.append(punch("휴~", 230, 760, 120, fill="#fff", scale=back(prog(t, 2.6, .4)), rot=-10))
    return s

def cut6(t):  # 다음 화 예고
    s = [bg(ORANGE)]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    shake = 10 * math.sin(t * 50) * (1 - prog(t, .9, .8)) if t > .5 else 0
    s.append(punch("캐피털 콜", 540 + shake, 860, 190, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch("폭탄!", 540 - shake, 1110, 230, fill=YELLOW, scale=back(prog(t, .8, .45)), rot=3))
    s.append(penguin(540, 1600 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "shock", sweat=1.0))
    s.append(f'<g opacity="{ease_out(prog(t, 2.4, .6))}">' + label("Capital Call · 약정액 인출 요청", 540, 1340, 46, "#fff", 800) + "</g>")
    return s

FUNCS = [cut1, cut2, cut3, cut4, cut5, cut6]

def frame_svg(T):
    for i, (a, b) in enumerate(CUTS):
        if a <= T < b or (i == len(CUTS) - 1 and T >= a):
            t = T - a
            body = "".join(FUNCS[i](t))
            # 컷 전환: 앞 0.18초 흰 플래시
            fl = 1 - prog(t, 0, .18) if i > 0 else 0
            if fl > 0: body += f'<rect width="{W}" height="{H}" fill="#fff" opacity="{fl:.2f}"/>'
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{DEFS}{body}</svg>'

# ---------- audio: 코드 진행 패드 + 컷 전환 팝 ----------
def make_audio(path, sr=44100):
    n = int(DUR * sr); tt = np.arange(n) / sr; y = np.zeros(n)
    chords = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    for k in range(int(DUR // 2) + 1):
        a, b = k * 2 * sr, min(n, (k + 1) * 2 * sr)
        if a >= n: break
        seg = tt[a:b] - k * 2
        env = np.minimum(1, seg / .05) * np.exp(-seg * 1.1)
        for f in chords[k % 4]:
            y[a:b] += .06 * env * (np.sin(2 * np.pi * f * seg) + .3 * np.sin(4 * np.pi * f * seg))
        # 8분음 하이햇 느낌
        for j in range(4):
            h0 = a + int(j * .5 * sr); h1 = min(n, h0 + int(.04 * sr))
            if h0 < n: y[h0:h1] += .05 * np.random.randn(h1 - h0) * np.linspace(1, 0, h1 - h0)
    for a, _ in CUTS:
        p0 = int(a * sr); L = int(.18 * sr); s = np.arange(L) / sr
        y[p0:p0 + L] += .35 * np.sin(2 * np.pi * (900 - 2500 * s) * s) * np.exp(-s * 25)
    y = np.clip(y / max(1e-9, np.abs(y).max()) * .8, -1, 1)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((y * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stills":   # 검수용 정지 컷
        for i, T in enumerate([2.5, 7.0, 13.2, 21.5, 27.0, 30.8]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/still_{i+1}.png")
        sys.exit()
    wav = f"{OUT}/bgm.wav"; make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep01.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(DUR * FPS):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait()
    print("done", mp4)
