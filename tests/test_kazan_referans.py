"""Kazan referans vakası: paket, claude.ai'de elle hesaplanan Kazan sonuçlarını yeniden üretmeli.

Kaynaklar: 02_Claude_Notlari/Kazan_Devam_Notu_v8.16.md (§ v8.16 doğrulama) ve
03_Veri_ikas_2026/SKU_Profil.csv (ikas 2026 Oca–Eki, 814 SKU).
"""
from pathlib import Path

import pandas as pd
import pytest

from depoplan import KAZAN_GUN_TIPLERI, Parametreler, abc_sinifla, bordro, kadro_hesapla, senaryolar, xyz_sinifla
from depoplan.kadro import GunTipi

KOK = Path(__file__).resolve().parents[1]
SKU_PROFIL = KOK / "03_Veri_ikas_2026" / "SKU_Profil.csv"
KAZAN_ORT = 5291  # sipariş/gün, ikas 2026 Oca–Eki


@pytest.fixture(scope="module")
def profil():
    if not SKU_PROFIL.exists():
        pytest.skip("Kazan SKU profili yok")
    return pd.read_csv(SKU_PROFIL, dtype={"sku": str})


# ------------------------------------------------------------ ABC / XYZ kuralları
def test_abc_adet_kazan_ile_ayni(profil):
    sinif, kum = abc_sinifla(profil["toplam_adet"])
    assert (sinif == profil["ABC_adet"]).all()
    assert kum.round(6).equals(profil["kum_pay_adet"].round(6))


def test_abc_satir_kazan_ile_ayni(profil):
    sinif, _ = abc_sinifla(profil["toplama_satiri"])
    farkli = (sinif != profil["ABC_satir(toplama_sikligi)"]).sum()
    assert farkli == 0, f"{farkli} SKU farklı sınıfta"


def test_xyz_kazan_ile_ayni(profil):
    assert (xyz_sinifla(profil["haftalik_cv"]) == profil["XYZ"]).all()


def test_sinif_dagilimi(profil):
    sinif, _ = abc_sinifla(profil["toplam_adet"])
    assert sinif.value_counts().to_dict() == {"C": 518, "B": 177, "A": 119}


# ------------------------------------------------------------ kadro modeli (v8.16 doğrulaması)
@pytest.mark.parametrize(
    "gun, toplam, araba, hucre_basi",
    [
        (GunTipi("2026 P95", 1.6), 40.5, 30, 8.3),
        (GunTipi("2027 P95", 1.6, 1.5), 60.8, 45, 12.4),
    ],
)
def test_kadro_v816(gun, toplam, araba, hucre_basi):
    r = kadro_hesapla(KAZAN_ORT, gun)
    assert r.toplam == pytest.approx(toplam, abs=0.05)
    assert r.araba == araba
    assert r.hucre_basi == pytest.approx(hucre_basi, abs=0.05)


def test_2027_p95_darbogaz():
    """v8.6 sonucu: 2027 P95'te göz değil insan yoğunluğu darboğaz (hücre sıkışma, paketleme 24 > 16)."""
    r = kadro_hesapla(KAZAN_ORT, GunTipi("2027 P95", 1.6, 1.5))
    assert r.hucre_durum == "sıkışma"
    assert r.paket_istasyon_ihtiyaci == 24
    assert not r.istasyon_yeter


def test_2026_normal_gun_sigiyor():
    r = kadro_hesapla(KAZAN_ORT, GunTipi("2026 normal", 0.84))
    assert r.hucre_durum == "rahat" and r.istasyon_yeter


def test_ucuncu_hucre_secenegi():
    """Seçenek B: 3. hücre + 8 istasyon 2027 P95'i karşılar."""
    p = Parametreler(hucre_sayisi=3, paket_istasyonu=24)
    r = kadro_hesapla(KAZAN_ORT, GunTipi("2027 P95", 1.6, 1.5), p)
    assert r.istasyon_yeter
    assert r.hucre_basi == pytest.approx(8.3, abs=0.05)


def test_bordro_devam():
    assert bordro(40.5, 0.73) == 56


def test_senaryo_seti():
    assert [s.gun_tipi for s in senaryolar(KAZAN_ORT)] == [g.ad for g in KAZAN_GUN_TIPLERI]
