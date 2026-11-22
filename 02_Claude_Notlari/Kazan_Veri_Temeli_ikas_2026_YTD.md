# Kazan Depo Veri Temeli — ikas E-ticaret Siparişleri 2026 YTD

**Sabit referans veri.** Kazan e-ticaret hattı, toplama alanı, hazır paket, kargo çıkışı ve kadro hesapları bu dosyadaki değerlere dayanır. Kaynak: ikas sipariş export'u (Ocak–Ekim 2026, ürün satırı seviyesi). Son güncelleme 21 Kasım 2026 (bölüm 11: 2027 büyümesi ×1,5). ikas verisi Nisan dahil tam.

## 0. Kapsam ve veri kalitesi

| Kalem | Değer |
|---|---|
| Dönem | 01.01.2026 – 31.10.2026 (**304 gün**, tüm aylar tam) |
| Ürün satırı | 3.251.442 |
| Sipariş | **1.608.573** |
| Adet | 3.654.567 |
| Satılan SKU | 814 (son 30 günde satan: 606) |
| İptal / iade | İptal ≈ 0; parçalı iade 1.770 sipariş (%0,1) |
| Stok lokasyonu | Tek lokasyon (proteinocean) |

- **Nisan:** İlk Excel export'u eksikti (109 bin sipariş, tek ürünlü pay %13). 04.11.2026'da CSV olarak yeniden alındı: **207.605 sipariş**, tek ürünlü pay %54,4, 30 günün hepsi dolu. Aylar arasında mükerrer sipariş yok.
- **KPI doğrulaması:** Haftalık Operasyon KPI Raporu'na göre Ekim 1–26 arası günde ortalama 4.422 kargo çıktı. ikas'ta Ekim ortalaması günde 4.309 sipariş. ikas, depodan çıkan hacmi doğru yansıtıyor.
- **ERP ile hacim farkı:** ikas adetleri, "Yeni_Depo_Eticaret_Hat_Stogu_Plani" dosyasındaki ERP/faturalanan adetlerden düşük (ör. Protein Ocean kanalı Ocak: ikas 282 bin, plan 405 bin adet, ×1,43). Olası nedenler: paket ürünlerin ERP'de bileşenlere açılması, ikas dışı kanallar, faturalama zamanlaması. **Sipariş ve toplama satırı için ikas, stok adedi için ERP esas alınır; ikisi mutabakat ister.** ikas SKU kodu (ör. 6390010) ERP stok kodundan (ör. 010200100001) farklı, eşleştirme barkodla yapılır.

## 1. Aylık ve günlük hacim

| Ay | Sipariş | Günlük ort. | Günlük P95 | Maks gün |
|---|---|---|---|---|
| Ocak | 151.196 | 4.877 | 6.546 | 7.532 |
| Şubat | 174.783 | 6.242 | 8.060 | 11.601 |
| **Mart** | **231.406** | **7.465** | 10.301 | 10.828 |
| **Nisan** | **207.605** | **6.920** | 8.649 | 8.919 |
| Mayıs | 167.689 | 5.409 | 9.361 | 11.039 |
| Haziran | 132.363 | 4.412 | 5.544 | 5.935 |
| Temmuz | 142.002 | 4.581 | 5.590 | 6.202 |
| Ağustos | 137.806 | 4.445 | 7.006 | 8.154 |
| Eylül | 130.140 | 4.338 | 5.267 | 5.665 |
| Ekim | 133.584 | 4.309 | 5.378 | 5.735 |
| **Ortalama** | **160.857** | **5.291** | | |

- **Sezon:** Şubat–Mayıs yüksek sezon (Mart ve Nisan zirve, 208–231 bin). Haziran–Ekim 130–142 bin bandında sabit.

| Günlük dağılım (304 gün) | Sipariş/gün | Toplama satırı/gün | Adet/gün |
|---|---|---|---|
| Ortalama | 5.291 | 10.689 | 12.022 |
| Medyan | 4.926 | 9.880 | 10.963 |
| P75 | 6.170 | 12.663 | 14.353 |
| P90 | 7.846 | 16.279 | 18.468 |
| **P95 (tasarım günü)** | **8.470** | **17.991** | **20.364** |
| P99 | 10.716 | 21.846 | 25.900 |
| Maks (16.02.2026) | 11.601 | 28.159 | 30.300 |

