"""EP.10 '캐치업 — 허들 넘으면 GP가 100%를?' — 9:16 웹툰 숏폼.
EP.09와 같은 숫자: 납입 100, 회수 160. 원금 100 → 허들 8 → 캐치업 2(GP 100%) → 잔여 50을 80/20 → LP 148, GP 12."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)
from render_ep05 import chip

GREEN, GREY, GOLD, TEAL = "#1E7F4F", "#8A94A6", "#9A6B00", "#0B6B68"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10.5), (10.5, 17.5), (17.5, 32), (32, 39), (39, 42.5)]
DUR = 42.5

def _eq(name, s=.5):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep10_1"), _eq("ep10_2"), _eq("ep10_3")]

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
             f'<rect x="170" y="1360" width="740" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.10 · 캐치업 (Catch-up)", 540, 1425, 54, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#E3F1EF")]
    s.append(punch("LPA 검토 중", 540, 170, 110, fill=TEAL, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,650) scale({p:.3f})">'
                 f'<rect x="-380" y="-260" width="760" height="520" rx="22" fill="#FFFDF6" stroke="{NAVY}" stroke-width="8"/>'
                 + label("Section 8.2  Distributions", -330, -190, 40, NAVY, 900, "start")
                 + "".join(f'<rect x="-330" y="{-130 + i*58}" width="{560 - (i%3)*90}" height="18" rx="9" fill="#D9DCE3"/>' for i in range(2))
                 + f'<rect x="-345" y="-20" width="690" height="150" rx="14" fill="{YELLOW}" opacity=".45"/>'
                 + label("(ii) 8% Preferred Return to LPs", -330, 20, 38, NAVY, 900, "start")
                 + label("(iii) 100% to GP — Catch-up", -330, 90, 38, RED, 900, "start")
                 + f'<rect x="-330" y="170" width="480" height="18" rx="9" fill="#D9DCE3"/>' + '</g>')
    if t > 1.9:
        sc = back(prog(t, 1.9, .35))
        inner.append(f'<g transform="translate(870,560) scale({sc:.3f})"><circle r="80" fill="#fff" stroke="{RED}" stroke-width="9"/>'
                     + label("100%?", 0, 2, 38, RED, 900) + '</g>')
    inner.append(penguin(540, 1290, .7, "shock" if t > 2.4 else "worry", sweat=prog(t, 2.4, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["허들 넘으면 GP가 100%를?", "이거 독소조항 아니에요?"], 540, 1700, 900, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.2, .45)), size=54))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.4))
    s.append(bubble(["허들까지는 우리가 먼저 받고,", "GP는 이익의 20%를 '따라잡을' 때까지만 몰아받아."], 540, 330, 1020, 250,
                    tail=(0, 1), scale=back(prog(t, .7, .45)), size=44))
    if t > 3.4:
        s.append(punch("따라잡기!", 540, 1650, 190, fill=YELLOW, scale=back(prog(t, 3.4, .45)), rot=-5))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("160이 흘러가는 순서", 540, 150, 96, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("납입 100 · 회수 160 · 허들 8% · Carry 20% (EP.09와 같은 펀드)", 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1170" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    # 범례
    s.append(f'<g opacity="{ease_out(prog(t, .4, .4)):.2f}"><rect x="600" y="368" width="36" height="28" rx="6" fill="{GREEN}"/>'
             + label("LP", 648, 382, 32, NAVY, 900, "start")
             + f'<rect x="730" y="368" width="36" height="28" rx="6" fill="{GOLD}"/>' + label("GP", 778, 382, 32, NAVY, 900, "start") + '</g>')
    X0, k, hb = 330, 5.6, 64
    rows = [  # (y, 단계명, 부제, [(금액, 색, 텍스트)], 시작)
        (460, "① 원금 반환", "Return of Capital", [(100, GREEN, "LP 100")], .7),
        (580, "② 우선수익", "허들 8%", [(8, GREEN, "LP 8")], 1.7),
        (700, "③ 캐치업", "GP 100%", [(2, GOLD, "GP 2")], 2.7),
        (820, "④ 80 / 20", "잔여 50", [(40, GREEN, "LP 40"), (10, GOLD, "GP 10")], 3.7),
    ]
    for y, name, sub, parts, a in rows:
        ap = ease_out(prog(t, a, .35))
        if ap <= 0: continue
        s.append(f'<g opacity="{ap:.2f}">' + label(name, 85, y - 14, 38, NAVY, 900, "start")
                 + label(sub, 85, y + 30, 28, "#777", 800, "start") + '</g>')
        x = X0; g = ease_out(prog(t, a + .2, .6))
        for amt, c, txt in parts:
            w = amt * k * g
            s.append(f'<rect x="{x:.0f}" y="{y-hb/2}" width="{max(w, 0):.0f}" height="{hb}" rx="6" fill="{c}"/>')
            if g > .9:
                if w > 120: s.append(label(txt, x + w / 2, y, 34, "#fff", 900))
                else: s.append(label(txt, x + w + 12, y, 34, c, 900, "start"))
            x += w + (6 if len(parts) > 1 else 0)
    # 캐치업 강조
    if t > 3.2:
        sc = back(prog(t, 3.2, .35))
        s.append(f'<g transform="translate(700,700) scale({sc:.3f})">' + chip("8 : 2 = 80 : 20으로 맞춤", 0, 0, RED, 1, w=380, size=30) + '</g>')
    # 합계
    s.append(f'<line x1="85" y1="895" x2="995" y2="895" stroke="{NAVY}" stroke-width="4" opacity="{ease_out(prog(t, 4.6, .3)):.2f}"/>')
    s.append(chip("LP 148", 360, 955, GREEN, back(prog(t, 4.8, .4)), w=300, size=42))
    s.append(chip("GP 12 = 이익 60 × 20%", 760, 955, GOLD, back(prog(t, 5.2, .4)), w=440, size=36))
    s.append(eq_img(0, 540, 1035, ease_out(prog(t, 6.0, .5))))
    s.append(eq_img(1, 540, 1135, ease_out(prog(t, 6.8, .5))))
    s.append(eq_img(2, 540, 1235, ease_out(prog(t, 7.8, .5))))
    s.append(f'<g opacity="{ease_out(prog(t, 8.3, .4)):.2f}">' + label("캐치업이 없으면 GP 몫은 20%에 못 미친다", 540, 1360, 34, RED, 900) + '</g>')
    s.append(owl(180, 1735, .45, point=True, blink=(12.6 < t < 12.75)))
    s.append(bubble(["100%는 잠깐이야.", "결국 20%로 수렴하지."], 650, 1690, 720, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.4, .45)), size=50))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 허들 계산 방식 · 캐치업 비율 · 적용 단위", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=900, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 캐치업 비율도", "협상할 수 있어요?"], 400, 320, 640, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["100% 대신 80%·50% 캐치업도 있어.", "비율이 낮을수록 GP가 천천히 따라잡지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("이해 완료!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(TEAL, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("워터폴", 540, 860, 230, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("Carry는 언제 받나? 유럽식 vs 미국식", 540, 1090, 54, "#fff", 800) + "</g>")
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
        for i, T in enumerate([2.8, 9.9, 17.0, 31.5, 38.5, 42.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep10_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm10.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep10.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
