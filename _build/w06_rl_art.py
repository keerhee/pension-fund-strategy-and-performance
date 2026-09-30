# -*- coding: utf-8 -*-
"""W06 보강 — 처음 배우는 강화학습의 그림.

실행: ../.venv/bin/python w06_rl_art.py   (→ _art/w06rl/)
원천: 보충교재/14_강화학습포트폴리오 (본편 II · 기초 부록 · 워크북)를 비전공생용으로 각색.
"""
import numpy as np
from matplotlib import pyplot as plt
from primer_lib import (out_dir, save, clean, svg, box, limebox, darkbox,
                        arrow, text, hrule, vrule, equation as eq_png, WIDE,
                        INK, PAPER, WHITE, LIME, TEAL, RED, BLUE, AMBER, MUTED, HAIR, DARK)

OUT = out_dir("w06rl")
FIG = (10.6, 4.2)   # WIDE보다 작게 그려 슬라이드에서 글씨가 1.2배 커지게
EX = "수업용으로 지어낸 예시입니다"
SIM = "컴퓨터로 만든 가상 실험입니다"


def sub(base, s):
    """아래첨자 — 유니코드 첨자는 글꼴에 없어서 tspan으로 내린다(문장 끝에만 쓴다)."""
    return f'{base}<tspan dy="8" font-size="0.66em">{s}</tspan>'


def cbox(x, y, w, h, title, subs=(), kind="white", stroke=HAIR, ts=34, ss=25):
    """제목·부제를 세로 가운데에 놓는 상자 (primer_lib.box는 위에 붙는다)."""
    fill, tc, sc = {"white": (WHITE, INK, MUTED), "dark": (DARK, LIME, "#B8C6C8"),
                    "lime": (LIME, DARK, DARK)}[kind]
    st = {"dark": DARK, "lime": INK}.get(kind, stroke)
    lh = ss * 1.45
    block = ts + (len(subs) * lh + 10 if subs else 0)
    top = y + (h - block) / 2 + ts * 0.85
    b = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" '
         f'stroke="{st}" stroke-width="2.5"/>')
    b += text(x + w / 2, top, title, ts, tc, bold=True)
    for i, t in enumerate(subs):
        b += text(x + w / 2, top + 12 + (i + 1) * lh, t, ss, sc)
    return b


def curve(x1, y1, cx, cy, x2, y2, color=TEAL, mk="aT", wt=5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{color}" '
            f'stroke-width="{wt}"{d} marker-end="url(#{mk})"/>')


# ── 1. 핵심 피드백 고리 ─────────────────────────────────────────
def loop(name="loop.png", agent=("에이전트", "결정하는 쪽", "규칙(정책)을 가진다"),
         env=("환경", "바깥 세상 전부", "규칙은 알려 주지 않는다"),
         act=("행동  a", "무엇을 할지 고른다"), st=("다음 상태  s′", "바뀐 상황을 보여 준다"),
         rw=("보상  r", "방금 한 일의 점수"), learn="보상을 보고 규칙을 고친다 = 학습",
         foot="이 고리가 수천·수만 번 돈다 — 점수의 합이 커지도록 규칙을 고쳐 가는 것이 강화학습"):
    b = cbox(40, 130, 470, 300, agent[0], agent[1:], "dark", ts=42, ss=30)
    b += cbox(1090, 130, 470, 300, env[0], env[1:], "white", stroke=TEAL, ts=42, ss=30)
    b += curve(510, 175, 800, 55, 1082, 175, TEAL, "aT", 5)
    b += text(800, 44, act[0], 38, TEAL, bold=True)
    b += text(800, 86, act[1], 29, MUTED)
    b += f'<line x1="1090" y1="272" x2="522" y2="272" stroke="{BLUE}" stroke-width="5" marker-end="url(#aM)"/>'
    b += f'<line x1="1090" y1="392" x2="522" y2="392" stroke="{RED}" stroke-width="5" marker-end="url(#aR)"/>'
    b += text(806, 254, st[0], 34, BLUE, bold=True)
    b += text(806, 310, st[1], 28, MUTED)
    b += text(806, 374, rw[0], 34, RED, bold=True)
    b += text(806, 430, rw[1], 28, MUTED)
    b += curve(420, 434, 275, 520, 130, 438, AMBER, "aM", 4, dash="10,8")
    b += text(275, 526, learn, 28, INK, bold=True)
    b += text(1325, 474, "한 칸 시간이 흐른다: t → t+1", 26, MUTED)
    b += text(800, 580, foot, 30, RED, bold=True)
    return svg(name, b, h=600)


