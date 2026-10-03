"""EP.08 '컨티뉴에이션 펀드 — GP가 자기 펀드 자산을 산다?' — 9:16 웹툰 숏폼.
GP 주도 세컨더리: 만기 펀드의 핵심 자산 X를 새 펀드(CV)로 이전. 기존 LP는 매각/잔류 선택. 핵심 쟁점은 이전 가격(이해상충)."""
import math, subprocess, sys, os, base64
import cairosvg
from PIL import Image
import render_ep01 as r1
from render_ep01 import (W, H, FPS, NAVY, ORANGE, YELLOW, CREAM, RED, DEFS, OUT,
                         ease_out, back, prog, bg, burst, punch, label, bubble, owl, penguin, panel_frame)
from render_ep05 import chip

GREEN, GREY, MAROON = "#1E7F4F", "#8A94A6", "#8E2C48"
HERE = os.path.dirname(os.path.abspath(__file__))
CUTS = [(0, 4), (4, 10.5), (10.5, 17.5), (17.5, 31), (31, 38), (38, 41.5)]
DUR = 41.5

def _eq(name, s=.5):
    p = os.path.join(HERE, "eq", f"{name}.png"); w, h = Image.open(p).size
    return base64.b64encode(open(p, "rb").read()).decode(), w * s, h * s
EQS = [_eq("ep08_1"), _eq("ep08_2"), _eq("ep08_3")]

def eq_img(i, x, y, a):
    b64, w, h = EQS[i]
    return (f'<g opacity="{a:.2f}" transform="translate(0,{(1-a)*30:.0f})">'
            f'<image x="{x - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" xlink:href="data:image/png;base64,{b64}"/></g>')

def arrow(x1, x2, y, c, p, txt, up=True):
    if p <= 0: return ""
    xe = x1 + (x2 - x1) * p
    d = 1 if x2 > x1 else -1
    head = f'<polygon points="{xe},{y} {xe-d*22},{y-14} {xe-d*22},{y+14}" fill="{c}"/>' if p > .95 else ""
    return (f'<line x1="{x1}" y1="{y}" x2="{xe:.0f}" y2="{y}" stroke="{c}" stroke-width="8"/>{head}'
            + (label(txt, (x1 + x2) / 2, y + (-30 if up else 32), 30, c, 900) if p > .95 else ""))

def cut1(t):
    s = [bg(YELLOW), burst(540, 1000, t)]
    s.append(punch("연기금 IC", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5))))
    s.append(punch("일기", 540, 1000, 330, fill=ORANGE, scale=back(prog(t, .5, .6)), rot=-4))
    tag = ease_out(prog(t, 1.3, .5))
    s.append(f'<g opacity="{tag}" transform="translate(0,{(1-tag)*60})">'
             f'<rect x="150" y="1360" width="780" height="130" rx="26" fill="{NAVY}"/>'
             + label("EP.08 · 컨티뉴에이션 펀드", 540, 1425, 54, "#fff", 800) + '</g>')
    s.append(penguin(300, 1720 + (1 - ease_out(prog(t, 1.8, .7))) * 500, .55, "worry"))
    s.append(owl(790, 1720 + (1 - ease_out(prog(t, 2.0, .7))) * 500, .55, blink=(2.9 < t < 3.05)))
    return s

def cut2(t):
    s = [bg("#F6E4E9")]
    s.append(punch("GP의 선택 통지서", 540, 170, 100, fill=MAROON, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,680) scale({p:.3f})">'
                 f'<rect x="-390" y="-290" width="780" height="580" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-290" width="780" height="100" rx="26" fill="{MAROON}"/><rect x="-390" y="-215" width="780" height="25" fill="{MAROON}"/>'
                 + label("Election Notice", 0, -240, 48, "#fff", 900)
                 + label("① 펀드 I 만기 도래", -340, -120, 40, NAVY, 800, "start")
                 + label("② 핵심 자산 X → 컨티뉴에이션 펀드", -340, -40, 40, NAVY, 800, "start")
                 + label("③ 기존 LP는 둘 중 선택", -340, 40, 40, NAVY, 800, "start")
                 + f'<rect x="-310" y="105" width="270" height="110" rx="18" fill="{GREY}"/>' + label("매각 Sell", -175, 160, 44, "#fff", 900)
                 + f'<rect x="40" y="105" width="270" height="110" rx="18" fill="{GREEN}"/>' + label("잔류 Roll", 175, 160, 44, "#fff", 900)
                 + '</g>')
    inner.append(penguin(540, 1300, .65, "shock" if t > 2.4 else "worry", sweat=prog(t, 2.4, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["GP가 자기 펀드 자산을", "자기가 산대요! 괜찮은 거예요?"], 540, 1700, 920, 230, tail=(-0.3, -1),
                    scale=back(prog(t, 3.0, .45)), size=52))
    return s

def cut3(t):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.4))
    s.append(bubble(["좋은 자산을 더 오래 들고 가려는 거야.", "문제는 가격을 GP가 양쪽에서 정한다는 것."], 540, 330, 1020, 250,
                    tail=(0, 1), scale=back(prog(t, .7, .45)), size=46))
    if t > 3.4:
        s.append(punch("이해상충!", 540, 1650, 180, fill=YELLOW, scale=back(prog(t, 3.4, .45)), rot=-5))
        s.append(f'<g opacity="{ease_out(prog(t, 3.8, .4)):.2f}">' + label("Conflict of Interest", 540, 1800, 42, "#fff", 800) + '</g>')
    return s

