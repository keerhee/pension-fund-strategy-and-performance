"""EP.02 '캐피털 콜 폭탄' — 9:16 웹툰 숏폼. 공통 부품(캐릭터·말풍선·타이포)은 render_ep01에서 가져온다."""
import math, subprocess, sys, os
import cairosvg
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)

GREEN = "#1E7F4F"
CUTS = [(0, 4), (4, 10), (10, 15), (15, 24), (24, 29.5), (29.5, 33)]
DUR = 33

# 약정액 대비 % — 연차별 납입(콜)·분배 (설명용 예시 수치)
CALLS = [20, 25, 20, 15, 8, 4, 2, 0, 0, 0]
DISTS = [0, 0, 2, 8, 18, 25, 30, 28, 20, 12]

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="200" y="1360" width="680" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.02 · 캐피털 콜 폭탄", 540, 1425, 56, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "shock", sweat=prog(t, 2.6, .4)))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def notice(y, gp, line, sc, x_off):
    return (f'<g transform="translate({x_off},0)"><g transform="translate(540,{y}) scale({sc})">'
            f'<rect x="-400" y="-95" width="800" height="190" rx="28" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
            f'<rect x="-370" y="-55" width="120" height="90" rx="10" fill="{ORANGE}" stroke="{NAVY}" stroke-width="6"/>'
            f'<polyline points="-370,-55 -310,-5 -250,-55" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/>'
            + label(f"Capital Call · {gp}", -210, -30, 44, NAVY, 900, "start")
            + label(line, -210, 35, 38, "#444", 700, "start") + '</g></g>')

def cut2(t):
    s = [bg("#FBE3CF")]
    s.append(punch("월요일 아침 9시", 540, 170, 96, fill=ORANGE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    items = [(470, "GP A", "약정액의 15% · 10영업일 내 납입", .5),
             (690, "GP B", "약정액의 10% · 신규 딜 클로징", 1.2),
             (910, "GP C", "약정액의 12% · 추가 출자 요청", 1.9)]
    for y, gp, line, a in items:
        p = prog(t, a, .35)
        if p > 0:
            inner.append(notice(y, gp, line, 1.0, (1 - ease_out(p)) * 900))
            pp = prog(t, a + .2, .35)
            if 0 < pp and t < a + 1.3:
                inner.append(punch("띵!", 900, y - 95, 80, fill=YELLOW, scale=back(pp), rot=12))
    inner.append(penguin(540, 1260, .8, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .5), flap=prog(t, 2.3, .8) if t < 3.1 else 0))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["부장님! 펀드 세 곳에서", "동시에 돈을 달래요!!"], 540, 1700, 900, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.1, .45)), size=56))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 2.4))
    s.append(bubble(["약정(Commitment)한 돈을", "GP가 투자할 때마다 나눠 부르는 거야."], 540, 330, 1000, 250, tail=(0, 1),
                    scale=back(prog(t, .7, .45)), size=50))
    if t > 2.4:
        s.append(punch("예정된 일!", 540, 1650, 190, fill=YELLOW, scale=back(prog(t, 2.4, .45)), rot=-5))
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("돈은 이렇게 오간다", 540, 150, 100, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("약정액 100 기준 · 연차별 현금흐름 (예시)", 540, 280, 44, NAVY, 700) + "</g>")
    s.append(f'<rect x="60" y="350" width="960" height="1090" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    X0, X1, Y0, k = 140, 990, 850, 6.5
    xs = lambda yr: X0 + (X1 - X0) * (yr + .5) / 10
    s.append(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{NAVY}" stroke-width="5"/>')
    for yr in range(10):
        s.append(label(str(yr + 1), xs(yr), 1345, 34, "#555", 700))
    s.append(label("연차", X1, 1395, 32, "#555", 700, "end"))
    # 범례
    for i, (c, txt) in enumerate([(RED, "콜 (납입)"), (GREEN, "분배"), (NAVY, "누적 순현금")]):
        lx = 130 + i * 300
        s.append(f'<rect x="{lx}" y="385" width="40" height="30" rx="6" fill="{c}"/>' + label(txt, lx + 55, 400, 34, NAVY, 800, "start"))
    bw = 54
    cum, pts = 0, []
    for yr in range(10):
        g = ease_out(prog(t, .8 + yr * .38, .45))
        if g <= 0: break
        hc, hd = CALLS[yr] * k * g, DISTS[yr] * k * g
        s.append(f'<rect x="{xs(yr)-bw/2-14}" y="{Y0}" width="{bw}" height="{hc:.1f}" fill="{RED}"/>')
        if hd > 0:
            s.append(f'<rect x="{xs(yr)-bw/2+14}" y="{Y0-hd:.1f}" width="{bw}" height="{hd:.1f}" fill="{GREEN}"/>')
        cum += (DISTS[yr] - CALLS[yr]) * g
        pts.append((xs(yr), Y0 - cum * k))
    if len(pts) > 1:
        d = " ".join(f"{'M' if i == 0 else 'L'} {x:.0f} {y:.0f}" for i, (x, y) in enumerate(pts))
        s.append(f'<path d="{d}" stroke="{NAVY}" stroke-width="10" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
        s.append(f'<circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="15" fill="{NAVY}"/>')
    notes = [(2.6, "① 초기 3~5년: 콜 집중", 790, 1250, RED),
             (4.6, "② 4년차부터 분배", 430, 560, GREEN)]
    for a, txt, x, y, c in notes:
        sc = back(prog(t, a, .4))
        if sc > 0:
            s.append(f'<g transform="translate({x},{y}) scale({sc})"><rect x="-210" y="-42" width="420" height="84" rx="20" fill="{c}"/>'
                     + label(txt, 0, 0, 38, "#fff", 800) + "</g>")
    s.append(owl(180, 1700, .5, point=True, blink=(6.6 < t < 6.75)))
    s.append(bubble(["미납 약정(Unfunded)만큼", "현금을 늘 준비해 둬야 해."], 640, 1610, 760, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 6.0, .45)), size=48))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1150, .9, "happy" if t > 3.0 else "worry", flap=prog(t, 3.0, 1.2))
    inner += owl(780, 1180, .78, blink=(1.2 < t < 1.35))
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 현금을 전부", "쌓아둬야 하나요?"], 400, 320, 680, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=50))
    if t > 1.6:
        s.append(bubble(["그건 비효율이지. 오버커밋먼트와", "유동성 버퍼로 맞추는 거야."], 540, 1720, 980, 230, tail=(0.5, -1),
                        scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.0:
        s.append(punch("아하!", 230, 760, 120, fill="#fff", scale=back(prog(t, 3.0, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(GREEN)]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("분배금이 왔다!", 540, 860, 150, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(punch("DPI vs TVPI", 540, 1100, 150, fill="#fff", scale=back(prog(t, .9, .45)), rot=3))
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "happy", flap=prog(t, 1.6, 1.2)))
    return s

FUNCS = [cut1, cut2, cut3, cut4, cut5, cut6]

def frame_svg(T):
    for i, (a, b) in enumerate(CUTS):
        if a <= T < b or (i == len(CUTS) - 1 and T >= a):
            t = T - a
            body = "".join(FUNCS[i](t))
            fl = 1 - prog(t, 0, .18) if i > 0 else 0
            if fl > 0: body += f'<rect width="{W}" height="{H}" fill="#fff" opacity="{fl:.2f}"/>'
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{DEFS}{body}</svg>'

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for i, T in enumerate([2.8, 8.6, 13.4, 23.0, 28.6, 32.4]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep02_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm02.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep02.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
