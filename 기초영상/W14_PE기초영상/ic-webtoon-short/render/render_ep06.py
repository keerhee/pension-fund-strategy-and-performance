"""EP.06 'PME — 시장보다 잘했나?' — 9:16 웹툰 숏폼.
EP.05의 딜(100 → 4년 뒤 160, IRR 12.5%)을 같은 기간 지수에 넣었을 때와 비교한다 (Kaplan-Schoar PME)."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)
from render_ep05 import chip

GREEN, GREY, PLUM = "#1E7F4F", "#8A94A6", "#7A2E5C"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10), (10, 16), (16, 29), (29, 36), (36, 39.5)]
DUR = 39.5

def _eq(name, s=.5):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep06_1"), _eq("ep06_2"), _eq("ep06_3")]

def eq_img(i, x, y, a):
    b64, w, h = EQS[i]
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})">'
            f'<image x="{x - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" xlink:href="data:image/png;base64,{b64}"/></g>')

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="130" y="1360" width="820" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.06 · PME, 시장보다 잘했나?", 540, 1425, 52, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "happy", flap=prog(t, 2.6, 1.0)))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#F6E7EF")]
    s.append(punch("IC 성과 보고", 540, 170, 110, fill=PLUM, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = ease_out(prog(t, .5, .45))
    inner.append(f'<g transform="translate(0,{(1-p)*-500:.0f})"><g transform="translate(540,620)">'
                 f'<rect x="-380" y="-210" width="760" height="420" rx="30" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 + label("PE 펀드 · 4년 성적표", 0, -140, 46, NAVY, 900)
                 + label("IRR", -185, -30, 48, "#555", 800) + punch("12.5%", -185, 60, 84, fill=GREEN)
                 + label("MOIC", 185, -30, 48, "#555", 800) + punch("1.60×", 185, 60, 84, fill=GREEN)
                 + label("100 → 160", 0, 160, 40, "#666", 800) + '</g></g>')
    if t > 2.0:
        inner.append(punch("짜잔!", 860, 400, 80, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=14))
    inner.append(penguin(540, 1260, .78, "happy", flap=prog(t, 2.0, 1.2)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["IRR 12.5%, MOIC 1.6배!", "이 정도면 대성공이죠?"], 540, 1700, 860, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.0, .45)), size=56))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.0))
    s.append(bubble(["같은 날, 같은 돈을 주식시장에", "넣었으면 얼마가 됐을까?"], 540, 330, 1000, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=52))
    if t > 3.0:
        s.append(punch("비교 대상이 먼저!", 540, 1650, 130, fill=YELLOW, scale=back(prog(t, 3.0, .45)), rot=-5))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("PME = 시장 대비 성적", 540, 150, 92, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("Public Market Equivalent · 같은 돈을 지수에 넣었다면", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1150" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    BASE, k, bw = 820, 1.9, 190
    bars = [(200, 160, GREEN, "PE 펀드", "160", .6),
            (540, 200, NAVY, "지수 2배", "200", 1.4),
            (880, 140, GREY, "지수 1.4배", "140", 2.2)]
    for x, v, c, name, val, a in bars:
        g = ease_out(prog(t, a, .6)); h = v * k * g
        s.append(f'<rect x="{x-bw/2}" y="{BASE-h:.0f}" width="{bw}" height="{h:.0f}" fill="{c}"/>')
        if g > .9: s.append(label(val, x, BASE - h + 45, 46, "#fff", 900))
        s.append(f'<g opacity="{ease_out(prog(t, a, .4)):.2f}">' + label(name, x, BASE + 40, 38, NAVY, 900) + '</g>')
    s.append(f'<line x1="110" y1="{BASE}" x2="970" y2="{BASE}" stroke="{NAVY}" stroke-width="5"/>')
    # 펀드 160 기준선
    gl = ease_out(prog(t, 3.0, .6))
    if gl > 0:
        y = BASE - 160 * k
        s.append(f'<line x1="105" y1="{y:.0f}" x2="{105 + 870*gl:.0f}" y2="{y:.0f}" stroke="{GREEN}" stroke-width="5" stroke-dasharray="12 9"/>')
    s.append(chip("PME 0.80 · 시장에 짐", 540, BASE + 110, RED, back(prog(t, 3.6, .4)), w=300, size=30))
    s.append(chip("PME 1.14 · 시장 이김", 870, BASE + 110, GREEN, back(prog(t, 4.2, .4)), w=300, size=30))
    s.append(eq_img(0, 300, 990, ease_out(prog(t, 5.2, .5))))
    s.append(eq_img(1, 760, 992, ease_out(prog(t, 6.0, .5))))
    s.append(eq_img(2, 540, 1160, ease_out(prog(t, 6.8, .5))))
    s.append(f'<g opacity="{ease_out(prog(t, 7.4, .5)):.2f}">'
             + label("D: 분배, C: 납입(콜), I: 지수 수준", 540, 1335, 34, "#666", 700)
             + label("지수 2배 = 연 18.9% > 펀드 IRR 12.5%", 540, 1400, 34, RED, 800) + '</g>')
    s.append(owl(180, 1700, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["PME가 1보다 커야", "시장을 이긴 거야."], 650, 1670, 720, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 8.6, .45)), size=52))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1150, .9, "happy" if t > 3.4 else "worry", flap=prog(t, 3.4, 1.2))
    inner += owl(780, 1180, .78, blink=(1.2 < t < 1.35))
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 지수는", "뭘로 골라요?"], 380, 320, 560, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=54))
    if t > 1.6:
        s.append(bubble(["투자 대상과 닮은 지수로.", "바이아웃이면 소형주 지수를 쓰기도 해."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.4:
        s.append(punch("벤치마크가 반!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.4, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(PLUM, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("세컨더리", 540, 860, 210, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("펀드 지분도 사고판다?", 540, 1100, 60, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "shock"))
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
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep06_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm06.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep06.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
