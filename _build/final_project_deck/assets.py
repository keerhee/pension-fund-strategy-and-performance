#!/usr/bin/env python3
"""XS 팀 프로젝트 안내 제로원 덱의 그림을 굽는다.

  viz/*.png  SVG 도해(cairosvg) · matplotlib 차트(zo_mpl)
  eq/*.png   수식(render_eq — 이 맥은 mathtext)

실행:  cd _build/final_project_deck && ../../.venv/bin/python assets.py
"""
import json, os, sys

SK = "/Users/keerhee/Project/.claude/skills/zeroone-pitch-deck/scripts"
sys.path.insert(0, SK)
import numpy as np
import cairosvg
from zo_mpl import fig, save, C
from render_eq import render, INK, PAPER, LIME, DARK

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs("viz", exist_ok=True)
MVP = os.path.join(HERE, "../../Final_Project/1_Student/3_Example_MVP")


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, t, size=30, fill=None, bold=False, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{700 if bold else 400}" fill="{fill or C["body"]}">{esc(t)}</text>')


def R(x, y, w, h, fill, stroke=None, rx=14, dash=None, sw=2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if dash:
        st += f' stroke-dasharray="{dash}"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>'


def arrow(pts, color=None, sw=5, head=14):
    color = color or C["teal"]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    v = np.array([x2 - x1, y2 - y1], float)
    v /= np.linalg.norm(v)
    n = np.array([-v[1], v[0]])
    tip = np.array([x2, y2])
    a = tip - v * head * 1.4 + n * head * 0.8
    b = tip - v * head * 1.4 - n * head * 0.8
    # 선은 화살촉 밑동에서 끝낸다
    base = tip - v * head * 1.2
    d = "M" + " L".join(f"{x} {y}" for x, y in pts[:-1]) + f" L{base[0]:.1f} {base[1]:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linejoin="round"/>'
            f'<path d="M{tip[0]:.1f} {tip[1]:.1f} L{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} z" '
            f'fill="{color}"/>')


def bake(name, parts, W, H):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'font-family="Noto Sans CJK KR">' + R(0, 0, W, H, C["paper"], rx=0) + "".join(parts) + "</svg>")
    open(f"viz/{name}.svg", "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"viz/{name}.png",
                     output_width=W, output_height=H)
    print(f"[svg] viz/{name}.png  {W}x{H}")


# ---------------------------------------------------------------------------
# 1) 여섯 층 (1600x620)
P = []
P.append(R(40, 30, 1520, 96, C["ink"]))
P.append(T(80, 92, "거버넌스 — IPS가 전 과정을 제약한다", 36, C["lime"], True, "start"))
P.append(T(1520, 92, "W01 · W15", 30, "#9FB0B2", False, "end"))
boxes = [("입력", "CMA 생성", "W03"), ("구성", "배분안 경쟁", "W04 · W05"),
         ("비평·투표", "상호 심사·표결", "16주 모의 IC"), ("결정", "IC 보고 → CIO", "사람의 감독")]
bw, gap, y0, bh = 320, 80, 180, 190
for i, (cap, ttl, wk) in enumerate(boxes):
    x = 40 + i * (bw + gap)
    last = i == 3
    P.append(R(x, y0, bw, bh, C["lime"] if last else C["white"], C["hair"]))
    P.append(T(x + bw / 2, y0 + 50, cap, 30, C["teal"] if not last else C["body"], True))
    P.append(T(x + bw / 2, y0 + 108, ttl, 36, C["body"], True))
    P.append(T(x + bw / 2, y0 + 160, wk, 30, C["muted"]))
    if not last:
        P.append(arrow([(x + bw + 8, y0 + bh / 2), (x + bw + gap - 8, y0 + bh / 2)]))