def loop_pension():
    return loop("loop_pension.png",
                agent=("기금 운용 규칙", "에이전트 = 운용 프로그램", "상태를 보고 비중을 정한다"),
                env=("시장 + 기금 계좌", "금리·주가·보험료·급여", "내 결정과 무관하게 움직임"),
                act=("행동: 이번 달 비중", "주식 40% → 45%? 채권을 늘릴까?"),
                st=("다음 상태", "금리·변동성·현재 비중·적립 수준"),
                rw=("보상", "비용 뺀 수익 − 위험 벌점"),
                learn="수익·손실을 보고 규칙을 고친다",
                foot="보상을 무엇으로 정하느냐가 곧 운용 철학이다 — 수익만? 낙폭까지? 비용까지?")


# ── 2. 한 에피소드 = 이어지는 선택 ─────────────────────────────
def episode():
    xs = [190, 590, 990, 1390]
    months = ["1월", "2월", "3월", "4월"]
    states = ["금리↑ 변동성↓", "금리↑ 변동성↑", "금리↓ 변동성↑", "금리↓ 변동성↓"]
    acts = ["주식 50%", "주식 40%", "주식 40%"]
    rews = ["+0.8", "−0.3", "+0.5"]
    b = ""
    for i, x in enumerate(xs):
        b += cbox(x - 160, 10, 320, 170, months[i], ["상태", states[i]], stroke=BLUE, ts=36, ss=27)
        if i < 3:
            b += f'<rect x="{x-130}" y="232" width="260" height="76" rx="10" fill="{TEAL}"/>'
            b += text(x, 282, acts[i], 32, WHITE, bold=True)
            b += f'<line x1="{x}" y1="182" x2="{x}" y2="226" stroke="{TEAL}" stroke-width="4" marker-end="url(#aT)"/>'
            b += arrow(x + 132, 270, xs[i + 1] - 162, 150, MUTED, "aM", 4)
            mx = (x + xs[i + 1]) / 2
            b += f'<rect x="{mx-78}" y="186" width="156" height="42" rx="8" fill="{PAPER}"/>'
            b += text(mx, 219, f"보상 {rews[i]}", 30, RED, bold=True)
    b += text(1390, 282, "계속…", 32, MUTED)
    b += text(800, 400, "오늘 고른 비중이 내일의 출발점(상태)이 된다", 32, INK)
    b += text(800, 452, "그래서 ‘한 번 예측’이 아니라 ‘이어지는 선택’이다", 32, INK)
    b += text(800, 530, "목표는 한 달 점수가 아니라 끝까지 받은 점수의 합", 34, RED, bold=True)
    return svg("episode.png", b, h=570)


