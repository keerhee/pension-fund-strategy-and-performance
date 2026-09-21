#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W7 M9 케이스 v3 수식 PNG — matplotlib mathtext(cm), 카드 배경색 #F4F5F9. 출력 img/eq_*.png + img/eq_ratios.json"""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = f"{os.path.dirname(HERE)}/img"; os.makedirs(IMG, exist_ok=True)
plt.rcParams.update({"mathtext.fontset": "cm", "font.size": 30})
BG, INK = "#F4F5F9", "#1B2C5E"
EQS = {   # mathtext: 한글 불가 · \text 불가 · cases 불가 → 라벨은 캡션에
    # 케이스 1
    "eq_cppi": r"$w_{t}=\min\left\{1,\ \dfrac{m\,(W_{t}-F_{t})}{W_{t}}\right\},\qquad C_{t}=W_{t}-F_{t}$",
    "eq_floor": r"$F_{t}=x\,G_{S}\,e^{-y_{t}(T-t)}\,(1-c/12)^{-(T-t)}$",
    "eq_goals": r"$P(W_{T}<G_{S})\leq 5\%,\qquad P(W_{T}\geq G_{M})\geq 70\%,\qquad G_{M}=1.0309^{10}$",
    "eq_gap": r"$L^{*}=\dfrac{1}{m}\qquad (m=2:\ 50\%,\ \ m=3:\ 33\%,\ \ m=6:\ 17\%)$",
    "eq_erosion": r"$1-(1-c)^{30}\qquad (c=0.5\%:\ 14\%,\ \ 1.0\%:\ 26\%,\ \ 1.5\%:\ 36\%)$",
    # 케이스 2
    "eq_spend": r"$S_{t}=0.8\,S_{t-1}(1+\pi)+0.2\,z\,W_{t-1}$",
    "eq_lockup": r"$L_{t}=L_{t-1}(1+\pi)-S-C_{t}-B_{t},\qquad N=\min\{t:\ L_{t}\leq 0\}\ \geq\ 10$",
    "eq_neutral": r"$P\!\left(\dfrac{W_{30}}{\prod_{t=1}^{30}(1+\pi_{t})}\geq W_{0}\right)\geq 50\%,\qquad z\geq 4.0\%$",
    "eq_buffer": r"$y\,W_{0}\,(1+r_{safe})\ \geq\ \sum_{t=1}^{3}S^{fix}_{t}+B\qquad (r_{safe}=-15\%)$",
    "eq_access": r"$\dfrac{x\,W_{0}}{100\ \mathrm{bn}}\geq 15\quad\wedge\quad \mathrm{staff}\geq 3$",
}
ratios = {}
for name, tex in EQS.items():
    fig = plt.figure(figsize=(0.1, 0.1)); fig.patch.set_facecolor(BG)
    txt = fig.text(0, 0, tex, color=INK, fontsize=30)
    fig.canvas.draw(); bb = txt.get_window_extent(); w, h = bb.width / fig.dpi + 0.6, bb.height / fig.dpi + 0.5
    plt.close(fig)
    fig = plt.figure(figsize=(w, h)); fig.patch.set_facecolor(BG)
    fig.text(0.5, 0.5, tex, color=INK, fontsize=30, ha="center", va="center")
    path = f"{IMG}/{name}.png"; fig.savefig(path, dpi=200, facecolor=BG); plt.close(fig)
    ratios[name] = round(w / h, 3); print("→", name, f"{w:.1f}x{h:.1f}in ratio {w/h:.2f}")
json.dump(ratios, open(f"{IMG}/eq_ratios.json", "w"), indent=1)
