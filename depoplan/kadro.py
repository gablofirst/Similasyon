"""Analitik kadro ve ekipman modeli (Kazan v8.16 kadro simülasyonunun Python karşılığı).

  toplayıcı  = sipariş × satır/sipariş ÷ (toplama hızı × net saat)
  paketleme  = sipariş ÷ (paketleme hızı × net saat)
  hazır paket= sipariş × hp payı ÷ (HP hızı × net saat)
  araba      = ⌈sipariş × WIP ÷ (göz × doluluk) × pay⌉

Doğrusal model: sıkışma ve kuyruğu göstermez. Hücre başı kişi eşiği yalnız uyarı verir;
asıl yanıt kesikli olay simülasyonunda (sonraki modül) ve sahada pilot ölçümündedir.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .sema import Parametreler


@dataclass(frozen=True)
class GunTipi:
    ad: str
    carpan: float          # ortalama güne göre
    buyume: float = 1.0


# Kazan ikas 2026 gün tipleri: normal ay ×0,84, P95 ×1,6, rekor ×2,193; 2027 büyüme ×1,5
KAZAN_GUN_TIPLERI = [
    GunTipi("2026 normal", 0.84), GunTipi("2026 P95", 1.6),
    GunTipi("2027 normal", 0.84, 1.5), GunTipi("2027 P95", 1.6, 1.5),
    GunTipi("rekor", 2.193),
]


@dataclass
class KadroSonucu:
    gun_tipi: str
    siparis: float
    satir: float
    toplayici: float
    paketleme: float
    hazir_paket: float
    toplam: float
    hucre_basi: float
    m_kisi: float
    araba: int
    paket_istasyon_ihtiyaci: int
    hucre_durum: str        # rahat / sınırda / sıkışma
    istasyon_yeter: bool

    def sozluk(self) -> dict:
        return asdict(self)


def kadro_hesapla(ort_siparis: float, gun: GunTipi, p: Parametreler | None = None) -> KadroSonucu:
    p = p or Parametreler()
    o = ort_siparis * gun.carpan * gun.buyume
    sat = o * p.satir_siparis
    top = sat / (p.toplama_hizi * p.net_saat)
    pak = o / (p.paketleme_hizi * p.net_saat)
    hp = o * p.hp_payi / (p.hazir_paket_hizi * p.net_saat)
    hb = top / max(1, p.hucre_sayisi)
    araba = math.ceil(o * p.araba_wip / (p.araba_goz * p.araba_doluluk) * p.araba_pay)
    esik = p.hucre_basi_rahat_kisi
    durum = "sıkışma" if hb > esik * 1.25 else "sınırda" if hb > esik else "rahat"
    return KadroSonucu(
        gun_tipi=gun.ad, siparis=o, satir=sat, toplayici=top, paketleme=pak, hazir_paket=hp,
        toplam=top + pak + hp, hucre_basi=hb, m_kisi=p.hucre_dongu_m / max(hb, 0.01), araba=araba,
        paket_istasyon_ihtiyaci=math.ceil(pak), hucre_durum=durum, istasyon_yeter=math.ceil(pak) <= p.paket_istasyonu,
    )


def bordro(sahada: float, devam: float) -> int:
    """Sahada gereken kişiyi devam oranıyla bordroya çevirir (Kazan ölçülen devam %73)."""
    return math.ceil(sahada / devam)


def senaryolar(ort_siparis: float, gun_tipleri=KAZAN_GUN_TIPLERI, p: Parametreler | None = None) -> list[KadroSonucu]:
    return [kadro_hesapla(ort_siparis, g, p) for g in gun_tipleri]
