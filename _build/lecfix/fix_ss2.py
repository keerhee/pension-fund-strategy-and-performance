# -*- coding: utf-8 -*-
"""W06 SS2 강의본(21→22장)을 케이스 1·2 v3(국민연금 리밸런싱 규칙 · 네 기관 차등)에 맞춰 보수.
실행: .venv/bin/python _build/lecfix/fix_ss2.py  (재실행 가능). 숫자는 W06_SS2_케이스데이터/w6ss2_results.json.
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import *
R = os.path.dirname(os.path.dirname(HERE)); W = f"{R}/W06_동적포트폴리오와장기투자"
OLD = f"{R}/_구판/강의본_구판_2026-09-21"; os.makedirs(OLD, exist_ok=True)
IMG = f"{R}/_build/w06_ss2_case/img"
def backup(name):
    for ext in (".pptx", ".pdf"):
        src, dst = f"{W}/{name}{ext}", f"{OLD}/{name}{ext}"
        if os.path.exists(dst): shutil.copy2(dst, src)
        elif os.path.exists(src): shutil.copy2(src, dst)
def to_pdf(p): subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(p), p], check=True, capture_output=True)
def rep1(prs, a, b):
    n = replace_all(prs, a, b); assert n >= 1, ("not found", a[:50]); return n

name = "W06_특별세션_SS2_재균형프리미엄_강의본"; backup(name)
prs = Presentation(f"{W}/{name}.pptx"); src = Presentation(f"{R}/W05_리스크패리티와HRP/W05_리스크패리티와HRP_강의본.pptx")
S = lambda k: prs.slides[k - 1]
# 오탈자
rep1(prs, "밸도별", "빈도별"); rep1(prs, "밸도 변론", "빈도 변론"); rep1(prs, "쓏린다", "쏠린다"); rep1(prs, "긎어먹나", "갉아먹나"); rep1(prs, "앵버 박스", "앰버 박스")
rep1(prs, "Claude Code가 짜다", "Claude Code가 짠다"); rep1(prs, "감정을 배제한 �기 매매", "감정을 배제한 역추세 매매")
# s01
rep1(prs, "Shannon's Demon · Diversification Return · 빈도별 최적 · Mean-Reversion · 실습", "Shannon's Demon · 분산수익(DR) · 빈도별 최적 · 평균회귀 · 케이스 1 · 2")
# s02 지도
set_text(find(S(2), "이번 강의의 지도 — 다섯 갈래"), "이 강의의 지도 — 다섯 갈래가 케이스의 조건으로 모인다")
set_text(find(S(2), "개념에서 실습·정책까지"), "무엇을 배우고, 케이스 1 · 2에서 어디에 쓰는가 — 처음 보는 사람은 이 표부터")
set_table(find_table(S(2)), [["구간", "주제 · 도구", "케이스에서"],
    ["1부", "리밸런싱이란 — Shannon's Demon · 캘린더 vs 밴드", "조건 ⑤ 지침 별표 1 · 경계 복원"],
    ["2부", "왜 수익이 나나 — 분산수익 DR (Booth–Fama 1992)", "조건 ② 순 프리미엄 = DR − 비용"],
    ["3부", "얼마나 자주 — 빈도별 DR · 비용 · 순 프리미엄", "조건 ③ 시장충격 · 한도 25bp"],
    ["4부", "언제 통하나 — 평균회귀 AR(1) φ · Chambers", "조건 ① 평균회귀 |t| ≥ 2"],
    ["5부", "실습 · 케이스 1 국민연금 규칙 · 케이스 2 네 기관", "기본 답 안 B (+42bp)"]])
set_text(find(S(2), "핵심 질문 —"), "핵심 질문 — “재조정이 왜 수익을 낳는가, 그 규칙을 어디까지 집행할 수 있는가”")
# s10 디바이더
rep1(prs, "빈도별 DR·비용·Net Alpha · Quarterly 최적", "빈도별 DR · 비용 · 순 프리미엄 — 월간~분기가 최적 구간")
# s11 빈도 차트
set_text(find(S(11), "리밸런싱 빈도별 Net Alpha"), "리밸런싱 빈도별 순 프리미엄 — NPS 규모")
replace_picture(pictures(S(11))[0], f"{IMG}/fig_freq.png")
set_text(find(S(11), "Daily는 비용이 DR 초과"), "일간도 플러스(+39bp)이나 비용 21.5bp가 잠식 · 월간 +56 ~ 분기 +54bp가 최적 구간(2bp 차)")
# s12 빈도별 숫자
set_text(find(S(12), "DR은 줄고 비용은 준다"), "DR도 비용도 빈도와 함께 준다 — NPS 규모(1,866조) · 20년 모의 패널 · bp/년")
set_table(find_table(S(12)), [["빈도", "분산수익 DR", "거래비용(스프레드 + 시장충격)", "순 프리미엄"],
    ["일간", "+60.5", "−21.5", "+39.0 (비용 잠식)"], ["주간", "+59.4", "−10.2", "+49.2"], ["월간", "+61.0", "−5.4", "+55.7 (최적)"],
    ["분기", "+56.7", "−3.1", "+53.7 (2bp 차)"], ["반기", "+52.8", "−2.1", "+50.7"], ["연간", "+50.5", "−1.4", "+49.1"]])
set_text(find(S(12), "핵심 — 더 자주가 아니라"), "핵심 — 더 자주가 아니라 “집행 가능한 빈도” · 케이스 1의 안 B는 월 점검 · 25bp 한도(+42bp)")
# s14 평균회귀 차트
set_text(find(S(14), "자산군별 Mean-Reversion 강도"), "자산군별 평균회귀 강도 — AR(1) φ 의 t값")
set_text(find(S(14), "평균회귀가 강해야 리밸런싱 효과"), "평균회귀가 강해야 리밸런싱 효과 — 케이스 1 조건 ①: |t| ≥ 2 인 자산에만 좁은 밴드가 정당하다")
replace_picture(pictures(S(14))[0], f"{IMG}/fig_ar1.png")
set_text(find(S(14), "EM·REIT은 강한 평균회귀"), "신흥주식 · 상장 부동산 φ −0.21(t −3.3) 강한 회귀 · 선진주식은 랜덤워크 · 국고채는 추세(+0.16)")
# s18 실습
set_text(find(S(18), "① 5종 빈도별 DR 계산"), "① 케이스 데이터 재현(w6ss2) — 빈도별 DR · 비용 · 순 프리미엄\n② 자산군별 AR(1) φ 검증\n③ 밴드 폭 ±2~±6 · 25bp 한도의 순 프리미엄")
set_text(find(S(18), "Quarterly가 Net으로 최적인가?"), "월간~분기가 최적 구간인가(2bp 차)?\n일간도 플러스인가(+39bp)?\n신흥 · 부동산 φ 가 가장 음인가?")
sh = find(S(18), "너는 리밸런싱 분석가다")
set_text(sh, "너는 리밸런싱 분석가다. 리밸런싱\n프리미엄 엔진을 python으로:\n1) 케이스 데이터 fml_w6ss2_panel_daily_sim\n   (7자산 20년 일간)을 읽어\n2) DR = g_port − Σ w·g_asset 계산\n3) 6종 빈도(일간~연간) DR 비교\n4) 자산별 거래비용 차감 순 프리미엄\n5) 자산군별 AR(1) phi로 평균회귀\n6) 밴드 ±2~±6 · 월 25bp 한도 비교\n각 단계 검증·표 저장·한국어 해석 포함.")
rep1(prs, "Case 2에서 4기관으로 확장", "케이스 2에서 네 기관으로 확장")
# s19 결과 읽기
rep1(prs, "빈도별 Net Alpha를 표로 보여주고, 왜 Quarterly가 최적인지 설명해줘.", "빈도별 순 프리미엄을 표로 보여주고, 왜 월간~분기가 최적 구간인지 설명해줘.")
set_text(find(S(19), "Daily Net −0.16%"), "일간 순 +39bp — DR 60.5 − 비용 21.5, 플러스이나 비용이 잠식\n월간 순 +56bp — DR 61.0 − 비용 5.4 = 최적 · 분기 +54bp(2bp 차)\n연간 순 +49bp — DR 50.5, 드리프트로 DR 자체가 준다\n신흥주식 · 상장 부동산 φ −0.21(t −3.3) — 가장 강한 평균회귀")
# s20 과제
rep1(prs, "KSWF 리밸런싱 정책 — 밸도+비용+트리거 1p.", "전략형 국부펀드의 집중 한도 · 유동성 하한 1p.")
rep1(prs, "자산군 mean-reversion으로 최적 빈도 2p 메모.", "자산군 평균회귀 t값으로 밴드 폭 · 빈도 2p 메모.")
# s21
rep1(prs, "더 자주가 아니라 Quarterly가 최적 — 거래비용이 DR을 잠식한다.", "더 자주가 아니라 집행 가능한 빈도 — 월간~분기가 최적, 25bp 한도가 규칙의 값이다.")
rep1(prs, "Case 1(학술) + Case 2(Python Lab)로 — 리밸런싱의 실전으로 이어진다", "케이스 1(국민연금 규칙 — 밴드 · 주기 · 한도) + 케이스 2(네 기관 차등)로 이어진다")
# s03 메시지 3
rep1(prs, "Mean-reversion이 있어야 진짜 프리미엄 · 거래비용과 빈도의 균형이 핵심.", "평균회귀가 있어야 진짜 프리미엄 · 거래비용 · 시장충격 · 실행 한도가 규칙의 값을 정한다.")
# 용어 ① (W05 s02 복제)
n0 = len(prs.slides); g1 = clone_slide(src, 1, prs)
set_text(find(g1, "먼저 읽는 용어 ① —"), "먼저 읽는 용어 — 재균형의 말")
set_text(find(g1, "처음 보는 사람도"), "처음 보는 사람도 이 한 쪽만 읽으면 뒤의 수식과 그림이 읽힌다 · 영어는 첫 등장에만")
set_table(find_table(g1), [["용어", "뜻", "이 덱에서"],
    ["분산수익 DR (diversification return)", "고정 비중 포트폴리오의 기하수익 − 자산 기하수익의 가중평균 ≈ ½(Σwσ² − σ_p²) — Booth–Fama 1992", "월간 61bp · 연간 50bp"],
    ["순 프리미엄", "DR에서 거래비용(스프레드 + 시장충격)을 뺀 것 — 규칙의 값", "월간 +56 · 분기 +54 · 케이스 조건 ②"],
    ["평균회귀 AR(1) φ", "이번 달 수익이 지난 달과 반대로 가는 경향 — φ < 0, |t| ≥ 2 면 회귀", "신흥 · 부동산 −0.21 · 조건 ①"],
    ["캘린더 vs 밴드", "정해진 날에 복원하나, 밴드를 벗어날 때만 복원하나 — 지침 별표 1은 밴드 ±3(국내주식)", "케이스 1 안 A · B · C"],
    ["실행 한도 · 오버레이", "한 달에 옮길 수 있는 비중의 상한(월 25bp) · 지수선물로 총 위험을 먼저 맞추는 것", "2026.7.2 재개 · 조건 ③"],
    ["시장충격", "복원 거래액 ÷ 일평균 거래대금 — 현물 5% · 선물 20% 참여율로 며칠 걸리나", "목표 복원 155조 = 64일 · 조건 ③"],
    ["CVaR95 위험한도 · 허용범위", "최악 5% 평균 손실 ≥ −15%(지침 제6조의2) · 자산군별 SAA 밴드(별표 1)", "위험자산 ≤ 67.4% · 조건 ④ · ⑤"]])
set_text(find(g1, "μ를 버리면"), "재균형은 예측이 아니라 규율 — 이 덱은 “그 규율의 값이 얼마이고, 어디까지 집행되나”를 배운다")
move_slide(prs, n0, 1); renumber(prs)
assert not scan_codes(prs), scan_codes(prs); assert len(prs.slides) == 22
prs.save(f"{W}/{name}.pptx"); to_pdf(f"{W}/{name}.pptx"); print("SS2 강의본 22장 저장")
