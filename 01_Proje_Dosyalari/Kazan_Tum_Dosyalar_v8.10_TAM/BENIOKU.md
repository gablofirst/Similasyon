# Kazan · tüm dosyalar v8.10 (20.11.2026)

Güncel not: `04_Dokuman/Kazan_Devam_Notu_v8.10.md` (tek güncel not).

| Klasör | İçerik | Durum |
|---|---|---|
| 01_Cizim | `Kazan_v8.10_AsBuilt_Yerlesim.dxf` (ana, katmanlı) · `.dwg` (R2000, düz) · `.png` · H1 giriş detayı · kaçış haritası v8.9 | Güncel: 2 kaçış tüneli, kuzey acil çıkışlar, H1 açıklığı kolonun güneyinde, 4.030 palet |
| 02_Simulasyon | 3D hücre/HP (v7.5), 3D VAS (v7.3) | **Eski**: H1 açıklığı, 6 HP kiti ve tüneller 3D'de yok |
| 03_Excel | Kit-Kutu-Araba v8.10 (+ "2027 Kapasite" sayfası, sarı = girdi) · Hücre Stoğu v8.10 · WMS Lokasyon v8.10 (drive-in 68 şerit) · B2B Toplama Yüzü v6.4 | Güncel |
| 05_Kaynak | Kod + veri. Değişenler: `yerlesim/hucre_geo.py` (açıklık parametreli), `veri/layout.json` (DI 68, KACIS, H1 acik_y), `kit/kit_explode.py` (6 HP kiti, 32'li = 3 satır), `hat_stogu/*` (yeniden üretildi), `kacis/` (kaçış mesafesi), `dxf_r2000_flat.py` (DWG yazımı) | Güncel |

Çalıştırma: notun §5 sırası; kit için `kit/bom_map.py` girdi olarak `kit/in/bom.xlsx` (= proje dosyası "Fitness paketi vb tüm bomlar.xlsx") ister.
