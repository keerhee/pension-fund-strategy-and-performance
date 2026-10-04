"""EP.09 '2 and 20 — 보수는 실제로 얼마나 떼가나?' — 9:16 웹툰 숏폼.
약정 100, 관리보수 2%×10년=20, 투자 80이 2.0배 → 160. 이익 60의 20% Carry 12 → LP 148, Net MOIC 1.48×."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)
from render_ep05 import chip

GREEN, GREY, GOLD = "#1E7F4F", "#8A94A6", "#9A6B00"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10), (10, 16.5), (16.5, 30), (30, 37), (37, 40.5)]
DUR = 40.5

def _eq(name, s=.44):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep09_1"), _eq("ep09_2"), _eq("ep09_3")]

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
             f'<rect x="230" y="1360" width="620" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.09 · 2 and 20", 540, 1425, 56, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "happy"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#F7EED8")]
    s.append(punch("GP 펀드레이징 미팅", 540, 170, 96, fill=GOLD, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,660) scale({p:.3f})">'
                 f'<rect x="-380" y="-250" width="760" height="500" rx="28" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 + label("Track Record", 0, -185, 46, NAVY, 900)
                 + label("Gross MOIC", 0, -90, 50, "#555", 800)
                 + punch("2.0×", 0, 30, 170, fill=GREEN)
                 + label("보수 · Carry 차감 전", 0, 175, 36, "#999", 700) + '</g>')
    if t > 2.0:
        inner.append(punch("두 배!", 850, 420, 90, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=14))
    inner.append(penguin(540, 1290, .72, "happy", flap=prog(t, 2.0, 1.2)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["100 넣으면 200 된대요!", "바로 약정하죠!"], 540, 1700, 820, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.0, .45)), size=58))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(["그건 보수 떼기 전 숫자야.", "2% 관리보수, 20% Carry를 빼 봐."], 540, 330, 1000, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=50))
    if t > 3.2:
        s.append(punch("Gross ≠ Net!", 540, 1650, 125, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("100이 어디로 가나", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("약정 100 · 10년 · 관리보수 2% · Carry 20% · 손계산", 540, 275, 40, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1130" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    BASE, k, bw = 960, 3.3, 230
    # 막대 1: 약정 100 = 투자 80 + 보수 20
    g1 = ease_out(prog(t, .5, .6))
    h80, h20 = 80 * k * g1, 20 * k * g1
    x1 = 290
    s.append(f'<rect x="{x1-bw/2}" y="{BASE-h80:.0f}" width="{bw}" height="{h80:.0f}" fill="{NAVY}"/>')
    s.append(f'<rect x="{x1-bw/2}" y="{BASE-h80-h20:.0f}" width="{bw}" height="{h20:.0f}" fill="{RED}"/>')
    if g1 > .9:
        s.append(label("투자 80", x1, BASE - h80 / 2, 44, "#fff", 900))
        s.append(label("보수 20", x1, BASE - h80 - h20 / 2, 38, "#fff", 900))
    s.append(f'<g opacity="{ease_out(prog(t, .5, .4)):.2f}">' + label("LP가 낸 돈 100", x1, BASE + 42, 36, NAVY, 900) + '</g>')
    # 화살표 ×2.0
    ar = ease_out(prog(t, 1.6, .6))
    if ar > 0:
        s.append(f'<g opacity="{ar:.2f}"><line x1="425" y1="{BASE-150}" x2="{425 + 165*ar:.0f}" y2="{BASE-150}" stroke="{GREEN}" stroke-width="9"/>'
                 + (f'<polygon points="590,{BASE-150} 566,{BASE-165} 566,{BASE-135}" fill="{GREEN}"/>' if ar > .95 else "")
                 + label("투자분 ×2.0", 505, BASE - 190, 34, GREEN, 900) + '</g>')
    # 막대 2: 회수 160 = 원금 100 + LP 이익 48 + Carry 12
    x2 = 760
    g2 = ease_out(prog(t, 2.4, .6)); g3 = ease_out(prog(t, 3.4, .5)); g4 = ease_out(prog(t, 4.2, .5))
    hp, hl, hc = 100 * k * g2, 48 * k * g3, 12 * k * g4
    s.append(f'<rect x="{x2-bw/2}" y="{BASE-hp:.0f}" width="{bw}" height="{hp:.0f}" fill="{GREY}"/>')
    if g2 > .9: s.append(label("원금 100", x2, BASE - hp / 2, 44, "#fff", 900))
    if hl > 0:
        s.append(f'<rect x="{x2-bw/2}" y="{BASE-hp-hl:.0f}" width="{bw}" height="{hl:.0f}" fill="{GREEN}"/>')
        if g3 > .9: s.append(label("LP 이익 48", x2, BASE - hp - hl / 2, 40, "#fff", 900))
    if hc > 0:
        s.append(f'<rect x="{x2-bw/2}" y="{BASE-hp-hl-hc:.0f}" width="{bw}" height="{hc:.0f}" fill="{GOLD}"/>')
        if g4 > .9: s.append(label("Carry 12 → GP", x2, BASE - hp - hl - hc - 30, 34, GOLD, 900))
    s.append(f'<g opacity="{ease_out(prog(t, 2.4, .4)):.2f}">' + label("회수 160", x2, BASE + 42, 36, NAVY, 900) + '</g>')
    s.append(f'<line x1="110" y1="{BASE}" x2="970" y2="{BASE}" stroke="{NAVY}" stroke-width="5"/>')
    s.append(chip("Gross 2.0×", 330, BASE + 120, GREY, back(prog(t, 4.8, .4)), w=300, size=40))
    s.append(punch("→", 540, BASE + 120, 70, fill=NAVY, scale=back(prog(t, 5.0, .3))))
    s.append(chip("Net 1.48×", 750, BASE + 120, GREEN, back(prog(t, 5.2, .4)), w=300, size=40))
    s.append(eq_img(0, 540, 1170, ease_out(prog(t, 6.0, .5))))
    s.append(eq_img(1, 540, 1250, ease_out(prog(t, 6.7, .5))))
    s.append(eq_img(2, 540, 1335, ease_out(prog(t, 7.4, .5))))
    s.append(owl(180, 1730, .45, point=True, blink=(11.8 < t < 11.95)))
    s.append(bubble(["투자 이익 80 중 32가 GP 몫.", "보수 20 + Carry 12야."], 650, 1680, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 8.6, .45)), size=46))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: Fee 기준 · 허들 · 캐치업 · 보수 상계", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=880, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["보수는 협상", "못 해요?"], 380, 320, 520, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=54))
    if t > 1.6:
        s.append(bubble(["투자기간이 끝나면 Fee 기준을", "약정 대신 투자잔액으로 바꾸자고 하지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("협상 포인트!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(GOLD, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("캐치업", 540, 860, 230, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("허들 넘으면 GP가 100%를?", 540, 1090, 56, "#fff", 800) + "</g>")
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
        for i, T in enumerate([2.8, 9.4, 16.0, 29.5, 36.5, 40.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep09_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm09.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep09.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
