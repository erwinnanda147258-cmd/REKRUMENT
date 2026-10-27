# Audit dan validasi rebuild

## Temuan file asli

- Seluruh pertanyaan, termasuk informasi benefit dan konfirmasi administrasi, memiliki tombol skor 1–5 dan masuk penyebut total.
- Rekomendasi lanjut/pertimbangkan/tolak muncul setelah satu nilai diberikan; item belum dinilai secara implisit menurunkan persentase.
- Tidak ada bobot kompetensi, rubrik perilaku per item, pemisahan legal/safety gate, atau modul praktik.
- `scores` hanya berada di memori dan direset ketika posisi diganti. Data kandidat dan catatan tidak dipersistensikan. localStorage hanya menyimpan template tanpa validasi skema.
- ID berdasarkan urutan tampilan tidak permanen; tidak ada snapshot hasil lama atau versioning.
- Tambah/hapus pertanyaan merender ulang tanpa membaca teks input yang belum disimpan.
- Pertanyaan dan panduan di-render memakai `innerHTML` tanpa escape di mode interview, sehingga template berbahaya bisa menjadi XSS.
- Persyaratan SIM B1 dibuat seragam untuk driver, dan kepemilikan SIM/mengemudi berat dianggap kompetensi staf armada.
- Sejumlah item menilai kesiapan umum, kondisi kesehatan, tanggungan/dukungan keluarga atau respons kompensasi alih-alih kompetensi teramati.
- Print hanya menyembunyikan sebagian kontrol; belum berupa laporan formal lengkap.

## Implementasi

Tujuh template spesifik posisi, 57 pertanyaan inti dinilai (8 per posisi, driver 9), tujuh pertanyaan informasi latar belakang, rubrik 1–4, kompetensi dan bobot terpisah. Tujuh simulasi praktik dengan instruksi, bahan, checklist, rubrik, supervisi, catatan dan dokumentasi teks. Riwayat kandidat IndexedDB, autosave dengan antrean penulisan, status kegagalan simpan, snapshot dan versioning template, pencarian/filter, perbandingan rekap per posisi, JSON/CSV, editor, pengaturan, dashboard berdasarkan data aktual, serta laporan A–K dan CSS A4.

Data dinamis dirender dengan `textContent`/`.value`, bukan HTML interpolation. Nilai ekspor CSV yang berpotensi menjadi formula diberi awalan aman. Impor dibatasi 30 MB dan 10.000 sesi, divalidasi sebelum transaksi; ID/versi/rubrik/bobot/jawaban/persyaratan/praktik diuji. Persyaratan inti tidak boleh dihapus/dibuat N/A. Satu tab penulis diberlakukan melalui Web Locks jika tersedia.

## Pengujian yang dijalankan

1. Pemeriksaan sintaks JavaScript dengan Node.
2. Chromium + Playwright, jaringan browser dimatikan, dokumen disajikan dari memori tanpa aset eksternal.
3. **50 pemeriksaan domain**: tujuh template valid, sesi awal kosong, skor 75 saat semua nilai 3, praktik wajib, persyaratan yang belum memenuhi menghalangi lanjut, nilai kosong tidak menjadi nol, snapshot tidak berubah, bobot salah ditolak, dan nilai keselamatan kritis tidak tertutup skor tinggi.
4. **8 pemeriksaan tepi**: N/A sah dengan alasan, N/A tanpa alasan ditolak, skor 5 ditolak, N/A item wajib ditolak, ID duplikat ditolak, rubrik kosong ditolak, ID berbahaya ditolak, dan backup dengan duplikasi ID sesi ditolak.
5. Alur UI: kondisi kosong, membuat kandidat, menampilkan pertanyaan dan rubrik, memberi nilai dan catatan, simpan manual/autosave, refresh, buka draft kembali, kandidat kedua dengan posisi berbeda tidak tercampur.
6. Ketujuh posisi dipilih melalui UI dan masing-masing tes praktik diisi melalui UI; semua menghasilkan skor praktik 75 untuk nilai 3.
7. Editor: perubahan teks tetap ada ketika tambah, hapus dan urut, simpan versi baru; pembatalan serta konfirmasi reset template juga diuji; hasil lama tetap mempertahankan pertanyaan lama. Bobot 101% ditolak dan koreksi 100% tersimpan.
8. Download JSON aktual, impor ulang tanpa duplikasi, struktur impor tidak valid ditolak tanpa kehilangan data, download CSV aktual.
9. Pembatalan reset mempertahankan sesi; reset yang dikonfirmasi menghasilkan database kosong setelah refresh.
10. Input nama berupa markup berbahaya ditampilkan sebagai teks; tidak ada elemen gambar/script yang dibuat atau eksekusi XSS.
11. Kelengkapan asesmen, keputusan final dan alasan HRD, pembatalan penandaan final ketika asesmen diubah.
12. PDF draft dan lengkap dihasilkan melalui Chromium. PDF lengkap A4, 5 halaman dalam skenario uji dengan bukti/rubrik penuh; draft memiliki label belum lengkap. Ukuran/isi PDF diperiksa.
13. Lebar 1440, 768 dan 390 piksel tanpa overflow horizontal pada laporan. Screenshot dashboard desktop/mobile ditinjau. Tidak ada ID DOM duplikat, dependensi jaringan, atau error JavaScript pada dua suite.

## Batas dan verifikasi operasional

- Chromium terkelola memblokir navigasi `file://`. Pembukaan langsung file pada Chrome/Edge perangkat HRD belum diuji di lingkungan ini; isi HTML yang sama lulus konteks offline melalui origin lokal. Pengujian tidak memerlukan server produksi/backend.
- Firefox/Safari, printer fisik, perangkat ponsel nyata, kegagalan kuota disk nyata, dan pemulihan data setelah browser menghapus penyimpanan belum diuji. UI menyediakan status kegagalan penyimpanan dan backup JSON.
- Dokumentasi praktik berupa teks/referensi berkas, tanpa menyimpan foto atau berkas sensitif di database.
- Kompensasi, BPJS, cuti, potongan dan ketentuan kerja lama hanya referensi bertanda **Perlu Verifikasi HRD/Pusat**. Tidak menetapkan kebijakan perusahaan/hukum baru.
- SIM harus diverifikasi terhadap kendaraan sebenarnya dan aturan terkini. Tes mengemudi harus ditangani penguji kompeten dengan kondisi aman; aplikasi bukan sertifikasi kemampuan mengemudi.
- Bank pertanyaan, bobot dan threshold awal perlu kalibrasi HRD melalui evaluasi hasil kerja dan konsistensi antarpenilai; tidak ada klaim validitas prediktif/psikometri.
- Database lokal tidak terenkripsi oleh aplikasi dan tidak mempunyai autentikasi/otorisasi. Browser/profil/origin berbeda tidak berbagi data. Backup dan pengendalian akses perangkat tetap diperlukan.
