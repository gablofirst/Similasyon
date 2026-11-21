"""Genel davranış: sentetik veriyle profil, doğrulama ve kit açma."""
import pandas as pd
import pytest

from depoplan import dogrula, siparis_ozeti, sku_profili
from depoplan.kit import ac, bom_sozlugu, siparisi_ac


@pytest.fixture
def siparis():
    # 4 gün; S1 tekli, S2 iki SKU, S3 aynı SKU iki satır, 21.01'de satış yok
    return pd.DataFrame(
        {
            "siparis_no": ["S1", "S2", "S2", "S3", "S3", "S4"],
            "tarih": ["2026-01-20 10:00", "2026-01-20 11:00", "2026-01-20 11:00", "2026-01-22", "2026-01-22", "2026-01-23"],
            "sku": ["A", "A", "B", "C", "C", "A"],
            "adet": [1, 2, 1, 1, 2, 5],
        }
    )


def test_profil_temel(siparis):
    p = sku_profili(siparis)
    a = p.loc["A"]
    assert a.toplam_adet == 8 and a.toplama_satiri == 3 and a.siparis == 3
    assert a.tekli_siparis == 2  # S1 ve S4
    assert p.loc["C"].toplama_satiri == 1  # aynı siparişte birleşti
    assert p.loc["C"].toplam_adet == 3
    # 4 takvim günü (21.01 sıfır dahil): A günlük ort = 8/4
    assert a.gunluk_ort == pytest.approx(2.0)
    assert set(p["ABC_adet"]) <= {"A", "B", "C"}


def test_siparis_ozeti(siparis):
    o = siparis_ozeti(siparis)
    assert o["siparis"] == 4 and o["gun"] == 4
    assert o["satir"] == 5  # S2 iki satır, S3 tek satır
    assert o["tekli_pay"] == pytest.approx(0.75)
    assert o["gunluk_maks"] == 2


def test_tarih_karisik_bicim():
    from depoplan.sema import tarih_coz

    t = tarih_coz(pd.Series(["2026-01-05 10:00", "05.01.2026", "05/01/2026 14:30", "bozuk"]))
    assert [x.strftime("%Y-%m-%d") for x in t[:3]] == ["2026-01-05"] * 3
    assert pd.isna(t[3])


def test_dogrulama_eksik_sutun():
    r = dogrula(pd.DataFrame({"sku": ["A"]}))
    assert not r.gecerli
    assert "zorunlu sütun yok" in r.bulgular[0].mesaj


def test_dogrulama_uyarilar(siparis):
    sku = pd.DataFrame({"sku": ["A", "B"], "en_cm": [10, None], "boy_cm": [10, 5], "yukseklik_cm": [10, 5]})
    r = dogrula(siparis, sku)
    assert r.gecerli
    m = " | ".join(b.mesaj for b in r.bulgular)
    assert "ana veride olmayan SKU" in m  # C yok
    assert "ölçüsü eksik" in m           # B en_cm boş
    assert "ağırlık yok" in m
    assert "günlük veri" in m            # 4 gün < 90


def test_kit_cok_seviyeli():
    bom = pd.DataFrame({"kit_sku": ["K", "K", "P"], "bilesen_sku": ["P", "X", "Y"], "miktar": [2, 1, 3]})
    assert sorted(ac("K", 1, bom_sozlugu(bom))) == [("X", 1.0), ("Y", 6.0)]


def test_kit_modlari():
    bom = pd.DataFrame({"kit_sku": ["K", "K", "H", "B32"], "bilesen_sku": ["X", "Y", "X", "Z"], "miktar": [1, 1, 1, 36]})
    s = pd.DataFrame({"siparis_no": ["1", "1", "2"], "sku": ["K", "H", "B32"], "adet": [1, 1, 1]})
    out = siparisi_ac(s, bom, hazir={"H"}, sabit_satir={"B32": 3})
    assert sorted(out[out.siparis_no == "1"].sku) == ["H", "X", "Y"]  # K açıldı, H hazır kit
    b = out[out.sku == "B32"].iloc[0]
    assert b.toplama_satir_agirlik == 3  # Kazan: 32'li bar = 3 satır
