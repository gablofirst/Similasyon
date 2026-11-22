"""Süreç modeli: layout etkisi, öncelikli dağıtım, Kazan karşılaştırması ve JS motoru eşitliği."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from depoplan.surec import Bolge, Senaryo, Surec, dagit, hesapla, mesafe, referanslari_sabitle, senaryo_sozlukten

KOK = Path(__file__).resolve().parents[1]
SABLON = KOK / "app" / "sablonlar.json"


def test_kazan_eticaret_surec_modeliyle():
    """Kazan v8.16 2026 P95: toplama + paketleme + hazır paket = 40,5 kişi (layoutsuz, seyahat payı 0)."""
    o = 5291 * 1.6
    s = Senaryo("kazan p95", [
        Surec("t", "toplama", "eticaret", "satır", o * 1.762, 120),
        Surec("p", "paketleme", "eticaret", "sipariş", o, 71),
        Surec("h", "hazır paket", "eticaret", "sipariş", o, 140),
    ])
    assert hesapla(s)["ihtiyac"] == pytest.approx(40.5, abs=0.05)


def _iki_bolge(x_b):
    return [Bolge("a", "A", 0, 0, 10, 10), Bolge("b", "B", x_b, 0, 10, 10)]


def test_layout_yalniz_yurume_payini_olcekler():
    p = Surec("t", "taşıma", "giris", "palet", 75, 10, seyahat=0.5, kaynak="a", hedef="b")
    s = Senaryo("x", [p], _iki_bolge(40))
    referanslari_sabitle(s)
    assert p.ref_mesafe == 40
    assert hesapla(s)["ihtiyac"] == pytest.approx(1.0)          # 75 / 10 / 7,5
    s.bolgeler = _iki_bolge(20)                                   # mesafe yarıya iner
    r = hesapla(s)["satirlar"][0]
    assert r["carpan"] == pytest.approx(0.75)                     # 0,5 + 0,5 × 20/40
    assert r["ihtiyac"] == pytest.approx(0.75)


def test_bolge_ici_mesafe():
    bz = {"a": Bolge("a", "A", 0, 0, 26, 20)}
    assert mesafe(bz, "a", "a") == 23


def test_dagit_oncelik_ve_adim():
    # öncelik 1 tam karşılanır (yarım FTE'ye yuvarlanmış), kalan öncelik 3'e
    n = dagit([10.0, 0.3, 15.0], [1, 1, 3], 12)
    assert n == [10.0, 0.5, 1.5]
    assert sum(dagit([10.0, 0.3, 15.0], [1, 1, 3], 30)) == 30   # fazla kişi orantılı eklenir


def test_dagit_yetmeyen_seviyede_orantili():
    assert dagit([6.0, 2.0], [1, 1], 4) == [3.0, 1.0]


def test_elle_atama_sabit_kalir():
    s = Senaryo("x", [Surec("a", "A", "vas", "adet", 750, 10, atanan=3), Surec("b", "B", "vas", "adet", 750, 10)],
                toplam_kisi=10)
    r = {x["id"]: x for x in hesapla(s)["satirlar"]}
    assert r["a"]["atanan"] == 3 and r["b"]["atanan"] == 7
    assert r["a"]["oran"] == pytest.approx(0.3)


def test_bolge_kalabalik_uyarisi():
    b = [Bolge("z", "Z", 0, 0, 10, 10, maks_kisi=5)]
    s = Senaryo("x", [Surec("a", "A", "eticaret", "satır", 7500, 100, kaynak="z", hedef="z")], b)
    assert hesapla(s)["bolge_uyari"] == ["z"]   # 10 kişi > 5


@pytest.fixture(scope="module")
def sablon():
    return json.loads(SABLON.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ornek(sablon):
    return next(x for x in sablon["sektorler"] if x["id"] == "fmcg")["senaryolar"]


def test_kayip_ve_hacim_carpani():
    p = Surec("t", "toplama", "eticaret", "satır", 900, 120, kayip=0.2)
    s = Senaryo("x", [p])
    assert hesapla(s)["ihtiyac"] == pytest.approx(900 / 96 / 7.5)        # 120 × 0,8 = 96
    s.hacim_carpani = 1.5
    assert hesapla(s)["satirlar"][0]["hacim"] == 1350


def test_sablonlar_tutarli(sablon):
    akislar = set(sablon["akislar"])
    assert len(sablon["sektorler"]) >= 5 and len(sablon["kutuphane"]) >= 20
    for k in sablon["kutuphane"]:
        assert k["akis"] in akislar and k["kaynak_tip"] in sablon["bolge_tipleri"]
    for sk in sablon["sektorler"]:
        for s in sk["senaryolar"]:
            W, H = s["bina"]["w"], s["bina"]["h"]
            ids = {b["id"] for b in s["bolgeler"]}
            for b in s["bolgeler"]:
                assert b["tip"] in sablon["bolge_tipleri"]
                assert 0 <= b["x"] and b["x"] + b["w"] <= W and 0 <= b["y"] and b["y"] + b["h"] <= H, (sk["id"], b["id"])
            bs = s["bolgeler"]
            for i in range(len(bs)):
                for j in range(i + 1, len(bs)):
                    a, c = bs[i], bs[j]
                    ust = min(a["x"] + a["w"], c["x"] + c["w"]) - max(a["x"], c["x"]) > 1e-6 and \
                        min(a["y"] + a["h"], c["y"] + c["h"]) - max(a["y"], c["y"]) > 1e-6
                    assert not ust, (sk["id"], s["ad"], a["id"], c["id"])
            for p in s["surecler"]:
                assert p["akis"] in akislar and p["kaynak"] in ids and p["hedef"] in ids, (sk["id"], p["id"])
            r = hesapla(senaryo_sozlukten(s))
            assert r["ihtiyac"] > 0


def test_ornek_senaryolar(ornek):
    r = [hesapla(senaryo_sozlukten(s)) for s in ornek]
    assert r[0]["mod"] == "ihtiyac" and r[0]["ihtiyac"] == pytest.approx(42.7, abs=0.05)
    assert r[1]["atanan"] == 30 and r[2]["atanan"] == 40
    # 30 kişi: çıkış akışları tam, VAS durur
    assert r[1]["akislar"]["eticaret"]["karsilama"] == 1 and r[1]["akislar"]["b2b"]["karsilama"] == 1
    assert r[1]["akislar"]["vas"]["karsilama"] < 0.05
    # layout + süreç değişikliği ihtiyacı düşürür, VAS karşılaması artar
    assert r[3]["ihtiyac"] < r[2]["ihtiyac"]
    assert r[3]["akislar"]["vas"]["karsilama"] > r[2]["akislar"]["vas"]["karsilama"]


@pytest.mark.skipif(shutil.which("node") is None, reason="node yok")
def test_js_motoru_python_ile_ayni(sablon):
    js = (
        "const m=require(process.argv[1]);const d=require(process.argv[2]);"
        "const ss=d.sektorler.flatMap(k=>k.senaryolar);ss.push(Object.assign({},ss[1],{hacim_carpani:1.3,"
        "surecler:ss[1].surecler.map(p=>Object.assign({},p,{kayip:0.2}))}));"
        "console.log(JSON.stringify(ss.map(s=>m.hesapla(s))));"
    )
    out = subprocess.run(["node", "-e", js, str(KOK / "app" / "motor.js"), str(SABLON)],
                         capture_output=True, text=True, check=True).stdout
    tum = [s for k in sablon["sektorler"] for s in k["senaryolar"]]
    ek = dict(tum[1], hacim_carpani=1.3, surecler=[dict(p, kayip=0.2) for p in tum[1]["surecler"]])
    tum.append(ek)
    jrs = json.loads(out)
    assert len(jrs) == len(tum)
    for jr, s in zip(jrs, tum):
        pr = hesapla(senaryo_sozlukten(s))
        assert jr["ihtiyac"] == pytest.approx(pr["ihtiyac"]) and jr["bordro"] == pr["bordro"]
        for a, b in zip(jr["satirlar"], pr["satirlar"]):
            assert a["id"] == b["id"]
            for k in ("mesafe", "carpan", "ihtiyac", "atanan", "oran"):
                assert a[k] == pytest.approx(b[k]), (s["ad"], a["id"], k)
        for k, v in pr["akislar"].items():
            assert jr["akislar"][k]["karsilama"] == pytest.approx(v["karsilama"])
            assert jr["akislar"][k]["darbogaz"] == v["darbogaz"]
