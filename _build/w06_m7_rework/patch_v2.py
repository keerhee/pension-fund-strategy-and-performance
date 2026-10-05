# -*- coding: utf-8 -*-
"""patch_textmath.py 다음에 실행(2026-10-05 2차 피드백 3건).
 1) '현물 연장'이 어색하다 → '30년 국고채 교체'(안 B) · '국고채 교체'(용어)
 2) Redington 전체 식 — 39장에 잉여금 전개식 전체 + 세 조건을 금액 꼴(A = L · D_A A = D_L L · C_A A > C_L L)로,
    40장 위쪽도 1차 항만 떼지 않고 전개식 전체를 보인다
 3) 안 A '헤지 3%'의 뜻 — 지금 보유분 2.1% + 이미 의결된 2027 목표 비중(국내채권 21.8%) 이행분.
    LDI 조치를 아무것도 하지 않아도 2027년이면 3%가 된다는 출발점임을 9·36·72·74장에 밝힌다"""
import copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lecfix"))
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
import lecfix
from rework_m7_tools import render, size_px, add_pic, remove, set_px

F = os.path.join(HERE, "..", "..", "W06_LDI와GBI", "W06_M7_LDI_부채연계투자_강의본.pptx")
P = Presentation(F)
def S(n): return P.slides[n - 1]
def sh(slide, sid): return next(x for x in slide.shapes if x.shape_id == sid)
def T(slide, sid, text): lecfix.set_text(sh(slide, sid), text)
def rep(a, b, n=1):
    k = lecfix.replace_all(P, a, b); assert k >= n, (a, k)

# ---------------------------------------------------------------- 1) 용어
rep("현물 연장 vs IRS 오버레이", "국고채 교체 vs IRS 오버레이")
rep("30년 국고채 매입(증거금 없음) / 고정 수취 스왑(증거금)", "보유 채권을 30년 국고채로 바꿈(증거금 없음) / 고정금리 수취 스왑을 얹음(증거금)")
rep("부채 벤치마크 도입과 현물 듀레이션 연장의 조건부 승인입니다", "부채 벤치마크 도입과 30년 국고채 교체의 조건부 승인입니다")
rep("현물이라 증거금이 없다", "채권을 직접 사므로 증거금이 없다")
rep("② 현물 ≤ 장기물 30%×5년(131조)", "② 국고채 교체 ≤ 장기물 30%×5년(131조)")
rep("A=L·D 일치·C_A≥C_L", "A = L · 금액 듀레이션 일치 · 금액 볼록성 우위")

# ---------------------------------------------------------------- 3) 안 A 3%
s = S(9)
T(s, 5, "헤지 비율 = 자산 DV01 ÷ 부채 DV01 · 지금 2.1%, 이미 의결된 2027 목표 비중만 채워도 3% — 이것이 출발점")
T(s, 8, "안 A · 현행 유지 · 헤지 3%")
T(s, 9, "LDI 조치를 하지 않는다")
T(s, 10, "새로 사지도, 계약하지도 않는다\n2027 목표 비중만 채운다\n부채 벤치마크 없음\n→ 헤지 2.1 → 3% · 갭 −34년")
T(s, 21, "안 B · 30년 국고채 교체 · 헤지 5%")
T(s, 22, "보유 채권을 바꿔 든다")
T(s, 16, "안 C · IRS 오버레이 · 헤지 30%")
T(S(36), 15, "국민연금 — 갭 약 −34년 · 헤지 2.1%(현 보유) → 3%(2027 목표 비중 이행 시)")
rep("안 A 새로 사지 않음(3%)", "안 A LDI 조치 없음(현 2.1% → 2027 목표 비중 이행 시 3%)")
s = S(74)
T(s, 10, "LDI 조치가 없어 헤지는 2027 목표 비중을 채워도 3%, 갭 −34년을 그대로 진다\n부채 벤치마크가 없어 갭을 재지도 못한다")

# ---------------------------------------------------------------- 2) Redington 전체 식
FULL = r"\Delta S=\Delta A-\Delta L\ \approx\ -\left(D_A\,A-D_L\,L\right)\Delta y\ +\ \frac{1}{2}\left(C_A\,A-C_L\,L\right)(\Delta y)^2"
E_FULL = render(FULL, "red_full.png", fontsize=30)
WHITE, INK, LIME = "#FFFFFF", "#071A1D", "#B7F34A"
E_C1 = render(r"A=L", "red_c1.png", fontsize=30, bg=WHITE)
E_C2 = render(r"D_A\,A=D_L\,L", "red_c2.png", fontsize=30, bg=WHITE)
E_C3 = render(r"C_A\,A>C_L\,L", "red_c3.png", fontsize=30, color=LIME, bg=INK)

