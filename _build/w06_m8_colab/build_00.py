# -*- coding: utf-8 -*-
from nbhelp import M, C, P, build, badge, colab_url

F = "00_시작하기.ipynb"
NB = [
    ("01_방법1_가장싼필요자본.ipynb", f"{P['o15']}~{P['M1']}장 · 부록 B-1~B-5", "방법 1 — z · w* · g · K 손계산, 4.91 · 2.24 · 1.97 · 합 9.13 · 49/22/28%", "2초"),
    ("02_방법2_DasMarkowitz.ipynb", f"{P['DM1']}~{P['DM2']} · {P['WHY']}장 · 부록 B-6", "방법 2 — (H, α) → γ 3.795 · 2.706 · 0.877, 롱온리 0 · 8.9 · 91.1, 12.4bp, Q_max −2.31%", "3초"),
    ("03_VaR_위험자본_CPPI.ipynb", f"{P['o37']}~{P['V2B']} · {P['FD']}장", "m ≤ 1/x · 위험 자본 floor 71.2/80/84.7 · 같은 답 74 · CPPI + Das–Markowitz", "2초"),
    ("04_방법3_몬테카를로_기초.ipynb", f"{P['MC1']}~{P['MX']} · {P['CB2']}장", "MC 원리 · 경로 1 표 · 장난감 K 2.2 → 2.26억 · 다수결 · 공통 난수", "5초"),
    ("05_방법3_여러목표_조합_우선순위.ipynb", f"{P['MXR']}~{P['MXP']} · {P['CB1']}~{P['CC']}장", "조합 폭발 · 격자 7.1억 · w 60% · 구간 분해 · 우선순위 9.14억 · 변수 묶기", "4초"),
    ("06_방법3으로_방법1·2_문제풀기.ipynb", f"{P['MC3']} · {P['DMC1']} · {P['DMC2']}장", "닫힌 해 vs MC · t5 · CPPI 위반 1.9 → 3.3% · Das–Markowitz MC", "20초"),
    ("07_동적계획법_GBWM.ipynb", f"{P['CB1']}장 각주 · 보충 13 DORS 덱", "(선택) DP 손계산 · 10년 두 배 66.6% · TDF 비교 · M8 세 목표 6.18억", "50초"),
]
table = "\n".join(f"| [{f}]({colab_url(f)}) | {pg} | {what} | {tm} |" for f, pg, what, tm in NB)

title = M(f"""
# 00 · 시작하기 — W06 M8 GBI 실습 노트북 세트

{badge(F)}

이 폴더의 노트북은 **W06 M8 GBI 목표기반투자 강의본**의 모든 방법론 · 몬테카를로 예제를 위에서부터 그대로 실행해
**강의본 숫자를 재현하고 그래프로 확인**하는 실습입니다. 노트북마다 혼자서 돌아갑니다(공용 파일 · 데이터 파일 없음, numpy · scipy · matplotlib만).

### Colab에서 여는 법
1. 아래 표의 노트북 이름(또는 각 노트북 맨 위의 **Open in Colab** 배지)을 누릅니다. 공개 저장소 `keerhee/pension-fund-strategy-and-performance`에서 바로 열립니다.
2. 메뉴 **런타임 → 모두 실행**(Ctrl/⌘ + F9). 처음 실행하면 한글 폰트(나눔고딕)를 설치하느라 10초쯤 더 걸립니다.
3. 결과를 저장하려면 **파일 → 드라이브에 사본 저장**. 원본은 읽기 전용입니다.
4. 열어 두기만 해도 지난 실행 결과(숫자 · 그래프)가 미리 보입니다.

### 로컬에서 여는 법
```bash
pip install numpy scipy matplotlib notebook
jupyter notebook          # 이 폴더에서 실행 → 00부터 차례로 연다
```

### 노트북 지도 — 강의 몇 장을 재현하나
| 노트북 | 강의본 장 | 무엇을 | 실행 시간(로컬 맥) |
|---|---|---|---|
{table}

Colab은 로컬보다 2~3배 느릴 수 있습니다. 06 · 07이 무거우면 노트북 위쪽 준비 셀의 `FAST = True`로 빠른 모드를 쓰세요.
""")