# ── 3. 할인계수 ──────────────────────────────────────────────────
def discount():
    k = np.arange(0, 21)
    fig, ax = plt.subplots(figsize=FIG)
    w = .27
    for j, (g, c, lab) in enumerate([(0.5, RED, "γ = 0.5  근시안 — 3달 뒤면 거의 무시"),
                                     (0.9, AMBER, "γ = 0.9  적당히 — 10달 뒤 0.35"),
                                     (0.99, TEAL, "γ = 0.99  멀리 봄 — 20달 뒤도 0.82")]):
        ax.bar(k + (j - 1) * w, g ** k, width=w, color=c, label=lab)
    ax.set_xlabel("몇 번 뒤에 받는 보상인가 (k)", fontsize=15)
    ax.set_ylabel(r"오늘 가치로 친 무게 $\gamma^k$", fontsize=15)
    ax.set_xticks(range(0, 21, 2))
    ax.set_ylim(0, 1.42)
    ax.set_yticks([0, .2, .4, .6, .8, 1.0])
    ax.legend(fontsize=16, frameon=False, loc="upper right", ncol=1)
    clean(ax)
    fig.tight_layout()
    return save(fig, "discount.png", "할인 무게를 그대로 그린 그림입니다")


# ── 4. 미로: 가치 지도와 정책 ───────────────────────────────────
ROWS, COLS = 4, 6
GOAL, TRAP = (0, 5), (1, 5)
WALLS = {(1, 1), (2, 3), (1, 3)}
START = (3, 0)
STEP, GAMMA = -0.4, 0.9
MOVES = {"↑": (-1, 0), "↓": (1, 0), "←": (0, -1), "→": (0, 1)}


def step_env(s, a):
    if s in (GOAL, TRAP):
        return s, 0.0, True
    r, c = s[0] + MOVES[a][0], s[1] + MOVES[a][1]
    if not (0 <= r < ROWS and 0 <= c < COLS) or (r, c) in WALLS:
        r, c = s
    n = (r, c)
    if n == GOAL:
        return n, 10.0, True
    if n == TRAP:
        return n, -10.0, True
    return n, STEP, False


def value_iteration():
    V = np.zeros((ROWS, COLS))
    for _ in range(200):
        V2 = V.copy()
        for r in range(ROWS):
            for c in range(COLS):
                s = (r, c)
                if s in WALLS or s in (GOAL, TRAP):
                    continue
                best = -1e9
                for a in MOVES:
                    n, rew, done = step_env(s, a)
                    best = max(best, rew + (0 if done else GAMMA * V[n]))
                V2[r, c] = best
        V = V2
    pol = {}
    for r in range(ROWS):
        for c in range(COLS):
            s = (r, c)
            if s in WALLS or s in (GOAL, TRAP):
                continue
            q = {}
            for a in MOVES:
                n, rew, done = step_env(s, a)
                q[a] = rew + (0 if done else GAMMA * V[n])
            pol[s] = max(q, key=q.get)
    return V, pol


def _grid(ax, V, pol=None, show_val=True, ok=None, title=None, tc=INK, shade=None, nums=True):
    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list("v", ["#F6D6D6", "#FFFFFF", "#CFE8E6", TEAL])
    vmax = 10
    for r in range(ROWS):
        for c in range(COLS):
            s = (r, c)
            y = ROWS - 1 - r
            if s in WALLS:
                fc = "#9AA5A9"
            elif s == GOAL:
                fc = LIME
            elif s == TRAP:
                fc = RED
            else:
                fc = cmap((V[r, c] + 2) / (vmax + 2)) if (show_val if shade is None else shade) else WHITE
            ax.add_patch(plt.Rectangle((c, y), 1, 1, fc=fc, ec=HAIR, lw=2))
            if s == GOAL:
                ax.text(c + .5, y + .5, "목표\n+10", ha="center", va="center", fontsize=15, fontweight="bold", color=DARK)
            elif s == TRAP:
                ax.text(c + .5, y + .5, "함정\n−10", ha="center", va="center", fontsize=15, fontweight="bold", color=WHITE)
            elif s in WALLS:
                ax.text(c + .5, y + .5, "벽", ha="center", va="center", fontsize=15, color=WHITE)
            else:
                if show_val and nums:
                    ax.text(c + .5, y + .5, f"{V[r, c]:.1f}", ha="center", va="center", fontsize=17,
                            color=WHITE if V[r, c] > 6 else INK, fontweight="bold")
                if pol is not None:
                    col = INK if ok is None else (TEAL if ok[s] else RED)
                    ax.text(c + .5, y + .5, pol[s], ha="center", va="center", fontsize=30,
                            color=col, fontweight="bold")
            if s == START:
                ax.text(c + .08, y + .1, "출발", fontsize=12, color=BLUE, fontweight="bold")
    ax.set_xlim(0, COLS); ax.set_ylim(0, ROWS); ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, fontsize=18, color=tc, pad=10, fontweight="bold")


