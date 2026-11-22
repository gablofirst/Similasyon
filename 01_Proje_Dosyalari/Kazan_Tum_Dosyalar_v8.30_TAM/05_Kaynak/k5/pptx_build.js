// v8.27 — ölçülmüş sunum JSON'undan düzenlenebilir PPTX üretir (metinler, kutular, tablolar yerel PowerPoint nesnesi).
// Kullanım: node pptx_build.js deck_olcu.json deck.json(bölümler) cikis.pptx
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const [, , MEAS, DECK, OUT] = process.argv;
const D = JSON.parse(fs.readFileSync(MEAS, 'utf8'));
const DJ = JSON.parse(fs.readFileSync(DECK, 'utf8'));
const PX = 144;                       // 1920 px = 13,333 in
const I = v => v / PX, PT = v => v * 0.5;   // px → in, px → pt
const FONT = 'Arial';
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.title = DJ.title; pres.author = 'Sedat Birinci'; pres.company = 'Protein Ocean';
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
const secStart = {}; Object.values(DJ.sections).forEach(s => secStart[s.start] = s.description);
let curSec = null;

const runOpts = (r, extra = {}) => {
  const o = { fontFace: FONT, fontSize: PT(r.size), color: r.color, bold: !!r.b, italic: !!r.i, ...extra };
  if (r.ls) o.charSpacing = PT(r.ls);
  if (r.link) o.hyperlink = { url: r.link };
  if (r.u) o.underline = { style: 'sng' };
  return o;
};
// paragraflar → pptxgenjs run dizisi
function textRuns(paras, it) {
  const arr = [];
  paras.forEach((p, pi) => {
    let first = true, soft = false;
    p.runs.forEach(r => {
      if (r.br) { soft = true; return; }
      const fsz = r.size;
      const o = runOpts(r);
      if (first && it.noPara) { if (pi > 0) arr[arr.length - 1].options.breakLine = true; first = false; }
      if (first) {
        o.align = it.align; o.lineSpacing = Math.round(PT(it.lh * fsz) * 10) / 10;
        if (p.bullet) { o.bullet = p.bullet === 'num' ? { type: 'number', indent: PT(it.indent || 30) } : { indent: PT(it.indent || 30) }; }
        if (it.gap && pi < paras.length - 1) o.paraSpaceAfter = PT(it.gap);
        if (pi > 0) arr[arr.length - 1].options.breakLine = true;
        first = false;
      }
      if (soft) { o.softBreakBefore = true; soft = false; }
      arr.push({ text: r.t, options: o });
    });
  });
  return arr;
}

D.forEach((s, si) => {
  if (secStart[s.id]) { curSec = secStart[s.id]; pres.addSection({ title: curSec }); }
  const sl = pres.addSlide(curSec ? { sectionTitle: curSec } : {});
  sl.background = { color: s.bg || 'FFFFFF' };
  let n = 0;
  s.items.forEach(it => {
    n++;
    if (it.k === 'rect') {
      if (it.w < 1 || it.h < 1) return;
      const o = { x: I(it.x), y: I(it.y), w: I(it.w), h: I(it.h), objectName: `${s.id}_kutu_${n}` };
      o.fill = it.fill ? { color: it.fill, transparency: Math.round((1 - (it.fa ?? 1)) * 100) } : { type: 'none' };
      o.line = it.line ? { color: it.line, width: PT(it.lw) } : { type: 'none' };
      if (it.rad > 0.5 && it.name !== 'kenar') { o.rectRadius = I(Math.min(it.rad, it.h / 2, it.w / 2)); sl.addShape(pres.shapes.ROUNDED_RECTANGLE, o); }
      else sl.addShape(pres.shapes.RECTANGLE, o);
    } else if (it.k === 'text') {
      const runs = textRuns(it.paras, it); if (!runs.length) return;
      const slack = 8;
      let x = it.x, w = it.w + slack;
      if (it.align === 'right') x -= slack; else if (it.align === 'center') x -= slack / 2;
      sl.addText(runs, { x: I(x), y: I(it.y), w: I(w), h: I(Math.max(it.h, 10)), margin: 0, valign: 'top', wrap: true, fit: 'none', isTextBox: true, objectName: `${s.id}_${String(it.name).split(' ')[0]}_${n}` });
    } else if (it.k === 'img') {
      let { x, y, w, h } = it;
      if (it.fit === 'contain' && it.nw && it.nh) { const sc = Math.min(w / it.nw, h / it.nh); const w2 = it.nw * sc, h2 = it.nh * sc; x += (w - w2) / 2; y += (h - h2) / 2; w = w2; h = h2; }
      const data = it.src.replace(/^data:/, '');
      sl.addImage({ data, x: I(x), y: I(y), w: I(w), h: I(h), altText: it.alt, objectName: `${s.id}_gorsel` });
    } else if (it.k === 'table') {
      // sütun genişlikleri: en çok hücreli satırdan
      const base = it.rows.reduce((a, r) => r.cells.length > a.cells.length ? r : a, it.rows[0]);
      const colW = base.cells.map(c => I(c.w));
      const rows = it.rows.map(r => r.cells.map(c => {
        const t = c.runs.length ? textRuns([{ runs: c.runs }], { align: c.align, lh: c.lh || 1.3, noPara: true }) : [{ text: '', options: { fontFace: FONT, fontSize: PT(c.fs) } }];
        const none = { type: 'none' };
        const o = { fill: c.fill ? { color: c.fill } : undefined, align: c.align, valign: c.valign, margin: [I(c.p.t), I(c.p.r), I(c.p.b), I(c.p.l)],
          border: [c.bt ? { pt: PT(c.bt), color: c.btc || 'C9D1D3' } : none, none, c.bb ? { pt: PT(c.bb), color: c.bbc || 'C9D1D3' } : none, none] };
        if (c.span > 1) o.colspan = c.span;
        return { text: t, options: o };
      }));
      sl.addTable(rows, { x: I(it.x), y: I(it.y), w: I(it.w), colW, rowH: it.rows.map(r => I(r.h)), autoPage: false, objectName: `${s.id}_tablo` });
    } else if (it.k === 'pg') {
      sl.slideNumber = { x: I(it.x - 8), y: I(it.y), w: I(it.w + 8), h: I(it.h), fontFace: FONT, fontSize: PT(it.size), color: it.color, align: 'right' };
    }
  });
  if (s.notes) sl.addNotes(s.notes);
});
pres.writeFile({ fileName: OUT }).then(f => console.log('yazıldı', f));
