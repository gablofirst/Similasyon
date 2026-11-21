"""Genel veri şeması: her şirketten istenen girdi tabloları ve doğrulama.

Dört tablo yeter:
  1. siparis_satiri  — sipariş satırı (ikas, Shopify, ERP export'u ...)
  2. sku             — ürün ana verisi (ölçü, ağırlık, koli/palet)
  3. bom             — kit / karma koli reçetesi (isteğe bağlı)
  4. parametreler    — verim, vardiya, eşikler (varsayılanlar Kazan v8.16'dan)

Doğrulama hata fırlatmaz; bulguları liste olarak döner. Kazan'da en çok zaman alan
iş veri temizliğiydi (ikas↔ERP farkı, eksik ölçü, barkod eşleşmesi); bu katman onu görünür kılar.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd
from pydantic import BaseModel, Field

# ---------------------------------------------------------------- tablo sütunları
SIPARIS_SATIRI = {
    "siparis_no": "str",      # zorunlu
    "tarih": "datetime",      # zorunlu, sipariş zamanı (saat varsa saat × gün analizi yapılır)
    "sku": "str",             # zorunlu
    "adet": "float",          # zorunlu, > 0
    "kanal": "str",           # isteğe bağlı: web, pazaryeri, b2b ...
    "tasiyici": "str",        # isteğe bağlı: kargo firması
    "iade": "bool",           # isteğe bağlı
}
SIPARIS_ZORUNLU = ["siparis_no", "tarih", "sku", "adet"]

SKU = {
    "sku": "str",             # zorunlu, siparis_satiri.sku ile eşleşir
    "ad": "str",
    "barkod": "str",
    "en_cm": "float", "boy_cm": "float", "yukseklik_cm": "float",
    "agirlik_kg": "float",
    "koli_ici_adet": "float",
    "palet_koli": "float",
    "kategori": "str",
}
SKU_ZORUNLU = ["sku"]

BOM = {
    "kit_sku": "str",         # zorunlu
    "bilesen_sku": "str",     # zorunlu
    "miktar": "float",        # zorunlu, > 0
}
BOM_ZORUNLU = ["kit_sku", "bilesen_sku", "miktar"]


class Parametreler(BaseModel):
    """Model girdileri. Varsayılanlar Kazan v8.16 kadro simülasyonundan; her şirket kendi ölçümüyle değiştirir."""

    toplama_hizi: float = Field(120, description="satır / adam-saat (arabalı hücre)")
    paketleme_hizi: float = Field(71, description="sipariş / adam-saat")
    hazir_paket_hizi: float = Field(140, description="sipariş / adam-saat")
    net_saat: float = Field(7.5, description="vardiya başı net çalışma saati")
    satir_siparis: float = Field(1.762, description="toplama satırı / sipariş (kit yükü dahil)")
    hucre_sayisi: int = 2
    hucre_basi_rahat_kisi: float = 8
    paket_istasyonu: int = 16
    hp_payi: float = Field(1.0, description="hazır paket hattına giden sipariş payı (Kazan modeli tüm hacme uygular)")
    araba_goz: int = 18
    araba_doluluk: float = 0.94
    araba_wip: float = Field(0.0538, description="dolaşımdaki sipariş / günlük sipariş")
    araba_pay: float = 1.1
    hucre_dongu_m: float = 30.6
    abc_esik: tuple[float, float] = (0.80, 0.95)
    xyz_esik: tuple[float, float] = (0.5, 1.0)


# ---------------------------------------------------------------- doğrulama
@dataclass
class Bulgu:
    seviye: str          # "hata" (model çalışmaz) | "uyari" (sonuç zayıflar)
    tablo: str
    mesaj: str
    adet: int = 0


@dataclass
class DogrulamaRaporu:
    bulgular: list[Bulgu] = field(default_factory=list)

    @property
    def gecerli(self) -> bool:
        return not any(b.seviye == "hata" for b in self.bulgular)

    def ekle(self, seviye: str, tablo: str, mesaj: str, adet: int = 0) -> None:
        self.bulgular.append(Bulgu(seviye, tablo, mesaj, adet))

    def tablo(self) -> pd.DataFrame:
        return pd.DataFrame([b.__dict__ for b in self.bulgular], columns=["seviye", "tablo", "mesaj", "adet"])


def _eksik_sutun(df: pd.DataFrame, zorunlu: list[str], ad: str, r: DogrulamaRaporu) -> bool:
    eksik = [c for c in zorunlu if c not in df.columns]
    if eksik:
        r.ekle("hata", ad, f"zorunlu sütun yok: {', '.join(eksik)}")
    return bool(eksik)


def tarih_coz(s: pd.Series) -> pd.Series:
    """Karışık biçimli tarih sütunu: ISO (2026-01-05) yıl-ay-gün, diğerleri (05.01.2026, 05/01/2026) gün-ay-yıl.

    Tek bir `dayfirst` ayarı ikisini birden doğru okuyamaz (ISO'yu gün-ay diye çevirir), bu yüzden ayrı çözülür.
    """
    if pd.api.types.is_datetime64_any_dtype(s):
        return s
    t = s.astype("string").str.strip()
    iso = t.str.match(r"^\d{4}-\d{1,2}-\d{1,2}").fillna(False)
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    if iso.any():
        out[iso] = pd.to_datetime(t[iso], errors="coerce", format="mixed")
    if (~iso).any():
        out[~iso] = pd.to_datetime(t[~iso], errors="coerce", format="mixed", dayfirst=True)
    return out


def siparis_hazirla(df: pd.DataFrame) -> pd.DataFrame:
    """Tipleri düzeltir; doğrulamadan önce çağrılır."""
    d = df.copy()
    d["siparis_no"] = d["siparis_no"].astype(str)
    d["sku"] = d["sku"].astype(str).str.strip()
    d["tarih"] = tarih_coz(d["tarih"])
    d["adet"] = pd.to_numeric(d["adet"], errors="coerce")
    return d


def dogrula(siparis: pd.DataFrame, sku: pd.DataFrame | None = None, bom: pd.DataFrame | None = None) -> DogrulamaRaporu:
    r = DogrulamaRaporu()
    if _eksik_sutun(siparis, SIPARIS_ZORUNLU, "siparis_satiri", r):
        return r
    s = siparis_hazirla(siparis)
    n = len(s)
    if n == 0:
        r.ekle("hata", "siparis_satiri", "tablo boş")
        return r
    if (k := s["tarih"].isna().sum()):
        r.ekle("hata", "siparis_satiri", "okunamayan tarih", int(k))
    if (k := (s["adet"].isna() | (s["adet"] <= 0)).sum()):
        r.ekle("uyari", "siparis_satiri", "adet boş veya ≤ 0 (iade/iptal olabilir, profilde dışarıda kalır)", int(k))
    if (k := s.duplicated(["siparis_no", "sku"]).sum()):
        r.ekle("uyari", "siparis_satiri", "aynı siparişte aynı SKU birden fazla satır (toplama satırı birleştirilir)", int(k))
    gun = s["tarih"].dt.normalize().nunique()
    if gun < 90:
        r.ekle("uyari", "siparis_satiri", f"yalnız {gun} günlük veri; P95 ve mevsimsellik için ≥ 1 yıl önerilir", gun)

    if sku is None:
        r.ekle("uyari", "sku", "ürün ana verisi yok: göz/raf hacmi ve kutu hesabı yapılamaz")
    elif not _eksik_sutun(sku, SKU_ZORUNLU, "sku", r):
        ana = set(sku["sku"].astype(str))
        satirda = s["sku"].unique()
        yok = [x for x in satirda if x not in ana]
        if yok:
            pay = s["sku"].isin(yok).mean()
            r.ekle("uyari", "sku", f"siparişte olup ana veride olmayan SKU (satırların %{pay*100:.1f}'i)", len(yok))
        olcu = [c for c in ("en_cm", "boy_cm", "yukseklik_cm") if c in sku.columns]
        if len(olcu) < 3:
            r.ekle("uyari", "sku", "ölçü sütunları eksik (en_cm, boy_cm, yukseklik_cm)")
        else:
            k = sku[olcu].isna().any(axis=1).sum()
            if k:
                r.ekle("uyari", "sku", "ölçüsü eksik SKU", int(k))
        if "agirlik_kg" not in sku.columns or sku["agirlik_kg"].isna().all():
            r.ekle("uyari", "sku", "ağırlık yok: raf yükü ve kargo desi/kg kontrolü yapılamaz")

    if bom is not None and not _eksik_sutun(bom, BOM_ZORUNLU, "bom", r):
        b = bom.astype({"kit_sku": str, "bilesen_sku": str})
        dongu = set(b["kit_sku"]) & set(b["bilesen_sku"])
        if dongu:
            r.ekle("uyari", "bom", "kit başka bir kitin bileşeni (çok seviyeli açılır)", len(dongu))
    return r


def bugun() -> str:
    return datetime.now().strftime("%d.%m.%Y")
