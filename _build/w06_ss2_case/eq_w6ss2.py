#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W6 SS2 케이스 v3 수식 PNG — matplotlib mathtext(cm), 카드 배경색 #F4F5F9. 출력 img/eq_*.png + img/eq_ratios.json"""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); IMG = f"{os.path.dirname(HERE)}/img"; os.makedirs(IMG, exist_ok=True)
plt.rcParams.update({"mathtext.fontset": "cm", "font.size": 30})
BG, INK = "#F4F5F9", "#1B2C5E"
EQS = {   # mathtext: 한글 불가 · cases 불가 → 라벨은 캡션에, 결정 트리는 SVG 도해로
    "eq_dr": r"$\mathrm{DR}=g_{p}-\sum_{i} w_{i}\,g_{i}\ \approx\ \frac{1}{2}\left(\sum_{i} w_{i}\sigma_{i}^{2}-\sigma_{p}^{2}\right)$",
    "eq_net": r"$\mathrm{Net}=\mathrm{DR}(\mathrm{rule})-\mathrm{Cost}(\mathrm{rule}),\qquad \mathrm{Cost}=\sum_{\mathrm{trades}}\frac{Q}{\mathrm{AUM}}\,(s+\eta\,\sigma_{d}\sqrt{p}\,)$",
    "eq_ar1": r"$r_{t}=a+\phi\,r_{t-1}+\varepsilon_{t},\qquad t_{\phi}\leq-2\ \Rightarrow\ \mathrm{mean\ reversion}$",
    "eq_days": r"$\mathrm{Days}=\frac{\Delta w\cdot \mathrm{AUM}}{p\cdot \mathrm{ADV}}\ \leq\ 20,\qquad p_{\mathrm{cash}}=5\%,\ p_{\mathrm{fut}}=20\%$",
    "eq_cvar": r"$\mathrm{CVaR}_{95}(w)=\mu(w)-2.063\,\sigma(w)\ \geq\ -15\%\ \Rightarrow\ w\leq w_{\max}=67.4\%$",
    "eq_drift": r"$w_{t+1}=\frac{w_{t}(1+r^{\mathrm{risk}}_{t})}{w_{t}(1+r^{\mathrm{risk}}_{t})+(1-w_{t})(1+r^{\mathrm{safe}}_{t})}$",
    "eq_rule": r"$\mathrm{Rule}=(\,b_{\mathrm{class}},\ b_{\mathrm{total}},\ \mathrm{check},\ \mathrm{cap},\ \mathrm{instrument}\,)$",
    "eq_flow": r"$\mathrm{FlowCap}=\frac{|\mathrm{net\ flow}|}{\mathrm{AUM}}\ \geq\ \frac{1}{2}\,\sigma_{\mathrm{drift},12m}$",
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