s = S(39)
T(s, 5, "Redington(1952) — 잉여금 변화의 전개식에서 1차 항을 0으로, 2차 항을 양수로 만든다 · 증명은 부록 B-3")
box, old = sh(s, 7), sh(s, 22)
set_px(box, x=69, y=218, w=1142, h=118)                       # 전폭 띠: 전개식 전체
w, h = size_px(E_FULL, maxw=1100, maxh=100)
add_pic(s, E_FULL, 640 - w / 2, 218 + (118 - h) / 2, w, h, before=old._element); remove(old)
for sid, path in ((11, E_C1), (15, E_C2), (19, E_C3)):           # 카드 속 조건도 금액 꼴 수식으로
    t = sh(s, sid); x, y, cw, ch = lecfix.px(t)
    w, h = size_px(path, maxh=46)
    add_pic(s, path, x, y + (ch - h) / 2, w, h); remove(t)
T(s, 12, "막는 것: 출발선 부족")
T(s, 16, "막는 것: 1차 항(방향)")
T(s, 20, "막는 것: 2차 항(휘어짐)")
src = sh(s, 21)                                               # 바닥 줄을 복제해 ※ 각주(앰버 13pt)로
el = copy.deepcopy(src._element); src._element.addprevious(el)
note = [x for x in s.shapes if x._element is el][0]; note._element.nvSpPr.cNvPr.id = 900
lecfix.set_text(note, "※ 세 조건은 모두 금액(×A, ×L) 꼴이다. A = L일 때만 A·L이 약분돼 ‘자산 D = 부채 D · 자산 C > 부채 C’로 줄어든다")
set_px(note, y=540, h=30)
for r in note.text_frame.paragraphs[0].runs:
    r.font.size = Pt(13); r.font.bold = False; r.font.color.rgb = RGBColor(0xF3, 0xA3, 0x3C)

s = S(40)
T(s, 5, "조건 2의 근거 — 전개식 전체에서 첫 항(1차, 방향)만 본다. 둘째 항(2차, 휘어짐)은 조건 3의 몫")
box, old = sh(s, 7), sh(s, 9)
set_px(box, x=69, y=224, w=1142, h=131)
T(s, 8, "잉여금 변화 — 이 장은 첫 항")
set_px(sh(s, 8), x=90, w=600)
w, h = size_px(E_FULL, maxw=1100, maxh=80)
add_pic(s, E_FULL, 640 - w / 2, 262 + (88 - h) / 2, w, h, before=old._element); remove(old)
t = sh(s, 12); x, y, cw, ch = lecfix.px(t)
w, h = size_px(E_C2, maxh=46); add_pic(s, E_C2, x, y + (ch - h) / 2, w, h); remove(t)
T(s, 17, "자산 금액 듀레이션 300 · 부채 금액 듀레이션 1,600")


# ---------------------------------------------------------------- 4) 적립비율 — 공시값과 우리 계산을 가른다(2026-10-05)
# 국민연금·공무원연금은 적립비율을 공시하지 않는다(국민연금 공시 지표는 적립배율).
# NPS 95%/69%는 w6m7_compute.py의 교육용 계산. 공무원연금 '약 25%'는 출처가 없어 폐기 →
# 기금 16.3조(2024 말, e-나라지표) vs 공무원 연금충당부채 900조 이상(2021 결산 904.6조 · 2024 공무원+군인 1,312.9조) → 2% 미만.
rep("95% vs 69% · 조건 ①", "95% vs 69%(우리 계산) · 조건 ①")
T(S(20), 10, "순부채 1,542조 · FR 95%(우리 계산)")
T(S(20), 13, "순부채 2,122조 · FR 69%(우리 계산)")
rep("보전금 증가세 둔화 — 그러나 적립비율은 여전히 약 25%", "보전금 증가세 둔화 — 그러나 기금은 연금충당부채의 2%도 안 된다")
s = S(23)
T(s, 5, "적립비율은 회계가 아니라 선택의 산물이다 — 공시값은 CalPERS뿐, 한국 두 연금의 비율은 우리 계산")
T(s, 9, "적립비율 2% 미만")
T(s, 10, "기금 16조 · 부채 900조+\n공시: 적립비율 없음")
set_px(sh(s, 10), w=318)
T(s, 14, "약 75% (FY2024)")
T(s, 15, "할인율 7.5% → 6.8%\n공시: 적립비율")
T(s, 20, "자체 5.5% / 국채 눈금\n공시: 적립배율뿐")
rep("공무원연금 적립비율 약 25%, NPS 순부채 2,122조(국채 눈금) · 소진 2071.",
    "공무원연금 기금은 연금충당부채의 2% 미만, NPS 순부채 2,122조(국채 눈금, 우리 계산) · 소진 2071.")
rep("① 갭 실재 — FR 95%(자체 5.5%) vs 69%(국채)", "① 갭 실재 — FR 95%(자체 5.5%) vs 69%(국채) · 우리 계산")

P.save(F); print("patched v2 + 적립비율")
