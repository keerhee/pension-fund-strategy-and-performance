"""공개 점검 T1~T8 — 제출본을 건드리지 않도록 매번 임시 복사본에서 돌린다."""
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, time
from .data import ROOT

SKIP = {"__pycache__", ".git", ".venv", "_live"}


def copy_repo(with_runs: bool = True) -> str:
    d = tempfile.mkdtemp(prefix="sdp_check_")
    for name in os.listdir(ROOT):
        if name in SKIP or (name == "runs" and not with_runs):
            continue
        s = os.path.join(ROOT, name)
        (shutil.copytree if os.path.isdir(s) else shutil.copy2)(s, os.path.join(d, name), **({"ignore": shutil.ignore_patterns("__pycache__")} if os.path.isdir(s) else {}))
    if not with_runs:
        os.makedirs(os.path.join(d, "runs"))
    return d


def py(root: str, code: str, env_extra: dict | None = None, timeout=600) -> subprocess.CompletedProcess:
    env = dict(os.environ, SDP_ROOT=root, PYTHONPATH=root, **(env_extra or {}))
    return subprocess.run([sys.executable, "-c", code], cwd=root, env=env, capture_output=True, text=True, timeout=timeout)


def _load(p):
    return json.load(open(p, encoding="utf-8"))


def _numbers(qdir: str) -> dict:
    """코드로 계산한 숫자만 모은다 — 재현 대조 대상."""
    out = {"cma": {k: v for k, v in _load(os.path.join(qdir, "cma.json")).items()},
           "eligibility": _load(os.path.join(qdir, "eligibility.json")),
           "votes": {k: _load(os.path.join(qdir, "votes.json"))[k] for k in ("result", "ranking", "winner", "ballots")},
           "holdings": _load(os.path.join(qdir, "holdings.json"))["weights"]}
    for f in sorted(os.listdir(os.path.join(qdir, "proposals"))):
        out["prop_" + f] = _load(os.path.join(qdir, "proposals", f))["w"]
    return out


def t1(log):
    d = copy_repo(with_runs=False)
    r = py(d, "from sdp import pipeline; pipeline.run_quarter('2022-08')")
    ok = r.returncode == 0 and os.path.exists(os.path.join(d, "runs", "2022-08", "ic_report.md"))
    return ok, "새 폴더(실행 기록 없음)에서 첫 분기를 처음부터 실행 → ic_report.md 생성" if ok else (r.stderr[-600:] or r.stdout[-600:])


def t2(log):
    d = copy_repo()
    code = ("from sdp import pipeline; "
            "w=[0.5,0.1,0,0.1,0.1,0,0,0.1,0,0.05,0.05]; "
            "pipeline.run_quarter('2022-08', extra_proposal={'agent':'injected-50pct','method':'주입된 위반안','family':'시험','lens':'-','w':w,'exp_ret':0,'exp_vol':0,'exp_sharpe':0})")
    r = py(d, code)
    if r.returncode != 0:
        return False, r.stderr[-600:]
    el = _load(os.path.join(d, "runs", "2022-08", "eligibility.json"))["injected-50pct"]
    v = _load(os.path.join(d, "runs", "2022-08", "votes.json"))
    ok = (not el["eligible"]) and "injected-50pct" not in v["result"] and all("injected-50pct" not in b for b in v["ballots"].values())
    return ok, f"SPY 50% 안 주입 → 기각 사유: {'; '.join(el['violations'])} · 표결 목록에 {'없음' if ok else '있음'}"


def t3(log):
    d = copy_repo()
    code = """
import json, os
from sdp import harness as H
from sdp.data import ROOT
p = os.path.join(ROOT, 'config', 'params.json'); before = H.sha(p)
h = H.Harness('2025-05', os.path.join(ROOT, 'runs', '_t3'))
def rogue():
    prm = json.load(open(p)); prm['cma']['shrink_delta'] = 0.9
    json.dump(prm, open(p, 'w'))
    return {'outputs': []}
try:
    h.call('meta-reviewer', 'meta-review', rogue, [p]); print('NOT_BLOCKED')
except H.ProtectedFileError as e:
    print('BLOCKED', H.sha(p) == before)
"""
    r = py(d, code)
    ok = "BLOCKED True" in r.stdout
    return ok, "meta-reviewer 가 params.json(수축 강도 0.5→0.9)을 직접 고치려 함 → 하네스가 되돌리고 거부, trace 에 blocked 기록" if ok else (r.stdout + r.stderr)[-600:]


