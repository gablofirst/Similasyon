# Kazan · tüm dosyalar v8.30 (21.11.2026)

Güncel not: `04_Dokuman/Kazan_Devam_Notu_v8.30.md` (tek güncel not). **Kural: her sürümde bu paket yenilenir ve projeye yüklenir; eski paket silinir.**

**v8.30:** onay sunumu v8.30 (özet kadro 24 / 45, tünelsiz kaçış 61,6 m); `05_Kaynak/k5/tunelsiz.py`.

**v8.27'de eklenen/değişen:**
- `01_Cizim/Kazan_v8.12_AsBuilt_Yerlesim_R2000.dxf` → **AutoCAD'de bunu açın** (tüm sürümler). `_R2010.dxf` yazıları MTEXT olarak korur. DWG bu sürümde yok (bkz. not).
- `02_Simulasyon/..._sim_v2.3.html` → açılışta ortalı görünüm (hazır paket dahil).
- `06_Sunum/Kazan_Onay_Sunumu_v8.27.pptx` → düzenlenebilir PowerPoint; ayrıca PDF ve çevrimdışı HTML.

---

**v8.23 paketine eklenen:** `02_Simulasyon/Kazan_v8.11_Eticaret_Akis_3D_sim_v2.1.html` (3D akış simülasyonu, çevrimdışı açılır) · `06_Sunum/` (onay sunumu PDF + HTML + slayt kaynakları) · `05_Kaynak/sim3d/` (sim düzenleme ve ölçüm betikleri). Eski 3D'ler ve v8.19 notu `arsiv/` klasörlerinde.

---
## v8.11 notları

**v8.11'de değişen:** e-ticaret bandı (H1, paketleme, H2, hazır paket) 17,03 m doğuya, bir kolon aksı. Kampanya (72 yer paleti) ve koli/dolgu duvarın doğusunda, H1'in batısında. VAS 5–6 eski kampanya alanında dikey. K1 güney kapı 139,0'dan çıkar. Saçak X 167,5'e uzar; tel çit taşınmalı. Rezerv 3.835 → 3.495 m². Kapasite 4.030 palet ve kaçış (en uzun 44,3 m) değişmedi.

| Klasör | İçerik | Durum |
|---|---|---|
| 01_Cizim | `Kazan_v8.11_AsBuilt_Yerlesim.dxf` (ana, katmanlı; PO_KACIS ve yeni PO_KAMPANYA_PALET dahil) · `.dwg` (R2000, düz) · `.png` · e-ticaret detay PNG · kaçış haritası v8.11 · `arsiv_v8.10/` | Güncel |
| 02_Simulasyon | 3D akış simülasyonu sim v2.1 (v8.11 koordinatları, hız 95, K5) · eski 3D'ler `arsiv/` | Güncel |
| 06_Sunum | Onay sunumu v8.23: PDF, çevrimdışı HTML, `kaynak/` | Güncel (plan slaytları eski görsel) |
| 03_Excel | Kit-Kutu-Araba v8.10 · Hücre Stoğu v8.10 · WMS Lokasyon v8.10 · B2B Toplama Yüzü v6.4 | Hücre içi göz düzeni geçerli; kampanya lokasyonu ve koordinatlar v8.11'de güncellenecek |
| 05_Kaynak | `veri/layout.json` = v8.11 (`layout_v8.10.json` önceki) · `yerlesim/dxfout_v811.py` · `v811/` (kaydırma, ek çakışma kontrolü, kaçış, as-built okuma) | Güncel |

Çalıştırma (v8.11): `python3 v811/asb_from_dxf.py 01_Cizim/arsiv_v8.10/Kazan_v8.10_AsBuilt_Yerlesim.dxf /home/claude/work/out/asb_plan.pkl` → `veri/layout.json` → `/home/claude/work/out/` → `carp.py` + `v811/carp_ek.py` → `yerlesim/dxfout_v811.py <layout.json> <çıktı.dxf> <taban.dxf>` (taban = v8.10 DXF'ten PO_ katmanları silinmiş, PO_KACIS kalır) → `dxf_r2000_flat.py` + LibreDWG `dxf2dwg -y --as r2000`.
