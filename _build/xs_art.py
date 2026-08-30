# -*- coding: utf-8 -*-
"""XS 프라이머의 그림 — 자율주행 포트폴리오(독립세션).

다른 주차와 달리 이 세션의 숫자는 지어낸 예시가 아니라
2026-08-22 본 강의 시뮬레이션의 실제 산출값이다. 각 그림에 그렇게 적는다.
"""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("xs")
RUN = "2026-08-22 본 강의 시뮬레이션 · 자산 11개 · 학습 84개월 / 평가 35개월"

# 실제 산출값
CAND = ["MVO", "블랙-리터맨", "리스크 패리티"]
NEFF = [3.93, 5.53, 9.92]          # 유효 종목 수
EXP = [5.93, 2.33, 5.25]           # 기대 수익(%)
REAL = [8.58, 4.80, 7.43]          # 실현 수익(%)
VOTE = [None, 22.50, 35.96]        # 표결 점수 (None = 자동 기각)
FLOOR = 4.0


# ── 여섯 층 (SVG) ────────────────────────────────────────────────
def layers():
    b = text(800, 44, "논문이 말하는 여섯 층 — 우리가 16주 동안 해온 일과 겹친다", 30, INK, bold=True)
    rows = [("거버넌스", "ips-guardian", "투자정책서가 전 과정을 제약한다", "W01 · W15", TEAL),
            ("입력", "cma-builder", "기대수익과 공분산을 만든다", "W03", BLUE),
            ("구성", "alloc-mvo · bl · riskparity", "여러 방법이 경쟁한다", "W04 · W05", BLUE),
            ("비평·투표", "ic-critic", "심사하고 표결한다", "16주 내내의 IC", LIME),
            ("탐색", "(MVP에서는 생략)", "새 방법을 제안한다", "W12 · W13", HAIR),
            ("자기개선", "meta-reviewer", "예측을 실현과 대조한다", "W09", BLUE)]
    for i, (layer, agent, does, week, c) in enumerate(rows):
        y = 92 + i * 82
        fill = LIME if c == LIME else WHITE
        st = INK if c == LIME else HAIR
        b += (f'<rect x="60" y="{y}" width="1480" height="68" rx="8" fill="{fill}" '
              f'stroke="{st}" stroke-width="{3 if c == LIME else 2}"/>')
        tc = DARK if c == LIME else INK
        b += text(90, y + 45, layer, 29, tc, "start", True)
        b += text(400, y + 44, agent, 25, DARK if c == LIME else TEAL, "start")
        b += text(880, y + 44, does, 25, DARK if c == LIME else MUTED, "start")
        b += text(1510, y + 44, week, 25, tc, "end", True)
    b += text(800, 606, "새 이론을 배우는 세션이 아니다 — 해온 일을 자동화하면 무엇이 남는지 보는 세션이다",
              27, RED, bold=True)
    return svg("layers.png", b)


# ── 에이전트란 무엇인가 (SVG) ───────────────────────────────────
def agent():
    """낱말부터 세운다 — 에이전트는 역할·입력·출력이 문서로 적힌 일꾼이다."""
    b = text(800, 44, "에이전트(agent)는 역할이 문서로 적힌 일꾼이다", 30, INK, bold=True)
    b += text(800, 84, "사람 운용역의 직무기술서를 그대로 옮겨 적은 것에 가깝다", 26, MUTED)
    b += limebox(70, 150, 400, 300, "alloc-mvo", ["에이전트 하나의 예"])
    rows = [("맡은 일", "평균-분산 최적화로 포트폴리오를 짠다"),
            ("받는 것", "자본시장 가정(CMA)과 투자정책서(IPS)"),
            ("내놓는 것", "자산별 비중 — 파일 하나로 남긴다"),
            ("지킬 것", "투자정책서의 제약을 어기면 스스로 물러난다")]
    for k, (label, desc) in enumerate(rows):
        y = 150 + k * 78
        b += (f'<rect x="530" y="{y}" width="1000" height="64" rx="8" fill="{WHITE}" '
              f'stroke="{HAIR}" stroke-width="2"/>')
        b += text(560, y + 42, label, 27, TEAL, "start", True)
        b += text(760, y + 42, desc, 25, INK, "start")
    b += text(800, 510, "일곱 에이전트가 이런 문서를 하나씩 갖고 서로 주고받는다",
              27, INK, bold=True)
    b += text(800, 552, "이렇게 여럿이 역할을 나눠 일하는 구조를 멀티 에이전트 시스템이라 부른다",
              27, RED, bold=True)
    b += text(800, 594, "새 조직을 만드는 것이 아니라, 지금 조직의 역할을 문서로 내려놓는 일이다", 25, MUTED)
    return svg("agent.png", b)


