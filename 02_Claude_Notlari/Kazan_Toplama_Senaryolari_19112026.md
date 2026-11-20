# Kazan e-ticaret toplama senaryoları (19.11.2026)

Doküman (COO için): https://claude.ai/artifact/JnWGEmW3414tmZZXNjazHX · Senaryo 3 3D: https://claude.ai/artifact/9A8V6gnxb5tHk1HsWGhVm7

## Ortak baz
- **Alan:** Hat bandı X 100,2–151,5 × Y 48,8–56,6 (≈400 m²). HP şeridi ve saçak yerinde.
- **Hacim (normal gün):** 4.500 sipariş. HP ≈1.230 sipariş alıyor; hatlara 2.929 sipariş, 6.047 satır kalıyor.
- **SKU:** 267 aktif fiziki SKU (A 77, B 83, C 107). Yalnız kitten oluşan siparişler (~340/gün) hesap dışı.
- **Toplama hızı (satır/adam-saat):** hat 75 · A bölgesi 100 · arabalı 120 · palet 90 · duvar 60 · C RF 30.
- **Paketleme:** tekli 60 sipariş/saat, ek satır başına +0,4 dk; ayrı istasyonda %10 daha hızlı.
- **Besleme:** 3 dk/kalem. **FTE:** 7,5 verimli saat, +%10 destek.

## Sonuç (normal gün FTE · besleme sıklığı)
- **Şu an (2 ikiz hat):** 27,8 FTE · 2 günde bir.
- **Senaryo 1 (A + Karma, konveyör + istasyon):** 23,1 FTE · A ve Karma ≈3 günde bir.
- **Senaryo 3 (kapalı kutu, arabalı toplama, tek stok 380 göz):** 17,6 FTE · ≈5 günde bir. **En verimli.**
- **Senaryo 4 (4 köşe ABC + ortada paletli ilk 20 A):** 23,4 FTE · palet ≈3, raf ≈5,5 günde bir.
- **Başabaş:** Senaryo 3, Senaryo 1'i arabalı toplama ≈69 satır/saat'in üstünde geçiyor.

## Senaryo 3 araba önerisi
- **Araba:** 12 gözlü (3 × 4), göz = 1 sipariş, göz ≈40 × 30 × 17 cm (20 L).
- **Sefer:** ≈25 satır, ≈13 dk; model hızı 112 satır/saat.
- **Büyük siparişler** (koli10/26, %4,3): iki göz ya da 6 gözlü araba.
- **Kapasite:** 16 paket istasyonu. Araba: normal gün ~25, P95 ~40.

## Karar
- **Sedat'ın kuralı:** En az FTE olan senaryo en iyisi.
- **Önerilen pilot:** Ostim'de 2–3 gün arabalı toplama. ≥ 80 satır/saat ve hata < %0,3 çıkarsa Senaryo 3, değilse Senaryo 1.
- Elenen: 4 kapalı hat (A/B/C/Karma), en pahalı seçenek ve alana sığmıyor.
- Kaynak kod: `/home/claude/abc4` (`s4x.py`), workspace'e özel.
