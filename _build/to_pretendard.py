"""Copy a .pptx/.docx with Korean/Latin text fonts switched to Pretendard (code/math fonts kept)."""
import zipfile, sys, re
KEEP = {"Consolas", "Courier New", "Cambria Math", "Menlo", "Symbol", "Wingdings", "OpenSymbol"}
def sub_attr(s, pat):
    return re.sub(pat, lambda m: m.group(0) if m.group(2) in KEEP else f'{m.group(1)}="Pretendard"', s)
def fix(name, s):
    if name.endswith(".xml"):
        s = sub_attr(s, r'(typeface)="([^"]*)"') if ("theme" in name or name.startswith("ppt/")) else s
        s = sub_attr(s, r'(w:(?:ascii|hAnsi|eastAsia|cs))="([^"]*)"')
    if name == "word/styles.xml":
        rf = '<w:rFonts w:ascii="Pretendard" w:hAnsi="Pretendard" w:eastAsia="Pretendard" w:cs="Pretendard"/>'
        m = re.search(r'<w:rPrDefault>\s*<w:rPr>(.*?)</w:rPr>', s, re.S)
        if m:
            inner = re.sub(r'<w:rFonts[^>]*/>', '', m.group(1))
            s = s[:m.start(1)] + rf + inner + s[m.end(1):]
        # theme references would override explicit names → drop them so Pretendard wins
    if name in ("word/styles.xml", "word/document.xml"):
        s = re.sub(r'\sw:(?:ascii|hAnsi|eastAsia|cs)Theme="[^"]*"', '', s)
    return s
src, dst = sys.argv[1:3]
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        d = zi.read(it.filename)
        if it.filename.endswith(".xml"):
            d = fix(it.filename, d.decode("utf8")).encode("utf8")
        zo.writestr(it, d)
