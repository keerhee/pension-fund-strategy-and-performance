# LibreOffice로 pptx → pdf 변환하되, 한글·영문 사이 자동 간격(Asian spacing)을 끈다.
import sys, os, time, subprocess, uno
from com.sun.star.beans import PropertyValue
def pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p
src, dst = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                         "--accept=socket,host=localhost,port=2002;urp;"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ctx = None
for _ in range(60):
    try:
        local = uno.getComponentContext()
        res = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        ctx = res.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception:
        time.sleep(0.5)
desk = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desk.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (pv("Hidden", True),))
def fix_text(obj):
    try:
        enum = obj.getText().createEnumeration()
    except Exception:
        return
    while enum.hasMoreElements():
        par = enum.nextElement()
        try:
            par.ParaIsCharacterDistance = False
        except Exception:
            pass
def walk(shape):
    if shape.supportsService("com.sun.star.drawing.GroupShape"):
        for i in range(shape.getCount()): walk(shape.getByIndex(i))
        return
    if shape.supportsService("com.sun.star.drawing.TableShape"):
        tbl = shape.Model
        for r in range(tbl.Rows.Count):
            for c in range(tbl.Columns.Count):
                fix_text(tbl.getCellByPosition(c, r))
        return
    fix_text(shape)
pages = doc.getDrawPages()
for i in range(pages.getCount()):
    pg = pages.getByIndex(i)
    for j in range(pg.getCount()): walk(pg.getByIndex(j))
doc.storeToURL(uno.systemPathToFileUrl(dst), (pv("FilterName", "impress_pdf_Export"),))
doc.close(True)
try: desk.terminate()
except Exception: pass
proc.wait(timeout=30)
print("PDF:", dst)
