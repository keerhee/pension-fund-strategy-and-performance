"""정적 대시보드 — 채점 콘솔과 같은 화면을 데이터만 담아 한 파일로 만든다(버튼은 비활성). 파이썬 없이 열어 볼 수 있다."""
import json, os
from .data import ROOT
from .server import summary, quarter


def build():
    s = summary()
    data = {"summary": s, "quarters": {r["q"]: quarter(r["q"]) for r in s["quarters"]}}
    html = open(os.path.join(ROOT, "console", "index.html"), encoding="utf-8").read()
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("<script>\nconst STATIC", f"<script>window.STATIC_DATA = {blob};</script>\n<script>\nconst STATIC", 1)
    open(os.path.join(ROOT, "dashboard.html"), "w", encoding="utf-8").write(html)
    return os.path.join(ROOT, "dashboard.html")
