# -*- coding: utf-8 -*-
"""W04 프라이머의 그림 — M4 MVO · M5 블랙-리터맨.

팔레트·저장·SVG 도구는 primer_lib 에 모여 있다. 여기에는 이 주차의 그림만 둔다.
숫자는 모두 수업용 예시이며 각 그림에 그렇게 적어 둔다.
"""
import os
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED,
                        BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w04")
_clean, _svg = clean, svg


# ── 아이스크림 가게와 우산 가게 ──────────────────────────────────
def two_shops():
    fig, axes = plt.subplots(1, 3, figsize=WIDE, sharey=True)
    days = ["맑음", "맑음", "비", "맑음", "비", "비", "맑음"]
    ice = np.array([100, 95, 22, 105, 18, 24, 100])
    umb = np.array([30, 40, 108, 25, 116, 106, 39])
    mix = (ice + umb) / 2
    assert ice.sum() == umb.sum() == mix.sum()
    for ax, (v, t, c) in zip(axes, [(ice, "아이스크림 가게만", TEAL),
                                    (umb, "우산 가게만", BLUE),
                                    (mix, "두 가게를 반씩", LIME)]):
        ax.bar(range(7), v, color=c, width=0.64,
               edgecolor=INK if c == LIME else "none", linewidth=1.1)
        ax.axhline(v.mean(), color=INK, lw=1.5, ls="--")
        ax.set_title(f"{t}\n하루 평균 {v.mean():.0f}만원 · 들쭉날쭉 {v.std():.0f}",
                     fontsize=17, color=INK, pad=12)
        ax.set_xticks(range(7)); ax.set_xticklabels(days, fontsize=13)
        ax.tick_params(labelsize=12)
        _clean(ax)
    axes[0].set_ylabel("하루 매출(만원)", fontsize=14)
    fig.tight_layout()
    return save(fig, "two_shops.png", "수업용으로 지어낸 예시입니다")


# ── 평균이 같아도 변동성이 다르다 ────────────────────────────────
def spread():
    rng = np.random.default_rng(4)
    a, b = rng.normal(70, 4, 4000), rng.normal(70, 14, 4000)
    fig, ax = plt.subplots(figsize=WIDE)
    bins = np.linspace(25, 115, 60)
    ax.hist(a, bins=bins, color=TEAL, alpha=.85, label="1반 — 평균 70점, 변동성 4점")
    ax.hist(b, bins=bins, color=AMBER, alpha=.72, label="2반 — 평균 70점, 변동성 14점")
    ax.axvline(70, color=INK, lw=2, ls="--")
    ax.text(71.4, ax.get_ylim()[1] * .94, "두 반의 평균은 똑같이 70점", fontsize=16, color=INK)
    ax.set_xlabel("시험 점수", fontsize=15)
    ax.set_ylabel("학생 수", fontsize=15)
    ax.tick_params(labelsize=13)
    ax.legend(fontsize=15, frameon=False, loc="upper left")
    _clean(ax)
    fig.tight_layout()
    return save(fig, "spread.png", "수업용으로 지어낸 예시입니다")


# ── 상관계수 세 가지 ───────────────────────────────────
def corr3():
    rng = np.random.default_rng(11)
    x = rng.normal(0, 1, 240)
    fig, axes = plt.subplots(1, 3, figsize=WIDE)
    setup = [(+1.0, "+1 · 늘 같이 움직인다", RED, "나눠 담아도 소용없다"),
             (0.0, "0 · 서로 상관없다", MUTED, "이득이 생긴다"),
             (-1.0, "−1 · 늘 반대로 움직인다", TEAL, "이득이 가장 크다")]
    for ax, (r, t, c, sub) in zip(axes, setup):
        y = r * x + np.sqrt(max(0.0, 1 - r * r)) * rng.normal(0, 1, 240)
        ax.scatter(x, y, s=17, color=c, alpha=.65, edgecolors="none")
        ax.set_title(t, fontsize=17, color=c, pad=11)
        ax.set_xlabel(sub, fontsize=15, color=INK)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)
        for sp in ax.spines.values():
            sp.set_color(HAIR)
    fig.suptitle("가로축은 첫째 것의 오르내림, 세로축은 둘째 것의 오르내림",
                 fontsize=16, color=MUTED, y=1.02)
    fig.tight_layout()
    return save(fig, "corr3.png", "수업용으로 지어낸 예시입니다")


