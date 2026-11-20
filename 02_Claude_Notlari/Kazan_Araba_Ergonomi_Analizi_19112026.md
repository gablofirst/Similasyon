# Kazan toplama arabası · ergonomi ve kasa analizi (19.11.2026)

**Soru (Sedat):** Şartnamedeki arabada kasa tabanları 300/650/1.000 mm. Alt kat eğilip kalkma demek, toplamayı yavaşlatmaz mı? Daha sığ / eğilmesiz bir araba daha iyi olmaz mı?

## Yöntem
- Sipariş satır verisi bu ortamda yok (parquet Sedat'ın bilgisayarında). 150.000 siparişlik simülasyon yapıldı:
  - sipariş başına SKU dağılımı (%54,7 tek SKU…)
  - SKU seçimi: tekli siparişler `tekli_siparis`, çoklu siparişler (satır − tekli) ağırlığıyla
  - adet: SKU'nun `satir_basi_adet` değeri
  - ölçüler: kap tipi tablosu, kitler bileşen listesiyle (fitness, mega, large, gainer, protein paketi vb.)
  - hazır paket tekli siparişleri (%88 yakalama) ve hediye ürünleri (paket masasında) arabadan çıkarıldı
- **Kalibrasyon:** İhsan'ın 7.000 siparişlik koli dağılımı. En iyi doluluk katsayısı 0,62. Model büyük siparişleri gerçekten fazla gösteriyor (koli10 model %7,4, gerçek %3,6), yani temkinli.
- Kaynak: `/home/claude/araba/` (sim2.py, calib.py, kasa.py, opt.py), workspace'e özel.

## Bulgular
- **Arabaya giren ürün hacmi (hücre siparişi):** P50 2,4 L · P75 5,6 · P90 9,9 · P95 13,1 · P99 20,3 L.
- **Kasa yüksekliği düşürülemez:** 1,5 L kutunun en kısa kenarı 11,8 cm, 5,5 L kavanoz çapı 16,5 cm.

| Kasa (dış, mm) | İç hacim | Sığan sipariş |
|---|---|---|
| 400×300×220 (şartname) | 19,8 L | %93,6 |
| 400×300×170 | 15,0 L | %85,4 |
| 400×300×120 | 10,2 L | %49,1 |
| 300×200×220 | 9,2 L | %76,6 |
| 300×200×170 | 7,0 L | %64,5 |
| 600×400×220 | 42,3 L | %99,7 |

- Sonuç: sorun kasa derinliği değil, **alt katın 300 mm'de olması**. 400×300×220 kasa doğru.

## Araba seçenekleri (normal gün, 2.929 hücre siparişi, 2,06 satır/sipariş)
Varsayımlar: satır başı 30 sn (120 satır/saat), eğilip kalkma 2,2 sn (MTM-1: B 29 + AB 31,9 TMU), sefer sabit süresi 50 sn + göz başı 3 sn, WIP 456 göz (P95).

| Seçenek | Göz | Sipariş/sefer | sn/sipariş | Eğilme/kişi/gün | Araba |
|---|---|---|---|---|---|
| A Mevcut 3 kat × 4 (300/650/1.000) | 12 | 11,3 | 71,1 | ≈260 | 40 |
| B 2 kat × 4 (650/1.000) | 8 | 7,5 | 71,8 | 0 | ≈61 |
| **C 2 kat × 4 + alt raf yalnız büyük sipariş** | 8 | 8,5 | 70,9 | ≈50 | ≈53 |
| D 3 kat yükseltilmiş (550/850/1.150), kasa 170 | 12 | 10,5 | 70,8 | ≈260 (hafif) | ≈44 |

- Süre farkı ±%1. Asıl fark ergonomi: günde kişi başı ≈260 eğilme → C'de ≈50.
- MTM süresi yorgunluğu, vardiya sonu hız düşüşünü ve sakatlık riskini kapsamaz.

## Öneri (karar Sedat'ta)
- **C:** üst iki kat ergonomik bölgede (kasa tabanı ≈650 ve ≈1.000–1.050 mm, kat aralığı ≥ 350–400 mm), 4'er göz. Alt raf (≈300 mm) açık, yalnız kasaya sığmayan büyük siparişler (≈%6) için.
- **Şartnameye:** kat kotları ayarlanabilir (50 mm adımlı delik). Ostim pilotunda A ve C aynı maketle denenir; satır/saat, hata ve personel yorumu ölçülür.
- **Etki:** araba 40 → ≈53; kasa ihtiyacı ≈530 → ≈470. Boş araba park alanı (+≈10–15 m²) kontrol edilmeli. İstasyonda araba değişimi 12 yerine 8,5 siparişte bir.
- Gerçek sipariş satırı (parquet) gelirse analiz aynı scriptlerle tekrarlanır.
