# -*- coding: utf-8 -*-
"""W07 강의본 109장 대본 합치기: 그대로 쓰는 38장(옛 narr.py) + 에이전트가 쓴 part_A~D.json → lectures/pension-w06/script/narr.py
옛 narr.py는 narr_backup_2026-10-07.py로 보관."""
import json, os, re, shutil, importlib.util, glob
HERE = os.path.dirname(os.path.abspath(__file__))
SD = "/Users/keerhee/Project/lectures/pension-w06/script"
bk = f"{SD}/narr_backup_2026-10-07.py"
if not os.path.exists(bk): shutil.copy2(f"{SD}/narr.py", bk)
spec = importlib.util.spec_from_file_location("narr", bk); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
plan = json.load(open(f"{HERE}/narr_plan.json"))
P = {}
for f in sorted(os.path.join(HERE, "narr", x) for x in os.listdir(os.path.join(HERE, "narr")) if x.startswith("part_") and x.endswith(".json")):
    for k, v in json.load(open(f)).items(): P[int(k)] = v
N = {}; miss = []
for p in plan:
    i = p["new"]
    if p["status"] == "keep": N[i] = [s.replace("재균형", "리밸런싱") for s in m.N[p["narr"]]]
    elif i in P: N[i] = P[i]
    else: miss.append(i)
assert not miss, f"대본 없음: {miss}"
bad = [(i, s) for i in N for s in N[i] if "돈" in s or "재균형" in s or len(re.findall(r"\d+(?:[.,]\d+)*", s)) > 4]
for b in bad: print("점검:", b)
with open(f"{SD}/narr.py", "w", encoding="utf-8") as f:
    f.write('# -*- coding: utf-8 -*-\n"""pension-w06 (109장) 나레이션 — 동적 포트폴리오와 장기투자. 2026-10-07 강의본 재구성(63→109) 반영.\n'
            '그대로 쓴 38장은 narr_backup_2026-10-07.py에서, 나머지 71장은 _build/w07_restructure/narr/part_*.json에서."""\nN = {}\n\n')
    for i in sorted(N):
        f.write(f"N[{i}] = " + json.dumps(N[i], ensure_ascii=False, indent=8).replace("\n]", "]") + "\n\n")
b = open(f"{SD}/build.py").read(); open(f"{SD}/build.py", "w").write(re.sub(r"m.N, \d+", "m.N, 109", b))
print(len(N), "장 ·", sum(len(v) for v in N.values()), "문장 ·", sum(len(s) for v in N.values() for s in v), "자 · 점검", len(bad))
