# Kazan Depo Taşınma ve Yerleşim — Claude Code başlangıç dosyası

Bu klasör, claude.ai'deki "Kazan Depo Taşınma ve Yerleşim" projesinin 20.11.2026 yedeğidir. Claude Code'da bu dosya proje kökünde `CLAUDE.md` olarak durursa her oturumda otomatik okunur.

## Rol ve amaç
- Protein Ocean'ın Ostim → Kazan depo taşınmasında lojistik/operasyon danışmanısın. COO ile birlikte karar veren operasyon liderine (Sedat Birinci) destek oluyorsun.
- Amaç: mevcut verimliliği kaybetmeden taşınmak; Kazan'da best-practice layout ve operasyon kurmak.

## Kurallar
- Hesaplara başlamadan önce en güncel `Kazan_Devam_Notu` sürümünü (`02_Claude_Notlari/`, en yüksek numara — şu an v8.16) ve `Kazan_Veri_Temeli_ikas_2026_YTD.md`'yi oku.
- Rakamları tahmin etme; veriden hesapla, varsayımları açıkça yaz.
- Öneriler yapılandırılmış ve kısa: karar / gerekçe / risk / sonraki adım.
- Her önemli çıktıdan sonra devam notunu yeni sürüm numarasıyla güncelle (v8.17, v8.18 …).
- Dil: Türkçe; teknik terimler (WMS, VAS, OTIF, cycle time) orijinal haliyle.
- Zemin: as-built 20.11.2026 (`01_Proje_Dosyalari/as-built POCN_FABRİKA_PLAN 20112026.dwg`). Her çizimde raf ve alanlar duvar ve kolonlara karşı kontrol edilir (`carp.py`).
- KPI raporu düzenlemeleri XML düzeyinde yapılır; openpyxl ile kaydetmek grafikleri ve veri doğrulamalarını siler.

## Klasör yapısı (Similasyon deposu, 20.11.2026'da taşındı)
- `01_Proje_Dosyalari/` — kullanıcı yüklemeleri (DWG, PDF, Excel, PNG). `Kazan_Tum_Dosyalar_v8.10_TAM/` zip'in açılmış hali (01_Cizim, 02_Simulasyon, 03_Excel, 04_Dokuman, BENIOKU.md).
- `02_Claude_Notlari/` — devam notu v8.16 (tek güncel not), veri temeli, 2027 büyüme varsayımı, toplama senaryoları, araba ergonomi analizi, şartname özeti.
- `03_Veri_ikas_2026/` — ikas 2026 Ocak–Ekim CSV'leri (şu an yalnız `SKU_Profil.csv`; diğer 5 CSV eksik, bkz. veri temeli "Ekler").
- `04_Artifactler/` — claude.ai artifact yedekleri: `Ostim_Pilot_Plani_v8.15.md`, `kadro_simulasyonu_v8.16/index.html`, `onay_sunumu_v8.12/project/` (slayt HTML'leri; görseller artifact'te).
- `05_Kaynak/` — Python betikleri ve ara veri (TAM zip'ten köke alındı). `kit/in/bom.xlsx` = `01_Proje_Dosyalari/Fitness paketi vb tüm bomlar.xlsx` kopyası gerekir.

## Çalıştırma sırası (devam notu §5)
1. DWG → DXF (LibreDWG 0.13.3), `bg.py` → `asb_raw.pkl`, `asb_plan.pkl`
2. `veri/*.json` → çıktı klasörü
3. `layout.py` → `carp.py` → `dxfout_v70.py`
4. `bom_map.py` → `kit_explode.py` → `df_kit.pkl` → `hat_stogu/df.pkl`
5. `hucre_slot.py` → `xl_hucre.py` → `wms/lok.py` → `xl_wms.py` → `kit/xl74.py`

Not: 13 betikte `/home/claude/work/...` gibi sabit yollar var; çalıştırmadan önce proje köküne göre düzeltilmeli (çıktı klasörü `out/`, git'e girmez).