def gridworld():
    V, pol = value_iteration()
    fig, axes = plt.subplots(1, 2, figsize=FIG)
    _grid(axes[0], V, None, True, title="가치 V — 여기서 출발하면 앞으로 받을 점수")
    _grid(axes[1], V, pol, False, title="정책 π — 칸마다 가치가 큰 쪽으로")
    fig.text(.5, .015, "한 걸음마다 −0.4 · 할인 γ = 0.9 · 목표 +10 · 함정 −10  →  가치가 큰 칸을 따라가면 그것이 최선의 길",
             ha="center", fontsize=15, color=INK)
    fig.tight_layout(rect=(0, .06, 1, 1))
    return save(fig, "gridworld.png", EX)


# ── 5. 벨만: 한 칸 앞만 본다 ─────────────────────────────────────
def bellman():
    V, _ = value_iteration()
    s = (2, 4)
    b = cbox(20, 150, 360, 220, "지금 칸", [f"가치 = {V[s]:.1f}", "(이걸 알고 싶다)"], "dark", ts=38, ss=30)
    rows = []
    for a in ["↑", "→", "↓", "←"]:
        n, rew, done = step_env(s, a)
        nv = 0 if done else V[n]
        rows.append((a, rew, nv, rew + (0 if done else GAMMA * nv), done))
    best = max(rows, key=lambda z: z[3])
    for i, (a, rew, nv, tot, done) in enumerate(rows):
        y = 8 + i * 118
        isb = (a == best[0])
        b += arrow(382, 260, 500, y + 50, TEAL if isb else MUTED, "aT" if isb else "aM", 5 if isb else 3)
        nm = {"↑": "위로", "→": "오른쪽", "↓": "아래로", "←": "왼쪽"}[a]
        f = LIME if isb else WHITE
        b += f'<rect x="510" y="{y}" width="1070" height="100" rx="10" fill="{f}" stroke="{INK if isb else HAIR}" stroke-width="2"/>'
        ex = f"{nm}: 보상 −0.4 + 0.9 × 다음 칸 가치 {nv:.1f}"
        b += text(540, y + 63, ex, 33, DARK, anchor="start", bold=isb)
        b += text(1550, y + 63, f"= {tot:.1f}", 36, RED if isb else INK, anchor="end", bold=True)
    b += text(800, 552, "지금 가치 = 행동마다 (당장 보상 + 할인한 다음 칸 가치)를 구해 가장 큰 값", 31, RED, bold=True)
    return svg("bellman.png", b, h=580)