# 아래 두 층
P.append(R(440, 425, 320, 180, C["white"], C["teal"], dash="10 8"))
P.append(T(600, 478, "탐색", 30, C["teal"], True))
P.append(T(600, 532, "새 방법 제안", 34, C["body"], True))
P.append(T(600, 582, "W12 · W13", 30, C["muted"]))
P.append(arrow([(600, 423), (600, y0 + bh + 6)]))
P.append(R(840, 425, 720, 180, C["white"], C["teal"], dash="10 8"))
P.append(T(1200, 490, "자기개선 — 예측과 실현을 대조 (W09)", 30, C["teal"], True))
P.append(T(1200, 545, "스킬 수정은 제안서로만, CIO 승인 후 반영", 32, C["body"], True))
P.append(arrow([(1400, y0 + bh + 6), (1400, 423)]))
bake("layers", P, 1600, 620)

# ---------------------------------------------------------------------------
# 2) 시점 잠금 (1600x620)
P = []
months = ["3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
X0, MW = 420, 112
xa = X0 + 6 * MW                       # 8월 말
P.append(R(xa, 40, X0 + 10 * MW - xa, 460, "#ECEFEE", rx=0))
for k in range(0, 40):                 # 빗금
    x = xa + k * 30 - 400
    P.append(f'<line x1="{x}" y1="500" x2="{x + 460}" y2="40" stroke="#DDE3E2" stroke-width="3"/>')
P.append(R(xa, 40, X0 + 10 * MW - xa, 460, "none", rx=0))
rows = [("ETF 총수익률 (D1)", 6, None), ("물가·실업률 (D4)", 5, "8월 값은 9월 발표"),
        ("리서치 자료 (D6)", None, None)]
for r, (lab, upto, tip) in enumerate(rows):
    y = 120 + r * 130
    P.append(T(380, y + 12, lab, 32, C["body"], True, "end"))
    if upto is not None:
        P.append(R(X0, y - 22, upto * MW - 6, 44, C["teal"], rx=8))
        if upto < 6:
            P.append(R(X0 + upto * MW, y - 22, MW - 6, 44, C["white"], C["muted"], rx=8, dash="8 6"))
            P.append(T(X0 + upto * MW - 14, y - 36, tip, 30, C["muted"], False, "end"))
        P.append(R(xa + 6, y - 22, 4 * MW - 12, 44, "#C9D1D0", rx=8))
    else:
        for m in [0.4, 1.3, 2.6, 3.2, 4.5, 5.6]:
            cx = X0 + m * MW
            P.append(R(cx - 16, y - 24, 32, 46, C["teal"], rx=4))
        for m in [6.7, 8.1, 9.3]:
            cx = X0 + m * MW
            P.append(R(cx - 16, y - 24, 32, 46, "#C9D1D0", rx=4))
            P.append(f'<path d="M{cx-22} {y-30} L{cx+22} {y+28} M{cx+22} {y-30} L{cx-22} {y+28}" '
                     f'stroke="{C["red"]}" stroke-width="5"/>')
# 축
P.append(f'<line x1="{X0}" y1="510" x2="{X0 + 10 * MW}" y2="510" stroke="{C["muted"]}" stroke-width="2"/>')
for i, m in enumerate(months):
    P.append(T(X0 + i * MW + MW / 2, 552, m, 30, C["muted"]))
P.append(f'<line x1="{xa}" y1="30" x2="{xa}" y2="520" stroke="{C["ink"]}" stroke-width="5"/>')
P.append(R(xa - 150, 566, 300, 50, C["ink"], rx=10))
P.append(T(xa, 602, "as_of = 2022-08-31", 30, C["lime"], True))
P.append(T(xa + 2 * MW + 20, 82, "공통 로더가 거부 → trace 기록", 30, C["red"], True))
bake("timelock", P, 1600, 630)

# ---------------------------------------------------------------------------
# 3) 분기 루프 (1600x620) — 뱀 모양 두 줄
P = []
bw, gap, h = 330, 60, 200
xs = [50 + i * (bw + gap) for i in range(4)]
row1 = [("M3 · M4 · M5", "입력", "매크로·CMA·리서치"), ("M6", "배분안 경쟁", "PC 4개+ · 적대적"),
        ("M1", "자동 기각", "ips-guardian"), ("M7", "리스크 심사", "CRO 보고서")]
row2 = {3: ("M8", "상호 검토·투표", "수정 보르다"), 2: ("M9", "IC 보고 → CIO", "승인·조건부·반려"),
        1: ("M10", "메타 리뷰", "예측 vs 실현")}
y1, y2 = 40, 380


def box(x, y, tag, ttl, sub, fill):
    out = [R(x, y, bw, h, fill, C["hair"])]
    out.append(T(x + bw / 2, y + 52, tag, 30, C["teal"] if fill != C["lime"] else C["body"], True))
    out.append(T(x + bw / 2, y + 112, ttl, 38, C["body"], True))
    out.append(T(x + bw / 2, y + 164, sub, 30, C["muted"] if fill != C["lime"] else C["body"]))
    return out


for i, (tag, ttl, sub) in enumerate(row1):
    P += box(xs[i], y1, tag, ttl, sub, C["white"])
    if i < 3:
        P.append(arrow([(xs[i] + bw + 6, y1 + h / 2), (xs[i + 1] - 6, y1 + h / 2)]))
P.append(arrow([(xs[3] + bw / 2, y1 + h + 6), (xs[3] + bw / 2, y2 - 6)]))
for c in (3, 2, 1):
    tag, ttl, sub = row2[c]
    P += box(xs[c], y2, tag, ttl, sub, C["lime"] if c == 2 else C["white"])
    P.append(arrow([(xs[c] - 6, y2 + h / 2), (xs[c - 1] + bw + 6, y2 + h / 2)]))
# 다음 분기
P.append(R(xs[0], y2, bw, h, "none", C["teal"], dash="12 9", sw=3))
P.append(T(xs[0] + bw / 2, y2 + 88, "다음 분기", 38, C["teal"], True))
P.append(T(xs[0] + bw / 2, y2 + 140, "변경은 킬스위치(M2)", 30, C["muted"]))
P.append(arrow([(xs[0] + bw / 2, y2 - 6), (xs[0] + bw / 2, y1 + h + 6)]))
bake("loop", P, 1600, 620)

# ---------------------------------------------------------------------------
# 4) 킬스위치 (1400x900)
P = []
P.append(R(40, 330, 360, 300, C["white"], C["hair"]))
P.append(T(220, 400, "에이전트", 32, C["teal"], True))
P.append(T(220, 470, "meta-reviewer", 32, C["body"], True))
P.append(T(220, 530, "research-agent", 32, C["body"], True))
P.append(T(220, 590, "제안만 쓴다", 30, C["muted"]))
P.append(R(1000, 330, 360, 300, C["ink"]))
P.append(T(1180, 400, "보호 파일", 32, C["lime"], True))
for k, t in enumerate(["ips.md", "SKILL.md", "코드"]):
    P.append(T(1180, 470 + k * 56, t, 32, C["white"], True))
# 직접 수정 — 차단
P.append(f'<path d="M220 326 L220 90 L1180 90 L1180 316" fill="none" stroke="{C["red"]}" '
         f'stroke-width="5" stroke-dasharray="16 10"/>')
P.append(f'<path d="M675 45 L765 135 M765 45 L675 135" stroke="{C["red"]}" stroke-width="10"/>')
P.append(T(700, 190, "직접 수정 차단", 32, C["red"], True))
# 정상 경로
mid = [("proposals/", "제안서로만 남는다"), ("CIO 승인", "CHANGELOG.md에 기록"),
       ("테스트 후 배포", "나아지면 승격 · 아니면 롤백")]
for k, (a, b) in enumerate(mid):
    y = 250 + k * 210
    last = k == 2
    P.append(R(480, y, 440, 150, C["lime"] if last else C["white"], C["hair"]))
    P.append(T(700, y + 62, a, 34, C["body"], True))
    P.append(T(700, y + 112, b, 30, C["body"] if last else C["muted"]))
    if k < 2:
        P.append(arrow([(700, y + 154), (700, y + 206)]))
P.append(arrow([(404, 480), (440, 480), (440, 325), (476, 325)]))
P.append(arrow([(924, 745), (960, 745), (960, 480), (996, 480)]))
bake("killswitch", P, 1400, 900)

# ---------------------------------------------------------------------------
# 5) 공개 점검 T1~T8 (1600x620)
P = []
tests = [("T1", "깨끗한 실행", "코드 수정 없이", "ic_report까지", "r"),
         ("T2", "IPS 위반 주입", "한 자산 50% →", "자동 기각", "s"),
         ("T3", "자기 수정 시도", "파일은 그대로,", "제안서만 생성", "s"),
         ("T4", "미래정보 차단", "as_of 이후 행을", "로더가 거부", "s"),
         ("T5", "투표 검산", "M8 예제 재현,", "채택 C", "r"),
         ("T6", "계산 재현", "두 번 실행해", "소수 6자리 일치", "r"),
         ("T7", "감사 추적", "trace만으로", "CIO 결정까지", "s"),
         ("T8", "증거 대조", "임의 2개 분기", "숫자가 같다", "r")]
cw, ch, g = 370, 285, 20
for k, (tag, ttl, a, b, kind) in enumerate(tests):
    r, c = divmod(k, 4)
    x, y = 30 + c * (cw + g), 20 + r * (ch + g)
    col = C["teal"] if kind == "r" else C["blue"]
    P.append(R(x, y, cw, ch, C["white"], C["hair"]))
    P.append(R(x, y, 14, ch, col, rx=0))
    P.append(T(x + 44, y + 64, tag, 40, col, True, "start"))
    P.append(T(x + 44, y + 128, ttl, 36, C["body"], True, "start"))
    P.append(T(x + 44, y + 192, a, 30, C["muted"], False, "start"))
    P.append(T(x + 44, y + 238, b, 30, C["muted"], False, "start"))
bake("tests", P, 1600, 630)

# ---------------------------------------------------------------------------
# 6) 아홉 단계 (1600x620)
P = []
phases = [("설계", [("1", "기금 정하기", "A · 전원"), ("2", "데이터와 시점 규율", "B · E"),
                  ("3", "입력 만들기", "B")]),
          ("실행", [("4", "배분안 경쟁", "C"), ("5", "심의", "D"), ("6", "분기 루프", "E · 전원")]),
          ("검증 · 결정", [("7", "재현성 3회", "E"), ("8", "정책 실험", "A · D"),
                         ("9", "도입 의결", "CIO")])]
pw, pg = 490, 40
for i, (ph, steps) in enumerate(phases):
    x = 25 + i * (pw + pg)
    P.append(R(x, 20, pw, 80, C["ink"], rx=12))
    P.append(T(x + pw / 2, 74, ph, 36, C["lime"], True))
    for j, (n, ttl, who) in enumerate(steps):
        y = 125 + j * 165
        last = n == "9"
        P.append(R(x, y, pw, 145, C["lime"] if last else C["white"], C["hair"]))
        P.append(f'<circle cx="{x + 70}" cy="{y + 72}" r="38" fill="{C["ink"] if last else C["teal"]}"/>')
        P.append(T(x + 70, y + 86, n, 38, C["lime"] if last else C["white"], True))
        P.append(T(x + 135, y + 66, ttl, 36, C["body"], True, "start"))
        P.append(T(x + 135, y + 116, "역할 " + who, 30, C["body"] if last else C["muted"], False, "start"))
    if i < 2:
        P.append(arrow([(x + pw + 6, 60), (x + pw + pg - 6, 60)], sw=4, head=11))
bake("steps", P, 1600, 620)


# ---------------------------------------------------------------------------
# 7) CIO 결정 12회 + 도입 의결 (1600x560) — 예시 MVP의 cio_decisions.csv
import csv
dec = list(csv.DictReader(open(os.path.join(MVP, "data/cio_decisions.csv"))))
P = []
bw, sp, x0, y0 = 96, 102, 40, 210
colmap = {"승인": C["teal"], "조건부 승인": C["amber"], "반려": C["red"]}
for i, d in enumerate(dec):
    x = x0 + i * sp
    lab = {"승인": "승인", "조건부 승인": "조건부", "반려": "반려"}[d["decision"]]
    P.append(R(x, y0, bw, 110, colmap[d["decision"]], rx=12))
    P.append(T(x + bw / 2, y0 + 66, lab, 30, "white", True))
    P.append(T(x + bw / 2, y0 + 160, d["as_of"][2:4] + "." + d["as_of"][5:], 30, C["muted"]))
i5 = [d["as_of"] for d in dec].index("2023-08")
xa = x0 + i5 * sp + bw / 2
P.append(f'<line x1="{xa}" y1="{y0-8}" x2="{xa}" y2="120" stroke="{C["amber"]}" stroke-width="4"/>')
P.append(T(xa, 104, "신흥국 상한 5% 조건", 30, C["body"], True))
i9 = [d["as_of"] for d in dec].index("2024-11")
xb = x0 + i9 * sp + bw + sp / 2 - bw / 2 - 3
P.append(f'<path d="M{x0+i9*sp+bw/2} {y0-8} L{x0+i9*sp+bw/2} 150 L{x0+(i9+1)*sp+bw/2} 150 L{x0+(i9+1)*sp+bw/2} {y0-8}" '
         f'fill="none" stroke="{C["red"]}" stroke-width="4"/>')
P.append(T(xb + 45, 72, "점수 차는 추정오차 안,", 30, C["body"], True))
P.append(T(xb + 45, 116, "회전율 32~35% → 현 보유 유지", 30, C["body"], True))
fx = x0 + 12 * sp + 20
P.append(arrow([(fx - 18, y0 + 55), (fx + 22, y0 + 55)]))
P.append(R(fx + 30, y0 - 30, 1570 - fx - 30, 170, C["lime"]))
P.append(T((fx + 30 + 1570) / 2, y0 + 30, "도입 의결", 34, C["body"], True))
P.append(T((fx + 30 + 1570) / 2, y0 + 86, "조건부 승인", 34, C["body"], True))
P.append(T(40, 470, "변경 제안 4건 — CIO 승인 1 · 반려 3 (approvals.csv) · 승인 1건도 테스트에서 롤백", 30, C["muted"], False, "start"))
P.append(T(40, 530, "평가 구간 매 분기 말 결정 → 프로젝트 끝 의결문", 30, C["teal"], True, "start"))
bake("decisions", P, 1600, 560)
# ---------------------------------------------------------------------------
# matplotlib 차트
perf = json.load(open(os.path.join(MVP, "reports/performance.json")))
paths, dates = perf["cum_paths"], perf["dates"]
f, ax = fig("panel")
x = np.arange(len(dates) + 1)
spec = [("60/40 (SPY·IEF)", "60/40", C["blue"], 2.2),
        ("pc-maxsharpe", "MVO 계속 보유", C["amber"], 2.2),
        ("동일가중 1/11", "동일가중", C["muted"], 2.0),
        ("채택 경로(CIO)", "채택 경로", C["lime_dk"], 3.6)]
OFF = {"60/40": 9, "MVO 계속 보유": -9, "동일가중": -9, "채택 경로": 8}
for key, lab, col, lw in spec:
    v = np.r_[1.0, np.array(paths[key])]
    ax.plot(x, (v - 1) * 100, color=col, lw=lw, label=lab)
    ax.annotate(f"{perf['metrics'][key]['ann_ret']*100:.2f}%", (x[-1], (v[-1] - 1) * 100),
                xytext=(6, OFF[lab]), textcoords="offset points", va="center", color=col,
                fontsize=14, fontweight="bold")
ticks = [0, 16, 28, len(dates)]
ax.set_xticks(ticks)
ax.set_xticklabels(["22.8", "23.12", "24.12", "25.7"])
ax.set_xlim(0, len(dates) + 8)
ax.set_ylabel("누적 수익률 (%)")
ax.legend(loc="upper left", fontsize=13)
save(f, "viz/perf.png")

# N_eff
f, ax = fig("panel")
ports = [("한 종목 70%", [0.7, 0.1, 0.1, 0.1]), ("(0.4, 0.3, 0.2, 0.1)", [0.4, 0.3, 0.2, 0.1]),
         ("4종 동일가중", [0.25] * 4), ("11종 동일가중", [1 / 11] * 11)]
vals = [1 / np.sum(np.square(w)) for _, w in ports]
cols = [C["muted"], C["red"], C["teal"], C["teal"]]
ax.barh(range(4), vals, color=cols, height=0.6)
ax.set_yticks(range(4))
ax.set_yticklabels([p for p, _ in ports])
ax.invert_yaxis()
ax.axvline(4.0, color=C["ink"], lw=2, ls="--")
ax.text(4.15, -0.62, "하한 4.0", color=C["ink"], fontsize=15, fontweight="bold")
for i, v in enumerate(vals):
    ax.text(max(v, 4.0) + 0.2, i, f"{v:.2f}", va="center", fontsize=15, fontweight="bold", color=C["body"])
ax.set_xlim(0, 12.5); ax.set_ylim(3.5, -0.95)
ax.set_xlabel(r"유효 종목 수 $N_{\mathrm{eff}}$")
ax.grid(axis="y", visible=False)
save(f, "viz/neff.png")

# 위험기여 (과정 표준 가정: 주식 16% · 채권 5% · 상관 0.2)
sd = np.array([0.16, 0.05]); rho = 0.2
S = np.array([[sd[0] ** 2, rho * sd[0] * sd[1]], [rho * sd[0] * sd[1], sd[1] ** 2]])


def rc(w):
    w = np.array(w); m = S @ w
    return w * m / (w @ m)


erc = np.array([1 / sd[0], 1 / sd[1]]); erc /= erc.sum()
rows_ = [("60/40 비중", [0.6, 0.4]), ("60/40 위험기여", rc([0.6, 0.4])),
         ("ERC 비중", erc), ("ERC 위험기여", rc(erc))]
f, ax = fig("panel")
for i, (lab, w) in enumerate(rows_):
    ax.barh(i, w[0] * 100, color=C["teal"], height=0.6, label="주식" if i == 0 else None)
    ax.barh(i, w[1] * 100, left=w[0] * 100, color=C["amber"], height=0.6, label="채권" if i == 0 else None)
    ax.text(w[0] * 50, i, f"{w[0]*100:.0f}", ha="center", va="center", color="white", fontsize=15, fontweight="bold")
    if w[1] > 0.06:
        ax.text(w[0] * 100 + w[1] * 50, i, f"{w[1]*100:.0f}", ha="center", va="center", color=C["body"],
                fontsize=15, fontweight="bold")
ax.set_yticks(range(4)); ax.set_yticklabels([r[0] for r in rows_]); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.set_xlabel("%")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=14)
ax.grid(axis="y", visible=False)
save(f, "viz/rc.png")
print("RC 60/40:", rc([0.6, 0.4]).round(3), "ERC w:", erc.round(3))

