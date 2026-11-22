// v8.27 — onay sunumu HTML'ini (1920×1080 section'lar) düzenlenebilir PPTX için ölçer.
// Tarayıcıda çalışır (playwright page.evaluate). Her slayt: arka plan, kutular, metin blokları, tablolar, görseller, notlar.
() => {
  const INLINE = new Set(['B', 'STRONG', 'I', 'EM', 'A', 'SPAN', 'BR', 'SUB', 'SUP', 'SMALL', 'U', 'CODE']);
  const hex = c => { const m = c && c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/); if (!m) return null; if (m[4] !== undefined && +m[4] === 0) return null; return [m[1], m[2], m[3]].map(v => (+v).toString(16).padStart(2, '0')).join('').toUpperCase(); };
  const alpha = c => { const m = c && c.match(/rgba\([^)]*,\s*([\d.]+)\)/); return m ? +m[1] : 1; };
  const out = [];
  document.querySelectorAll('section').forEach((sec, si) => {
    const S = sec.getBoundingClientRect(); const items = []; const scs = getComputedStyle(sec);
    const R = el => { const r = el.getBoundingClientRect(); return { x: r.left - S.left, y: r.top - S.top, w: r.width, h: r.height }; };
    const runStyle = (el, cs) => ({ b: +cs.fontWeight >= 600, i: cs.fontStyle === 'italic', color: hex(cs.color) || '000000', size: parseFloat(cs.fontSize), head: /Grotesk/.test(cs.fontFamily), upper: cs.textTransform === 'uppercase', ls: parseFloat(cs.letterSpacing) || 0, link: el.closest('a') ? el.closest('a').href : null, u: cs.textDecorationLine.includes('underline') });
    const isTextBlock = el => { let txt = false; for (const n of el.childNodes) { if (n.nodeType === 3 && n.textContent.trim()) txt = true; else if (n.nodeType === 1 && !INLINE.has(n.tagName)) return false; else if (n.nodeType === 1 && n.textContent.trim()) txt = true; } return txt; };
    const runsOf = el => { const runs = []; const walk = (node) => { for (const n of node.childNodes) { if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' '); if (t) runs.push(Object.assign({ t }, runStyle(node, getComputedStyle(node)))); } else if (n.nodeType === 1) { if (n.tagName === 'BR') runs.push({ br: true }); else walk(n); } } }; walk(el);
      // kırp: baştaki/sondaki boşluk
      while (runs.length && !runs[0].br && !runs[0].t.trim()) runs.shift(); if (runs.length && runs[0].t) runs[0].t = runs[0].t.replace(/^\s+/, '');
      while (runs.length && !runs[runs.length - 1].br && !runs[runs.length - 1].t.trim()) runs.pop(); if (runs.length && runs[runs.length - 1].t) runs[runs.length - 1].t = runs[runs.length - 1].t.replace(/\s+$/, '');
      runs.forEach(r => { if (r.upper && r.t) r.t = r.t.toLocaleUpperCase('tr-TR'); }); return runs; };
    const pad = cs => ({ l: parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), r: parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth), t: parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth), b: parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth) });
    const box = (el, cs) => { const bg = hex(cs.backgroundColor); const bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(cs['border' + s + 'Width']) || 0); const bc = ['Top', 'Right', 'Bottom', 'Left'].map(s => hex(cs['border' + s + 'Color']));
      const uniform = bw.every(w => w === bw[0]) && bw[0] > 0 && bc.every(c => c === bc[0]);
      if (!bg && !bw.some(w => w > 0)) return; const r = R(el); const rad = parseFloat(cs.borderTopLeftRadius) || 0;
      items.push({ k: 'rect', ...r, fill: bg, fa: alpha(cs.backgroundColor), line: uniform ? bc[0] : null, lw: uniform ? bw[0] : 0, rad, name: (el.className || el.tagName).toString() });
      if (!uniform) ['Top', 'Right', 'Bottom', 'Left'].forEach((s, i) => { if (bw[i] > 0 && bc[i]) { const t = bw[i]; const g = s === 'Top' ? { x: r.x, y: r.y, w: r.w, h: t } : s === 'Bottom' ? { x: r.x, y: r.y + r.h - t, w: r.w, h: t } : s === 'Left' ? { x: r.x, y: r.y, w: t, h: r.h } : { x: r.x + r.w - t, y: r.y, w: t, h: r.h }; items.push({ k: 'rect', ...g, fill: bc[i], fa: 1, line: null, lw: 0, rad: 0, name: 'kenar' }); } }); };
    const textItem = (el, cs, paras) => { const r = R(el); const p = pad(cs); const lh = parseFloat(cs.lineHeight); const fs = parseFloat(cs.fontSize);
      items.push({ k: 'text', x: r.x + p.l, y: r.y + p.t, w: r.w - p.l - p.r, h: r.h - p.t - p.b, align: cs.textAlign === 'center' ? 'center' : (cs.textAlign === 'right' || cs.textAlign === 'end') ? 'right' : 'left', lh: isNaN(lh) ? 1.2 : lh / fs, paras, gap: 0, name: (el.className || el.tagName).toString() }); };
    const visit = el => { const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || el.tagName === 'ASIDE') return;
      if (el.tagName === 'IMG') { const r = R(el); items.push({ k: 'img', ...r, src: el.src, nw: el.naturalWidth, nh: el.naturalHeight, fit: cs.objectFit, alt: el.alt }); return; }
      if (el.tagName === 'TABLE') { const r = R(el); const rows = []; for (const tr of el.rows) { const trc = getComputedStyle(tr); const cells = []; for (const td of tr.cells) { const c = getComputedStyle(td); const p = pad(c); const bb = parseFloat(c.borderBottomWidth) || 0;
            cells.push({ runs: runsOf(td), w: td.getBoundingClientRect().width, span: td.colSpan, fill: hex(c.backgroundColor) || hex(trc.backgroundColor), align: c.textAlign === 'center' ? 'center' : (c.textAlign === 'right' || c.textAlign === 'end') ? 'right' : 'left', valign: c.verticalAlign === 'top' ? 'top' : c.verticalAlign === 'bottom' ? 'bottom' : 'middle', p, bb, bbc: hex(c.borderBottomColor), bt: parseFloat(c.borderTopWidth) || 0, btc: hex(c.borderTopColor), fs: parseFloat(c.fontSize), lh: parseFloat(c.lineHeight) / parseFloat(c.fontSize) }); }
          rows.push({ h: tr.getBoundingClientRect().height, cells }); }
        items.push({ k: 'table', ...r, rows, collapse: getComputedStyle(el).borderCollapse }); return; }
      if (el.classList.contains('pg')) { const r = R(el); items.push({ k: 'pg', ...r, n: si + 1, color: hex(cs.color), size: parseFloat(cs.fontSize) }); return; }
      box(el, cs);
      if (el.tagName === 'UL' || el.tagName === 'OL') { const paras = []; let gapPx = 0; const lis = [...el.children].filter(c => c.tagName === 'LI'); if (lis.length > 1) gapPx = lis[1].getBoundingClientRect().top - lis[0].getBoundingClientRect().bottom;
        lis.forEach(li => paras.push({ runs: runsOf(li), bullet: el.tagName === 'OL' ? 'num' : true })); const r = R(el); const lh = parseFloat(cs.lineHeight), fs = parseFloat(cs.fontSize);
        items.push({ k: 'text', x: r.x, y: r.y, w: r.w, h: r.h, indent: parseFloat(cs.paddingLeft), align: 'left', lh: isNaN(lh) ? 1.2 : lh / fs, paras, gap: gapPx, name: 'liste' }); return; }
      if (isTextBlock(el)) { textItem(el, cs, [{ runs: runsOf(el) }]); return; }
      for (const c of el.children) visit(c); };
    for (const c of sec.children) visit(c);
    const aside = sec.querySelector('aside');
    out.push({ id: sec.id, bg: hex(scs.backgroundColor), items, notes: aside ? aside.textContent.trim().replace(/\s+/g, ' ') : '' });
  });
  return out;
}