# ── 6. 탐색과 활용: 슬롯머신 세 대 ───────────────────────────────
def bandit():
    rng = np.random.default_rng(7)
    mu = np.array([.2, .5, .8])
    T, R = 1000, 400
    res = {}
    for eps in (0.0, 0.1, 0.3):
        avg = np.zeros(T)
        for _ in range(R):
            Q, N = np.zeros(3), np.zeros(3)
            for t in range(T):
                a = rng.integers(3) if rng.random() < eps else int(np.argmax(Q + rng.random(3) * 1e-6))
                r = rng.normal(mu[a], 1.0)
                N[a] += 1; Q[a] += (r - Q[a]) / N[a]
                avg[t] += r
        avg /= R
        k = 50
        res[eps] = np.convolve(avg, np.ones(k) / k, mode="valid")
    fig, ax = plt.subplots(figsize=FIG)
    lab = {0.0: "ε = 0 — 탐색 안 함: 처음 좋아 보인 것에 갇힌다",
           0.1: "ε = 0.1 — 열 번에 한 번 새로 시도: 가장 좋다",
           0.3: "ε = 0.3 — 탐색이 너무 많다: 아는 최선을 자주 버린다"}
    col = {0.0: RED, 0.1: TEAL, 0.3: AMBER}
    for eps, y in res.items():
        ax.plot(np.arange(len(y)) + 50, y, color=col[eps], lw=3.6 if eps == .1 else 2.8, label=lab[eps])
    ax.axhline(.8, color=INK, lw=1.4, ls="--")
    ax.text(990, .82, "가장 좋은 기계의 평균 0.8", ha="right", fontsize=15, color=INK)
    ax.set_xlabel("몇 번째 시도", fontsize=15)
    ax.set_ylabel("평균 보상", fontsize=15)
    ax.set_ylim(.2, .92)
    ax.legend(fontsize=15.5, frameon=False, loc="lower right")
    clean(ax)
    fig.tight_layout()
    return save(fig, "bandit.png", "평균 0.2·0.5·0.8인 기계 세 대, 400번 반복 평균 — " + SIM)


# ── 7. Q-러닝이 배워 가는 모습 ───────────────────────────────────
def optimal_sets():
    V, _ = value_iteration()
    best = {}
    for r in range(ROWS):
        for c in range(COLS):
            s = (r, c)
            if s in WALLS or s in (GOAL, TRAP):
                continue
            q = {a: (lambda n, rew, d: rew + (0 if d else GAMMA * V[n]))(*step_env(s, a)) for a in MOVES}
            m = max(q.values())
            best[s] = {a for a, v in q.items() if v > m - 1e-6}
    return best


def qlearn_progress():
    opt = optimal_sets()
    rng = np.random.default_rng(3)
    acts = list(MOVES)
    Q = {(r, c): np.zeros(4) for r in range(ROWS) for c in range(COLS)}
    snaps, marks = {}, (5, 50, 1000)
    alpha, eps = .5, .2
    for ep in range(1, 1001):
        s = START
        for _ in range(60):
            a = rng.integers(4) if rng.random() < eps else int(np.argmax(Q[s] + rng.random(4) * 1e-6))
            n, rew, done = step_env(s, acts[a])
            target = rew + (0 if done else GAMMA * Q[n].max())
            Q[s][a] += alpha * (target - Q[s][a])
            s = n
            if done:
                break
        if ep in marks:
            snaps[ep] = {k: v.copy() for k, v in Q.items()}
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.2))
    for ax, ep in zip(axes, marks):
        Qs = snaps[ep]
        V = np.zeros((ROWS, COLS))
        pol, ok = {}, {}
        for (r, c), q in Qs.items():
            if (r, c) in WALLS or (r, c) in (GOAL, TRAP):
                continue
            V[r, c] = q.max()
            pol[(r, c)] = acts[int(np.argmax(q))] if q.any() else "·"
            ok[(r, c)] = pol[(r, c)] in opt[(r, c)]
        n_ok = sum(ok.values())
        _grid(ax, V, pol, True, ok=ok, nums=False,
              title=f"{ep}판 뒤 — 맞는 칸 {n_ok}/{len(ok)}",
              tc=TEAL if n_ok == len(ok) else INK)
    fig.text(.5, .02, "초록 화살표 = 최선의 행동(동점 포함) · 빨강 = 아직 틀림 · 칸 색 = 배운 가치(진할수록 높음)",
             ha="center", fontsize=15, color=INK)
    fig.tight_layout(rect=(0, .07, 1, 1))
    return save(fig, "qlearn_progress.png", "α = 0.5 · ε = 0.2 — " + SIM)


