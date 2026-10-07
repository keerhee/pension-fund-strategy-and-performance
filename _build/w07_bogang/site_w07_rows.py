# -*- coding: utf-8 -*-
"""사이트 W07 목록: 보강 1 TDF 3덱 · 보강 2 GP(보충교재 16에서 이동) · 보강 3 강화학습. 보충교재 목록에서 GP 행 제거."""
import re, urllib.parse, os, subprocess, sys
S = sys.argv[1]   # 다운로드 zip 안의 index.html (TDF 행 원본)
h = open("site/index.html", encoding="utf-8").read(); z = open(S, encoding="utf-8").read()
W = "W07_동적포트폴리오와장기투자"; q = urllib.parse.quote
PAGES = re.compile(r"Pages:\s+(\d+)")
def meta(name):
    p = f"{W}/{name}.pdf"; n = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
    return "%s장 · %.1f MB" % (PAGES.search(n).group(1), os.path.getsize(p) / 1e6)
ROW = r'<li class="row"(?:(?!</li>).)*</li>'
def setmeta(r, name): return re.sub(r'<span class="meta">[^<]*</span>', '<span class="meta">%s</span>' % meta(name), r)
w07 = re.search(r'<section class="wk" id="W07">.*?</section>', h).group(0)
rl = [r for r in re.findall(ROW, w07) if "처음 배우는 강화학습" in r][0]
sup = re.search(r'<section class="wk" id="SUP">.*?</section>', h).group(0)
gps = [r for r in re.findall(ROW, sup) if "16_Garleanu" in urllib.parse.unquote(r)]
assert len(gps) == 1, len(gps); gp = gps[0]
ztdf = [r for r in re.findall(ROW, z) if "TDF" in r and "보강 1" in r]; assert len(ztdf) == 3
names = {"TDF%EC%9D%98%EC%9B%90%EB%A6%AC": "W07_보강1_TDF의원리와최신기법", "Kritzman2017": "W07_보강1_스페셜_국면기반TDF_Kritzman2017",
         "%EC%9D%B4%ED%9B%84": "W07_보강1_스페셜II_국면기반TDF이후"}
tdf = [setmeta(r, names[next(k for k in names if k in r)]) for r in ztdf]
old = re.search(r'main/([^"]*?\.pdf)"', gp).group(1)
newgp = gp.replace(old, q(W) + "/" + q("W07_보강2_GP동적거래모델_조준점과부분이동") + ".pdf")
newgp = re.sub(r'<span class="ttl">.*?<em class="sub">[^<]*</em>',
               '<span class="ttl">보강 2 — Gârleanu–Pedersen 동적 거래 모델<em class="sub">3교시 닫힌 해와 함께 · 조준점과 부분 이동</em>', newgp)
newgp = re.sub(r'data-t="[^"]*"', 'data-t="보강"', newgp).replace(" w06 보충교재", " 보강")
newgp = re.sub(r'<span class="tag [^"]*">[^<]*</span>', '<span class="tag t-4">보강</span>', newgp, 1)
newgp = setmeta(newgp.replace('data-k="', 'data-k="보강 2 ', 1), "W07_보강2_GP동적거래모델_조준점과부분이동")
newrl = rl.replace("보강 1 — 처음 배우는 강화학습", "보강 3 — 처음 배우는 강화학습").replace('data-k="보강 1 ', 'data-k="보강 3 ')
newrl = setmeta(newrl.replace(q("W07_보강1_강화학습기초_처음배우는RL"), q("W07_보강3_강화학습기초_처음배우는RL")), "W07_보강3_강화학습기초_처음배우는RL")
w07n = w07.replace(rl, "".join(tdf) + newgp + newrl)
cnt = lambda sec: re.sub(r'(<span class="cnt">)\d+(</span>)', lambda m: m.group(1) + str(len(re.findall(ROW, sec))) + m.group(2), sec, 1)
w07n = cnt(w07n); supn = cnt(sup.replace(gp, ""))
h = h.replace(w07, w07n).replace(sup, supn); open("site/index.html", "w", encoding="utf-8").write(h)
print("W07", len(re.findall(ROW, w07n)), "SUP", len(re.findall(ROW, supn)))
for r in re.findall(ROW, w07n):
    print("  ", re.search(r'<span class="ttl">([^<]*)', r).group(1), "|", re.search(r'<span class="meta">([^<]*)', r).group(1))
print("missing:", [urllib.parse.unquote(u) for u in re.findall(r'main/([^"]+\.pdf)"', h) if not os.path.exists(urllib.parse.unquote(u))])