# ── 투자정책서란 무엇인가 (SVG) ─────────────────────────────────
def ips():
    b = text(800, 44, "투자정책서(IPS)는 이 기금 하나에만 적용되는 내부 규정이다", 30, INK, bold=True)
    b += text(800, 84, "나라의 경제정책이 아니라, 이사회가 정해 문서로 남긴 운용의 규칙이다", 26, MUTED)
    cells = [("무엇을 이루려 하나", ["목표 수익 · 감내할 손실"], TEAL),
             ("무엇을 넘지 말아야 하나", ["자산별 상·하한", "유효 종목 수 4.0 이상"], BLUE),
             ("무엇을 하면 안 되나", ["금지 자산 · 레버리지 한도"], AMBER),
             ("누가 언제 확인하나", ["보고 주기 · 승인 절차"], RED)]
    for k, (title_, lines, c) in enumerate(cells):
        x = 60 + (k % 2) * 760
        y = 130 + (k // 2) * 200
        b += (f'<rect x="{x}" y="{y}" width="720" height="170" rx="12" fill="{WHITE}" '
              f'stroke="{c}" stroke-width="3"/>')
        b += text(x + 360, y + 56, title_, 29, c, bold=True)
        for m, ln in enumerate(lines):
            b += text(x + 360, y + 104 + m * 38, ln, 25, INK)
    b += darkbox(300, 522, 1000, 84, "이 세션에서는 이 문서를 ips.md 라는 파일 하나로 둔다",
                 ["일곱 에이전트가 모두 이 파일을 읽고 그 안에서만 움직인다"])
    return svg("ips.png", b)


# ── 왜 하나가 아니라 여럿인가 (SVG) ─────────────────────────────
def why_multi():
    """멀티 에이전트의 핵심 — 성능이 아니라 역할 분리와 견제다."""
    b = text(800, 44, "왜 똑똑한 모형 하나가 아니라 여럿인가", 30, INK, bold=True)
    b += text(800, 84, "성능 때문이 아니라 책임을 나누기 위해서다", 26, MUTED)
    b += (f'<rect x="60" y="130" width="700" height="330" rx="12" fill="{WHITE}" '
          f'stroke="{HAIR}" stroke-width="2"/>')
    b += text(410, 190, "모형 하나가 다 한다", 32, MUTED, bold=True)
    b += hrule(110, 710, 214, HAIR, 2)
    for i, ln in enumerate(["왜 그렇게 정했는지 알 수 없다",
                            "짜는 쪽과 검사하는 쪽이 같다",
                            "고치려면 통째로 바꿔야 한다"]):
        b += text(410, 272 + i * 52, ln, 26, INK)
    b += text(410, 434, "사람 조직으로 치면 1인 회사다", 24, RED)
    b += (f'<rect x="840" y="130" width="700" height="330" rx="12" fill="{LIME}" '
          f'stroke="{INK}" stroke-width="3"/>')
    b += text(1190, 190, "역할을 나눈 여럿", 32, DARK, bold=True)
    b += hrule(890, 1490, 214, DARK, 2)
    for i, ln in enumerate(["각자 맡은 범위가 문서에 적혀 있다",
                            "짜는 에이전트와 심사하는 에이전트가 다르다",
                            "하나만 고쳐도 된다"]):
        b += text(1190, 272 + i * 52, ln, 25, DARK)
    b += text(1190, 434, "운용역과 리스크 부서를 나누는 이유와 같다", 24, DARK)
    b += text(800, 528, "그래서 이 일은 더 똑똑한 모형을 만드는 일이 아니라 구조를 설계하는 일이 된다",
              28, INK, bold=True)
    b += text(800, 590, "핵심은 똑똑함이 아니라 견제다 — 짜는 자가 스스로를 심사하지 않는다",
              27, RED, bold=True)
    return svg("why_multi.png", b)


# ── 전체 구조 (SVG) ─────────────────────────────────────────────
def architecture():
    """일곱 에이전트가 무엇을 받아 무엇을 내놓는지 — 구조 전체를 한 장에."""
    W, H = 1800, 730

    def node(x, y, w, h, name, role, fill=WHITE, stroke=HAIR, tc=INK, sc=MUTED, sw=2):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="{sw}"/>'
                + text(x + w / 2, y + 42, name, 26, tc, bold=True)
                + text(x + w / 2, y + 76, role, 21, sc))

    b = text(900, 40, "일곱 에이전트가 무엇을 받아 무엇을 내놓는가", 31, INK, bold=True)

    # 모두를 묶는 투자정책서
    b += f'<rect x="60" y="70" width="1680" height="66" rx="10" fill="{DARK}"/>'
    b += text(900, 112, "투자정책서 IPS (ips.md) — 일곱 에이전트가 모두 이 문서를 읽고 그 안에서만 움직인다",
              25, LIME, bold=True)
    for x in (300, 700, 1100, 1500):
        b += f'<line x1="{x}" y1="136" x2="{x}" y2="168" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>'

    # ① 입력
    b += text(175, 200, "① 입력", 23, MUTED, bold=True)
    b += node(60, 214, 230, 106, "cma-builder", "기대수익·공분산", stroke=BLUE, tc=BLUE)

    # ② 구성 — 셋이 나란히 경쟁
    b += text(475, 200, "② 구성 — 셋이 겨룬다", 23, MUTED, bold=True)
    for k, (nm, role) in enumerate([("alloc-mvo", "평균-분산"),
                                    ("alloc-bl", "블랙-리터맨"),
                                    ("alloc-riskparity", "위험기여 균등")]):
        y = 214 + k * 118
        b += node(370, y, 250, 100, nm, role, stroke=TEAL, tc=TEAL)
        b += arrow(300, 267, 360, y + 50, MUTED, "aM", 3)
        b += arrow(630, y + 50, 700, 267, MUTED, "aM", 3)

    # ③ 정책 검사 → 심사·표결
    b += text(790, 200, "③ 검사와 표결", 23, MUTED, bold=True)
    b += node(710, 214, 180, 106, "ips-guardian", "정책 위반 판정", stroke=RED, tc=RED)
    b += arrow(898, 267, 958, 267, MUTED, "aM", 4)
    b += node(968, 214, 210, 106, "ic-critic", "네 관점 표결", stroke=TEAL, tc=TEAL)
    b += arrow(1186, 267, 1246, 267, TEAL, "aT", 4)
    b += (f'<rect x="1256" y="214" width="180" height="106" rx="10" fill="{LIME}" '
          f'stroke="{INK}" stroke-width="3"/>')
    b += text(1346, 256, "채택안", 26, DARK, bold=True)
    b += text(1346, 290, "이번 사이클의 답", 21, DARK)

    # ④ 대조 — 되먹임
    b += text(1620, 200, "④ 대조", 23, MUTED, bold=True)
    b += node(1500, 214, 240, 106, "meta-reviewer", "예측 대 실현", stroke=BLUE, tc=BLUE)
    b += arrow(1444, 267, 1492, 267, MUTED, "aM", 4)
    # 되먹임 — 상자 아래로 크게 돌아 cma-builder 밑면으로 들어간다
    b += (f'<path d="M1620 330 v240 q0 40 -40 40 H215 q-40 0 -40 -40 v-200" '
          f'fill="none" stroke="{TEAL}" stroke-width="4" marker-end="url(#aT)"/>')
    b += text(900, 648, "빗나간 곳을 찾아 다음 사이클의 가정과 규칙을 고치자고 제안한다",
              25, TEAL, bold=True)
    b += hrule(60, 1740, 676, HAIR, 2)
    b += text(900, 716, "짜는 에이전트와 심사하는 에이전트가 다르다 — 이 분리가 구조의 핵심이다",
              27, RED, bold=True)
    return svg("architecture.png", b, W, H)