# ── 8. 기법 지도 ────────────────────────────────────────────────
def taxonomy():
    def chip(x, y, w, t, fill=WHITE, tc=INK, st=HAIR, fs=27):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="62" rx="31" fill="{fill}" stroke="{st}" stroke-width="2"/>'
                + text(x + w / 2, y + 42, t, fs, tc, bold=True))
    b = cbox(610, 6, 380, 70, "강화학습", (), "dark", ts=34)
    b += f'<path d="M800,76 L800,96 L440,96 L440,116 M800,96 L1290,96 L1290,116" fill="none" stroke="{TEAL}" stroke-width="4"/>'
    b += cbox(160, 118, 560, 80, "모델 없이 (model-free)", (), stroke=TEAL, ts=32)
    b += text(440, 236, "부딪히며 직접 배운다", 27, MUTED)
    b += cbox(1010, 118, 560, 80, "모델 기반 (model-based)", (), stroke=BLUE, ts=32)
    b += text(1290, 236, "세상의 규칙을 흉내 내 머릿속에서 연습", 27, MUTED)
    b += f'<path d="M440,250 L440,266 L150,266 L150,284 M440,266 L440,284 M440,266 L730,266 L730,284" fill="none" stroke="{TEAL}" stroke-width="3"/>'
    for x, t, s1 in [(150, "가치 기반", "점수표를 배운다"), (440, "정책 기반", "행동 확률을 직접"), (730, "둘 다", "Actor–Critic")]:
        b += cbox(x - 140, 286, 280, 110, t, [s1], ts=31, ss=26)
    b += chip(10, 414, 280, "Q-러닝")
    b += chip(10, 490, 280, "DQN")
    b += chip(300, 414, 280, "REINFORCE")
    b += chip(300, 490, 280, "PPO · GRPO", fill=LIME, st=INK, tc=DARK)
    b += chip(590, 414, 280, "DDPG · TD3")
    b += chip(590, 490, 280, "SAC · A2C")
    b += vrule(935, 270, 560, HAIR, 2)
    b += f'<line x1="1290" y1="250" x2="1290" y2="284" stroke="{BLUE}" stroke-width="3"/>'
    b += cbox(1010, 286, 560, 110, "계획 + 학습", ["미리 굴려 보고 고른다"], stroke=BLUE, ts=31, ss=26)
    b += chip(1010, 414, 270, "Dyna · MPC")
    b += chip(1300, 414, 270, "MuZero", fs=27)
    b += chip(1010, 490, 560, "Dreamer (세계 모형) · AlphaZero")
    return svg("taxonomy.png", b, h=566)


# ── 9. Actor–Critic ─────────────────────────────────────────────
def actor_critic():
    b = cbox(10, 10, 440, 230, "Actor (운용역)", ["정책: 비중을 정한다", "좋았던 쪽으로 조금씩"], "dark", ts=38, ss=29)
    b += cbox(580, 10, 440, 230, "환경 (시장)", ["수익·비용이 난다", "다음 상황이 온다"], stroke=TEAL, ts=38, ss=29)
    b += cbox(1150, 10, 440, 230, "Critic (리스크 담당)", ["이 상황의 기대 점수", "실제와 예상을 견준다"], stroke=BLUE, ts=36, ss=29)
    b += arrow(454, 125, 570, 125, TEAL, "aT", 4)
    b += text(512, 104, "행동", 30, TEAL, bold=True)
    b += arrow(1024, 125, 1140, 125, TEAL, "aT", 4)
    b += text(1082, 104, "보상", 30, TEAL, bold=True)
    b += f'<path d="M1370,242 L1370,340 L230,340 L230,252" fill="none" stroke="{RED}" stroke-width="5" marker-end="url(#aR)"/>'
    b += f'<rect x="490" y="306" width="620" height="70" rx="10" fill="{PAPER}"/>'
    b += text(800, 354, "놀람 = 실제 − 예상 (TD 오차)", 36, RED, bold=True)
    b += text(800, 440, "놀람이 +이면 그 행동을 더 자주, −이면 덜 한다", 32, INK)
    b += text(800, 486, "예상이라는 기준이 있어 점수 잡음이 줄고 더 빨리 배운다", 32, INK)
    b += text(800, 546, "PPO · SAC · DDPG가 모두 이 구조다 (강의본 3교시 33쪽 DDPG 루프)", 28, MUTED)
    return svg("actor_critic.png", b, h=572)


