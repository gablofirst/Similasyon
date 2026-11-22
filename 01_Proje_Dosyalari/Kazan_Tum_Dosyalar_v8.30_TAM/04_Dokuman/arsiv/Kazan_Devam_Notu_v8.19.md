# Kazan yerleşim · devam notu (v8.19, 21.11.2026) · TEK GÜNCEL NOT

Yeni sohbet yalnız bu notla ve `claude/Kazan_Veri_Temeli_ikas_2026_YTD.md` ile başlar. Bu not kendi başına yeterlidir. Eski devam notları (v6.3–v8.18) arşivdir.

> **⚠ ÖNEMLİ — ARABA (Sedat, 20.11):** Toplama arabası **tedarik edilecek ve pilotta test edilecek.** Araba Kazan'ın tek yeni ekipmanı; 2026'da 30, 2027'de ≈45 adet. **30 adetlik sipariş, numune araba Ostim pilotunda test edilmeden verilmez.**
> - Numune: 24.11 onayından hemen sonra 1–2 tedarikçiden 2 adet; teslim hedefi 02.12 (pilot başı). Şartname ölçüsü 100 × 70 × 160 cm, 18 göz, 3 kat (taban 50/80/110), göz içi 32 × 34 × 28 cm, ayarlanabilir kat.
> - Pilotta test: göz ölçüsü (5,5 L kavanoz dik), uzak sıra erişimi, dolu itme/dönüş, 160 cm'de görüş, tekerlek/fren, istasyonda boşaltma süresi, 5 günde hasar.
> - Numune gecikirse: pilot koli10'lu geçici arabayla (3 kat × 6 koli10 = 18 göz) başlar, numune gelince +1 gün araba testi.
> - Sonuç → şartname son hali (kat kotu, tekerlek, ayırıcı, tutamak) → sipariş.

