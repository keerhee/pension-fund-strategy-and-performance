# -*- coding: utf-8 -*-
"""W07 강의본 — 보강 재배치(2026-10-07)에 맞춘 순서·내용 정리.

보강 1 = 처음 배우는 TDF (+ 스페셜 I Kritzman 2017 국면 기반 TDF · 스페셜 II 그 이후)  — 2교시와 함께
보강 2 = Gârleanu–Pedersen 동적 거래 모델 (옛 보충교재 16)                          — 3교시 닫힌 해와 함께
보강 3 = 처음 배우는 강화학습 (옛 보강 1)                                            — 3교시 RL 전에

3교시를 보강 순서대로: 비용이 있는 동적 거래의 닫힌 해(무거래 구간 · GP, 옛 33~35쪽)를 먼저,
그다음 MDP · 강화학습(옛 30~32쪽), 기준선 사다리 이후는 그대로.
4부 구분 장 'WEEK 7 · 보강'(에피소드)은 별도 보강 덱과 헷갈리지 않게 'WEEK 7 · 에피소드'로.

원본: _구판/W07보강재배치_구판_2026-10-07/ (항상 거기서 다시 시작 — 재실행해도 같은 결과)
실행: .venv/bin/python _build/lecfix/fix_w07_bogang_order.py   → 그다음 soffice로 PDF
"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import *
R = os.path.dirname(os.path.dirname(HERE)); W = "W07_동적포트폴리오와장기투자"
NAME = "W07_동적포트폴리오와장기투자_강의본.pptx"
SRC = f"{R}/_구판/W07보강재배치_구판_2026-10-07/{W}/{NAME}"; DST = f"{R}/{W}/{NAME}"
shutil.copy2(SRC, DST)
prs = Presentation(DST)
S = lambda k: prs.slides[k - 1]

def rep(a, b, n=1):
    k = replace_all(prs, a, b); assert k == n, (a, k); return k

def cell(slide, row_prefix, col, text):
    t = find_table(slide)
    for r in t.table.rows:
        if r.cells[0].text.startswith(row_prefix):
            set_tf(r.cells[col].text_frame, text); return
    raise AssertionError(row_prefix)

# 보강 번호 (먼저 읽는 용어 ② · 3교시 상태 · 기준선 ②)
rep("3교시 · 기초는 보강 1", "3교시 · 기초는 보강 3")
rep("3교시 · 보충교재 16", "3교시 · 보강 2")
rep("W07 보강 1 ‘처음 배우는 강화학습’", "W07 보강 3 ‘처음 배우는 강화학습’")
rep("자세한 내용은 보충교재 16", "자세한 내용은 W07 보강 2")

# 강의 지도
cell(S(4), "2교시", 1, "BMS 총부 · TDF To/Through(상품은 보강 1) · 4대 비판 · 리밸런싱 · 기관의 생애주기")
cell(S(4), "3교시", 1, "비용이 있는 동적 거래의 닫힌 해 — 무거래 구간 · GP(보강 2) → MDP(기초는 보강 3) · 기준선 사다리 · DDPG · 보상과 회계 · 검증 · 하이브리드")
cell(S(4), "보강 · 에피소드", 0, "에피소드")

# 2교시 → 보강 1
rep("형태의 선택이 2022년 성과를 갈랐다", "형태의 선택이 2022년 성과를 갈랐다 · 상품 구조 · 국내 시장 · 국면 기반 TDF는 W07 보강 1")

# 1·2교시 종합의 다음 예고 · 3교시 구분 장
rep("3교시 — 강화학습의 현대 동적 배분, 에피소드 5편",
    "3교시 — 닫힌 해에서 강화학습으로, 에피소드 5편")
rep("해석해가 없는 곳에서 — 데이터로 배우는 배분 : MDP · 기준선(무거래 구간 · GP) · DDPG · 검증 · 하이브리드",
    "닫힌 해가 있는 곳(무거래 구간 · GP)에서 없는 곳으로 — 데이터로 배우는 배분 : MDP · DDPG · 검증 · 하이브리드")

# 닫힌 해 세 장: RL보다 먼저 오므로 'RL이 넘어야 할 벽'이 아니라 비용이 있는 동적 거래 그 자체로
rep("3교시 · 기준선 ①", "3교시 · 닫힌 해 ①"); rep("3교시 · 기준선 ②", "3교시 · 닫힌 해 ②"); rep("3교시 · 기준선 ③", "3교시 · 닫힌 해 ③")
rep("RL이 넘어야 할 벽 ① — 비례 비용이면 무거래 구간", "비용 있는 거래 ① — 비례 비용이면 무거래 구간")
rep("RL이 넘어야 할 벽 ② — 이차 비용이면 GP의 조준과 부분 이동", "비용 있는 거래 ② — 이차 비용이면 GP의 조준과 부분 이동")
rep("RL은 먼저 이 구간을 재현해야 한다", "RL도 이 구간부터 재현해야 한다")
# MDP 장은 이제 닫힌 해 다음 — 왜 RL로 넘어가는지 한 줄로 잇는다
rep("Merton이 해석해로 푼 문제의 일반형 — 풀 수 없는 곳에서 “학습”이 등장한다",
    "Merton · GP가 닫힌 해로 푼 문제의 일반형 — 풀 수 없는 곳에서 “학습”이 등장한다")

# 4부 구분 장
rep("WEEK 7 · 보강", "WEEK 7 · 에피소드")

# 순서: 옛 33·34·35쪽(닫힌 해)을 3교시 구분 장(29쪽) 바로 뒤로
for k, (old, new) in enumerate(((32, 29), (33, 30), (34, 31))):
    move_slide(prs, old, new)
renumber(prs)
prs.save(DST)
print("저장:", NAME, len(prs.slides), "장")
