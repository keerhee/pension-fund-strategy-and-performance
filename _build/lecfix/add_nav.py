# -*- coding: utf-8 -*-
"""본문 ↔ 부록 이동 버튼 — 본문에서 부록으로 가는 버튼과, 부록에서 그 본문으로 돌아오는 버튼을 단다.

· 버튼은 꼬리 줄(워드마크와 쪽번호 사이)에 놓는 알약 도형이고, 도형 클릭 = 그 장으로 이동.
· 본문의 '부록 B-3' 같은 글자도 같은 곳으로 가는 링크로 만든다.
· LibreOffice PDF 변환이 슬라이드 이동을 PDF 내부 링크(GoTo)로 옮기므로 PDF에서도 눌린다.
· 다시 돌려도 같은 결과 — 전에 단 NAV_ 도형은 지우고 새로 단다. fix_* 스크립트를 다시 돌린 뒤에는 이것을 마지막에 돌린다.
"""
import copy, os, re, subprocess, sys, zipfile
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 덱 → 참조 목록 [(본문 쪽, 부록 쪽들, 본문에서 링크할 글자 또는 None, 버튼 이름)]  — 쪽은 1부터
#   부록 쪽들의 첫 쪽으로 가고, 부록 쪽마다 그 본문으로 돌아오는 버튼이 붙는다.
DECKS = {
    "W15_TPA/W15_TPA_제1부_사일로해체와설계_강의본": dict(refs=[
        (21, [71, 72], "부록 B-3", "부록 B-3"),
        (23, [73], "부록 B-4", "부록 B-4"),
        (23, [74], "B-5", "부록 B-5"),
        (47, [70], "부록 B-2", "부록 B-2"),
        # 본문에 '부록 B-1'·'용어집' 표기는 없다 — 식 번호를 쓰는 장과 개념을 모아 보는 장에서 건다
        (12, [69], None, "부록 B-1"),
        (14, [69], "식 ①", "부록 B-1"),
        (47, [69], "식 ④", "부록 B-1"),
        (48, [69], "식 ⑦", "부록 B-1"),
        (2, [66], None, "용어집"),
        (63, [66], None, "용어집"),
    ]),
    # 용어집 — 첫머리 지도(2장)와 '개념 → IC 쟁점 매핑' 장에서 건다 (본문에 용어집 표기는 없어 버튼만)
    "W01_시장개요와자산소유자/W01_시장개요와자산소유자_강의본": dict(refs=[(2, [51], None, "용어집")]),
    "W10_주식퀀트모델/W10_주식퀀트모델_강의본": dict(refs=[(2, [49], None, "용어집"), (47, [49], None, "용어집")]),
    "W11_채권투자/W11_채권투자_제1부_채권수학과곡선전략": dict(refs=[(2, [52], None, "용어집"), (50, [52], None, "용어집")]),
    "W12_팩터투자/W12_팩터투자_강의본": dict(refs=[(2, [49], None, "용어집"), (47, [49], None, "용어집")]),
    "W13_글로벌매크로와CTA/W13_글로벌매크로와CTA_강의본": dict(refs=[(2, [50], None, "용어집"), (48, [50], None, "용어집")]),
    "W14_대체투자와비유동성/W14_대체투자와비유동성_강의본": dict(refs=[(2, [55], None, "용어집"), (53, [55], None, "용어집")]),
    "W15_TPA/W15_TPA_제2부_MeasuringWhatMatters_성과평가": dict(refs=[(2, [28], None, "용어집")]),
    # 앞쪽 '먼저 읽는 용어' 장 — 교시 체크포인트 · IC 쟁점 매핑 · 부록 A 한 장 요약에서 건다
    "W04_MVO와블랙리터맨/W04_M4_MVO와공분산추정_강의본": dict(refs=[(x, [2, 3], None, "먼저 읽는 용어") for x in (12, 23, 33, 50)]),
    "W04_MVO와블랙리터맨/W04_M5_블랙리터맨_균형과뷰_강의본": dict(refs=[(x, [2, 3], None, "먼저 읽는 용어") for x in (15, 24, 34, 51)]),
    "W06_동적포트폴리오와장기투자/W06_동적포트폴리오와장기투자_강의본": dict(refs=[(x, [2, 3], None, "먼저 읽는 용어") for x in (16, 26, 39, 54)]),
    "W06_동적포트폴리오와장기투자/W06_특별세션_SS2_재균형프리미엄_강의본": dict(refs=[(x, [2], None, "먼저 읽는 용어") for x in (3, 22)]),
    "W07_LDI와GBI/W07_M8_LDI_부채연계투자_강의본": dict(refs=[(x, [2, 3], None, "먼저 읽는 용어") for x in (18, 31, 44, 53, 56)]),
    # 새로 붙인 부록 용어집(add_glossary.py) — 첫머리 · 교시 체크포인트 · IC 쟁점 매핑 · 한 장 요약에서 건다
    "W02_자산배분과CAPM/W02_자산배분과CAPM_강의본": dict(refs=[(x, [77], None, "용어집") for x in (2, 12, 60, 75)]),
    "W03_연기금모델과CMA/W03_연기금모델과CMA_강의본": dict(refs=[(x, [63], None, "용어집") for x in (2, 11, 30, 43, 61)]),
    "W09_위험관리와성과평가/W09_위험관리와성과평가_강의본": dict(refs=[(x, [60], None, "용어집") for x in (2, 16, 27, 38, 52, 54)]),
    "W07_LDI와GBI/W07_M9_GBI_목표기반투자_강의본": dict(refs=[
        (16, [67], "부록 B-1", "부록 B-1"),
        (18, [68], "부록 B-2", "부록 B-2"),
        (18, [69], "B-3", "부록 B-3"),
        (18, [70], "B-4", "부록 B-4"),
        (19, [71, 72], "부록 B-5", "부록 B-5"),
        (34, [73], "부록 B-6", "부록 B-6"),
        (35, [74], "부록 B-7", "부록 B-7"),
    ] + [(x, [75], None, "용어집") for x in (2, 20, 40, 52, 61, 64)]),     # 부록 C 용어집(add_glossary.py)
    "W05_리스크패리티와HRP/W05_리스크패리티와HRP_강의본": dict(
        # NCO 심화 부록은 57쪽(간지)부터다 — 본문의 옛 쪽 표기 54p를 바로잡는다
        fixes=[("(54p~)", "(57p~)")],
        refs=[
            (8, list(range(57, 69)), "부록", "부록"),
            (26, list(range(57, 69)), None, "부록"),      # 남색 띠 위라 글자 링크는 안 보인다 — 버튼만
        ] + [(x, [2, 3], None, "먼저 읽는 용어") for x in (16, 27, 39, 54)]),
    "W11_채권투자/W11_보강1_채권트레이딩4전략과투자게임": dict(refs=[
        (25, [37, 38, 39, 40, 41], "(37–41p)", "부록"),
        (31, [38, 39, 40], "(38–40p)", "부록"),
    ]),
    "보충교재/07_블랙리터맨_W04/BL_Expected_Return_Update_bj": dict(
        geom=dict(y=7.035, h=0.28, right=12.42, fs=11, font="맑은 고딕", ink="1B2A41"),
        pdf_font=("맑은 고딕", "Pretendard"),                 # 이 덱의 PDF는 Pretendard로 바꿔 찍어 왔다
        refs=[(10, [21, 22, 23, 24, 25], "부록 A", "부록 A")]),
    "보충교재/09_HRP와NCO_W05/HRP_NCO_JJ_Brief_II": dict(
        geom=dict(y=0.10, h=0.30, right=8.32, fs=11, font="맑은 고딕", ink="1E4E8C"),   # 맨 위 띠, 쪽번호(8.40~) 앞
        pdf_font=("맑은 고딕", "Pretendard"),
        refs=[(9, list(range(53, 63)), "부록 A", "부록 A")]),
}