**v8.19 (21.11, Sedat onayı): çizim v8.11 üretildi — e-ticaret bandı 17,03 m doğuda.** Paket: `Kazan_Tum_Dosyalar_v8.11_TAM.zip` (Sedat projeye yükleyecek; v8.10 zip'in yerine).
- Kaydırma **17,03 m** (as-built kolon ekseni 116,12 → 133,15; kolonlar X 99,12 / 116,12 / 133,15+133,80 / 150,82 / 167,82). H1 X 122,73–133,93 · paketleme 134,43–145,63 · H2 146,13–157,33 · HP 157,43–168,53. Hücreler 29 göz × 5 kat, döngü 30,6 m (değişmedi).
- Kolon kontrolü: H1 kolonu 132,87–133,42 doğu raf ucunda, döngüde net **1,62 m** (v8.10: 1,60); ikiz 133,52–134,07 rafın arkasında, H1 kenarından 0,14 m taşar (paketleme araba alanına). H2 kolonu 150,52–151,12 ada içinde (tasarım gereği). carp.py: 1 bulgu (soyunma, as-built, bilinen) · ek kontrol (hücre rafı, kampanya palet, VAS 5–6): 0.
- Duvarın doğusu: **kampanya X 100,2–115,6 (229 m²)**: 3 palet sırası (duvar tarafı tek 100,4–101,6 · orta çift 104,6–107,0 · doğu tek 110,0–111,2; Y 49,4–63,6), aralarda 3,0 m koridor, **72 yer paleti**; boş araba şeridi X 111,2–115,6. Kolon 115,82–116,42 boşlukta. **Koli/dolgu X 116,6–122,3 (85 m²)**. Akış E0: boş araba + lansman → H1 girişi (güney şerit Y 62,4 üzerinden); E5: lansman rezervi ana koridordan (kapı X 105,6).
- **VAS 5–6** eski kampanya alanında dikey: X 85,5–90,9 ve 93,1–98,5, Y 50–62 (65 m² × 2), koridor 90,9–93,1, tampon Y 62,2–63,9; girdi V6 ana koridordan (kapı 91,9). Eski VAS 5–6 yeri (X 70,6–81,7) → **SERBEST 133 m²** (VAS 7–8 olası).
- Kargo: K1 X 140,13 → **güney kapı 139,0**; saptırıcı X 140,13; K4-batı 127,0–140,13 + batı masası 121–127; K4-doğu 140,13–156,0 + doğu masası 156–162. Kafes: HepsiJet X 100,2–139,8 (206 m²), Trendyol 140,1–163,5 (122 m²), Yurtiçi 163,8–167,5 (19 m²). **Saçak ve yanaşma şeridi X 167,5'e uzar; tel çit X 150,7 → 167,6 taşınmalı** (as-built'te başka engel yok, yalnız zemin kaplaması). HP çıkışı güney kapı 156,0.
- Ana koridor ve bariyer X 168,5'e uzar; kapılar 60 / 79,3 / 91,9 / 105,6 / 113,4 / 128,6 / 151,6 / 163,0.
- **Rezerv 3.835 → 3.495 m²** (kullanılan 340 m²: e-ticaret bandı 262 + ana koridor uzantısı ≈66 + pay). Rezerv sınırı basamaklı: X 151,9 (Y < 44,3), X 168,9 (Y 44,3–64,3). 3. hücre + 8 istasyon (seçenek B) için yer yeterli.
- **Kaçış (kac811.py):** en uzun **44,3 m** (X 48,4 / Y 28,4, sevk tamponu batı ucu) — v8.10 ile aynı (aynı kodla v8.10 = 44,3; not v8.9'daki 44,5 ızgara farkı). E-ticaret bandında en uzun 22,5 m. 45 m üstü alan 0.
- Kod: `05_Kaynak/v811/` (v811_layout.py kaydırma, carp_ek.py ek kontrol, kac811.py kaçış, asb_from_dxf.py as-built'i v8.10 DXF'ten okur — LibreDWG gerekmeden), `yerlesim/dxfout_v811.py`. DWG: dxf_r2000_flat.py + LibreDWG 0.13.3 dxf2dwg; dwgread ile doğrulandı (8.615 nesne, 33 PO katmanı).
- Kalan: hucre_slot kampanya kuralı (lansman = kampanya palet yüzü, H1 dalgası), WMS lokasyon (kampanya K-01…24 → palet yerleri), simülasyon planı, sunum plan görseli, İhsan'a yeni koordinatlar (hücre rafı, HP rafları, K4), saçak ruhsatı kapsamı.

**v8.18 (21.11, Sedat'ın önerisi): e-ticaret bandını doğuya kaydır — ÖNERİ, karar bekliyor (v8.17'deki şerit önerisinin yerine).**
- H1, paketleme, H2 ve HP **17,1 m doğuya** (1 kolon aksı): H1 X 122,8–134,0 · paketleme 134,5–145,7 · H2 146,2–157,4 · HP 157,5–168,6. Rezervden 262 m² (kalan ≈3.573 m²; 3. hücre için yeter).
- Neden 17,1 (Sedat'ın 220 m² ≈ 14,4 m'si değil): kolonlar hücrelerde bugünkü doğrulanmış yerinde kalır (H1 doğu raf ucu göreli 10,4 m, H2 adası, HP doğu rafı). 14,4 m'de 133,2/133,85 dilatasyon çifti paketleme istasyonlarının içine düşer (batıdan 1,4–2,05 m).
- Duvarın doğusunda **kampanya + koli/dolgu birleşik alanı X 100,2–122,8 = 346 m²** (eski kampanya 211 + koli 74 = 285 m² → ≈60 m² boş araba payı). Kolon 116,1 / Y 54,5 bu alanın içinde: palet sıraları kolona göre dizilir. Araba rotası: boş araba + kampanya → H1. Göz = sipariş korunur, duvar sorunu kalkar.
- Eski kampanya alanı (X 85–98,8 / Y 48,6–63,9, 211 m²) → **VAS 5–6 dikey** (2 × 5,4 m hat, 12 m boy, arada 2,2 m koridor = 13,0 ≤ 13,8 m; içinde kolon yok). Eski VAS 5–6 yeri (X 70,6–81,7) boşalır. "VAS'ın tamamını güneye çekme" yorumu ayrıca hesaplanacak.
- Kargo: K1 X 140,2'ye gelir → güney kapı 139,0 (bugünkü 121,3 yerine). HP çıkışı kapı 156,0 / 173,0. Saçak bugün X 150,5'te bitiyor: Trendyol + Yurtiçi kafesi HP yanında kalsın diye **saçak ≈18 m doğuya uzamalı** (ruhsat); HepsiJet kafesi K1'in batısına. K4 konveyörü yeniden çizilir.
- Yapılacak (karar sonrası): layout.json → carp.py (kolon/duvar), kacis.py yeniden, hucre_slot kampanya kuralı, simülasyon planı, sunum plan görseli.

**v8.17 (21.11, Sedat'ın tespiti): kampanya lokasyonu duvarın yanlış tarafında — ÖNERİ, karar bekliyor.**
- Sorun: kampanya lokasyonu (X 85–98,8 / Y 48,6–63,9) ile e-ticaret alanı arasında iç duvar X 99,1 (Y 45,2–63,8). Geçiş yalnız ana koridordan (Y < 45,2, forklift trafiği, kolon hattı net ≈3,0 m). Kampanya → H1/paketleme tek yön ≈35–40 m. v6.6'daki "lansman palet önünden toplanır" kuralı (hucre_slot.py) rotaya hiç bağlanmamıştı.
- Veri (hucre_slotted.pkl, son 90 gün hızı): kampanyadaki 5 lansman SKU (Creatine SB 120g, Whey Almond Coffee, Pea Peanut Choc, CoR Peanut Choc 1kg, Mass Gainer Choc&Hazelnut) = **≈784 satır/gün, hücre satırının %11,5'i** (yıl ortalamasında %2,7; şu an aktif lansmanlar). Bunun ≈491/gün çok ürünlü siparişte → sipariş iki yerden toplanır, göz = sipariş bozulur. 3 günlük stokla 31,3 göz gerekir; hücrede boş göz 10,75 → hücreye sığmaz.
- Öneri: (1) kampanya **toplama yüzü** duvarın doğusuna, koli/dolgu/boş araba şeridine (X 100,2–105,2 / Y 48,6–63,9, 5 × 15,3 m): duvar tarafında ≈10 yer palet yüzü + 1,8 m koridor + boş araba; araba rotasının başı (boş araba alınır → lansman → H1). (2) **Koli/dolgu** duvarın batısına (kampanya alanı 211 m²), paketlemeye vardiyada 2–3 kez parti besleme. (3) Batı kampanya alanı = lansman **rezervi** (günlük besleme) + lansman günü **tekli ön paketleme** (≈293 satır/gün tekli; HP mantığı, parti çıkış); pikte serbest alan 149 m² / VAS 5–6 (2027'ye kadar boş). (4) WMS kuralı: lansman satırı olan siparişler H1 dalgasına.
- Alternatif: X 99,1 duvarına Y ≈55 civarında kapı (mimari + İSG; duvarın yangın bölmesi olup olmadığı bilinmiyor).
- Yapılacak: Sedat kararı → çizim v8.11 (carp.py ile kolon/duvar kontrolü), hucre_slot kampanya kuralı, simülasyon.

**v8.16 (20.11): yeni kadro simülasyonu** — https://claude.ai/artifact/CMviKHGobasRgSNiAdiKKn (v8.15 hücre tasarımı). Eski 4 hatlı sürümler duruyor: Kazan Hat ve Kadro Simülasyonu https://claude.ai/artifact/SULTKQv58LFAv8Fkg5HVjc (05.11), Kazan Hat ve Kadro Planı https://claude.ai/artifact/6imksoun8Hz9jqhdD3CZuL (12.11).
- Model: toplayıcı = sipariş × 1,762 hücre satırı/sipariş ÷ (hız × 7,5 sa); paketleme 71, HP 140 sipariş/adam-saat (v8.6 P95 kadrosundan geri hesap); araba = sipariş × 0,0538 ÷ (18 × 0,94) × 1,1. Gün tipleri: 2026/2027 normal (×0,84) ve P95 (×1,6), rekor (×2,19). Devam %100/90/85/73, FM 2,5 sa/gün ve 22,5 sa/ay sınırı, A/B/C seçenek kontrolü, VAS bloğu (hacim/verim eski simülasyondan, KPI v3.5).
- Doğrulama: 2026 P95 → 40,5 kişi, 30 araba; 2027 P95 → 60,8 kişi, 45 araba, hücre başı 12,4, paketleme 24/16 (v8.6 ile tutarlı). Normal günde HP ve paketleme sürekli modelle ≈21,3 (v8.6 yuvarlamalı 22,1).

**v8.15 (20.11): araba tedarik + test, pilot planı genişletildi.** Pilot planına "Adım adım: Ostim'de nasıl kurulur" ve "Araba testi" bölümleri eklendi. Pilot mevcut bir çift yüzlü raf sırasının etrafında kurulur (stok taşınmaz, koridor bantla 1,8 m, raf ≈7,5 m → döngü ≈15 m); asıl ölçü aynı gün/aynı kişi/aynı ürünle bugünkü yöntem vs arabalı döngü karşılaştırması, fark Kazan kadrosuna uygulanır. Basit alternatif: döngüsüz, mevcut hatta numune araba 2 gün (V3 ölçülmez). Maket araba yerine numune araba.

**v8.14 (20.11): Haftalık Operasyon KPI Raporu v3.18** (`Haftalik_Operasyon_KPI_Raporu_v3_18_20112026.xlsx`, v3.17'nin 20.11 anlık kopyası üzerine, XML düzeyinde; grafikler ve korumalar korundu).
- VAS Kayıt İş tipi'ne iki yeni ek proses: **İade** (adet = iade ürün adedi) ve **B2B Hazırlık** (adet = koli; Getir, Yemeksepeti, Arabica, stand).
- Haftalık KPI BX:CC (adam-saat, adet, verim); BR ve BW'ye dahil. KPI Tanımları 25–26: standart boş = nötr, 3–4 hafta veriden sonra standart.
- VAS "Diğer" için de %10 sınırı (Ayarlar B8 × VAS ödenen saat); aşan kısım fiili saate (Haftalık KPI CD:CE → BE).
- Doğrulama: LibreOffice yeniden hesabında mevcut tüm değerler v3.17 ile aynı; 299 #N/A COO Özet'te v3.17'de de var.
- Kazan bağlantısı: iade ve B2B hazırlık adam-saat/koli verisi, kalite/iade alanı (X 49,2–70 / Y 59,5–63,9) ve B2B toplama yüzü boyutlandırması için §7-6 eksiğini doldurmaya başlar.
- 20.11 saha notu: bayi hattı notta 3 kişi, VAS Kayıt 321–323'te 2-1-1 = 4 kişi → düzeltilecek; Günlük E-ticaret 18–20.11 raf basımı saati (V) ve Diğer saati (Z) boş.

**v8.13 (20.11): Ostim pilot planı hazırlandı** — https://claude.ai/artifact/NQy8hqV4TAveCcFxnqrV7m
- Karar kuralı: ≥120 satır/saat model geçerli · 80–120 hücre geçerli, kadro pilot hızıyla yeniden · 69–80 gri bölge (Senaryo 1 ile yeniden karşılaştır) · <69 veya hata ≥%0,3 → Senaryo 1. Hata için ≥3.000 kontrollü satır, ≤3 hata = %95 güvenle <%0,3.
- Test: V1 hız, V2 hata, V3 hücre başı sınır kişi (yarım döngü 15 m'de 3→6 kişi = tam döngüde 6→12), V4 uzak sıra (doldurma kuralı A yakın sıra önce / B sıralı), V5 sefer başına ≈17 sipariş ve görüş; yan ölçüm paketleme sipariş/saat.
- Yerleşim: Kazan hücresinin yarısı 1:1 (1,8 m koridor, ≈15 m + 1 dönüş, ≈15 × 6 m), ilk ≈100 SKU (satırların ≈%75'i), 2 numune araba (18 göz; v8.15'te maket yerine). WMS mantığı Excel listesiyle taklit.
- Takvim (öneri): hazırlık 25.11–02.12, ölçüm 03/04/07/08/09.12, rapor 11.12. Black Friday 27.11 ve Cyber Monday 30.11 dışarıda; kampanya takvimiyle teyit.
- Açık: Ostim'de 15 × 6 m alan; pilot sorumlusu ve gözlemci isimleri.

**v8.12 (20.11): not temizliği + 24.11 karar listesi + onay sunumu v8.12.**
- Tutarsızlıklar düzeltildi: kaçış her yerde **2 tünel / 68 şerit / 4.030 palet** (eski "3 tünel, 4.010" ifadeleri kaldırıldı); §3 kit ve hücre rakamları v8.6 değerlerine çekildi (6 HP kiti, hücre ek yükü 1.816,7, hücre satırı 9.322, göz 134,2/145); "WMS yetenekleri teyit edildi" ifadesi v8.8 ışığında "sözleşmede yok" olarak düzeltildi; Excel çıktıları v8.10.
- **Veri temeli §11'deki "e-ticaret %20/yıl" geçersiz** → 2027 ×1,5 (v7.8). Veri temeli dosyasının kendisi düzeltilmedi; hesaplarda bu not esas.
- 24.11 karar listesi §6-c'ye yazıldı (WMS sözleşmesi eklendi).
- Onay sunumu (Slides artifact, aynı link) v6.7 → v8.12 güncellendi.

**v8.11 (20.11): bağlam paketi yenilendi** — `Kazan_Tum_Dosyalar_v8.10_TAM.zip` (116 dosya). Hücre stoğu, WMS lokasyon (drive-in 68 şerit = 1.360) ve kit Excel'i v8.10 verisiyle yeniden üretildi; kit Excel'ine "2027 Kapasite" sayfası eklendi. 3D dosyalar eski (v7.5).

**v8.10 (Sedat, 20.11): H1 girişindeki kolon düzeltildi.**
- Sorun: kolon (X 116,1 / Y 54,5; 0,6 × 0,6 m) H1'in doğu açıklığının (Y 52,6–56,6) tam ortasındaydı; araba dönüşü kolon köşesinde, döngü koridoru kolon önünde 1,58 m; döngü başı/sonu tıkanma noktası.
- Çözüm: açıklık kolonun güneyine alındı: **Y 55,5–59,32 (3,82 m; giriş 55,5–57,41, çıkış 57,41–59,32)**. Doğu raf hattı Y 49,88–54,2 (2 göz), kolon raf hattının ucunda, açıklıktan 0,7 m. Göz sayısı 29, döngü 30,6 m. Kolon önü 1,58 m ama düz yolda.
- `hucre_geo.py` açıklığı parametreli (`acik_y`, `kolon_y`); H2 değişmedi. Girişe yakın 2–3 gözün yüzü (D/A) iki hücrede farklı.
- Kolon taraması: **ana koridorda kolon hattında net ≈3,0 m** (Y 45,2–48,2) → iki yönlü forklift için dar; tek yön / geçiş kuralı veya RT tipi (İhsan). Diğer alanlarda çakışma yok.
- Çıktılar: `Kazan_v8.10_AsBuilt_Yerlesim.dxf/.dwg/.png`.

**v8.9 (Sedat + İSG, 20.11): kuzey kapı planı kesinleşti.**
- Kuzey duvar: 5 seksiyonel (X 60,8 / 86,4 / 121,9 / 156,6 / 190,6) + 8 yangın kapısı (X 81,2 / 108,4 / 125,4 / 143,1 / 160,1 / 177,1 / 194,1 / 211,1). Güneyde de aynı X'lerde 8 yangın kapısı.
- Karar: kuzey **iptal 211,1 · 177,1 · 143,1 · 108,4; acil çıkış 81,2 · 125,4 · 160,1 · 194,1**. Seksiyonel kuzey kapılar kapalı, çıkış değil (Sedat teyit edecek).
- 81,2 ve 125,4 drive-in arkasında → **2 kaçış tüneli** (v8.3'teki 3 tünel iptal). Şerit 22 ve 53 kaldırıldı; ADEYA kalan şeritleri ≈0,4 m kaydırarak tüneli kapı eksenine ortalamalı, olmazsa bir şerit daha gider (−20 palet).
- Kapasite: drive-in **68 şerit (batı 34, orta 34) = 1.360**; toplam **4.030 palet**.
- Kaçış (sprinkler yok, sınır 45 m): en uzun **44,5 m** (X 48,4 / Y 28, sevk tamponu batı ucu) → uygun, **pay 0,5 m**. Pay; rampa kapılarının çıkış sayılmasına ve sevk tamponu / streç geçişinin açık kalmasına bağlı → İSG teyidi.
- Çıktılar: `Kazan_v8.9_AsBuilt_Yerlesim.dxf/.png` (PO_KACIS), `Kazan_Kacis_Mesafesi_v8.9.png`, `layout.json`.

**v8.8 (20.11): WMS sözleşmesi incelendi** (`PROTEINOCEAN_SOZ_WM_01.pdf`, AXATA axata/WM V.2.3, taslak V.1, imzasız).
- **Kritik:** kapsamda "e-ticaret modülü hariç". Kazan tasarımının dayandığı yetenekler (e-ticaret dalgası, 18 gözlü araba–sipariş eşleştirme, kit/BOM açma, HP ayrıştırma, kargo barkodu/taşıyıcı tanıma, ikas ve kargo entegrasyonu) sözleşmede yok; yalnız ERP entegrasyonu var. v8.5'teki "WMS yapabiliyor" teyidi sözleşmeye yazılmadıkça geçersiz.
- Diğer: mobil lisans 20 (2026 P95 ≈40, 2027 ≈60 kişi); tesis Ostim, Kazan yok; destek hafta içi 08:30–18:00, SLA/ceza yok; teslim "donanımdan sonra 3 ay", gecikme cezası yok; garanti kuruluştan başlıyor; ödemenin %40'ı kurulumda; uygulama 20 adam/gün, entegrasyon açık uçlu (19.700 TL/adam/gün); eğitim 2 gün key user; kabul/UAT, veri taşıma (lot/SKT), hypercare, performans hedefi, veri iadesi yok; Wi-Fi a/b/g ve "Windows/SQL 2018" eski/hatalı.
- Öneri: imzadan önce Ek-1 Fonksiyonel Kapsam + Ek-2 Entegrasyonlar + Ek-3 SLA + Ek-4 Kabul kriterleri.

**v8.7 (Sedat, 20.11):** Kargo dedike ofisle çalışıyor, araçlara anlık çekiyor → kafes kısa tampon. 2027 P95 (12.705 koli/gün, ≈1.694/saat): saatlik hacim HepsiJet ≈8,0 m³ (≈10 m²), Trendyol ≈2,1 m³, Yurtiçi ≈0,4 m³. Kafesler (≈167 / 80 / 11 m²) 17 / 30 / 22 saatlik üretimi tutar → **kafes alanı 2027'de yeterli, kapandı.** Asıl kısıt yanaşma şeridi (Y 71–74,6) ve çekme ritmi.

**v8.6 (hesap, 20.11): 2027 ×1,5 kapasite kontrolü.**
- `bom_map.py` → `kit_explode.py` (HP_KIT'e 6568150; 6000490 = 3 satır) → `hucre_slot.py` (×1,0 ve ×1,5).
- Kit sonucu (2026): hücre ek yükü **1.816,7** satır/gün, masa 161,7, 6 HP kiti 404,6 kit/gün. Hücre satırı **9.322**/gün.

| | 2026 | 2027 (×1,5) | Kısıt / sonuç |
|---|---|---|---|
| Hücre satırı/gün (yıl ort.) | 9.322 | 13.983 | |
| Hücre gözü (iki hücre aynı) | 134,2 / 145, besleme 3 günde bir | 134,2 / 145, **besleme 2 günde bir** | **Sığıyor.** Besleme 203 → 304 kalem/gün |
| Toplayıcı normal / P95 | 8,7 / 16,6 | 13,1 / **24,9** | P95'te hücre başı 12,4 kişi; 30,6 m döngüde ≈2,5 m/kişi → **sıkışma** (varsayım: hücre başı en fazla ≈8 kişi, pilotla ölçülecek) |
| Paketleme kişi normal / P95 | 9 / 16 | 13,5 / **24** | 16 istasyon: normal sığar, **P95 sığmaz** |
| HP hattı + HP topla + kit kurma | 4,4 / 7,8 | 6,6 / 11,7 | HP hattı tek: kapasite pilotla |
| Araba (18 göz) | 30 | **45** | P95 WIP 456 → 684 |
| Sahada toplam normal / P95 | 22,1 / 40,4 | 33,2 / 60,5 | besleme, kargo ekibi, şef hariç |
| Sipariş/gün ort. / P95 | 5.291 / 8.470 | 7.937 / 12.705 | kargo ≈3.930 → ≈5.900/gün |

- Hesap kuralları: toplayıcı = hücre satırı × (normal 0,84 / P95 1,6) ÷ (120 satır/saat × 7,5 saat); paketleme, HP ve araba hacimle doğrusal; Karma Kutu hücrede 1,75 göz.
- **Sonuç:** 2027'de darboğaz göz değil, **P95 günü insan yoğunluğu**. Seçenekler: (A) P95'te ikinci/uzatılmış vardiya, (B) 3. hücre + 8 istasyon doğu rezerv alanda (≈3.815 m²), (C) karışık: 2027 başı A, büyüme teyit edilince B. **Öneri C**; karar 24.11'de. P95 büyümesinin de ×1,5 olduğu varsayıldı.

**v8.5 (Sedat, 20.11):** WMS'in dalga, sipariş–araba gözü eşleştirme, kit açma, kargo barkodundan taşıyıcı tanıma yapabildiği söylendi. **v8.8 ile geçersiz: sözleşmede yok.**

**v8.4 (Sedat, 20.11):** COO + GM onay toplantısı Salı 24.11.2026. Mimari açıklıklar: X 48 kritik, X 99,1 değil, onay durumu bilinmiyor. Ostim pilotu planlanmadı; planı Claude hazırlayacak.

**v8.3 (Sedat + ölçüm, 20.11):** Sprinkler yok → sınır iki yön 45 m, tek yön 15 m. Ölçüm `layout.json` üzerinden (0,2 m ızgara, 8 yönlü en kısa yol). Tünelsiz en uzun 58,7 m (≈518 m² 45 m üstü) → uygun değil. 3 tünel önerilmişti; **v8.9'da 2 tünel (81,2 / 125,4) ile değiştirildi.** Şartlar: tünel 1 şerit boş, üstü koruma ağlı, iki yanı bariyerli (ADEYA); kuzey kapılarda panik bar (md. 30/4), yönlendirme ve acil aydınlatma; tünel ve kapı önü daima boş (md. 35). Kod `kacis.py`.

**v8.2 (20.11):** Mevzuat (BYKHY): depolarda kaçış tek yön 15 m (sprinklerli 25), iki yön 45 m (sprinklerli 60) [Ek-5/B]; kullanıcı yükü depo 30 m²/kişi, paketleme 10 m²/kişi [Ek-5/A]; >50 kişi ≥2, >500 ≥3, >1.000 ≥4 çıkış [md. 39]; çıkışların önü engellenemez [md. 31, 33/6, 35].

**v8.1 (Sedat, 20.11):** Forklift ve RT kiralanacak; tip, adet, kaldırma yüksekliği İhsan'ın bilgisine göre.

**v8.0 (20.11):** Kutu dosyasına Trendyol sayfası eklendi. Trendyol ort. 1,38 desi, %80'i 1 desi. Tümü ort. 1,99 desi, ≤10 desi %99,85.

**v7.9 (Sedat, 20.11):** Protein Bar Karma Kutu (6740013) tek ürün, hücreden 1 satır (hücrede 1,75 göz). Protein Bar 32'li paket (6000490) = 3 × 12'li display (36 bar), siparişte toplanır → **3 satır**. Ana veri: ikas adı "32'Lİ", içerik 36; WMS kit tanımı "3 × 12'li display, aroma serbest".

**v7.8 (Sedat, 20.11):** 2027 e-ticaret büyümesi **×1,5** kesin. Genel %80, Aralık bütçesiyle teyit.

**v7.7 (Sedat, 20.11):** **6 HP kiti:** Fitness Bisküvi/Ahududu, Fitness Çikolata/Karpuz, Fitness Çikolata/Ahududu (6568150) (bugünkü 3) + Günlük Vitamin, Whey Protein Paketi, Cream of Rice Paketi (yeni 3).

**v7.3–v7.6:** VAS 5,4 m; kolon Y düzeltmesi; kit BOM işlendi; araba 18 göz × 10 desi; bağlam denetimi.

## 1. Zemin ve koordinat
- **As-built 20.11.2026:** `as-built POCN_FABRİKA_PLAN 20112026.dwg`, birim cm. LibreDWG 0.13.3 ile DXF: `./configure --disable-bindings && make -j8 -C src && make -j8 -C programs dwg2dxf dxf2dwg`, ≈4 dk.
- **Plan (m) → as-built (cm):** X = 8706 + (x − 48,1)·100 · Y = 11530 − (y − 6,48)·100.
  - Kolon aksları X 48,1 / 65,1 / 82,1 / 99,1 / 116,1 / 133,2+133,85 (dilatasyon) / 150,8 / … / 218,9.
  - Kolon aksları **Y 6,48 / 16,1 / 25,7 / 35,3 / 44,9 / 54,5 / 64,1** (kolon 0,6 × 0,6 m).
- **Bina:** X 48,1–218,9, Y 6,5–64,4. Rampa annex X 37,1–47,8 / Y 6,2–39,9 ("iç mekâna eklenecek alan 1"). X 48 duvarı Y 16–30 arasında açılmalı (teyit).
- **İç duvar X 99,1:** Y 6,8–25,4 ve Y 45,2–63,8.
- **Kapılar:**
  - Kuzey seksiyonel: X 60,8 / 86,4 / 121,9 / 156,6 / 190,6 (kapalı, çıkış değil).
  - Kuzey yangın: X 81,2 / 108,4 / 125,4 / 143,1 / 160,1 / 177,1 / 194,1 / 211,1 → **acil çıkış 81,2 · 125,4 · 160,1 · 194,1; iptal 108,4 · 143,1 · 177,1 · 211,1**.
  - Güney seksiyonel: X 60,8 / 86,4 / 104,3 / 121,3 / 139,0 / 156,0 / 173,0 / 190,0 / 207,0.
  - Güney yangın: X 81,2 / 108,4 / 125,4 / 143,1 / 160,1 / 177,1 / 194,1 / 211,1.
- **Ofis bloğu:** X 37–48 / Y 40–57. **Soyunma:** X 48,1–56,6 / Y 40,5–50,0. **Tel çit:** saçakta X 99,5 ve 150,7.
- **Kural:** her çizimden önce `carp.py` (raflar ve alanlar × DUVAR / PARAPET / KOLON). Çakışma kalmadan dosya gönderilmez.
  - İstisna: VAS 1–4 içindeki X 65,1 kolonu tasarım gereği hat içinde.
  - Bir "çakışmayı" düzeltmeden önce tasarımın bunu bilerek mi yaptığına bakılır (v7.1 hatası).

## 2. Yerleşim (v8.10 geçerli; plan koordinatı, m)
- **Batı (VAS / sevk):**
  - Rampa X 37,6–47,8 / Y 7–36,1.
  - Sevk tamponu X 48,4–57,6 / Y 16,1–26,6 (97 m², 27 palet). Streç Y 27,0–30,6. **Kaçış payı için geçiş açık tutulur.**
  - Şef ofisi X 48,1–56,6 / Y 31,0–40,5.
  - Mal kabul X 57,9–76 / Y 16,1–22,4 (114 m²).
  - **VAS 1–4: X 59–71, Y 22,6–44,2, her biri 5,4 m (65 m²).** Hat içi 1,7 m servis koridoru, masalar 2-2-1, giriş doğu, çıkış batı.
  - VAS transpalet koridoru X 56,8–59, Y 31–44,3. Yarı mamül bekleme X 71,4–76 (20 palet).
  - Stokla X 57–70 / Y 48,6–51,8. Serbest alan Y 52,2–59,1. Kalite / iade X 49,2–70 / Y 59,5–63,9. VAS 5–6 (2027 yedek) X 70,6–81,7.
- **Ana koridor:** Y 44,3–48,2, X 56,8'den. X 99,1 duvarını 4. sıranın güney 1 gözü kaldırılarak geçer. **Kolon hattında net ≈3,0 m.**
- **ADEYA sırt sırta (12 sıra):** 1/4/7/10. sıralar kolon bantlarında kesik; 4. sıra güney göz 01 yok, batı yüz göz 07–09 yok; 1. sıra alt göz 1–3 B2B yüzü; 8–12. sıra uzatma Y 35,8–44,2 (+360); 13. sıra tek yüz (+114).
- **Drive-in:** 5 derinlik × 4 kat = 20 palet/şerit. **68 şerit (batı 34, orta 34) = 1.360.** Kaçış tünelleri X 81,2 ve 125,4 eksenlerinde. Drive-in koridoru Y 12,4–16,1.
- **Kampanya lokasyonu (v8.11):** X 100,2–115,6 / Y 49–63,9, 72 yer paleti + boş araba şeridi. Eski yer (X 85–98,8) → VAS 5–6 dikey.
- **Hücreler (v8.11):** H1 X 122,73–133,93, H2 X 146,13–157,33, Y 49,0–60,2. Hücre 11,2 m, ada 5,84 m. Döngü 1,8 m, tek yön, 30,6 m. 29 göz × 5 kat = 145 göz/hücre. **H1 açıklığı Y 55,5–59,32.**
- **Paketleme (v8.11):** X 134,43–145,63, 16 istasyon. K1 X 140,13 → güney kapı X 139,0.
- **Koli / dolgu (v8.11):** X 116,6–122,3; boş araba kampanya şeridinde (X 111,2–115,6) ve hücre güneylerinde Y 60,6–63,9.
- **Hazır paket (v8.11):** X 157,43–168,53 (aşağıdaki iç koordinatlar v8.10'dur, +17,03). Mamül raf batı Y 49,4–54,8, doğu Y 48,6–54,0. HP hattı X 145–147, fatura Y 62,5–63,6. Çıkış → K2 139.
- **Saçak (v8.11: X 100,2–167,5; K1 140,13, kafesler HJ 100,2–139,8 / TY 140,1–163,5 / YK 163,8–167,5 — aşağısı v8.10):** K1 → X 123 tarayıcı + saptırıcı. K4-batı (HepsiJet) X 123 → 110 + masa 104–110. K4-doğu (Trendyol + Yurtiçi) X 123 → 141 + masa 141–147. K3 iptal. Kafesler HepsiJet X 100,2–132,3, Trendyol 132,6–148, Yurtiçi 148,3–150,5. Yanaşma şeridi Y 71–74,6.
- **Kapasite 4.030 palet** = ADEYA 2.196 + uzatma 360 + 13. sıra 114 + drive-in 1.360. HP rafları hariç (paketli 48, mamül 2 × 24). WMS sayımı: back-to-back 2.694 lokasyon (+24 fark, İhsan) + drive-in 1.360.

## 3. Operasyon kararları
- **Veri:** ikas 2026 Ocak–Ekim. Ort. 5.291 sipariş/gün, P95 8.470. Tekli %54,7.
- **Taşıyıcı payı:** tüm siparişler HepsiJet %65,6 · Trendyol %30,7 · Yurtiçi %3,4; tekli 52,5 / 44,3 / 2,6; paketleme hattı 69,1 / 27,3 / 3,6.
- **Günlük akış (ort. / P95):** HP → Trendyol/Yurtiçi ≈500 / ≈800 · HP → HepsiJet ≈555 / ≈890 · Paketleme → K4-doğu ≈1.310 / ≈2.090 · Paketleme → K4-batı ≈2.925 / ≈4.685.
- **Hücre stoğu (v8.10):** 304 SKU iki hücrede aynı gözde; 5 lansman SKU kampanya lokasyonunda. Göz 134,2 / 145, besleme 3 günde bir (2027: 2 günde bir). Kat sırası 3 → 2 → 4 → 1 → 5; 5,5 L kavanoz yalnız kat 2/1.
- **Araba:** raflı kafes 100 × 70 × 160 cm, 18 göz (3 kat × 3 × 2), göz = sipariş, 10 desi (iç 32 × 34 × 28 cm). Sefer başına ≈17 sipariş. **2026: 30 araba, 2027: ≈45.** Riskler: uzak sıra erişimi (WMS önce yakın sırayı doldurur / öne çekilebilir kasa), 160 cm'de görüş. Pilotta denenecek.
- **VAS (konveyörsüz):** su örümceği girdi/çıktı; forklift V1 ve V5'. Verim toz 160, vitamin 370 adet/adam-saat.
- **Kitler (v8.6):**
  - BOM 409 karma koli, 1.122 bileşen satırı; ikas kit SKU'larının 195/274'ü eşleşiyor (talebin %78'i).
  - **6 HP kiti** (404,6 kit/gün). Tekli siparişler HP'den; çok ürünlü siparişte kit kutusu hücreden 1 satır.
  - **Hücre ek yükü 1.816,7 satır/gün; hücre satırı 9.322/gün.** Masa (bar, shaker) 161,7 satır/gün.
  - Karma Kutu tek ürün (1 satır), 32'li paket 3 satır.
- **Kadro (v8.6):** sahada normal 22,1 / P95 40,4 (2027: 33,2 / 60,5); besleme, kargo ekibi 2–3, şef 1 hariç. Pilotla teyit.
- **Kutu dağılımı (desi):**

| Kapsam | Kargo/gün | Ort. desi | 1 desi | ≤2 | ≤3 | ≤5 | ≤7 | ≤10 |
|---|---|---|---|---|---|---|---|---|
| HepsiJet + Yurtiçi (Ağu–Eki) | ≈2.650 | 2,41 | %52 | %68 | %79 | %93 | %97 | %99,76 |
| Trendyol (Eyl+Eki) | ≈1.335 | 1,38 | %80 | %90 | %96 | %99,3 | %99,8 | %99,98 |
| **Tümü (Eyl+Eki)** | **≈3.930** | **1,99** | **%63** | **%77** | **%86** | **%96** | **%98,6** | **%99,85** |

  - 10 desiden büyük günde ≈6 kargo. koli1 paket masasında ve HP'de elin altında. HepsiJet+Yurtiçi ikas'a göre ≈%13 eksik (düşük öncelik).
- **Kargo ayırma:** K4 saptırıcı kargo barkodundan taşıyıcıyı tanıyan WMS ile çalışır — **bu yetenek WMS sözleşmesine yazılmalı (v8.8).**

## 4. WMS lokasyon kodlaması (`Kazan_WMS_Lokasyon_ve_Atama_v8.10.xlsx`)
- **Back-to-back:** `B{sıra 01–13}{yüz B/D}-{göz 01–10}-{kat 1–4}{poz A/B/C}`. Göz 01 güney ucu. B04 göz 01 yok; B04B göz 07–09 yok.
- **Drive-in:** `D{şerit}-{kat 1–4}`, 68 şerit (22 ve 53 tünel).
- **Hücre:** `H{1/2}{yüz D/A}-{göz}-{kat}{bölme}`, göz no = döngü sırası, giriş = 01.
- **Diğer:** kampanya `K-01..24`; alan kodları MK, ST, STR, VG, VS, Q, PM, HP, KRG.
- **Canlı öncesi:** ERP aktif SKU listesi (barkod eşleşmesi), koli/palet verisi, taşınma anı stok (lot/SKT), ADEYA kesin göz/tünel.

## 5. Dosyalar (`Kazan_Tum_Dosyalar_v8.10_TAM.zip`, 116 dosya)
- **01_Cizim (v8.11 TAM zip):** `Kazan_v8.11_AsBuilt_Yerlesim.dxf/.dwg/.png`, `Kazan_v8.11_Eticaret_Detay.png`, `Kazan_Kacis_Mesafesi_v8.11.png`; v8.10 dosyaları `arsiv_v8.10/`.
- **02_Simulasyon:** 3D'ler **eski** (v7.5/v7.3).
- **03_Excel:** `Kazan_Kit_Kutu_Araba_v8.10.xlsx` ("2027 Kapasite" sayfası) · `Kazan_Eticaret_Hucre_Stogu_v8.10.xlsx` · `Kazan_WMS_Lokasyon_ve_Atama_v8.10.xlsx` · `Kazan_B2B_Toplama_Yuzu_v6.4.xlsx`.
- **05_Kaynak:** `yerlesim/hucre_geo.py`, `veri/layout.json`, `kit/kit_explode.py`, `hat_stogu/`, `kacis/`, `dxf_r2000_flat.py`; `kit/bom_map.py` girdi `kit/in/bom.xlsx`.
- **Çalıştırma sırası:** (1) DWG → DXF, `bg.py` → `asb_raw.pkl`, `asb_plan.pkl` (2) `veri/*.json` → `/home/claude/work/out/` (3) `layout.py` → `carp.py` → `dxfout_v70.py` (4) `bom_map.py` → `kit_explode.py` → `df_kit.pkl` → `hat_stogu/df.pkl` (5) `hucre_slot.py` → `xl_hucre.py` → `wms/lok.py` → `xl_wms.py` → `kit/xl74.py`.
- **KPI raporu:** `Haftalik_Operasyon_KPI_Raporu_v3_18_20112026.xlsx` (v8.14; düzenleme XML düzeyinde yapılır, openpyxl ile kaydetmek 22 grafiği ve veri doğrulama uzantılarını siler).
- **Artifact'ler:**
  - **Kadro simülasyonu (v8.16):** https://claude.ai/artifact/CMviKHGobasRgSNiAdiKKn
  - **Onay sunumu (v8.12):** https://claude.ai/artifact/FaFp72xqyCmKRD2azgR32w
  - **Ostim pilot planı (v8.13, v8.15'te genişletildi):** https://claude.ai/artifact/NQy8hqV4TAveCcFxnqrV7m
  - 3D https://claude.ai/artifact/1ESkc5Xsxv6Kaduc3zDDDt (v7.5, eski)
  - Şartname https://claude.ai/artifact/AZt5q3WEdkmRghjgH2zAxv (v6.9, eski)

## 6. Açık işler (öncelik sırası)

**24.11 onay toplantısına kadar (Claude):**
- a) ~~×1,5 kapasite kontrolü~~ yapıldı (v8.6).
- b) ~~Onay sunumunu güncelle~~ **yapıldı (v8.12).**
- c) **Karar listesi (v8.12).** Sunumda 8 karar: (1) yerleşim v8.10, (2) 2 tünel, (3) WMS Ek-1…4, (4) X 48, (5) 2027 seçenek C, (6) pilot, (7) teklif + forklift/RT kiralama, (8) saçak ruhsatı + taşınma tarihi. Gerekçe/risk tablosu:

| # | Karar | Gerekçe | Risk | Sonraki adım |
|---|---|---|---|---|
| 1 | 2 kaçış tüneli, 4.030 palet | Sprinkler yok; tünelsiz 59,8 m (v8.9 ölçümü; v8.3'te 58,7) > 45 m; 2 tünelle 44,5 m | Pay 0,5 m (rampa kapıları, sevk tamponu geçişi) | İSG yazılı teyit; tünel tasarımı İhsan |
| 2 | 2027 P95: seçenek C (önce vardiya, teyitte 3. hücre + 8 istasyon) | Göz sığıyor; darboğaz hücre 12,4 kişi/hücre, paketleme 24 > 16 | P95 ×1,5 varsayımı; bütçe farklı çıkabilir | Aralık bütçesi; rezerv alan korunur |
| 3 | Rampa X 48 duvarı Y 16–30 açıklığı | Açılmazsa rampa–sevk tamponu bağlantısı kopar | Onay durumu bilinmiyor, kritik yol | Mal sahibi/mimara yazılı talep |
| 4 | WMS sözleşmesi Ek-1…4 olmadan imzalanmaz | "E-ticaret modülü hariç"; tasarım yetenekleri yok; lisans 20 vs 40–60 | Kazan canlıya geçişi durur | AXATA'ya revize talep |
| 5 | Forklift + RT kiralama, spesifikasyon ADEYA | Ana koridor kolon hattı net ≈3,0 m | Yanlış tip: koridor/kaldırma yetmez | İhsan spesifikasyonu, trafik kuralı |
| 6 | Ostim pilotu: tarih ve sorumlu | 1,8 m koridor, araba, hücre başı ≈8 kişi ölçülmeli | Kadro/araba tahmin kalır | Pilot planı (d) |

- **KAMPANYA LOKASYONU: KARAR VERİLDİ, çizim v8.11 (v8.19).** Kalan: hucre_slot/WMS/simülasyon/sunum güncellemesi, İhsan'a yeni koordinatlar, saçak ruhsatı X 167,5.
- **ARABA: numune tedariki ve pilot testi (önemli, v8.15) — 30 adetlik sipariş testten sonra.**
- d) ~~Pilot planı~~ **yapıldı (v8.13, v8.15'te genişletildi):** https://claude.ai/artifact/NQy8hqV4TAveCcFxnqrV7m. Kalan: alan ve isimler (Sedat), pilot SKU seçimi ve göz ataması (Claude, onaydan sonra).
- e) Şartname güncellemesi (araba, hücre rafı, tünel, kapı adları) — toplantı sonrasına kalabilir.
- f) Excel/3D'nin 6 HP kiti ve H1 açıklığıyla yeniden üretimi (3D eski).
- g) **KPI v3.18 (v8.14):** ortak klasöre geçiş (Sedat); 3–4 hafta sonra İade ve B2B Hazırlık standartları KPI Tanımları D25–D26'ya (Claude, veriden).

1. **İhsan:** ADEYA çizimini as-built'e oturtma; 4. sıra; drive-in 68 şerit ve X 99,1 bölünmesi; 2 kaçış tüneli (X 81,2 / 125,4 eksenine ortalı, koruma ağı + bariyer); hücre rafı 29 göz × 2; konveyör (K3 yok, K4 iki yönlü + saptırıcı); H1 doğu raf hattı Y 49,88–54,2, açıklık Y 55,5–59,32; ana koridor ≈3,0 m trafik kuralı; **forklift + RT spesifikasyonu** (kaldırma yüksekliği, koridor, drive-in araç tipi ve şase, palet yükü, adet).
2. **Mimari:** rampa X 48 açıklığı (**kritik**); X 99,1 Y 45,2–48,2 açıklığı (isteğe bağlı).
3. **İSG:** kaçış payı 0,5 m teyidi (rampa kapıları, sevk tamponu); kuzey seksiyonellerin çıkış sayılmadığı teyidi.
4. **WMS sözleşmesi:** Ek-1…4, lisans, SLA, kabul, Kazan adresi (v8.8).
5. Ostim pilotu: plan hazır (v8.15); 24.11 onayı, alan ve ekip isimleri, **numune araba siparişi** bekleniyor.
6. Eşleşmeyen tekli bar aromaları (düşük etki).

## 7. Veri envanteri ve eksikler (denetim 20.11.2026)

**Var ve güncel:** ikas 01.01–31.10.2026 (1,61 M sipariş, 814 SKU) ve 6 CSV; 2027 e-ticaret ×1,5 (genel %80 teyit bekliyor); as-built 20.11 DWG ve ADEYA raf projesi; BOM; kutu desi dağılımı (3 taşıyıcı); cycle time ve KPI v3.18; personel dağılımı; v8.10 Excel'ler, çizim, kaynak kod; WMS sözleşme taslağı (incelendi, v8.8).

**Var ama eski veya eksik:** ürün ağırlıkları yok, 120 varyant ölçüsü eksik (%4,3); proje takip 27.10; şartname v6.6/v6.9; 3D v7.5; araba ergonomi analizi eski araba üzerine; veri temeli §11 büyüme oranı (%20) geçersiz; 2027 talebi toplam düzeyde — Aralık bütçesinden istenenler: (1) SKU × ay adet, (2) SKU × ay × kanal, (3) hedef stok günü, (4) 2028+ kanal bazında büyüme.

**Eksik — canlıdan önce şart:**
1. ERP aktif SKU listesi ve ikas↔ERP barkod eşleşmesi.
2. SKU ağırlıkları, eksik ölçüler, koli içi adet, koli ölçüsü/ağırlığı, palet başı koli.
3. Taşınma anı stok: lot, SKT, palet sayısı.
4. ADEYA kesin göz/tünel listesi.
5. **İmzalı, e-ticaret kapsamlı WMS sözleşmesi** (Ek-1…4).

**Eksik — tasarımı keskinleştirir:**
6. B2B/VAS/Bim sipariş/satır verisi, VAS çıktısı, mal kabul araç planı. **İade ve B2B hazırlık adam-saat/koli verisi KPI v3.18 ile 20.11'den itibaren toplanıyor.**
7. HepsiJet+Yurtiçi kutu verisinde ≈%13 eksik.
8. Mimari onaylar (X 48, X 99,1, saçak ruhsatı); İSG yazılı teyidi.
9. ikas satır verisi (parquet, kullanıcının bilgisayarında) — dalga simülasyonu için.
10. Ostim pilot ölçümleri.
11. Logo ölçü dosyası `Urun_Olcu_Agirlik_Logo_19112026.xlsx` bağlamda yok.
