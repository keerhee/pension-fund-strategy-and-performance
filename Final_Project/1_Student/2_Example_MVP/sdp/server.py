"""채점 콘솔 — 브라우저 버튼으로 제출본을 다시 계산하고 점검한다.

    python -m sdp serve        (start.command / start.bat 가 대신 실행)
    → http://localhost:8765

모든 버튼은 제출 폴더를 건드리지 않고 임시 복사본에서 돈다.
"""
from __future__ import annotations
import json, os, threading, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from .data import ROOT
from . import live, selfcheck, perf
from .pipeline import quarters

PORT = int(os.environ.get("SDP_PORT", "8765"))


def _read(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def summary() -> dict:
    qs = [q for q in quarters(include_last=True) if os.path.exists(os.path.join(ROOT, "runs", q, "votes.json"))]
    rows = []
    for q in qs:
        v = json.load(open(os.path.join(ROOT, "runs", q, "votes.json")))
        h = os.path.join(ROOT, "runs", q, "holdings.json")
        el = json.load(open(os.path.join(ROOT, "runs", q, "eligibility.json")))
        mac = json.load(open(os.path.join(ROOT, "runs", q, "macro.json")))
        rows.append({"q": q, "winner": v["winner"], "decision": json.load(open(h))["decision"] if os.path.exists(h) else "대기",
                     "regime": mac["label"], "rejected": [k for k, e in el.items() if not e["eligible"]]})
    pj = os.path.join(ROOT, "reports", "performance.json")
    sj = os.path.join(ROOT, "reports", "selfcheck.json")
    return {"quarters": rows, "performance": json.load(open(pj)) if os.path.exists(pj) else None,
            "selfcheck": json.load(open(sj)) if os.path.exists(sj) else None,
            "docs": {k: _read(os.path.join(ROOT, f)) for k, f in [("readme", "README.md"), ("ips", "ips.md"), ("changelog", "CHANGELOG.md"),
                                                                  ("interventions", "INTERVENTIONS.md"), ("resolution", "reports/resolution.md"),
                                                                  ("performance", "reports/performance.md"), ("prereg", "PREREG.md")]}}


def quarter(q: str) -> dict:
    qd = os.path.join(ROOT, "runs", q)
    out = {k: _read(os.path.join(qd, f)) for k, f in [("ic_report", "ic_report.md"), ("cio", "cio_decision.md"), ("macro", "macro.md"), ("research", "research_memo.md")]}
    for k in ("votes", "eligibility", "cro_report", "holdings", "meta_review", "reviews", "changes"):
        f = os.path.join(qd, k + ".json")
        out[k] = json.load(open(f)) if os.path.exists(f) else None
    out["trace"] = [json.loads(l) for l in open(os.path.join(qd, "trace.jsonl"), encoding="utf-8")] if os.path.exists(os.path.join(qd, "trace.jsonl")) else []
    return out


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        b = body if isinstance(body, bytes) else (json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body).encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path); qs = parse_qs(u.query)
        try:
            if u.path in ("/", "/index.html"):
                return self._send(200, _read(os.path.join(ROOT, "console", "index.html")), "text/html; charset=utf-8")
            if u.path == "/api/summary":
                return self._send(200, summary())
            if u.path == "/api/quarter":
                return self._send(200, quarter(qs["q"][0]))
            return self._send(404, {"error": "없는 경로"})
        except Exception as e:
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        p = urlparse(self.path).path
        try:
            if p == "/api/recompute":
                return self._send(200, live.recompute(body["q"]))
            if p == "/api/selfcheck":
                res = selfcheck.run(log=lambda *a: None, only=body.get("only"))
                if not body.get("only"):
                    selfcheck.write(res)
                return self._send(200, res)
            if p == "/api/l1":
                return self._send(200, live.l1(body["q"], body["overrides"]))
            if p == "/api/l2":
                return self._send(200, live.l2(float(body["equity"]), float(body["rate_bp"]), float(body["gold"]), float(body["commodity"])))
            if p == "/api/l3":
                return self._send(200, live.l3(body["kind"], body.get("q", "2024-11")))
            return self._send(404, {"error": "없는 경로"})
        except Exception as e:
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})


def serve(open_browser: bool = True):
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://localhost:{PORT}"
    print(f"채점 콘솔: {url}  (끝내려면 이 창에서 Ctrl+C)")
    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