# ── 자율주행 단계 (SVG) ─────────────────────────────────────────
def autonomy():
    """자동차의 자율주행 단계에 빗대어 이 세션이 어느 단계인지 못 박는다."""
    b = text(800, 44, "“자율주행”은 사람이 빠진다는 뜻이 아니다", 30, INK, bold=True)
    b += text(800, 84, "자동차처럼 단계가 있고, 이 세션이 다루는 것은 그중 하나다", 26, MUTED)
    lv = [("0단계", "사람이 다 한다", "지금 대부분의 기금", 210, HAIR, INK),
          ("1단계", "계산만 기계가 한다", "엑셀 · 최적화 도구", 400, HAIR, INK),
          ("2단계", "후보까지 기계가 만든다", "사람이 고르고 판단한다", 590, HAIR, INK),
          ("3단계", "제안까지 기계, 승인은 사람", "이 세션이 다루는 곳", 900, LIME, DARK),
          ("4단계", "사람 없이 굴린다", "아직 아무도 못 한다", 980, DARK, LIME)]
    for k, (name, what, note, w, fill, tc) in enumerate(lv):
        y = 128 + k * 88
        st = INK if fill == LIME else (DARK if fill == DARK else HAIR)
        b += (f'<rect x="230" y="{y}" width="{w}" height="66" rx="8" fill="{fill}" '
              f'stroke="{st}" stroke-width="{3 if fill == LIME else 2}"/>')
        b += text(200, y + 44, name, 27, INK, "end", True)
        b += text(258, y + 43, what, 26, tc, "start", True)
        b += text(250 + w + 24, y + 43, note, 24,
                  INK if fill == LIME else MUTED, "start")
    b += text(800, 596, "3단계에서는 판단의 자리가 남는다 — 무엇을 승인하고 무엇을 되돌릴지",
              28, RED, bold=True)
    return svg("autonomy.png", b)