# ── 10. 70년 연표 ────────────────────────────────────────────────
def timeline():
    ev = [(1957, "벨만", "동적계획법", -1),
          (1989, "왓킨스", "Q-러닝", 1),
          (1992, "TD-Gammon", "백개먼 고수", -1),
          (2015, "DQN", "아타리 게임", 1),
          (2016, "알파고", "이세돌 9단에 4:1", -1),
          (2017, "PPO", "표준 기본값", 2),
          (2019, "MuZero", "규칙 몰라도 계획", -1),
          (2022, "RLHF", "ChatGPT를 다듬다", 1),
          (2025, "GRPO · R1", "추론 모델", -1),
          (2025.5, "튜링상", "바토·서튼", 2)]
    x0, x1 = 100, 1480
    def X(y):
        if y < 2012:
            return x0 + (y - 1955) / (2012 - 1955) * (x1 - x0) * .25
        return x0 + (x1 - x0) * .25 + (y - 2012) / (2026 - 2012) * (x1 - x0) * .75
    L = 268
    b = f'<line x1="{x0-60}" y1="{L}" x2="{x1+80}" y2="{L}" stroke="{INK}" stroke-width="4"/>'
    b += f'<line x1="{X(2011.2)}" y1="{L-18}" x2="{X(2012.2)}" y2="{L+18}" stroke="{PAPER}" stroke-width="14"/>'
    b += text(X(2011.7), L + 48, "≈", 32, MUTED)
    tops = {1: 4, 2: 124, -1: 300}
    for y, a, d, pos in ev:
        x = X(y)
        c = RED if y >= 2025 else TEAL
        yy = tops[pos]
        if pos > 0:
            b += f'<line x1="{x}" y1="{yy+108}" x2="{x}" y2="{L-10}" stroke="{HAIR}" stroke-width="2"/>'
        else:
            b += f'<line x1="{x}" y1="{L+10}" x2="{x}" y2="{yy+2}" stroke="{HAIR}" stroke-width="2"/>'
        b += f'<circle cx="{x}" cy="{L}" r="11" fill="{c}"/>'
        b += text(x, yy + 28, str(int(y)), 25, MUTED, bold=True)
        b += text(x, yy + 64, a, 31, c, bold=True)
        b += text(x, yy + 98, d, 25, INK)
    b += text(800, 480, "지금의 AI 챗봇·추론 모델도 마지막 단계에서 강화학습으로 다듬는다", 31, RED, bold=True)
    return svg("timeline.png", b, h=510)


