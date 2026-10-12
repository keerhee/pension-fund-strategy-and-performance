"""접수 에이전트(intake-agent) — 어떤 형식으로 들어온 입력이든 엔진이 읽는 표준 형식으로 옮긴다.

원칙: 계산은 코드, 판단은 에이전트, 결정은 사람.
  · 이 에이전트는 "해석"만 한다 — 바꿀 항목과 값을 뽑고, 근거가 된 원문 구절을 붙이고, 모르는 것은 '확인 필요'로 남긴다.
  · 해석은 사람이 화면에서 ✓ 확인해야 입력이 된다. 숫자 계산은 여전히 파이프라인(코드)이 한다.
  · 표준 형식으로 쓴 파일은 해석하지 않고 그대로 읽는다.

두 가지 방식:
  · LLM — 환경변수 ANTHROPIC_API_KEY가 있으면 Claude가 해석한다 (모델: SDP_INTAKE_MODEL, 기본 claude-sonnet-5-5).
  · 규칙 대역 — 키가 없으면 정해진 낱말·숫자 규칙으로 해석한다. 채점자 컴퓨터에서 키 없이도 같은 결과가 나와야 하므로
    예시 MVP의 다른 에이전트처럼 대역을 기본으로 둔다.
"""
from __future__ import annotations
import json, os, re, urllib.request
from . import demo
from .pipeline import quarters

# 항목 이름(표준) → 원문에서 찾을 말들
IPS_WORDS = {
    "유효 종목 수 하한": [r"유효\s*종목\s*수", r"분산\s*요건", r"N[_ ]?eff", r"유효\s*자산\s*수"],
    "변동성 상한": [r"변동성\s*(상한|한도|제한|캡)", r"vol[_ ]?cap", r"사전\s*변동성"],
    "종목 상한": [r"종목\s*(상한|한도)", r"한\s*종목", r"단일\s*(자산|종목)\s*(상한|한도|최대)", r"asset[_ ]?max"],
    "종목 하한": [r"종목\s*하한", r"asset[_ ]?min"],
    "주식 하한": [r"주식[^.,\n]{0,12}(하한|최소)"], "주식 상한": [r"주식[^.,\n]{0,12}(상한|최대)"],
    "채권 하한": [r"채권[^.,\n]{0,12}(하한|최소)"], "채권 상한": [r"채권[^.,\n]{0,12}(상한|최대)"],
    "대체 하한": [r"대체[^.,\n]{0,12}(하한|최소)"], "대체 상한": [r"대체[^.,\n]{0,12}(상한|최대)"],
}
MARKET_WORDS = {
    "주식 한 달 수익률": [r"주식", r"증시", r"주가", r"S&P", r"코스피"],
    "금리 변화": [r"금리", r"국채\s*수익률", r"10년물"],
    "금": [r"(?<![가-힣])금(?![리융])", r"\bgold\b"],
    "원자재": [r"원자재", r"원유", r"유가", r"commodit"],
}
NUM = r"[-+−]?\d+(?:\.\d+)?"
# 엔진이 읽지 않는 주제 — 나오면 '확인 필요'로 알린다
UNSUPPORTED = [r"신용\s*스프레드", r"환율", r"달러", r"부동산\s*(가격|지수)", r"인플레이션\s*기대", r"부채\s*듀레이션", r"적립률"]


def _clauses(s: str) -> list[str]:
    """'금은 3% 오르고 원자재는 5% 하락' → 두 구절 — 오르내림은 구절 안에서만 읽는다."""
    return [c for c in re.split(r"(?<=[고며])\s+|,\s*|，", s) if c.strip()]


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?。])\s+|\n+|(?<=다)\s+|·|;", text)
    return [p.strip(" -*>#\t") for p in parts if p and p.strip(" -*>#\t")]


def _quarter(text: str) -> tuple[str | None, str | None]:
    qs = quarters(include_last=True)
    m = re.search(r"(20\d\d)\s*[-./년]\s*(\d{1,2})\s*월?", text)
    if not m:
        return None, None
    q = f"{m.group(1)}-{int(m.group(2)):02d}"
    return (q if q in qs else None), m.group(0)


def _value_after(s: str, start: int) -> tuple[float | None, str]:
    """키워드 뒤의 숫자 — '4.0에서 3.5로', '10% → 8%'처럼 바뀌는 값이면 마지막 숫자."""
    tail = s[start:start + 60]
    nums = [(m.group(1), m.group(2) or "") for m in re.finditer("(" + NUM + r")\s*(%p|%|bp|퍼센트)?", tail.replace("−", "-"))]
    if not nums:
        return None, ""
    if len(nums) >= 2 and re.search(r"→|->|에서\s*" + NUM + r"[^.]{0,8}(로|으로)", tail):
        v, unit = nums[1]
    else:
        v, unit = nums[0]
    return float(v), unit


