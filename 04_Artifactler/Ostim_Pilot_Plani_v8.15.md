# Kazan · Ostim Pilot Planı (arabalı hücre toplama)

Nov 20, 2026 · @Sedat Birinci

## Amaç ve karar kuralı

Pilot, Kazan hücre tasarımının dayandığı tek ölçülmemiş sayıyı doğrular: 18 gözlü arabayla 1,8 m tek yön döngüde toplama hızı. Model 120 satır/adam-saat varsayıyor; hücrenin Senaryo 1'e (A + Karma) göre başabaşı ≈69 satır/saat.

| Sonuç (öğrenme dönemi hariç, ortalama) | Karar |
| --- | --- |
| ≥ 120 satır/saat ve hata < %0,3 | Model geçerli. Kadro planı (sahada 22 / 40) aynen. |
| 80–120 satır/saat ve hata < %0,3 | Hücre kararı geçerli. Kadro ve araba adedi pilot hızıyla yeniden hesaplanır. |
| 69–80 satır/saat | Gri bölge. Senaryo 1 ile FTE karşılaştırması pilot hızıyla tekrarlanır, karar COO'da. |
| < 69 satır/saat veya hata ≥ %0,3 | Senaryo 1'e (A + Karma, konveyör + istasyon) dönülür. |

İkinci çıktı hücre başı en fazla kişi sayısıdır. 2027 P95'te hücre başı 12,4 kişi gerekiyor; model ≈8'de sıkışma bekliyor. Pilot bu sınırı ölçer ve 2027 seçenek C'nin (vardiya mı, 3. hücre mi) zamanlamasını belirler.

## Test edilecek varsayımlar

Beş varsayım ölçülür; ilk ikisi karar kuralını belirler, diğerleri şartnameye ve kadroya girer.

| # | Varsayım (Kazan modeli) | Kaynak | Pilotta nasıl ölçülür | Hedef |
| --- | --- | --- | --- | --- |
| V1 | Arabalı toplama 120 satır/adam-saat | Senaryo modeli | Sefer başı satır ÷ sefer süresi; günlük toplam satır ÷ çalışılan saat | ≥ 80 (karar), 120 (model) |
| V2 | Toplama hatası < %0,3 | Mevcut KPI hedefi | Paket istasyonunda %100 kontrol: yanlış ürün, eksik, fazla, yanlış göz | < %0,3 satır |
| V3 | 1,8 m döngüde hücre başı ≈8 kişi rahat çalışır | v8.6 varsayımı | Kişi sayısı adım adım artırılır; kişi başı hız %10'dan fazla düştüğü nokta sınırdır | Sınır kişi sayısı |
| V4 | 18 gözlü arabada uzak sıra gözüne erişim hızı düşürmez | Araba tasarımı v7.4 | Uzak sıraya koyma sayısı ve arabanın etrafından dolaşma sayısı; iki göz doldurma kuralı karşılaştırılır | Dolaşma < sefer başına 2 |
| V5 | Sefer başına ≈17 sipariş; 160 cm araba itilirken görüş yeterli | Araba tasarımı v7.4 | Sefer başına sipariş; dönüşlerde çarpma / durma sayısı; personel anketi | ≈17; çarpma 0 |

Yan ölçüm: paket istasyonunda arabadan paketleme süresi (sipariş/saat). Kazan'da 16 istasyon varsayımı buna bağlı.

## Pilot yerleşimi (Ostim)

Kazan hücresinin yarısı 1:1 kurulur: 1,8 m net koridor, ≈15 m düz yol ve bir 90° dönüş. Tam döngü 30,6 m; yarım döngü hız ölçümü için yeter, dönüş ve sıkışma davranışını da gösterir.