# ── 한 사이클 (SVG) ─────────────────────────────────────────────
def cycle():
    b = text(800, 44, "한 사이클은 네 걸음으로 돈다", 30, INK, bold=True)
    b += text(800, 84, "우리가 16주 동안 사람으로 해온 순서와 같다", 26, MUTED)
    steps = [("① 자본시장 가정", "cma-builder", "기대수익·공분산을 만든다", "W03", WHITE),
             ("② 포트폴리오 구성", "alloc-mvo · bl · rp", "세 방법이 각자 짠다", "W04 · W05", WHITE),
             ("③ 심사와 표결", "ic-critic", "투자정책서 위반을 걸러낸다", "4교시 IC", WHITE),
             ("④ 예측 대 실현", "meta-reviewer", "빗나간 곳을 찾아낸다", "W09", LIME)]
    for k, (t0, agent_, does, week, fill) in enumerate(steps):
        x = 45 + k * 385
        st = INK if fill == LIME else HAIR
        tc = DARK if fill == LIME else INK
        sc = DARK if fill == LIME else MUTED
        b += (f'<rect x="{x}" y="150" width="345" height="250" rx="12" fill="{fill}" '
              f'stroke="{st}" stroke-width="{3 if fill == LIME else 2}"/>')
        b += text(x + 172, 200, t0, 28, tc, bold=True)
        b += text(x + 172, 246, agent_, 23, DARK if fill == LIME else TEAL)
        b += text(x + 172, 300, does, 24, sc)
        b += text(x + 172, 360, week, 25, tc, bold=True)
        if k < 3:
            b += arrow(x + 352, 275, x + 424, 275, MUTED, "aM", 5)
    b += f'<path d="M1580 400 q40 90 -60 90 H210 q-100 0 -60 -90" fill="none" stroke="{TEAL}" stroke-width="4" marker-end="url(#aT)"/>'
    b += text(800, 540, "④에서 찾아낸 것이 다음 사이클의 ①을 고친다", 28, TEAL, bold=True)
    b += text(800, 588, "이 되먹임이 “자율주행”이라 부르는 부분이다", 26, MUTED)
    return svg("cycle.png", b)


