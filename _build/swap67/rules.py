# -*- coding: utf-8 -*-
"""W06 ↔ W07 맞바꾸기 규칙 (2026-10-03).

주차: 6 ↔ 7  (W06/W6/WEEK 6/Week 6/6주차/6주 ↔ 7)
모듈: M7(동적) → M9 · M8(LDI) → M7 · M9(GBI) → M8
두 번호를 모두 덮는 범위(W5–W7, W6~W7, M1–M9, M7–M9 …)는 집합이 그대로라 손대지 않는다.
"""
import re

WK = {"6": "7", "7": "6"}
MD = {"7": "9", "8": "7", "9": "8"}
DASH = r"\s*[–\-~〜∼]\s*"

# 범위: 앞뒤 번호를 함께 본다
RANGE_W = re.compile(r"(?<![A-Za-z0-9])(W)(0?)(\d{1,2})(" + DASH + r")(W?)(0?)(\d{1,2})(?![0-9])")
RANGE_M = re.compile(r"(?<![A-Za-z0-9])(M)(\d{1,2})(" + DASH + r")(M?)(\d{1,2})(?![0-9])")
RANGE_K = re.compile(r"(?<![0-9])(\d{1,2})(" + DASH + r")(\d{1,2})(주차|주)")
TOK = re.compile(
    r"(?P<w>(?<![A-Za-z0-9])W0?(?P<wn>[67])(?![0-9]))"
    r"|(?P<wk>(?<![A-Za-z])(?:WEEK|Week|week)\s?(?P<wkn>[67])(?![0-9]))"
    r"|(?P<k>(?<![0-9.,])(?P<kn>[67])(?P<ks>주차|주)(?!간|일|년))"
    r"|(?P<m>(?<![A-Za-z0-9])M(?P<mn>[789])(?![0-9]))"
    r"|(?P<f>(?<![A-Za-z0-9])W0?(?P<fn>[67])_)")


def _range_keep(a, b, swapset):
    """범위 a~b 가 swapset 을 전부 덮거나 전혀 안 덮으면 그대로 둔다."""
    a, b = int(a), int(b)
    cov = {x for x in swapset if a <= x <= b}
    return len(cov) in (0, len(swapset))


def swap(text, log=None):
    """text 안의 주차·모듈 표기를 맞바꾼다. 범위는 집합이 같을 때만 그대로 둔다."""
    out, pos = [], 0
    spans = []
    for rx, kind in ((RANGE_W, "W"), (RANGE_M, "M"), (RANGE_K, "K")):
        for m in rx.finditer(text):
            if kind == "W":
                a, b = m.group(3), m.group(7)
                keep = _range_keep(a, b, {6, 7})
            elif kind == "M":
                a, b = m.group(2), m.group(5)
                keep = _range_keep(a, b, {7, 8, 9})
            else:
                a, b = m.group(1), m.group(3)
                keep = _range_keep(a, b, {6, 7})
            spans.append((m.start(), m.end(), keep, kind, m.group(0)))
    def in_range(i):
        for s, e, keep, kind, g in spans:
            if s <= i < e:
                return (keep, kind, g)
        return None
    def rep(m):
        r = in_range(m.start())
        if r is not None and r[0]:
            if log is not None: log.append(("범위유지", r[2]))
            return m.group(0)
        if r is not None and not r[0]:
            if log is not None: log.append(("범위변경?", r[2]))
        g = m.group(0)
        if m.group("w"):
            n = m.group("wn"); new = g.replace(n, WK[n])
        elif m.group("wk"):
            n = m.group("wkn"); new = g[:-1] + WK[n]
        elif m.group("k"):
            n = m.group("kn"); new = WK[n] + m.group("ks")
        elif m.group("m"):
            n = m.group("mn"); new = "M" + MD[n]
        else:
            n = m.group("fn"); new = g.replace(n, WK[n])
        if log is not None: log.append((g, new))
        return new
    return TOK.sub(rep, text)