# 기본 자리: 강의본 꼬리 줄 — 워드마크(0.62~)와 쪽번호(11.71~) 사이
GEOM = dict(y=7.10, h=0.30, right=11.55, fs=12, font="Noto Sans CJK KR", ink="1B2C5E")
TINT, GAP = RGBColor(0xE8, 0xEE, 0xF8), 0.12
G = dict(GEOM)                                         # 지금 덱의 자리 (build가 바꾼다)


def width(text):
    """버튼 폭 — 한글 1자 ≈ 글자크기, 숫자·기호 ≈ 0.55배, 좌우 여백 0.30in."""
    em = sum(1.0 if ord(c) > 0x2E80 else 0.58 for c in text)
    return round(em * G["fs"] / 72 + 0.34, 2)


def pill(slide, x, w, text, target, tag):
    NAVY = RGBColor.from_string(G["ink"])
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(G["y"]), Inches(w), Inches(G["h"]))
    sh.name = "NAV_" + tag
    sh.adjustments[0] = 0.5
    # PDF에서는 링크 글자가 테마의 링크 색으로 칠해진다 — 그래서 바탕은 밝게, 링크 색은 남색으로 맞춘다(theme_link_color)
    sh.fill.solid(); sh.fill.fore_color.rgb = TINT
    sh.line.color.rgb = NAVY; sh.line.width = Pt(1)
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(0.06); tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(G["fs"]); r.font.bold = True; r.font.name = G["font"]; r.font.color.rgb = NAVY
    sh.click_action.target_slide = target                         # PowerPoint·Keynote: 도형 어디를 눌러도
    rPr = r._r.get_or_add_rPr()                                   # PDF: LibreOffice는 도형 클릭을 안 옮기고 글자 링크만 옮긴다
    rId = slide.part.relate_to(target.part, RT.SLIDE)
    rPr.append(rPr.makeelement(qn("a:hlinkClick"), {qn("r:id"): rId, "action": "ppaction://hlinksldjump"}))
    rPr.set("u", "none")
    return sh


