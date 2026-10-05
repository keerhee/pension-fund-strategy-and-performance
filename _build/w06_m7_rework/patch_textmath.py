"""rework_m7.py 다음에 실행 — 39·48장의 밑줄 기호(텍스트 수식)를 말로 바꾼다(수식은 위의 PNG가 맡는다)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lecfix"))
from pptx import Presentation
import lecfix
F = os.path.join(os.path.dirname(__file__), "..", "..", "W06_LDI와GBI", "W06_M7_LDI_부채연계투자_강의본.pptx")
P = Presentation(F)
R = [("현재가치가 같으면 조건 2·3은 D_A A = D_L L, C_A A ≥ C_L L과 같다", "현재가치가 같으면 조건 2·3은 금액 듀레이션 일치 · 금액 볼록성 우위와 같다"),
     ("PV_A = PV_L", "자산 PV = 부채 PV"), ("D_A = D_L", "자산 D = 부채 D"), ("C_A > C_L", "자산 C > 부채 C"),
     ("LHP = (1/FR) × (D_L/D_H)에는", "헤지 몫 식(앞 장)에는")]
for a, b in R:
    n = lecfix.replace_all(P, a, b); assert n >= 1, a
P.save(F); print("patched")