# 투표 검산
lam = 0.5
Sraw = np.array([0, 5, 5, -6.0]); Sh = (Sraw - Sraw.min()) / (Sraw.max() - Sraw.min())
M_ = np.array([0.40, 0.70, 0.80, 0.90]); score = lam * Sh + (1 - lam) * M_
print("score", score.round(3))
f, ax = fig("panel")
lab = ["A", "B", "C", "D"]
ax.bar(lab, lam * Sh, color=C["teal"], width=0.6, label=r"$\lambda\,\hat S$ (득표)")
ax.bar(lab, (1 - lam) * M_, bottom=lam * Sh, color=C["blue"], width=0.6, label=r"$(1-\lambda)\,M$ (정량)")
for i, v in enumerate(score):
    ax.text(i, v + 0.03, f"{v:.3f}", ha="center", fontsize=16, fontweight="bold",
            color=C["body"])
ax.bar([2], [score[2]], fill=False, edgecolor=C["lime_dk"], lw=4, width=0.6)
ax.text(2, score[2] + 0.13, "채택", ha="center", fontsize=16, fontweight="bold", color=C["lime_dk"])
ax.set_ylim(0, 1.45); ax.set_ylabel("Score")
ax.legend(loc="upper left", fontsize=13, ncol=2)
ax.grid(axis="x", visible=False)
save(f, "viz/vote.png")

