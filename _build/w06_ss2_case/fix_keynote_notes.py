#!/usr/bin/env python3
"""LibreOffice round-trip 후처리 — Keynote가 pptx를 못 여는 문제를 고친다.

`soffice --convert-to pptx` 정규화를 거치면 LibreOffice가 슬라이드마다 빈
notesSlide를 만들면서 `<p:clrMapOvr>`를 빼먹는다. PowerPoint·LibreOffice는
그냥 열지만 Keynote의 OOXML 파서는 이 요소를 필수로 보고, 파일을 열지 못한 채
모달 오류창에서 멈춘다(zip·rels·Content_Types는 전부 정상이라 4단계 무결성
검증은 통과한다 — 그래서 놓치기 쉽다).

고치는 방법은 각 notesSlide의 `</p:cSld>` 바로 뒤에 아래 한 줄을 넣는 것뿐이다.
슬라이드 내용·서식·노트 텍스트는 전혀 바뀌지 않는다.

    <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>

사용법:
    python3 fix_keynote_notes.py _norm/out.pptx          # 제자리 수정
    python3 fix_keynote_notes.py <디렉터리>               # 하위 pptx 일괄
    python3 fix_keynote_notes.py --check <경로>           # 수정 없이 진단만
    python3 fix_keynote_notes.py --backup <경로>          # 원본을 *.bak.pptx로 남김

이미 정상인 파일은 건드리지 않으므로 몇 번 돌려도 안전하다.
종료 코드: 0 = 정상(또는 수정 완료), 1 = --check에서 문제 발견, 2 = 오류.
"""
import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile

NOTES_RE = re.compile(r"ppt/notesSlides/notesSlide\d+\.xml$")
CLRMAPOVR = "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"


def targets(zf):
    """clrMapOvr가 없는 notesSlide 파트 이름."""
    return [
        n for n in zf.namelist()
        if NOTES_RE.match(n) and "<p:clrMapOvr" not in zf.read(n).decode("utf-8", "ignore")
    ]


def patch(path, backup=False):
    """반환값: 패치한 notesSlide 수(0이면 손대지 않음)."""
    with zipfile.ZipFile(path) as zi:
        todo = targets(zi)
        if not todo:
            return 0
        names = zi.namelist()
        fd, tmp = tempfile.mkstemp(suffix=".pptx", dir=os.path.dirname(path) or ".")
        os.close(fd)
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
            for n in names:
                data = zi.read(n)
                if n in todo:
                    xml = data.decode()
                    if xml.count("</p:cSld>") != 1:
                        raise RuntimeError(f"{path}::{n}: </p:cSld>가 1개가 아니다")
                    data = xml.replace("</p:cSld>", "</p:cSld>" + CLRMAPOVR, 1).encode()
                zo.writestr(n, data)

    with zipfile.ZipFile(tmp) as z2:
        if len(z2.namelist()) != len(names):
            os.unlink(tmp)
            raise RuntimeError(f"{path}: 파트 수가 달라졌다")
    if backup:
        shutil.copy2(path, path[:-5] + ".bak.pptx")
    os.replace(tmp, path)
    return len(todo)


def collect(paths):
    for p in paths:
        if os.path.isdir(p):
            for dp, _, fn in os.walk(p):
                for f in sorted(fn):
                    if f.lower().endswith(".pptx") and not f.endswith(".bak.pptx"):
                        yield os.path.join(dp, f)
        else:
            yield p


def main():
    ap = argparse.ArgumentParser(description="pptx notesSlide에 clrMapOvr 보강 (Keynote 호환)")
    ap.add_argument("paths", nargs="+", help="pptx 파일 또는 디렉터리")
    ap.add_argument("--check", action="store_true", help="수정하지 않고 진단만")
    ap.add_argument("--backup", action="store_true", help="원본을 *.bak.pptx로 남김")
    args = ap.parse_args()

    bad = fixed = clean = 0
    for path in collect(args.paths):
        try:
            if args.check:
                with zipfile.ZipFile(path) as zf:
                    todo = targets(zf)
                if todo:
                    bad += 1
                    print(f"NG  {len(todo):3d}개 notesSlide 누락  {path}")
                else:
                    clean += 1
            else:
                n = patch(path, backup=args.backup)
                if n:
                    fixed += 1
                    print(f"수정 {n:3d}개 notesSlide  {path}")
                else:
                    clean += 1
        except zipfile.BadZipFile:
            print(f"오류 pptx로 열 수 없음  {path}", file=sys.stderr)
            return 2
        except Exception as e:  # 손상된 파일을 조용히 지나치지 않는다
            print(f"오류 {e}", file=sys.stderr)
            return 2

    if args.check:
        print(f"\n정상 {clean}개 / 문제 {bad}개")
        return 1 if bad else 0
    print(f"\n수정 {fixed}개 / 원래 정상 {clean}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
