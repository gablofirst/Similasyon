"""Süreç bazlı depo modeli: hacim + verim + layout → kişi; ya da kişi → kapasite, darboğaz.

Her depo aynı yapı taşlarından oluşur: mal kabul, yerleştirme, x-dock, besleme, yer değiştirme (ABC),
toplama, paketleme, kantar/kontrol, sevk, VAS ... Yönetici her süreç için şunu verir:
  hacim   : günlük birim (palet, koli, satır, sipariş, adet)
  verim   : birim / adam-saat — bugünkü layout'ta ölçülmüş (KPI raporu, cycle time)
  seyahat : verimin içindeki yürüme/sürüş payı (0–1)
  kaynak → hedef : layout'ta sürecin başladığı ve bittiği bölge

Layout etkisi: bölgeler taşınınca yalnız yürüme payı mesafeyle orantılı değişir,
  süre çarpanı = (1 − seyahat) + seyahat × mesafe / referans_mesafe
  etkin verim  = verim × (1 − kayıp) / süre çarpanı
referans_mesafe = verimin ölçüldüğü layout'taki mesafe (senaryo ilk kurulduğunda sabitlenir).

İki mod:
  ihtiyaç  : kişi = hacim ÷ etkin verim ÷ net saat
  kapasite : süreçlere kişi atanır (toplam N kişi önceliğe göre dağıtılır veya elle); kapasite, doluluk,
             akış bazında günlük karşılama = en düşük kapasite/hacim oranı (darboğaz)

Dağıtım (N kişi): 0,5 FTE adımlarla, önce öncelik 1 süreçlerin ihtiyacı tam karşılanır, sonra 2, sonra 3;
kişi yetmeyen seviyede ihtiyaca orantılı paylaştırılır (en büyük kalan). Artan kişi ihtiyaca orantılı eklenir.
0,5 FTE = yarım gün; küçük süreçleri (yerleştirme, x-dock) paylaşımlı personelin yaptığını temsil eder.

Uygulamadaki `app/motor.js` ile birebir aynı hesap; eşitlik `tests/test_surec.py` içinde Node ile denenir.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Bolge:
    id: str
    ad: str
    x: float
    y: float
    w: float
    h: float
    maks_kisi: float | None = None

    @property
    def merkez(self) -> tuple[float, float]:
        return self.x + self.w / 2, self.y + self.h / 2


@dataclass
class Surec:
    id: str
    ad: str
    akis: str            # giris | cikis | ic | vas
    birim: str
    hacim: float
    verim: float
    seyahat: float = 0.0
    kaynak: str | None = None
    hedef: str | None = None
    ref_mesafe: float | None = None
    aktif: bool = True
    atanan: float | None = None   # elle atanmış kişi (kapasite modu)
    oncelik: int = 2              # 1 = önce karşılanır (sevk süresi olan çıkış), 3 = ertelenebilir (VAS, ABC)
    kayip: float = 0.0            # akış kaybı (sefer hazırlığı, dönüş, sıkışma); ölçülmüş verimde 0, hedef verimde ≈0,2


@dataclass
class Senaryo:
    ad: str
    surecler: list[Surec]
    bolgeler: list[Bolge] = field(default_factory=list)
    net_saat: float = 7.5
    vardiya: int = 1
    devam: float = 1.0
    toplam_kisi: float | None = None   # None → ihtiyaç modu
    atama_adimi: float = 0.5           # FTE
    hacim_carpani: float = 1.0         # what-if: tüm hacimler × (büyüme, kampanya günü)


def mesafe(bolgeler: dict[str, Bolge], a: str | None, b: str | None) -> float:
    """Manhattan mesafesi (raf koridorlarında yürüme dik açılıdır). Aynı bölge içi: (en + boy) / 2."""
    if not a or not b or a not in bolgeler or b not in bolgeler:
        return 0.0
    if a == b:
        z = bolgeler[a]
        return (z.w + z.h) / 2
    (ax, ay), (bx, by) = bolgeler[a].merkez, bolgeler[b].merkez
    return abs(ax - bx) + abs(ay - by)


def referanslari_sabitle(s: Senaryo) -> None:
    """Verimin ölçüldüğü layout: ref_mesafe boş olan süreçlere bugünkü mesafeyi yazar."""
    bz = {b.id: b for b in s.bolgeler}
    for p in s.surecler:
        if p.ref_mesafe is None:
            p.ref_mesafe = mesafe(bz, p.kaynak, p.hedef)


def _en_buyuk_kalan(agirlik: list[float], birim: int) -> list[int]:
    t = sum(agirlik)
    if t <= 0 or birim <= 0:
        return [0] * len(agirlik)
    pay = [birim * x / t for x in agirlik]
    taban = [math.floor(x + 1e-9) for x in pay]
    kalan = birim - sum(taban)
    sira = sorted(range(len(pay)), key=lambda i: (-(pay[i] - taban[i]), i))
    for i in sira[:kalan]:
        taban[i] += 1
    return taban


def dagit(ihtiyac: list[float], oncelik: list[int], toplam: float, adim: float = 0.5) -> list[float]:
    """Toplam kişiyi önceliğe göre, `adim` FTE birimleriyle dağıtır (açıklama: modül başı)."""
    n = len(ihtiyac)
    birim = int(math.floor(toplam / adim + 1e-9))
    gerek = [math.ceil(x / adim - 1e-9) if x > 0 else 0 for x in ihtiyac]
    out = [0] * n
    for lvl in sorted(set(oncelik)):
        idx = [i for i in range(n) if oncelik[i] == lvl]
        g = sum(gerek[i] for i in idx)
        if g <= birim:
            for i in idx:
                out[i] = gerek[i]
            birim -= g
        else:
            for i, u in zip(idx, _en_buyuk_kalan([ihtiyac[i] for i in idx], birim)):
                out[i] = u
            birim = 0
            break
    if birim > 0:
        for i, u in enumerate(_en_buyuk_kalan(ihtiyac, birim)):
            out[i] += u
    return [u * adim for u in out]


def hesapla(s: Senaryo) -> dict:
    bz = {b.id: b for b in s.bolgeler}
    aktif = [p for p in s.surecler if p.aktif and p.hacim > 0 and p.verim > 0 and p.kayip < 1]
    satirlar = []
    for p in aktif:
        d = mesafe(bz, p.kaynak, p.hedef)
        ref = p.ref_mesafe if p.ref_mesafe else 0.0
        carpan = (1 - p.seyahat) + p.seyahat * (d / ref) if ref > 0 else 1.0
        ev = p.verim * (1 - p.kayip) / carpan
        hacim = p.hacim * s.hacim_carpani
        adam_saat = hacim / ev
        satirlar.append(dict(id=p.id, ad=p.ad, akis=p.akis, birim=p.birim, hacim=hacim, mesafe=d,
                             carpan=carpan, etkin_verim=ev, adam_saat=adam_saat,
                             ihtiyac=adam_saat / s.net_saat, kaynak=p.kaynak, atanan_elle=p.atanan,
                             oncelik=p.oncelik))

    ihtiyac_top = sum(r["ihtiyac"] for r in satirlar)
    kapasite_modu = s.toplam_kisi is not None or any(r["atanan_elle"] is not None for r in satirlar)
    if kapasite_modu:
        elle = sum(r["atanan_elle"] for r in satirlar if r["atanan_elle"] is not None)
        oto = [r for r in satirlar if r["atanan_elle"] is None]
        if s.toplam_kisi is None:   # yalnız elle atananlar: diğerleri ihtiyaç kadar
            for r in oto:
                r["atanan"] = r["ihtiyac"]
        else:
            kalan = max(0.0, s.toplam_kisi - elle)
            for r, n in zip(oto, dagit([r["ihtiyac"] for r in oto], [r["oncelik"] for r in oto], kalan, s.atama_adimi)):
                r["atanan"] = n
        for r in satirlar:
            if r["atanan_elle"] is not None:
                r["atanan"] = r["atanan_elle"]
            r["kapasite"] = r["atanan"] * s.net_saat * r["etkin_verim"]
            r["oran"] = r["kapasite"] / r["hacim"]
            r["doluluk"] = r["hacim"] / r["kapasite"] if r["kapasite"] > 0 else math.inf
    else:
        for r in satirlar:
            r["atanan"] = r["ihtiyac"]
            r["kapasite"] = r["hacim"]
            r["oran"] = 1.0
            r["doluluk"] = 1.0

    akislar = {}
    for r in satirlar:
        a = akislar.setdefault(r["akis"], dict(karsilama=math.inf, darbogaz=None))
        if r["oran"] < a["karsilama"]:
            a["karsilama"], a["darbogaz"] = r["oran"], r["id"]
    for a in akislar.values():
        a["karsilama"] = min(1.0, a["karsilama"])

    bolge_kisi = {}
    for r in satirlar:
        if r["kaynak"]:
            bolge_kisi[r["kaynak"]] = bolge_kisi.get(r["kaynak"], 0.0) + r["atanan"] / max(1, s.vardiya)
    bolge_uyari = [k for k, v in bolge_kisi.items() if bz.get(k) and bz[k].maks_kisi and v > bz[k].maks_kisi]

    atanan_top = sum(r["atanan"] for r in satirlar)
    return dict(
        satirlar=satirlar,
        ihtiyac=ihtiyac_top,
        atanan=atanan_top,
        bordro=math.ceil(atanan_top / s.devam - 1e-9) if s.devam > 0 else math.inf,
        akislar=akislar,
        bolge_kisi=bolge_kisi,
        bolge_uyari=bolge_uyari,
        mod="kapasite" if kapasite_modu else "ihtiyac",
    )


def _sec(cls, d: dict) -> dict:
    alan = cls.__dataclass_fields__
    return {k: v for k, v in d.items() if k in alan}


def senaryo_sozlukten(d: dict) -> Senaryo:
    """Uygulamanın JSON senaryosundan (app/motor.js biçimi) Senaryo kurar; bilinmeyen alanlar (renk vb.) atlanır."""
    return Senaryo(
        ad=d.get("ad", ""),
        net_saat=d.get("net_saat", 7.5),
        vardiya=d.get("vardiya", 1),
        devam=d.get("devam", 1.0),
        toplam_kisi=d.get("toplam_kisi"),
        atama_adimi=d.get("atama_adimi", 0.5),
        hacim_carpani=d.get("hacim_carpani", 1.0),
        bolgeler=[Bolge(**_sec(Bolge, b)) for b in d.get("bolgeler", [])],
        surecler=[Surec(**_sec(Surec, p)) for p in d.get("surecler", [])],
    )
