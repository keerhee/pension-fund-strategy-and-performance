"""시연 화면(자율주행 프로세스)의 엔진 쪽 — 화면은 /api/demo/* 를 부르고, 여기서 예시 MVP 파이프라인을 임시 복사본에서 돌린다.

흐름: 입력 md(IPS 변경) · 돌발 md(IPS 변경 · 시장 충격 · 모델 교체)를 읽는다 → 임시 복사본에 반영 →
     그 분기를 다시 계산하되 CIO 결정은 비워 둔다(사람 CIO가 화면에서 결정) → 결정이 오면 그 결정으로 마저 진행.
제출 폴더는 건드리지 않는다. 숫자는 모두 파이프라인(코드)이 계산한다 — 화면은 파일을 읽기만 한다.
"""
from __future__ import annotations
import csv, json, os, re, shutil, uuid
import pandas as pd
import yaml
from .data import ROOT, TICKERS
from .selfcheck import copy_repo, py
from .pipeline import quarters

SESS: dict[str, dict] = {}

# 입력 md의 항목 이름 → ips.md 제약 표(YAML)의 키, 퍼센트로 적는 항목인가
KEYS = {
    "변동성 상한": ("vol_cap", True), "종목 상한": ("asset_max", True), "종목 하한": ("asset_min", True),
    "유효 종목 수 하한": ("effective_n_min", False),
    "주식 하한": ("groups.equity.min", True), "주식 상한": ("groups.equity.max", True),
    "채권 하한": ("groups.fixed_income.min", True), "채권 상한": ("groups.fixed_income.max", True),
    "대체 하한": ("groups.alternative.min", True), "대체 상한": ("groups.alternative.max", True),
}
SHOCK_KEYS = {"주식 한 달 수익률": "equity", "금리 변화": "rate_bp", "금": "gold", "원자재": "commodity"}
DUR = {"IEF": 7.5, "TLT": 16.5, "LQD": 8.5, "HYG": 3.5, "TIP": 7.0}


def _num(s: str) -> float | None:
    m = re.findall(r"[-+−]?\d+(?:\.\d+)?", str(s).replace("−", "-"))
    return float(m[-1]) if m else None   # "10% → 8%"처럼 적으면 마지막 숫자가 새 값


def _items(md: str) -> dict:
    out = {}
    for line in md.splitlines():
        m = re.match(r"^\s*-\s*([^:：]+?)\s*[:：]\s*(.+)$", line)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out


def _top(md: str, key: str) -> str | None:
    m = re.search(rf"^{key}\s*[:：]\s*(.+)$", md, re.M)
    return m.group(1).strip() if m else None


def _ips_overrides(items: dict, errors: list) -> dict:
    ov = {}
    for k, v in items.items():
        if k not in KEYS:
            continue
        key, pct = KEYS[k]
        x = _num(v)
        if x is None:
            errors.append(f"'{k}' 값을 숫자로 읽지 못했다: {v}")
            continue
        ov[key] = round(x / 100, 6) if pct else x
    return ov


def parse_input(md: str | None) -> dict:
    """입력 파일: '기준 분기: 2024-02' + '## IPS 변경' 아래 '- 항목: 값'."""
    qs = quarters(include_last=True)
    if not md:
        return {"name": "없음 (제출본 IPS 그대로)", "q": None, "overrides": {}, "errors": [], "warnings": []}
    errors, warnings = [], []
    q = _top(md, "기준 분기")
    if q and q not in qs:
        errors.append(f"기준 분기 {q}가 없다 — 고를 수 있는 분기: {qs[0]} ~ {qs[-1]} (3개월 간격)")
    items = _items(md)
    unknown = [k for k in items if k not in KEYS]
    if unknown:
        warnings.append("읽지 않은 항목: " + ", ".join(unknown) + " — 읽는 항목: " + ", ".join(KEYS))
    ov = _ips_overrides(items, errors)
    if not ov and not errors:
        warnings.append("IPS 변경 항목이 없다 — 제출본 IPS 그대로 계산한다")
    return {"name": (re.search(r"^#\s+(.+)$", md, re.M) or [None, "입력 파일"])[1], "q": q, "overrides": ov, "errors": errors, "warnings": warnings}