def _rule(text: str, slot: str) -> dict:
    items, quotes, unclear, mentioned = {}, {}, [], {}
    q, qq = _quarter(text)
    sents = _sentences(text)
    used = set()
    for s in sents:
        for key, pats in IPS_WORDS.items():
            if key in items:
                continue
            m = next((re.search(p, s, re.I) for p in pats if re.search(p, s, re.I)), None)
            if not m:
                continue
            v, unit = _value_after(s, m.end())
            if v is None:
                mentioned.setdefault(key, s); continue
            items[key] = f"{v:g}%" if (unit in ("%", "퍼센트") or (key != "유효 종목 수 하한" and v > 1)) else (f"{v * 100:g}%" if key != "유효 종목 수 하한" else f"{v:g}")
            quotes[key] = s; used.add(s)
    for key, s in mentioned.items():
        if key not in items:
            unclear.append(f"'{key}' 이야기가 있으나 바꿀 값이 없다 — 바꾸려는 것이면 값을 적는다: “{s}”")
    market = {}
    for s in [c for x in sents for c in _clauses(x)]:
        for key, pats in MARKET_WORDS.items():
            if key in market:
                continue
            m = next((re.search(p, s, re.I) for p in pats if re.search(p, s, re.I)), None)
            if not m or any(re.search(p, s, re.I) for ps in IPS_WORDS.values() for p in ps):
                continue
            v, unit = _value_after(s, m.end())
            if v is None:
                continue
            down = re.search(r"하락|빠지|빠진|떨어|급락|내리|내린|내려|인하|폭락|하향|줄어|감소|마이너스", s[m.end():m.end() + 40])
            if key == "금리 변화":
                bp = v * 100 if unit in ("%p", "%", "퍼센트") else v
                market[key] = f"{-abs(bp) if down else (bp if bp < 0 else abs(bp)):+g}bp"
            else:
                x = -abs(v) if down else v
                market[key] = f"{x:+g}%"
            quotes[key] = s; used.add(s)
    used |= {x for x in sents if any(c in used for c in _clauses(x))}
    model = None
    for s in sents:
        m = re.search(r"(판단\s*)?모델[^.\n]{0,20}(교체|바꾸|바꿔|변경)", s)
        if m:
            nm = re.search(r"((?:llm|claude|gpt)[-A-Za-z0-9._]+|[A-Za-z][A-Za-z0-9._-]*-\d[A-Za-z0-9._-]*)", s, re.I)
            model = nm.group(1) if nm else "새 모델"; quotes["판단 모델"] = s; used.add(s)
    for s in sents:
        hit = next((p for p in UNSUPPORTED if re.search(p, s)), None)
        if hit:
            unclear.append(f"엔진이 읽지 않는 항목이 있다(무시함): “{s}”")
            used.add(s)
    for s in sents:
        if s not in used and re.search(r"\d", s) and not re.fullmatch(r".*(20\d\d)\s*[-./년]\s*\d{1,2}\s*월?.*", s) and len(s) > 6:
            unclear.append(f"숫자가 있으나 어느 항목인지 모른다: “{s}”")
    return _assemble(slot, q, qq, items, market, model, quotes, unclear, "규칙 대역 (키 없음 — 정해진 낱말·숫자 규칙)")


def _assemble(slot, q, qq, items, market, model, quotes, unclear, method) -> dict:
    kind = "market" if market else ("model" if model and not items else ("ips" if items else "none"))
    if slot == "input" and kind in ("market", "model"):
        unclear.insert(0, "입력 칸에 시장 충격·모델 교체 내용이 있다 — 돌발 과제 칸에 올려야 한다")
    if kind == "none":
        unclear.insert(0, "엔진이 쓸 항목을 하나도 찾지 못했다 — 표준 형식으로 고쳐 올리거나 내용을 더 분명히 적는다")
    lines = []
    if slot == "input":
        lines = ["# 입력 파일 — 접수 에이전트가 옮긴 표준 형식"]
        if q:
            lines.append(f"기준 분기: {q}")
        lines += ["", "## IPS 변경"] + [f"- {k}: {v}" for k, v in items.items()]
    else:
        title = {"ips": "IPS 변경", "market": "시장 충격", "model": "모델 교체"}.get(kind, "알 수 없음")
        lines = [f"# 돌발 과제 — 접수 에이전트가 옮긴 표준 형식", f"유형: {title}", "", "## 변경 내용"]
        if kind == "ips":
            lines += [f"- {k}: {v}" for k, v in items.items()]
        elif kind == "market":
            lines += [f"- {k}: {v}" for k, v in market.items()]
        elif kind == "model":
            lines.append(f"- 판단 모델: {model}")
    mapping = [{"항목": k, "값": v, "근거": quotes.get(k, "")} for k, v in {**items, **market, **({"판단 모델": model} if model else {})}.items()]
    if qq:
        mapping.insert(0, {"항목": "기준 분기", "값": q or f"{qq} (없는 분기)", "근거": qq})
    blocking = kind == "none" or (slot == "input" and kind in ("market", "model"))
    return {"method": method, "kind": kind, "standard_md": "\n".join(lines) + "\n", "mapping": mapping, "unclear": unclear, "can_confirm": not blocking}


