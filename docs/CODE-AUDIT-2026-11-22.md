# Audit isi kode — 79 repository devarent

Tanggal: **22 November 2026 (UTC)**. Lanjutan dari [audit metadata](AUDIT-2026-11-22.md).

## Ringkasan jujur tentang cakupan

- Semua **79 repo publik** dalam atlas diperiksa pada commit default branch yang dicatat di [data audit](CODE-AUDIT-DATA.json).
- **77 repo** dipindai melalui archive; `aws-rds` dan `dbx` menggunakan fallback Git tree karena archive melebihi batas 80 MiB. Tidak ada checkout/perubahan branch repo lain.
- **31.986 file teks dibaca secara otomatis** dari 55.295 file reguler yang terinventarisasi. Ini **bukan** 31.986 file yang sudah direview manusia atau dinyatakan benar.
- Pemeriksaan parser: **968 Python AST**, **2.516 strict JSON**, **713 YAML safe-load**, **313 bash syntax**. Tambahan pola workflow dan Compose bukan validasi schema lengkap.
- **27.424 file teks dibaca tanpa parser bahasa yang sesuai**, termasuk sebagian besar TypeScript/JavaScript, Rust, Java, PHP, SQL/CQL dan Terraform. Hanya contoh terpilih yang direview manual.
- **6 reproduksi lokal** mengonfirmasi bug terpilih; **5 patch usulan** lulus pemeriksaan applicability dan pemeriksaan terarah. Detail: [hasil probe](CODE-AUDIT-PROBES.json), [patches](audit-patches/README.md).
- Tes asli `database-labs-demo` dengan SQLite in-memory: **7 passed**, 1 warning deprecation dependency. Ini tidak membuktikan PostgreSQL atau deployment cloud lulus.
- **22 tes tooling audit lulus** dengan dependency parser terpasang. Tidak ada perubahan/push pada 78 repository lain.

## P0 — private key dalam `aws-rds`

File `my-aws-ec2-key.ppk` ter-commit di repo publik. Pemeriksaan terbatas menunjukkan header **PuTTY-User-Key-File-3**, `Encryption: none`, serta bagian private-key berisi baris data. Material key **tidak dicetak, tidak disalin ke laporan/patch, tidak digunakan untuk mencoba login**, dan tidak diuji apakah masih aktif.

**Tindakan segera pemilik:**

1. Identifikasi server/akun yang mempercayai public key pasangannya; cabut otorisasi key lama dan pasang key baru melalui jalur administrasi tepercaya. Menghapus EC2 key-pair di control plane saja tidak otomatis mencabut `authorized_keys` pada instance yang sudah berjalan.
2. Jika key masih dipercaya, perlakukan sebagai credential yang terpapar. Periksa log akses sesuai prosedur insiden. Jangan menempelkan private key di issue/chat.
3. Setelah rotasi/revokasi, hapus file dari tip dan bersihkan riwayat dengan prosedur terkoordinasi; pertimbangkan clone/fork/cache yang masih menyimpan salinan. Jangan melakukan rewrite history/force push tanpa rencana pemilik.
4. Tambahkan aturan ignore dan secret scanning, tetapi jangan menganggap `.gitignore` menghapus file yang sudah tracked.

Status: **keberadaan material private key terkonfirmasi; validitas/akses aktif belum diketahui**. Tidak ada bukti dalam audit ini bahwa akun sudah disusupi.

## Bug dan masalah yang direview