# ── 섞으면 얌전해진다 ────────────────────────────────────────────
def mix_smooth():
    rng = np.random.default_rng(3)
    n = 60
    t = np.arange(n)
    z = rng.normal(0, 1, n)
    ra = 0.6 + 2.6 * (z + rng.normal(0, .5, n))
    rb = 0.6 + 2.6 * (-z + rng.normal(0, .5, n))
    rm = (ra + rb) / 2
    a, b, mix = (100 + np.cumsum(r) for r in (ra, rb, rm))
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(t, a, color=BLUE, lw=2.0, alpha=.9, label=f"가 자산만 — 매달 {ra.std():.1f}씩 출렁")
    ax.plot(t, b, color=AMBER, lw=2.0, alpha=.9, label=f"나 자산만 — 매달 {rb.std():.1f}씩 출렁")
    ax.plot(t, mix, color=TEAL, lw=4.2, label=f"반씩 섞으면 — 매달 {rm.std():.1f}씩만 출렁")
    ax.set_xlabel("시간(개월)", fontsize=15)
    ax.set_ylabel("자산 값", fontsize=15)
    ax.tick_params(labelsize=13)
    ax.legend(fontsize=16, frameon=False, loc="upper left")
    _clean(ax)
    fig.tight_layout()
    return save(fig, "mix_smooth.png", "수업용으로 지어낸 예시입니다")


# ── ρ만 바꾸면 ───────────────────────────────────────────────────
def rho_effect():
    s1, s2 = 0.20, 0.10
    rho = np.linspace(-1, 1, 400)
    sig = np.sqrt(.25 * s1**2 + .25 * s2**2 + 2 * .25 * rho * s1 * s2)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(rho, sig * 100, color=TEAL, lw=4)
    marks = [(-1, LIME, "ρ = −1\n5.0%", (20, 18), "left"),
             (0, BLUE, "ρ = 0\n11.2%", (0, -58), "center"),
             (1, RED, "ρ = +1\n15.0%", (-18, -58), "right")]
    for r, c, lab, off, ha in marks:
        v = np.sqrt(.25 * s1**2 + .25 * s2**2 + 2 * .25 * r * s1 * s2) * 100
        ax.scatter([r], [v], s=170, color=c, zorder=5,
                   edgecolors=INK if c == LIME else "none", linewidth=1.4)
        ax.annotate(lab, (r, v), textcoords="offset points", xytext=off, ha=ha,
                    fontsize=16, color=INK if c == LIME else c, fontweight="bold")
    ax.axhline(15, color=MUTED, lw=1.2, ls=":")
    ax.text(-0.98, 17.3, "그냥 반씩 더하면 15.0% — 곡선이 그 아래로 내려간 만큼이 나눠 담기의 이득",
            fontsize=15, color=MUTED)
    ax.set_xlabel("상관계수  ρ", fontsize=15)
    ax.set_ylabel("섞은 뒤 변동성(%)", fontsize=15)
    ax.set_ylim(0, 19.5)
    ax.tick_params(labelsize=13)
    _clean(ax)
    fig.tight_layout()
    return save(fig, "rho_effect.png", "변동성 20%와 10%인 두 자산을 반씩 담았을 때")


# ── 효율적 투자선 ────────────────────────────────────────────────
def frontier():
    m1, s1, m2, s2, rho = .08, .20, .04, .10, .20
    w = np.linspace(0, 1, 400)
    mu = w * m1 + (1 - w) * m2
    sg = np.sqrt(w**2 * s1**2 + (1 - w)**2 * s2**2 + 2 * w * (1 - w) * rho * s1 * s2)
    k = sg.argmin()
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(sg[k:] * 100, mu[k:] * 100, color=TEAL, lw=4.4, zorder=3,
            label="여기서 고른다 — 같은 변동성이면 더 버는 쪽")
    ax.plot(sg[:k + 1] * 100, mu[:k + 1] * 100, color=HAIR, lw=3.6, ls="--", zorder=2,
            label="여기는 고를 이유가 없다 — 더 흔들리는데 덜 번다")
    for xv, yv, c, lab, off, ha in [(s1, m1, BLUE, "가 자산만 100%", (-16, 10), "right"),
                                    (s2, m2, AMBER, "나 자산만 100%", (14, -8), "left")]:
        ax.scatter([xv * 100], [yv * 100], s=150, color=c, zorder=5)
        ax.annotate(lab, (xv * 100, yv * 100), xytext=off, textcoords="offset points",
                    fontsize=16, color=c, ha=ha)
    ax.scatter([sg[k] * 100], [mu[k] * 100], s=420, color=LIME, marker="*", zorder=6,
               edgecolors=INK, linewidth=1.2)
    ax.annotate("가장 덜 흔들리는 조합", (sg[k] * 100, mu[k] * 100), xytext=(18, 14),
                textcoords="offset points", fontsize=16, color=INK, fontweight="bold")
    ax.set_xlabel("변동성(%)  →  오른쪽일수록 불안하다", fontsize=15)
    ax.set_ylabel("앞으로 벌 것으로 보는 수익(%)", fontsize=15)
    ax.legend(fontsize=15, frameon=False, loc="lower right")
    ax.set_xlim(7, 22)
    ax.tick_params(labelsize=13)
    _clean(ax, grid="both")
    fig.tight_layout()
    return save(fig, "frontier.png", "수업용으로 지어낸 예시입니다")


