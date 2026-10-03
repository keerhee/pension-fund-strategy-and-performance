"""EP.05 'Subscription Line의 비밀' — 9:16 웹툰 숏폼.
같은 딜(4년 뒤 160 회수)인데 신용한도로 LP 콜을 1년 늦추면 IRR은 오르고 MOIC는 내려간다."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)

GREEN, GREY, TEAL = "#1E7F4F", "#8A94A6", "#0B6B68"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10), (10, 16), (16, 29), (29, 36), (36, 39.5)]
DUR = 39.5

def _eq(name, s=.47):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep05_1"), _eq("ep05_2"), _eq("ep05_3")]

def eq_img(i, x, y, a):
    b64, w, h = EQS[i]
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})">'
            f'<image x="{x - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" xlink:href="data:image/png;base64,{b64}"/></g>')

def chip(txt, x, y, c, sc, w=420, size=40):
    if sc <= 0: return ""
    return (f'<g transform="translate({x},{y}) scale({sc})"><rect x="{-w/2}" y="-40" width="{w}" height="80" rx="20" fill="{c}"/>'
            + label(txt, 0, 0, size, "#fff", 900) + "</g>")

def report_card(x, y, title, irr, c, sc, x_off, note):
    return (f'<g transform="translate({x_off:.0f},0)"><g transform="translate({x},{y}) scale({sc})">'
            f'<rect x="-200" y="-230" width="400" height="460" rx="30" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
            f'<rect x="-200" y="-230" width="400" height="110" rx="30" fill="{c}"/><rect x="-200" y="-150" width="400" height="30" fill="{c}"/>'
            + label(title, 0, -175, 46, "#fff", 900) + label("IRR", 0, -40, 50, "#555", 800)
            + punch(irr, 0, 60, 88, fill=("#4A78C8" if c == NAVY else c)) + label(note, 0, 170, 34, "#666", 800) + '</g></g>')

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="80" y="1360" width="920" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.05 · Subscription Line의 비밀", 540, 1425, 50, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#E3F1EF")]
    s.append(punch("같은 딜, 다른 IRR?", 540, 170, 100, fill=TEAL, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    pa, pb = ease_out(prog(t, .5, .45)), ease_out(prog(t, 1.1, .45))
    inner.append(report_card(305, 640, "보고서 ①", "12.5%", NAVY, 1, -(1 - pa) * 700, "4년 뒤 160 회수"))
    inner.append(report_card(775, 640, "보고서 ②", "15.1%", TEAL, 1, (1 - pb) * 700, "4년 뒤 160 회수"))
    if t > 1.9:
        inner.append(punch("?!", 540, 640, 110, fill=YELLOW, scale=back(prog(t, 1.9, .35)), rot=8))
    inner.append(penguin(540, 1260, .78, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["회수 금액이 똑같은데", "IRR은 왜 올랐죠?"], 540, 1700, 820, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.0, .45)), size=58))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.0))
    s.append(bubble(["GP가 은행 돈으로 먼저 사고,", "우리 돈은 1년 늦게 불렀거든."], 540, 330, 1000, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=52))
    if t > 3.0:
        s.append(punch("시계를 늦게 켰다!", 540, 1650, 130, fill=YELLOW, scale=back(prog(t, 3.0, .45)), rot=-5))
    return s

def timeline(t, y0, tag, c, a0, bank, chip_txt, years):
    """y0 = 기준선. bank=True면 0년차 은행 차입 → 1년차 LP 콜 105."""
    X0, X1, k = 300, 960, .5
    xs = lambda yr: X0 + (X1 - X0) * yr / 4
    o = []
    ap = ease_out(prog(t, a0, .4))
    o.append(f'<g opacity="{ap:.2f}">' + chip(tag, 165, y0, c, 1, w=210, size=36)
             + f'<line x1="{X0-30}" y1="{y0}" x2="{X1+20}" y2="{y0}" stroke="{NAVY}" stroke-width="5"/>'
             + "".join(f'<line x1="{xs(y)}" y1="{y0-10}" x2="{xs(y)}" y2="{y0+10}" stroke="{NAVY}" stroke-width="4"/>' for y in range(5))
             + '</g>')
    start = 0
    if bank:
        gb = ease_out(prog(t, a0 + .4, .4))
        o.append(f'<rect x="{xs(0)-32}" y="{y0}" width="64" height="{100*k*gb:.0f}" fill="{GREY}"/>')
        if gb > .9: o.append(label("은행 100", xs(0), y0 + 80, 30, GREY, 900))
        gl = ease_out(prog(t, a0 + 1.0, .4))
        o.append(f'<rect x="{xs(1)-32}" y="{y0}" width="64" height="{105*k*gl:.0f}" fill="{RED}"/>')
        if gl > .9: o.append(label("LP −105", xs(1) + 45, y0 + 30, 34, RED, 900, "start"))
        start = 1
    else:
        g = ease_out(prog(t, a0 + .4, .4))
        o.append(f'<rect x="{xs(0)-32}" y="{y0}" width="64" height="{100*k*g:.0f}" fill="{RED}"/>')
        if g > .9: o.append(label("LP −100", xs(0) + 45, y0 + 30, 34, RED, 900, "start"))
    ar = ease_out(prog(t, a0 + 1.4, .9))
    if ar > 0:
        xe = xs(start) + (xs(4) - xs(start)) * ar
        o.append(f'<line x1="{xs(start)}" y1="{y0-28}" x2="{xe:.0f}" y2="{y0-28}" stroke="{c}" stroke-width="6" stroke-dasharray="14 10"/>')
        if ar > .95: o.append(label(years, (xs(start) + xs(4)) / 2, y0 - 62, 34, c, 900))
    g2 = ease_out(prog(t, a0 + 2.3, .45))
    if g2 > 0:
        h = 160 * k * g2
        o.append(f'<rect x="{xs(4)-32}" y="{y0-h:.0f}" width="64" height="{h:.0f}" fill="{GREEN}"/>')
        if g2 > .9: o.append(label("+160", xs(4) - 48, y0 - h + 20, 36, GREEN, 900, "end"))
    o.append(chip(chip_txt, 600, y0 + 150, c, back(prog(t, a0 + 2.8, .4)), w=600, size=40))
    return "".join(o)

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("시계를 늦게 켜면", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("같은 딜 · 신용한도 금리 5% · 손계산 예시", 540, 275, 42, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1230" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<g opacity="{ease_out(prog(t, .4, .4))}">'
             + "".join(label(str(y), 300 + 165 * y, 385, 32, "#777", 700) for y in range(5))
             + label("연차", 1010, 350, 28, "#777", 700, "end") + "</g>")
    s.append(timeline(t, 560, "① 없음", NAVY, .5, False, "IRR 12.5% · MOIC 1.60×", "4년"))
    s.append(timeline(t, 935, "② 사용", TEAL, 3.6, True, "IRR 15.1% · MOIC 1.52×", "3년"))
    s.append(eq_img(0, 540, 1170, ease_out(prog(t, 7.2, .5))))
    s.append(eq_img(1, 540, 1265, ease_out(prog(t, 7.9, .5))))
    s.append(eq_img(2, 540, 1370, ease_out(prog(t, 8.6, .5))))
    s.append(owl(180, 1735, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["IRR은 올랐지만, 이자 5만큼", "손에 쥐는 돈은 줄었지."], 650, 1700, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.6, .45)), size=46))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "shock" if t > 3.2 else "worry", sweat=prog(t, 3.2, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("LP 체크: 신용한도 전·후 IRR 함께 받기 (ILPA)", 540, 1480, NAVY, back(prog(t, 4.3, .45)), w=900, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["GP는 왜", "그렇게 해요?"], 380, 320, 560, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=54))
    if t > 1.6:
        s.append(bubble(["IRR로 다음 펀드를 모으고,", "허들 8%도 빨리 넘어 Carry를 받지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.2:
        s.append(punch("그랬구나!", 300, 740, 110, fill="#fff", scale=back(prog(t, 3.2, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(TEAL, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("PME", 540, 860, 230, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("그래서, 시장보다 잘했나?", 540, 1100, 60, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry"))
    return s

FUNCS = [cut1, cut2, cut3, cut4, cut5, cut6]

def frame_svg(T):
    for i, (a, b) in enumerate(CUTS):
        if a <= T < b or (i == len(CUTS) - 1 and T >= a):
            t = T - a
            body = "".join(FUNCS[i](t))
            fl = 1 - prog(t, 0, .18) if i > 0 else 0
            if fl > 0: body += f'<rect width="{W}" height="{H}" fill="#fff" opacity="{fl:.2f}"/>'
            return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                    f'width="{W}" height="{H}">{DEFS}{body}</svg>')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for i, T in enumerate([2.8, 8.8, 15.0, 28.5, 35.5, 39.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep05_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm05.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep05.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