# ── 11. 경험의 양: 게임 vs 시장 ──────────────────────────────────
def data_scarcity():
    items = [("알파고 제로\n자가대국(판)", 4.9e6, TEAL),
             ("DQN 한 게임\n학습 화면 수", 5.0e7, TEAL),
             ("주식 일별 30년\n(거래일)", 7.5e3, RED),
             ("주식 월별 100년\n(달)", 1.2e3, RED),
             ("기금 전략배분 결정\n(연 1회, 30년)", 30, RED)]
    fig, ax = plt.subplots(figsize=FIG)
    y = np.arange(len(items))[::-1]
    for yi, (lab, v, c) in zip(y, items):
        ax.barh(yi, v, color=c, height=.62)
        ax.text(v * 1.4, yi, f"{v:,.0f}", va="center", fontsize=17, color=INK, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([i[0] for i in items], fontsize=15, color=INK)
    ax.set_xscale("log"); ax.set_xlim(10, 1e9)
    ax.set_xlabel("배울 수 있는 경험의 수 (눈금 한 칸 = 10배)", fontsize=15)
    ax.text(14, 3.0, "게임은 원하는 만큼 새로 둘 수 있다", fontsize=16, color=WHITE, fontweight="bold", va="center")
    ax.text(3e4, .5, "시장의 과거는 한 번뿐 — 같은 30년을 되풀이해도 새 경험은 늘지 않는다",
            fontsize=16, color=RED, fontweight="bold", va="center")
    clean(ax, grid="x")
    fig.tight_layout()
    return save(fig, "data_scarcity.png", "알파고 제로 490만 판(Silver 외 2017) · DQN 게임당 5,000만 화면(Mnih 외 2015)")


# ── 12. 연기금 하이브리드 구조 ──────────────────────────────────
def hybrid():
    w, g = 280, 40
    xs = [20 + i * (w + g) for i in range(5)]
    spec = [("① 전략 배분", ["위원회가 정한다", "SAA · IPS"], "white", INK),
            ("② RL 제안", ["상태를 보고", "± 몇 %p 조정"], "white", TEAL),
            ("③ 가드레일", ["허용 범위·유동성", "넘으면 잘라 낸다"], "white", RED),
            ("④ 실행", ["비용 감안 거래"], "lime", INK),
            ("⑤ 성과 측정", ["보상 계산", "기준선과 비교"], "white", BLUE)]
    b = ""
    for x, (t, s1, k, st) in zip(xs, spec):
        b += cbox(x, 10, w, 220, t, s1, k, stroke=st, ts=35, ss=28)
    for i in range(4):
        b += arrow(xs[i] + w + 3, 120, xs[i + 1] - 7, 120, TEAL, "aT", 4)
    cx5, cx2, cx1 = xs[4] + w / 2, xs[1] + w / 2, xs[0] + w / 2
    b += f'<path d="M{cx5},232 L{cx5},318 L{cx2},318 L{cx2},242" fill="none" stroke="{AMBER}" stroke-width="4" stroke-dasharray="12,8" marker-end="url(#aM)"/>'
    b += text((cx2 + cx5) / 2, 302, "학습은 과거 데이터 시뮬레이터 안에서만 — 실제 계좌로 ‘탐색’하지 않는다", 29, INK, bold=True)
    b += f'<path d="M{cx5},318 L{cx5},410 L{cx1},410 L{cx1},242" fill="none" stroke="{MUTED}" stroke-width="4" marker-end="url(#aM)"/>'
    b += text((cx1 + cx5) / 2, 394, "연 1회 검토: RL이 기준선(단순 규칙)을 못 이기면 끈다", 29, MUTED, bold=True)
    b += text(800, 490, "강의본 36쪽 ‘RL을 혼자 두지 마라’ · 46쪽 Two Sigma의 가드레일 방식", 29, INK)
    return svg("hybrid.png", b, h=520)


# ── 수식 ────────────────────────────────────────────────────────
def equations():
    eq_png(r"$G_t \;=\; r_{t+1} \;+\; \gamma\, r_{t+2} \;+\; \gamma^{2} r_{t+3} \;+\; \cdots$",
           "eq_return.png", fontsize=44, width=9.6)
    eq_png(r"$V(s) \;=\; \max_{a}\;\left[\; r \;+\; \gamma\, V(s') \;\right]$",
           "eq_bellman.png", fontsize=44, width=8.0)
    eq_png(r"$Q(s,a) \;\leftarrow\; Q(s,a) \;+\; \alpha\,\left[\; r + \gamma\,\max_{a'} Q(s',a') \;-\; Q(s,a) \;\right]$",
           "eq_qlearn.png", fontsize=38, width=11.4)


if __name__ == "__main__":
    loop(); loop_pension(); episode(); discount(); gridworld(); bellman()
    bandit(); qlearn_progress(); taxonomy(); actor_critic(); timeline()
    data_scarcity(); hybrid(); equations()
    print("끝.")