# ── 입력을 1%p 바꾸면 ────────────────────────────────────────────
def unstable():
    sd = np.array([.18, .19, .20])
    C3 = np.array([[1, .90, .88], [.90, 1, .92], [.88, .92, 1]])
    S = np.outer(sd, sd) * C3
    g = np.arange(0, 1.001, .01)
    grid = np.array([(a, b, 1 - a - b) for a in g for b in g if a + b <= 1.0000001])

    def best(mu):
        ret = grid @ mu
        vol = np.sqrt(np.einsum("ij,jk,ik->i", grid, S, grid))
        return grid[((ret - .02) / vol).argmax()]

    base = np.array([.060, .065, .070])
    a, b = best(base), best(base + np.array([.00, .01, .00]))
    fig, ax = plt.subplots(figsize=WIDE)
    idx = np.arange(3)
    ax.bar(idx - .19, a * 100, .38, color=BLUE, label="처음 생각한 수익률로 풀었을 때")
    ax.bar(idx + .19, b * 100, .38, color=RED, label="나 자산만 1%p 올려 다시 풀었을 때")
    for i in idx:
        for v, off in ((a[i] * 100, -.19), (b[i] * 100, .19)):
            ax.annotate(f"{v:.0f}%", (i + off, v), ha="center", va="bottom",
                        xytext=(0, 6), textcoords="offset points",
                        fontsize=16, color=INK, fontweight="bold")
    ax.set_xticks(idx)
    ax.set_xticklabels(["가 자산", "나 자산", "다 자산"], fontsize=17)
    ax.set_ylabel("담으라고 나온 비중(%)", fontsize=15)
    ax.set_ylim(0, 122)
    ax.tick_params(labelsize=13)
    ax.legend(fontsize=15, frameon=False, loc="upper left")
    _clean(ax)
    fig.tight_layout()
    return save(fig, "unstable.png", "서로 비슷하게 움직이는 자산 셋 · 예상 수익률만 1%p 바꿨습니다")


# ── 확신의 크기만큼 ──────────────────────────────────────────────
def confidence():
    c = np.linspace(0, 1, 300)
    mkt, view = 30.0, 70.0
    w = mkt + (view - mkt) * c
    fig, ax = plt.subplots(figsize=WIDE)
    ax.plot(c * 100, w, color=TEAL, lw=4.4)
    ax.axhline(mkt, color=BLUE, lw=2, ls="--")
    ax.axhline(view, color=AMBER, lw=2, ls="--")
    ax.text(99, mkt - 4.2, "시장이 이미 매긴 값 30%", fontsize=16, color=BLUE, ha="right")
    ax.text(1, view + 2.4, "내 생각대로라면 70%", fontsize=16, color=AMBER)
    for cc, lab, off, ha, va in [(0.15, "확신이 약하면\n시장 쪽에 가깝다", (-14, 14), "right", "bottom"),
                                 (0.85, "확신이 강하면\n내 생각 쪽으로", (14, -12), "left", "top")]:
        v = mkt + (view - mkt) * cc
        ax.scatter([cc * 100], [v], s=170, color=LIME, zorder=5,
                   edgecolors=INK, linewidth=1.4)
        ax.annotate(lab, (cc * 100, v), xytext=off, textcoords="offset points",
                    ha=ha, va=va, fontsize=15.5, color=INK)
    ax.set_xlabel("내 생각에 대한 확신(%)", fontsize=15)
    ax.set_ylabel("최종으로 담는 비중(%)", fontsize=15)
    ax.set_ylim(16, 82); ax.set_xlim(-4, 112)
    ax.tick_params(labelsize=13)
    _clean(ax)
    fig.tight_layout()
    return save(fig, "confidence.png", "확신의 정도를 0에서 100으로 놓고 그린 그림입니다")


