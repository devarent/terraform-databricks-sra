# Usulan patch lintas repository — belum diterapkan

Patch ini disiapkan pada branch kerja `terraform-databricks-sra`, **bukan perubahan remote** pada repo tujuan. Tidak ada PR, push atau merge yang dilakukan. Snapshot commit dan hasil reproduksi ada di [CODE-AUDIT-PROBES.json](../CODE-AUDIT-PROBES.json).

| Patch | Repo tujuan | Perbaikan | Verifikasi lokal |
|---|---|---|---|
| [arya123.patch](arya123.patch) | devarent/arya123 | Hapus `EOF` yang tertinggal pada playbook Ansible | Parser YAML sesudah perbaikan + applicability |
| [uts-ec2-amazon-linux.patch](uts-ec2-amazon-linux.patch) | devarent/uts-ec2-amazon-linux | Perbaikan playbook yang sama | Parser YAML + applicability |
| [aws-billing-qwen-3-32b.patch](aws-billing-qwen-3-32b.patch) | devarent/aws-billing-qwen-3-32b | Tutup tanda kutip key `ignoreFailures` | Parser JSON + applicability |
| [chromadb-lab.patch](chromadb-lab.patch) | devarent/chromadb-lab | Tambahkan `curl -f` agar fallback heartbeat bekerja pada HTTP error | Stub HTTP 404/200 + applicability |
| [database-labs-demo.patch](database-labs-demo.patch) | devarent/database-labs-demo | Trim input sebelum validasi panjang, tetap tolak tipe non-string | Model Pydantic: blank/single-character/non-string ditolak, valid text di-trim + applicability |

## Cara menerapkan nanti

Di sesi terpisah untuk repository tujuan, review diff dan pastikan commit/file belum berubah signifikan. Dari root repo tujuan:

```bash
# Gunakan path nyata ke patch yang sesuai; jangan jalankan dari repo SRA ini.
git apply --check /path/to/appropriate.patch
git apply /path/to/appropriate.patch
```

Kemudian jalankan pengujian native repo dan review perubahan sebelum membuat PR. `git apply --check` hanya memeriksa kecocokan patch, **bukan** kebenaran runtime/deployment.

Patch `database-labs-demo` hanya memperbaiki validasi input, **bukan autentikasi endpoint**. Patch Chroma tidak menjamin versi server/SDK kompatibel. Perbaikan Cassandra dan ML membutuhkan desain/test lebih luas sehingga tidak diberi patch spekulatif.

Tidak ada private key, password atau hasil model yang disertakan. Jangan membuat patch yang menyalin key terpapar; revokasi/rotasi credential dilakukan oleh pemilik melalui jalur aman.

Sumber file yang dipatch berasal dari repository berlisensi MIT menurut snapshot GitHub. Pertahankan LICENSE dan atribusi repository tujuan; patch tidak mengganti lisensi sumber.
