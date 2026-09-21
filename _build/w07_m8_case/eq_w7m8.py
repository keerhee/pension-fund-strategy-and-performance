#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W07 M8 케이스 v3 수식 PNG — matplotlib mathtext(cm), 카드 배경색 #F4F5F9. 출력 img/eq_*.png (비율은 charts_w7m8.py 가 img_ratios.json 에 모은다)"""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = f"{os.path.dirname(HERE)}/img"; os.makedirs(IMG, exist_ok=True)
plt.rcParams.update({"mathtext.fontset": "cm", "font.size": 30})
BG, INK = "#F4F5F9", "#1B2C5E"
EQS = {   # mathtext: 한글 불가 · cases 불가 · \le \ge 불가 → \leq \geq · \tfrac 불가 → \frac
    "eq_fr": r"$FR=\dfrac{A}{L},\qquad \Delta FR\ \approx\ FR\,(r_A-r_L)$",
    "eq_liab": r"$L_r=\sum_{t=1}^{46}\dfrac{B_{t}-C_{t}}{(1+r_t)^{t}},\qquad t=1\ (2026)\ \ldots\ 46\ (2071)$",
    "eq_dv01": r"$DV01=D_{mod}\cdot V\cdot 10^{-4},\qquad h=\dfrac{DV01_A}{DV01_L},\qquad Gap=D_A-D_L$",
    "eq_need": r"$\Delta DV01=h^{*}\,DV01_L-DV01_A,\qquad Q_{30y}=\dfrac{\Delta DV01}{(D_{30y}-D_{bond})\cdot 10^{-4}},\qquad N_{IRS}=\dfrac{\Delta DV01}{D_{IRS}\cdot 10^{-4}}$",
    "eq_margin": r"$VM_{3d}=\Delta DV01\cdot 200,\qquad Buffer=\Delta DV01\cdot 250\ \leq\ Liquid$",
    "eq_frshift": r"$FR(\Delta y)=\dfrac{A\,(1-D_A\,\Delta y)}{L\,(1-D_L\,\Delta y)}$",
    "eq_cap": r"$Q_{30y}\ \leq\ 0.30\times 5\times I_{20/30/50},\qquad N_{IRS}\ \leq\ 0.05\times T_{IRS}$",
    "eq_hurdle": r"$\mu_{after}=\mu_{SAA}+\dfrac{Q_{30y}}{A}\,(y_{30}-\mu_{bond})\ \geq\ 5.5\%$",
}
for name, tex in EQS.items():
    fig = plt.figure(figsize=(0.1, 0.1)); fig.patch.set_facecolor(BG)
    txt = fig.text(0, 0, tex, color=INK, fontsize=30)
    fig.canvas.draw(); bb = txt.get_window_extent(); w, h = bb.width / fig.dpi + 0.6, bb.height / fig.dpi + 0.5
    plt.close(fig)
    fig = plt.figure(figsize=(w, h)); fig.patch.set_facecolor(BG)
    fig.text(0.5, 0.5, tex, color=INK, fontsize=30, ha="center", va="center")
    fig.savefig(f"{IMG}/{name}.png", dpi=200, facecolor=BG); plt.close(fig)
    print("→", name, f"{w:.1f}x{h:.1f}in ratio {w/h:.2f}")
