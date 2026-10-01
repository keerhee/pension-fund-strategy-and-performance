# -*- coding: utf-8 -*-
"""W07 M8 LDI 강의본 — 2022 영국 위기 교훈(39쪽) 뒤에 2023 실리콘밸리은행(SVB) 비교 장표 1장 (58 → 59장, 2026-10-01).

SVB 수치(2022년 말 · 2023년 3월): 총자산 약 2,090억 달러 · 예금 약 1,755억 달러(비보험 약 94%) ·
만기보유(HTM) 증권 약 910억 달러, 미실현손실 150억 달러+ (자기자본 약 160억 달러와 맞먹음) ·
3/8 매도가능 증권 210억 달러 매각 · 손실 18억 달러 확정 · 22.5억 달러 증자 발표 · 3/9 하루 예금 420억 달러 인출 ·
3/10 폐쇄(FDIC 관재) · 3/12 예금 전액 보호(시스템 위험 예외).
실행: .venv/bin/python _build/lecfix/fix_w07_svb.py   (재실행 가능 — _구판/W07_SVB추가_구판_2026-10-01/ 에서 원본 복원)
"""
import os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lecfix import *
from slidekit import Kit, place

R = os.path.dirname(os.path.dirname(HERE))
W = f"{R}/W07_LDI와GBI"
OLD = f"{R}/_구판/W07_SVB추가_구판_2026-10-01"; os.makedirs(OLD, exist_ok=True)
name = "W07_M8_LDI_부채연계투자_강의본"
for ext in (".pptx", ".pdf"):
    src, dst = f"{W}/{name}{ext}", f"{OLD}/{name}{ext}"
    if os.path.exists(dst): shutil.copy2(dst, src)
    elif os.path.exists(src): shutil.copy2(src, dst)

prs = Presentation(f"{W}/{name}.pptx")
assert len(prs.slides) == 58, len(prs.slides)
S = lambda k: prs.slides[k - 1]
assert find(S(39), "2022 영국 위기의 다섯 가지 교훈")
kit = Kit(prs, panel_idx=[37], table_idx=38, bottom_idx=38)

s = kit.new(S(39), "3교시 · 비교 사례", "같은 금리 급등, 반대 방향의 갭 — 2023 실리콘밸리은행",
            "영국 연기금은 레버리지로 헤지했고 SVB는 헤지하지 않았다 — 둘 다 ‘금리가 오른 날의 현금’에서 무너졌다")
kit.table(s, 60, 196, 1161, [
    ["", "2022 영국 LDI", "2023 실리콘밸리은행(SVB)"],
    ["듀레이션 갭", "부채에 맞춰 길게 — 레버리지 IRS · 레포로 헤지", "자산(국채 · MBS)은 길고, 부채(예금)는 언제든 인출"],
    ["금리 상승의 상처", "헤지 손실 → 증거금 현금 부족", "만기보유 증권 910억 달러 · 미실현손실 150억+ ≈ 자기자본"],
    ["방아쇠", "9/23 미니예산 → 30년 길트 급등", "3/8 증권 210억 달러 매각 · 손실 18억 확정 · 증자 발표"],
    ["유동성 붕괴", "1,000개 연기금 동시 매도 — Doom Loop", "3/9 하루 예금 420억 달러 인출 — 비보험 예금 약 94%"],
    ["결말", "BOE £65B 한도 개입(13일) · 연기금은 생존", "3/10 폐쇄 · 3/12 예금 전액 보호 — 은행은 소멸"],
    ["*교훈", "*담보 버퍼 의무화(250bp)", "*장부(만기보유)가 아니라 시가로 갭을 본다"]],
    [1.6, 3.6, 4.6], rowh=44, pt=15, align="lll")
kit.banner(s, 520, "듀레이션 갭은 어느 쪽으로 열려도 위험하다 — 금리가 오른 날 현금이 있느냐가 생사를 가른다")
kit.bottom(s, "연기금은 부채(급여)가 인출되지 않아 SVB식 뱅크런은 없다 — 그러나 헤지의 증거금이 같은 ‘현금 시험’을 만든다 : 오후 조건 ③(버퍼)",
           pt=15, y=592)

place(prs, [(s, 39)])
assert len(prs.slides) == 59
renumber(prs)
idx = {id(x): i for i, x in enumerate(prs.slides, 1)}
for x in list(prs.slides)[1:3]:
    for sh in x.shapes:
        if sh.has_text_frame and re.fullmatch(r"◀ \d+쪽", sh.text_frame.text.strip()):
            tgt = sh.click_action.target_slide
            set_text(sh, f"◀ {idx[id(tgt)]}쪽")

prs.save(f"{W}/{name}.pptx")
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", W, f"{W}/{name}.pptx"], check=True, capture_output=True)
print("저장:", name, len(prs.slides), "장 · 새 장표", idx[id(s)])
