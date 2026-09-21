#!/usr/bin/env python3
# ============================================================================
# qa_callout_overlap.py  *v1.9.3
# ----------------------------------------------------------------------------
# 라벨 얹힌 "짧은" 콜아웃(tint 박스 + 상단 라벨 + 본문)에서 본문이 위로 넘쳐
# 라벨과 겹치는 사고(미션 박스형)를 빌드 후 결정적으로 색출한다.
#
# 원리(줄 수 추정에 의존하지 않음 = 안정적):
#   라벨 아래 본문이 valign != "top" 이면, 내용이 박스보다 길 때 위로도 넘쳐
#   라벨을 침범한다. 단, 큰 2단 분석 패널(h가 큼)은 라벨↔본문 간격이 넉넉해
#   middle이어도 안 겹치고 그게 정상이다. 그래서 짧은 콜아웃 박스
#   (BOX_MIN <= h < BOX_MAX) 로 한정해, 그 안의 본문이 top이 아닌 것만 잡는다.
#   해소법은 한 가지 - 본문을 valign="top"으로 바꾸거나 panel()로 다시 만든다
#   (panel은 h<3.0에서 자동 top). 짧은 콜아웃은 top으로 둬도 모양이 깔끔하다.
#
#   * 아래쪽 잘림(박스 높이 부족, 9p형)은 줄 수에 좌우돼 자동탐지가 불안정하므로
#     이 스크립트가 아니라 1.2.1 "콜아웃 최소 높이 공식"으로 설계 단계에서 막는다.
#
# 사용:  python qa_callout_overlap.py <deck.pptx> [deck2.pptx ...]
# 종료코드: 후보가 있으면 1, 없으면 0 (검수 게이트용).
# ============================================================================
import sys
from pptx import Presentation
from pptx.util import Emu

TINTS = {"EAF1FB", "E6F5F0", "F4F5F9", "FCF2E0", "FDF0E0"}
BODY_MIN, BODY_MAX = 0.40, 1.20   # 짧은 본문 박스만(큰 분석 패널 본문 h>=1.2는 middle이 정상)

def inch(v):
    return Emu(v).inches if v is not None else None

def fill_of(sh):
    try:
        if sh.fill.type == 1:
            return str(sh.fill.fore_color.rgb)
    except Exception:
        pass
    return None

def scan(path):
    prs = Presentation(path)
    hits = []
    for i, sl in enumerate(prs.slides, 1):
        shapes = list(sl.shapes)
        for box in shapes:
            if fill_of(box) not in TINTS or box.height is None:
                continue
            bx, by, bw, bh = inch(box.left), inch(box.top), inch(box.width), inch(box.height)
            if bh is None or bh < 0.6 or bh >= 3.0:      # tint 박스(풀블리드·chrome 제외)
                continue
            inside = [s for s in shapes
                      if s is not box and s.has_text_frame and s.text.strip() and s.top is not None
                      and inch(s.left) >= bx - 0.1 and inch(s.left) <= bx + bw
                      and inch(s.top) >= by - 0.15 and inch(s.top) <= by + bh + 0.05]
            if len(inside) < 2:
                continue
            inside.sort(key=lambda s: inch(s.top))
            label = inside[0]
            for body in inside[1:]:
                if len(body.text) < 25 or body.height is None:
                    continue
                body_h = inch(body.height)
                # 짧은 본문 박스 + 본문 valign != top → 위로 넘쳐 라벨 침범 위험
                if not (BODY_MIN <= body_h < BODY_MAX):
                    continue
                va = str(body.text_frame.vertical_anchor or "TOP")
                if "TOP" not in va:
                    hits.append((i, label.text[:14], va.split()[0],
                                 round(body_h, 2), round(inch(body.top), 2),
                                 body.text[:34].replace("\n", " ")))
    return hits

def main(argv):
    bad = 0
    for path in argv:
        hits = scan(path)
        print(f"\n=== {path} ===")
        if not hits:
            print("  통과 - 짧은 라벨 콜아웃 본문이 모두 top 정렬")
            continue
        bad += 1
        for i, lbl, va, bh, bt, prev in hits:
            print(f"  s{i}: 라벨'{lbl}' | 본문 valign={va} (박스h={bh}, 본문y={bt}) :: {prev!r}")
        print(f"  -> {len(hits)}건. 본문을 valign=\"top\"으로(또는 panel()로) 바꾸세요.")
    return 1 if bad else 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python qa_callout_overlap.py <deck.pptx> [...]")
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
