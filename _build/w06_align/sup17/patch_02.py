# -*- coding: utf-8 -*-
"""보충교재 17 · LDI/02 수식 도출 II — W06 M7 강의본(2026-10-05 개정)과 정합.
  · 25장 Redington: 잉여금 전개식 전체 + 금액 꼴 조건 A = L · D_A A = D_L L · C_A A > C_L L (구판 A ≥ L · ≥)
  · 29장 4번: '국민연금 안 B … 현물 131조' → 안 B 이름(30년 국고채 교체)과 강의본 숫자(보유 채권 131조 · 헤지 3 → 5%)
실행: <python-pptx + matplotlib 파이썬> patch_02.py   (늘 _구판/W06_정합전_2026-10-05/보충17_프라이머/LDI/에서 읽는다)
"""
import os
from common import *
from pptx import Presentation

SRC = os.path.join(BK, "LDI", "02_LDI_Derivations_II_zeroone.pptx")
DST = os.path.join(SUP, "LDI", "02_LDI_Derivations_II_zeroone.pptx")
LIME, DARK = "#B7F34A", "#071A1D"

def redington_png():
    plt = mpl()
    W, H, dpi = 11.31, 1.50, 220
    fig = plt.figure(figsize=(W, H), dpi=dpi); fig.patch.set_facecolor(DARK)
    fig.text(0.5, 0.74, r"$\Delta S\approx-(D_A\,A-D_L\,L)\,\Delta y+\frac{1}{2}\,(C_A\,A-C_L\,L)\,(\Delta y)^2$",
             fontsize=25, color=LIME, ha="center", va="center")
    for x, tex, lab in ((0.22, r"A=L", "① 현재가치 일치"), (0.50, r"D_A\,A=D_L\,L", "② 1차 항 = 0 · 금액 듀레이션"),
                        (0.78, r"C_A\,A>C_L\,L", "③ 2차 항 > 0 · 금액 볼록성")):
        fig.text(x, 0.36, f"${tex}$", fontsize=21, color=LIME, ha="center", va="center")
        fig.text(x, 0.10, lab, fontsize=12.5, color="#FFFFFF", ha="center", va="center")
    out = os.path.join(ART, "s02_redington.png")
    fig.savefig(out, dpi=dpi, facecolor=DARK); plt.close(fig)
    return out

P = Presentation(SRC)
# ---- 25장
s = P.slides[24]
card, pic = shape(s, 7), shape(s, 8)
card.height = E(160)
remove(pic)
add_pic(s, redington_png(), 69 + 5, 218 + 5, 1131 - 10, 150)
for sid in (9, 10, 11, 12, 13, 14, 15, 16, 17):
    move_px(shape(s, sid), dy=28)
lecfix.set_text(shape(s, 5), "3-2 — Redington(1952) 면역화의 세 조건 · 모두 금액(×A, ×L) 꼴, A = L일 때만 ‘자산 D = 부채 D · 자산 C > 부채 C’로 줄어든다")
lecfix.set_text(shape(s, 17), "2차 항을 양수로 — 금액 볼록성 우위: 크게 움직여도 잉여금이 오히려 는다")
# ---- 29장
s = P.slides[28]
lecfix.set_text(shape(s, 18), "시장 한계를 확인한다 — 국민연금 안 B(30년 국고채 교체)는 131조(장기물 발행의 30% × 5년)까지, 헤지 3% → 5%")
P.save(DST)
print("saved", DST)
