# Paket portfolio Databricks × devarent

**Status: katalog + rancangan integrasi + fork dry-run. Tidak ada pemasangan atau perubahan GitHub remote.**

Paket ini menggabungkan navigasi ke ekosistem Databricks dan portfolio devarent tanpa mencampurkan kepemilikan kode. Seluruh perubahan file berada di branch kerja repository `terraform-databricks-sra`.

## Hasil snapshot 22 November 2026

| Item | Hasil |
|---|---|
| Repository publik Databricks | **253** |
| Repository publik devarent | **79** |
| Entri metadata siap impor ke aplikasi | **332**, dengan ID `owner/name` unik |
| Databricks archived | **73** — katalog/referensi secara default |
| Databricks yang merupakan fork | **94** — perlu review source/root network |
| Benturan nama publik | **3**, semuanya fork langsung yang sudah ada |
| Usulan memakai ulang fork | `devarent/devhub`, `devarent/terraform-databricks-sra`, `devarent/zerobus-sdk` |
| Sisanya | **177** memerlukan review sebelum fork; bukan otomatis disetujui |
| Metadata lisensi Databricks | 45 `NOASSERTION`, 39 tidak terdeteksi; semuanya perlu pembacaan ketentuan sumber |
| Repo Databricks berukuran estimasi ≥100 MiB | **25**; angka GitHub bukan ukuran download pasti |

Angka ini bukan konstanta; generator dapat menghasilkan snapshot berbeda setelah refresh. Tidak ada private repo yang diinventarisasi, jadi nama target yang tidak ada secara publik **belum tentu tersedia**.

## Deliverables

1. **[Katalog Databricks lengkap](DATABRICKS-CATALOG.md)** — tautan 253 repo, deskripsi, bahasa utama, lisensi, archived, fork, kategori dan prioritas integrasi.
2. **[Manifest sumber + tujuan](DATABRICKS-MANIFEST.json)** — metadata kedua pemilik, bukti parent/source fork tujuan, keputusan dry-run, dan semua batasan otomatisasi.
3. **[Fork dry-run](FORK-DRY-RUN.md)** — pemetaan sumber → usulan target, benturan nama dan review gates; setiap entri `execution_allowed: false`.
4. **[Data katalog web](WEB-CATALOG.json)** — 332 entri siap diadaptasi ke UI, tanpa source code atau credential.
5. **[Rencana integrasi aplikasi](WEB-INTEGRATION-PLAN.md)** — rekomendasi `repo-atlas-next`, Next/React/Tailwind/Radix, API Laravel opsional dan acceptance criteria.
6. **[Bukti manifest aplikasi](WEB-STACK-EVIDENCE.json)** — deklarasi dependency tiga repo aplikasi pada commit yang diperiksa; bukan hasil build.

Katalog milik devarent sebelumnya tetap berada di [REPO-ATLAS.md](../REPO-ATLAS.md). Temuan source code devarent berada di [CODE-AUDIT-2026-11-22.md](../CODE-AUDIT-2026-11-22.md); temuan itu tidak otomatis berlaku pada upstream Databricks. Khusus private key pada `aws-rds`, tindak lanjut revokasi/rotasi tetap prioritas pemilik dan belum terselesaikan oleh paket katalog ini.

## Reproduksi

```bash
# GET metadata publik seluruh halaman + detail fork yang sudah ada.
# Memerlukan Python 3 dan gh terautentikasi; tidak ada remote write.
python3 scripts/plan_databricks_portfolio.py --refresh

# Regenerasi offline dari manifest tersimpan, tanpa akses API:
python3 scripts/plan_databricks_portfolio.py

# Tes offline planner dan metadata audit; parser tests opsional memerlukan PyYAML:
python3 -m unittest discover -s scripts -p 'test_portfolio_plan.py' -v
```

Generator memperbarui empat file: manifest JSON, katalog Markdown, dry-run Markdown, dan data web JSON. Rencana integrasi, bukti stack aplikasi serta ringkasan ini direview manual; tidak otomatis berubah saat refresh. File lama dibiarkan utuh jika pengambilan metadata gagal. Tidak ada mode `--execute`.

## Verifikasi tahap ini

- **10 tes planner lulus**: benturan nama case-insensitive, fork yang berganti nama, root-network review, lisensi unknown, archived/size gates, ID lintas pemilik, konsistensi output dan tidak adanya mode execute.
- **32 tes offline gabungan lulus** melalui `PYTHON=.venv/bin/python bash scripts/validate.sh` pada environment yang sudah memiliki PyYAML.
- JSON/Markdown hasil generator konsisten dengan snapshot; tautan file lokal tervalidasi dan `git diff --check` lulus.
- Terraform fmt di-skip karena CLI tidak tersedia. Tes ini tidak menjalankan fork, app build, npm/composer install, integrasi cloud atau deployment.

## Keputusan implementasi berikutnya

- Katalog/frontend: lanjutkan di sesi repository `repo-atlas-next`, review lima area: data, lint, kompatibilitas dependency, UI/aksesibilitas, build/test.
- Fork: tidak perlu semua 253 untuk menggunakan ekosistem. Mulai dari subset aktif yang memang perlu modifikasi, pertahankan atribusi dan lisensi, serta gunakan fork yang sudah ada.
- Laravel/semua bahasa: gunakan sebagai service/toolchain sesuai kebutuhan; bukan kumpulan runtime yang harus dipasang bersamaan dalam satu aplikasi atau repo Terraform.
