"""시즌 3 공통 컷 — 타이틀 · 문제(카드) · 반전 · 후속 · 예고 + 대본 JSON 저장.
회차 스크립트는 META(대본 · fact-check)와 cut4(해설)만 직접 짠다."""
import json, os, sys
from webtoon_lib import *

SEASON = "시즌 3 · 시간은 답을 바꾼다"
CUTS = [(0, 4), (4, 10.5), (10.5, 17), (17, 31), (31, 38), (38, 41.5)]
DUR = 41.5
STILLS = [2.8, 9.9, 16.5, 30.5, 37.5, 41.0]


def title(t, ep_label, chip_w=860):
    s = title_cut(t, ep_label, chip_w=chip_w)
    s.insert(2, punch(SEASON, 540, 330, 58, fill="#fff", scale=back(prog(t, 0, .45)), sw=8))
    return s


def problem(t, head, head_c, bgc, card_title, body, bubble_lines, sfx, mood_after="worry", bubble_size=50):
    """body: 카드 안 SVG 조각(카드 중심 기준 좌표, 폭 ±390 · 높이 −150~+250)."""
    s = [bg(bgc)]
    s.append(punch(head, 540, 170, 110, fill=head_c, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{head_c}"/><rect x="-390" y="-180" width="780" height="26" fill="{head_c}"/>'
                 + label(card_title, 0, -202, 40, "#fff", 900) + body + '</g>')
    if t > 2.0:
        inner.append(punch(sfx, 770, 975, 76, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=10))
    mood = "happy" if t < 2.6 else mood_after
    inner.append(penguin(380, 1290, .7, mood, sweat=prog(t, 2.6, .4) if mood_after == "shock" else 0))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(bubble_lines, 540, 1700, 940, 230, tail=(-0.3, -1), scale=back(prog(t, 3.1, .45)), size=bubble_size))
    return s


def twist(t, lines, sfx, size=46, sfx_size=130):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(lines, 540, 330, 1030, 250, tail=(0, 1), scale=back(prog(t, .7, .45)), size=size))
    if t > 3.2:
        s.append(punch(sfx, 540, 1650, sfx_size, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


def explainer_frame(t, head, sub, head_size=104):
    return [bg(CREAM), punch(head, 540, 150, head_size, fill=ORANGE, scale=back(prog(t, 0, .45))),
            f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label(sub, 540, 275, 34, NAVY, 700) + "</g>",
            f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>']


def explainer_tail(t, red, sub, owl_lines, a0=8.0, red_size=48, owl_size=44):
    s = [f'<g opacity="{ease_out(prog(t, a0, .5))}">' + label(red, 540, 1410, red_size, RED, 900) + "</g>",
         f'<g opacity="{ease_out(prog(t, a0 + .4, .5))}">' + label(sub, 540, 1490, 34, NAVY, 800) + "</g>",
         owl(180, 1745, .45, point=True, blink=(12.5 < t < 12.65)),
         bubble(owl_lines, 650, 1710, 760, 220, tail=(-1.6, 1), scale=back(prog(t, a0 + 1.4, .45)), size=owl_size)]
    return s


def relief(t, q, a, sfx, chip_txt, happy=False, a_size=44, chip_size=34, sfx_size=100):
    s = [bg("#CFE6F2")]
    inner = penguin(310, 1120, .85, ("happy" if happy else "shock") if t > 3.6 else "worry", sweat=0 if happy else prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip(chip_txt, 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=940, size=chip_size)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(q, 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=48))
    if t > 1.6:
        s.append(bubble(a, 540, 1720, 1020, 230, tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=a_size))
    if t > 3.6:
        s.append(punch(sfx, 540, 740, sfx_size, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-6))
    return s


def eqs(t, files, ys, a0=5.0, scale=.48):
    sc = scale if isinstance(scale, (list, tuple)) else [scale] * len(files)
    return [eq_img(f, 540, y, ease_out(prog(t, a0 + .8 * i, .5)), scale=s_) for i, (f, y, s_) in enumerate(zip(files, ys, sc))]


def main(funcs, ep, meta):
    out = f"../output/ic_webtoon_s3_ep{ep}.mp4"
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        js = f"../episodes/ep{ep}_script.json"
        meta = dict(season="시즌 3 「시간은 답을 바꾼다」 (W07 동적 포트폴리오 · SS2 리밸런싱)", **meta)
        json.dump(meta, open(js, "w"), ensure_ascii=False, indent=1)
    run(funcs, CUTS, DUR, out, STILLS)


def table(t, a0, cols, xs, header, rows, y0=395, dy=64, size=27, head_size=26):
    """rows: [(cells, colors)] — 셀마다 색. 머리행은 NAVY."""
    o = [f'<g opacity="{ease_out(prog(t, a0, .4)):.2f}">' + "".join(label(h, x, y0, head_size, NAVY, 900) for h, x in zip(header, xs))
         + f'<line x1="80" y1="{y0+28}" x2="1000" y2="{y0+28}" stroke="{NAVY}" stroke-width="3"/></g>']
    for r, (cells, colors) in enumerate(rows):
        y = y0 + 28 + dy * (r + .75)
        g = ease_out(prog(t, a0 + .4 + .55 * r, .4))
        o.append(f'<g opacity="{g:.2f}">' + "".join(label(c, x, y, size, col, 900) for c, x, col in zip(cells, xs, colors)) + "</g>")
    return "".join(o)