def t4(log):
    d = copy_repo()
    code = """
import os, json
from sdp import harness as H, data
from sdp.data import ROOT
h = H.Harness('2022-08', os.path.join(ROOT, 'runs', '_t4'))
try:
    h.call('cma-builder', 'cma-build', lambda: data.returns('2022-08', end='2022-12'), [])
    print('NOT_BLOCKED')
except data.AsOfViolation:
    rec = [json.loads(l) for l in open(h.trace_path)][-1]
    print('BLOCKED', 'error' in rec)
"""
    r = py(d, code)
    ok = "BLOCKED True" in r.stdout
    return ok, "as_of=2022-08 에서 2022-12 까지 요청 → AsOfViolation, trace 에 error 기록" if ok else (r.stdout + r.stderr)[-600:]


def t5(log):
    from .agents_review import borda_example
    e = borda_example()
    ok = e["score"] == {"A": 0.473, "B": 0.85, "C": 0.9, "D": 0.45} and e["winner"] == "C"
    return ok, f"득표 {e['S']} · Score {e['score']} · 채택 {e['winner']}"


def t6(log):
    a, b = copy_repo(with_runs=False), copy_repo(with_runs=False)
    for d in (a, b):
        r = py(d, "from sdp import pipeline; pipeline.run_quarter('2022-08')")
        if r.returncode != 0:
            return False, r.stderr[-600:]
    na, nb = _numbers(os.path.join(a, "runs", "2022-08")), _numbers(os.path.join(b, "runs", "2022-08"))
    ok = na == nb
    return ok, "같은 as_of 로 두 번 실행 → CMA·배분안·득표·보유 비중 완전 일치" if ok else "불일치: " + ", ".join(k for k in na if na[k] != nb.get(k))


def t7(log, q: str = "2024-11"):
    qd = os.path.join(ROOT, "runs", q)
    recs = [json.loads(l) for l in open(os.path.join(qd, "trace.jsonl"), encoding="utf-8")]
    produced = {}
    for r in recs:
        for o in r.get("outputs", []):
            produced[o["file"]] = (r["agent"], o["sha"])
    from .harness import sha
    chain, bad = [], []
    for r in recs:
        for i in r.get("inputs", []):
            f = i["file"]
            if f in produced:
                ok = produced[f][1] == i["sha"]
                chain.append(f"{produced[f][0]} → {r['agent']} ({os.path.basename(f)})")
                if not ok:
                    bad.append(f)
    for f, (_, h) in produced.items():
        if sha(os.path.join(ROOT, f)) != h:
            bad.append(f + " (제출 파일이 기록과 다름)")
    need = {"cma-builder", "pc-agents(6)", "ips-guardian", "vote", "ic-agent", "CIO(사람)"}
    seen = {r["agent"] for r in recs}
    ok = not bad and need <= seen
    return ok, (f"{q} 분기: " + " · ".join(dict.fromkeys(chain)) if ok else f"끊긴 고리: {bad or need - seen}")


def t8(log, qs=("2023-08", "2024-11")):
    d = copy_repo()
    msgs, ok = [], True
    for q in qs:
        r = py(d, f"from sdp import pipeline; pipeline.run_quarter('{q}')")
        if r.returncode != 0:
            return False, r.stderr[-600:]
        a, b = _numbers(os.path.join(ROOT, "runs", q)), _numbers(os.path.join(d, "runs", q))
        same = a == b
        md = all(os.path.exists(os.path.join(d, "runs", q, f)) for f in ("macro.md", "research_memo.md", "ic_report.md", "cio_decision.md"))
        ok &= same and md
        msgs.append(f"{q}: 숫자 {'일치' if same else '불일치'} · 판단 문서 양식 {'완비' if md else '누락'}")
    return ok, " / ".join(msgs)


TESTS = [("T1", "깨끗한 실행", t1), ("T2", "IPS 위반 주입", t2), ("T3", "자기 수정 시도", t3), ("T4", "미래정보 차단", t4),
         ("T5", "투표 검산", t5), ("T6", "계산 재현", t6), ("T7", "감사 추적", t7), ("T8", "증거 대조", t8)]


def run(log=print, only: list | None = None) -> list:
    res = []
    for tid, name, fn in TESTS:
        if only and tid not in only:
            continue
        t0 = time.time()
        try:
            ok, msg = fn(log)
        except Exception as e:
            ok, msg = False, f"{type(e).__name__}: {e}"
        res.append({"id": tid, "name": name, "pass": bool(ok), "detail": msg, "sec": round(time.time() - t0, 1)})
        log(f"  {tid} {name:<10} {'통과' if ok else '실패'}  {msg[:110]}")
    return res


def write(res: list):
    L = ["# 자가 점검 결과 (공개 점검 T1~T8)", "", f"통과 {sum(r['pass'] for r in res)} / {len(res)}", "", "| # | 점검 | 결과 | 내용 |", "|---|---|---|---|"]
    for r in res:
        L.append(f"| {r['id']} | {r['name']} | {'통과' if r['pass'] else '**실패**'} | {r['detail']} |")
    open(os.path.join(ROOT, "reports", "selfcheck.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump(res, open(os.path.join(ROOT, "reports", "selfcheck.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