- Maks gün / ortalama = 2,19. P95 / ortalama = 1,60. Mevcut hat stoğu planındaki 2,87 kampanya katsayısı toplam hacim için ihtiyatlı kalıyor. Hat stoğunda SKU bazlı pik katsayısı kullanılmalı (bölüm 4).
- Pik günler: 16 Şubat, 3–5 ve 23–31 Mart, 5–7 Mayıs, 17 Ağustos.

## 2. Saat ve gün profili (vardiya, cut-off)

**Haftanın günü (ortalama sipariş, ortalamaya oran):** Pzt 6.082 (1,15) · Sal 6.085 (1,15) · Çar 5.792 (1,09) · Per 5.338 (1,01) · Cum 4.856 (0,92) · Cmt 4.238 (0,80) · Paz 4.683 (0,88).

**Saatlik geliş (günlük ortalama sipariş):**

| Saat | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sipariş | 247 | 155 | 90 | 53 | 32 | 24 | 28 | 48 | 95 | 165 | 234 | 291 |
| **Saat** | **12** | **13** | **14** | **15** | **16** | **17** | **18** | **19** | **20** | **21** | **22** | **23** |
| Sipariş | 321 | 346 | 347 | 354 | 316 | 294 | 278 | 279 | 297 | 325 | 345 | 328 |

- 16:00 öncesi gelen: %53,5. 16:00–24:00: %46,5. 00:00–08:00: %12,8.
- **Sabah vardiyası başladığında günlük işin ≈ %59'u hazır bekliyor** (önceki gün 16:00 – bugün 08:00).
- Cut-off günü (önceki gün 16:00 – bugün 16:00): ortalama 5.274, P95 8.522, maks 10.789 sipariş.
- Gün içinde en yoğun saatler 12:00–16:00 (saatte 320–355 sipariş).

## 3. Sipariş profili

| Sipariş başına farklı SKU | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |
|---|---|---|---|---|---|---|---|
| Pay | **%54,7** | %21,4 | %10,2 | %5,7 | %3,5 | %2,1 | %2,5 |
| Kümülatif | %54,7 | %76,0 | %86,2 | %91,9 | %95,4 | %97,5 | %100 |

- Sipariş başına ortalama 2,02 farklı SKU, 2,27 adet. Tek adetli sipariş %47,5. Satır başına ~1,13 adet: **tekli (each) toplama baskın.**

