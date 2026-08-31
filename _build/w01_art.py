# -*- coding: utf-8 -*-
"""W01 강의본의 도해 재생성 — 1600×640 PNG, 덱 팔레트 그대로.

두 장을 다시 그린다.
  ecosystem.png  (슬라이드 4)  — 원본은 오른쪽 "발행자·기업" 상자가 캔버스 밖으로
                                 잘리고 화살표가 글자를 덮었다.
  roadmap.png    (슬라이드 48) — 원본은 옛 주차 번호(W8·W9 / W13–W15 / W16)를 달고
                                 있었고 마지막 카드의 글자가 상자 밖으로 넘쳤다.
새 배치표: LDI·GBI=W7 · 팩터=W12 · 매크로=W13 · 대체=W14 · TPA=W15 · 캡스톤=W16.
"""
import os
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt, font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

W, H = 1600, 640
NAVY, BLUE, GREEN = "#1b2c5e", "#2e5baa", "#3fa36f"
INK, MUTED = "#3b4252", "#6b7280"
PANEL, BLUEP, GREENP = "#f4f5f9", "#eaf1fb", "#e6f5f0"
HAIR = "#d4d9e4"

_FD = os.path.expanduser("~/Library/Fonts")
for _f in ("Pretendard-Regular.otf", "Pretendard-SemiBold.otf", "Pretendard-Bold.otf"):
    fm.fontManager.addfont(os.path.join(_FD, _f))
plt.rcParams["font.family"] = "Pretendard"
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_art", "w01")
os.makedirs(OUT, exist_ok=True)


def canvas():
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.invert_yaxis(); ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


def card(ax, x, y, w, h, fc="white", ec=HAIR, lw=1.6, r=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fc, edgecolor=ec, linewidth=lw))


def t(ax, x, y, s, size=14, color=INK, weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
            fontweight=weight, linespacing=1.5)


def arrow(ax, x0, y0, x1, y1, color=MUTED, lw=2.2, ls="-"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", linestyle=ls,
                                 mutation_scale=16, linewidth=lw, color=color,
                                 shrinkA=0, shrinkB=0))


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=100, facecolor="white")
    plt.close(fig)
    print("saved", p)
    return p


# ── 슬라이드 4 — 자본시장 생태계 ────────────────────────────────
def ecosystem():
    fig, ax = canvas()
    t(ax, W / 2, 34, "자본시장 생태계 — 돈은 위에서 아래로 흐른다", 21, NAVY, "bold")

    M, GAP = 44, 40
    n = 5
    bw = (W - 2 * M - (n - 1) * GAP) / n
    by, bh = 88, 168
    boxes = [
        ("자산소유자", "연기금 · SWF · 보험 · 기금", "자본의 원천 — 정점", NAVY, "white"),
        ("자산운용사", "BlackRock · PIMCO · 미래에셋", "위임 운용 — 대리인", BLUEP, BLUE),
        ("투자은행", "Goldman · MS · KB", "발행 · 주선 · 중개", BLUEP, BLUE),
        ("거래소 · 인프라", "NYSE · KRX · DTCC", "체결 · 청산 · 예탁", GREENP, GREEN),
        ("발행자 · 기업", "자본의 수요자", "실물 경제", PANEL, INK),
    ]
    xs = []
    for i, (title, mid, bot, fc, tc) in enumerate(boxes):
        x = M + i * (bw + GAP)
        xs.append(x)
        ec = NAVY if i == 0 else (GREEN if i == 3 else (BLUE if i in (1, 2) else HAIR))
        card(ax, x, by, bw, bh, fc=fc, ec=ec, lw=1.8)
        cx = x + bw / 2
        body = "white" if i == 0 else INK
        sub = "#cdd6ea" if i == 0 else MUTED
        t(ax, cx, by + 48, title, 18, tc if i else "white", "bold")
        t(ax, cx, by + 98, mid, 14, body)
        t(ax, cx, by + 134, bot, 14, sub)
        if i:
            arrow(ax, x - GAP + 6, by + bh / 2, x - 8, by + bh / 2)

    # 환류 — 오른쪽 끝에서 왼쪽 첫 상자로 돌아오는 점선
    ry = by + bh + 62
    x_last = xs[-1] + bw / 2
    x_first = xs[0] + 34
    ax.plot([x_last, x_last], [by + bh + 6, ry], color=GREEN, lw=2.0, ls=(0, (5, 4)))
    ax.plot([x_first, x_last], [ry, ry], color=GREEN, lw=2.0, ls=(0, (5, 4)))
    arrow(ax, x_first, ry, x_first, by + bh + 6, color=GREEN, lw=2.0, ls=(0, (5, 4)))
    ax.add_patch(plt.Rectangle((W / 2 - 250, ry - 15), 500, 30, facecolor="white",
                               edgecolor="none", zorder=3))
    t(ax, W / 2, ry, "투자 수익의 환류 — 결국 자산소유자에게 돌아온다", 14, GREEN, "bold")

    # 하단 세 카드
    cy, ch = 392, 178
    cw = (W - 2 * M - 2 * GAP) / 3
    cards = [
        ("① 자본의 궁극적 주인", "BlackRock $11조는 BlackRock의 돈이", "아니다 — 최종 책임은 소유자에게"),
        ("② 초장기 시간 지평", "트레이더 ms · 헤지펀드 분기 · 연기금", "10~30년 · SWF 영구 — 자유도의 원천"),
        ("③ 실질적 시장 조성자", "지수 가중 · 거버넌스 관례 · ESG 표준 —", "GPFG의 제외 리스트가 곧 신호다"),
    ]
    for i, (h1, l1, l2) in enumerate(cards):
        x = M + i * (cw + GAP)
        card(ax, x, cy, cw, ch, fc=PANEL, ec=HAIR, lw=1.4)
        cx = x + cw / 2
        t(ax, cx, cy + 48, h1, 17, NAVY, "bold")
        t(ax, cx, cy + 100, l1, 14, INK)
        t(ax, cx, cy + 134, l2, 14, INK)
    return save(fig, "ecosystem.png")


