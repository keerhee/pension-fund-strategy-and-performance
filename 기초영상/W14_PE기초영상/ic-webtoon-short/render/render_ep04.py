"""EP.04 'IRR의 함정' — 9:16 웹툰 숏폼. IRR(속도)과 MOIC(크기)의 차이를 손계산 수치로 보여준다."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)

GREEN, PURPLE = "#1E7F4F", "#5B3FA0"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10), (10, 15.5), (15.5, 27), (27, 33), (33, 36.5)]
DUR = 36.5

def _eq(name, s=.5):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep04_1"), _eq("ep04_2"), _eq("ep04_3")]

def eq_img(i, x, y, a):
    b64, w, h = EQS[i]
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})">'
            f'<image x="{x - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'xlink:href="data:image/png;base64,{b64}"/></g>')

def chip(txt, x, y, c, sc, w=420, size=40):
    if sc <= 0: return ""
    return (f'<g transform="translate({x},{y}) scale({sc})"><rect x="{-w/2}" y="-40" width="{w}" height="80" rx="20" fill="{c}"/>'
            + label(txt, 0, 0, size, "#fff", 900) + "</g>")

def pitch_card(x, y, gp, irr, c, sc, x_off):
    return (f'<g transform="translate({x_off:.0f},0)"><g transform="translate({x},{y}) scale({sc})">'
            f'<rect x="-200" y="-230" width="400" height="460" rx="30" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
            f'<rect x="-200" y="-230" width="400" height="110" rx="30" fill="{c}"/><rect x="-200" y="-150" width="400" height="30" fill="{c}"/>'
            + label(gp, 0, -175, 52, "#fff", 900) + label("IRR", 0, -40, 50, "#555", 800)
            + punch(irr, 0, 60, 120, fill=c) + label("제안서 1쪽", 0, 170, 34, "#888", 700) + '</g></g>')

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="240" y="1360" width="600" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.04 · IRR의 함정", 540, 1425, 56, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#EDE6F7")]
    s.append(punch("GP 제안서 비교", 540, 170, 104, fill=PURPLE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    pa, pb = ease_out(prog(t, .5, .45)), ease_out(prog(t, 1.1, .45))
    inner.append(pitch_card(305, 640, "펀드 A", "50%", ORANGE, 1, -(1 - pa) * 700))
    inner.append(pitch_card(775, 640, "펀드 B", "25%", GREEN, 1, (1 - pb) * 700))
    if t > 2.2:
        inner.append(punch("반짝!", 420, 345, 70, fill=YELLOW, scale=back(prog(t, 2.2, .35)), rot=-12))
    inner.append(penguin(540, 1260, .78, "happy" if t > 2.4 else "worry", flap=prog(t, 2.4, 1.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["당연히 A죠!", "IRR이 두 배잖아요!"], 540, 1700, 820, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.0, .45)), size=58))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 2.6))
    s.append(bubble(["잠깐. 얼마를, 얼마 동안", "불렸는지부터 봐야지."], 540, 330, 960, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=54))
    if t > 2.6:
        s.append(punch("배수도 봐!", 540, 1650, 190, fill=YELLOW, scale=back(prog(t, 2.6, .45)), rot=-5))
    return s

def row(t, y0, name, c, exit_yr, amount, a0, chip_txt):
    """한 펀드의 현금흐름 타임라인. y0 = 기준선."""
    X0, X1, k = 260, 960, .5
    xs = lambda yr: X0 + (X1 - X0) * yr / 5
    out = []
    ap = ease_out(prog(t, a0, .4))
    out.append(f'<g opacity="{ap:.2f}">' + label(name, 150, y0, 46, c, 900)
               + f'<line x1="{X0-30}" y1="{y0}" x2="{X1+20}" y2="{y0}" stroke="{NAVY}" stroke-width="5"/>')
    for yr in range(6):
        out.append(f'<line x1="{xs(yr)}" y1="{y0-10}" x2="{xs(yr)}" y2="{y0+10}" stroke="{NAVY}" stroke-width="4"/>')
    out.append('</g>')
    g = ease_out(prog(t, a0 + .4, .4))
    out.append(f'<rect x="{xs(0)-35}" y="{y0}" width="70" height="{100*k*g:.0f}" fill="{RED}"/>')
    if g > .9: out.append(label("−100", xs(0) + 80, y0 + 45, 36, RED, 900))
    # 시간 화살표 (돈이 묶여 있는 기간)
    ar = ease_out(prog(t, a0 + .9, .9))
    if ar > 0:
        xe = xs(0) + (xs(exit_yr) - xs(0)) * ar
        out.append(f'<line x1="{xs(0)}" y1="{y0-30}" x2="{xe:.0f}" y2="{y0-30}" stroke="{c}" stroke-width="6" stroke-dasharray="14 10"/>')
    g2 = ease_out(prog(t, a0 + 1.8, .45))
    if g2 > 0:
        h = amount * k * g2
        out.append(f'<rect x="{xs(exit_yr)-35}" y="{y0-h:.0f}" width="70" height="{h:.0f}" fill="{GREEN}"/>')
        if g2 > .9: out.append(label(f"+{amount}", xs(exit_yr) - 50, y0 - h + 20, 38, GREEN, 900, "end"))
    out.append(chip(chip_txt, 610, y0 + 125, c, back(prog(t, a0 + 2.4, .4)), w=640, size=38))
    return "".join(out)

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("속도 vs 크기", 540, 150, 112, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("둘 다 100을 넣었다면 · 손계산 예시", 540, 275, 44, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1220" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<g opacity="{ease_out(prog(t, .4, .4))}">'
             + "".join(label(str(y), 260 + 140 * y, 395, 32, "#777", 700) for y in range(6))
             + label("연차", 1010, 355, 28, "#777", 700, "end") + "</g>")
    s.append(row(t, 560, "A", ORANGE, 1, 150, .5, "IRR 50% · MOIC 1.5× · 이익 50"))
    s.append(row(t, 930, "B", GREEN, 5, 300, 2.6, "IRR 25% · MOIC 3.0× · 이익 200"))
    s.append(eq_img(0, 540, 1140, ease_out(prog(t, 5.6, .5))))
    s.append(eq_img(1, 540, 1255, ease_out(prog(t, 6.3, .5))))
    s.append(eq_img(2, 540, 1375, ease_out(prog(t, 7.0, .5))))
    s.append(owl(180, 1730, .45, point=True, blink=(9.5 < t < 9.65)))
    s.append(bubble(["IRR은 속도,", "배수(MOIC)는 크기야."], 640, 1700, 720, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 8.0, .45)), size=52))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1150, .9, "shock" if t > 3.2 else "worry", sweat=prog(t, 3.2, .4))
    inner += owl(780, 1180, .78, blink=(1.2 < t < 1.35))
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 IRR만 올리는", "방법도 있어요?"], 400, 320, 640, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["Subscription Line으로 콜을 늦추면", "IRR이 올라가. 그래서 둘 다 봐."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.2:
        s.append(punch("소름!", 230, 760, 120, fill="#fff", scale=back(prog(t, 3.2, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(PURPLE, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("시계 조작?", 540, 860, 190, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("Subscription Line의 비밀", 540, 1100, 60, "#fff", 800) + "</g>")
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
        for i, T in enumerate([2.8, 8.8, 14.0, 26.5, 32.5, 36.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep04_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm04.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep04.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
