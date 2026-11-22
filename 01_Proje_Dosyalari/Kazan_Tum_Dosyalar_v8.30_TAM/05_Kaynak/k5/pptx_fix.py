# pptxgenjs aynı paragrafta ikinci run'dan önce <a:pPr> yazıyor (geçersiz OOXML, PowerPoint "onar" uyarısı verir).
# Paragraf içindeki ilk pPr dışındakileri siler. Kullanım: python3 pptx_fix.py giris.pptx cikis.pptx
import sys, re, zipfile
src, dst = sys.argv[1], sys.argv[2]; n = 0
pat = re.compile(r'(</a:r>)<a:pPr\b(?:[^>]*/>|[^>]*>.*?</a:pPr>)', re.S)
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        if it.filename.endswith('/'): continue
        b = zi.read(it.filename)
        if it.filename.startswith('ppt/slides/slide') and it.filename.endswith('.xml'):
            s = b.decode('utf-8'); s, k = pat.subn(r'\1', s); n += k; b = s.encode('utf-8')
        zo.writestr(it, b)
print('ara pPr silindi:', n)
