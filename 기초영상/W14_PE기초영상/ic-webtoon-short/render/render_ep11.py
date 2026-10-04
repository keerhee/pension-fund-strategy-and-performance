"""EP.11 '워터폴 — Carry는 언제 받나? 유럽식 vs 미국식' — 9:16 웹툰 숏폼.
딜 A: 50 → 100 (3년차), 딜 B: 50 → 20 (6년차). 펀드 납입 100, 회수 120, 이익 20.
미국식(딜별): 3년차 GP 10 → 과다, 클로백 6. 유럽식(펀드 전체): 원금 100 먼저, GP 4."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)
from render_ep05 import chip

GREEN, GREY, GOLD, BLUE = "#1E7F4F", "#8A94A6", "#9A6B00", "#2F6FB0"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10.5), (10.5, 17.5), (17.5, 32), (32, 39), (39, 42.5)]
DUR = 42.5

def _eq(name, s=.5):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep11_1"), _eq("ep11_2"), _eq("ep11_3")]

def eq_img(i, x, y, a):
    b64, w, h = EQS[i]
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})">'
            f'<image x="{x - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" xlink:href="data:image/png;base64,{b64}"/></g>')

def deal_card(x, y, name, inv, out, c, sc):
    if sc <= 0: return ""
    return (f'<g transform="translate({x},{y}) scale({sc:.3f})"><rect x="-200" y="-70" width="400" height="140" rx="20" fill="#fff" stroke="{c}" stroke-width="8"/>'
            + label(name, -170, -25, 38, c, 900, "start") + label(f"{inv} → {out}", 0, 30, 48, NAVY, 900) + '</g>')

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="150" y="1360" width="780" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.11 · 워터폴 (Waterfall)", 540, 1425, 54, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#E4ECF6")]
    s.append(punch("첫 딜 회수!", 540, 170, 110, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{BLUE}"/><rect x="-390" y="-180" width="780" height="26" fill="{BLUE}"/>'
                 + label("Distribution Notice · 딜 A 매각", 0, -202, 42, "#fff", 900)
                 + label("회수 100 (투자 50)", 0, -90, 46, NAVY, 900)
                 + label("LP 분배", -170, 10, 40, "#555", 800) + punch("90", -170, 90, 100, fill=GREEN)
                 + label("GP Carry", 170, 10, 40, "#555", 800) + punch("10", 170, 90, 100, fill=GOLD) + '</g>')
    if t > 2.0:
        inner.append(punch("벌써?!", 840, 960, 90, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=14))
    inner.append(penguin(540, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["GP는 벌써 Carry를 받았는데,", "우린 원금도 다 못 돌려받았어요!"], 540, 1700, 940, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=50))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.4))
    s.append(bubble(["딜별로 계산하는 미국식이라 그래.", "펀드 전체로 보는 유럽식이면 원금부터 다 받지."], 540, 330, 1020, 250,
                    tail=(0, 1), scale=back(prog(t, .7, .45)), size=44))
    if t > 3.4:
        s.append(punch("순서의 차이!", 540, 1650, 170, fill=YELLOW, scale=back(prog(t, 3.4, .45)), rot=-5))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("미국식 vs 유럽식", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("딜 2개 · 납입 100 · 회수 120 · Carry 20% (허들 생략)", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1170" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(deal_card(300, 430, "딜 A · 3년차", 50, 100, GREEN, back(prog(t, .5, .4))))
    s.append(deal_card(780, 430, "딜 B · 6년차", 50, 20, RED, back(prog(t, .9, .4))))
    # 두 줄 타임라인
    X0, X1 = 330, 980
    xs = lambda yr: X0 + (X1 - X0) * yr / 7
    rows = [(650, "미국식", "Deal-by-deal", BLUE, 1.5), (920, "유럽식", "Whole-of-fund", GREEN, 4.6)]
    for y, name, sub, c, a in rows:
        ap = ease_out(prog(t, a, .4))
        if ap <= 0: continue
        s.append(f'<g opacity="{ap:.2f}">' + label(name, 85, y - 16, 42, c, 900, "start") + label(sub, 85, y + 28, 28, "#777", 800, "start")
                 + f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{NAVY}" stroke-width="5"/>'
                 + "".join(f'<line x1="{xs(k)}" y1="{y-10}" x2="{xs(k)}" y2="{y+10}" stroke="{NAVY}" stroke-width="4"/>' for k in range(8))
                 + label("3년", xs(3), y + 40, 28, "#777", 800) + label("6년", xs(6), y + 40, 28, "#777", 800) + '</g>')
    # 미국식: 3년차 GP 10, 6년차 GP 0, 클로백 -6
    s.append(f'<g transform="translate({xs(3)},{560})">' + chip("GP 10", 0, 0, GOLD, back(prog(t, 2.0, .4)), w=170, size=36) + '</g>')
    s.append(f'<g transform="translate({xs(6)},{560})">' + chip("GP 0", 0, 0, GREY, back(prog(t, 2.6, .4)), w=150, size=36) + '</g>')
    if t > 3.3:
        sc = back(prog(t, 3.3, .45))
        s.append(f'<g transform="translate({xs(6)-70},{758}) rotate(-5) scale({sc:.3f})"><rect x="-150" y="-40" width="300" height="80" rx="14" fill="{RED}"/>'
                 + label("클로백 −6", 0, 0, 40, "#fff", 900) + '</g>')
    # 유럽식: 3년차 GP 0 (LP 원금 100 먼저), 6년차 GP 4
    s.append(f'<g transform="translate({xs(3)},{850})">' + chip("GP 0 · LP 100", 0, 0, GREY, back(prog(t, 5.0, .4)), w=250, size=34) + '</g>')
    s.append(f'<g transform="translate({xs(6)},{850})">' + chip("GP 4", 0, 0, GOLD, back(prog(t, 5.6, .4)), w=150, size=36) + '</g>')
    s.append(eq_img(0, 540, 1020, ease_out(prog(t, 6.4, .5))))
    s.append(eq_img(1, 540, 1110, ease_out(prog(t, 7.1, .5))))
    s.append(eq_img(2, 540, 1205, ease_out(prog(t, 7.8, .5))))
    s.append(f'<g opacity="{ease_out(prog(t, 8.3, .4)):.2f}">' + label("공정한 Carry는 4 · 미국식은 먼저 받고 나중에 정산", 540, 1345, 34, RED, 900) + '</g>')
    s.append(owl(180, 1735, .45, point=True, blink=(12.6 < t < 12.75)))
    s.append(bubble(["미국식이면 받은 Carry를", "돌려받는 장치가 꼭 필요해."], 650, 1690, 740, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=48))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 워터폴 방식 · 클로백 · 에스크로 · GP 보증", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["GP가 이미 쓴 돈이면", "어떻게 돌려받아요?"], 400, 320, 640, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["그래서 Carry 일부를 에스크로에 묶거나,", "GP 파트너들의 보증을 받아 두지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("안전장치!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(BLUE, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("NAV 론", 540, 860, 220, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("펀드가 포트폴리오를 담보로 돈을 빌린다?", 540, 1090, 50, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "shock", sweat=prog(t, 2.0, .4)))
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
        for i, T in enumerate([2.8, 9.9, 17.0, 31.5, 38.5, 42.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep11_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm11.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep11.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
