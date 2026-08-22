# -*- coding: utf-8 -*-
"""⑥ meta-reviewer — 예측을 실현과 대조하고 지시문 수정을 제안한다 (W10).
   IPS 7.4항에 따라 제안만 하고 자동 반영하지 않는다(킬스위치)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, common

def main(run):
    ips = common.load_ips(); cma = common.load("cma.json", run)
    R = common.load_panel(); tick = cma["tickers"]
    test = R.loc[cma["as_of"]:].iloc[1:]              # 평가구간 — 여기서 처음 본다
    mu_hat = np.array([cma["mu"][t] for t in tick])
    mu_real = ((1+test[tick]).prod()**(12/len(test)) - 1).values

    err = mu_real - mu_hat
    lines = []
    for f in ("alloc_mvo.json","alloc_bl.json","alloc_rp.json"):
        c = common.load(f, run); w = np.array([c["weights"][t] for t in tick])
        pf = common.perf(w, test[tick])
        lines.append({"agent":c["agent"], "expected_ret":c["expected"]["ret"],
                      "realized_ret":pf["ann_return"], "realized_vol":pf["ann_vol"],
                      "mdd":pf["mdd"], "sharpe":pf["sharpe"],
                      "gap": pf["ann_return"]-c["expected"]["ret"],
                      "eligible": not c["ips_violations"]})
    props = []
    if abs(err).mean() > 0.02:
        props.append({"target":"cma-builder",
            "change":"SHRINK_MU 0.5 → 0.7 (역사적 평균 의존을 낮춘다)",
            "why":"평균 절대 예측오차 %.1f%%p" % (abs(err).mean()*100)})
    worst = tick[int(np.argmax(np.abs(err)))]
    props.append({"target":"cma-builder",
        "change":"%s의 기대수익률 산정에 국면 구분을 추가한다" % worst,
        "why":"%s 오차 %.1f%%p로 최대" % (worst, err[int(np.argmax(np.abs(err)))]*100)})
    if any(l["gap"] < -0.02 and l["eligible"] for l in lines):
        props.append({"target":"ic-critic",
            "change":"'목표달성' 관점 가중을 낮추고 '견고성' 관점을 신설한다",
            "why":"채택안의 실현수익이 기대를 2%p 이상 밑돌았다"})

    out = {"run":run, "test_period":"%s ~ %s (%d개월)"
           % (test.index[0].date(), test.index[-1].date(), len(test)),
           "forecast_error":dict(zip(tick, np.round(err,4).tolist())),
           "mae": float(abs(err).mean()), "portfolios":lines,
           "proposals":props,
           "auto_applied": False,
           "gate":"IPS 7.4항 — 사람이 변경 이력을 검토한 뒤에만 반영한다"}
    p = common.save("meta_review.json", out, run)

    print("  평가구간 %s" % out["test_period"])
    print("  CMA 예측오차 MAE %.2f%%p (최대 오차 %s %.1f%%p)"
          % (out["mae"]*100, worst, err[int(np.argmax(np.abs(err)))]*100))
    print("  %-18s %8s %8s %8s %7s" % ("후보","기대","실현","격차","MDD"))
    for l in lines:
        tag = "" if l["eligible"] else "  (기각안)"
        print("  %-18s %7.2f%% %7.2f%% %7.2f%%p %6.1f%%%s"
              % (l["agent"], l["expected_ret"]*100, l["realized_ret"]*100,
                 l["gap"]*100, l["mdd"]*100, tag))
    print("  지시문 수정 제안 %d건 — 자동 반영: %s" % (len(props), out["auto_applied"]))
    for pr in props: print("     · [%s] %s" % (pr["target"], pr["change"]))
    print("  → %s" % os.path.relpath(p, common.ROOT))

if __name__ == "__main__": main(sys.argv[1])