# ── 슬라이드 48 — 커리큘럼 로드맵 ──────────────────────────────
def roadmap():
    fig, ax = canvas()
    t(ax, W / 2, 34, "커리큘럼에서 오늘의 위치 — 1주", 21, NAVY, "bold")

    M, GAP = 44, 40
    n = 5
    bw = (W - 2 * M - (n - 1) * GAP) / n
    by, bh = 108, 250
    steps = [
        ("W1 · 오늘", "시장 개요와 자산소유자",
         ["누가 장기 자본의 주인인가", "4대 참여자 · 4유형 · 거버넌스"], NAVY, "white", NAVY),  # 오늘
        ("W2–W3", "CAPM · SAA · CMA",
         ["왜 SAA가 91.5%를 정하는가", "연기금 3대 모델과 CMA"], BLUE, BLUEP, BLUE),
        ("W7", "LDI · GBI",
         ["DB의 부채 매칭 — LDI", "DC의 목표 설계 — GBI"], GREEN, GREENP, GREEN),
        ("W12–W14", "팩터 · 매크로 · 대체",
         ["팩터 선별 3대 기준", "비유동성 프리미엄"], NAVY, PANEL, HAIR),
        ("W15–W16", "TPA · 캡스톤",
         ["CPPIB의 길 · CalPERS의 시험", "KIC의 선택 — 오늘 질문의 답"], NAVY, PANEL, HAIR),
    ]
    for i, (chip, title, lines, chipc, fc, ec) in enumerate(steps):
        x = M + i * (bw + GAP)
        card(ax, x, by, bw, bh, fc=fc, ec=ec, lw=1.8)
        cx = x + bw / 2
        # 상단 칩
        chw, chh = bw * 0.62, 44
        card(ax, cx - chw / 2, by - 22, chw, chh, fc=chipc, ec=chipc, r=10)
        t(ax, cx, by, chip, 15, "white", "bold")
        tc = BLUE if i == 1 else (GREEN if i == 2 else NAVY)
        body = INK
        t(ax, cx, by + 92, title, 17, tc, "bold")
        t(ax, cx, by + 148, lines[0], 13, body)
        t(ax, cx, by + 182, lines[1], 13, body)
        if i:
            arrow(ax, x - GAP + 6, by + bh / 2, x - 8, by + bh / 2)

    yb, hb = 436, 86
    card(ax, M + 120, yb, W - 2 * M - 240, hb, fc="white", ec=NAVY, lw=1.8)
    t(ax, W / 2, yb + hb / 2,
      "오늘 던진 질문 — “우리는 누구의 돈을 운용하는가” — 가 16주 전체를 관통한다",
      16, NAVY, "bold")
    return save(fig, "roadmap.png")


if __name__ == "__main__":
    ecosystem()
    roadmap()
