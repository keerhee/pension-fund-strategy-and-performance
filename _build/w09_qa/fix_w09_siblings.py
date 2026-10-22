# -*- coding: utf-8 -*-
"""W09 강의본 보강(60 → 77장, fix_qa_w09.py) 뒤 같은 주차 덱의 연결을 맞춘다(2026-10-22).
  케이스 ① · ② — '강의 덱 NNp' 쪽 참조를 77장 판 쪽번호로 (원래도 옛 56장 판 번호였다)
  실습데이터 — "케이스의 −8.6%는 실제 공시 수치" 문구를 케이스 덱(가상 기관)과 맞추고, 데이터 위치를 W09_케이스데이터/로
실행: .venv/bin/python _build/w09_qa/fix_w09_siblings.py   (재실행 가능 — _구판/W09_QA보강_구판_2026-10-22/ 에서 원본 복원)
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lecfix"))
from lecfix import *

R = os.path.abspath(os.path.join(HERE, "..", ".."))
W = f"{R}/W09_위험관리와성과평가"
OLD = f"{R}/_구판/W09_QA보강_구판_2026-10-22"; os.makedirs(OLD, exist_ok=True)


def load(name):
    for ext in (".pptx", ".pdf"):
        src, dst = f"{W}/{name}{ext}", f"{OLD}/{name}{ext}"
        if os.path.exists(dst): shutil.copy2(dst, src)
        elif os.path.exists(src): shutil.copy2(src, dst)
    return Presentation(f"{W}/{name}.pptx")


def save(prs, name):
    prs.save(f"{W}/{name}.pptx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", W, f"{W}/{name}.pptx"],
                   check=True, capture_output=True)
    print("저장", name)


def rep(prs, pairs):
    for a, b in pairs:
        n = replace_all(prs, a, b)
        assert n == 1, (n, a)


COMMON = [("강의 덱 49p “무기 매핑”을 펴 놓고 시작하라", "강의 덱 61p “무기 매핑”을 펴 놓고 시작하라")]

name = "W09_케이스1_국부펀드2022성과평가_IC"; prs = load(name)
rep(prs, COMMON + [
    ("강의 11–13p (Coherent·스트레스) + 본 덱 10p", "강의 11–15p (Coherent·스트레스) + 본 덱 10p"),
    ("강의 20–21p (6지표) + 본 덱 7p (3렌즈)", "강의 22–26p (6지표) + 본 덱 7p (3렌즈)"),
    ("강의 27–28p (Brinson) + 본 덱 9p", "강의 36–38p (Brinson) + 본 덱 9p"),
    ("강의 30–31p (팩터 렌즈) + 본 덱 9p", "강의 39–42p (팩터 렌즈) + 본 덱 9p"),
    ("강의 36p (LTCM) + 본 덱 10p (UK LDI)", "강의 47p (LTCM) + 본 덱 10p (UK LDI)")])
save(prs, name)

name = "W09_케이스2_대체투자라이프사이클측정체계_IC"; prs = load(name)
rep(prs, COMMON + [
    ("본 덱 6p (대상별 자)", "강의 27p (TWR·MWR) + 본 덱 6p"),
    ("본 덱 7–8p (PME·KS-PME)", "강의 28p + 본 덱 7–8p (PME·KS-PME)"),
    ("강의 20p (6지표) + 본 덱 11p", "강의 25p (6지표) + 본 덱 11p"),
    ("강의 14p (MDD·Calmar) + 본 덱 11p", "강의 19p (MDD·Calmar) + 본 덱 11p"),
    ("강의 32–33p (SPIVA·Core-Satellite)", "강의 43–44p (SPIVA·Core-Satellite)")])
save(prs, name)

name = "W09_실습데이터_위험관리와성과평가"; prs = load(name)
rep(prs, [
    ("각 기금 연차보고서 (케이스 −8.6%)", "W09_케이스데이터/ (케이스 −8.6%)"),
    ("가상 데이터는 쓰지 않는다", "실습 데이터는 새로 지어내지 않는다"),
    ("케이스의 −8.6%는 실제 공시 수치다. 기간·잣대·책임 논의가 실제 숫자 위에서 이뤄져야 한다",
     "케이스 국부펀드(−8.6%)만 가상 기관이다 — 계산 데이터는 W09_케이스데이터/")])
s5 = next(sl for sl in prs.slides if find(sl, "국부펀드 2022 실적"))   # 표가 아니라 글상자 격자다
y0 = px(find(s5, "국부펀드 2022 실적"))[1]
cell = next(sh for sh in s5.shapes if sh.has_text_frame and sh.text_frame.text.strip() == "PDF" and abs(px(sh)[1] - y0) < 5)
set_text(cell, "CSV")
rep(prs, [("케이스2 자료 (라이프사이클 측정)", "케이스2 덱 + W09_케이스데이터/"), ("강의 자료", "PDF · CSV")])
save(prs, name)
