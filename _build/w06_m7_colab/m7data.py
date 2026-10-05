# -*- coding: utf-8 -*-
"""빌드 때 케이스 · 실습 CSV를 읽어 노트북에 '상수'로 박아 넣는 도구 (노트북은 파일을 읽지 않는다). 원자료는 읽기만 한다."""
import csv, os
from nbhelp import ROOT
W6 = os.path.join(ROOT, "W06_LDI와GBI")
CASE = os.path.join(W6, "W06_M7_케이스데이터")

def _rows(path):
    lines = [l for l in open(path, encoding="utf-8-sig") if not l.startswith("#")]
    return list(csv.DictReader(lines))

def fmt_list(xs, per=10, ind="    "):
    xs = [f"{x:g}" for x in xs]
    return "[\n" + "\n".join(ind + ", ".join(xs[i:i + per]) + "," for i in range(0, len(xs), per)) + "\n]"

def cashflow():
    r = _rows(os.path.join(CASE, "fml_w6m7_cashflow.csv"))
    return ([int(x["year"]) for x in r], [float(x["contrib_trn_krw"]) for x in r], [float(x["benefit_trn_krw"]) for x in r],
            [float(x["net_outflow_trn_krw"]) for x in r])

def curve():
    r = _rows(os.path.join(CASE, "fml_w6m7_curve.csv"))
    return [float(x["maturity_y"]) for x in r], [float(x["yield_pct"]) for x in r]

def params():
    return {x["key"]: x["value"] for x in _rows(os.path.join(CASE, "fml_w6m7_params.csv"))}

def market():
    return {x["key"]: x["value"] for x in _rows(os.path.join(CASE, "fml_w6m7_market.csv"))}

def assets():
    return _rows(os.path.join(CASE, "fml_w6m7_assets.csv"))

def liability_lab():
    r = _rows(os.path.join(W6, "fml_w7_liability.csv"))
    return [int(x["year"]) for x in r], [float(x["연간지급액_억원"]) for x in r]