def parse_shock(md: str | None) -> dict | None:
    """돌발 md: '유형: IPS 변경 | 시장 충격 | 모델 교체' + '## 변경 내용' 아래 '- 항목: 값'."""
    if not md:
        return None
    kind = _top(md, "유형") or ""
    items = _items(md)
    errors = []
    out = {"title": (re.search(r"^#\s+(.+)$", md, re.M) or [None, "돌발 과제"])[1], "kind_text": kind, "errors": errors, "md": md}
    if "IPS" in kind:
        out["kind"] = "ips"; out["overrides"] = _ips_overrides(items, errors)
        if not out["overrides"]:
            errors.append("IPS 변경 항목이 없다 — 읽는 항목: " + ", ".join(KEYS))
    elif "시장" in kind or "충격" in kind:
        out["kind"] = "market"; sh = {}
        for k, key in SHOCK_KEYS.items():
            if k in items:
                sh[key] = _num(items[k])
        if not sh:
            errors.append("시장 충격 항목이 없다 — 읽는 항목: " + ", ".join(SHOCK_KEYS))
        out["shock"] = {"equity": 0.0, "rate_bp": 0.0, "gold": 0.0, "commodity": 0.0, **{k: v for k, v in sh.items() if v is not None}}
    elif "모델" in kind:
        out["kind"] = "model"; out["model"] = items.get("판단 모델", "새 모델")
    elif "결함" in kind:   # 숨은 결함 주입(공개 점검 T2 · 라이브 점검 L3) — 시스템이 스스로 잡아내는지 본다
        out["kind"] = "defect"; out["q"] = _top(md, "기준 분기")
        if "주입 배분안" in items:
            w = {t: 0.0 for t in TICKERS}
            for tk, x in re.findall(r"([A-Z]{3,4})\s*[:=]?\s*([-+]?\d+(?:\.\d+)?)\s*%?", items["주입 배분안"]):
                if tk in w: w[tk] = float(x) / 100
                else: errors.append(f"모르는 종목 {tk} — 읽는 종목: {', '.join(TICKERS)}")
            out["proposal"] = [round(w[t], 6) for t in TICKERS]; out["proposal_sum"] = round(sum(out["proposal"]), 6)
        if "리서치 메모 추가" in items:
            out["memo"] = items["리서치 메모 추가"].strip(" \"'“”")
        if "proposal" not in out and "memo" not in out:
            errors.append("결함 항목이 없다 — 읽는 항목: 주입 배분안 · 리서치 메모 추가")
    else:
        out["kind"] = "unknown"; errors.append(f"모르는 유형: '{kind}' — IPS 변경 · 시장 충격 · 모델 교체 · 결함 주입 중 하나")
    return out


def _apply_ips(d: str, ov: dict) -> dict:
    p = os.path.join(d, "ips.md")
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"```yaml\n(.*?)```", txt, re.S)
    y = yaml.safe_load(m.group(1))
    before = {}
    for k, v in ov.items():
        node, keys = y["constraints"], k.split(".")
        for kk in keys[:-1]:
            node = node[kk]
        before[k] = node.get(keys[-1])
        node[keys[-1]] = float(v)
    open(p, "w", encoding="utf-8").write(txt[: m.start(1)] + yaml.safe_dump(y, allow_unicode=True, sort_keys=False) + txt[m.end(1):])
    return before


