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
| 5b | **Süreç modeli + Depo Senaryo Stüdyosu** (hacim × verim × layout → kişi; N kişi → karşılama, darboğaz; sektör şablonları, süreç kütüphanesi, sürüklenebilir layout, senaryo karşılaştırma) | kadro simülasyonu v8.16, onay sunumu | **v0.2** `surec.py`, `app/` |
| 6 | Toplama yöntemi karşılaştırma | toplama senaryoları | sırada |
| 7 | Slotting (göz, kat ergonomisi, besleme) | `hucre_slot.py` | sırada |
| 8 | Depolama kapasitesi (raf kütüphanesi) | `layout.py`, `lok.py` | sırada |
| 9 | Kesikli olay simülasyonu | 3D akış sim v2.4 (tarayıcıda, ajan tabanlı; hedef 120 → akışta 95 satır/saat) | sırada: sim'in zaman modeli (`T_`: satır süresi, sefer hazırlığı, bırakma, yürüme hızı) genelleştirilip Stüdyo'daki süreçlere bağlanacak |
| 10 | Bina modeli, çakışma, kaçış mesafesi | `carp.py`, `kacis.py` | 2. faz |
| 11 | Çıktılar: DXF, WMS lokasyon, rapor | `dxfout_v70.py`, `xl_wms.py` | 2. faz |
| 12 | Web arayüzü | kadro simülasyonu artifact'i | 2. faz |

## Kararlar (22.11.2026)
| Karar | Gerekçe | Risk | Sonraki adım |
|---|---|---|---|
| Model süreç bazlı: her depo aynı yapı taşları (kabul, yerleştirme, x-dock, besleme, ABC, toplama, paketleme, kantar, sevk, iade, VAS); sektör farkı şablonla | Yönetici kendi KPI'ından hacim ve verimi verebilir; sektör seçimi ilk 5 dakikayı kısaltır | Şablon rakamları kıyaslama sanılabilir | Uygulamada "örnek değer" uyarısı; gerçek müşteri verisiyle kalibrasyon |
| Layout etkisi yalnız yürüme payı üzerinden, merkezler arası Manhattan mesafe | Basit, açıklanabilir; bölge içi yürüme bölge boyutuna bağlı | Koridor/engel yok sayılır | DES modülünde rota ızgarası (kacis.py'deki 0,2 m ızgara yaklaşımı) |
| Kişi dağıtımı 0,5 FTE adımlarla, öncelik sırasıyla | Gerçekte çıkış süreçleri önce doldurulur; küçük süreçler paylaşımlı | Çok becerili personel esnekliği tam yansımaz | Kullanıcı "elle kişi" ile düzeltir |
| Hedef verime "akış kaybı" alanı | Kazan sim: analitik 120 → akışta 95 (%21) | Kayıp süreçten sürece değişir | DES ile süreç bazında ölçülür |

## Çalıştırma
```bash
python3 -m pytest -q
```
