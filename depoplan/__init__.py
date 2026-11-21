"""depoplan — veriden depo kararına: profil, senaryo, kit, kadro (ve sonra slotting, yerleşim, DES).

Referans vaka: Kazan (Protein Ocean). Kazan verisi pakete girmez; yalnız testlerde depodaki
dosyalardan okunur.
"""
from .kadro import KAZAN_GUN_TIPLERI, GunTipi, KadroSonucu, bordro, kadro_hesapla, senaryolar
from .profil import abc_sinifla, siparis_ozeti, sku_profili, xyz_sinifla
from .sema import DogrulamaRaporu, Parametreler, dogrula

__all__ = [
    "Parametreler", "dogrula", "DogrulamaRaporu",
    "sku_profili", "siparis_ozeti", "abc_sinifla", "xyz_sinifla",
    "GunTipi", "KAZAN_GUN_TIPLERI", "KadroSonucu", "kadro_hesapla", "senaryolar", "bordro",
]
__version__ = "0.1.0"
