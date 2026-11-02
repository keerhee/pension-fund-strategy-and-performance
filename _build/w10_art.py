# -*- coding: utf-8 -*-
"""W10 프라이머의 그림 — M11 주식 퀀트 투자.

zeroone-pitch-deck v1.11 규칙으로 다시 그린 판(2026-11-02).
 · matplotlib 차트는 스킬의 zo_mpl로 그린다 — Medium 글꼴, 글씨 14pt 하한, 계열색 글씨 금지,
   막대 안 글씨는 ink_on(), 저장 직전 검사 경고 0건(strict).
 · 차트는 슬라이드 표시 크기(약 10.0 × 3.85in)로 그린다 — 크게 그려 줄이면 글씨가 작아진다.
 · SVG 도해는 1600×600, 글씨 30px 이상, 보조 글씨 #4A5A60 · font-weight 500 이상(§7.1·§7.2).
 · 수식 PNG는 흰 카드에 얹으므로 흰 배경 + 잉크색(v1.10).
"""
import os
import sys
import numpy as np

ZO = os.environ.get("ZO_SCRIPTS", os.path.expanduser(
    "~/.claude/skills/synced/6a672863-e83f-481a-b0f5-8d9879345faa_528c1cd5-61c9-4543-927c-27df014bc8b9/"
    "zeroone-pitch-deck/scripts"))
sys.path.insert(0, ZO)
import zo_mpl  # noqa: E402
from zo_mpl import fig, save, note, ink_on, C  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_art", "w10")
os.makedirs(OUT, exist_ok=True)
EX = "※ 수업용으로 지어낸 예시입니다"

# 팔레트 (룰북 §1.1 · v1.11)
INK, BODY, SUB, MUTED = C["ink"], C["body"], C["sub"], "#4A5A60"
TEAL, RED, LIME, BLUE, AMBER = C["teal"], C["red"], C["lime"], C["blue"], C["amber"]
PAPER, WHITE, HAIR, GREYBAR = C["paper"], C["white"], C["hair"], "#8A979C"

SIZE = (10.0, 3.85, 16)          # 슬라이드 표시 크기(in)와 기본 글씨(pt)


def P(name):
    return os.path.join(OUT, name)


def bar_grid(ax):
    """막대 차트는 세로 격자선을 끈다(§7.4)."""
    ax.grid(False, axis="x")
    ax.grid(True, axis="y")


# ══ matplotlib 차트 ══════════════════════════════════════════════