- **Alan:** ≈15 × 6 m (raf + koridor + dönüş + paket istasyonu). Ostim'de yer, Sedat'ın alan seçimiyle kesinleşir.
- **Raf:** Mevcut Ostim raflarından iki karşılıklı hat, koridor 1,8 m'ye zemin bandıyla sabitlenir. 5 kat, Kazan kat kuralı (3 → 2 → 4 → 1 → 5; 5,5 L kavanoz yalnız kat 1–2).
- **Stok:** Satır payına göre ilk ≈100 SKU (toplama satırlarının ≈%75'i). Lansman SKU'ları hariç.
- **Araba:** 2 adet numune araba, tedarikçiden (yetişmezse koli10'lu geçici araba) (100 × 70 × 160 cm, taban 50 / 80 / 110 cm, her katta 3 × 2 göz, göz içi 32 × 34 × 28 cm). Biri toplamada, biri istasyonda.
- **Giriş-çıkış:** Döngünün başı ve sonu paket istasyonuna bakar; tek yön okları zemine.
- **Paket istasyonu:** 1–2 Ostim istasyonu döngü çıkışına; kantar ve okutma burada.
- **Göz etiketi:** Kazan formatında (`H1D-07-3A` gibi) ki toplayıcı Kazan kodlamasını da denesin.

Açık soru: Ostim'de 15 × 6 m boş alan var mı, yoksa pilot mevcut bir hatın bir bölümünde mi kurulur?

## Adım adım: Ostim'de nasıl kurulur

Pilot Kazan binasını değil yöntemi test eder: göz = sipariş araba, tek yön döngü ve döngü sıralı liste. Üçü de Ostim'de mevcut bir raf sırasının etrafında kurulur.

1. **Raf:** Bugün A ürünlerinin durduğu, iki yüzünden erişilen bir raf sırası seçilir. Stok taşınmaz; pilot o raftaki ürünlerle çalışır. Koridor 1,8 m'den genişse zemin bandıyla daraltılır. Raf ≈7,5 m ise döngü ≈15 m olur.
2. **Araba:** Kazan için seçilen arabanın numunesi tedarik edilir ve pilotta test edilir (aşağıda "Araba testi"). Numune yetişmezse geçici çözüm: mevcut rafı araba + 18 koli10 kutusu (3 kat × 6). Koli10'un dış ölçüsü (34 × 30 × 30 cm) Kazan gözüne (32 × 34 × 28 cm) çok yakın.
3. **Sipariş listesi:** Sabah ERP/ikas'tan günün siparişleri çekilir. Tüm ürünleri o raf sırasında olan siparişler ayrılır. Excel'de her 18 siparişe göz 1–18 verilir, satırlar raftaki yürüme sırasına dizilir.
4. **Toplama:** Toplayıcı istasyondan çıkar, rafı tek yönde dolaşır, her ürünü listedeki göze koyar, istasyona döner.
5. **İstasyon:** Paketçi gözleri sırayla paketler; her siparişi okutur ve kantarda kontrol eder.
6. **Ölçüm:** Telefonla sefer süresi; başlangıç, bitiş ve satır sayısı forma. Hatalar paket masasında sayılır. Günde 2 sefer videoya alınır.

**Kazan'a ne taşınır:** göz = sipariş yönteminin hızı ve hatası, arabanın kendisi, uzak göze erişim, aynı koridorda kaç kişinin sıkıştığı. **Taşınmayan:** bina, WMS ve tam 30,6 m döngü. Bu yüzden asıl ölçü karşılaştırmadır: aynı gün, aynı kişiler, aynı ürünler, bir saat bugünkü Ostim yöntemi ve bir saat arabalı döngü. Fark (örneğin %30 daha hızlı) Kazan kadro hesabına uygulanır; yürüme süresi videodan ayrılıp 30,6 m'ye ölçeklenir.

**Daha basit alternatif:** Döngü kurmadan, mevcut hatta numune araba 2 gün bugünkü yöntemin yanında denenir. Hız, hata ve araba ölçülür; koridor yoğunluğu (V3) ölçülmez.

## Araba testi (tedarik + pilot)

**Araba Kazan'ın tek yeni ekipmanıdır ve satınalmadan önce numunesi pilotta test edilir.** 2026'da 30, 2027'de ≈45 adet alınacağı için yanlış tasarımın bedeli büyük.

- **Tedarik:** 24.11 onayından hemen sonra 1–2 tedarikçiden 2 numune araba istenir (şartname ölçüsü: 100 × 70 × 160 cm, 18 göz, 3 kat, taban 50 / 80 / 110 cm, göz içi 32 × 34 × 28 cm, ayarlanabilir kat). Teslim hedefi: 02.12 (pilot başlangıcı).
- **Pilotta test edilenler:** göz ölçüsü (5,5 L kavanoz dik sığıyor mu), uzak sıra gözüne erişim, dolu araba itme ve dönüş, 160 cm'de görüş, tekerlek ve fren, istasyonda boşaltma süresi, 5 günlük kullanımda hasar.
- **Sonuç:** Şartname son haline getirilir (kat kotu, tekerlek, ayırıcı, tutamak); 30 adetlik sipariş pilot raporundan sonra verilir.
- **Numune gecikirse:** pilot koli10'lu geçici arabayla başlar; numune gelince araba testi için 1 gün eklenir.

## Malzeme ve hazırlık

Hazırlık 4 iş günü sürer; tek satın alma 2 numune arabadır.

- [ ] Pilot alanını seç, 1,8 m koridoru zemin bandıyla işaretle
- [ ] İlk ≈100 SKU'yu ikas SKU profilinden seç, kat kuralına göre göz ata (Claude, `SKU_Profil.csv`)
- [ ] Rafları stokla (≈3 günlük pilot talebi), göz etiketlerini Kazan formatında bas
- [ ] 2 numune araba siparişi (24.11 sonrası, teslim 02.12); yedek: koli10'lu geçici araba, göz numarası etiketli
- [ ] Toplama listesi: döngü sırasına göre sıralı, sipariş → araba gözü eşleşmeli (Excel; WMS yoksa kağıt/tablet)
- [ ] Sipariş filtresi: tüm satırları pilot SKU'larında olan, hazır paket dışı siparişler
- [ ] El terminali veya barkod okuyucu, kantar, 2 telefon (video + kronometre)
- [ ] Ölçüm formu (tablet/Excel) ve personel anketi
- [ ] Pilot ekibine 1 saatlik brifing: döngü, göz kodu, araba kuralı

Not: WMS'in dalga ve göz eşleştirme mantığı pilotta Excel listesiyle taklit edilir. Kazan'da bu yetenek WMS sözleşmesine yazılmadan gerçekleşmez.

## Test tasarımı

5 ölçüm günü, ≥ 3.000 kontrol edilmiş satır. 3.000 satırda en fazla 3 hata çıkarsa hata oranı %95 güvenle %0,3'ün altındadır (Poisson üst sınırı 7,75 / 3.000 = %0,26).

| Gün | Kişi | Ne denenir | Ölçülen |
| --- | --- | --- | --- |
| G1 | 2 | Alıştırma; döngü, göz kodu, araba | Kaydedilir ama karara sayılmaz (öğrenme) |
| G2 | 2 | Normal tempo; araba doldurma kuralı A: önce yakın sıra | V1, V2, V4, V5 |
| G3 | 3 | Doldurma kuralı B: sıralı (göz 1 → 18) | V1, V2, V4 karşılaştırma |
| G4 | 3 → 4 → 5 → 6 | Yoğunluk: her adım 1 saat | V3: kişi başı hız, durma ve bekleme |
| G5 | 3 | En iyi kural, tam gün; hata sayımını tamamla | V1, V2; Ostim mevcut yöntemle aynı gün kıyas |

- **Yoğunluk ölçeği:** Yarım döngü 15 m. 3 / 4 / 5 / 6 kişi = 5,0 / 3,75 / 3,0 / 2,5 m/kişi; Kazan'ın tam döngüsünde 6 / 8 / 10 / 12 kişiye karşılık gelir. 2027 P95 ihtiyacı (12,4 kişi/hücre) son adımda test edilmiş olur.
- **Kişi seçimi:** 6 toplayıcı rotasyonla: 2 deneyimli, 2 orta, 2 yeni. Sonuç kişi grubuna göre de ayrılır.
- **Siparişler:** Gerçek günlük siparişler, pilot SKU filtresiyle. Sipariş başına satır dağılımı kaydedilir ve Kazan hücre siparişinin profiliyle (≈2,06 satır/sipariş, kit hariç) karşılaştırılır.
- **Paketleme:** Pilot siparişleri paket istasyonunda %100 kontrol edilir; hata müşteriye gitmez.

## Ölçüm yöntemi ve form

Satır/saat sefer bazında ölçülür: sefer başlangıcı = araba döngüye giriş, bitiş = araba istasyona teslim. Günlük hız = toplam satır ÷ toplama saati (mola ve bekleme ayrı yazılır). G1 ve her kişinin ilk 2 seferi karara sayılmaz.

**Sefer formu** (her sefer bir satır; gözlemci doldurur):

| Tarih | Sefer no | Toplayıcı | Döngüdeki kişi | Doldurma kuralı | Başlangıç | Bitiş | Sipariş | Satır | Adet | Uzak sıra koyma | Dolaşma | Bekleme (sn) | Çarpma / durma | Not |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

**Hata formu** (paket istasyonu; her hata bir satır):

| Tarih | Sefer no | Sipariş no | Göz | Hata tipi (yanlış ürün / eksik / fazla / yanlış göz) | SKU | Toplayıcı | Muhtemel neden |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

**Günlük özet:** toplam satır, toplama saati, satır/saat (kişi ve toplam), hata sayısı ve oranı, paketleme sipariş/saat.

**Personel anketi** (gün sonu, 1–5): araba itme ve görüş, uzak göze erişim, koridor genişliği, göz kodunu okuma, yorgunluk. Bir açık soru: en çok neyi değiştirirdin?

Video: her gün 2 sefer baştan sona çekilir (yüz yok, el ve araba); süre dağılımı (yürüme / arama / alma / koyma) videodan çıkarılır.

## Ekip ve takvim

Ölçüm 03–09.12.2026 arasında 5 iş günü, rapor 11.12'de. Black Friday (27.11) ve Cyber Monday (30.11) haftası bilerek dışta bırakıldı; kampanya takvimiyle teyit edilmeli.

| Rol | Kişi | Zaman | Görev |
| --- | --- | --- | --- |
| Sponsor | Sedat Birinci | Karar anları | Alan, kişi ve tarih onayı; sonuç kararı |
| Pilot sorumlusu | E-ticaret şefi | Tam zaman (ölçüm günleri) | Ekip, sipariş akışı, günlük plan |
| Gözlemci | 1 kişi (ekip lideri) | Tam zaman | Sefer ve hata formu, video |
| Toplayıcı | 6 kişi, rotasyon | Günde 2–6 kişi | Pilot toplaması, anket |
| Paketçi | 1–2 kişi | Tam zaman | %100 kontrol, paketleme süresi |
| Kurulum | 2 kişi | Hazırlık haftası | Raf, bant, etiket, stok, araba maketi |
| IT / ERP | 1 kişi | Günde ≈30 dk | Pilot SKU filtresiyle sipariş listesi |
| Claude | – | Hazırlık + rapor | SKU seçimi, göz ataması, form, analiz ve rapor |

1. 24.11 — COO + GM onayı (karar 6)
2. 25.11–02.12 — Hazırlık: alan, raf, stok, araba maketi, liste, brifing
3. 03.12 — G1 alıştırma
4. 04.12, 07.12, 08.12, 09.12 — G2–G5 ölçüm
5. 11.12 — Pilot raporu ve karar (WMS sözleşmesi ve satınalma siparişinden önce)

## Riskler ve önlemler

En büyük risk sonucun Kazan'ı temsil etmemesidir; önlemlerin çoğu bu yüzden karşılaştırmayı aynı gün ve aynı kişilerle yapar.

| Risk | Etkisi | Önlem |
| --- | --- | --- |
| Pilot Ostim operasyonunu yavaşlatır | Kargo çıkışı gecikir | Pilot siparişleri günlük hacmin küçük bir bölümü; kampanya haftası dışında |
| Gözlenme etkisi (hız yapay yüksek) | Model iyimser kalır | G1 ve ilk seferler sayılmaz; 5 günün ortalaması alınır; rotasyon |
| WMS yok, Excel listesi | Hız gerçekten farklı çıkar | Liste döngü sıralı ve göz eşleşmeli; sapma raporda belirtilir |
| Yarım döngü tam döngüyü yansıtmaz | Yürüme payı düşük çıkar | Yürüme süresi videodan ayrılır ve 30,6 m'ye ölçeklenir |
| Sipariş karışımı Kazan'dan farklı | Satır/sipariş farklı olur | Satır/sipariş kaydedilir; hız satır bazında karşılaştırılır |
| Numune araba pilota yetişmez | Araba testi yapılamadan satınalma kararı verilir | Numune siparişi 24.11'den hemen sonra; gecikirse geçici arabayla başla, numune gelince 1 gün ek test; 30 adetlik sipariş testten sonra |
| Hata müşteriye gider | Şikayet | %100 istasyon kontrolü, kantar |

## Sonuç raporu şablonu

Rapor tek sayfa: tablo, karar ve plana etkisi. Boş hücreler pilottan sonra doldurulur.

| Ölçüt | Hedef | Ölçülen | Sonuç |
| --- | --- | --- | --- |
| Satır/adam-saat (G2–G5 ort.) | ≥ 80 (model 120) |  |  |
| Hata oranı (satır) | < %0,3, ≥ 3.000 satır |  |  |
| Hücre başı sınır kişi (tam döngü eşdeğeri) | ≥ 8 |  |  |
| Uzak sıra dolaşma / sefer | < 2 |  |  |
| Sipariş / sefer | ≈17 |  |  |
| Paketleme sipariş/saat | Mevcut Ostim değeri |  |  |
| Personel anketi (1–5, ortalama) | ≥ 3,5 |  |  |

**Karar:** Karar kuralı tablosuna göre hücre / yeniden hesap / Senaryo 1.

**Plana etkisi:**

- Kadro: sahada normal / P95, pilot hızıyla yeniden (2026 ve 2027)
- Araba adedi ve doldurma kuralı → şartname ve WMS Ek-1
- Hücre başı sınır kişi → 2027 seçenek C zamanlaması (vardiya / 3. hücre)
- Araba tasarımı değişiklikleri (kat kotu, kasa, görüş) → satınalma şartnamesi
