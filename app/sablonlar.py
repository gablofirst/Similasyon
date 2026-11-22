"""Sektör şablonları ve süreç kütüphanesi → app/sablonlar.json

Uygulama açılışta "sektör seç" ile bu şablonlardan birini yükler; kullanıcı süreç ekler/çıkarır,
hacim ve verimi kendi ölçümüyle değiştirir. Tüm rakamlar ÖRNEK başlangıç değerleridir (sektör
kıyaslaması değildir); hiçbir müşterinin verisi değildir.

Çalıştırma: python3 app/sablonlar.py
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from depoplan.surec import Bolge, mesafe  # noqa: E402

AKISLAR = {
    "giris": "Giriş",
    "ic": "Depo içi",
    "eticaret": "E-ticaret çıkış",
    "b2b": "B2B / bayi çıkış",
    "iade": "İade",
    "vas": "VAS",
}

# Bölge tipleri (renk ve süreç önerisi için)
BOLGE_TIPLERI = {
    "rampa": "Rampa / kapı", "kabul": "Mal kabul", "kalite": "Kalite / karantina", "rezerv": "Rezerv stok",
    "toplama": "Toplama alanı", "paket": "Paketleme", "kontrol": "Kontrol / kantar", "sevk": "Sevk / kargo",
    "tampon": "Tampon / konsolidasyon", "vas": "VAS", "iade": "İade", "soguk": "Soğuk oda", "ofis": "Ofis / sosyal",
}

# Süreç kütüphanesi: "+ Süreç ekle" listesi. verim = birim / adam-saat (örnek), seyahat = yürüme payı
KUTUPHANE = [
    # id, ad, akış, birim, verim, seyahat, öncelik, önerilen kaynak tipi, önerilen hedef tipi, açıklama
    ("kabul", "Mal kabul (boşaltma + sayım)", "giris", "palet", 10, 0.30, 2, "rampa", "kabul", "Araçtan indirme, irsaliye karşılaştırma"),
    ("kabul_koli", "Mal kabul (koli bazlı)", "giris", "koli", 45, 0.30, 2, "rampa", "kabul", "Parsiyel/koli gelen ürün"),
    ("kalite", "Kalite kontrol", "giris", "adet", 350, 0.05, 2, "kabul", "kalite", "Numune veya %100 kontrol"),
    ("etiket", "Etiketleme / WMS kaydı", "giris", "palet", 40, 0.10, 2, "kabul", "kabul", "Palet etiketi, lot/SKT kaydı"),
    ("yerlestirme", "Yerleştirme (put-away)", "giris", "palet", 12, 0.60, 2, "kabul", "rezerv", "Forklift/reach truck ile rafa"),
    ("xdock", "X-dock aktarma", "giris", "palet", 15, 0.50, 1, "kabul", "tampon", "Stoğa girmeden sevke"),
    ("besleme", "Toplama besleme (replenishment)", "ic", "koli", 50, 0.55, 1, "rezerv", "toplama", "Rezervden toplama gözüne"),
    ("abc", "Yer değiştirme (ABC)", "ic", "palet", 5, 0.60, 3, "rezerv", "rezerv", "Hıza göre lokasyon düzeltme"),
    ("sayim", "Döngüsel sayım", "ic", "lokasyon", 60, 0.50, 3, "rezerv", "rezerv", "Periyodik stok sayımı"),
    ("palet_topla", "Tam palet toplama", "b2b", "palet", 14, 0.60, 1, "rezerv", "tampon", "B2B tam palet çıkış"),
    ("koli_topla", "Koli toplama", "b2b", "koli", 110, 0.50, 1, "toplama", "tampon", "Bayi/market siparişi"),
    ("satir_topla", "E-ticaret toplama (satır)", "eticaret", "satır", 120, 0.55, 1, "toplama", "toplama", "Araba/hücre/zone toplama"),
    ("toplu_topla", "Toplu toplama (batch)", "eticaret", "satır", 180, 0.60, 1, "toplama", "toplama", "Çok siparişe birlikte toplama"),
    ("putwall", "Put-wall / sorter ayrıştırma", "eticaret", "adet", 600, 0.10, 1, "tampon", "paket", "Toplu toplamadan siparişe ayırma"),
    ("paket", "Paketleme", "eticaret", "sipariş", 71, 0.10, 1, "paket", "kontrol", "Kutu, dolgu, fatura"),
    ("kantar", "Kantar / kontrol", "eticaret", "koli", 450, 0.15, 1, "kontrol", "sevk", "Tartım, okutma"),
    ("kargo", "Kargo ayırma ve teslim", "eticaret", "koli", 400, 0.40, 1, "sevk", "sevk", "Taşıyıcıya göre ayırma"),
    ("konsol", "Konsolidasyon / streç", "b2b", "palet", 10, 0.20, 1, "tampon", "tampon", "Rota/müşteri paleti"),
    ("yukle", "Sevk yükleme", "b2b", "palet", 20, 0.40, 1, "tampon", "rampa", "Araca yükleme"),
    ("iade", "İade kabul ve kontrol", "iade", "adet", 80, 0.15, 2, "iade", "iade", "Sınıflandırma: satılabilir / hurda"),
    ("iade_yer", "İade yerleştirme", "iade", "adet", 220, 0.50, 3, "iade", "toplama", "Satılabilir iadeyi stoğa"),
    ("vas", "VAS üretim", "vas", "adet", 160, 0.10, 3, "vas", "vas", "Paketleme, etiket, set, shrink"),
    ("vas_besle", "VAS malzeme besleme", "vas", "palet", 8, 0.60, 3, "rezerv", "vas", "Hatlara malzeme"),
    ("kit", "Kit kurma", "vas", "kit", 30, 0.20, 3, "vas", "vas", "Karma koli / set hazırlama"),
]


def _bolgeler(liste):
    return [dict(id=i, ad=a, tip=t, x=x, y=y, w=w, h=h, maks_kisi=m) for i, a, t, x, y, w, h, m in liste]


def _surecler(bolgeler, liste):
    bz = {b["id"]: Bolge(**{k: b[k] for k in ("id", "ad", "x", "y", "w", "h", "maks_kisi")}) for b in bolgeler}
    out = []
    for i, a, k, u, v, r, sey, src, dst, o in liste:
        out.append(dict(id=i, ad=a, akis=k, birim=u, hacim=v, verim=r, seyahat=sey, kaynak=src, hedef=dst,
                        ref_mesafe=round(mesafe(bz, src, dst), 3), aktif=True, atanan=None, oncelik=o, kayip=0.0))
    return out


def _senaryo(ad, bina, bolgeler, surecler, **kw):
    s = dict(ad=ad, net_saat=7.5, vardiya=1, devam=0.85, toplam_kisi=None, atama_adimi=0.5, hacim_carpani=1.0,
             bina=bina, bolgeler=bolgeler, surecler=_surecler(bolgeler, surecler), not_="")
    s.update(kw)
    return s


# ------------------------------------------------------------------ 1. FMCG · e-ticaret + B2B
def fmcg():
    bina = {"w": 120, "h": 60}
    b = _bolgeler([
        ("rampa", "Rampa", "rampa", 0, 0, 6, 40, None),
        ("kabul", "Mal kabul", "kabul", 6, 0, 16, 14, 6),
        ("kalite", "Kalite / iade", "kalite", 6, 14, 16, 8, None),
        ("xdock", "X-dock tamponu", "tampon", 6, 22, 16, 8, None),
        ("sevk_tampon", "B2B sevk tamponu", "tampon", 6, 30, 16, 10, 4),
        ("rezerv", "Rezerv raf (palet)", "rezerv", 24, 0, 56, 30, None),
        ("b2b", "B2B toplama yüzü", "toplama", 24, 30, 22, 8, 4),
        ("vas", "VAS hatları", "vas", 82, 0, 38, 30, 16),
        ("toplama", "E-ticaret toplama", "toplama", 48, 36, 26, 20, 10),
        ("paket", "Paketleme", "paket", 76, 36, 18, 20, 14),
        ("kantar", "Kantar / kontrol", "kontrol", 96, 36, 8, 20, 3),
        ("sevk", "Kargo sevk", "sevk", 106, 36, 14, 24, 4),
        ("ofis", "Ofis / sosyal", "ofis", 0, 44, 22, 16, None),
    ])
    p = [
        ("kabul", "Mal kabul", "giris", "palet", 60, 10, 0.30, "rampa", "kabul", 2),
        ("yerlestirme", "Yerleştirme", "giris", "palet", 55, 12, 0.60, "kabul", "rezerv", 2),
        ("xdock", "X-dock aktarma", "giris", "palet", 5, 15, 0.50, "kabul", "sevk_tampon", 1),
        ("besleme", "Toplama besleme", "ic", "koli", 350, 50, 0.55, "rezerv", "toplama", 1),
        ("abc", "Yer değiştirme (ABC)", "ic", "palet", 12, 5, 0.60, "rezerv", "rezerv", 3),
        ("etopla", "E-ticaret toplama", "eticaret", "satır", 9000, 120, 0.55, "toplama", "toplama", 1),
        ("paket", "Paketleme", "eticaret", "sipariş", 5100, 71, 0.10, "paket", "kantar", 1),
        ("kantar", "Kantar / kontrol", "eticaret", "koli", 5100, 450, 0.15, "kantar", "sevk", 1),
        ("kargo", "Kargo ayırma ve teslim", "eticaret", "koli", 5100, 400, 0.40, "sevk", "sevk", 1),
        ("b2btopla", "B2B toplama", "b2b", "koli", 900, 80, 0.45, "b2b", "sevk_tampon", 1),
        ("b2byukle", "B2B yükleme", "b2b", "palet", 30, 12, 0.50, "sevk_tampon", "rampa", 1),
        ("vas", "VAS üretim", "vas", "adet", 18000, 160, 0.10, "vas", "vas", 3),
        ("vasbesle", "VAS malzeme besleme", "vas", "palet", 20, 8, 0.60, "rezerv", "vas", 3),
    ]
    a = _senaryo("İhtiyaç · mevcut layout", bina, b, p, not_="Hacim ve verimden süreç bazlı kişi ihtiyacı.")
    s30 = copy.deepcopy(a)
    s30.update(ad="30 kişi", toplam_kisi=30, not_="30 kişi önceliğe göre dağıtıldı: çıkış süreçleri önce, VAS ve ABC en son.")
    s40 = copy.deepcopy(a)
    s40.update(ad="40 kişi", toplam_kisi=40, not_="40 kişi önceliğe göre dağıtıldı.")
    d = copy.deepcopy(s40)
    d.update(ad="40 kişi · kompakt toplama, kantar pakette",
             not_="Layout: toplama alanı 26 × 20 → 18 × 16 m (A ürünler öne), paketleme toplamaya bitişik, kargo sevk "
                  "paketlemenin yanına. Süreç: ayrı kantar kaldırıldı, tartım paket masasında (paketleme verimi 71 → 68).")
    bz = {z["id"]: z for z in d["bolgeler"]}
    bz["toplama"].update(x=56, y=38, w=18, h=16)
    bz["paket"].update(x=76, y=36, w=18, h=20)
    bz["kantar"].update(x=96, y=36, w=4, h=20)
    bz["sevk"].update(x=100, y=36, w=20, h=24)
    sp = {x["id"]: x for x in d["surecler"]}
    sp["kantar"]["aktif"] = False
    sp["paket"].update(verim=68, hedef="sevk")   # ref_mesafe aynı kalır: verim eski layoutta ölçüldü
    return [a, s30, s40, d]


# ------------------------------------------------------------------ 2. 3PL / çok müşterili depo
def lojistik3pl():
    bina = {"w": 140, "h": 70}
    b = _bolgeler([
        ("rampa_g", "Giriş rampası", "rampa", 0, 0, 6, 36, None),
        ("kabul", "Mal kabul", "kabul", 6, 0, 18, 18, 8),
        ("kalite", "Karantina", "kalite", 6, 18, 18, 8, None),
        ("xdock", "X-dock alanı", "tampon", 6, 26, 18, 12, 4),
        ("rezerv", "Rezerv raf (palet)", "rezerv", 26, 0, 88, 44, None),
        ("koli_topla", "Koli toplama alanı", "toplama", 26, 47, 40, 20, 10),
        ("konsol", "Konsolidasyon", "tampon", 68, 47, 22, 20, 6),
        ("vas", "VAS", "vas", 92, 47, 22, 20, 10),
        ("sevk_tampon", "Sevk tamponu", "tampon", 116, 40, 18, 30, 6),
        ("rampa_c", "Çıkış rampası", "rampa", 134, 0, 6, 70, None),
        ("ofis", "Ofis / sosyal", "ofis", 0, 42, 24, 28, None),
    ])
    p = [
        ("kabul", "Mal kabul", "giris", "palet", 180, 12, 0.30, "rampa_g", "kabul", 2),
        ("etiket", "Etiketleme / WMS kaydı", "giris", "palet", 180, 40, 0.10, "kabul", "kabul", 2),
        ("yerlestirme", "Yerleştirme", "giris", "palet", 160, 14, 0.60, "kabul", "rezerv", 2),
        ("xdock", "X-dock aktarma", "giris", "palet", 20, 18, 0.50, "xdock", "sevk_tampon", 1),
        ("besleme", "Toplama besleme", "ic", "koli", 600, 60, 0.50, "rezerv", "koli_topla", 1),
        ("palet_topla", "Tam palet toplama", "b2b", "palet", 90, 14, 0.60, "rezerv", "sevk_tampon", 1),
        ("koli_topla", "Koli toplama", "b2b", "koli", 2400, 110, 0.50, "koli_topla", "konsol", 1),
        ("konsol", "Konsolidasyon / streç", "b2b", "palet", 70, 10, 0.20, "konsol", "sevk_tampon", 1),
        ("yukle", "Sevk yükleme", "b2b", "palet", 180, 22, 0.40, "sevk_tampon", "rampa_c", 1),
        ("vas", "VAS (etiket, set)", "vas", "adet", 6000, 220, 0.10, "vas", "vas", 3),
        ("sayim", "Döngüsel sayım", "ic", "lokasyon", 300, 60, 0.50, "rezerv", "rezerv", 3),
        ("abc", "Yer değiştirme (ABC)", "ic", "palet", 25, 6, 0.60, "rezerv", "rezerv", 3),
    ]
    return [_senaryo("İhtiyaç · mevcut layout", bina, b, p)]


# ------------------------------------------------------------------ 3. Moda / tekstil e-ticaret
def moda():
    bina = {"w": 100, "h": 60}
    b = _bolgeler([
        ("rampa", "Rampa", "rampa", 0, 0, 6, 30, None),
        ("kabul", "Mal kabul", "kabul", 6, 0, 16, 14, 6),
        ("kalite", "Kalite kontrol", "kalite", 6, 14, 16, 10, 6),
        ("iade", "İade alanı", "iade", 6, 24, 16, 14, 10),
        ("rezerv", "Rezerv (koli)", "rezerv", 24, 0, 46, 28, None),
        ("vas", "VAS (etiket, askı)", "vas", 72, 0, 28, 28, 8),
        ("toplama", "Toplama (raf / mezanin)", "toplama", 24, 30, 40, 26, 14),
        ("putwall", "Put-wall", "tampon", 66, 30, 12, 26, 6),
        ("paket", "Paketleme", "paket", 80, 30, 12, 26, 12),
        ("sevk", "Kargo sevk", "sevk", 92, 30, 8, 30, 4),
        ("ofis", "Ofis / sosyal", "ofis", 0, 40, 22, 20, None),
    ])
    p = [
        ("kabul", "Mal kabul (koli)", "giris", "koli", 400, 45, 0.30, "rampa", "kabul", 2),
        ("kalite", "Kalite kontrol", "giris", "adet", 6000, 350, 0.05, "kabul", "kalite", 2),
        ("yerlestirme", "Yerleştirme (adet)", "giris", "adet", 6000, 250, 0.50, "kalite", "toplama", 2),
        ("besleme", "Toplama besleme", "ic", "koli", 250, 40, 0.50, "rezerv", "toplama", 1),
        ("topla", "Toplu toplama", "eticaret", "satır", 12000, 180, 0.60, "toplama", "toplama", 1),
        ("putwall", "Put-wall ayrıştırma", "eticaret", "adet", 13000, 600, 0.10, "putwall", "paket", 1),
        ("paket", "Paketleme", "eticaret", "sipariş", 6500, 90, 0.10, "paket", "sevk", 1),
        ("kargo", "Kargo ayırma ve teslim", "eticaret", "koli", 6500, 500, 0.40, "sevk", "sevk", 1),
        ("iade", "İade kabul ve kontrol", "iade", "adet", 1800, 80, 0.15, "iade", "iade", 2),
        ("iade_yer", "İade yerleştirme", "iade", "adet", 1500, 220, 0.50, "iade", "toplama", 3),
        ("vas", "VAS (etiket, askı)", "vas", "adet", 3000, 250, 0.10, "vas", "vas", 3),
    ]
    return [_senaryo("İhtiyaç · mevcut layout", bina, b, p)]


# ------------------------------------------------------------------ 4. Gıda / soğuk zincir dağıtım
def gida():
    bina = {"w": 120, "h": 60}
    b = _bolgeler([
        ("rampa_g", "Giriş rampası", "rampa", 0, 0, 6, 30, None),
        ("kabul", "Mal kabul (+4 °C)", "kabul", 6, 0, 16, 16, 6),
        ("soguk", "Soğuk oda rezerv (+4 °C)", "soguk", 24, 0, 40, 30, None),
        ("dondurucu", "Dondurucu (−18 °C)", "soguk", 66, 0, 20, 30, 4),
        ("kuru", "Kuru rezerv", "rezerv", 88, 0, 32, 30, None),
        ("koli_topla", "Koli toplama (+4 °C)", "toplama", 24, 32, 50, 22, 14),
        ("konsol", "Rota konsolidasyon", "tampon", 76, 32, 24, 22, 8),
        ("iade", "İade", "iade", 100, 32, 14, 12, 3),
        ("sevk_tampon", "Sevk tamponu", "tampon", 100, 44, 14, 16, 4),
        ("sevk_rampa", "Sevk rampası", "rampa", 114, 32, 6, 28, None),
        ("ofis", "Ofis / sosyal", "ofis", 0, 40, 22, 20, None),
    ])
    p = [
        ("kabul", "Mal kabul + SKT kontrol", "giris", "palet", 120, 14, 0.30, "rampa_g", "kabul", 2),
        ("yerlestirme", "Yerleştirme", "giris", "palet", 110, 16, 0.60, "kabul", "soguk", 2),
        ("besleme", "Toplama besleme", "ic", "koli", 900, 70, 0.50, "soguk", "koli_topla", 1),
        ("topla", "Koli toplama (soğuk)", "b2b", "koli", 6000, 150, 0.55, "koli_topla", "konsol", 1),
        ("donuk_topla", "Dondurucu toplama", "b2b", "koli", 1200, 100, 0.50, "dondurucu", "konsol", 1),
        ("kuru_topla", "Kuru ürün toplama", "b2b", "koli", 1500, 140, 0.55, "kuru", "konsol", 1),
        ("konsol", "Rota konsolidasyon / streç", "b2b", "palet", 140, 12, 0.20, "konsol", "sevk_tampon", 1),
        ("yukle", "Araç yükleme", "b2b", "palet", 140, 20, 0.40, "sevk_tampon", "sevk_rampa", 1),
        ("iade", "İade ve imha ayrımı", "iade", "koli", 300, 60, 0.20, "iade", "iade", 2),
        ("sayim", "Sayım / SKT kontrol", "ic", "lokasyon", 200, 50, 0.50, "soguk", "soguk", 3),
    ]
    return [_senaryo("İhtiyaç · mevcut layout", bina, b, p)]


# ------------------------------------------------------------------ 5. Yedek parça / B2B dağıtım
def yedek_parca():
    bina = {"w": 100, "h": 60}
    b = _bolgeler([
        ("rampa", "Rampa", "rampa", 0, 0, 6, 28, None),
        ("kabul", "Mal kabul", "kabul", 6, 0, 16, 14, 6),
        ("kalite", "Kalite / iade", "kalite", 6, 14, 16, 10, 4),
        ("rezerv", "Rezerv (palet)", "rezerv", 24, 0, 40, 26, None),
        ("vas", "Kitleme / VAS", "vas", 66, 0, 34, 26, 8),
        ("raf", "Küçük parça raf / mezanin", "toplama", 24, 28, 40, 28, 16),
        ("paket", "Paketleme", "paket", 66, 28, 16, 20, 10),
        ("kontrol", "Kontrol", "kontrol", 66, 48, 16, 8, 3),
        ("sevk", "Sevk", "sevk", 84, 28, 16, 32, 4),
        ("ofis", "Ofis / sosyal", "ofis", 0, 36, 22, 24, None),
    ])
    p = [
        ("kabul", "Mal kabul (koli)", "giris", "koli", 300, 40, 0.30, "rampa", "kabul", 2),
        ("yerlestirme", "Yerleştirme (satır)", "giris", "satır", 1500, 90, 0.60, "kabul", "raf", 2),
        ("besleme", "Raf besleme", "ic", "koli", 150, 30, 0.50, "rezerv", "raf", 1),
        ("topla", "Parça toplama", "b2b", "satır", 4000, 70, 0.65, "raf", "raf", 1),
        ("paket", "Paketleme", "b2b", "sipariş", 1100, 30, 0.10, "paket", "kontrol", 1),
        ("kontrol", "Kontrol / tartım", "b2b", "koli", 1100, 120, 0.10, "kontrol", "sevk", 1),
        ("yukle", "Sevk / teslim", "b2b", "koli", 1100, 200, 0.40, "sevk", "sevk", 1),
        ("iade", "İade kontrol", "iade", "satır", 150, 25, 0.20, "kalite", "kalite", 2),
        ("kit", "Kit kurma", "vas", "kit", 200, 12, 0.20, "vas", "vas", 3),
        ("sayim", "Döngüsel sayım", "ic", "lokasyon", 400, 80, 0.40, "raf", "raf", 3),
    ]
    return [_senaryo("İhtiyaç · mevcut layout", bina, b, p)]


SEKTORLER = [
    ("fmcg", "FMCG · e-ticaret + B2B", "Gıda takviyesi, kozmetik, temizlik: güçlü B2C, bayi/market B2B, VAS hatları.", fmcg),
    ("3pl", "3PL · çok müşterili depo", "Palet ağırlıklı giriş, x-dock, koli ve palet toplama, rampa yükleme.", lojistik3pl),
    ("moda", "Moda / tekstil e-ticaret", "Adet bazlı toplu toplama, put-wall, yüksek iade.", moda),
    ("gida", "Gıda · soğuk zincir dağıtım", "+4 °C / −18 °C bölgeler, SKT kontrolü, rota bazlı konsolidasyon.", gida),
    ("parca", "Yedek parça / B2B dağıtım", "Çok SKU, küçük parça rafı, kitleme, sipariş başı düşük adet.", yedek_parca),
]


def uret():
    return {
        "surum": 1,
        "akislar": AKISLAR,
        "bolge_tipleri": BOLGE_TIPLERI,
        "kutuphane": [dict(id=i, ad=a, akis=k, birim=u, verim=v, seyahat=s, oncelik=o, kaynak_tip=kt, hedef_tip=ht, aciklama=ac)
                      for i, a, k, u, v, s, o, kt, ht, ac in KUTUPHANE],
        "sektorler": [dict(id=i, ad=a, aciklama=ac, senaryolar=f()) for i, a, ac, f in SEKTORLER],
    }


if __name__ == "__main__":
    out = Path(__file__).with_name("sablonlar.json")
    out.write_text(json.dumps(uret(), ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)
