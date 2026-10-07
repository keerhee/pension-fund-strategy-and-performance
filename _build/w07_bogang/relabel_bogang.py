# -*- coding: utf-8 -*-
"""W07 보강 재배치(2026-10-07): 보강 1 = TDF(+스페셜 I·II) · 보강 2 = GP 동적 거래 모델(옛 보충교재 16) · 보강 3 = 강화학습 기초(옛 보강 1).
덱 사이 상호 참조와 파일명을 맞춘다. 실행: .venv/bin/python _build/w07_bogang/relabel_bogang.py"""
import os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(ROOT)
sys.path.insert(0, "_build/lecfix")
from lecfix import Presentation, replace_all
W = "W07_동적포트폴리오와장기투자"
def fix(path, pairs):
    prs = Presentation(path); tot = 0
    for a, b, n in pairs:
        k = replace_all(prs, a, b); assert k == n or (n is None and k > 0), (path, a, k); tot += k
    cp = prs.core_properties
    if cp.title:
        for a, b, _ in pairs:
            cp.title = cp.title.replace(a, b)
    prs.save(path); print(f"{tot:3d}  {os.path.basename(path)}")

# 강화학습 기초: 보강 1 → 보강 3, 파일명도
old = f"{W}/W07_보강1_강화학습기초_처음배우는RL"; new = f"{W}/W07_보강3_강화학습기초_처음배우는RL"
for ext in (".pptx", ".pdf", ".mp4"):
    if os.path.exists(old + ext): os.rename(old + ext, new + ext)
fix(new + ".pptx", [("보강 2", "보강 3", None), ("보강 1", "보강 3", 0),
     ("보충교재 14 RL 포트폴리오 · 16 GP 모델", "보충교재 14 RL 포트폴리오 · W07 보강 2 GP 모델", 1),
     ("과 16번(GP 모델)에 있습니다", "과 W07 보강 2(GP 모델)에 있습니다", 1)])
p = Presentation(new + ".pptx"); p.core_properties.title = "W07 보강3 강화학습기초 처음배우는RL"; p.save(new + ".pptx")

# GP: 보충교재 16 → W07 보강 2
src = "보충교재/16_Garleanu_Pedersen모델/GP_동적거래모델_조준점과부분이동_ZeroOne"
gp = f"{W}/W07_보강2_GP동적거래모델_조준점과부분이동"
for ext in (".pptx", ".pdf"):
    if os.path.exists(src + ext): shutil.move(src + ext, gp + ext)
if os.path.isdir(os.path.dirname(src)) and not os.listdir(os.path.dirname(src)): os.rmdir(os.path.dirname(src))
fix(gp + ".pptx", [("보충교재 16 · Gârleanu–Pedersen 모델", "W07 보강 2 · Gârleanu–Pedersen 모델", None),
     ("보충교재 14 · 강화학습 포트폴리오", "다음 보강 3 · 처음 배우는 강화학습", 1)])
p = Presentation(gp + ".pptx"); p.core_properties.title = "W07 보강2 GP 동적거래모델 조준점과 부분이동"; p.save(gp + ".pptx")

# TDF 본편: 다음 읽을 보강
fix(f"{W}/W07_보강1_TDF의원리와최신기법.pptx", [("다음 보강 2 · 처음 배우는 강화학습", "다음 보강 2 · Gârleanu–Pedersen 동적 거래 모델", 1)])
# 스페셜 II: 강화학습은 보강 3
fix(f"{W}/W07_보강1_스페셜II_국면기반TDF이후.pptx", [("보강 2의 강화학습", "보강 3의 강화학습", 1),
     ("보강 2의 기준선 사다리", "보강 3의 기준선 사다리", 1),
     ("W07 보강 2 · 처음 배우는 강화학습", "W07 보강 3 · 처음 배우는 강화학습", 1)])

# 2026-10-07 렌더 확인 후: 마지막 장 오른쪽 문구가 세 줄로 접혀 줄인다
fix(new + ".pptx", [("보충교재 14 RL 포트폴리오 · W07 보강 2 GP 모델", "보충교재 14 RL 포트폴리오 · 보강 2 GP", 1)])
fix(f"{W}/W07_보강1_TDF의원리와최신기법.pptx", [("다음 보강 2 · Gârleanu–Pedersen 동적 거래 모델", "다음 보강 2 · GP 동적 거래 모델", 1)])
