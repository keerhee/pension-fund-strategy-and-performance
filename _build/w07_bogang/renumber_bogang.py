# -*- coding: utf-8 -*-
"""W07 보강 번호 체계화 (2026-10-07): 보강 1-1 · 1-2 · 1-3 (TDF) → 2-1 · 2-2 (GP · 딥러닝) → 3 (강화학습).
파일명 · 머리말 · 표지 · 마지막 장 '다음 보강' 안내를 맞춘다. 재실행 가능(이미 바뀐 것은 건너뜀).
실행: .venv/bin/python _build/w07_bogang/renumber_bogang.py  → 그다음 PDF 재생성"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(ROOT)
sys.path.insert(0, "_build/lecfix")
from lecfix import Presentation, replace_all
W = "W07_동적포트폴리오와장기투자"
REN = [("W07_보강1_TDF의원리와최신기법", "W07_보강1-1_TDF의원리와최신기법"),
       ("W07_보강1_스페셜_국면기반TDF_Kritzman2017", "W07_보강1-2_국면기반TDF_Kritzman2017"),
       ("W07_보강1_스페셜II_국면기반TDF이후", "W07_보강1-3_국면기반TDF이후"),
       ("W07_보강2_GP동적거래모델_조준점과부분이동", "W07_보강2-1_GP동적거래모델_조준점과부분이동"),
       ("W07_보강2_부록_딥러닝동적자산배분모델", "W07_보강2-2_딥러닝동적자산배분모델")]
for a, b in REN:
    for ext in (".pptx", ".pdf", ".mp4"):
        if os.path.exists(f"{W}/{a}{ext}"): os.rename(f"{W}/{a}{ext}", f"{W}/{b}{ext}")

def fix(name, pairs, title):
    p = f"{W}/{name}.pptx"; prs = Presentation(p); tot = 0
    for a, b in pairs: tot += replace_all(prs, a, b)
    prs.core_properties.title = title; prs.save(p); print(f"{tot:3d}  {name}")

fix("W07_보강1-1_TDF의원리와최신기법", [
    ("W07 보강 1 · TDF의 원리와 최신 기법", "W07 보강 1-1 · TDF의 원리와 최신 기법"),
    ("W07 보강 1 · 2교시 ‘인적자본과 글라이드패스’를 실제 상품으로 읽기", "W07 보강 1-1 · 2교시 ‘생애주기와 TDF’를 실제 상품으로 읽기"),
    ("다음 보강 2 · GP 동적 거래 모델", "다음 보강 1-2 · 국면 기반 TDF")], "W07 보강1-1 TDF의 원리와 최신 기법")
fix("W07_보강1-2_국면기반TDF_Kritzman2017", [
    ("W07 보강 1 스페셜 · 국면 기반 TDF", "W07 보강 1-2 · 국면 기반 TDF"),
    ("— 보강 1의 부록", "— 보강 1-2"),
    ("보강 1 본편의 동적 글라이드패스", "보강 1-1의 동적 글라이드패스"),
    ("다시 보강 1", "다음은"), ("본편으로", "보강 1-3으로"),
    ("W07 보강 1 · 처음 배우는 TDF", "다음 보강 1-3 · 국면 기반 TDF 이후")], "W07 보강1-2 국면 기반 TDF Kritzman 2017")
fix("W07_보강1-3_국면기반TDF이후", [
    ("W07 보강 1 스페셜 II · 국면 기반 TDF 이후", "W07 보강 1-3 · 국면 기반 TDF 이후"),
    ("스페셜 I의", "보강 1-2의"),
    ("다시 보강 1", "다음은"), ("본편으로", "보강 2-1로"),
    ("W07 보강 1 스페셜 I · 국면 기반 TDF", "관련 보강 1-2 · 국면 기반 TDF"),
    ("W07 보강 3 · 처음 배우는 강화학습", "다음 보강 2-1 · GP 동적 거래 모델")], "W07 보강1-3 국면 기반 TDF 이후")
fix("W07_보강2-1_GP동적거래모델_조준점과부분이동", [
    ("W07 보강 2 · Gârleanu–Pedersen 모델", "W07 보강 2-1 · Gârleanu–Pedersen 모델"),
    ("다음 보강 3 · 처음 배우는 강화학습", "다음 보강 2-2 · 딥러닝 동적 자산배분")], "W07 보강2-1 GP 동적 거래 모델")
_dl = Presentation(f"{W}/W07_보강2-2_딥러닝동적자산배분모델.pptx")
if not replace_all(_dl, "W07 보강 2-2", "W07 보강 2-2", count_only=True):      # 재실행 때 접두어가 겹치지 않게
    fix("W07_보강2-2_딥러닝동적자산배분모델", [("딥러닝 동적 자산배분", "W07 보강 2-2 · 딥러닝 동적 자산배분")], "W07 보강2-2 딥러닝 동적 자산배분")
fix("W07_보강3_강화학습기초_처음배우는RL", [
    ("보충교재 14 RL 포트폴리오 · 보강 2 GP", "보충교재 14 RL 포트폴리오 · 보강 2-1 GP"),
    ("과 W07 보강 2(GP 모델)에", "과 W07 보강 2-1(GP 모델)에")], "W07 보강3 강화학습 기초 처음 배우는 RL")
