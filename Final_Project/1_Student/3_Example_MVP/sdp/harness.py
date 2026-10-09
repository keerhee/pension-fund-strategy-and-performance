"""하네스 — 감사 기록(trace), 보호 파일, 킬스위치.

- 모든 에이전트 호출은 Harness.call() 을 거친다. 입력·출력 파일의 해시와 근거가 trace.jsonl 에 남는다.
- 보호 파일(ips.md, config/params.json, .claude/skills/**)은 호출 전후 해시를 비교한다.
  에이전트가 고쳤다면 원래대로 되돌리고 ProtectedFileError 를 던진다.
- 보호 파일을 바꾸는 유일한 길은 apply_change() — CIO 승인(data/approvals.csv)과 테스트 통과가 모두 있어야 한다.
"""
from __future__ import annotations
import glob, hashlib, json, os, shutil
from .data import ROOT

PROTECTED = ["ips.md", "config/params.json", "config/param_changes.json"]


class ProtectedFileError(Exception):
    pass


class LookaheadError(Exception):
    pass


import re
_DATE = re.compile(r"(20\d{2})\s*[-./년]\s*(\d{1,2})(?!\d)")


def future_dates(text: str, as_of: str) -> list[str]:
    """에이전트가 쓴 문장에서 as_of 이후 연월을 찾는다 — 미래정보 혼입 탐지."""
    a = (int(as_of[:4]), int(as_of[5:7]))
    hits = []
    for y, m in _DATE.findall(text):
        if 1 <= int(m) <= 12 and (int(y), int(m)) > a:
            hits.append(f"{y}-{int(m):02d}")
    return sorted(set(hits))


def sha(path: str) -> str:
    if not os.path.exists(path):
        return "-"
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def protected_files() -> list[str]:
    fs = [os.path.join(ROOT, p) for p in PROTECTED]
    fs += sorted(glob.glob(os.path.join(ROOT, ".claude", "skills", "**", "*.md"), recursive=True))
    return fs


def _changes() -> list:
    p = os.path.join(ROOT, "config", "param_changes.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def load_params(as_of: str | None = None) -> dict:
    """기본 파라미터 + 그 시점까지 승격된 변경. 변경은 승인한 다음 분기부터 효력이 있다."""
    prm = json.load(open(os.path.join(ROOT, "config", "params.json"), encoding="utf-8"))
    for ch in _changes():
        if as_of is None or ch["effective_after"] < as_of:
            sec, key = ch["path"]
            prm[sec][key] = ch["new"]
    return prm


class Harness:
    def __init__(self, as_of: str, run_dir: str):
        self.as_of, self.run_dir = as_of, run_dir
        os.makedirs(run_dir, exist_ok=True)
        self.trace_path = os.path.join(run_dir, "trace.jsonl")
        open(self.trace_path, "w").close()
        self.seq = 0

    def rel(self, p: str) -> str:
        return os.path.relpath(p, ROOT)

    def call(self, agent: str, skill: str, fn, inputs: list[str], note: str = "", constraints: list[str] | None = None):
        snap = {p: (sha(p), open(p, "rb").read() if os.path.exists(p) else None) for p in protected_files()}
        in_h = [{"file": self.rel(p), "sha": sha(p)} for p in inputs]
        err = None
        try:
            result = fn()
        except Exception as e:  # 실패도 감사 기록에 남긴다
            err, result = e, {}
        finally:
            touched = [p for p, (h, _) in snap.items() if sha(p) != h]
            for p in touched:  # 되돌린다
                open(p, "wb").write(snap[p][1])
        outs = result.get("outputs", []) if isinstance(result, dict) else []
        future = []
        for p in outs:
            if p.endswith(".md"):
                future += future_dates(open(p, encoding="utf-8").read(), self.as_of)
        self.seq += 1
        rec = {"seq": self.seq, "as_of": self.as_of, "agent": agent, "skill": skill, "inputs": in_h,
               "outputs": [{"file": self.rel(p), "sha": sha(p)} for p in outs],
               "constraints": constraints or [], "note": (result.get("note") if isinstance(result, dict) else None) or note}
        if touched:
            rec["blocked"] = [self.rel(p) for p in touched]
        if err is not None:
            rec["error"] = f"{type(err).__name__}: {err}"
        if future:
            rec["lookahead"] = future
        with open(self.trace_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if err is not None:
            raise err
        if future:
            raise LookaheadError(f"{agent} 산출물에 결정 시점({self.as_of}) 이후 날짜 {future} — 미래정보 혼입 의심, 이 분기를 멈춘다")
        if touched:
            raise ProtectedFileError(f"{agent} 가 보호 파일을 수정하려 함: {[self.rel(p) for p in touched]} — 되돌림")
        return result

    def log(self, agent: str, note: str, **kw):
        self.seq += 1
        rec = {"seq": self.seq, "as_of": self.as_of, "agent": agent, "note": note, **kw}
        with open(self.trace_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def approvals() -> dict:
    p = os.path.join(ROOT, "data", "approvals.csv")
    out = {}
    if os.path.exists(p):
        import csv
        for r in csv.DictReader(open(p, encoding="utf-8")):
            out[r["proposal_id"]] = r
    return out


def apply_change(proposal: dict, as_of: str) -> dict:
    """킬스위치를 통과하는 유일한 경로. 승인 + 테스트 통과일 때만 params.json 을 고친다."""
    pid = proposal["id"]
    ap = approvals().get(pid)
    status = {"id": pid, "as_of": as_of, "target": proposal["target"], "change": proposal["change"]}
    if not ap or ap["decision"] != "승인":
        status.update(result="미반영", why=("CIO 반려: " + ap["reason"]) if ap else "CIO 승인 없음")
        return status
    test = proposal.get("test", {})
    if proposal["kind"] == "param" and not test.get("improved", False):
        status.update(result="롤백", why=f"테스트 미통과 ({test.get('summary','')})")
        return status
    if proposal["kind"] == "param":
        p = os.path.join(ROOT, "config", "param_changes.json")
        chs = _changes()
        if not any(c["id"] == pid for c in chs):
            chs.append({"id": pid, "path": proposal["path"], "old": proposal["old"], "new": proposal["new"], "effective_after": as_of})
            json.dump(chs, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        status.update(result="승격", why=f"CIO 승인({ap['date']}) + 테스트 통과 ({test.get('summary','')})")
    else:
        status.update(result="승격(문서)", why="CIO 승인")
    return status


def snapshot_protected(dst: str):
    os.makedirs(dst, exist_ok=True)
    for p in PROTECTED:
        q = os.path.join(dst, p.replace("/", "__"))
        shutil.copy(os.path.join(ROOT, p), q)