def _append_shock(d: str, s: dict) -> tuple[str, dict]:
    """가상의 다음 달을 데이터 끝에 붙인다 (live.l2와 같은 환산)."""
    pp = os.path.join(d, "data", "panel_monthly.csv")
    P = pd.read_csv(pp)
    nxt = (pd.Timestamp(P["date"].iloc[-1]) + pd.DateOffset(months=1)).strftime("%Y-%m-01")
    eq, dy = float(s["equity"]), float(s["rate_bp"]) / 100.0
    row = {"date": nxt, "ret_SPY": eq, "ret_EFA": eq, "ret_EEM": eq * 1.2, "ret_VNQ": eq * 1.1, "ret_GLD": float(s["gold"]), "ret_DBC": float(s["commodity"])}
    for t, D in DUR.items():
        row[f"ret_{t}"] = -D * dy + (0.4 * eq if t == "HYG" else 0.0)
    pd.concat([P, pd.DataFrame([row])[P.columns]], ignore_index=True).round(4).to_csv(pp, index=False)
    mp = os.path.join(d, "data", "macro_monthly.csv")
    M = pd.read_csv(mp)
    mr = M.iloc[-1].copy(); mr["date"] = nxt
    mr["DGS10"] += dy; mr["T10Y2Y"] += dy * 0.5; mr["CPIAUCSL"] *= 1.002
    mr["BAA10Y"] += 0.5 if eq <= -10 else 0.0
    pd.concat([M, pd.DataFrame([mr])], ignore_index=True).round(4).to_csv(mp, index=False)
    return nxt[:7], row


def _drop_decision(d: str, q: str) -> dict | None:
    """그 분기의 CIO 결정을 임시 복사본에서 지운다 — 사람 CIO가 화면에서 다시 결정한다. 지운 행(제출본의 기록)을 돌려준다."""
    p = os.path.join(d, "data", "cio_decisions.csv")
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    kept, gone = [r for r in rows if r["as_of"] != q], [r for r in rows if r["as_of"] == q]
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["as_of", "decision", "condition", "reason"]); w.writeheader(); w.writerows(kept)
    return gone[0] if gone else None


def _ls(folder: str, ext: str = ".json") -> list[str]:
    """폴더의 파일 목록 — glob은 경로의 [2026] 같은 대괄호를 패턴으로 읽어 쓰지 않는다."""
    return [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.endswith(ext)] if os.path.isdir(folder) else []


