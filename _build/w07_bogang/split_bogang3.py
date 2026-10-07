# -*- coding: utf-8 -*-
"""W07 보강 3을 둘로 (2026-10-07): 3-1 처음 배우는 강화학습(옛 보강 3) · 3-2 강화학습과 역강화학습 — 퀀트 금융 응용
(보충교재 14의 05_RL_IRL_Quant_Finance_zeroone_III 사본 — 원본은 14번 묶음에 그대로 둔다). 재실행 가능."""
import os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(ROOT)
sys.path.insert(0, "_build/lecfix")
from lecfix import Presentation, replace_all
W = "W07_동적포트폴리오와장기투자"
A, A2 = "W07_보강3_강화학습기초_처음배우는RL", "W07_보강3-1_강화학습기초_처음배우는RL"
for ext in (".pptx", ".pdf", ".mp4"):
    if os.path.exists(f"{W}/{A}{ext}"): os.rename(f"{W}/{A}{ext}", f"{W}/{A2}{ext}")
B = f"{W}/W07_보강3-2_강화학습과역강화학습_퀀트금융응용.pptx"
if not os.path.exists(B):
    shutil.copy2("보충교재/14_강화학습포트폴리오/05_RL_IRL_Quant_Finance_zeroone_III.pptx", B)

def fix(path, pairs, title):
    prs = Presentation(path); n = sum(replace_all(prs, a, b) for a, b in pairs)
    prs.core_properties.title = title; prs.save(path); print(n, os.path.basename(path))

fix(f"{W}/{A2}.pptx", [("W07 보강 3 · ", "W07 보강 3-1 · "),
                        ("보충교재 14 RL 포트폴리오 · 보강 2-1 GP", "다음 보강 3-2 · 강화학습과 역강화학습")], "W07 보강3-1 강화학습 기초 처음 배우는 RL")
_b = Presentation(B)
_done = replace_all(_b, "W07 보강 3-2 · ", "", count_only=True) > 0       # 재실행 때 접두어가 겹치지 않게
fix(B, ([] if _done else [("Igor Halperin(2020) 강연 재구성 · 원 논문 보강", "W07 보강 3-2 · Igor Halperin(2020) 강연 재구성 · 원 논문 보강")]) + [
        ("다음 단계: 손계산 워크북에서", "다음 단계: 보충교재 14번 손계산 워크북에서")], "W07 보강3-2 강화학습과 역강화학습 퀀트 금융 응용")
# 보강 1-3 · 2-1 덱이 가리키는 강화학습 기초는 이제 3-1
fix(f"{W}/W07_보강1-3_국면기반TDF이후.pptx", [("보강 3의 강화학습", "보강 3-1의 강화학습"), ("보강 3의 기준선 사다리", "보강 3-1의 기준선 사다리")], "W07 보강1-3 국면 기반 TDF 이후")
