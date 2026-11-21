"""Kit / karma koli açma (Kazan `kit_explode.py` genelleştirmesi).

Kitin nasıl toplanacağı şirkete göre değişir; üç mod:
  - "bilesen": kit satırı bileşen satırlarına açılır (Kazan: BOM'lu karma koli, aynı göze)
  - "hazir":   kit önceden kurulur, siparişte tek satır (Kazan: 6 hazır paket kiti)
  - "sabit":   kit tek ürün gibi davranır, ama satır sayısı sabit (Kazan: 32'li bar = 3 satır)
Kazan'daki sabit SKU listeleri (HP_KIT vb.) burada parametre olur.
"""
from __future__ import annotations

import pandas as pd


def bom_sozlugu(bom: pd.DataFrame) -> dict[str, list[tuple[str, float]]]:
    b = bom.astype({"kit_sku": str, "bilesen_sku": str})
    return {k: list(zip(g["bilesen_sku"], g["miktar"].astype(float))) for k, g in b.groupby("kit_sku")}


def ac(sku: str, adet: float, bom: dict, derinlik: int = 0, maks: int = 5) -> list[tuple[str, float]]:
    """Kiti en alt bileşenlere açar (çok seviyeli, döngü koruması `maks`)."""
    if sku not in bom or derinlik >= maks:
        return [(sku, adet)]
    out: list[tuple[str, float]] = []
    for c, m in bom[sku]:
        out += ac(c, adet * m, bom, derinlik + 1, maks)
    return out


def siparisi_ac(
    siparis: pd.DataFrame,
    bom: pd.DataFrame,
    hazir: set[str] = frozenset(),
    sabit_satir: dict[str, int] | None = None,
) -> pd.DataFrame:
    """Sipariş satırlarını toplama satırına çevirir. Çıktıda `kaynak_kit` sütunu kitten gelen satırı işaretler.

    `sabit_satir` kitleri tek satır olarak kalır; `toplama_satir_agirlik` o kitin kaç satır sayılacağını taşır.
    """
    bd = bom_sozlugu(bom)
    sabit_satir = sabit_satir or {}
    rows = []
    for r in siparis.itertuples(index=False):
        d = r._asdict()
        sku = str(d["sku"])
        if sku in hazir or sku not in bd:
            rows.append({**d, "kaynak_kit": None, "toplama_satir_agirlik": 1})
        elif sku in sabit_satir:
            rows.append({**d, "kaynak_kit": sku, "toplama_satir_agirlik": sabit_satir[sku]})
        else:
            for c, q in ac(sku, float(d["adet"]), bd):
                rows.append({**d, "sku": c, "adet": q, "kaynak_kit": sku, "toplama_satir_agirlik": 1})
    return pd.DataFrame(rows)
