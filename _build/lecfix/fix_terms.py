# -*- coding: utf-8 -*-
"""용어 정리 — 어색한 말을 실무 표기로 바꾼다 (2026-09-21 사용자 지시).

  표류 경로      → 자연감소경로
  필요 매도      → 연간 순매도 소요액
  정합성(조건 ③) → 국내주식 상한 (해외주식 목표 유지조건)
  이행 한도      → 연간 매도 한도
  참여율 한도    → 거래참여율 한도
  강건 해        → 강건최적화결과
  시장 점유      → 시가총액 대비 보유비중
  기계적 매도    → 기계적 리밸런싱 매도

'정합성'은 W04 M4 두 덱에서만 조건 ③의 이름이다 — M5·W05에서는 '역최적화의 자체 정합성',
'뷰와 위험예산의 정합성'처럼 다른 뜻이라 건드리지 않는다.
'참여율'은 W06 SS2 세 덱에서도 같은 뜻이라 함께 바꾼다.

실행: .venv/bin/python _build/lecfix/fix_terms.py [--dry]
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import Presentation, replace_all, grep

R = os.path.dirname(os.path.dirname(HERE))
DRY = "--dry" in sys.argv

# (긴 것부터) 공통 규칙
BASE = [
    ("표류 경로", "자연감소경로"),
    ("표류", "자연감소"),
    ("연 필요 순매도", "연간 순매도 소요액"),
    ("필요 매도액", "연간 순매도 소요액"),
    ("필요 매도", "연간 순매도 소요액"),
    ("이행 한도", "연간 매도 한도"),
    ("참여율 한도", "거래참여율 한도"),
    ("참여율", "거래참여율"),
    ("강건 해", "강건최적화결과"),
    ("시장 점유", "시가총액 대비 보유비중"),
    ("기계적 매도", "기계적 리밸런싱 매도"),
]
# 조건 ③ 이름 — 정의가 나오는 자리에는 괄호 설명을 붙인다(긴 것 먼저).
COND3 = [
    # 조건을 정식으로 정의하는 두 자리(판정 조건 한눈에 · 조건표)에만 괄호 설명을 붙인다.
    # 다른 곳에 다 붙이면 배너·표 칸이 넘친다.
    ("조건 ③ 2031 정합성 조건", "조건 ③ 국내주식 상한 조건"),
    ("제1호 조건 ③ 2031 정합성", "제1호 조건 ③ 국내주식 상한 (해외주식 목표 유지조건)"),
    ("조건 ③ 2031 정합성", "조건 ③ 국내주식 상한 (해외주식 목표 유지조건)"),
    ("정합성 상한", "국내주식 상한"),
    ("2031 정합성", "2031 국내주식 상한"),
    ("정합성 위반", "국내주식 상한 위반"),
    ("정합성 파라미터", "국내주식 상한 파라미터"),
    ("정합성", "국내주식 상한"),
]

DECKS = {
    f"{R}/W04_MVO와블랙리터맨/W04_M4_MVO와공분산추정_강의본.pptx": BASE + COND3,
    f"{R}/W04_MVO와블랙리터맨/W04_M4_케이스_2027-2031자산배분결정_기금운용위.pptx": BASE + COND3,
    f"{R}/W04_MVO와블랙리터맨/W04_M4_실습데이터_MVO와공분산추정.pptx": BASE,
    f"{R}/W05_리스크패리티와HRP/W05_리스크패리티와HRP_강의본.pptx": [("강건 해", "강건최적화결과")],
    f"{R}/W06_동적포트폴리오와장기투자/W06_특별세션_SS2_재균형프리미엄_강의본.pptx":
        [("참여율 한도", "거래참여율 한도"), ("참여율", "거래참여율")],
    f"{R}/W06_동적포트폴리오와장기투자/W06_특별세션_SS2_케이스1_국민연금리밸런싱규칙_IC.pptx":
        [("참여율 한도", "거래참여율 한도"), ("참여율", "거래참여율")],
    f"{R}/W06_동적포트폴리오와장기투자/W06_특별세션_SS2_케이스2_4기관차등규칙_IC.pptx":
        [("참여율 한도", "거래참여율 한도"), ("참여율", "거래참여율")],
}

def to_pdf(p):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    os.path.dirname(p), p], check=True, capture_output=True)

total = 0
for path, rules in DECKS.items():
    if not os.path.exists(path):
        print(f"!! 없음 {path}"); continue
    prs = Presentation(path)
    n = 0
    for a, b in rules:
        k = replace_all(prs, a, b)
        if k:
            n += k
            print(f"   {os.path.basename(path)[:44]:46s} {a!r} → {b!r}  {k}건")
    if n and not DRY:
        prs.save(path); to_pdf(path)
        print(f"== 저장·PDF {os.path.basename(path)} ({n}건)")
    total += n

print(f"\n덱 치환 총 {total}건" + (" (dry run)" if DRY else ""))

# 남은 말이 있는지 확인
if not DRY:
    LEFT = ["표류", "필요 매도", "이행 한도", "참여율", "강건 해", "시장 점유", "기계적 매도"]
    for path in DECKS:
        prs = Presentation(path)
        for t in LEFT:
            hits = grep(prs, re.escape(t))
            if hits:
                print(f"  남음 {os.path.basename(path)[:40]} [{t}] {len(hits)}곳: {hits[0][0]}쪽")