def theme_link_color(prs, rgb="1B2C5E"):
    """테마의 링크 색(hlink · folHlink)을 덱 남색으로 — 본문 링크도 파랑 대신 남색 밑줄이 된다."""
    from lxml import etree
    for rel in prs.slide_master.part.rels.values():
        if rel.reltype == RT.THEME:
            part = rel.target_part
            root = etree.fromstring(part.blob)
            for tag in ("a:hlink", "a:folHlink"):
                el = root.find(".//" + qn(tag))
                for c in list(el): el.remove(c)
                etree.SubElement(el, qn("a:srgbClr"), val=rgb)
            part._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def pills(slide, items):
    """items = [(글자, 목표 슬라이드)] — 오른쪽 끝(쪽번호 앞)에서부터 왼쪽으로 늘어놓는다."""
    x = G["right"]
    for text, target in reversed(items):
        w = width(text)
        x -= w
        pill(slide, x, w, text, target, re.sub(r"\W", "", text))
        x -= GAP


def link_text(slide, needle, target):
    """본문 글자 needle을 target 장으로 가는 링크로 만든다 (런을 셋으로 나눠 가운데에만 링크)."""
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if needle not in r.text:
                    continue
                pre, post = r.text.split(needle, 1)
                runs = []
                for t in (pre, needle, post):
                    if t:
                        nr = copy.deepcopy(r._r); nr.find(qn("a:t")).text = t; runs.append((t, nr))
                for t, nr in runs:
                    r._r.addprevious(nr)
                    if t == needle:
                        rPr = nr.find(qn("a:rPr"))
                        if rPr is None:
                            rPr = nr.makeelement(qn("a:rPr"), {}); nr.insert(0, rPr)
                        rId = slide.part.relate_to(target.part, RT.SLIDE)
                        h = rPr.makeelement(qn("a:hlinkClick"), {qn("r:id"): rId, "action": "ppaction://hlinksldjump"})
                        # hlinkClick은 rPr 안에서 채우기·글꼴 뒤에 온다
                        rPr.append(h)
                        rPr.set("u", "sng")
                p._p.remove(r._r)
                return True
    return False


