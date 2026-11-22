# Rencana integrasi web dan ekosistem bahasa

**Status: desain/kontrak integrasi, bukan aplikasi yang sudah dipasang.** Tidak ada dependency, file aplikasi, cloud resource atau repository remote yang diubah pada tahap ini.

## 1. Repository tujuan dan alasan

**Rekomendasi frontend: [`devarent/repo-atlas-next`](https://github.com/devarent/repo-atlas-next).** Repository itu sudah berfungsi sebagai control center portfolio, sehingga lebih tepat dikembangkan daripada menambah aplikasi web ke repo Terraform SRA ini. Implementasi dilakukan pada sesi/branch repository tujuan setelah pemilik menyetujui desain.

Pemeriksaan manifest pada 22 November 2026 tersimpan di [WEB-STACK-EVIDENCE.json](WEB-STACK-EVIDENCE.json), lengkap dengan commit dan URL sumber:

| Repo / lokasi | Deklarasi yang ditemukan | Implikasi |
|---|---|---|
| `repo-atlas-next/package.json` | Next `16.4.6`, React/React DOM `19.0.0`, Tailwind `^4.0.0`, Radix Dialog/Tabs/Tooltip/ScrollArea/Separator/Slot | Kandidat aplikasi utama; jangan pasang seluruh repo React/Radix/Databricks sebagai source dependency. |
| `nextjs-aws-production/app/package.json` | Next `14.2.15`, React `^18.3.1`, PostgreSQL client `pg` | Versinya berbeda; jadikan referensi deployment saja dahulu. Tidak ada upgrade lintas major otomatis. |
| `hris-itk-laravel/composer.json` | PHP `^8.2`, Laravel `^11.57` | Backend Laravel adalah opsi terpisah, bukan dependency npm. Repository ini berisi HRIS: jangan menautkan data karyawan/penggajian ke katalog publik. |
| `hris-itk-laravel/package.json` | Vite + Alpine + dependency frontend tersendiri | Jangan mencampur asset pipeline Laravel dan Next secara membabi buta. |

Ini adalah **constraint manifest**, bukan bukti lockfile sudah terpasang, versi tersedia di semua environment, kompatibilitas teruji, atau bebas kerentanan. Periksa engine Node, package-lock, advisory, lint dan build pada sesi implementasi. Audit sebelumnya menemukan `repo-atlas-next` masih memakai `next lint`; migrasikan ke ESLint CLI/config yang kompatibel sebelum menyatakan lint berhasil.

## 2. Bentuk integrasi yang disarankan

```text
Browser
  │ same-origin HTTPS
  ▼
repo-atlas-next — Next.js / React
  ├── Tailwind CSS untuk styling
  ├── Radix primitives untuk dialog, tabs, tooltip, keyboard/focus
  ├── HTML semantik + progressive rendering
  ├── katalog statis dari WEB-CATALOG.json (tanpa token/API saat browsing)
  └── route server /api/*, HANYA jika fitur dinamis diperlukan
         ├── GitHub metadata refresh (server/CI, read-only)
         ├── Databricks SDK/SQL connector terpilih (server-only, setelah use case disepakati)
         └── Laravel API opsional (authorization + DB, jaringan internal)
```

Tahap pertama **cukup katalog statis**. Tidak perlu database, akun Databricks, semua SDK, backend Laravel, atau 253 fork untuk menampilkan 332 entri katalog.

- Databricks upstream dan repository devarent adalah dua sumber yang berbeda, bukan klaim seluruh kode dibuat devarent.
- Archived disimpan untuk referensi, bukan direkomendasikan sebagai dependency produksi.
- Fork metadata menandakan hubungan GitHub, bukan otomatis lisensi atau hak atas seluruh konten.
- Semua fitur write/fork/deploy disembunyikan/tidak tersedia pada tahap ini. Jangan menambahkan tombol “Install all” yang menjalankan mutasi akun.

## 3. Kontrak data siap impor

File [WEB-CATALOG.json](WEB-CATALOG.json) memuat 332 item pada snapshot ini. Generator dapat menghasilkan jumlah berbeda setelah refresh; jangan hard-code 332 di aplikasi.

```typescript
type RepositoryCard = {
  id: string;                 // full_name, mis. databricks/devhub, BUKAN name saja
  github_id: number;
  name: string;
  owner: 'databricks' | 'devarent';
  source_kind: 'upstream' | 'owned';
  url: string;                // canonical GitHub URL dari API
  description: string | null;
  language: string | null;    // primary language saja
  license_spdx: string | null;
  archived: boolean;
  fork: boolean;
  category: string;           // heuristik navigasi, perlu koreksi manual bila salah
  size_kb: number;            // estimasi GitHub, bukan byte download
  integration_priority: string | null;
  verification: 'metadata_only';
};
```

Di sesi aplikasi tujuan:

1. Salin hanya payload metadata yang telah direview, misalnya ke `lib/data/repository-catalog.json`; jangan menyalin archive/source cache atau manifest secrets.
2. Tambahkan schema validation saat build, termasuk unique `id`, owner/source_kind yang valid, URL `https://github.com/<owner>/<name>`, tipe nullable, dan batas panjang teks.
3. Gunakan `id`/`full_name` sebagai React key dan kunci pencarian. Nama `devhub` atau `zerobus-sdk` muncul pada dua pemilik dan **tidak boleh saling menimpa**.
4. Buat tabs **Milik devarent** / **Upstream Databricks**, pencarian, filter bahasa/kategori/lisensi/archived/fork, badge `metadata only`, serta tanggal snapshot.
5. Render description sebagai teks React yang di-escape, bukan `dangerouslySetInnerHTML`. Batasi URL ke GitHub untuk link repo, tambahkan `rel="noopener noreferrer"` bila membuka tab baru.
6. Sediakan empty state, error state, loading state bila perlu, keyboard navigation dan focus management. Pagination/virtualization hanya jika profiling membuktikan perlu.
7. Cache metadata di repo atau artifact static. Fetch GitHub dilakukan server/CI dengan rate-limit handling, retry terbatas dan last-known-good snapshot; token tidak pernah di browser atau `NEXT_PUBLIC_*`.
8. Jangan memberi label “sudah diaudit/lulus tes” hanya karena metadata ada. Temuan audit source devarent tetap dokumen terpisah dan tidak berlaku otomatis untuk source upstream.

## 4. Integrasi bahasa / layanan — sesuai kebutuhan, bukan semua runtime sekaligus

| Teknologi | Peran yang masuk akal | Batas / gate sebelum implementasi |
|---|---|---|
| HTML, CSS, JavaScript, TypeScript | UI semantik, styling, interaksi dan type-check | ESLint, `tsc --noEmit`, tes aksesibilitas dan build. |
| React + Next.js + Tailwind + Radix | Aplikasi katalog/control center | Pakai package resmi yang diperlukan; review peer dependencies dan lockfile bersama. |
| PHP / Laravel | API CRUD/admin bila katalog butuh penyimpanan/workflow akun | Service terpisah; validation, policy, auth, CSRF bila cookie-based, rate limit, migration/rollback. HRIS bukan data publik. |
| Python | Metadata refresh, backend data/AI atau SQL connector | Dependency environment terpisah; jangan menjalankan notebook/model pickle asing dari browser. |
| Node.js Databricks SQL connector / SDK JS | Query use case server-side yang jelas | Pilih SDK sesuai API yang diperlukan; least-privilege OAuth/service principal, timeout, biaya query dan sanitasi hasil. |
| Java, Go, Rust, C/C++, Scala | Adapter/service sesuai SDK atau engine yang benar-benar dipakai | Build/test per repo dan batas API yang jelas; tidak dimasukkan sebagai dependency frontend. |
| Terraform/HCL, Shell, YAML | Provisioning dan CI | Plan/review manual, state terproteksi, secret manager, tidak ada `apply` dari katalog publik. |
| SQL, CQL dan notebook | Contoh/lab dan pipeline data | Dialek engine yang tepat, fixture sandbox, cleanup aman, tidak memakai database produksi. |
| Bahasa lain dalam katalog | Filter/referral ke repo sumber | Menampilkan bahasa tidak berarti memasang compiler/runtime atau membuktikan kode bekerja. |

SDK yang tepat dipilih setelah kebutuhan jelas; `databricks-sdk-py` dan `databricks-sql-python` memiliki peran berbeda. Dilarang menambahkan seluruh repo sebagai git submodule atau dependency hanya supaya semua nama muncul di tech stack.

## 5. Laravel opsional: kontrak dan pemisahan keamanan

Jika diperlukan fitur admin dinamis, proposal endpoint:

- `GET /api/repositories`: public metadata yang diizinkan, filter/pagination tervalidasi.
- `POST /api/admin/catalog-refresh`: admin terautentikasi, enqueue refresh read-only dengan timeout/idempotency/rate-limit.
- Tidak ada endpoint publik untuk fork massal, shell execution, cloud deployment, arbitrary URL fetch atau upload credential.

Browser memakai path relatif `/api/...`; Next/proxy meneruskan ke API internal. Jangan memakai `localhost` browser untuk menghubungi service remote. Definisikan CORS/origin, authentication dan audit log tanpa secret; fitur mutasi wajib mempunyai authorization per action. Jangan menyalin `.env`, credential DB atau informasi HRIS ke frontend.

## 6. Tahapan implementasi dan acceptance criteria

### Tahap A — katalog statis

- Implementasi di `repo-atlas-next`, bukan repo Terraform.
- Kedua kelompok muncul, semua ID unik, count sesuai payload, tidak ada data tertimpa akibat nama sama.
- Semua filter dan pencarian bekerja; archived/fork/license unknown tampil jelas.
- UI keyboard-accessible dan responsif; no token/network GitHub diperlukan untuk browsing.
- Lint baru, typecheck, build, unit tests parsing/filter, dan smoke tests halaman lulus.

### Tahap B — integrasi server terpilih

- Pilih satu use case (mis. query SQL sandbox), bukan semua connector sekaligus.
- Uji connector dengan mock lebih dahulu; query live hanya dengan otorisasi dan anggaran jelas.
- Tangani expired credential, 401/403/429, timeout, retry bounded, logging redacted dan error state.
- Backend Laravel hanya bila fitur membutuhkannya; tes unit/feature dan kontrak API terpisah.

### Tahap C — deployment

- Review Dockerfile, runtime Node/OS, healthcheck, TLS, CSP/headers, image vulnerability scan dan secret handling.
- Preview bind `0.0.0.0`, izinkan preview host yang sah, API browser tetap relative-origin.
- Tetapkan rollback image/snapshot, observability dan biaya. Deployment cloud tidak termasuk pekerjaan katalog/dry-run ini.

## 7. Hal yang belum dilakukan

Tidak ada perubahan di `repo-atlas-next`, `nextjs-aws-production`, `hris-itk-laravel`, atau upstream Databricks. Tidak ada `npm install`, `composer install`, app build, upgrade dependency, pembuatan service, fork, push atau deploy dalam paket rencana ini. Selesai di tahap ini berarti **katalog, data impor, kontrak integrasi dan rencana fork tersedia**, bukan 253 repo terpasang atau seluruh aplikasi sudah terhubung.