def _read(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def _json(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def view(d: str, q: str) -> dict:
    """한 분기의 산출물 파일을 그대로 모은다 — 화면의 단계마다 하나씩 보여 준다."""
    qd = os.path.join(d, "runs", q)
    cma = _json(os.path.join(qd, "cma.json"))
    if cma:
        cma = {k: v for k, v in cma.items() if k != "cov"} | {"cov": f"{len(cma.get('cov', []))}×{len(cma.get('cov', []))} 행렬 (생략 — cma.json에 있다)"}
    props = {os.path.basename(f)[:-5]: _json(f) for f in _ls(os.path.join(qd, "proposals"))}
    tr = os.path.join(qd, "trace.jsonl")
    return {"q": q, "macro": _read(os.path.join(qd, "macro.md")), "macro_json": _json(os.path.join(qd, "macro.json")), "cma": cma,
            "research": _read(os.path.join(qd, "research_memo.md")),
            "proposals": {k: {kk: v.get(kk) for kk in ("method", "family", "weights", "exp_ret", "exp_vol", "exp_sharpe") if kk in v} for k, v in props.items()},
            "proposals_change": [_json(f) for f in _ls(os.path.join(qd, "proposals_change"))],
            "eligibility": _json(os.path.join(qd, "eligibility.json")), "cro": _json(os.path.join(qd, "cro_report.json")),
            "reviews": _json(os.path.join(qd, "reviews.json")), "votes": _json(os.path.join(qd, "votes.json")),
            "ic": _read(os.path.join(qd, "ic_report.md")), "cio": _read(os.path.join(qd, "cio_decision.md")),
            "holdings": _json(os.path.join(qd, "holdings.json")), "meta": _json(os.path.join(qd, "meta_review.json")),
            "changes": _json(os.path.join(qd, "changes.json")),
            "trace": [json.loads(l) for l in open(tr, encoding="utf-8")] if os.path.exists(tr) else []}


def is_check(md: str | None) -> bool:
    return bool(md) and "점검" in (_top(md, "유형") or "")


def parse_check(md: str) -> dict:
    """점검 지시서: '유형: 공개 점검' + '- 점검: T1, T3' (+ '- 분기: 2024-11' — T7·T8이 쓴다). '전체'면 T1~T8."""
    from .selfcheck import TESTS
    items = _items(md); ids_all = [t[0] for t in TESTS]
    raw = items.get("점검", "")
    ids = ids_all if "전체" in raw else [t for t in ids_all if re.search(rf"\b{t}\b", raw.upper())]
    qs = re.findall(r"\d{4}-\d{2}", items.get("분기", ""))
    errors = [] if ids else [f"점검 항목이 없다 — '- 점검: T1 ~ T8 중 하나 이상 또는 전체'로 적는다"]
    bad = [x for x in qs if x not in quarters(include_last=True)]
    if bad:
        errors.append(f"없는 분기: {', '.join(bad)}")
    params = {}
    if qs:
        params["T7"] = {"q": qs[0]}; params["T8"] = {"qs": qs}
    return {"title": (re.search(r"^#\s+(.+)$", md, re.M) or [None, "점검 지시서"])[1], "ids": ids, "params": params, "errors": errors}


def run_check(md: str, intake_log: dict | None = None) -> dict:
    from . import selfcheck
    c = parse_check(md)
    check = {"점검 지시서": c["title"], "점검": c["ids"], "분기": c["params"].get("T8", {}).get("qs") or "기본값(T7 2024-11 · T8 2023-08·2024-11)", "오류": c["errors"]}
    if intake_log:
        check["접수 에이전트"] = intake_log
    if c["errors"]:
        return {"failed": True, "input_check": check}
    res = selfcheck.run(log=lambda *a: None, only=c["ids"], params=c["params"])
    check["결과"] = f"통과 {sum(r['pass'] for r in res)} / {len(res)}"
    return {"selfcheck": res, "input_check": check, "title": c["title"]}


def start(q: str, input_md: str | None, shock_md: str | None, intake_log: dict | None = None) -> dict:
    for md in (shock_md, input_md):   # 점검 지시서는 어느 칸에 올려도 된다
        if is_check(md):
            return run_check(md, intake_log)
    qs = quarters(include_last=True)
    inp = parse_input(input_md)
    sh = parse_shock(shock_md)
    q = inp["q"] or (sh.get("q") if sh else None) or q or qs[-1]
    errs = inp["errors"] + (sh["errors"] if sh else [])
    if sh and sh.get("q") and sh["q"] not in qs:
        errs.append(f"돌발 파일의 기준 분기 {sh['q']}가 없다 — 고를 수 있는 분기: {qs[0]} ~ {qs[-1]} (3개월 간격)")
    check = {"입력 파일": inp["name"], "기준 분기": q, "IPS 변경(입력)": inp["overrides"], "경고": inp["warnings"],
             "돌발": (sh["title"] + " · 유형 " + sh["kind_text"]) if sh else "없음", "오류": errs}
    if intake_log:
        check["접수 에이전트"] = intake_log   # 원문 파일 · 해석 방식 · 옮긴 항목과 근거 · 확인 필요 · 확인한 사람
    if errs:
        return {"failed": True, "input_check": check}

    d = copy_repo()
    ov = dict(inp["overrides"])
    note = ""
    if sh and sh["kind"] == "ips":
        ov.update(sh["overrides"])
    before = _apply_ips(d, ov) if ov else {}
    check["IPS 변경(적용)"] = {k: f"{before.get(k)} → {v}" for k, v in ov.items()}
    shock_row = None
    if sh and sh["kind"] == "market":
        q, shock_row = _append_shock(d, sh["shock"])
        note = f"가상의 한 달({q})을 붙이고 그 분기를 새로 결정한다 — 제출본에는 없는 분기다"
        check["기준 분기"] = f"{q} (시장 충격으로 새로 만든 분기)"
    if sh and sh["kind"] == "model":
        note = (f"판단 모델을 '{sh['model']}'로 바꿔 다시 실행했다. 예시 MVP의 판단 문장은 규칙 기반 대역이고 숫자는 코드가 계산하므로, "
                "결론이 제출본과 같아야 정상이다 — LLM을 쓰는 팀은 문장이 달라지는지 비교표로 보인다")
    code, env = f"from sdp import pipeline; pipeline.run_quarter('{q}')", None
    if sh and sh["kind"] == "defect":
        if "proposal" in sh:
            ep = {"agent": "injected", "method": "주입된 배분안", "family": "시험", "lens": "-", "w": sh["proposal"], "exp_ret": 0, "exp_vol": 0, "exp_sharpe": 0}
            code = f"from sdp import pipeline; pipeline.run_quarter('{q}', extra_proposal={ep!r})"
            check["결함 주입"] = f"배분안 'injected'(비중 합 {sh['proposal_sum']})를 후보에 끼웠다 — ④ IPS 적격 심사에서 걸러져야 한다"
        if "memo" in sh:
            env = {"SDP_INJECT_MEMO": sh["memo"]}
            check["결함 주입(메모)"] = f"리서치 메모에 한 줄 추가: {sh['memo']} — 하네스가 결정 시점 이후 날짜를 잡아야 한다"
        note = "결함 주입 — 시스템이 스스로 잡는지 본다. 코드는 고치지 않았다"
    recorded = _drop_decision(d, q)
    r = py(d, code, env_extra=env)
    pending = "PendingDecision" in r.stderr
    if "LookaheadError" in r.stderr:   # 하네스가 미래정보를 잡고 분기를 멈춤 = 결함을 잡았다
        msg = [l for l in r.stderr.splitlines() if "LookaheadError" in l][-1].split("LookaheadError:")[-1].strip()
        check["하네스 정지"] = msg
        check["판정"] = "결함을 잡았다 — 이 분기는 계산하지 않고 멈췄다(trace.jsonl에 lookahead 기록)"
        shutil.rmtree(d, ignore_errors=True)
        return {"failed": True, "halted": True, "input_check": check}
    if r.returncode != 0 and not pending:
        shutil.rmtree(d, ignore_errors=True)
        check["오류"] = [r.stderr[-800:]]
        return {"failed": True, "input_check": check}
    sid = uuid.uuid4().hex[:8]
    SESS[sid] = {"dir": d, "q": q, "recorded": recorded}
    sub = os.path.join(ROOT, "runs", q, "votes.json")
    return {"sid": sid, "q": q, "input_check": check, "shock": sh["md"] if sh else None, "shock_kind": sh["kind"] if sh else None,
            "shock_row": shock_row, "note": note, "recorded_decision": recorded, "pending": pending,
            "submitted_winner": json.load(open(sub))["winner"] if os.path.exists(sub) else None, "view": view(d, q)}


def decide(sid: str, decision: str, reason: str, condition: str = "") -> dict:
    """사람 CIO의 결정을 임시 복사본의 cio_decisions.csv에 적고 그 분기를 마저 진행한다."""
    s = SESS[sid]; d, q = s["dir"], s["q"]
    p = os.path.join(d, "data", "cio_decisions.csv")
    with open(p, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([q, decision, condition, reason or "시연 화면에서 결정"])
    r = py(d, f"from sdp import pipeline; pipeline.run_quarter('{q}')")
    if r.returncode != 0:
        return {"ok": False, "log": r.stderr[-800:]}
    return {"ok": True, "q": q, "view": view(d, q), "csv_row": [q, decision, condition, reason]}


def replay(q: str) -> dict:
    """제출본 그대로 — 다시 계산하지 않고 runs/{q}/ 를 읽는다."""
    return {"q": q, "view": view(ROOT, q), "input_check": {"입력 파일": "없음 (제출본 재생)", "기준 분기": q, "오류": []}}


def samples() -> dict:
    base = os.path.join(ROOT, "올릴파일")
    return {os.path.basename(f): open(f, encoding="utf-8").read() for f in _ls(base, ".md") + _ls(base, ".txt") if not os.path.basename(f).startswith("README")}