def _llm(text: str, slot: str, key: str) -> dict:
    model = os.environ.get("SDP_INTAKE_MODEL", "claude-sonnet-5-5")
    qs = quarters(include_last=True)
    sysmsg = ("너는 연기금 자율주행 포트폴리오 시스템의 접수 에이전트다. 사람이 보낸 글을 엔진 입력으로 옮긴다. "
              "추측하지 말고, 글에 없는 값은 만들지 않는다. 애매하면 unclear에 적는다. JSON 하나만 출력한다.")
    user = f"""글의 종류: {'입력 파일(IPS 변경)' if slot == 'input' else '돌발 과제'}
허용 항목(IPS): {list(IPS_WORDS)} — 값은 퍼센트 항목이면 'N%', 유효 종목 수 하한은 숫자
허용 항목(시장 충격): 주식 한 달 수익률(%) · 금리 변화(bp, %p는 ×100) · 금(%) · 원자재(%) — 하락은 음수
모델 교체: 판단 모델 이름
기준 분기 후보: {qs}
출력 JSON 형식: {{"quarter": "YYYY-MM 또는 null", "ips": {{항목: 값}}, "market": {{항목: 값}}, "model": "이름 또는 null",
 "quotes": {{항목: "근거가 된 원문 구절"}}, "unclear": ["확인이 필요한 점"]}}
글:
<<<
{text}
>>>"""
    body = json.dumps({"model": model, "max_tokens": 1200, "system": sysmsg, "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    out = json.load(urllib.request.urlopen(req, timeout=60))
    raw = "".join(b.get("text", "") for b in out.get("content", []))
    j = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
    unclear = list(j.get("unclear") or [])
    items = {k: str(v) for k, v in (j.get("ips") or {}).items() if k in IPS_WORDS}
    market = {k: str(v) for k, v in (j.get("market") or {}).items() if k in MARKET_WORDS}
    dropped = [k for k in list((j.get("ips") or {})) + list((j.get("market") or {})) if k not in IPS_WORDS and k not in MARKET_WORDS]
    if dropped:
        unclear.append("허용 항목이 아니라 버린 것: " + ", ".join(dropped))
    q = j.get("quarter") if j.get("quarter") in qs else None
    if j.get("quarter") and not q:
        unclear.append(f"기준 분기 {j.get('quarter')}는 고를 수 있는 분기가 아니다")
    return _assemble(slot, q, j.get("quarter"), items, market, j.get("model"), j.get("quotes") or {}, unclear, f"LLM ({model})")


def interpret(text: str, slot: str, name: str = "") -> dict:
    """slot: 'input' | 'shock'. 표준 형식이면 그대로, 아니면 LLM(키가 있을 때) 또는 규칙 대역으로 해석한다."""
    if demo.is_check(text):
        c = demo.parse_check(text)
        return {"method": "표준 형식 — 점검 지시서, 해석 없이 그대로 읽음", "kind": "check", "standard_md": text,
                "mapping": [{"항목": "점검", "값": ", ".join(c["ids"]), "근거": "표준 형식"}], "unclear": c["errors"], "can_confirm": not c["errors"], "name": name}
    std = demo.parse_input(text) if slot == "input" else demo.parse_shock(text)
    if slot == "input" and not std["errors"] and std["overrides"] and re.search(r"^##\s*IPS 변경", text, re.M):
        return {"method": "표준 형식 — 해석 없이 그대로 읽음", "kind": "ips", "standard_md": text, "mapping": [{"항목": k, "값": v, "근거": "표준 형식"} for k, v in std["overrides"].items()],
                "unclear": std["warnings"], "can_confirm": True, "name": name}
    if slot == "shock" and std and not std["errors"]:
        return {"method": "표준 형식 — 해석 없이 그대로 읽음", "kind": std["kind"], "standard_md": text, "mapping": [], "unclear": [], "can_confirm": True, "name": name}
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        try:
            r = _llm(text, slot, key)
        except Exception as e:   # 네트워크·키 문제 — 대역으로 내려가고 그 사실을 남긴다
            r = _rule(text, slot); r["method"] += f" · LLM 호출 실패로 대역 사용 ({type(e).__name__})"
    else:
        r = _rule(text, slot)
    r["name"] = name
    return r