# ── 수식 (Computer Modern) ───────────────────────────────────────
def equation():
    """pdflatex이 이 환경에 없어 matplotlib mathtext의 Computer Modern으로 굽는다.
    글자꼴은 LaTeX 기본과 같은 CM이다. 배경은 카드 색(PAPER)을 구워 넣는다 — §7.5."""
    fig = plt.figure(figsize=(11.4, 1.9), facecolor=PAPER)
    fig.text(.5, .5,
             r"$\sigma_p^{\,2}\;=\;w_1^{2}\sigma_1^{2}\;+\;w_2^{2}\sigma_2^{2}"
             r"\;+\;2\,w_1w_2\,\rho\,\sigma_1\sigma_2$",
             ha="center", va="center", fontsize=42, color=INK)
    p = os.path.join(OUT, "equation.png")
    fig.savefig(p, bbox_inches="tight", facecolor=PAPER, pad_inches=0.26)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(p).size
    print(f"   equation.png  {w}x{h}  ratio={w/h:.3f}")
    return p


# ── SVG 개념 도해 (ZeroOne 팔레트) ───────────────────────────────
def _svg(name, body, w, h):
    import cairosvg
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{PAPER}"/>'
           f'<style>text{{font-family:"Noto Sans CJK KR","Noto Sans CJK JP",sans-serif}}</style>'
           f'{body}</svg>')
    p = os.path.join(OUT, name)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=p, output_width=w * 2)
    print(f"   {name}  {w*2}x{int(h*2)}  ratio={w/h:.3f}")
    return p


def _box(x, y, w, h, fill, stroke, title, sub, tc, sc):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="2"/>'
         f'<text x="{x+w/2}" y="{y+46}" font-size="34" font-weight="700" fill="{tc}" '
         f'text-anchor="middle">{title}</text>')
    for i, ln in enumerate(sub):
        s += (f'<text x="{x+w/2}" y="{y+86+i*34}" font-size="26" fill="{sc}" '
              f'text-anchor="middle">{ln}</text>')
    return s


def bl_flow():
    W, H = 1600, 620
    b = ('<defs>'
         f'<marker id="ar" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">'
         f'<path d="M0,0 L9,4 L0,8 z" fill="{RED}"/></marker>'
         f'<marker id="ag" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">'
         f'<path d="M0,0 L9,4 L0,8 z" fill="{TEAL}"/></marker></defs>')
    b += f'<text x="60" y="88" font-size="30" font-weight="700" fill="{RED}">M4 · 지금까지 방식</text>'
    b += _box(430, 40, 380, 150, WHITE, HAIR, "예상 수익률", ["“가는 8%, 나는 4%”"], INK, MUTED)
    b += _box(1010, 40, 380, 150, WHITE, HAIR, "담을 비중", ["계산해서 나온 답"], INK, MUTED)
    b += f'<line x1="826" y1="115" x2="994" y2="115" stroke="{RED}" stroke-width="5" marker-end="url(#ar)"/>'
    b += f'<text x="910" y="98" font-size="26" fill="{RED}" text-anchor="middle">넣는다</text>'
    b += f'<text x="910" y="238" font-size="27" fill="{MUTED}" text-anchor="middle">왼쪽을 조금만 바꿔도 오른쪽이 확 뒤집힌다</text>'
    b += f'<line x1="60" y1="300" x2="1540" y2="300" stroke="{HAIR}" stroke-width="2"/>'
    b += f'<text x="60" y="400" font-size="30" font-weight="700" fill="{TEAL}">M5 · 블랙-리터맨</text>'
    b += _box(430, 352, 380, 150, WHITE, HAIR, "지금 시장 비중", ["누구나 볼 수 있는 값"], INK, MUTED)
    b += _box(1010, 352, 380, 150, LIME, INK, "시장이 매긴 수익률", ["여기에 내 생각을 섞는다"], DARK, DARK)
    b += f'<line x1="826" y1="427" x2="994" y2="427" stroke="{TEAL}" stroke-width="5" marker-end="url(#ag)"/>'
    b += f'<text x="910" y="410" font-size="26" fill="{TEAL}" text-anchor="middle">꺼낸다</text>'
    b += f'<text x="910" y="550" font-size="27" fill="{MUTED}" text-anchor="middle">출발점이 흔들리지 않으니 답도 얌전하다</text>'
    return _svg("bl_flow.png", b, W, H)


if __name__ == "__main__":
    print("ZeroOne 팔레트로 그림을 만듭니다 →", OUT)
    two_shops(); spread(); corr3(); mix_smooth(); rho_effect()
    frontier(); unstable(); confidence(); equation(); bl_flow()
    print("끝.")