| Kanal | Sipariş (pay) | Ort. SKU | Ort. adet | Tek SKU payı | Ort. tutar (TL) |
|---|---|---|---|---|---|
| Proteinocean (web) | 937.276 (%58,3) | 2,38 | 2,71 | %42 | 1.455 |
| Trendyol | 493.758 (%30,7) | 1,30 | 1,41 | **%79** | 749 |
| Mobil Uygulama (+Neon, Ekim'den) | 120.199 (%7,5) | 2,49 | 2,83 | %40 | ≈1.445 |
| Hepsiburada | 51.204 (%3,2) | 1,24 | 1,39 | **%83** | 775 |
| N11 + Amazon | 6.118 (%0,4) | 1,12 | 1,22 | %90 | — |

- Pazaryerleri (Trendyol, Hepsiburada, N11) **%34,2**. Bu siparişlerin ~%80'i tek ürünlü, **tekli / pazaryeri hızlı hattına** uygun.
- Web ve mobil çok ürünlü (ort. 2,4–2,5 SKU), ana hatlara gider.

## 4. SKU hızı ve slotting (ABC × XYZ)

Toplama satırına göre ABC (A = satırların %80'i, B = %80–95, C = %95–100). XYZ haftalık değişkenliğe göre (X: CV < 0,5, Y: 0,5–1, Z: > 1).

| | X (stabil) | Y | Z (dalgalı) | Toplam SKU | Satır payı |
|---|---|---|---|---|---|
| **A** | 63 SKU · %43,1 | 26 · %15,3 | 38 · %21,6 | **127** | %80 |
| **B** | 80 · %6,4 | 49 · %4,2 | 50 · %4,3 | **179** | %15 |
| **C** | 38 · %1,0 | 143 · %2,4 | 327 · %1,7 | **508** | %5 |

**SKU sayısına göre kümülatif toplama satırı:** 20 SKU %40 · 50 SKU %59 · 100 SKU %75 · 150 SKU %83 · 200 SKU %89 · 300 SKU %95 · 400 SKU %98.

- **Altın bölge:** İlk ≈ 50 SKU satırların %59'u. AX grubu (63 SKU, %43) hat stoğuna en uygun grup.
- **Lansman SKU'ları** (Whey Peanut Chocolate, Creatine Lansman serisi, Cream of Rice Lansman, Collector Edition) yıllık toplamda A sınıfında görünüyor ama günlük P95/ortalama oranları 5–11 arası ve güncel hızları düşük. **Esnek lansman / kampanya lokasyonu ve ön paketleme** gerekir, kalıcı hat stoğuna konmamalı.
- **Hediye / eklenti ürünler:** Pocket Shaker siparişlerin %13'ünde var, %80'i ücretsiz. Protein Bar Tekli 30g, Tester, Huni ve Pillbox da benzer. Fiyatsız satırlar tüm satırların ~%8,6'sı. **Paket masasında tutulursa toplama satırının ≈ %9'u hattan çıkar.**
- C sınıfı 508 SKU satırların %5'i: ortak kuyruk, raf alt seviyesi, RF toplama.
- SKU bazlı baz/son 90/son 30 günlük talep, P95, maks ve XYZ değerleri `SKU_Profil.csv` dosyasında. Hat stoğu = baz günlük × SKU P95/ortalama × kapsama günü.

**İlk 15 SKU (toplama satırı):**

| ikas SKU | Ürün | Satır | Baz günlük adet | P95 günlük | P95/ort | XYZ | Tekli sipariş payı |
|---|---|---|---|---|---|---|---|
| 6390010 | POCKET SHAKER 500 ML | 213.855 | 710 | 1.296 | 1,8 | X | %5 (eklenti) |
| 6090019 | CREATINE Aromasız 120g | 136.183 | 518 | 827 | 1,7 | X | %53 |
| 6091016 | CREATINE Aromasız 300g | 128.073 | 438 | 740 | 1,7 | X | %61 |
| 6610255 | COLLAGEN Ahududu 250g | 84.672 | 332 | 802 | 2,4 | Y | %74 |
| 6678637 | GÜNLÜK VİTAMİN PAKETİ | 82.631 | 277 | 554 | 2,0 | X | %14 |
| 6002920 | WHEY LANSMAN Peanut Choc. 400g | 69.684 | 369 | 3.194 | 8,7 | Z | %33 |
| 6740013 | PROTEİN BAR KARMA KUTU | 55.070 | 276 | 607 | 2,2 | Y | %22 |
| 6550032 | WHEY Çikolata 400g | 54.298 | 187 | 442 | 2,4 | Y | %40 |
| 6620186 | MAGNESIUM BISGLYCINATE | 53.744 | 188 | 309 | 1,7 | X | %13 |
| 6002951 | CREATINE LANSMAN Raspberry Pineapple | 53.490 | 267 | 2.017 | 7,6 | Z | %41 |
| 6620049 | ZMA | 48.922 | 165 | 309 | 1,9 | X | %14 |
| 6002227 | CREATINE Pineapple Mango 120g | 48.672 | 197 | 951 | 4,8 | Z | %48 |
| 6550155 | WHEY Bisküvi 400g | 42.962 | 146 | 308 | 2,1 | X | %46 |
| 6720039 | CREAM OF RICE Çikolata 1kg | 38.193 | 134 | 241 | 1,8 | X | %29 |
| 6630017 | OMEGA 3 | 34.765 | 118 | 190 | 1,6 | X | %6 |

## 5. Hazır paket (tek ürünlü sipariş)

- Tek ürünlü siparişler toplamın %54,7'si. Yıl geneli: ilk 20 SKU+adet kombinasyonu siparişlerin %25,4'ü, ilk 50 kombinasyon %34,4'ü.
- **Güncel hız (son 90 gün, Ağu–Eki), N kombinasyonun toplam siparişe payı:** 9 → %20,1 · 12 → %22,7 · 16 → %25,2 · 20 → %27,4 · 23 → %28,7 · 27 → %30,3 · 43 → %35,2.
- **KPI doğrulaması:** Ekim'de hazır paket kullanımı %20, hedef %25. Mevcut 9 SKU (≈ 12 kombinasyon) tavanı %22,7, gerçekleşen bunun %88'i. **Hedef SKU eklenmeden tutmaz.** %88 yakalamayla %25 için ≈ 23 kombinasyon gerekir.
- **KPI raporu v3.6, Hazır Paket Hedef sayfası (04.11.2026, ikas Ekim tekli siparişleri, ürün + adet bazında):** Mevcut oran %20,1. **%25'e 5. satırda ulaşılır:** (1) Strawberry Banana ×2 üretimini artır (talep 135/gün, kullanım 53), (2) High+ Strawberry Cheesecake yeni (65/gün), (3) Strawberry Banana ×1 üretimini artır (118/gün, kullanım 47), (4) Protein Fusion 80 Brownie acil yeniden üret (53/gün, kullanım 2), (5) Creatine Aromasız 1kg yeni (41/gün). Tüm liste uygulanırsa %31,3. **Çıkarılacaklar** (tekli talep < 8/gün): Pre-workout Cool Lime Lansman (3,9), Cream of Rice Lansman Peanut Choc (7,5), Collagen Şeftali (7,4). Eylül listesindeki Whey Almond Coffee Ekim'de 2,5/güne düştü, listeden çıktı.
- Aday listesi bölüm 9'da. Liste son 90 günün hızına göre seçilmeli; lansman SKU'larının yıllık sırası yanıltıcı. Tam liste `Tekli_Siparis_HazirPaket.csv` dosyasında.

## 6. Birlikte toplanan SKU'lar

- En sık ikililer: Shaker + Günlük Vitamin Paketi, Creatine 120g + Shaker, Whey Peanut Choc + Shaker, Shaker + Whey Çikolata 400g.
- Yüksek lift: ZMA + Günlük Vitamin Paketi (≈4,9), Magnesium + Günlük Vitamin Paketi (≈4,0), Shaker + Whey Çikolata 1,6kg (≈4,2). **Vitamin grubu (ZMA, Magnesium, D3K2, Omega 3, Günlük Vitamin Paketi) yan yana slotlanmalı.**
- En sık tam sepetler tek tek ≤ %0,25. Kit/ön paket kazancı çok ürünlü sepette değil, tekli siparişte.
- Liste: `SKU_Birlikte_Toplama.csv`.

## 7. Kargo ve coğrafya (sorter / çıkış tasarımı)

**Taşıyıcı yapısı (sabit kabul, Sedat Birinci 04.11.2026):**
- Site (web), mobil uygulama ve Hepsiburada siparişlerini **HepsiJet** taşır.
- **Trendyol** kendi kargosunu kendisi alır.
- **Kapıda ödemeli** siparişler (sadece site ve mobilde) **Yurtiçi Kargo** ile gider.

| Taşıyıcı çıkışı | Kapsam | Sipariş payı |
|---|---|---|
| **HepsiJet** | Site + mobil (kapıda ödeme hariç) + Hepsiburada | **%65,6** |
| **Trendyol** | Trendyol siparişleri | **%30,7** |
| **Yurtiçi Kargo** | Kapıda ödeme (nakit + kapıda kredi kartı) | **%3,4** |
| Netleşecek | N11 + Amazon | %0,4 |

- Kapıda ödeme payı: site %4,9, mobil %7,1, Neon mobil %4,7. Pazaryerlerinde yok.
- Sorter / kargo kafesleri **taşıyıcıya göre 3 çıkış** olarak tasarlanır, il ayrımı gerekmez.
- İl dağılımı: İstanbul %31,3 · Ankara %10,1 · İzmir %7,7 · Antalya %4,6 · Bursa %3,7 · Kocaeli %3,7. İlk 3 il %49, ilk 10 il ≈ %69.

## 8. Müşteri

- 1.109.128 tekil müşteri (anonim anahtar). %81,2'si dönemde tek sipariş vermiş. Tekrar eden müşteriler siparişlerin %44'ünü oluşturuyor.

## 9. Kazan Hat ve Kadro Planı'na işlenen kararlar (04.11.2026)

- **Hacim bazı:** Kadro normal aya göre kurulur (varsayılan **135 bin sipariş/ay**, Haz–Eki 130–142 bin). Yüksek sezon (Şubat–Mayıs; Mart 231 bin, Nisan 208 bin) fazla mesai ve geçici kaynakla karşılanır. Planda hazır seçenekler var: normal ay 135 bin, yıllık ortalama 161 bin, pik ay 230 bin.
- **Pik gün kontrolü:** Plan, seçili kadronun P95 gününü (8.470 sipariş) fazla mesaiyle karşılayıp karşılayamadığını gösterir. 135 bin bazında 2 hat (24 istasyon) çıkıyor. P95 gününde 10 saatle ≈ 29 kişi gerekiyor, bu yüzden **3. hat yuvası yedek ayrılmalı**.
- **Hazır paket SKU sayısına bağlandı:** Beklenen oran = son 90 günde en sık N kombinasyonun payı × yakalama oranı (%88). **%25 hedefi ≈ 23 kombinasyon** demek (bugün ≈ 12). Hazır paket stok alanı buna göre büyütülmeli.
- **Tekli / pazaryeri hızlı hattı:** Son aktif e-ticaret hattı tek ürünlü siparişlere ayrılır (pazaryeri %34,2, bunların ~%80'i tek ürünlü).
- **Hediye / eklenti bölgesi:** Shaker, tester, huni ve tekli bar paket masalarına beslenir.
- **Kargo çıkışı:** 3 taşıyıcı kafesi: HepsiJet, Trendyol, Yurtiçi (kapıda ödeme).

**Hazır paket aday listesi (son 90 gün, günlük sipariş; "mevcut" = bugün hazır paketlenen):** Creatine Aromasız 300g ×1 (246, mevcut) · Creatine Aromasız 120g ×1 (202, mevcut) · Collagen Ahududu ×1 (108, mevcut) · Creatine Strawberry Banana 120g ×2 (64, mevcut SKU) · Creatine Fruit Fusion 300g ×1 (59, mevcut) · Strawberry Banana ×1 (56, mevcut) · Whey Çikolata 400g ×1 (54, mevcut) · Whey Bisküvi 400g ×1 (53, mevcut) · **Creatine Aromasız 1kg ×1 (44)** · **Whey Lansman Almond Coffee ×1 (44)** · Pineapple Mango 120g ×1 (35, mevcut) · **Cream of Rice Çikolata ×1 (32)** · **Pocket Shaker ×1 (31)** · Fitness Paketi Çikolata/Karpuz ×1 (27, mevcut) · **Pea Protein Lansman Peanut Choc ×1 (26)** · **High+ Strawberry Cheesecake ×1 (26)** · **Günlük Vitamin Paketi ×1 (25)** · **Creapure ×1 (25)** · **Fitness Paketi Bisküvi ×1 (23)** · Strawberry Banana ×3 (23) · **Creatine Pineapple Mango (2. varyant) ×1 (21)** · **Magnesium Bisglycinate ×1 (19)** · Creatine 120g ×2 (18).

## 10. Koli dağılımı ve otomasyon değerlendirmesi (ISITEC / ADEYA, 10.11.2026)

**Kaynak:** Raf firması sahibi İhsan'ın paylaştığı "Protein Ocean Sipariş Paketleme Analizi" (10.09.2026, bir günlük 7.000 sipariş). Tarihi ve ham dosyası istenecek.

| Koli | Dış ölçü (cm) | Hacim (L) | Yaklaşık desi | Sipariş | Pay |
|---|---|---|---|---|---|
| koli1 | 13 × 13 × 21 | 3,55 | 1,18 | 2.831 | **%40,4** |
| koli2 | 17 × 27 × 13 | 5,97 | 1,99 | 1.382 | **%19,7** |
| koli3 | 23 × 30 × 13 | 8,97 | 2,99 | 824 | %11,8 |
| koli4 | 19 × 27 × 26 | 13,34 | 4,45 | 1.251 | %17,9 |
| koli6 | 24 × 24 × 30 | 17,28 | 5,76 | 414 | %5,9 |
| koli10 | 34 × 30 × 30 | 30,60 | 10,20 | 251 | %3,6 |
| koli26 | 43 × 62 × 30 | 79,98 | 26,66 | 48 | %0,7 |

- **koli1 + koli2 = %60.** Paket masasında bu iki koli elin altında, koli10 ve koli26 merkezi noktada tutulur.
- koli6 → koli10 hacim sıçraması %77, koli10 → koli26 %161. Ara ölçü desi maliyetini düşürebilir.
- Analizde tekli sipariş %39, ikas'ta tek SKU %54,7. Fark büyük ihtimalle hazır paket siparişlerinin analizde olmaması (54,7 − ~20 ≈ 35). Teyit edilecek.
- Analizdeki kapasite hesabı (2 sorter, 14.000 sipariş/vardiya) sorter içindir; darboğaz paketleme. 22 kişilik kadro (4 toplama, 4 besleme, 2 aktarma, 12 paketleme) 7.000 siparişte paketçi başı ~83 sipariş/saat demek, gerçekçi değil. Karşılaştırılan baz kadro verilmemiş.

**Teklif edilen otomasyon (sunum 08.07.2026):**

| Ürün | Kapasite | Kısıt | Bize uygunluğu |
|---|---|---|---|
| ISIWALL 3D putwall | 2.500 adet/saat, 100 göz | ürün en fazla 380×300×150 mm, 3 kg | Çok ürünlü siparişler için **1 adet yeter** (P95 gün ≈ 7,4 saat). Teklifteki 2 adet gereksiz. Büyük kavanozlar sığmayabilir. |
| ISIBAGGER torba paketleme | 600 sipariş/saat | torba 200–500 × 420–700 mm | Tekli hatta pilot adayı (koli1–2 ürünleri). Ezilme testi şart. "80 kW" teyit edilecek. |
| ISIWALL 2D kargo sorter | 1.800 adet/saat | — | Gereksiz: 3 taşıyıcı kafesi yeterli. |
| AutoStore (22×62 m, 22.000 sepet, 15 robot) | 2.000–2.500 satır/saat | — | Uygun değil: 814 SKU, ilk 50 SKU satırların %59'u. Hat stoğu + akışlı raf daha ekonomik. |
| Loop konveyör 25–30 m | 1.800 adet/saat | — | Sadece putwall alınırsa tampon olarak. |

**Kazan Hat ve Kadro Planı, adım 4 "Otomasyonlu senaryo" (10.11.2026):** 135 bin sipariş/ay, varsayılan verimlerle (batch toplama 220 adet, gözden paketleme 70, tekli toplama 90, tekli kolileme 80 sipariş/adam-saat, destek %15) 1 ISIWALL + 1 ISIBAGGER **manuelle aynı kadroyu** veriyor (sahada 24, bordro 33). Otomasyonlu verim ≈ 30 sipariş/adam-saat, manuel 30. 175 bin € yatırımın 24 ayda dönmesi için ≈ 7 kişilik bordro azalışı, yani otomasyonlu verimin ≈ 37,5 sipariş/adam-saate çıkması gerekir. Gerekçe kadro değil, kapasite (pik, büyüme), doğruluk ve alan olmalı. Verimler ISITEC referans ziyareti ve pilotla teyit edilmeli.

## 11. Planlama parametreleri (Sedat Birinci, 10.11.2026; büyüme 20.11.2026'da güncellendi)

| Parametre | Değer | Not |
|---|---|---|
| Kişi başı işveren maliyeti (cost to company) | **70.333,79 TL / FTE / ay** | yıllık 844.005 TL; 56,4 TL/€ kurla ≈ 14.965 € |
| EUR/TL kuru | 56,4 | 4 Kasım 2026; yatırımlar € ile, işçilik TL ile hesaplanır |
| E-ticaret büyümesi | **2027: ×1,5 (kesin, Sedat 20.11.2026)** | normal ay 135 bin → 2027 ≈202,5 bin; ort. 5.291 → 7.937 sipariş/gün, P95 8.470 → 12.705. P95 de ×1,5 varsayıldı. Şirket geneli %80, Aralık bütçesiyle teyit. **2028+ kanal bazında büyüme Aralık bütçesinden bekleniyor.** 10.11'deki "%20/yıl, 2027 ve 2028" varsayımı **geçersiz**. |
| Kazan kira / değerlendirme süresi | **10 yıl (120 ay)** | yatırım geri dönüşü bu süre içinde aranır |
| En büyük ürün | Mass Gainer 2,5 kg, Ø16,5 × 27,5 cm kavanoz | 5,5 LT ambalaj; Whey 1,6 kg, Pea, Isolate, Mega paket aynı kavanozda |
| Hedef | En verimli ve ideal depo çözümü, otomasyonlu ya da otomasyonsuz | ISITEC teklifi seçeneklerden biri |

**SKU ölçü listesi (variant-mappings-boyutlu, 10.11.2026):** 818 varyant, ikas SKU profiliyle eşleşme toplama satırlarının %95,7'si (ilk 50 SKU %100, ilk 150 SKU %97,5). Ağırlık yok. 120 SKU'nun ölçüsü eksik (satırların %4,3'ü; bar 4'lü/8'li, tester, Protein Fusion 80, bazı Creatine 300 g ve Cream of Rice aromaları). Ağırlık, eksik ölçüler ve koli/palet bilgisi Sedat tarafından iletilecek (şablon: Kazan_SKU_Olcu_Agirlik_Koli_Sablonu.xlsx). Logo ölçü/ağırlık dosyası `Urun_Olcu_Agirlik_Logo_19112026.xlsx` 21.11'de projeye eklendi, henüz işlenmedi.
- ISIWALL 3D'ye (≤ 380×300×150 mm, ≤ 3 kg) sığmayan: 5,5 LT kavanoz ve termal korse. Satırların %3,9'u, çok ürünlü siparişlerin en fazla %13,7'si → manuel hat.
- Cream of Rice 1 kg ve Whey 400 g 1,5 LT kutu (12,5 × 11,8 × 16,5) → sığıyor.
- Ambalaj formu (satır payı): silindir %58,6 · kutu %36,9 · karma paket %4,5.
- Tekli siparişlerin teorik %87'si koli1'e sığıyor (paketleme analizinde tüm siparişlerde koli1 %40) → desi tasarrufu potansiyeli, sahada doğrulanacak.

**Otomasyon sonucu (Hat ve Kadro Planı adım 4, 10.11'deki eski %20/yıl büyümesiyle):** 1 ISIWALL + 1 ISIBAGGER bordroyu manuelle hemen hemen aynı tutuyor (2028+: 47 → 46); 175 bin € yatırım 10 yılda dönmüyor. Başabaş ≈ 2 kişi bordro azalışı, otomasyonlu verim ≈ 31,5 sipariş/adam-saat (manuel 30). Karar pilot / referans sahada ölçülecek verime bağlı; ISIBAGGER fiyatı bekleniyor. ×1,5 büyümeyle yeniden hesaplanmadı.

## Ekler (proje dosyaları)

- `veri/ikas_2026/SKU_Profil.csv`: 814 SKU için aylık adet (Oca–Eki), baz / son 90 / son 30 günlük talep, P95, maks, CV, ABC (adet ve satır), XYZ, tekli sipariş payı, iade oranı, barkod, alış ve satış fiyatı.
- `veri/ikas_2026/Tekli_Siparis_HazirPaket.csv`: tek ürünlü siparişlerde SKU + adet kombinasyonları ve son 90 gün hızı.
- `veri/ikas_2026/SKU_Birlikte_Toplama.csv`: birlikte toplanan SKU ikilileri ve lift değerleri.
- `veri/ikas_2026/Gunluk_Seri.csv`: günlük sipariş, satır, adet ve kanal kırılımı.
- `veri/ikas_2026/SKU_Boyut_Uygunluk.csv`: 814 SKU için ambalaj formu, paket içeriği ölçüleri, putwall uygunluğu, sığmayan bileşen ve teorik en küçük koli.
- `veri/ikas_2026/Saat_x_Haftagunu.csv`: saat × haftanın günü ortalama sipariş.
- Tam Excel (24 sayfa) ve anonimleştirilmiş satır verisi (parquet) bilgisayarda "İndirilenler" ve "ikas yıllık veri" klasörlerinde.

**Yöntem:** Kişisel veriler (ad, e-posta, adres, telefon, TC/vergi no, not) çıkarıldı. Müşteri sadece tek yönlü anonim anahtarla tutuldu. Sipariş seviyesindeki alanlar siparişin tüm satırlarına yayıldı. İptal satırları hariç tutuldu.