def cut4(t):
    s = [bg(CREAM)]
    s.append(punch("누가 누구에게 파나", 540, 150, 100, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label("지분 10% LP · X를 100에 이전 · 3년 뒤 150 가정", 540, 275, 40, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1120" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    # 구조도
    a1 = ease_out(prog(t, .5, .4)); a2 = ease_out(prog(t, .9, .4))
    s.append(f'<g opacity="{a1:.2f}"><rect x="85" y="500" width="320" height="150" rx="20" fill="{GREY}"/>'
             + label("펀드 I", 245, 550, 44, "#fff", 900) + label("기존 LP", 245, 605, 32, "#fff", 800) + '</g>')
    s.append(f'<g opacity="{a2:.2f}"><rect x="675" y="500" width="320" height="150" rx="20" fill="{GREEN}"/>'
             + label("컨티뉴에이션", 835, 545, 40, "#fff", 900) + label("신규 투자자 + 잔류 LP", 835, 605, 28, "#fff", 800) + '</g>')
    s.append(arrow(410, 670, 545, NAVY, ease_out(prog(t, 1.4, .6)), "자산 X"))
    s.append(arrow(670, 410, 610, ORANGE, ease_out(prog(t, 2.0, .6)), "현금 100", up=False))
    ag = back(prog(t, 2.8, .45))
    if ag > 0:
        s.append(f'<g opacity="{min(1,ag):.2f}"><path d="M 470 410 L 260 495 M 610 410 L 820 495" stroke="{RED}" stroke-width="6" stroke-dasharray="12 8"/></g>')
        s.append(f'<g transform="translate(540,405) scale({ag:.3f})"><circle r="52" fill="{RED}"/>' + label("GP", 0, 2, 44, "#fff", 900) + '</g>')
        s.append(f'<g opacity="{ease_out(prog(t, 3.2, .4)):.2f}">' + label("양쪽 모두 GP", 760, 405, 34, RED, 900, "start") + '</g>')
    # 선택 카드
    for x, c, ttl, val, a in [(290, GREY, "매각 Sell", "지금 10 회수", 4.0), (790, GREEN, "잔류 Roll", "3년 뒤 14 (가정)", 4.6)]:
        sc = back(prog(t, a, .4))
        if sc > 0:
            s.append(f'<g transform="translate({x},790) scale({sc:.3f})"><rect x="-215" y="-85" width="430" height="170" rx="22" fill="#fff" stroke="{c}" stroke-width="8"/>'
                     f'<rect x="-215" y="-85" width="430" height="66" rx="22" fill="{c}"/><rect x="-215" y="-40" width="430" height="21" fill="{c}"/>'
                     + label(ttl, 0, -52, 38, "#fff", 900) + label(val, 0, 35, 42, NAVY, 900) + '</g>')
    s.append(eq_img(0, 540, 925, ease_out(prog(t, 5.6, .5))))
    s.append(eq_img(1, 540, 1015, ease_out(prog(t, 6.3, .5))))
    s.append(eq_img(2, 540, 1165, ease_out(prog(t, 7.4, .5))))
    s.append(f'<g opacity="{ease_out(prog(t, 7.0, .4)):.2f}">' + label("잔류: 3년 MOIC 1.4× · IRR 약 11.9% (신규 Carry 20% 차감)", 540, 1115, 32, "#555", 800) + '</g>')
    s.append(f'<g opacity="{ease_out(prog(t, 8.0, .4)):.2f}">' + label("가격을 90으로 낮게 잡으면 매각 LP 몫 1이 사는 쪽으로 이전", 540, 1290, 34, RED, 900) + '</g>')
    s.append(owl(180, 1720, .45, point=True, blink=(11.8 < t < 11.95)))
    s.append(bubble(["그래서 이전 가격이", "이 거래의 전부야."], 650, 1640, 720, 220, tail=(-1.6, 1),
                    scale=back(prog(t, 9.0, .45)), size=50))
    return s

def cut5(t):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 가격 산정 · 선택 기간 · 새 보수 조건", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=880, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 우리는", "뭘 확인해요?"], 380, 320, 560, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=54))
    if t > 1.6:
        s.append(bubble(["경쟁입찰로 정한 가격인지,", "Fairness Opinion·LPAC 승인이 있는지."], 540, 1720, 1000, 230,
                        tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6:
        s.append(punch("체크리스트!", 330, 740, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s

def cut6(t):
    s = [bg(MAROON, "dotsW")]
    s.append(punch("다음 화", 540, 560, 130, fill="#fff", scale=back(prog(t, 0, .45))))
    s.append(punch("2 and 20", 540, 860, 200, fill=YELLOW, scale=back(prog(t, .5, .45)), rot=-3))
    s.append(f'<g opacity="{ease_out(prog(t, 1.0, .5))}">' + label("보수는 실제로 얼마나 떼가나?", 540, 1090, 58, "#fff", 800) + "</g>")
    s.append(penguin(540, 1610 + (1 - ease_out(prog(t, 1.4, .6))) * 400, .7, "worry", sweat=prog(t, 2.0, .4)))
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
        for i, T in enumerate([2.8, 9.8, 17.0, 30.5, 37.5, 41.0]):
            cairosvg.svg2png(bytestring=frame_svg(T).encode(), write_to=f"{OUT}/ep08_still_{i+1}.png")
        sys.exit()
    r1.CUTS, r1.DUR = CUTS, math.ceil(DUR)
    wav = f"{OUT}/bgm08.wav"; r1.make_audio(wav)
    mp4 = f"{OUT}/ic_webtoon_ep08.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS)):
        ff.stdin.write(cairosvg.svg2png(bytestring=frame_svg(f / FPS).encode()))
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("done", mp4)
