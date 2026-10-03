"""EP.03 '분배금이 왔다 — DPI vs TVPI' — 9:16 웹툰 숏폼. 공통 부품은 render_ep01에서 가져온다.
수식은 eq/*.png (pdflatex 렌더)를 SVG에 임베드한다."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)

GREEN = "#1E7F4F"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10), (10, 15.5), (15.5, 26), (26, 31.5), (31.5, 35)]
DUR = 35
PAID, DIST, NAV = 100, 70, 90          # 설명용 예시 (약정 대비 납입 100 기준)

def _eq(i):
    p = os.path.join(HERE, "eq", f"eq{i}.png")
    w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * .6, h * .6
EQS = [_eq(i) for i in (1, 2, 3)]

def eq_img(i, x, y, a):
    b64, w, h = EQS[i]
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})">'
            f'<image x="{x - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'xlink:href="data:image/png;base64,{b64}" xmlns:xlink="http://www.w3.org/1999/xlink"/></g>')

def coin(x, y, r=34, rot=0):
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})"><circle r="{r}" fill="{YELLOW}" stroke="{NAVY}" stroke-width="6"/>'
            + label("₩", 0, 2, r * 1.1, NAVY, 900) + '</g>')

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="190" y="1360" width="700" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.03 · 분배금이 왔다", 540, 1425, 56, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "happy", flap=prog(t, 2.6, 1.2)))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#DDF0E4")]
    s.append(punch("드디어 입금!", 540, 170, 110, fill=GREEN, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = ease_out(prog(t, .5, .4))
    inner.append(f'<g transform="translate({(1-p)*900:.0f},0)"><g transform="translate(540,470)">'
                 f'<rect x="-400" y="-95" width="800" height="190" rx="28" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
                 f'<rect x="-370" y="-55" width="120" height="90" rx="10" fill="{GREEN}" stroke="{NAVY}" stroke-width="6"/>'
                 f'<polyline points="-370,-55 -310,-5 -250,-55" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/>'
                 + label("Distribution Notice · GP A", -210, -30, 42, NAVY, 900, "start")
                 + label("포트폴리오 회사 매각 대금 분배", -210, 35, 38, "#444", 700, "start") + '</g></g>')
    # 동전 비
    if t > 1.0:
        for k in range(14):
            st = 1.0 + (k % 7) * .18 + (k // 7) * .6
            tt = (t - st) % 1.3 if t - st > 0 else -1
            if tt > 0:
                x = 170 + (k * 137) % 760
                y = 600 + tt * 650 - 0 * k
                if y < 1430: inner.append(coin(x, y, 30, tt * 200 + k * 30))
    inner.append(penguin(540, 1240, .8, "happy", flap=prog(t, 1.2, 2.0)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["부장님! 우리 펀드가", "벌써 1.6배래요! 부자다!!"], 540, 1700, 900, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.2, .45)), size=56))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 2.6))
    s.append(bubble(["1.6배는 TVPI야.", "실제로 손에 쥔 돈은 DPI로 봐야지."], 540, 330, 1000, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=52))
    if t > 2.6:
        s.append(punch("절반 넘게 평가액!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 2.6, .45)), rot=-5))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("DPI vs TVPI", 540, 150, 110, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("납입 100 기준 · 지금까지의 성적표 (예시)", 540, 275, 44, NAVY, 700) + "</g>")
    s.append(f'<rect x="60" y="330" width="960" height="1210" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    BASE, k, bw = 1010, 3.5, 230
    # 납입 막대
    g1 = ease_out(prog(t, .6, .7))
    s.append(f'<rect x="{300-bw/2}" y="{BASE-PAID*k*g1:.0f}" width="{bw}" height="{PAID*k*g1:.0f}" fill="{NAVY}"/>')
    if g1 > .9: s.append(label("납입 100", 300, BASE - PAID * k / 2, 46, "#fff", 900))
    s.append(label("Paid-in", 300, BASE + 45, 36, "#555", 800))
    # 분배 + NAV 누적 막대
    g2 = ease_out(prog(t, 1.4, .7)); g3 = ease_out(prog(t, 2.2, .7))
    hd, hn = DIST * k * g2, NAV * k * g3
    s.append(f'<rect x="{720-bw/2}" y="{BASE-hd:.0f}" width="{bw}" height="{hd:.0f}" fill="{GREEN}"/>')
    if g2 > .9: s.append(label("분배 70", 720, BASE - DIST * k / 2, 46, "#fff", 900))
    if hn > 0:
        s.append(f'<rect x="{720-bw/2}" y="{BASE-hd-hn:.0f}" width="{bw}" height="{hn:.0f}" fill="{ORANGE}"/>')
        s.append(f'<rect x="{720-bw/2}" y="{BASE-hd-hn:.0f}" width="{bw}" height="{hn:.0f}" fill="url(#dotsW)"/>')
    if g3 > .9: s.append(label("NAV 90", 720, BASE - DIST * k - NAV * k / 2 - 18, 46, "#fff", 900)
                         + label("(미실현)", 720, BASE - DIST * k - NAV * k / 2 + 32, 32, "#fff", 800))
    s.append(label("Value", 720, BASE + 45, 36, "#555", 800))
    tv = back(prog(t, 4.0, .4))
    if tv > 0:
        s.append(f'<g transform="translate(720,{BASE-(DIST+NAV)*k-50}) scale({tv})"><rect x="-150" y="-36" width="300" height="72" rx="18" fill="{NAVY}"/>' + label("TVPI 1.6×", 0, 0, 40, "#fff", 900) + "</g>")
    s.append(f'<line x1="120" y1="{BASE}" x2="960" y2="{BASE}" stroke="{NAVY}" stroke-width="5"/>')
    # 괄호 표시: DPI (분배 구간), TVPI (전체)
    def brace(y0, y1, txt, c, a):
        if a <= 0: return ""
        x = 865
        return (f'<g opacity="{a:.2f}"><path d="M {x-20} {y0} h 20 v {y1-y0} h -20" fill="none" stroke="{c}" stroke-width="7"/>'
                + label(txt, x + 50, (y0 + y1) / 2, 40, c, 900) + '</g>')
    s.append(brace(BASE - DIST * k, BASE, "DPI", GREEN, ease_out(prog(t, 3.2, .4))))
    s.append(brace(BASE - (DIST + NAV) * k, BASE - DIST * k - 8, "RVPI", ORANGE, ease_out(prog(t, 3.6, .4))))
    # 수식 (LaTeX)
    s.append(eq_img(0, 540, 1090, ease_out(prog(t, 4.2, .5))))
    s.append(eq_img(1, 540, 1235, ease_out(prog(t, 5.0, .5))))
    s.append(eq_img(2, 540, 1395, ease_out(prog(t, 5.8, .5))))
    s.append(owl(180, 1720, .45, point=True, blink=(8.0 < t < 8.15)))
    s.append(bubble(["NAV는 GP의 평가액이라", "팔기 전까진 확정이 아니야."], 640, 1700, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 7.0, .45)), size=48))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1150, .9, "happy" if t > 3.0 else "worry", flap=prog(t, 3.0, 1.2))
    inner += owl(780, 1180, .78, blink=(1.2 < t < 1.35))
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 뭘 보고", "판단해야 해요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6:
        s.append(bubble(["초기엔 TVPI, 후반엔 DPI.", "둘의 차이가 미실현 몫이야."], 540, 1720, 920, 230, tail=(0.5, -1),
                        scale=back(prog(t, 1.6, .4)), size=50))
    if t > 3.0:
        s.append(punch("메모!", 230, 760, 120, fill="#fff", scale=back(prog(t, 3.0, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(NAVY, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("IRR의 함정", 540, 860, 190, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("빨리 돌려주면 IRR이 오른다?", 540, 1080, 56, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "shock", sweat=prog(t, 2.0, .5)))
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
        for i, T in enumerate([2.8, 8.6, 14.0, 25.0, 30.5, 34.4]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep03_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, DUR
    wav = f"{OUT}/bgm03.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep03.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