# ── 정책이 후보 하나를 걸러 냈다 ─────────────────────────────────
def screen():
    fig, ax = plt.subplots(figsize=WIDE)
    cols = [RED, BLUE, LIME]
    ax.bar(range(3), NEFF, color=cols, width=.55,
           edgecolor=[INK if c == LIME else "none" for c in cols], linewidth=1.4)
    for i, v in enumerate(NEFF):
        ax.text(i, v + .18, f"{v:.2f}", ha="center", fontsize=22, color=INK, fontweight="bold")
    ax.axhline(FLOOR, color=INK, lw=2.4, ls="--")
    ax.text(-0.45, FLOOR + .30, f"정책이 정한 하한 {FLOOR:.1f}", fontsize=17,
            color=INK, fontweight="bold", ha="left")
    ax.annotate("하한을 밑돌아 자동 기각", (0, NEFF[0]), xytext=(0, -70),
                textcoords="offset points", ha="center", fontsize=17,
                color=RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax.set_xticks(range(3)); ax.set_xticklabels(CAND, fontsize=18)
    ax.set_ylabel("유효 종목 수 — 얼마나 고르게 나눠 담았나", fontsize=15)
    ax.set_ylim(0, 11.6)
    clean(ax)
    fig.tight_layout()
    return save(fig, "screen.png", RUN)


# ── 기각된 안이 가장 많이 벌었다 ─────────────────────────────────
def discipline():
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=WIDE)
    ax.bar(x - .19, EXP, .38, color=MUTED, label="처음에 기대한 수익")
    ax.bar(x + .19, REAL, .38, color=[RED, BLUE, LIME],
           edgecolor=[("none"), ("none"), INK], linewidth=1.4,
           label="실제로 나온 수익")
    for i in x:
        ax.text(i - .19, EXP[i] + .18, f"{EXP[i]:.2f}", ha="center", fontsize=15, color=INK)
        ax.text(i + .19, REAL[i] + .18, f"{REAL[i]:.2f}", ha="center", fontsize=16,
                color=INK, fontweight="bold")
    gap = REAL[0] - REAL[2]
    ax.annotate("", xy=(0.19, REAL[0]), xytext=(2.19, REAL[2]),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.2, ls=":"))
    ax.text(1.2, 9.3, f"규율을 지킨 대가  {gap:.2f}%p", ha="center", fontsize=19,
            color=RED, fontweight="bold")
    ax.text(1.2, 8.6, "기각된 안이 실제로는 가장 많이 벌었다", ha="center",
            fontsize=16, color=MUTED)
    ax.set_xticks(x); ax.set_xticklabels(CAND, fontsize=18)
    ax.set_ylabel("연 수익률(%)", fontsize=15)
    ax.set_ylim(0, 10.4)
    ax.legend(fontsize=15.5, frameon=False, loc="upper left")
    clean(ax)
    fig.tight_layout()
    return save(fig, "discipline.png", RUN)


