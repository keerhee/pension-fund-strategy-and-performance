# -*- coding: utf-8 -*-
"""⑤ ic-critic — 투자위원회의 심사와 표결.
   16주 동안 사람이 해온 IC를 그대로 옮긴 층이다.
   IPS 위반은 자동 기각(표결에 올리지 않는다 — IPS 7.3항)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, common

INFLATION = 0.02        # 실질 목표 → 명목 환산 가정

def lens_scores(cand, ips):
    """네 관점이 각각 0~10점을 매긴다. 관점마다 보는 것이 다르다."""
    e = cand["expected"]; w = np.array(list(cand["weights"].values()))
    nominal_target = ips["real_return_target"] + INFLATION
    s = {}
    s["목표달성"] = round(max(0, min(10, 10*e["ret"]/nominal_target)), 2)
    s["위험한도"] = round(10.0 if e["vol"] <= ips["vol_cap"] else
                       max(0, 10 - 40*(e["vol"]-ips["vol_cap"])), 2)
    s["분산"]     = round(max(0, min(10, 10*e["effective_n"]/8.0)), 2)
    s["집중도"]   = round(max(0, min(10, 10*(1 - (w.max()-0.10)/0.25))), 2)
    return s

def main(run):
    ips = common.load_ips()
    cands = [common.load(f, run) for f in ("alloc_mvo.json","alloc_bl.json","alloc_rp.json")]
    rows = []
    for c in cands:
        v = c["ips_violations"]
        rec = {"agent":c["agent"], "method":c["method"], "week":c["week"],
               "violations":v, "eligible": not v}
        if v:
            rec["scores"], rec["total"], rec["note"] = None, None, "IPS 위반 — 자동 기각(7.3항)"
        else:
            sc = lens_scores(c, ips)
            rec["scores"], rec["total"] = sc, round(sum(sc.values()), 2)
            rec["note"] = ""
        rows.append(rec)
    elig = [r for r in rows if r["eligible"]]
    winner = max(elig, key=lambda r: r["total"]) if elig else None
    out = {"run":run, "nominal_target": ips["real_return_target"]+INFLATION,
           "lenses":["목표달성","위험한도","분산","집중도"], "candidates":rows,
           "winner": winner["agent"] if winner else None,
           "decision": ("채택: %s" % winner["method"]) if winner else "채택안 없음 — 전원 기각"}
    p = common.save("ic_vote.json", out, run)

    print("  명목 목표수익률 %.1f%% (실질 %.1f%% + 인플레 %.1f%%)"
          % (out["nominal_target"]*100, ips["real_return_target"]*100, INFLATION*100))
    print("  %-18s %-8s %s" % ("후보", "합계", "관점별 점수 / 기각 사유"))
    for r in rows:
        if r["eligible"]:
            det = "  ".join("%s %.1f" % (k, v) for k, v in r["scores"].items())
            print("  %-18s %-8.2f %s" % (r["agent"], r["total"], det))
        else:
            print("  %-18s %-8s %s" % (r["agent"], "기각", "; ".join(r["violations"])))
    print("  → 결정: %s" % out["decision"])
    print("  → %s" % os.path.relpath(p, common.ROOT))

if __name__ == "__main__": main(sys.argv[1])