# 진행표 (wide)
f, ax = fig("wide")
f.set_size_inches(8.0, 3.5)
plan = [("팀 구성 · MVP 실행", 6, 7), ("프로포절 + MVP v0", 8, 8.9), ("M1~M5 거버넌스·입력", 9, 9.9),
        ("M6~M7 구성·CRO", 10, 10.9), ("M8~M9 투표·IC·CIO", 11, 11.9), ("분기 루프 통합", 12, 12.9),
        ("M10 학습 + 정책 실험", 13, 13.9), ("재실행 3회 + 창의", 14, 14.9),
        ("자가 점검 · 리허설", 15, 15.9), ("최종 발표", 16, 16.9)]
for i, (lab_, a, b) in enumerate(plan):
    col = C["lime_dk"] if lab_ == "최종 발표" else (C["amber"] if "v0" in lab_ else C["teal"])
    ax.barh(i, b - a, left=a, color=col, height=0.62)
ax.set_yticks(range(len(plan))); ax.set_yticklabels([p[0] for p in plan], fontsize=12)
ax.invert_yaxis()
ax.set_xticks(np.arange(6, 17) + 0.45)
ax.set_xticklabels([f"W{w:02d}" for w in range(6, 17)], fontsize=12)
ax.set_xlim(5.9, 17.1)
ax.grid(axis="y", visible=False)
save(f, "viz/schedule.png")