# ── 표결 결과 ────────────────────────────────────────────────────
def vote():
    """세로 위치 2·1·0에 MVO·블랙-리터맨·리스크 패리티를 그대로 대응시킨다.
    (전에 값만 뒤집어 넣어 MVO가 채택된 것처럼 보였다)"""
    ypos = [2, 1, 0]
    vals = [0 if v is None else v for v in VOTE]
    cols = [HAIR, BLUE, LIME]
    labs = ["정책을 못 넘어 표결에 오르지 못함",
            f"{VOTE[1]:.2f}", f"{VOTE[2]:.2f}   채택"]
    fig, ax = plt.subplots(figsize=WIDE)
    for y, v, c in zip(ypos, vals, cols):
        ax.barh([y], [v], color=c, height=.5,
                edgecolor=INK if c == LIME else "none", linewidth=1.4)
    for y, v, lab, c in zip(ypos, vals, labs, cols):
        ax.text(v + .8, y, lab, va="center", fontsize=19,
                color=MUTED if c == HAIR else INK, fontweight="bold")
    ax.set_yticks(ypos); ax.set_yticklabels(CAND, fontsize=18)
    ax.set_xlabel("네 관점을 합친 표결 점수", fontsize=15)
    ax.set_xlim(0, 52); ax.set_ylim(-.95, 2.6)
    ax.text(26, -.72, "정책을 통과한 둘만 표결에 올랐고, 가장 고르게 나눈 안이 이겼다",
            ha="center", fontsize=17, color=INK, fontweight="bold")
    clean(ax, grid="x")
    fig.tight_layout()
    return save(fig, "vote.png", RUN)


# ── 메타 에이전트와 킬스위치 (SVG) ─────────────────────────────
def human():
    b = text(800, 44, "스스로 고치겠다는 제안은 사람이 승인해야 반영된다", 30, INK, bold=True)
    b += text(800, 84, "이 승인 절차를 킬스위치(kill switch)라 부른다", 26, MUTED)
    b += box(50, 150, 380, 150, "meta-reviewer", ["예측과 실현을 대조하는", "메타 에이전트"],
             stroke=TEAL, tc=TEAL, sc=INK, ts=27, ss=24)
    b += arrow(440, 225, 520, 225, MUTED, "aM", 5)
    b += box(540, 150, 380, 150, "지시문을 고치자", ["다른 에이전트의 규칙을", "바꾸자는 제안"],
             stroke=HAIR, ts=27, ss=24)
    b += arrow(930, 225, 1010, 225, RED, "aR", 5)
    b += (f'<rect x="1030" y="150" width="240" height="150" rx="12" fill="{RED}"/>')
    b += text(1150, 212, "킬스위치", 30, WHITE, bold=True)
    b += text(1150, 254, "자동 반영 금지", 23, WHITE)
    b += arrow(1280, 225, 1350, 225, TEAL, "aT", 5)
    b += limebox(1370, 150, 180, 150, "사람", ["승인"])
    b += hrule(50, 1550, 350, HAIR, 2)
    b += text(800, 412, "메타 에이전트는 스스로를 고치는 층이다 — 논문에서 가장 강력하고 가장 위험한 부분이다",
              27, INK, bold=True)
    b += text(800, 458, "고칠수록 좋아지는지, 고칠수록 자기 실수를 굳히는지 알기 어렵기 때문이다", 25, MUTED)
    b += text(800, 530, "그래서 투자정책서에 “자동 반영 금지” 조항을 두고 사람의 승인을 요구한다",
              27, TEAL, bold=True)
    b += text(800, 590, "자동화가 지운 것은 계산이고, 남긴 것은 책임이다", 28, RED, bold=True)
    return svg("human.png", b)


# ── 수식 ─────────────────────────────────────────────────────────
def equation():
    return eq_png(r"$N_{eff}\;=\;\left(\,w_1^{2}+w_2^{2}+\cdots+w_n^{2}\,\right)^{-1}$"
                  , fontsize=42, width=10.0)


if __name__ == "__main__":
    agent(); why_multi(); layers(); architecture(); autonomy(); cycle(); ips()
    screen(); discipline(); vote()
    human(); equation()
    print("끝.")
