"""SKU profili: sipariş satırından ABC/XYZ, günlük talep, P95, tekli sipariş payı.

Kazan'daki `SKU_Profil.csv` kurallarıyla aynı:
  - ABC: büyükten küçüğe sıralı kümülatif pay ≤ 0,80 → A, ≤ 0,95 → B, kalan C
    (adet için `toplam_adet`, toplama sıklığı için `toplama_satiri` üzerinden)
  - XYZ: haftalık adet değişim katsayısı (CV) < 0,5 → X, < 1,0 → Y, kalan Z
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .sema import siparis_hazirla


def abc_sinifla(deger: pd.Series, esik: tuple[float, float] = (0.80, 0.95)) -> tuple[pd.Series, pd.Series]:
    """Sınıf ve kümülatif payı döner (girdi sırası korunur)."""
    sira = deger.sort_values(ascending=False, kind="mergesort")
    kum = sira.cumsum() / sira.sum()
    sinif = pd.Series(np.where(kum <= esik[0], "A", np.where(kum <= esik[1], "B", "C")), index=kum.index)
    return sinif.reindex(deger.index), kum.reindex(deger.index)


def xyz_sinifla(cv: pd.Series, esik: tuple[float, float] = (0.5, 1.0)) -> pd.Series:
    return pd.Series(np.where(cv < esik[0], "X", np.where(cv < esik[1], "Y", "Z")), index=cv.index)


def sku_profili(siparis: pd.DataFrame, abc_esik=(0.80, 0.95), xyz_esik=(0.5, 1.0)) -> pd.DataFrame:
    """Sipariş satırı → SKU başına profil.

    Günlük seriler verinin ilk ve son günü arasındaki tüm takvim günleri üzerinden
    (satış olmayan gün = 0) hesaplanır; P95 bu seriden alınır.
    """
    s = siparis_hazirla(siparis)
    s = s[s["tarih"].notna() & (s["adet"] > 0)]
    s["gun"] = s["tarih"].dt.normalize()
    # aynı siparişte aynı SKU = tek toplama satırı
    s = s.groupby(["siparis_no", "sku", "gun"], as_index=False)["adet"].sum()

    gunler = pd.date_range(s["gun"].min(), s["gun"].max(), freq="D")
    satir_say = s.groupby("siparis_no")["sku"].transform("size")

    p = s.groupby("sku").agg(
        toplam_adet=("adet", "sum"),
        toplama_satiri=("adet", "size"),
        siparis=("siparis_no", "nunique"),
        ilk_tarih=("gun", "min"),
        son_tarih=("gun", "max"),
        satis_olan_gun=("gun", "nunique"),
    )
    p["tekli_siparis"] = s[satir_say == 1].groupby("sku").size().reindex(p.index, fill_value=0)
    p["tekli_siparis_pay"] = p["tekli_siparis"] / p["siparis"]

    gunluk = s.pivot_table(index="gun", columns="sku", values="adet", aggfunc="sum").reindex(gunler, fill_value=0).fillna(0)
    p["gunluk_ort"] = gunluk.mean()
    p["gunluk_p95"] = gunluk.quantile(0.95)
    p["gunluk_maks"] = gunluk.max()
    son90 = gunluk.iloc[-90:]
    p["son90_gunluk_ort"] = son90.mean()
    p["son30_gunluk_ort"] = gunluk.iloc[-30:].mean()
    p["pik_katsayi_p95/ort"] = p["gunluk_p95"] / p["gunluk_ort"].replace(0, np.nan)

    haftalik = gunluk.resample("W-SUN").sum()
    p["haftalik_cv"] = haftalik.std(ddof=1) / haftalik.mean().replace(0, np.nan)
    p["satir_basi_adet"] = p["toplam_adet"] / p["toplama_satiri"]

    p["ABC_adet"], p["kum_pay_adet"] = abc_sinifla(p["toplam_adet"], abc_esik)
    p["ABC_satir"], p["kum_pay_satir"] = abc_sinifla(p["toplama_satiri"], abc_esik)
    p["XYZ"] = xyz_sinifla(p["haftalik_cv"].fillna(np.inf), xyz_esik)
    return p.sort_values("toplama_satiri", ascending=False)


def siparis_ozeti(siparis: pd.DataFrame) -> dict:
    """Depo boyutlandırmanın ilk tablosu: günlük sipariş, satır, gün tipi çarpanları."""
    s = siparis_hazirla(siparis)
    s = s[s["tarih"].notna() & (s["adet"] > 0)]
    s["gun"] = s["tarih"].dt.normalize()
    sip = s.groupby("siparis_no").agg(gun=("gun", "first"), satir=("sku", "nunique"))
    gunluk = sip.groupby("gun").size().reindex(pd.date_range(sip["gun"].min(), sip["gun"].max()), fill_value=0)
    ort = gunluk.mean()
    return {
        "gun": int(len(gunluk)),
        "siparis": int(len(sip)),
        "satir": int(sip["satir"].sum()),
        "satir_siparis": float(sip["satir"].mean()),
        "tekli_pay": float((sip["satir"] == 1).mean()),
        "gunluk_ort": float(ort),
        "gunluk_p95": float(gunluk.quantile(0.95)),
        "gunluk_maks": int(gunluk.max()),
        "carpan_p95": float(gunluk.quantile(0.95) / ort),
        "carpan_maks": float(gunluk.max() / ort),
    }