# 점수표 구조
f, ax = fig("panel")
areas = [("창의성", 35), ("완성도·재현성", 25), ("감독·하네스", 20), ("분석·해석", 10), ("발표·문서", 10)]
for i, (a, v) in enumerate(areas):
    ax.barh(i, v, color=C["lime_dk"] if i == 0 else C["teal"], height=0.62)
    ax.text(v + 0.6, i, f"{v}", va="center", fontsize=17, fontweight="bold", color=C["body"])
ax.set_yticks(range(len(areas))); ax.set_yticklabels([a for a, _ in areas]); ax.invert_yaxis()
ax.set_xlim(0, 40); ax.set_xlabel("배점 (100점)")
ax.grid(axis="y", visible=False)
save(f, "viz/score.png")

# ---------------------------------------------------------------------------
# 수식
render(r"N_{\mathrm{eff}}=1\,\Big/\,\sum_i w_i^{2}\qquad 1\,/\,0.30=3.33", "eq_neff.png", 32, INK, PAPER)
render(r"\hat{\mu}_i=(1-\delta)\,\bar{r}_i+\delta\,\bar{r}", "eq_mu.png", 30, INK, PAPER)
render(r"\max_{w\in\mathcal{W}_{\mathrm{IPS}}}\ \frac{1}{K}\sum_{k=1}^{K}(w-w_k)^{\top}\Sigma\,(w-w_k)"
       r"\quad \mathrm{s.t.}\ \ \mathrm{SR}(w)\geq \mathrm{SR}_{\min}", "eq_adv.png", 28, INK, PAPER)
render(r"\mathrm{TE}_{ab}=\sqrt{(w_a-w_b)^{\top}\Sigma\,(w_a-w_b)}", "eq_te.png", 28, LIME, DARK)
render(r"\mathrm{RC}_i=\frac{w_i\,\mathrm{Cov}(r_i,\,r_p)}{\sigma_p^{2}},\qquad \sum_i \mathrm{RC}_i=1",
       "eq_rc.png", 30, INK, PAPER)
render(r"S_i=\sum_{j\neq i} v_{j\to i},\quad \hat{S}_i=\frac{S_i-\min_k S_k}{\max_k S_k-\min_k S_k},"
       r"\quad \mathrm{Score}_i=\lambda\,\hat{S}_i+(1-\lambda)\,M_i", "eq_score.png", 28, LIME, DARK)
render(r"\mathrm{MAE}_t=\frac{1}{N}\sum_{i=1}^{N}\left|\,\hat{\mu}_{i,t}-r_{i,t}\,\right|", "eq_mae.png", 30, INK, PAPER)
