# Kazan yerleşim · devam notu (v8.11, 20.11.2026) · TEK GÜNCEL NOT

Yeni sohbet yalnız bu notla ve `claude/Kazan_Veri_Temeli_ikas_2026_YTD.md` ile başlar. Bu not kendi başına yeterlidir. Eski devam notları (v6.3–v8.10) arşivdir.

**v8.11'de değişen (20.11): bağlam paketi yenilendi** — `Kazan_Tum_Dosyalar_v8.10_TAM.zip` (116 dosya). Hücre stoğu, WMS lokasyon (drive-in 68 şerit = 1.360) ve kit Excel'i v8.10 verisiyle yeniden üretildi; kit Excel'ine "2027 Kapasite" sayfası eklendi. 3D dosyalar eski (v7.5). Proje bağlamında v7.5 zip, v7.3 PNG ve Kit v7.5 Excel yerine v8.10 karşılıkları konacak.

**v8.10 (Sedat, 20.11): H1 girişindeki kolon düzeltildi.**
- Sorun: kolon (X 116,1 / Y 54,5; 0,6 × 0,6 m → X 115,8–116,4, Y 54,2–54,8) H1'in doğu açıklığının tam ortasındaydı (açıklık Y 52,6–56,6). Giriş 1,6 m + çıkış 1,8 m'ye bölünüyor, araba (100 × 70) dönüşü kolon köşesinde yapılıyor, döngü koridoru kolon önünde 1,58 m'ye düşüyordu; döngünün başı/sonu (A01 önü) tıkanma noktasıydı. v7.x'te "giriş/çıkış ayırıcı" diye kabul edilmiş, dönüş geometrisi kontrol edilmemişti.
- Çözüm: açıklık kolonun güneyine alındı: **Y 55,5–59,32 (3,82 m; giriş 55,5–57,41, çıkış 57,41–59,32)**. Doğu raf hattı Y 49,88–54,2 (2 göz), kolon raf hattının ucunda, kolon ile açıklık arasında 0,7 m boşluk. Göz sayısı 29 (değişmedi), döngü 30,6 m. Kolon önünde koridor yine 1,58 m ama düz yolda, dönüşte değil.
- `hucre_geo.py` açıklığı parametreli yapıldı (`acik_y`, `kolon_y`); H1 için layout.json'a işlendi. H2 değişmedi (kolonları adada).
- Etki: H1 göz numaraları (döngü sırası) birkaç gözde değişti → H1 ve H2 aynı göz numarasını korur ama girişe yakın 2–3 gözün yüzü (D/A) iki hücrede farklı. Hücre stoğu ve WMS lokasyon listesi yeniden üretilecek.
- Kolon taraması (tüm alanlar): drive-in koridoru (Y 16,1) ve ana koridor (Y 44,9) kolonları koridor kenarında; **ana koridorda kolon hattında net genişlik ≈3,0 m** (Y 45,2–48,2). İki yönlü forklift trafiği için dar → tek yön / geçiş kuralı veya RT tipi buna göre (İhsan'a). Diğer alanlarda çakışma yok.
- Çıktılar: `Kazan_v8.10_AsBuilt_Yerlesim.dxf/.dwg/.png`.

**v8.9 (Sedat + İSG, 20.11): kuzey kapı planı kesinleşti.**
- As-built'te kapılar yeniden okundu: kuzey duvarda 5 seksiyonel (X 60,8 / 86,4 / 121,9 / 156,6 / 190,6) + **8 yangın kapısı** (X 81,2 / 108,4 / 125,4 / 143,1 / 160,1 / 177,1 / 194,1 / 211,1). Güney duvarda da aynı X'lerde 8 yangın kapısı var (eski notta yalnız 81,2 yazıyordu).
- Karar (İSG ile, Sedat'ın DWG'si): kuzey **sağdan 1/3/5/7. yangın kapıları iptal** (X 211,1 · 177,1 · 143,1 · 108,4); **acil çıkış: X 81,2 · 125,4 · 160,1 · 194,1**. Yorum: sayım yalnız yangın kapıları üzerinden (8 kapı); seksiyonel kuzey kapılar kapalı, çıkış değil — Sedat teyit edecek.
- Depo içinde kalan 81,2 ve 125,4 drive-in arkasında → **2 kaçış tüneli** (v8.3'teki 3 tünel X 60,8/86,4/121,9 iptal). Şerit 22 (79,86–81,29) ve 53 (125,19–126,62) kaldırıldı. Kapı şerit sınırına denk geliyor (81,2 ≈ 81,29): ADEYA kalan şeritleri ≈0,4 m kaydırarak tünel boşluğunu kapı eksenine ortalamalı; olmazsa 2. şerit gider (−20 palet).
- Kapasite: drive-in 70 → **68 şerit (batı 34, orta 34) = 1.360**; toplam **4.070 → 4.030 palet** (v8.3'teki 4.010 yerine).
- Kaçış (sprinkler yok, sınır 45 m; güney 9 seksiyonel + 8 yangın kapısı, kuzey 81,2/125,4/160,1/194,1): en uzun **44,5 m** (X 48,4 / Y 28 — sevk tamponu batı ucu) → uygun ama **pay 0,5 m**. Pay; rampa kapılarının çıkış sayılmasına ve sevk tamponu / streç alanında geçişin açık tutulmasına bağlı → İSG'ye teyit ettir.
- Çıktılar: `Kazan_v8.9_AsBuilt_Yerlesim.dxf/.png` (PO_KACIS katmanı: tünel, ACİL ÇIKIŞ, İPTAL işaretleri; metinler 680/680, 4.030), `Kazan_Kacis_Mesafesi_v8.9.png`, `layout.json` (DI 68, KACIS alanı).

**v8.8 (20.11): WMS sözleşmesi incelendi** (`PROTEINOCEAN_SOZ_WM_01.pdf`, AXATA axata/WM V.2.3, taslak V.1, imzasız).
- **Kritik:** kapsam maddesi "e-ticaret modülü hariç". Sözleşme Kazan tasarımının dayandığı yetenekleri (e-ticaret dalgası, 18 gözlü araba–sipariş eşleştirme, kit/BOM açma, HP ayrıştırma, kargo barkodu/taşıyıcı tanıma, ikas ve kargo entegrasyonu) içermiyor; yalnız ERP entegrasyonu var. v8.5'teki "WMS yapabiliyor" teyidi sözleşmeye yazılmadıkça geçersiz.
- Diğer ana eksikler: mobil lisans 20 (2026 P95 sahada ≈40, 2027 ≈60 kişi); tesis yeri/adres Ostim, Kazan yok; destek yalnız hafta içi 08:30–18:00, SLA ve ceza yok; teslim "donanımdan sonra 3 ay", gecikme cezası yok, taşınma tarihine bağlı değil; garanti kuruluştan başlıyor (canlıdan değil); ödeme %40'ı kurulumda (kabulden önce); uygulama 20 adam/gün ve entegrasyon açık uçlu (19.700 TL/adam/gün); eğitim 2 gün yalnız key user; kabul kriteri/UAT, veri taşıma (lot/SKT), hypercare, performans hedefi, veri iadesi yok; Wi-Fi a/b/g ve "Windows/SQL 2018" eski/hatalı.
- Öneri: imzadan önce Ek-1 Fonksiyonel Kapsam (Kazan v8.x gereksinimleri) + Ek-2 Entegrasyonlar + Ek-3 SLA + Ek-4 Kabul kriterleri eklenmeli.

**v8.7 (Sedat, 20.11):** Kargo dedike ofisle çalışıyor, araçlara anlık çekiyor → kafes alanı uzun süreli bekleme değil kısa tampon. 2027 P95 (12.705 koli/gün, 7,5 saatte ≈1.694/saat; koli hacmi HepsiJet/Yurtiçi 2,41 desi ≈7,2 L, Trendyol 1,38 desi ≈4,1 L; istif 0,8 m³/m² varsayımı): saatlik hacim HepsiJet ≈8,0 m³ (≈10 m²), Trendyol ≈2,1 m³ (≈2,7 m²), Yurtiçi ≈0,4 m³. Mevcut kafesler (≈167 / 80 / 11 m²) 17 / 30 / 22 saatlik üretimi tutar → **kafes alanı 2027'de yeterli, kapandı.** Asıl kısıt araç yanaşma şeridi (Y 71–74,6) ve çekme ritmi; dedike ofisle sorun beklenmiyor.

**v8.6 (hesap, 20.11): 2027 ×1,5 kapasite kontrolü.**
- Model yeniden çalıştırıldı: `bom_map.py` → `kit_explode.py` (HP_KIT'e 6568150 eklendi; 6000490 = 3 satır, 8 aroma 12'li display'e talep payıyla dağıtıldı) → `hucre_slot.py` (talep ×1,0 ve ×1,5). Yaması `kit_explode_v8.6.py`.
- Kit sonucu (2026): hücre ek yükü **1.816,7** satır/gün, masa 161,7, HP kiti 6 adet 404,6 kit/gün. Hücre satırı **9.322**/gün (yıl ort.).

| | 2026 | 2027 (×1,5) | Kısıt / sonuç |
|---|---|---|---|
| Hücre satırı/gün (yıl ort.) | 9.322 | 13.983 | |
| Hücre gözü (iki hücre aynı) | 134,2 / 145, besleme 3 günde bir | 134,2 / 145, **besleme 2 günde bir** | **Sığıyor.** Besleme 203 → 304 kalem/gün |
| Toplayıcı normal / P95 | 8,7 / 16,6 | 13,1 / **24,9** | P95'te hücre başı 12,4 kişi; 30,6 m döngüde ≈2,5 m/kişi → **sıkışma** (varsayım: hücre başı en fazla ≈8 kişi, pilotla ölçülecek) |
| Paketleme kişi normal / P95 | 9 / 16 | 13,5 / **24** | 16 istasyon: normal sığar, **P95 sığmaz** (8 istasyon-vardiya eksik) |
| HP hattı + HP topla + kit kurma | 4,4 / 7,8 | 6,6 / 11,7 | HP hattı tek (X 145–147): kapasite pilotla |
| Araba (18 göz) | 30 | **45** | P95 WIP 456 → 684 |
| Sahada toplam normal / P95 | 22,1 / 40,4 | 33,2 / 60,5 | besleme, kargo ekibi, şef hariç |
| Sipariş/gün ort. / P95 | 5.291 / 8.470 | 7.937 / 12.705 | kargo ≈3.930 → ≈5.900/gün |

- Hesap kuralları: toplayıcı = hücre satırı × (normal 0,84 / P95 1,6) ÷ (120 satır/saat × 7,5 saat); paketleme, HP ve araba hacimle doğrusal; Karma Kutu hücrede 1,75 göz (palet yüzü gerekmiyor).
- **Sonuç:** 2027'de darboğaz göz değil, **P95 günü insan yoğunluğu** (hücre döngüsü + 16 paketleme istasyonu). Seçenekler: (A) P95 günlerinde ikinci vardiya / uzatılmış vardiya, (B) 3. hücre + 8 istasyon doğudaki rezerv alanda (≈3.815 m²), (C) karışık: 2027 başı A, büyüme teyit edilince B. Öneri C; karar 24.11 toplantısında.
- ~~Kargo kafes alanı~~ yeterli (v8.7). P95 büyümesinin de ×1,5 olduğu varsayıldı.

**v8.5 (Sedat, 20.11):** WMS gerekli yetenekleri karşılıyor (Sedat): dalga toplama, sipariş–araba gözü eşleştirme, kiti bileşene açma, kargo barkodundan taşıyıcı tanıma. Tasarım bu varsayımla kesinleşti. Soru turu tamamlandı; açık kalanlar: mimari onay (X 48 kritik), İhsan listesi, İSG onayı, pilot planı.

**v8.4 (Sedat, 20.11):**
- **COO + GM onay toplantısı: Salı 24.11.2026.** Toplantıya kadar iş sırası §6'nın başında.
- Mimari açıklıklar (X 48 rampa, X 99,1): onay durumu bilinmiyor. X 48 kritik (açılmazsa rampa–sevk tamponu bağlantısı kopar); X 99,1 değil (mevcut plan açıklıksız çalışıyor).
- Ostim pilotu planlanmadı; pilot planını Claude hazırlayacak.

**v8.3 (Sedat + ölçüm, 20.11):** **Sprinkler yok** → sınır iki yön 45 m, tek yön 15 m. Kaçış mesafesi `layout.json` üzerinden ölçüldü (0,2 m ızgara, 8 yönlü en kısa yol, raf/duvar/ofis/hücre engel; tampon alanlar geçilebilir; doğudaki rezerv alan açık, kuzey kapı 156,6 kullanılabilir; rampa kapıları sayılmadı):
- Tünelsiz (yalnız güney kapıları): en uzun **58,7 m**, ≈518 m² alan 45 m üstü (drive-in koridoru ve ADEYA kuzey uçları) → **uygun değil**.
- 2 tünel (X 60,8 + 121,9): 43,3 m → sınırda uygun (pay 1,7 m).
- **3 tünel (X 60,8 / 86,4 / 121,9): 34,7 m → uygun, ≈10 m pay. KARAR ÖNERİSİ.**
- Kapasite: drive-in 70 → 67 şerit, **4.070 → 4.010 palet** (2 tünelde 4.030). Eski "≈3.770" varsayımı geçersiz.
- Görsel: `Kazan_Kacis_Mesafesi_v8.3.png`; kod `kacis.py` (05_Kaynak/kacis/ olarak zip'e eklenecek).
- Şartlar: tünel 1 şerit (≈1,43 m) boş, üstü koruma ağlı, iki yanı bariyerli (ADEYA tasarlar); kuzey kapılarda panik bar/kilitsiz kaçış kapısı (md. 30/4), yönlendirme ve acil aydınlatma; tünel ve kapı önü daima boş (md. 35). İSG uzmanı onayı gerekli.

**v8.2 (20.11):** Kuzey kapı sorusu mevzuattan ön değerlendirildi (BYKHY). Kurallar: depolarda en uzun kaçış uzaklığı tek yön 15 m (sprinklerli 25), iki yön 45 m (sprinklerli 60) [Ek-5/B]; kullanıcı yükü depo 30 m²/kişi, paketleme 10 m²/kişi [Ek-5/A]; >50 kişi ≥2, >500 ≥3, >1.000 ≥4 çıkış [md. 39]; çıkışların önü engellenemez [md. 31, 33/6, 35]. Kaba ölçü: drive-in koridorundan (Y≈14) en yakın güney kapısına yürüme ≈62–70 m → sprinklersiz 45 m'yi kesin, sprinklerli 60 m'yi büyük olasılıkla aşıyor. Sonuç: kuzeyde kaçış çıkışı gerekli, ama 5 kapının tamamı değil. **Öneri:** 3 kuzey kaçış geçişi, her biri 1 drive-in şeridi boş (koruma ağlı tünel) → drive-in 70 → 67, kapasite 4.070 → ≈4.010 (−60; eski varsayım −300). Teyit: sprinkler var mı, onaylı yangın projesinde kuzey kapılar çıkış mı, tehlike sınıfı (İSG/yangın danışmanı); ölçüm çizimden yapılacak.

**v8.1 (Sedat, 20.11):** Forklift ve reach truck (RT) kiralanacak; tip, adet ve kaldırma yüksekliği İhsan'ın (ADEYA) vereceği bilgiye göre belirlenecek. Madde İhsan listesine taşındı.

**v8.0 (20.11):** Kutu dosyasına Trendyol sayfası eklendi (Eyl, Eki, Kas 1–≈20). Eski dosya yalnız HepsiJet + Yurtiçi imiş (varsayım doğrulandı). Trendyol ortalama 1,38 desi, %80'i 1 desi. Tümü (Eyl+Eki) ortalama 1,99 desi, ≤10 desi %99,85. §3 kutu dağılımı güncellendi.

**v7.9 (Sedat, 20.11):**
- **Protein Bar Karma Kutu (6740013):** üretimden tek kutu gelir (4 aroma bar), tek ürün. Model varsayımı doğru: hücreden 1 satır (181 satır/gün). Ostim'de istasyonda arabada ve orta alanda paletli tutuluyor; hacmi yüksek (son 90 gün 134 adet/gün), Kazan'da hücre gözüne ek palet yüzü gerekebilir (1b'de bakılacak).
- **Protein Bar 32'li paket (6000490):** fiziksel olarak 3 farklı aromada 3 adet 12'li display (36 bar). Önden hazırlanmaz, aromalar stoğa göre değişir, kargo hazırlanırken toplanır. Sabit BOM yok → model: sipariş başına **3 satır** 12'li display SKU'larından (hücre). Etki: hücre ek yükü ≈1.730 → ≈1.816 satır/gün (+86), satır/sipariş ≈2,53 → ≈2,55. **Ana veri uyumsuzluğu:** ikas adı "32'Lİ", içerik 36; WMS'te kit tanımı "3 × 12'li display, aroma serbest" olmalı.

**v7.8 (Sedat, 20.11):** 2027 e-ticaret büyümesi **×1,5 (%50)** kesin kabul. Genel (tüm alanlar) için %80 söylendi, Aralık bütçesiyle teyit edilecek. Bütçe raporlamaya istenen kırılımlar §7'de. ×1,5'in ilk etkisi: araba 30 → ≈45, P95 paketleme 16 → ≈24 kişi (16 istasyonu aşıyor), hücre gözü 145'i aşma riski. Ayrıntılı kontrol açık iş 1b.

**v7.7 (Sedat, 20.11):** Bugünkü HP kitleri: Fitness Bisküvi/Ahududu, Çikolata/Karpuz, **Çikolata/Ahududu (6568150)**. Çikolata/Ahududu modelde bileşene açılıyordu (3 hücre + 1 masa satırı). Doğru model **6 HP kiti** (bugünkü 3 + yeni 3: Günlük Vitamin, Whey Protein Paketi, Cream of Rice Paketi). Etki: hücreye ek yük 1.860 → ≈1.730 satır/gün, masa 210 → ≈162, satır/sipariş 2,57 → ≈2,53. Ek HP işi değişmez (bu kit bugün zaten HP'de). Excel/3D yeniden üretimi bekliyor (`kit_explode.py` HP_KIT'e 6568150 eklenecek). Açık işler artık tek tek soruluyor; kapananlar §6'da işaretli.

**v7.6:** Bağlam ve TAM zip denetlendi (107 dosya, eksiksiz). Veri envanteri ve eksik veri listesi §7'ye eklendi. Yerleşim ve hesaplar değişmedi.

**v7.5'te değişen (Sedat, 20.11):** Hazır pakette yapılan kit 3'ten 5'e çıkıyor, diğer kitler hücrede bileşen olarak toplanıyor.
- Modeldeki 5 HP kiti: Fitness Çikolata/Karpuz, Fitness Bisküvi/Ahududu, Günlük Vitamin, Whey Protein Paketi, Cream of Rice Paketi.
- Bugünkü 3. HP kiti bilinmiyor, teyit edilecek.

**v7.4'te değişen:**
- Kit BOM işlendi; kitler hücrede bileşen olarak.
- Kutu dağılımı değerlendirildi.
- Araba 10 desilik göz olarak tasarlandı (18 göz, 30 araba).

**v7.3'te değişen:**
- VAS 5,4 m'ye geri alındı.
- Kolon Y değerleri düzeltildi.

## 1. Zemin ve koordinat
- **As-built 20.11.2026:** projede `as-built POCN_FABRİKA_PLAN 20112026.dwg` (sohbetteki adı `POCN_FABR_KA_PLAN_20112026.dwg`, içerik aynı), birim cm. LibreDWG 0.13.3 ile DXF'e çevrilir: `./configure --disable-bindings && make -j8 -C src && make -j8 -C programs dwg2dxf dxf2dwg`, ≈4 dk.
- **Plan (m) → as-built (cm):** X = 8706 + (x − 48,1)·100 · Y = 11530 − (y − 6,48)·100.
  - Kolon aksları X 48,1 / 65,1 / 82,1 / 99,1 / 116,1 / 133,2+133,85 (dilatasyon) / 150,8 / … / 218,9.
  - Kolon aksları **Y 6,48 / 16,1 / 25,7 / 35,3 / 44,9 / 54,5 / 64,1** (kolon 0,6 × 0,6 m).
- **Bina:** X 48,1–218,9, Y 6,5–64,4. Rampa annex X 37,1–47,8 / Y 6,2–39,9: as-built'te "iç mekâna eklenecek alan 1". X 48 duvarı Y 16–30 arasında açılmalı (teyit).
- **İç duvar X 99,1:** Y 6,8–25,4 ve Y 45,2–63,8.
- **Kapılar (as-built, v8.9'da yeniden okundu):**
  - Kuzey seksiyonel: X 60,8 / 86,4 / 121,9 / 156,6 / 190,6 (kapalı, çıkış değil).
  - Kuzey yangın kapıları: X 81,2 / 108,4 / 125,4 / 143,1 / 160,1 / 177,1 / 194,1 / 211,1 → **acil çıkış 81,2 · 125,4 · 160,1 · 194,1; iptal 108,4 · 143,1 · 177,1 · 211,1** (İSG, 20.11).
  - Güney seksiyonel: X 60,8 / 86,4 / 104,3 / 121,3 / 139,0 / 156,0 / 173,0 / 190,0 / 207,0.
  - Güney yangın kapıları: X 81,2 / 108,4 / 125,4 / 143,1 / 160,1 / 177,1 / 194,1 / 211,1.
- **Ofis bloğu:** X 37–48 / Y 40–57.
- **Soyunma odası:** X 48,1–56,6 / Y 40,5–50,0.
- **Tel çit:** saçakta X 99,5 ve 150,7.
- **Kural:** her çizimden önce `carp.py` çalışır (raflar ve alanlar × as-built DUVAR / PARAPET / KOLON). Çakışma kalmadan dosya gönderilmez.
  - İstisna: VAS 1–4 içindeki X 65,1 kolonu tasarım gereği hat içinde. Konveyörsüz VAS'ta masalar kolonun iki yanına bölünür.
  - Bir "çakışmayı" düzeltmeden önce tasarımın bunu bilerek mi yaptığına bakılır (v7.1 hatası).

## 2. Yerleşim v7.3 (plan koordinatı, m)
- **Batı (VAS / sevk):**
  - Rampa X 37,6–47,8 / Y 7–36,1.
  - Sevk tamponu X 48,4–57,6 / Y 16,1–26,6 (97 m², 9 sıra × 3 = 27 palet).
  - Streç Y 27,0–30,6.
  - Şef ofisi X 48,1–56,6 / Y 31,0–40,5 (soyunma odasının kuzeyinde, aynı ölçü).
  - Mal kabul X 57,9–76 / Y 16,1–22,4 (114 m²).
  - **VAS 1–4: X 59–71, Y 22,6–44,2, her biri 5,4 m (65 m²).**
    - Hat içinde 1,7 m servis koridoru. Masalar 2-2-1 kişi düzeninde.
    - Giriş doğu uçta, çıkış batı uçta. X 65,1 kolonunda masalar bölünür.
  - VAS transpalet koridoru X 56,8–59 (2,2 m), Y 31–44,3.
  - Yarı mamül bekleme X 71,4–76 (V2, 20 palet).
  - Stokla X 57–70 / Y 48,6–51,8.
  - Serbest alan Y 52,2–59,1.
  - Kalite / iade X 49,2–70 / Y 59,5–63,9.
  - VAS 5–6 (2027 yedek) X 70,6–81,7.
- **Ana koridor:** Y 44,3–48,2, X 56,8'den başlar. X 99,1 duvarını 4. sıranın güney 1 gözü kaldırılarak geçer. Alternatif: duvarda Y 45,2–48,2 açıklık.
- **ADEYA sırt sırta (12 sıra):**
  - 1/4/7/10. sıralar kolon bantlarında kesik.
  - 4. sıra: güney göz 01 yok (geçiş). Batı yüz göz 07–09 yok (duvar).
  - 1. sıra alt göz 1–3 B2B yüzü (18 yer), göz 4–9 esnek.
  - 8–12. sıra uzatma Y 35,8–44,2 (+360). 13. sıra tek yüz (+114).
- **Drive-in:** 5 derinlik × 4 kat = 20 palet/şerit.
  - Bloklar X 48,4–98,85 (35 şerit), X 99,45–132,95 ve X 134,15–151,5 (35 şerit) → 70 şerit.
  - Kapı önü boşlukları İhsan'ın uyarısıyla kaldırıldı. ADEYA 69 diyor.
  - Drive-in koridoru Y 12,4–16,1, duvarda ikiye bölünür.
- **E-ticaret kampanya lokasyonu:** X 85–98,8 / Y 48,6–63,9 (K-01…24, lansman / Z).
- **Hücreler:**
  - H1 X 105,7–116,9, H2 X 129,1–140,3, ikisi de Y 49,0–60,2. Hücre 11,2 m, ada 5,84 m.
  - Döngü koridoru 1,8 m, tek yön, 30,6 m. Giriş/çıkış paketlemeye bakan kenarda.
  - 29 göz (dış 17 + ada 12) × 5 kat = 145 göz/hücre.
  - Ada içi kapalı, ölü alan. H2 kolonları orada.
  - **H1 açıklığı (v8.10): Y 55,5–59,32**, kolon X 116,1 doğu raf hattının ucunda (açıklıktan 0,7 m kuzeyde); döngüde kolon önü net 1,58 m (düz yol).
- **Paketleme:** X 117,4–128,6, 16 istasyon. K1 X 123,1 → güney kapı X 121,3 ("K2 121").
- **Koli / dolgu / boş araba:** X 100,2–105,2. Hücre güneyleri Y 60,6–63,9 boş araba / koli.
- **Hazır paket:** X 140,4–151,5, ana koridordan beslenir.
  - Mamül raf: batı Y 49,4–54,8, doğu Y 48,6–54,0 (kolon).
  - Paketli raf: batı 1 göz, doğu 3 göz.
  - HP hattı X 145–147, fatura Y 62,5–63,6.
  - Çıkış X 140,4–144,9 → K2 139.
- **Saçak (Y 64,7–71, X 100,2–150,5):**
  - K1 → X 123 tarayıcı + saptırıcı. K4-batı (HepsiJet) X 123 → 110 + batı masası 104–110. K4-doğu (Trendyol + Yurtiçi) X 123 → 141 + doğu masası 141–147.
  - K3 iptal. HP kolileri banda girmez: Trendyol ve Yurtiçi kafesi yanında, HepsiJet arabayla ≈15 m.
  - Kafes alanları: HepsiJet X 100,2–132,3, Trendyol 132,6–148, Yurtiçi 148,3–150,5.
  - Yanaşma şeridi Y 71–74,6.
- **Kapasite 4.070 palet** = ADEYA 2.196 (2.256 − 60 duvar) + uzatma 360 + 13. sıra 114 + drive-in 1.400.
  - **Kaçış (v8.9, İSG ile):** kuzey acil çıkış X 81,2 / 125,4 (drive-in tüneli) / 160,1 / 194,1; drive-in 68 şerit, toplam **4.030 palet**.
  - HP rafları bu toplamın dışında (paketli 48, mamül 2 × 24).
  - WMS sayımı: back-to-back 2.694 lokasyon (ADEYA göz listesi, plana göre +24, İhsan'la kapanacak) + drive-in 1.400.

## 3. Operasyon kararları
- **Veri:** ikas 2026 Ocak–Ekim. Ortalama 5.291 sipariş/gün, P95 8.470. Tekli sipariş %54,7.
- **Taşıyıcı payı:**
  - Tüm siparişler: HepsiJet %65,6 · Trendyol %30,7 · Yurtiçi %3,4.
  - Tekli: 52,5 / 44,3 / 2,6.
  - Paketleme hattı: HepsiJet + diğer 69,1 · Trendyol 27,3 · Yurtiçi 3,6.
- **Günlük akış (ortalama / P95):**

| Akış | Ortalama | P95 |
|---|---|---|
| HP → Trendyol/Yurtiçi kafesi | ≈500 | ≈800 |
| HP → HepsiJet (araba) | ≈555 | ≈890 |
| Paketleme → K4-doğu | ≈1.310 | ≈2.090 |
| Paketleme → K4-batı | ≈2.925 | ≈4.685 |

- **Hücre stoğu (`hucre_slot.py`, v7.5):**
  - 304 SKU iki hücrede aynı gözde (kitsiz 241). 5 lansman SKU kampanya lokasyonunda.
  - Besleme ≈3 günde bir, göz ihtiyacı 135,1 / 145, 203 kalem/gün.
  - Kat 2–3 toplama payı %68. Ergonomi kuralı: kat sırası 3 → 2 → 4 → 1 → 5; 5,5 L kavanoz yalnız kat 2/1.
- **Araba (v7.4):** raflı kafes, 100 × 70 × 160 cm.
  - Göz = sipariş, 10 desi (30 L) (Sedat, 20.11: siparişler en fazla 10 desi).
  - Göz iç ölçüsü 32 × 34 × 28 cm = 30,8 L (10,3 desi). Ayırıcı 1 cm, kat aralığı 30 cm.
  - Her katta 3 × 2 göz; iki uzun yüzden erişim.
  - 3 ergonomik kat, taban kotları 50 / 80 / 110 cm, en üst göz üst kenarı ≈140 cm → 18 göz.
  - En alt tabla (≈20 cm) yalnız 10 desiden büyük sipariş ve boş koli için.
  - Sefer başına ≈17 sipariş. **Araba ihtiyacı 30** (P95 WIP 456 sipariş, %94 doluluk, %10 yedek). Eski 12 gözlü arabada 40'tı.
  - Mass Gainer kavanozu (Ø16,5 × 27,5) 28 cm göze dik sığar.
  - **Risk:** uzak sıradaki göze (35 cm derin) erişim için arabanın çevresinden dolaşmak gerekir. Çözüm seçenekleri: WMS önce yakın sırayı doldurur, ya da öne çekilebilir kasa kullanılır. Pilotta denenecek.
  - Görüş riski: 160 cm araba itilirken önü göstermez.
  - 3D'de araba yeni modelle (18 göz) gösteriliyor.
- **VAS (konveyörsüz):**
  - Su örümceği girdi getirir, dolu paleti streçe, boş paleti hat doğusundan batısına taşır.
  - Forklift V1 (drive-in → V2) ve V5' (stok → B2B) işlerini yapar.
  - Verim toz 160, vitamin 370 adet/adam-saat (KPI).
- **Kitler (v7.4, `Fitness paketi vb tüm bomlar.xlsx`):**
  - BOM: 409 karma koli, 1.122 bileşen satırı.
  - Eşleşme: ikas kit SKU'larının 195/274'ü (kit talebinin %78'i). Bileşen 1.050/1.122. Eşleşmeyenler tester, bazı tekli bar aromaları ve PEA 1,6 kg.
  - Kit satırı günde 1.160:
    - 5 HP kiti 441
    - BOM'dan bileşene açılan 403
    - BOM'suz kit kutusu 315 (Protein Bar Karma Kutu 181, 32'li paket 43; tek ürün gibi hücreden toplanır, varsayım)
  - **HP kiti kuralı:** tekli siparişler HP'den çıkar. Çok ürünlü siparişte hazır kit kutusu hücreden 1 satır olarak toplanır; payı 1 − tekli sipariş payı (Günlük Vitamin %86, Fitness %21).
  - **Hücreye ek yük günde +1.860 satır** (yıl ortalaması; hücre satırı 7.502 → 9.365, +%25). Satır/sipariş 2,06 → ≈2,57.
    - 2 HP kitiyle +2.742 olurdu; 5 HP kiti günde 882 satır azaltıyor.
  - Bar ve shaker bileşenleri paket masasına gider (+210 satır/gün).
  - **Ek toplayıcı:** normal gün +1,7 kişi, P95 +3,3 kişi (120 satır/saat, 7,5 saat). 2 HP kitiyle +2,6 / +4,9 olurdu.
  - **Ek HP işi:** yeni 3 HP kiti günde ≈293 kit (yıl ortalaması). 45 sn/kit-kişi ile normal gün ≈3,1 saat, P95 ≈5,9 saat (≈0,4–0,8 kişi).
    - Süre varsayımı HP cycle time ölçümünden: 2 desi 36 sn, 3 desi 53 sn/adet-kişi.
  - **Kadro:** hücre toplayıcısı normal 4+3 → ≈5+4, P95 7+6 → ≈9+7. HP +1 kişi (P95). Pilotla teyit edilecek.
- **Kadro:**
  - Sahada normal 20, P95 36: hücre 4+3 (P95 7+6), paketleme 9 (16), HP hattı 2 (3), HP topla 2 (4).
  - Kadroya sayılmayanlar: besleme (toplayıcılar boş zamanda), kargo ekibi 2–3, operasyon şefi 1.
  - Modele göre 27,8 → ≈18,1 FTE.
- **Kutu dağılımı (desi; `Ağustos-eylül -ekim kullanılan Kutu dağılımı.xlsx`, Trendyol sayfası 20.11'de eklendi):**

| Kapsam | Kargo/gün | Ort. desi | 1 desi | ≤2 | ≤3 | ≤5 | ≤7 | ≤10 |
|---|---|---|---|---|---|---|---|---|
| HepsiJet + Yurtiçi (Ağu–Eki, 244.313) | ≈2.650 | 2,41 | %52 | %68 | %79 | %93 | %97 | %99,76 |
| Trendyol (Eyl+Eki, 81.450) | ≈1.335 | 1,38 | %80 | %90 | %96 | %99,3 | %99,8 | %99,98 |
| **Tümü (Eyl+Eki, 239.808)** | **≈3.930** | **1,99** | **%63** | **%77** | **%86** | **%96** | **%98,6** | **%99,85** |

  - Tümünde desi payı: 1 %62,7 · 2 %14,5 · 3 %8,6 · 4 %1,6 · 5 %8,3 · 6 %1,5 · 7 %1,4 · 10 %1,1. Tepe noktaları 1/2/3/5/7/10 koli ölçüleriyle eşleşiyor. 10 desiden büyük günde ≈6 kargo.
  - Trendyol hafif çünkü %79'u tekli sipariş (veri temeli §3). 1 desi koli (koli1) paket masasında ve HP'de elin altında olmalı.
  - Hacim mutabakatı (Eyl+Eki, ikas 4.323 sipariş/gün): Trendyol ≈%100 tutuyor. HepsiJet + Yurtiçi ≈2.596/gün, ikas'ta Trendyol dışı ≈2.996 → **≈%13 (≈400/gün) eksik**, nedeni bilinmiyor (dosya kapsamı/çoklu koli/Hepsiburada?). Düşük öncelik.
- **Kargo ayırma:** WMS kargo barkodundan taşıyıcıyı tanıyor (Sedat, 20.11) → K4 saptırıcı WMS ile çalışır.

## 4. WMS lokasyon kodlaması (`Kazan_WMS_Lokasyon_ve_Atama_v7.5.xlsx`)
- **Back-to-back:** `B{sıra 01–13}{yüz B/D}-{göz 01–10}-{kat 1–4}{poz A/B/C}`. Göz 01 güney ucu. Güneyden 5. göz tünel.
  - B04 göz 01 yok. B04B göz 07–09 yok. ADEYA göz numaraları korunur.
- **Drive-in:** `D{şerit}-{kat 1–4}`, D01–D70.
- **Hücre:** `H{1/2}{yüz D/A}-{göz}-{kat}{bölme}`. Göz no = döngü sırası, giriş = 01, 29 göz.
- **Diğer:** kampanya `K-01..24`. Alan kodları MK, ST, STR, VG, VS, Q, PM, HP, KRG.
- **Kapsam:** 337 SKU (v7.5, kit bileşenleri, HP kit kutuları ve BOM'suz kit kutuları dahil). Rezerv 14 günlük talepten.
- **Canlı öncesi gerekenler:** ERP aktif SKU listesi (barkodla ikas eşleşmesi), koli/palet lojistik verisi, taşınma anı stok (lot/SKT, FEFO drive-in'e konmaz), ADEYA kesin göz/tünel.

## 5. Dosyalar (`Kazan_Tum_Dosyalar_v8.10_TAM.zip`, 116 dosya; içinde BENIOKU.md)
- **01_Cizim:** `Kazan_v8.10_AsBuilt_Yerlesim.dxf` (ana, katmanlı; PO_KACIS dahil) · `.dwg` (R2000, düz; `05_Kaynak/dxf_r2000_flat.py` + LibreDWG dxf2dwg ile) · `.png` · `Kazan_v8.10_H1_giris_detay.png` · `Kazan_Kacis_Mesafesi_v8.9.png`.
- **02_Simulasyon:** `Kazan_v7.5_Hucre_HazirPaket_3D.html`, `Kazan_v7.3_VAS_Konveyorsuz_Simulasyon_3D.html` — **eski** (H1 açıklığı, 6 HP kiti, tüneller yok). İnternet gerekir (three.js CDN).
- **03_Excel:** `Kazan_Kit_Kutu_Araba_v8.10.xlsx` (formüllü, girdiler sarı, "2027 Kapasite" sayfası) · `Kazan_Eticaret_Hucre_Stogu_v8.10.xlsx` · `Kazan_WMS_Lokasyon_ve_Atama_v8.10.xlsx` · `Kazan_B2B_Toplama_Yuzu_v6.4.xlsx` (geçerli).
- **04_Dokuman:** bu not (v8.10/v8.11).
- **05_Kaynak:** önceki yapı + değişenler: `yerlesim/hucre_geo.py` (açıklık parametreli), `veri/layout.json` (DI 68, KACIS, H1 acik_y/kolon_y), `kit/kit_explode.py` (6 HP kiti, 32'li = 3 satır), `hat_stogu/` (df_kit, hucre_* yeniden), `kacis/` (kaçış mesafesi: kacis.py, kac2/kac3, png89), `dxf_r2000_flat.py`. `kit/bom_map.py` girdi olarak `kit/in/bom.xlsx` (= "Fitness paketi vb tüm bomlar.xlsx") ister.
- **Çalıştırma sırası:**
  1. As-built'i DXF'e çevir, `bg.py` ile `asb_raw.pkl` ve `asb_plan.pkl` üret.
  2. `veri/*.json` → `/home/claude/work/out/`.
  3. `layout.py` → `carp.py` → `dxfout_v70.py`.
  4. `kit/bom_map.py` → `kit/kit_explode.py` → `df_kit.pkl` → `hat_stogu/df.pkl`.
  5. `hucre_slot.py` → `xl_hucre.py` → `wms/lok.py` → `xl_wms.py` → `kit/xl74.py`.
- **Artifact'ler:**
  - 3D https://claude.ai/artifact/1ESkc5Xsxv6Kaduc3zDDDt (hücre + HP, v7.5)
  - Onay sunumu https://claude.ai/artifact/FaFp72xqyCmKRD2azgR32w (v6.7)
  - Şartname https://claude.ai/artifact/AZt5q3WEdkmRghjgH2zAxv (v6.9 saçak var; araba, hücre rafı, kapı adları eski)

## 6. Açık işler (öncelik sırası)

**24.11 onay toplantısına kadar (Claude):**
- a) ~~×1,5 kapasite kontrolü~~ **yapıldı (v8.6).** Excel/3D yeniden üretimi sunumla birlikte.
- b) Onay sunumunu güncelle (v6.7 → v8.x): 6 HP kiti, araba 18 göz/30 (2027 ≈45), kaçış tünelleri ve 4.010 palet, desi dağılımı, 2027 ×1,5 etkisi.
- c) Toplantıda karar istenecekler listesi: 3 kaçış tüneli, P95'te paketleme istasyonu (16 vs ≈24), mimari X 48 açıklığı, forklift/RT kiralama, pilot.
- d) Pilot planı (yerleşim, ölçüm formu, süre, kişi).
- e) Şartname güncellemesi (araba, hücre rafı, tünel, kapı adları) — toplantı sonrasına kalabilir.

1. ~~Bugünkü 3. HP kiti~~ **KAPANDI (20.11):** Fitness Çikolata/Ahududu → model 6 HP kiti. Kalan: Excel/3D'yi 6 kitle yeniden üret. Kadro ≈5+4 (P95 9+7) değişmez, ek toplayıcı ≈+1,6. **Araba** (18 göz, 30 adet) şartnameye; uzak sıra erişimi pilotta.
   - ~~2027 büyümesi~~ **KAPANDI (20.11):** e-ticaret ×1,5. Veri temeli §11'deki %20/yıl geçersiz. Genel %80 bütçeyle teyit edilecek.
1b. ~~2027 ×1,5 kapasite kontrolü~~ **YAPILDI (v8.6):** göz sığıyor (besleme 2 günde bir); darboğaz P95 insan yoğunluğu (hücre 12,4 kişi/hücre, paketleme 24 > 16 istasyon); araba 45. Karar: vardiya mı, 3. hücre mi (öneri: önce vardiya, büyüme teyidinde rezerv alana 3. hücre).
2. **İhsan:**
   - ADEYA çizimini as-built'e oturtma
   - 4. sıra
   - drive-in 69/70 şerit ve X 99,1 bölünmesi; **2 kaçış tüneli** (yangın kapısı X 81,2 ve 125,4 eksenine ortalı, koruma ağı + bariyer) → 68 şerit
   - hücre rafı 29 göz × 2
   - konveyör: K3 yok, K4 iki yönlü + saptırıcı
   - H1 doğu raf hattı Y 49,88–54,2 (kolona kadar, 2 göz), açıklık Y 55,5–59,32 (v8.10)
   - ana koridor kolon hattında net ≈3,0 m: forklift/RT trafiği kuralı
   - **forklift + RT spesifikasyonu (kiralama için):** raf en üst kotu / kaldırma yüksekliği, koridor genişliği (RT dönüş), drive-in'e girecek araç tipi ve şase genişliği, palet yükü (kg), önerilen adet
3. ~~Kuzey kapılar~~ **KAPANDI (20.11, İSG ile, v8.9):** acil çıkış X 81,2 / 125,4 / 160,1 / 194,1; 2 tünel; en uzun kaçış 44,5 m (pay 0,5 m — rampa kapıları ve sevk tamponu geçişi İSG'ye teyit); kapasite 4.030. Kalan: tünel tasarımı İhsan'a.
4. **Mimari (durum bilinmiyor, 20.11):** rampa X 48 duvarı Y 16–30 açıklığı (**kritik**, mal sahibi/mimara sorulmalı); X 99,1 Y 45,2–48,2 açıklığı (isteğe bağlı, 4. sıra göz 01'i geri kazandırır).
5. ~~Karma Kutu ve 32'li paket~~ **KAPANDI (20.11):** Karma Kutu tek ürün; 32'li paket = 3 × 12'li display, siparişte toplanır (3 satır). Kalan: eşleşmeyen tekli bar aromaları (düşük etki, 1,4 satır/gün).
6. Sunum ve şartnameyi v7.5'e güncelle.
7. Ostim pilotu (planlanmadı, 20.11; planı Claude hazırlayacak): 1,8 m koridor, araba maketi, satır/saat ≥ 80, hata < %0,3.
8. **COO + GM onay toplantısı: 24.11.2026 (Salı).**
9. **WMS sözleşmesi (YENİDEN AÇILDI, v8.8):** taslakta e-ticaret modülü hariç; yetenekler sözleşmede yok. İmzadan önce kapsam, lisans sayısı, SLA, kabul ve entegrasyon ekleri eklenmeli (ayrıntı v8.8).

## 7. Veri envanteri ve eksikler (denetim 20.11.2026)

**Var ve güncel:**
- Sipariş verisi: ikas 01.01–31.10.2026 (1,61 M sipariş, 814 SKU) ve 6 CSV.
- 2027 büyüme varsayımı: e-ticaret ×1,5 (kesin, Sedat 20.11). Genel %80 (teyit bekliyor).
- Zemin: as-built 20.11 DWG ve ADEYA raf projesi (PDF + DWG 22.10).
- Kit: BOM.
- Kutu: Ağu–Eki HepsiJet+Yurtiçi + Eyl–Kas Trendyol desi dağılımı.
- Ölçümler: cycle time (e-ticaret, HP), Haftalık KPI v3.17 (16.11).
- Kadro: personel dağılımı.
- Hesap çıktıları: TAM zip içinde v7.5 Excel'ler, 3D, çizim, kaynak kod.

**Var ama eski veya eksik:**
- Ürün ölçüleri: ağırlık yok; 120 varyantın ölçüsü eksik (satırların %4,3'ü).
- Proje takip: 27.10'dan beri güncellenmedi.
- Şartname: v6.6 doküman, v6.9 artifact.
- Onay sunumu: v6.7.
- Araba ergonomi analizi: eski araba üzerine.
- 2027 talebi: toplam düzeyde. Aralık bütçesinden istenenler (bütçe raporlamaya mail gitti): (1) SKU × ay adet, (2) SKU × ay × kanal (e-ticaret web/mobil/pazaryeri, Bim/VAS, B2B), (3) mamul ve ticari ürün hedef stok günü (palet ihtiyacını belirler), (4) 2028+ kanal bazında büyüme yönü (kira 10 yıl, alan rezervi buna göre).

**Eksik — canlıdan önce şart:**
1. ERP aktif SKU listesi ve ikas↔ERP barkod eşleşmesi (IT/ERP).
2. SKU ağırlıkları, eksik ölçüler, koli içi adet, koli ölçüsü/ağırlığı, palet başı koli (Sedat / satınalma).
3. Taşınma anı stok: lot, SKT, palet sayısı (depo / ERP).
4. ADEYA kesin göz/tünel listesi; drive-in 69/70 (İhsan).
5. ~~Bugünkü 3. HP kiti; Karma Kutu ve 32'li paket~~ (kapandı).

**Eksik — tasarımı keskinleştirir:**
6. B2B/VAS/Bim tarafı: sipariş/satır verisi, VAS koli/palet çıktısı, mal kabul araç/saat planı.
7. ~~Kutu dosyasının taşıyıcı kapsamı~~ (kapandı 20.11: Trendyol ayrı sayfada eklendi). Kalan: HepsiJet+Yurtiçi tarafında ikas'a göre ≈%13 eksik.
8. ~~Forklift tipi ve sayısı~~ (kapandı 20.11: kiralanacak, spesifikasyon İhsan'dan; §6-2).
9. ~~İSG kuzey kapı kararı~~ (v8.3: 3 tünel, İSG onayı bekliyor); mimari: rampa X 48 duvarı, X 99,1 açıklığı, saçak ruhsatı.
10. ikas satır verisi (parquet, kullanıcının bilgisayarında); sepet bazlı dalga simülasyonu için gerekli.
11. Ostim pilot ölçümleri: satır/saat ve hata oranı (1,8 m koridor, araba maketi).
12. WMS teklif dokümanları (bağlamda yok; yetenekler Sedat tarafından teyit edildi, 20.11).
13. Logo ölçü dosyası `Urun_Olcu_Agirlik_Logo_19112026.xlsx` bağlamda yok.