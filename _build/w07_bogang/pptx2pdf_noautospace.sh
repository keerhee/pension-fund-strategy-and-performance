#!/bin/zsh
# pptx2pdf_noautospace.py 의 대체 — LibreOffice 내장 python(UNO)이 이 맥에서 Gatekeeper에 막혀(exit 137) 못 돌 때.
# pptx → odp → 모든 문단 스타일에 style:text-autospace="none" → pdf. 결과는 UNO 판과 같다(Kritzman 덱으로 화소 대조).
#   pptx2pdf_noautospace.sh <in.pptx> <out.pdf>
set -e
IN=${1:A}; OUT=${2:A}; T=$(mktemp -d); B=${IN:t:r}
soffice --headless --convert-to odp --outdir "$T" "$IN" >/dev/null 2>&1
mkdir "$T/x"; (cd "$T/x" && unzip -q "../$B.odp")
/usr/bin/python3 - "$T/x" <<'PY'
import re, sys, os
d = sys.argv[1]
for f in ("content.xml", "styles.xml"):
    p = os.path.join(d, f); s = open(p, encoding="utf-8").read()
    s = re.sub(r'\sstyle:text-autospace="[^"]*"', "", s)
    s = re.sub(r"<style:paragraph-properties(?=[\s/>])", '<style:paragraph-properties style:text-autospace="none"', s)
    # 문단 속성이 없는 문단 스타일에도 넣는다
    s = re.sub(r'(<style:style [^>]*style:family="paragraph"[^>]*>)(?!<style:paragraph-properties)',
               r'\1<style:paragraph-properties style:text-autospace="none"/>', s)
    open(p, "w", encoding="utf-8").write(s)
PY
(cd "$T/x" && rm -f "../$B.odp" && zip -q -X -0 "../$B.odp" mimetype && zip -q -X -r "../$B.odp" . -x mimetype)
soffice --headless --convert-to pdf --outdir "$T" "$T/$B.odp" >/dev/null 2>&1
cp "$T/$B.pdf" "$OUT"; rm -rf "$T"; echo "PDF: $OUT"
