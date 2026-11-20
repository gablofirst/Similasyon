# Kazan Depo — 2027 Büyüme Varsayımı (güncelleme 16.11.2026)

**Bu not, `Kazan_Veri_Temeli_ikas_2026_YTD.md` bölüm 11'deki "%20 / yıl, 2027" satırının yerine geçer.**

## Gelen bilgi
- **2027 organik büyüme: toplam %80, dolar bazında.** Dolar bazı olduğu için adet büyümesi gibi okunuyor (Sedat Birinci).
- **Kanal kırılımı:** E-ticarette büyüme kabaca **%50**. Diğer kanallarda (VAS/Bim, B2B) daha fazla.
- **Aralık 2026:** SKU bazında aylık kırılımlı 2027 verisi ve **2027 bütçesi** gelecek. Kanal detayı, kanal karışımı ve sezon dağılımı bununla netleşecek.
- **2028 ve sonrası:** Belli değil, sorulacak. Sedat'ın beklentisi: bundan sonra büyümeyi daha çok **B2B** taşır.

## Planlama yaklaşımı (2028+ belirsiz)
- 2028+ için tek oran yerine **senaryo aralığı** ile çalışılır. E-ticaret ve B2B/VAS ayrı oranlarla senaryolanır.
- Layout **modüler** kurulur: e-ticaret hatları için yedek hat yuvaları, B2B/VAS için genişleyebilir alan ve rampa kapasitesi. Kesin kapasite 2027 bütçesine göre, yedek alan senaryo aralığına göre ayrılır.

## E-ticaret: 2026 bazına %50 uygulanırsa (ön hesap, doğrusal ölçek)

| Gösterge | 2026 | 2027 (×1,5) |
|---|---|---|
| Normal ay (kadro bazı) | 135 bin sipariş | **203 bin** |
| Yıllık ortalama ay | 161 bin | **241 bin** |
| Pik ay (Mart) | 231 bin | **347 bin** |
| Ortalama gün | 5.291 | **7.937** |
| P95 tasarım günü | 8.470 | **12.705** |
| Maks gün | 11.601 | **17.402** |
| P95 gün toplama satırı | 17.991 | **26.987** |
| P95 gün adet | 20.364 | **30.546** |

**Kadro ve hat (manuel, yaklaşık 30 sipariş/adam-saat, ön tahmin):**
- Normal ay: sahada yaklaşık 24 → **≈ 36**, bordroda yaklaşık 33 → **≈ 50 kişi**.
- Hat: 2 hat → **3 hat**. 4. hat yuvası yedek.
- Pik ay (347 bin) 2026 pikinin 1,5 katı. Yüksek sezonda ikinci vardiya gerekir.

**Etkilenen kararlar:**
- **Otomasyon:** Önceki sonuç (%20 büyümeyle "10 yılda dönmüyor") yeniden hesaplanmalı. 1 ISIWALL P95 gününde yaklaşık 11 saat çalışır. Tek vardiyada sınırda, iki vardiyada yeterli.
- **Hat stoğu ve toplama alanı:** Hat stoğu adedi yaklaşık 1,5 kat.
- **Kargo çıkışı:** Günde ortalama yaklaşık 8 bin koli, pik günde 17 bin. Araç sıklığı ve güney çıkış alanı kontrol edilmeli.

## VAS/Bim ve B2B: büyüme e-ticaretten hızlı
- Kazan'da **VAS alanı, batı rampaları (Bim/FTL), mal kabul ve palet stoğu** en çok baskı görecek bölgeler. 2028+ büyümeyi de daha çok B2B taşıyacaksa genişleme payı burada ayrılmalı.
- Kabul edilen VAS aylık maksimum kapasiteleri (Toz 1 230.000, Toz 2 125.000, Vitamin 265.000 adet) 2027 talebiyle karşılaştırılmalı. Hat sayısı ve taşeron ihtiyacı buna göre çıkar.
- ADEYA raf yerleşimi palet kapasitesi bu büyümeyle teyit edilmeli.

## Aralık verisi ve bütçe geldiğinde
- SKU × ay talebinden ABC/XYZ, hat stoğu ve P95 (`SKU_Profil.csv` mantığıyla).
- Kanal karışımı ve sezon profiline göre tekli hat payı ve pik planı.
- Hazır paket aday listesi 2027 hızına göre.
- Hat ve Kadro Planı ile otomasyon senaryosu 2027 aylık profilinden.
- VAS hat kapasitesi ile 2027 VAS/B2B talebinin karşılaştırması.
