"""EP.07 '세컨더리 — 펀드 지분도 사고판다?' — 9:16 웹툰 숏폼.
매도자: 덴오미네이터 효과로 PE 비중 초과 → 할인 매각. 매수자: NAV 100을 85에 사 J-커브를 건너뛴다."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT, jcurve,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)
from render_ep05 import chip

GREEN, GREY, BLUE = "#1E7F4F", "#8A94A6", "#2F6FB0"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10.5), (10.5, 18), (18, 31), (31, 38), (38, 41.5)]
DUR = 41.5

def _eq(name, s=.5):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep07_1"), _eq("ep07_2"), _eq("ep07_3")]

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
             f'<rect x="210" y="1360" width="660" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.07 · 세컨더리", 540, 1425, 56, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#E4ECF6")]
    s.append(punch("지분 매물 등장", 540, 170, 108, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = ease_out(prog(t, .4, .4))
    inner.append(f'<g transform="translate({(1-p)*900:.0f},0)"><g transform="translate(540,450)">'
                 f'<rect x="-410" y="-75" width="820" height="150" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
                 f'<rect x="-385" y="-40" width="110" height="80" rx="12" fill="{RED}"/>' + label("속보", -330, 0, 40, "#fff", 900)
                 + label("주식 급락… 연기금들 PE 지분 매각", -250, 0, 38, NAVY, 900, "start") + '</g></g>')
    q = back(prog(t, 1.1, .45))
    inner.append(f'<g transform="translate(540,800) scale({q:.3f})">'
                 f'<rect x="-300" y="-190" width="600" height="380" rx="30" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 + label("PE 펀드 지분 (LP Interest)", 0, -125, 40, NAVY, 900)
                 + label("NAV 100", -140, -20, 52, "#777", 900)
                 + f'<line x1="-230" y1="-20" x2="-50" y2="-20" stroke="{RED}" stroke-width="8"/>'
                 + label("→", 20, -20, 52, NAVY, 900)
                 + punch("85", 150, -10, 120, fill=BLUE)
                 + label("매각 희망가", 0, 120, 36, "#666", 800) + '</g>')
    if t > 2.0:
        sc = back(prog(t, 2.0, .35))
        inner.append(f'<g transform="translate(730,985) rotate(-10) scale({sc:.3f})"><rect x="-130" y="-48" width="260" height="96" rx="14" '
                     f'fill="none" stroke="{RED}" stroke-width="9"/>' + label("15% 할인", 0, 0, 50, RED, 900) + '</g>')
    inner.append(penguin(540, 1290, .7, "shock" if t > 2.4 else "worry", sweat=prog(t, 2.4, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["100짜리를 85에 판대요!", "왜 손해 보고 팔죠?"], 540, 1700, 820, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.2, .45)), size=58))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(260, 1250 + (1 - ease_out(prog(t, 0, .5))) * 300, .85, blink=(2.1 < t < 2.25), point=t > 2.0))
    s.append(bubble(["주식이 빠지니 PE 비중이", "목표를 넘어버렸거든."], 540, 330, 960, 250, tail=(-0.5, 1),
                    scale=back(prog(t, .7, .45)), size=54))
    # 포트폴리오 막대: 전(100) → 주식 −30% 후(74.5)
    BASE, k, bw = 1460, 6.0, 170
    for x, tot, pe_pct, name, a in [(660, 100, 15, "평소", 1.6), (900, 74.5, 20, "주식 −30%", 2.6)]:
        g = ease_out(prog(t, a, .6)); hpe = 15 * k * g; hot = (tot - 15) * k * g
        s.append(f'<rect x="{x-bw/2}" y="{BASE-hpe:.0f}" width="{bw}" height="{hpe:.0f}" fill="{ORANGE}"/>')
        s.append(f'<rect x="{x-bw/2}" y="{BASE-hpe-hot:.0f}" width="{bw}" height="{hot:.0f}" fill="#5B6E96"/>')
        if g > .9:
            s.append(label(f"PE {pe_pct}%", x, BASE - hpe / 2, 36, "#fff", 900))
            s.append(label("주식·채권", x, BASE - hpe - hot / 2, 32, "#fff", 800))
        s.append(f'<g opacity="{ease_out(prog(t, a, .4)):.2f}">' + label(name, x, BASE + 40, 36, "#fff", 900) + '</g>')
    if t > 3.4:
        s.append(f'<g opacity="{ease_out(prog(t, 3.4, .4)):.2f}">' + label("PE는 그대로인데 분모가 줄었다", 780, 760, 36, YELLOW, 900) + '</g>')
    if t > 4.4:
        s.append(f'<g opacity="{ease_out(prog(t, 4.8, .4)):.2f}">' + label("Denominator Effect", 540, 1850, 40, "#fff", 800) + '</g>')
        s.append(punch("분모 효과!", 540, 1700, 140, fill=YELLOW, scale=back(prog(t, 4.4, .45)), rot=-4))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("매수자의 계산서", 540, 150, 104, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("NAV 100 지분을 85에 매수 · 2년 뒤 110 회수 가정", 540, 275, 40, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1100" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    # 미니 J-커브 (EP.01 회상)
    ai = ease_out(prog(t, .5, .5))
    X0, X1, Y0, kk = 110, 520, 560, 2.4
    xs = lambda yr: X0 + (X1 - X0) * yr / 10
    pts = " ".join(f"{'M' if i == 0 else 'L'} {xs(10*i/60):.0f} {Y0 - jcurve(10*i/60)*kk:.0f}" for i in range(61))
    s.append(f'<g opacity="{ai:.2f}"><line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{NAVY}" stroke-width="4"/>'
             f'<path d="{pts}" stroke="{GREY}" stroke-width="9" fill="none" stroke-linecap="round"/>'
             + label("원 LP의 J-커브", (X0 + X1) / 2, 395, 32, "#666", 800) + '</g>')
    am = ease_out(prog(t, 1.2, .6))
    if am > 0:
        n = int(24 + 36 * am)
        seg = " ".join(f"{'M' if i == 24 else 'L'} {xs(10*i/60):.0f} {Y0 - jcurve(10*i/60)*kk:.0f}" for i in range(24, n + 1))
        s.append(f'<path d="{seg}" stroke="{BLUE}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        s.append(f'<circle cx="{xs(4):.0f}" cy="{Y0}" r="14" fill="{BLUE}"/>')
    s.append(chip("여기서 진입 → 바닥은 이미 지남", 780, 500, BLUE, back(prog(t, 1.9, .4)), w=440, size=30))
    # 매수자 현금흐름 타임라인 (0~2년)
    TX0, TX1, B, k = 300, 900, 830, .8
    tx = lambda yr: TX0 + (TX1 - TX0) * yr / 2
    at = ease_out(prog(t, 2.6, .4))
    s.append(f'<g opacity="{at:.2f}"><line x1="{TX0-40}" y1="{B}" x2="{TX1+40}" y2="{B}" stroke="{NAVY}" stroke-width="5"/>'
             + "".join(f'<line x1="{tx(y)}" y1="{B-10}" x2="{tx(y)}" y2="{B+10}" stroke="{NAVY}" stroke-width="4"/>'
                       for y in range(3))
             + label("매수자", 160, B, 40, BLUE, 900) + '</g>')
    g1 = ease_out(prog(t, 3.0, .4))
    s.append(f'<rect x="{tx(0)-32}" y="{B}" width="64" height="{85*k*g1:.0f}" fill="{RED}"/>')
    if g1 > .9: s.append(label("−85", tx(0) + 45, B + 30, 36, RED, 900, "start"))
    ar = ease_out(prog(t, 3.5, .8))
    if ar > 0:
        s.append(f'<line x1="{tx(0)}" y1="{B-28}" x2="{tx(0) + (tx(2)-tx(0))*ar:.0f}" y2="{B-28}" stroke="{BLUE}" stroke-width="6" stroke-dasharray="14 10"/>')
        if ar > .95: s.append(label("2년 보유", tx(1), B - 62, 34, BLUE, 900))
    g2 = ease_out(prog(t, 4.3, .45))
    if g2 > 0:
        h = 110 * k * g2
        s.append(f'<rect x="{tx(2)-32}" y="{B-h:.0f}" width="64" height="{h:.0f}" fill="{GREEN}"/>')
        if g2 > .9: s.append(label("+110", tx(2) - 48, B - h + 20, 36, GREEN, 900, "end"))
    s.append(chip("IRR 13.8% · MOIC 1.29×", 600, 970, BLUE, back(prog(t, 4.9, .4)), w=560, size=40))
    s.append(eq_img(0, 540, 1050, ease_out(prog(t, 5.8, .5))))
    s.append(eq_img(1, 540, 1140, ease_out(prog(t, 6.5, .5))))
    s.append(eq_img(2, 540, 1250, ease_out(prog(t, 7.2, .5))))
    s.append(owl(180, 1720, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(["단, NAV가 몇 달 전 숫자라면", "진짜 할인이 아닐 수도 있어."], 650, 1640, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 8.4, .45)), size=46))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.4 else "worry", flap=prog(t, 3.4, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 할인율 · NAV 기준일 · 미납 약정", 540, 1480, NAVY, back(prog(t, 4.3, .45)), w=860, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["매수자가 또", "떠안는 건요?"], 380, 320, 560, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=54))
    if t > 1.6:
        s.append(bubble(["남은 약정(Unfunded)까지 같이 넘겨받지.", "콜이 오면 이제 매수자가 내는 거야."], 540, 1720, 1010, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=44))
    if t > 3.4:
        s.append(punch("꼼꼼히!", 300, 740, 110, fill="#fff", scale=back(prog(t, 3.4, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(BLUE, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("컨티뉴에이션 펀드", 540, 860, 118, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("GP가 자기 펀드 자산을 산다?", 540, 1080, 58, "#fff", 800) + "</g>")
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
        for i, T in enumerate([2.8, 9.8, 17.5, 30.5, 37.5, 41.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep07_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm07.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep07.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
