# depoplan · ürün yol haritası

Hedef: FMCG / e-ticaret / B2B şirketlerinin sipariş verisinden depo yöntemi, kadro, alan ve yerleşim kararını
günler içinde verdiği uygulama. Referans vaka: Kazan (Protein Ocean) — her sürüm Kazan sonuçlarını yeniden üretmeli.

## Kararlar (21.11.2026)
| Karar | Gerekçe | Risk | Sonraki adım |
|---|---|---|---|
| MVP = e-ticaret/B2C kapasite ve kadro planlayıcı; yerleşim editörü 2. faz | Kazan'da en çok değer bu adımlardan (profil, senaryo, kit, kadro) çıktı; geometri en pahalı kısım | Veri hazırlığı her müşteride tekrar eder | Veri içe aktarma + doğrulama katmanı |
| İki katmanlı model: analitik (saniyeler) + kesikli olay simülasyonu | Analitik model sıkışmayı göremiyor (Kazan V3: hücre başı 12,4 kişi) | DES kalibrasyonu veri ister | Ostim pilot ölçümleri (Aralık) ile kalibrasyon |
| Kazan verisi pakete girmez | Gizlilik ve fikri mülkiyet | Kodun sahipliği sözleşmeye bağlı | Sözleşme kontrolü (Sedat) |

## Modüller ve durum
| # | Modül | Kazan kaynağı | Durum |
|---|---|---|---|
| 1 | Veri şeması + doğrulama | sohbetteki veri temizliği | **v0.1** `sema.py` |
| 2 | SKU profili, sipariş özeti | `SKU_Profil.csv`, veri temeli | **v0.1** `profil.py` (Kazan ABC/XYZ ile birebir) |
| 3 | Gün tipleri ve büyüme | v8.6, v8.16 | **v0.1** `kadro.py` |
| 4 | Kit/BOM açma | `kit_explode.py` | **v0.1** `kit.py` (SKU listeleri parametre) |
| 5 | Analitik kadro ve ekipman | kadro simülasyonu v8.16 | **v0.1** `kadro.py` (v8.16 değerleri test) |
| 6 | Toplama yöntemi karşılaştırma | toplama senaryoları | sırada |
| 7 | Slotting (göz, kat ergonomisi, besleme) | `hucre_slot.py` | sırada |
| 8 | Depolama kapasitesi (raf kütüphanesi) | `layout.py`, `lok.py` | sırada |
| 9 | Kesikli olay simülasyonu (SimPy) | — (pilot sorusu) | sırada |
| 10 | Bina modeli, çakışma, kaçış mesafesi | `carp.py`, `kacis.py` | 2. faz |
| 11 | Çıktılar: DXF, WMS lokasyon, rapor | `dxfout_v70.py`, `xl_wms.py` | 2. faz |
| 12 | Web arayüzü | kadro simülasyonu artifact'i | 2. faz |

## Çalıştırma
```bash
python3 -m pytest -q
```
