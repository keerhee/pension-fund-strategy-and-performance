#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W06 케이스 v3 수식 PNG — matplotlib mathtext(cm), 카드 배경색 #F4F5F9. 출력 img/eq_*.png + img/eq_ratios.json"""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = f"{os.path.dirname(HERE)}/img"; os.makedirs(IMG, exist_ok=True)
plt.rcParams.update({"mathtext.fontset": "cm", "font.size": 30})
BG, INK = "#F4F5F9", "#1B2C5E"
EQS = {   # mathtext: 한글 불가 · cases 불가 → 라벨은 캡션에, 결정 트리는 SVG 도해로
    "eq_merton": r"$w^{*}=\dfrac{\mu-r}{\gamma\,\sigma^{2}}$",
    "eq_timediv": r"$\sigma_{\mathrm{ann}}=\dfrac{\sigma}{\sqrt{T}}\ \downarrow\qquad\quad \sigma_{\mathrm{cum}}=\sigma\sqrt{T}\ \uparrow$",
    "eq_bms": r"$\mathrm{RiskShare}_{t}=\dfrac{w_{t}\,F_{t}}{F_{t}+H_{t}},\qquad H_{t}=\sum_{k=1}^{30}\dfrac{C_{t+k}}{(1+\delta)^{k}}$",
    "eq_glide": r"$w_{t}=\max\{\,w_{h},\ 0.65-0.01\,(t-t^{*})\,\}$",
    "eq_trigger": r"$t^{*}=\min\{t:\ H_{t}/F_{t}<0.625\},\qquad w_{h}=\dfrac{5.5-\mu_{s}}{\mu_{r}-\mu_{s}}=50\%$",
    "eq_loss": r"$L_{t}=\dfrac{w_{t}\,\sigma_{r}\,F_{t}}{B_{t}}\ \leq\ 1$",
    "eq_icapm": r"$w^{*}=\dfrac{\mu-r}{\gamma\sigma^{2}}\;+\;\left(1-\dfrac{1}{\gamma}\right)\dfrac{\beta\,\sigma_{x}}{\sigma_{a}}$",
    "eq_predict": r"$\bar r_{t\rightarrow t+10}=\alpha+\beta\,x_{t}+\varepsilon_{t},\qquad t_{\beta}\ \geq\ 2\ \ (\mathrm{Newey\!-\!West})$",
    "eq_hedge": r"$h_{i}=\left(1-\dfrac{1}{\gamma}\right)\dfrac{\beta_{i}\,\sigma_{x_i}}{\sigma_{a_i}},\qquad \gamma=5,\ T=10$",
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
