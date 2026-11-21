# depoplan · veri şeması v0.1

Her şirketten istenen girdi. Yalnız ilk tablo zorunlu; diğerleri hesapları derinleştirir.
Kod karşılığı: `depoplan/sema.py`. Doğrulama: `depoplan.dogrula(siparis, sku, bom)` → bulgu tablosu (hata / uyarı).

## 1. `siparis_satiri` (zorunlu)

Bir satır = bir siparişteki bir ürün. Kaynak: e-ticaret altyapısı (ikas, Shopify, Ticimax …), pazaryeri, ERP export'u.

| Sütun | Tip | Zorunlu | Not |
|---|---|---|---|
| `siparis_no` | metin | ✓ | |
| `tarih` | tarih-saat | ✓ | ISO (`2026-01-05 10:00`) veya Türk biçimi (`05.01.2026`) karışık olabilir; saat varsa saat × gün analizi |
| `sku` | metin | ✓ | `sku` tablosuyla eşleşir |
| `adet` | sayı | ✓ | > 0; iade/iptal satırları profil dışında |
| `kanal` | metin | | web, pazaryeri, b2b, bayi … |
| `tasiyici` | metin | | kargo firması (kafes ve ayırma hesabı) |
| `iade` | evet/hayır | | |

Kurallar: aynı siparişte aynı SKU = **tek toplama satırı**. Günlük seriler ilk ve son gün arasındaki tüm takvim günleri üzerinden (satışsız gün = 0).
Önerilen süre ≥ 12 ay (P95 ve mevsimsellik); < 90 gün uyarı verir.

## 2. `sku` (önerilir)

| Sütun | Tip | Not |
|---|---|---|
| `sku` | metin | zorunlu |
| `ad`, `barkod`, `kategori` | metin | barkod, e-ticaret ↔ ERP eşleştirmesinin anahtarı |
| `en_cm`, `boy_cm`, `yukseklik_cm` | sayı | göz/raf hacmi, kutu (desi) |
| `agirlik_kg` | sayı | raf yükü, kargo kg kontrolü |
| `koli_ici_adet`, `palet_koli` | sayı | rezerv palet ihtiyacı |

## 3. `bom` (kit / karma koli varsa)

| Sütun | Tip | Not |
|---|---|---|
| `kit_sku` | metin | |
| `bilesen_sku` | metin | başka bir kit olabilir (çok seviyeli açılır) |
| `miktar` | sayı | kit başına bileşen adedi |

Kit toplama modu kitte değil senaryoda seçilir (`depoplan/kit.py`): `bilesen` (bileşenlere aç), `hazir` (önceden kurulu, tek satır), `sabit` (tek ürün, N satır).

## 4. `parametreler`

`depoplan.Parametreler` — toplama/paketleme/hazır paket hızı, net saat, hücre ve istasyon sayısı, araba gözü, ABC/XYZ eşikleri.
Varsayılanlar Kazan v8.16 modelinden; pilot veya cycle time ölçümüyle her şirkette değiştirilir.

## Profil çıktısı (`sku_profili`)

`toplam_adet`, `toplama_satiri`, `siparis`, `tekli_siparis(_pay)`, `gunluk_ort/p95/maks`, `son90/son30_gunluk_ort`,
`pik_katsayi_p95/ort`, `haftalik_cv`, `ABC_adet` (kümülatif adet payı ≤ %80 A, ≤ %95 B), `ABC_satir` (aynı kural, toplama satırı), `XYZ` (haftalık CV < 0,5 X, < 1,0 Y).
Kazan `SKU_Profil.csv` sınıflarıyla birebir aynı (test: `tests/test_kazan_referans.py`).

## Henüz yok (sıradaki sürümler)

- Stok tablosu (lot, SKT, lokasyon) — rezerv ve taşınma planı
- Bina modeli (kolon, duvar, kapı, bölge) — `layout.json`'un genel hali
- Mal kabul / B2B sevk planı (araç, palet)