def quantile():
    """막대(해마다 번 몫)와 선(쌓인 값)이 같은 숫자에서 나오게 한다 — v1.11 p5 사고 방지."""
    ann = np.linspace(-.120, .144, 5)                 # 다섯 등급의 연 수익: −12.0 … +14.4%
    f, axes = fig(size=SIZE, ncols=2, gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axes[0]
    cols = [RED, AMBER, GREYBAR, BLUE, TEAL]
    bars = ax.bar(range(5), ann * 100, color=cols, width=.62)
    zo_mpl.val_label(ax, bars, fmt="{:+.1f}%", size=16)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xticks(range(5))
    ax.set_xticklabels(["1등급\n낮은 점수", "2", "3", "4", "5등급\n높은 점수"], fontsize=15)
    ax.set_ylabel("해마다 번 몫(%)", fontsize=16)
    ax.set_ylim(-20, 20)
    ax.set_title("점수 순으로 다섯 무리를 만들면", fontsize=17, fontweight="bold", color=INK, pad=10)
    bar_grid(ax)

    ax = axes[1]
    rng = np.random.default_rng(4)
    n = 60
    t = np.arange(n + 1) / 12
    for mu, c, lab in [(ann[-1], TEAL, "높은 점수 무리"), (ann[0], RED, "낮은 점수 무리")]:
        z = rng.normal(0, .028, n)
        r = (1 + mu) ** (1 / 12) - 1 + (z - z.mean())   # 잡음은 평균 0 — 끝값이 막대와 맞는다
        v = 100 * np.concatenate([[1], np.cumprod(1 + r)])
        ax.plot(t, v, color=c, lw=3.4, label=lab)
    ax.axhline(100, color=GREYBAR, lw=1.2, ls=":")
    ax.set_xlabel("햇수", fontsize=16)
    ax.set_ylabel("100으로 시작한 값", fontsize=16)
    ax.legend(loc="upper left", fontsize=16)
    ax.set_title("두 무리를 5년 들고 있으면", fontsize=17, fontweight="bold", color=INK, pad=10)
    note(f, EX)
    return save(f, P("quantile.png"), strict=True)


def overfit():
    rng = np.random.default_rng(11)
    n = 96
    t = np.arange(n) / 12
    r = np.concatenate([rng.normal(.016, .022, n // 2), rng.normal(.001, .030, n // 2)])
    v = 100 * np.cumprod(1 + r)
    f, ax = fig(size=SIZE)
    ax.plot(t[:n // 2], v[:n // 2], color=TEAL, lw=3.8, label="규칙을 만들 때 쓴 기간")
    ax.plot(t[n // 2 - 1:], v[n // 2 - 1:], color=RED, lw=3.8, label="그 뒤 실제로 굴린 기간")
    ax.axvline(t[n // 2], color=INK, lw=2, ls="--")
    ax.text(t[n // 2] + .1, v.max() * .99, "여기서부터가 진짜", fontsize=17,
            color=INK, fontweight="bold", va="top")
    ax.text(.22, .92, "고르고 고른 규칙이라\n좋아 보인다", transform=ax.transAxes,
            ha="center", va="top", fontsize=16, color=TEAL, fontweight="bold")
    ax.text(.80, .62, "밖에서는 그만큼\n나오지 않는다", transform=ax.transAxes,
            ha="center", va="top", fontsize=16, color=RED, fontweight="bold")
    ax.set_xlabel("햇수", fontsize=16)
    ax.set_ylabel("100으로 시작한 값", fontsize=16)
    ax.legend(loc="lower right", fontsize=16)
    note(f, "※ 과최적화를 보이려고 만든 예시입니다")
    return save(f, P("overfit.png"), strict=True)


def ff_lineage():
    names = ["1964  CAPM\n시장 하나만", "1993  파마-프렌치 3팩터\n＋크기 ＋가치",
             "2015  파마-프렌치 5팩터\n＋수익성 ＋투자"]
    r2 = [72, 90, 94]
    cols = [GREYBAR, TEAL, LIME]
    f, ax = fig(size=SIZE)
    bars = ax.bar(range(3), r2, color=cols, width=.56,
                  edgecolor=[("none" if c != LIME else INK) for c in cols], linewidth=1.4)
    zo_mpl.val_label(ax, bars, fmt="{:.0f}%", size=21)
    ax.set_xticks(range(3))
    ax.set_xticklabels(names, fontsize=16)
    ax.set_ylabel("설명되는 몫(%)", fontsize=16)
    ax.set_ylim(0, 132)
    ax.annotate("", xy=(.68, 99), xytext=(.20, 99),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.4))
    ax.text(.5, 103, "시장 하나로는 부족했다", ha="center", fontsize=17,
            color=RED, fontweight="bold")
    ax.text(1.5, 120, "“설명되지 않던 몫”을 줄여 온 60년",
            ha="center", fontsize=18, color=INK, fontweight="bold")
    bar_grid(ax)
    note(f, "※ 설명되는 몫은 자료와 기간에 따라 달라집니다 · 흐름을 보이려는 예시입니다")
    return save(f, P("ff_lineage.png"), strict=True)


def decompose():
    """한 종목의 한 해 수익을 '어디서 왔는지'로 쪼갠다 — W10 p12.
    v1.11: 조각 이름을 계열색(파랑·주황)으로 칠하지 않고 잉크 bold로, 괄호 설명은 보조색이 아니라 잉크로."""
    parts = [("시장이 올라서", 8.0, TEAL), ("작은 회사라서", 3.0, BLUE),
             ("싼 주식이라서", 2.0, AMBER), ("설명 안 되는 몫", 1.4, LIME)]
    total = sum(v for _, v, _ in parts)
    known = total - parts[-1][1]
    f, ax = fig(size=SIZE)
    left = 0.0
    for k, (name, v, c) in enumerate(parts):
        ax.barh([0], [v], left=[left], height=.50, color=c,
                edgecolor=INK if c == LIME else "none", linewidth=1.4)
        ax.text(left + v / 2, 0, f"{v:.1f}%", ha="center", va="center",
                fontsize=19, color=ink_on(c), fontweight="bold")
        # 이름은 막대 위에 번갈아 놓아 겹치지 않게 한다
        ax.text(left + v / 2, .34 if k % 2 == 0 else .62, name, ha="center",
                fontsize=17, color=INK, fontweight="bold")
        left += v
    ax.text(total + .25, 0, f"합쳐서 {total:.1f}%", va="center", fontsize=18,
            color=INK, fontweight="bold")

    def bracket(x0, x1, y, lab, lc, tc):
        ax.plot([x0, x0, x1, x1], [y + .07, y, y, y + .07], color=lc, lw=2.2)
        ax.text((x0 + x1) / 2, y - .12, lab, ha="center", va="top",
                fontsize=17, color=tc, fontweight="bold")
    bracket(0, known, -.34, "여기까지는 누구나 살 수 있다 — 팩터로 설명되는 몫", TEAL, TEAL)
    bracket(known, total, -.34, "이것만 실력", RED, RED)
    ax.set_xlim(-.3, total + 3.4)
    ax.set_ylim(-.72, .9)
    ax.set_xticks(range(0, 17, 2))
    ax.set_xlabel("한 해 수익률(%)", fontsize=16)
    ax.set_yticks([])
    ax.grid(False)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    note(f, EX)
    return save(f, P("decompose.png"), strict=True)


def alpha_shrink():
    models = ["시장 하나만\n놓고 볼 때", "크기·가치를\n더하면", "수익성·투자를\n더하면", "오르던 것까지\n더하면"]
    alpha = [4.2, 2.1, 0.9, 0.3]
    cols = [RED, AMBER, BLUE, GREYBAR]
    f, ax = fig(size=SIZE)
    bars = ax.bar(range(4), alpha, color=cols, width=.56)
    zo_mpl.val_label(ax, bars, fmt="{:.1f}%", size=20)
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_xticks(range(4))
    ax.set_xticklabels(models, fontsize=16)
    ax.set_ylabel("실력이라 부를 몫  α(%)", fontsize=16)
    ax.set_ylim(0, 5.9)
    ax.text(1.95, 5.25, "설명하는 조각을 늘릴수록 남는 몫이 줄어든다",
            ha="center", fontsize=18, color=INK, fontweight="bold")
    ax.text(1.95, 4.6, "처음에 실력처럼 보이던 것이 대부분 이미 알려진 조각이었다",
            ha="center", fontsize=16, color=SUB)
    bar_grid(ax)
    note(f, "※ 같은 펀드를 서로 다른 모형으로 재봤을 때를 본뜬 예시입니다")
    return save(f, P("alpha_shrink.png"), strict=True)


# ══ SVG 도해 ═════════════════════════════════════════════════════
W, H = 1600, 600


def svg(name, body):
    import cairosvg
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{PAPER}"/>'
           f'<style>text{{font-family:"Pretendard","Noto Sans CJK KR",sans-serif}}</style>'
           f'<defs>'
           f'<marker id="aT" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">'
           f'<path d="M0,0 L9,4 L0,8 z" fill="{TEAL}"/></marker>'
           f'</defs>{body}</svg>')
    p = P(name)
    cairosvg.svg2png(bytestring=doc.encode("utf-8"), write_to=p, output_width=W * 2)
    print(f"[svg] {p}  {W*2}×{H*2}  ratio:{W}/{H}")
    return p


def T(x, y, t, size=32, color=INK, anchor="middle", bold=False):
    assert size >= 30, f"SVG 글씨 30px 미만: {t}"
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
            + (' font-weight="700"' if bold else ' font-weight="500"') + f'>{t}</text>')


def R(x, y, w, h, fill=WHITE, stroke=HAIR, sw=2):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def box(x, y, w, h, title, sub=(), fill=WHITE, stroke=HAIR, tc=INK, sc=MUTED, ts=34, ss=30):
    s = R(x, y, w, h, fill, stroke, 3 if fill == LIME else 2)
    top = y + h / 2 - (len(sub) * 40) / 2 + 6
    s += T(x + w / 2, top, title, ts, tc, bold=True)
    for i, ln in enumerate(sub):
        s += T(x + w / 2, top + 46 + i * 40, ln, ss, sc)
    return s


def arrow(x1, y1, x2, y2, wt=5):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TEAL}" '
            f'stroke-width="{wt}" marker-end="url(#aT)"/>')


def pipeline():
    b = T(800, 52, "사람이 종목을 고르는 대신, 규칙을 만들어 기계에 맡긴다", 36, INK, bold=True)
    steps = [("① 자료를 모은다", ["값 · 실적 · 거래량"]),
             ("② 점수를 매긴다", ["규칙 하나를 정해", "종목마다 점수를"]),
             ("③ 담을 것을 정한다", ["점수 높은 쪽을 사고", "낮은 쪽은 던다"])]
    xs = [40, 430, 820]
    for x, (t0, lines) in zip(xs, steps):
        b += box(x, 100, 340, 220, t0, lines, ts=32)
        b += arrow(x + 348, 210, x + 382, 210)
    b += box(1210, 100, 350, 220, "④ 사고판다", ["수수료를 줄이며"], fill=LIME, stroke=INK,
             tc=INK, sc=INK, ts=32)
    b += T(800, 400, "사람이 하는 일은 규칙을 정하고 지키는 것이다", 34, TEAL, bold=True)
    b += T(800, 456, "종목 하나하나를 들여다보는 일이 아니다", 32, MUTED)
    b += T(800, 548, "그래서 “왜 이 규칙인가”에 답하지 못하면 그 규칙은 쓸 수 없다", 32, RED, bold=True)
    return svg("pipeline.png", b)


def what_is_factor():
    b = T(800, 48, "한 종목이 오르내리는 이유는 세 갈래다", 36, INK, bold=True)
    b += box(30, 225, 330, 150, "어느 회사 주식", ["이번 달 +5.0%"], ts=32)
    rows = [(80, "① 시장 전체가 올라서", "+3.0%", "모든 주식이 함께 움직인 몫", WHITE),
            (228, "② 같은 성질끼리 함께 올라서", "+1.5%", "작은 회사들이 다 같이 올랐다", LIME),
            (376, "③ 그 회사만의 일", "+0.5%", "신제품이 잘 팔렸다", WHITE)]
    for y, name, val, desc, fill in rows:
        b += arrow(368, 300, 432, y + 66, 4)
        b += R(445, y, 760, 132, fill, INK if fill == LIME else HAIR, 3 if fill == LIME else 2)
        b += T(475, y + 52, name, 32, INK, "start", True)
        b += T(475, y + 102, desc, 30, INK if fill == LIME else MUTED, "start")
        b += T(1180, y + 80, val, 38, INK, "end", True)
    b += T(1232, 280, "여러 종목을", 30, INK, "start", True)
    b += T(1232, 322, "함께 움직이게 하는", 30, INK, "start", True)
    b += T(1232, 368, "공통 원인", 34, INK, "start", True)
    b += T(1232, 424, "= 팩터", 38, TEAL, "start", True)
    b += T(800, 572, "①은 누구나 얻고 ③은 흩어져 사라진다 — 골라 담을 수 있는 것은 ②뿐이다",
           32, RED, bold=True)
    return svg("what_is_factor.png", b)


def factor_menu():
    b = T(800, 46, "모형에 흔히 넣는 팩터들", 36, INK, bold=True)
    b += T(800, 92, "모두 “한 묶음에서 다른 묶음을 뺀 수익”으로 만든다", 30, MUTED)
    specs = [("시장", "MKT", "주식 전체", "− 국채"),
             ("크기", "SMB", "작은 회사", "− 큰 회사"),
             ("가치", "HML", "싼 주식", "− 비싼 주식"),
             ("수익성", "RMW", "잘 버는 회사", "− 못 버는 회사"),
             ("투자", "CMA", "조심히 늘리는 회사", "− 마구 늘리는 회사"),
             ("모멘텀", "UMD", "오르던 것", "− 내리던 것")]
    for i, (ko, tag, l1, l2) in enumerate(specs):
        x = 40 + (i % 3) * 520
        y = 118 + (i // 3) * 214
        b += R(x, y, 480, 196)
        b += T(x + 30, y + 52, ko, 34, INK, "start", True)
        b += T(x + 450, y + 52, tag, 30, TEAL, "end", True)
        b += f'<line x1="{x+30}" y1="{y+74}" x2="{x+450}" y2="{y+74}" stroke="{HAIR}" stroke-width="2"/>'
        b += T(x + 240, y + 122, l1, 30, BODY)
        b += T(x + 240, y + 166, l2, 30, MUTED)
    b += T(800, 584, "앞의 다섯은 파마와 프렌치가, 모멘텀은 카하트가 정리했다", 30, MUTED)
    return svg("factor_menu.png", b)


def meta_label():
    b = T(800, 52, "“살까 말까”와 “얼마나 걸까”는 다른 질문이다", 36, INK, bold=True)
    b += box(40, 105, 400, 210, "첫째 모형", ["살까, 팔까", "방향만 정한다"])
    b += arrow(450, 225, 628, 225)
    b += T(539, 200, "그 답을 받아", 30, TEAL, bold=True)
    b += box(640, 105, 470, 210, "둘째 모형", ["이 판단이 맞을 확률은?", "크게 걸까, 작게 걸까"],
             stroke=TEAL, tc=TEAL, sc=INK)
    b += arrow(1118, 210, 1218, 210)
    b += box(1230, 105, 330, 210, "최종 크기", ["확신만큼만"], fill=LIME, stroke=INK, sc=INK)
    b += f'<line x1="40" y1="355" x2="1560" y2="355" stroke="{HAIR}" stroke-width="2"/>'
    b += T(800, 418, "방향을 맞히는 일과 크기를 정하는 일을 한 모형에 맡기지 않는다", 34, INK, bold=True)
    b += T(800, 474, "확신이 낮은 판단에 크게 걸면, 맞아도 남는 게 없다", 32, MUTED)
    b += T(800, 556, "이렇게 나눈 것을 메타 레이블링이라 부른다", 32, RED, bold=True)
    return svg("meta_label.png", b)


# ══ 수식 ═════════════════════════════════════════════════════════

def equation():
    """흰 카드에 얹으므로 흰 배경 + 잉크색(v1.10). pdflatex이 없어 mathtext(CM)로 굽는다."""
    tex = r"$r_i\;=\;\alpha\;+\;\beta_1 f_1\;+\;\beta_2 f_2\;+\;\cdots\;+\;\varepsilon$"
    plt.rcParams["mathtext.fontset"] = "cm"
    f = plt.figure(figsize=(9.6, 1.9), facecolor=WHITE)
    f.text(.5, .5, tex, ha="center", va="center", fontsize=44, color=INK)
    p = P("equation.png")
    f.savefig(p, bbox_inches="tight", facecolor=WHITE, pad_inches=0.26, dpi=200)
    plt.close(f)
    print(f"[eq] {p}")
    return p


if __name__ == "__main__":
    pipeline(); quantile(); what_is_factor(); factor_menu(); ff_lineage()
    decompose(); alpha_shrink(); overfit()
    meta_label(); equation()
    print("끝.")