cells = [
M("""
## 1. 준비 셀이 하는 일
모든 노트북의 첫 코드 셀(바로 위)은 같습니다.
- **환경 감지** — Colab이면 `apt-get install fonts-nanum`으로 나눔고딕을 설치, 맥이면 `~/Library/Fonts/Pretendard-*.otf`를 찾아 matplotlib에 등록(폰트 캐시 갱신과 같은 효과).
- **강의 색** — 잉크 `#071A1D` · 라임 `#B7F34A` · 티일 `#0B6B68` · 빨강 `#C00000`, 바탕 아이보리.
- **`check(이름, 계산값, 강의값, 허용오차)`** — 계산이 강의본 숫자와 맞는지 확인합니다. 허용오차는 보통 강의 표기 자릿수의 반(반올림하면 같은 값). 틀리면 멈춥니다(`assert`).
- **`FAST`** — True면 경로 · 표본 수를 줄여 빨리 돌고, 확인은 표시만 합니다(멈추지 않음).

아래 그래프가 한글로 보이면 준비 완료입니다.
"""),
C("""
fig, ax = plt.subplots(figsize=(7, 3))
cols = [(INK, "잉크 #071A1D"), (LIME, "라임 #B7F34A"), (TEAL, "티일 #0B6B68"), (RED, "빨강 #C00000")]
for i, (c, lab) in enumerate(cols):
    ax.bar(i, 1, color=c, edgecolor=INK)
    ax.text(i, 1.05, lab, ha="center", fontsize=9)
ax.set_ylim(0, 1.3); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("한글 폰트 · 강의 색 확인 — 목표기반투자(GBI)")
plt.show()
"""),
M(f"""
## 2. 공통 가정과 공통 함수 — 미리 보기
강의본 단원 ③의 같은 문제: **55세 · 금융자산 10억 · 10년 뒤** 세 목표(Safety 6억 95% · Market 3억 70% · Aspirational 5억 30%).
자본시장 가정: GHP 실질 2%(변동성 0), 주식 초과수익 λ 6% · 변동성 σ 20%.
노트북마다 아래 함수 중 필요한 것을 **그 노트북 안에 다시** 정의합니다(파일 하나만 열어도 돌게). 여기서는 미리 한 번씩 써 봅니다.

| 함수 | 하는 일 | 나오는 곳 |
|---|---|---|
| `k_closed(G, z, w)` | 방법 1 닫힌 해 K = G·exp(−T·g) | 01 · 04 · 06 |
| `run_fixed(W0, w, R)` | 고정 비중 — 해마다 주식 w로 되돌리고 한 해 수익 반영 | 04 · 05 · 06 |
| `run_cppi(W0, G, m, R)` | CPPI — floor = 목표의 현가, 노출 = m × 쿠션 | 03 · 04 · 06 |
| `k_min(G, p, 성장 배수)` | 성공 비율 ≥ p인 최소 K — 이분법(같은 경로) | 04 · 05 · 06 |
| `solve_gamma(H, α)` | 방법 2 — (H, α)를 지키는 효율선 위 γ | 02 · 05 · 06 |
"""),
C("""
r, lam, sig, T = 0.02, 0.06, 0.20, 10
RG = math.exp(r) - 1

def k_closed(G, z, w):
    m = r + w * lam - 0.5 * w * w * sig * sig; s = w * sig
    return G * math.exp(-T * (m - z * s / math.sqrt(T)))

def run_fixed(W0, w, R):
    W = np.empty((R.shape[0], T + 1)); W[:, 0] = W0
    for t in range(T):
        W[:, t + 1] = W[:, t] * (w * (1 + R[:, t]) + (1 - w) * (1 + RG))
    return W

def k_min(G, p, growth):
    lo, hi = 0.0, G * 10
    for _ in range(60):
        mid = (lo + hi) / 2
        if np.mean(mid * growth >= G) >= p: hi = mid
        else: lo = mid
    return hi

# 방법 1 (닫힌 해) — Market 3억 · 70% · 주식 67%
K1 = k_closed(3.0, 0.524, 0.6708)
# 방법 3 (몬테카를로) — 같은 문제를 경로 100,000개로 센다
R = np.exp(r + lam - 0.5 * sig**2 + sig * np.random.default_rng(2026).standard_normal((100_000, T))) - 1
K3 = k_min(3.0, 0.70, run_fixed(1.0, 0.6708, R)[:, -1])
print(f"Market 3억 · 70%: 방법 1 닫힌 해 K = {K1:.2f}억 · 방법 3 몬테카를로 K = {K3:.2f}억")
check("미리 보기 — 방법 1 K", K1, 2.24, 0.005, ".2f")
check("미리 보기 — 방법 3 K", K3, 2.26, 0.005, ".2f")
"""),
M(f"""
## 3. 세 방법 한눈에 (강의 {P['CMP2']}장)
| | 방법 1 — 가장 싼 필요 자본 | 방법 2 — Das–Markowitz | 방법 3 — 몬테카를로 |
|---|---|---|---|
| 묻는 것 | 목표 G · 시점 T · 확률 p | 최소 수익률 H · 확률 한도 α | 목표 · 확률 + 현금흐름 · 운용 규칙 |
| 가정 | 로그정규 · 고정 비중 | 한 기간 · 정규 · 고정 비중 | 아무 분포 · 동적 규칙 가능 |
| 답 | K 4.91 · 2.24 · 1.97억 → 49/22/28% | γ 3.795 · 2.706 · 0.877 | 세어 낸 확률 · K 2.26억 · 부족액 |
| 노트북 | 01 | 02 | 04 · 05 · 06 (+ 03 CPPI, 07 DP) |

방법 1 · 2는 확률을 평균 · 변동성 조건으로 번역하고, 방법 3은 그 번역이 맞는지 경로로 확인합니다.
"""),
]

ex = [
    "준비 셀의 `FAST = True`로 바꾸고 위 미리 보기 셀을 다시 실행하면 무엇이 달라지나? (이 노트북은 경로 수를 고정해 두어 그대로다 — 04에서 해 보라)",
    "미리 보기에서 Market 확률을 80%로(`k_closed(3.0, 0.8416, 0.6708)`, `k_min(3.0, 0.80, ...)`) 바꾸면 두 방법의 K는?",
]

if __name__ == "__main__":
    build(F, title, cells, ex)
