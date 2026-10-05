from nbhelp import P, OUT, colab_url
import os
rows = [
 ("00_시작하기.ipynb", "도입 · 지도", "Colab 여는 법 · 한글 폰트 · 공통 함수 미리 보기 · 노트북 지도", "3초"),
 ("01_방법1_가장싼필요자본.ipynb", f"{P['o15']}~{P['M1']}장 · 부록 B-1~B-5({P['o72']}~{P['o76']}장)", "z · w* · g · K 손계산 → 4.91 · 2.24 · 1.97 · 합 9.13 · 49/22/28%, 아홉 칸 표 · 잉여 처리", "3초"),
 ("02_방법2_DasMarkowitz.ipynb", f"{P['DM1']}~{P['DM2']} · {P['WHY']}장 · 부록 B-6({P['B6A']}~{P['B6C']}장)", "60/30/10 검사 · 두 자산 w* 52.2% · 행렬 γ 3.795 · 2.706 · 0.877 · 롱온리(SLSQP = 엑셀 해 찾기) · γ 2.174 · 12.4bp · Q_max −2.31%", "3초"),
 ("03_VaR_위험자본_CPPI.ipynb", f"{P['o37']}~{P['V2B']} · {P['FD']}장", "m ≤ 1/x · 위험 자본 floor 71.2/80/84.7 · 같은 답 74 · CPPI + Das–Markowitz · CPPI 경로", "3초"),
 ("04_방법3_몬테카를로_기초.ipynb", f"{P['MC1']}~{P['MX']} · {P['CB2']}장", "표준오차 · 경로 1 표 · 장난감 K 2.2 → 2.26억 · 다수결 · 공통 난수 70.63/69.90%", "4초"),
 ("05_방법3_여러목표_조합_우선순위.ipynb", f"{P['MXR']}~{P['MXP']} · {P['CB1']}~{P['CC']}장", "조합 폭발 · 격자 7.1억 · w 60% · 구간 분해 · 우선순위 9.14억 · 변수 묶기", "4초"),
 ("06_방법3으로_방법1·2_문제풀기.ipynb", f"{P['MC3']} · {P['DMC1']} · {P['DMC2']}장", "닫힌 해 vs MC · t5 · CPPI floor 위반 1.9 → 3.3% · Das–Markowitz MC(200,000 표본)", "17초"),
 ("07_동적계획법_GBWM.ipynb", f"{P['CB1']}장 각주 · 보충교재 13 DORS 덱 17~39장", "(선택) DP 손계산 0.647 · 10년 두 배 66.6% · TDF 58.6 vs 25.6% · M8 세 목표 6.18억", "50초"),
]
tab = "\n".join(f"| [{f}]({colab_url(f)}) | {pg} | {w} | {t} |" for f, pg, w, t in rows)
md = f"""# W06 M8 GBI 실습 — Colab 노트북 세트

W06 M8 **GBI 목표기반투자 강의본**(`../W06_M8_GBI_목표기반투자_강의본.pdf`)의 모든 방법론 · 몬테카를로 예제를 위에서부터 그대로 실행해
**강의본 숫자를 재현하고 그래프로 확인**하는 노트북입니다. 수강생과 교수 모두 같은 파일을 씁니다.

- 노트북마다 혼자서 돌아갑니다 — 공용 `.py` · 데이터 파일 없음, 필요한 숫자는 노트북 안의 상수. 패키지는 numpy · scipy · matplotlib만.
- 시드 고정(2026). 계산 결과마다 강의본 숫자를 옆에 적고 `check()`(= `assert`)로 자동 확인합니다. 출력이 저장되어 있어 열기만 해도 결과가 보입니다.
- 강의 색(잉크 #071A1D · 라임 #B7F34A · 티일 #0B6B68 · 빨강 #C00000), 한글 폰트(Colab 나눔고딕 · 맥 Pretendard 자동 감지).
- 노트북 끝마다 **바꿔 보기** 연습 문제 2~3개와 빈 코드 셀.

## 노트북과 강의 장

| 노트북 (Colab에서 열기) | 강의본 장 | 무엇을 재현하나 | 실행 시간* |
|---|---|---|---|
{tab}

\\* 로컬 맥(M 시리즈) 기준 커널 시작 포함. Colab은 2~3배 걸릴 수 있습니다. 06 · 07이 무거우면 준비 셀의 `FAST = True`(경로 · 표본 축소, 07은 탐색 생략 — 확인은 표시만).
장 번호는 강의본 {max(P.values())}장 기준(`_build/w06_m8_rework/pages.json`).

## Colab에서 열기
위 표의 링크는 공개 저장소 `keerhee/pension-fund-strategy-and-performance`의 `W06_LDI와GBI/W06_M8_실습_Colab/` 경로를 가리킵니다
(형식: `https://colab.research.google.com/github/keerhee/pension-fund-strategy-and-performance/blob/main/<URL 인코딩한 경로>`).
**이 폴더를 저장소에 푸시한 뒤에 동작합니다.** 열면 **런타임 → 모두 실행**, 저장은 **파일 → 드라이브에 사본 저장**.

## 로컬에서 실행
```bash
pip install numpy scipy matplotlib notebook
jupyter notebook            # 이 폴더에서 → 00부터 차례로
```
출력까지 다시 저장하려면: `jupyter nbconvert --to notebook --execute --inplace 01_방법1_가장싼필요자본.ipynb`

## 숫자의 출처
`../gbi_mc.py`(+ `gbi_mc_results.json` · `gbi_mc_demo.json`), `../priority_mc.py`, `../dm_mc.py`, 보충교재 `17_LDI_GBI 수식도출/GBI/05_Martellini_GBI_Formula_Derivations_III.md` 3-6 · 4-2절,
`_build/gbwm_deck/gbwm_dp.py` · `compute.py`(DORS 덱). 노트북은 이 스크립트들과 같은 난수 순서를 써서 같은 숫자를 냅니다.

## 재현 메모
- 모든 확인 항목 통과(00: 2 · 01: 34 · 02: 87 · 03: 56 · 04: 48 · 05: 64 · 06: 74 · 07: 18).
- 허용오차는 강의 표기 자릿수의 반(예: 1.25% → 표 1.2%). 강의의 합산 롱온리 비중 35.4%는 합 100을 맞춘 반올림(계산 35.35%), 원문 오기 σ 19.89%의 손실은 강의 "약 34bp" vs 계산 34.6bp.
- 04의 "다수결": 매년 비중을 되돌리는 규칙에서는 경로별 사후 최적 비중이 양 끝(0 · 100%)으로 가는 경로가 83%(나머지 17%는 중간) — 강의의 "주식 100% · GHP 100%로 갈린다"는 대부분이라는 뜻으로 읽는다.
"""
open(os.path.join(OUT, "README.md"), "w").write(md)
print("ok")