Tautan sumber di bagian [bukti commit](#bukti-commit) menunjuk snapshot yang diperiksa, bukan branch yang dapat berubah.

| ID | Repo / file | Bukti, dampak dan tindakan | Status |
|---|---|---|---|
| F01 | `arya123`, `uts-ec2-amazon-linux` — `UTS-EC2-WebHosting/ansible/deploy-static-apache.yml:65` | Baris literal `EOF` di luar YAML membuat playbook gagal diparse. Hapus baris heredoc yang tertinggal. | Dua reproduksi parser; dua patch. Ansible/SSH tidak dijalankan. |
| F02 | `aws-billing-qwen-3-32b` — `.vscode/launch.json:19` | Key JSON `ignoreFailures` kehilangan tanda kutip penutup. Debug configuration tidak valid. | Parser gagal sebelum, lulus sesudah; patch tersedia. |
| F03 | `chromadb-lab` — `examples/01_heartbeat.sh:3-4` | `curl -sS` mengembalikan exit 0 untuk HTTP 404, sehingga cabang fallback API v1 tidak dicoba. Gunakan `-f` agar HTTP error menghasilkan kegagalan shell. | Stub HTTP lokal mereproduksi; patch `-fsS` lulus. Chroma asli belum dijalankan. |
| F04 | `ml-pipeline-end-to-end` — `inference_deploy.py:54-58` | `pd.get_dummies(..., drop_first=True)` dihitung ulang per batch inference. Record SSH yang sama menghasilkan `service_ssh=0` jika sendirian, tetapi `=1` dalam batch bersama HTTP. Reindex tidak memulihkan kategori yang sudah dibuang. | Direproduksi terhadap fungsi asli yang direview, identity scaler. Gunakan encoder yang di-fit pada training dan diserialisasi bersama pipeline; jangan load pickle yang tidak dipercaya. |
| F05 | `database-labs-demo` — `app/main.py:49-58` | Validator strip berjalan setelah `min_length`; input dua spasi lolos lalu menjadi string kosong. Nama/kategori kosong bisa mencapai handler insert. | Reproduksi model Pydantic; patch before-validator menolak blank/karakter tunggal/non-string dan mempertahankan trim input valid. |
| F06 | `cassandra-lab` — `examples/01_schema.cql:11`, `examples/02_queries.cql:13-16` | PK `((day), event_time, device)` tidak mendukung `GROUP BY device` dengan hanya `day` dibatasi; clustering `event_time` dilewati. | Temuan review aturan CQL, belum dieksekusi pada Cassandra 5. Untuk agregat per device, desain tabel sesuai query (misalnya `((day), device, event_time)`) atau agregasi sisi aplikasi; jangan sekadar menambah `ALLOW FILTERING`. |
| F07 | `ml-pipeline-end-to-end` — `train_nids_model.py:58-63`, `generate_dataset.py:106-111` | Cabang saat CSV tidak ada memanggil generator yang hanya mengembalikan DataFrame, lalu langsung membaca CSV. Penulisan CSV hanya ada pada blok `__main__` generator yang tidak dijalankan saat import. | Terbukti melalui control-flow source; full training tidak dijalankan. Pakai DataFrame hasil fungsi atau simpan dengan `to_csv` sebelum membaca. |
| F08 | `ml-pipeline-end-to-end` — `train_nids_model.py:100-140,153-159`, `inference_deploy.py:45-55` | Median, batas clipping dan frekuensi kategori dihitung sebelum train/test split. Inference menggunakan frekuensi hard-coded serta tidak mengulang imputasi/clipping training. Ini berisiko leakage evaluasi dan training-serving skew. | Review source; besarnya dampak akurasi belum diukur. Split data dahulu, fit semua transformer hanya pada train, lalu gunakan pipeline yang sama untuk test/inference. |
| F09 | `repo-atlas-next` — `package.json:9,21` | Script `lint` adalah `next lint`, tetapi CLI paket Next **16.4.6** yang dipatok tidak mendaftarkan command `lint`. | Manifest dibandingkan dengan `package/dist/bin/next` pada tarball npm versi tepat. Versi paket memang ada; tidak dilaporkan keliru sebagai dependency tidak tersedia. Migrasikan ke ESLint CLI + config/dependency kompatibel dan uji `npm run lint`. Build aplikasi belum diuji. |

### Risiko kontekstual, bukan otomatis bug

- `elasticsearch-lab/examples/01_create_index.sh:3` dan `02_bulk.sh:3`: `curl -sS` tidak menggagalkan shell pada HTTP 4xx/5xx. Untuk bulk, HTTP 200 masih bisa mengandung kegagalan per item (`errors: true`), sehingga `-f` saja tidak cukup. Tambahkan pemeriksaan body JSON dan uji sengaja satu dokumen invalid. Ini review source, belum integration test Elasticsearch.
- `database-labs-demo/app/main.py:147-179`: endpoint mutasi tanpa autentikasi. **Sudah dinyatakan dalam `DEPLOY.md:159-171`**, jadi bukan temuan kerentanan tersembunyi baru. Pastikan proteksi proxy/auth/read-only diterapkan sebelum layanan publik; audit tidak memeriksa instance live.
- **21 kandidat port Compose** dipublikasikan tanpa binding loopback eksplisit. Untuk web frontend publik hal itu bisa disengaja. Untuk database/admin UI/lab lokal perlu peninjauan; keberadaan mapping tidak membuktikan dapat diakses dari internet karena firewall/proxy belum diketahui.
- `ibm-db2-lab`: `privileged: true` perlu lingkungan lab terisolasi. Jangan menghapusnya tanpa memeriksa kebutuhan image Db2 dan menguji startup.
- `redshift-lab/examples/02_queries.sql:1-9`: seed INSERT bukan idempotent. Menjalankan ulang dapat menggandakan data karena key Redshift bukan constraint uniqueness yang ditegakkan seperti OLTP. Dokumentasikan reset/repeat strategy pada schema lab khusus; jangan menjalankan cleanup destruktif pada data nyata. SQL belum diuji terhadap Redshift.
- Pada snapshot remote, dua repo SRA masih memiliki `docs-deploy.yml` yang seluruhnya komentar dan `checkout@main` pada tfsec commenter. Repo aktif sudah memiliki usulan checkout pin di working branch dari pekerjaan sebelumnya; snapshot remote tidak mencakup perubahan lokal itu. Aktivasi Pages tidak dilakukan otomatis.

## Menyaring false positive

Pemindai menghasilkan **107 kandidat**, bukan 107 bug terkonfirmasi:

- **66 strict-JSON failures:** 65 berada di `tsconfig*.json` yang memakai dialek JSONC/komentar/trailing comma. Jangan menghapus syntax JSONC yang valid hanya untuk memuaskan parser JSON biasa. Dalam audit ini 65 kandidat tersebut **tidak dihitung sebagai bug**; TypeScript belum memvalidasi konfigurasi tersebut. Satu error `.vscode/launch.json` dikonfirmasi sebagai F02.
- **3 YAML failures:** dua EOF playbook adalah F01. Satu CloudFormation `iac/cloudformation/al2023-stack.yaml` memakai intrinsic tags yang tidak dikenal safe-loader generik; **bukan bukti syntax CloudFormation salah**.
- Sisanya: 21 pola port Compose, 14 moving-branch Actions, 2 file workflow hanya komentar, dan 1 privileged container. Ini perlu penilaian konteks, bukan klaim eksploitasi atau runtime failure.
- **52 template YAML** dilewati parser karena templating, bukan dinyatakan valid.
- Tidak ditemukan error syntax oleh Python AST dan `bash -n` pada file yang dicakup. Import, tipe, dependency, kesesuaian versi interpreter, logika, concurrency dan hasil runtime **tidak** dibuktikan oleh parse saja.

## Hasil pengujian dan patch

- Enam reproduksi dalam [CODE-AUDIT-PROBES.json](CODE-AUDIT-PROBES.json) selesai dengan assertion yang diharapkan. Script menjalankan hanya fungsi ML dan model Pydantic yang direview dalam isolasi, bukan modul/training penuh, bukan saved-model pickle.
- Lima patch di [audit-patches](audit-patches/README.md) lulus `git apply --check` pada salinan file commit yang diperiksa. **Belum diterapkan pada repository asal**; patch tidak sama dengan PR yang sudah merged.
- `database-labs-demo`: tujuh tes asli lulus di SQLite in-memory, menggunakan FastAPI 0.115.6, SQLAlchemy 2.0.36, Pydantic 2.10.4, httpx 0.28.1, pytest 8.3.4. Tes asli belum mencakup whitespace-only input; F05 menjelaskan mengapa suite hijau belum cukup. Percobaan awal harness gagal mengimpor `app` karena cwd, lalu diperbaiki dengan menjalankan pytest dari root salinan demo; itu bukan bug repo.
- 22 tes offline tooling audit lulus menggunakan environment dengan PyYAML. Tanpa dependency opsional, 10 tes code-audit secara eksplisit di-skip; jangan laporkan sebagai lulus.
- Belum dilakukan: full build Next/React/shadcn/DevHub, kompilasi Rust/Java/Go/PHP/Arduino, tes engine SQL/CQL, Terraform validate/mock/live tests, Docusaurus build, vulnerability scan dependencies, inspeksi riwayat Git untuk seluruh secret, dan deploy cloud.
- `Docker`, Terraform, PHP, Java, Go dan Rust toolchains tidak tersedia di sandbox saat pemeriksaan. Tidak ada cloud credentials yang diminta atau dipakai.

## Reproduksi

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements-code-audit.txt
# Memerlukan gh terautentikasi; GET ke GitHub/codeload saja, tidak ada deploy/push
.venv/bin/python scripts/code_audit.py
# Tanpa network API; tes pemindai terhadap fixture sintetis
PYTHON=.venv/bin/python bash scripts/validate.sh

# Probe opsional terhadap cached source pada commit laporan; review script dahulu
.venv/bin/pip install -r scripts/requirements-audit-probes.txt
.venv/bin/python scripts/reproduce_code_findings.py
```

Archive berada di `.cache/repo-code-audit/`, di-ignore dan **tidak dipersist sebagai deliverable Git**. Jika cache hilang, unduh kembali archive commit yang tertera dalam JSON; jangan menyamakan hasil snapshot baru dengan temuan commit lama. `--repos NAME ... --output PATH` dapat dipakai untuk audit subset tanpa menimpa laporan semua repo.

Batas default: 80 MiB compressed/repo, 300 MiB expanded/repo, 1 MiB/file, 60.000 file/archive. Dependency/generated directories dilewati. Fallback tree maksimal 120 file, diprioritaskan workflow dan path dangkal; mode ini **bukan audit penuh repo besar**. Notebook (`.ipynb`), binary, lockfile berformat di luar daftar ekstensi, dan format lain bisa tidak tercakup. Seluruh skip dicatat di JSON. Tidak ada klaim bahwa semua kode di seluruh repo sudah bebas error.

## Urutan tindak lanjut

1. **Segera:** pemilik menangani key `aws-rds` (rotasi/revokasi sebelum cleanup).
2. Terapkan lima patch pada repo masing-masing melalui sesi/PR terpisah; jalankan tes native sebelum merge.
3. Perbaiki model query Cassandra dan pipeline preprocessing ML, lalu tambahkan regression/integration tests.
4. Migrasikan lint `repo-atlas-next`; periksa build dan deployment terpisah dari audit metadata.
5. Jalankan CI sesuai stack untuk semua repo, dengan prioritas pada file yang hanya dibaca tanpa parser dan 6.143 kandidat source `dbx` di luar sampel.

## Bukti commit

<!-- Source links and the complete per-repository coverage matrix follow. -->
- `aws-rds`: [my-aws-ec2-key.ppk](https://github.com/devarent/aws-rds/blob/0746fc97342ad513bc9b921c577eeee97933dc44/my-aws-ec2-key.ppk)
- `arya123`: [UTS-EC2-WebHosting/ansible/deploy-static-apache.yml:65](https://github.com/devarent/arya123/blob/d144474c8db891bddee5aad898f76bc6a5abab49/UTS-EC2-WebHosting/ansible/deploy-static-apache.yml#L65)
- `uts-ec2-amazon-linux`: [UTS-EC2-WebHosting/ansible/deploy-static-apache.yml:65](https://github.com/devarent/uts-ec2-amazon-linux/blob/af8f998ab1b86e12ab25945b26e3dd390d9d16f8/UTS-EC2-WebHosting/ansible/deploy-static-apache.yml#L65)
- `aws-billing-qwen-3-32b`: [.vscode/launch.json:19](https://github.com/devarent/aws-billing-qwen-3-32b/blob/f5e6ade8c2701389d1a401bbf30be217abde5d6e/.vscode/launch.json#L19)
- `chromadb-lab`: [examples/01_heartbeat.sh:3](https://github.com/devarent/chromadb-lab/blob/66b53871a4031843d8235d250ac94a679b03cb67/examples/01_heartbeat.sh#L3)
- `ml-pipeline-end-to-end`: [inference_deploy.py:54](https://github.com/devarent/ml-pipeline-end-to-end/blob/23a1da6a4f8a990dfd227b00e99059efca92a9cb/inference_deploy.py#L54)
- `ml-pipeline-end-to-end`: [train_nids_model.py:58](https://github.com/devarent/ml-pipeline-end-to-end/blob/23a1da6a4f8a990dfd227b00e99059efca92a9cb/train_nids_model.py#L58)
- `database-labs-demo`: [app/main.py:49](https://github.com/devarent/database-labs-demo/blob/84ab5618104e14b51f4f430c6a00e13ebf918a5d/app/main.py#L49)
- `cassandra-lab`: [examples/01_schema.cql:11](https://github.com/devarent/cassandra-lab/blob/eb0855eecde48d9e1ca0874946844dfb34474995/examples/01_schema.cql#L11)
- `cassandra-lab`: [examples/02_queries.cql:13](https://github.com/devarent/cassandra-lab/blob/eb0855eecde48d9e1ca0874946844dfb34474995/examples/02_queries.cql#L13)
- `repo-atlas-next`: [package.json:9](https://github.com/devarent/repo-atlas-next/blob/0c85f974531369796edfa90daeb0175042fe0314/package.json#L9)
- `elasticsearch-lab`: [examples/02_bulk.sh:3](https://github.com/devarent/elasticsearch-lab/blob/0f8e18f323da3a1128ca1f98c4903b90684b47b2/examples/02_bulk.sh#L3)
- `redshift-lab`: [examples/02_queries.sql:1](https://github.com/devarent/redshift-lab/blob/d26a000bd167229a9a5229514f3c281c719bb1de/examples/02_queries.sql#L1)

## Matriks seluruh 79 repo

Lihat [CODE-AUDIT-DATA.md](CODE-AUDIT-DATA.md) untuk setiap repository, commit, jumlah file, jumlah parser checks, kandidat mentah dan error pengambilan. [JSON](CODE-AUDIT-DATA.json) memuat lokasi kandidat dan semua hitungan skip.
