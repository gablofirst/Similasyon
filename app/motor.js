/* depoplan süreç motoru — depoplan/surec.py ile birebir aynı hesap (eşitlik testi: tests/test_surec.py).
 *
 * süre çarpanı = (1 − seyahat) + seyahat × mesafe / referans_mesafe
 * etkin verim  = verim × (1 − kayıp) / süre çarpanı;  kişi = hacim ÷ etkin verim ÷ net saat
 * kapasite modu: toplam_kisi önceliğe göre 0,5 FTE adımlarla dağıtılır (elle atananlar sabit),
 *   oran = kapasite / hacim, akış karşılaması = min(oran) (darboğaz)
 */
(function (kok) {
  'use strict';

  function merkez(b) { return [b.x + b.w / 2, b.y + b.h / 2]; }

  function mesafe(bz, a, b) {
    if (!a || !b || !bz[a] || !bz[b]) return 0;
    if (a === b) return (bz[a].w + bz[a].h) / 2;
    const [ax, ay] = merkez(bz[a]), [bx, by] = merkez(bz[b]);
    return Math.abs(ax - bx) + Math.abs(ay - by);
  }

  function bolgeSozluk(s) {
    const bz = {};
    for (const b of s.bolgeler || []) bz[b.id] = b;
    return bz;
  }

  function referanslariSabitle(s) {
    const bz = bolgeSozluk(s);
    for (const p of s.surecler) if (p.ref_mesafe == null) p.ref_mesafe = mesafe(bz, p.kaynak, p.hedef);
    return s;
  }

  function enBuyukKalan(agirlik, birim) {
    const t = agirlik.reduce((a, b) => a + b, 0);
    if (t <= 0 || birim <= 0) return agirlik.map(() => 0);
    const pay = agirlik.map(x => birim * x / t);
    const taban = pay.map(x => Math.floor(x + 1e-9));
    const kalan = birim - taban.reduce((a, b) => a + b, 0);
    const sira = pay.map((_, i) => i).sort((i, j) => ((pay[j] - taban[j]) - (pay[i] - taban[i])) || (i - j));
    for (const i of sira.slice(0, kalan)) taban[i] += 1;
    return taban;
  }

  // Önceliğe göre, `adim` FTE birimleriyle dağıtım (depoplan/surec.py dagit ile aynı)
  function dagit(ihtiyac, oncelik, toplam, adim) {
    adim = adim || 0.5;
    const n = ihtiyac.length;
    let birim = Math.floor(toplam / adim + 1e-9);
    const gerek = ihtiyac.map(x => (x > 0 ? Math.ceil(x / adim - 1e-9) : 0));
    const out = new Array(n).fill(0);
    const seviyeler = [...new Set(oncelik)].sort((a, b) => a - b);
    for (const lvl of seviyeler) {
      const idx = [];
      for (let i = 0; i < n; i++) if (oncelik[i] === lvl) idx.push(i);
      const g = idx.reduce((a, i) => a + gerek[i], 0);
      if (g <= birim) { for (const i of idx) out[i] = gerek[i]; birim -= g; }
      else {
        const u = enBuyukKalan(idx.map(i => ihtiyac[i]), birim);
        idx.forEach((i, k) => { out[i] = u[k]; });
        birim = 0;
        break;
      }
    }
    if (birim > 0) enBuyukKalan(ihtiyac, birim).forEach((u, i) => { out[i] += u; });
    return out.map(u => u * adim);
  }

  function hesapla(s) {
    const bz = bolgeSozluk(s);
    const net = s.net_saat || 7.5;
    const hc = s.hacim_carpani == null ? 1 : s.hacim_carpani;
    const aktif = s.surecler.filter(p => p.aktif !== false && p.hacim > 0 && p.verim > 0 && (p.kayip || 0) < 1);
    const satirlar = aktif.map(p => {
      const d = mesafe(bz, p.kaynak, p.hedef);
      const ref = p.ref_mesafe || 0;
      const sey = p.seyahat || 0;
      const carpan = ref > 0 ? (1 - sey) + sey * (d / ref) : 1;
      const ev = p.verim * (1 - (p.kayip || 0)) / carpan;
      const hacim = p.hacim * hc;
      const adam_saat = hacim / ev;
      return {
        id: p.id, ad: p.ad, akis: p.akis, birim: p.birim, hacim, mesafe: d, carpan,
        etkin_verim: ev, adam_saat, ihtiyac: adam_saat / net, kaynak: p.kaynak,
        atanan_elle: p.atanan == null ? null : p.atanan, oncelik: p.oncelik == null ? 2 : p.oncelik,
      };
    });

    const ihtiyacTop = satirlar.reduce((a, r) => a + r.ihtiyac, 0);
    const kapasiteModu = s.toplam_kisi != null || satirlar.some(r => r.atanan_elle != null);
    if (kapasiteModu) {
      const elle = satirlar.filter(r => r.atanan_elle != null).reduce((a, r) => a + r.atanan_elle, 0);
      const oto = satirlar.filter(r => r.atanan_elle == null);
      if (s.toplam_kisi == null) {
        for (const r of oto) r.atanan = r.ihtiyac;
      } else {
        const kalan = Math.max(0, s.toplam_kisi - elle);
        const n = dagit(oto.map(r => r.ihtiyac), oto.map(r => r.oncelik), kalan, s.atama_adimi || 0.5);
        oto.forEach((r, i) => { r.atanan = n[i]; });
      }
      for (const r of satirlar) {
        if (r.atanan_elle != null) r.atanan = r.atanan_elle;
        r.kapasite = r.atanan * net * r.etkin_verim;
        r.oran = r.kapasite / r.hacim;
        r.doluluk = r.kapasite > 0 ? r.hacim / r.kapasite : Infinity;
      }
    } else {
      for (const r of satirlar) { r.atanan = r.ihtiyac; r.kapasite = r.hacim; r.oran = 1; r.doluluk = 1; }
    }

    const akislar = {};
    for (const r of satirlar) {
      const a = akislar[r.akis] || (akislar[r.akis] = { karsilama: Infinity, darbogaz: null });
      if (r.oran < a.karsilama) { a.karsilama = r.oran; a.darbogaz = r.id; }
    }
    for (const k in akislar) akislar[k].karsilama = Math.min(1, akislar[k].karsilama);

    const bolge_kisi = {};
    const vard = Math.max(1, s.vardiya || 1);
    for (const r of satirlar) if (r.kaynak) bolge_kisi[r.kaynak] = (bolge_kisi[r.kaynak] || 0) + r.atanan / vard;
    const bolge_uyari = Object.keys(bolge_kisi).filter(k => bz[k] && bz[k].maks_kisi && bolge_kisi[k] > bz[k].maks_kisi);

    const atananTop = satirlar.reduce((a, r) => a + r.atanan, 0);
    const devam = s.devam || 1;
    return {
      satirlar, ihtiyac: ihtiyacTop, atanan: atananTop,
      bordro: Math.ceil(atananTop / devam - 1e-9),
      akislar, bolge_kisi, bolge_uyari, mod: kapasiteModu ? 'kapasite' : 'ihtiyac',
    };
  }

  const api = { mesafe, referanslariSabitle, dagit, hesapla };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else kok.DepoMotor = api;
})(typeof window !== 'undefined' ? window : globalThis);
