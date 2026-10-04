"""PE 시즌 1 공통 컷(EP.18~): 문제(문서 카드) · 반전 · 해설 카드 틀 · 후속 질문.
EP.12~17에서 회차마다 복사하던 같은 배치를 함수로 묶었다. 회차 파일은 cut4만 직접 그린다."""
from webtoon_lib import *


def problem_cut(t, bgc, title, title_c, head, head_c, line, left, right, sfx, bubble_lines,
                title_size=110, line_c=NAVY, sfx_size=84, mood="happy", bubble_size=54, bubble_w=900):
    """left/right = (라벨, 값, 색, 글자크기)."""
    s = [bg(bgc)]
    s.append(punch(title, 540, 170, title_size, fill=title_c, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    p = back(prog(t, .4, .5))
    (ll, lv, lc, ls), (rl, rv, rc, rs) = left, right
    inner.append(f'<g transform="translate(540,640) scale({p:.3f})">'
                 f'<rect x="-390" y="-250" width="780" height="500" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="9"/>'
                 f'<rect x="-390" y="-250" width="780" height="96" rx="26" fill="{head_c}"/><rect x="-390" y="-180" width="780" height="26" fill="{head_c}"/>'
                 + label(head, 0, -202, 40, "#fff", 900)
                 + label(line, 0, -90, 42, line_c, 900)
                 + label(ll, -170, 10, 38, "#555", 800) + punch(lv, -170, 90, ls, fill=lc)
                 + label(rl, 170, 10, 38, "#555", 800) + punch(rv, 170, 90, rs, fill=rc)
                 + '</g>')
    if t > 2.0:
        inner.append(punch(sfx, 760, 965, sfx_size, fill=YELLOW, scale=back(prog(t, 2.0, .35)), rot=12))
    if mood == "happy":
        inner.append(penguin(540, 1290, .7, "happy" if t > 2.3 else "worry", flap=prog(t, 2.3, 1.0)))
    else:
        inner.append(penguin(540, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(bubble_lines, 540, 1700, bubble_w, 230, tail=(-0.3, -1), scale=back(prog(t, 3.1, .45)), size=bubble_size))
    return s


def twist_cut(t, lines, sfx, size=46, sfx_size=150):
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.2))
    s.append(bubble(lines, 540, 330, 1010, 250, tail=(0, 1), scale=back(prog(t, .7, .45)), size=size))
    if t > 3.2:
        s.append(punch(sfx, 540, 1650, sfx_size, fill=YELLOW, scale=back(prog(t, 3.2, .45)), rot=-5))
    return s


def explain_frame(t, title, sub, title_size=100):
    s = [bg(CREAM)]
    s.append(punch(title, 540, 150, title_size, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t, .3, .5))}">' + label(sub, 540, 275, 36, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1250" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    return s


def explain_tail(t, eqs, ys, a0, summary, sum_y, sum_a, bubble_lines, bub_a, sum_size=42, eq_scale=.47):
    s = []
    for i, (p, y) in enumerate(zip(eqs, ys)):
        s.append(eq_img(p, 540, y, ease_out(prog(t, a0 + .7 * i, .5)), scale=eq_scale))
    s.append(f'<g opacity="{ease_out(prog(t, sum_a, .5))}">' + label(summary, 540, sum_y, sum_size, RED, 900) + "</g>")
    s.append(owl(180, 1745, .45, point=True, blink=(11.5 < t < 11.65)))
    s.append(bubble(bubble_lines, 650, 1710, 760, 220, tail=(-1.6, 1), scale=back(prog(t, bub_a, .45)), size=46))
    return s


def relief_cut(t, q, a, sfx, chip_txt, q_size=52, a_size=46, chip_size=33, mood="happy", sfx_size=100):
    s = [bg("#CFE6F2")]
    if mood == "happy":
        inner = penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    else:
        inner = penguin(310, 1120, .85, "shock" if t > 3.6 else "worry", sweat=prog(t, 3.6, .4))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip(chip_txt, 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=930, size=chip_size)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(q, 400, 320, 640, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=q_size))
    if t > 1.6:
        s.append(bubble(a, 540, 1720, 1010, 230, tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=a_size))
    if t > 3.6:
        s.append(punch(sfx, 330, 740, sfx_size, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s


def vbar(t, a0, x, v, k, base, c, top, bottom=(), w=200, top_size=40, inside=None):
    """세로 막대(EP.26~): 값 v × k px. top은 막대 위 라벨, bottom은 기준선 아래 줄들, inside는 막대 안 흰 글자."""
    g = ease_out(prog(t, a0, .5))
    if g <= 0: return ""
    h = v * k * g
    o = [f'<rect x="{x-w/2}" y="{base-h:.0f}" width="{w}" height="{h:.0f}" fill="{c}" rx="6"/>']
    if g > .9:
        if top: o.append(label(top, x, base - h - 28, top_size, c, 900))
        if inside: o.append(label(inside, x, base - h / 2, 34, "#fff", 900))
        for i, line in enumerate(bottom):
            o.append(label(line, x, base + 40 + 36 * i, 32 if i == 0 else 28, NAVY, 900 if i == 0 else 800))
    return "".join(o)


def baseline(t, y, x1=100, x2=980):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{NAVY}" stroke-width="5" opacity="{ease_out(prog(t, .4, .4)):.2f}"/>'
