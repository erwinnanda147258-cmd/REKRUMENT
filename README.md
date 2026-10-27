# BARAKA Express — Recruitment Assessment System

Aplikasi asesmen rekrutmen lokal, berbahasa Indonesia, tanpa backend, CDN, atau login buatan.

## Menjalankan

1. Unduh/salin **INTERVIEW_BARAKA_FINAL.html**, lalu buka menggunakan Chrome atau Edge modern.
2. Pastikan indikator penyimpanan lokal siap. Gunakan satu tab dan browser/profil yang sama.
3. Tinjau **Pengaturan Penilaian**: kebijakan per posisi/cabang, bobot, ambang, dan persyaratan. Konfigurasikan kendaraan dan klasifikasi SIM untuk driver berdasarkan aturan yang sudah dikonfirmasi HRD. Referensi benefit lama belum menjadi kebijakan aktif.
4. Pilih **Interview Baru**, posisi, lalu jalankan lima tahap. Nilai tidak diisi otomatis. Gunakan rubrik dan catat bukti perilaku; pengalaman informal dapat dipakai.
5. Tes praktik wajib secara default untuk seluruh posisi. Pelaksanaan yang melibatkan kendaraan harus disupervisi penguji kompeten di area uji yang disetujui. Gunakan paket dummy/ringan untuk simulasi bongkar muat.
6. Review hasil, tetapkan keputusan serta alasan HRD setelah asesmen lengkap, lalu preview laporan dan **Cetak / Simpan PDF**.
7. Gunakan **Backup JSON** secara rutin dan sebelum menghapus/reset. CSV hanya rekap, bukan backup lengkap.

Jika browser memblokir IndexedDB saat membuka file lokal, aplikasi menampilkan kegagalan penyimpanan; jangan menutup sebelum mengekspor data. Alternatifnya jalankan server statis lokal menggunakan Python:

```sh
cd /path/ke/REKRUMENT
python -m http.server 8000 --bind 127.0.0.1
```

Buka file final melalui server lokal itu. Gunakan origin/port yang sama setiap kali. Data browser terikat profil dan origin; perpindahan lokasi/origin perlu backup/impor. Aplikasi tidak menyinkronkan perangkat dan tidak menyediakan kontrol akses enterprise. Simpan backup data kandidat dengan akses terbatas.

## Perhitungan dan keputusan

- Rata-rata nilai **1–4** dalam kompetensi ÷ 4 × bobot kompetensi. Jumlah bobot wajib tepat 100%.
- Item administrasi, informasi, persyaratan, gaji dan benefit tidak masuk skor.
- Nilai kosong tetap belum dinilai, bukan nol. N/A hanya untuk pertanyaan opsional nonkritis, dengan alasan; dikeluarkan dari rata-rata. Setiap kompetensi harus tetap mempunyai item wajib dinilai.
- Gabungan default interview/praktik: TKBM 50/50, Kenek 50/50, Driver 40/60, empat posisi staf 60/40. Tes praktik wajib default; bila ingin meniadakannya, nonaktifkan kewajiban dan set interview 100%.
- Nilai akhir dan kelengkapan administratif dibedakan. Belum memenuhi persyaratan mencegah rekomendasi lanjut meski skor tinggi.
- Ambang awal 75 untuk tahap berikutnya, 65 untuk pembinaan, batas keselamatan 3/4. Temuan kritis yang belum terselesaikan, item keselamatan di bawah batas, atau praktik di bawah batas mengarahkan ke pendalaman, bukan penolakan otomatis.
- Contoh: semua nilai 3 menghasilkan interview 75 dan praktik 75; total 75 untuk setiap konfigurasi bobot awal.
- Parameter ini konfigurasi awal internal, belum merupakan standar hukum atau instrumen psikometri tervalidasi. Keputusan tetap pada pihak berwenang.

Sesi menyimpan snapshot template: perubahan pertanyaan/rubrik/bobot/kebijakan tidak mengubah sesi lama. Pengubahan kendaraan/SIM pada sesi driver membatalkan verifikasi SIM sebelumnya. Suntingan asesmen membatalkan penandaan keputusan final sebelumnya.

## Backup dan editor

Impor menerima backup JSON versi 1, memvalidasi semua template dan sesi sebelum menulis secara atomik. ID sesi yang sudah ada **dilewati**, bukan ditimpa; impor ulang tidak menambah duplikat. Template aktif diganti dari backup setelah konfirmasi, sementara snapshot sesi lama tetap utuh. Untuk koreksi kandidat yang sudah ada, buka sesi tersebut dari riwayat.

Editor mempertahankan input saat tambah/hapus/urut. Klik **Validasi dan terapkan versi baru** untuk menyimpan. Draft editor belum tersimpan jika halaman dimuat ulang sebelum diterapkan. Penilaian kandidat tersimpan otomatis dan tersedia tombol simpan manual.

## Pengembangan dan pengujian

File distribusi mandiri dibangun dari `app.js`, `templates.json`, dan `legacy-policy.json`; file asli `INTERVIEW.html` tidak diubah.

```sh
python build.py
node --check app.js
python tests/test_browser.py
python tests/test_edges.py
```

Pengujian memerlukan Python Playwright dan Chromium di `/usr/bin/chromium`. Uji memakai konteks browser terisolasi; data uji tidak disertakan pada aplikasi. Lihat `AUDIT_DAN_PENGUJIAN.md` untuk bukti dan batas pengujian.