def replace_text(prs, a, b):
    n = 0
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                for r in (r for p in sh.text_frame.paragraphs for r in p.runs):
                    if a in r.text:
                        r.text = r.text.replace(a, b); n += 1
    return n


def grep_text(prs, t):
    return any(sh.has_text_frame and t in sh.text_frame.text for s in prs.slides for sh in s.shapes)


def to_pdf(pptx, font_map=None):
    """PDF 변환. font_map=(원래 글꼴, PDF용 글꼴)이면 글꼴만 바꾼 임시 사본을 변환한다 (원본 pptx는 그대로)."""
    import shutil, tempfile
    names = zipfile.ZipFile(pptx).namelist()
    assert len(names) == len(set(names)), "zip 안에 중복 파일"
    src, tmp = pptx, None
    if font_map:
        tmp = tempfile.mkdtemp()
        src = os.path.join(tmp, os.path.basename(pptx))
        a, b = (f'typeface="{f}"'.encode() for f in font_map)
        with zipfile.ZipFile(pptx) as zi, zipfile.ZipFile(src, "w", zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                data = zi.read(it)
                if it.filename.endswith(".xml"):
                    data = data.replace(a, b)
                zo.writestr(it, data)
    r = subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(src), src],
                       check=True, capture_output=True, text=True)
    assert "Error" not in (r.stdout + r.stderr), r.stdout + r.stderr
    if tmp:
        shutil.move(src[:-5] + ".pdf", pptx[:-5] + ".pdf"); shutil.rmtree(tmp)


def build(deck, cfg):
    G.clear(); G.update(GEOM, **cfg.get("geom", {}))
    refs = cfg["refs"]
    path = os.path.join(ROOT, deck + ".pptx")
    prs = Presentation(path)
    S = prs.slides
    for s in S:                                                   # 전에 단 버튼 지우기
        for sh in [x for x in s.shapes if x.name.startswith("NAV_")]:
            sh._element.getparent().remove(sh._element)

    for s in S:                                                   # 전에 건 슬라이드 이동 글자 링크 걷기
        for h in list(s._element.iter(qn("a:hlinkClick"))):
            if h.get("action") == "ppaction://hlinksldjump":
                rPr = h.getparent(); rPr.remove(h)
                if rPr.get("u") == "sng": del rPr.attrib["u"]
    for a, b in cfg.get("fixes", []):
        n = replace_text(prs, a, b)
        assert n or grep_text(prs, b), a
    theme_link_color(prs, G["ink"])
    fwd, back = {}, {}
    for src, dsts, label, name in refs:
        fwd.setdefault(src, []).append((f"▶ {name} · {dsts[0]}쪽", S[dsts[0] - 1]))
        if label:
            assert link_text(S[src - 1], label, S[dsts[0] - 1]), (src, label)
        for d in dsts:
            back.setdefault(d, [])
            if src not in [b for b, _ in back[d]]:
                back[d].append((src, S[src - 1]))

    for src, items in fwd.items():                                # 부록 쪽 순서대로 늘어놓는다
        pills(S[src - 1], sorted(items, key=lambda it: int(re.search(r"(\d+)쪽", it[0]).group(1))))
    for d, srcs in back.items():
        short = len(srcs) > 2                                     # 돌아올 곳이 많으면 '◀ 12쪽'으로 줄인다
        pills(S[d - 1], [(f"◀ {src}쪽" if short else f"◀ 본문 {src}쪽으로", t) for src, t in sorted(srcs)])

    prs.save(path); to_pdf(path, cfg.get("pdf_font"))
    print(deck, "→", {k: [i[0] for i in v] for k, v in fwd.items()}, "| 돌아오기", {k: [s for s, _ in v] for k, v in back.items()})


if __name__ == "__main__":
    for deck, cfg in DECKS.items():
        if len(sys.argv) < 2 or sys.argv[1] in deck:
            build(deck, cfg)
