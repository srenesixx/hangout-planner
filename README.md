# 🔵 Hangout Planner

**Hangout Planner** adalah aplikasi desktop berbasis GUI Python (menggunakan CustomTkinter) yang dirancang untuk membantu pengguna merencanakan kegiatan nongkrong (hangout) secara terstruktur sekaligus mengelola anggaran keuangan secara cerdas. 

Aplikasi ini mengintegrasikan estimasi pengeluaran di berbagai lokasi, pembagian tagihan (split bill), analisis budget cerdas, proyeksi pengeluaran berdasarkan suasana hati (mood), hingga perhitungan skor kesehatan anggaran pengguna secara berkala.

---

## 📥 Download Aplikasi (Siap Pakai - Windows Only)

Bagi pengguna umum yang ingin langsung menggunakan aplikasi **tanpa harus menginstal Python atau mengunduh source code**, silakan unduh aplikasi melalui tautan di bawah ini:

### 🚀 [**Download HangoutPlanner.exe (Rilis Terbaru)**](https://github.com/srenesixx/hangout-planner/releases/latest)

> 💡 **Cara Menjalankan:** 
> 1. Unduh file **`HangoutPlanner.exe`** dari tautan di atas (pada bagian *Assets*).
> 2. Pindahkan file tersebut ke **Desktop** Anda atau folder mana saja sesuai keinginan Anda.
> 3. Klik dua kali file `.exe` untuk membukanya. Database lokal (`hangout_planner.db`) akan otomatis dibuat di folder tempat file `.exe` diletakkan untuk menyimpan seluruh data Anda secara aman.

---

## ✨ Fitur Utama

1. **Autentikasi Multi-User (Login & Register)**:
   - Mendukung banyak pengguna pada satu perangkat dengan data terisolasi secara aman menggunakan hashing password.
2. **Dashboard Finansial**:
   - Menampilkan saldo aktif, total pengeluaran bulan berjalan, ringkasan rencana nongkrong mendatang, dan skor kesehatan finansial.
3. **Perencana Rencana Nongkrong (Hangout Planner)**:
   - Membuat rencana nongkrong dengan detail tanggal, jumlah teman (termasuk opsi *Solo Hangout*), alokasi budget, jenis transportasi, dan estimasi biayanya.
4. **Estimasi Biaya per Item**:
   - Menambahkan daftar item belanjaan/pesanan per lokasi tujuan dengan rincian harga satuan dan jumlah untuk membandingkan total estimasi dengan alokasi budget.
5. **Kalkulator Split Bill**:
   - Mempermudah pembagian tagihan secara rata di antara teman-teman yang ikut nongkrong.
6. **Smart Budget**:
   - Rekomendasi otomatis apakah rencana nongkrong "aman" dilakukan berdasarkan sisa saldo pengguna.
7. **Mood Budget (Proyeksi Mood)**:
   - Slider interaktif yang memproyeksikan potensi pembengkakan pengeluaran berdasarkan kondisi suasana hati (*mood*) pengguna saat merencanakan hangout.
8. **Statistik & Grafik**:
   - Visualisasi tren pengeluaran bulanan dan distribusi pengeluaran per kategori menggunakan Matplotlib.
9. **Budget Health Score**:
   - Penilaian skor kesehatan keuangan pengguna (skala 0–100) berdasarkan kebiasaan menabung dan pengeluaran nongkrong.
10. **Riwayat & Profil**:
    - Melihat daftar riwayat nongkrong sebelumnya dan manajemen profil serta saldo.

---

## 🛠️ Persyaratan Sistem

Aplikasi ini dapat dijalankan dengan dua metode:
1. **Metode Executable (`.exe`)**: Langsung dijalankan di Windows tanpa perlu menginstal Python atau library lainnya.
2. **Metode Source Code (Python)**: Memerlukan instalasi **Python** versi 3.10 atau yang lebih baru beserta pustaka pendukung di `requirements.txt`.

---

## 🚀 Cara Menjalankan Aplikasi

Pilih salah satu metode berikut untuk menjalankan aplikasi:

### Metode 1: Menggunakan Standalone Executable (Rekomendasi Cepat - Windows Only)
Metode ini adalah cara tercepat karena tidak memerlukan Python atau instalasi library tambahan.

1. Buka halaman rilis resmi di [GitHub Releases](https://github.com/srenesixx/hangout-planner/releases/latest).
2. Unduh file **`HangoutPlanner.exe`** dari daftar aset rilis terbaru.
3. Simpan file tersebut di mana saja (misalnya Desktop Anda) dan klik dua kali untuk membukanya.
4. Aplikasi akan mendeteksi/membuat file database lokal `hangout_planner.db` secara otomatis di folder yang sama untuk menyimpan data Anda.

---

### Metode 2: Menjalankan dari Source Code (Multiplatform / Development)
Gunakan metode ini jika Anda ingin memodifikasi kode atau menjalankan aplikasi di luar sistem operasi Windows.

#### 1. Persiapan Direktori
Pastikan Anda berada di direktori utama proyek `hangout-planner`.

#### 2. Buat & Aktifkan Virtual Environment (Sangat Disarankan)
Untuk menghindari konflik dengan library Python global di sistem Anda, buat virtual environment baru:

* **Di Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **Di Windows (CMD):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```
* **Di macOS/Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

#### 3. Instal Dependensi
Instal semua library yang dibutuhkan menggunakan `pip`:
```bash
pip install -r requirements.txt
```

#### 4. Jalankan Aplikasi
Jalankan file utama `main.py` menggunakan Python:
```bash
python main.py
```

Aplikasi Hangout Planner akan terbuka dalam jendela desktop baru.

---

### 📦 Cara Melakukan Build / Kompilasi Ulang ke Executable (.exe)
Jika Anda melakukan perubahan pada kode sumber dan ingin membuat file `.exe` baru secara lokal:

1. Pastikan library `pyinstaller` sudah terinstal di dalam virtual environment Anda:
   ```bash
   pip install pyinstaller
   ```
2. Jalankan perintah build langsung dari script utama `main.py`:
   ```bash
   pyinstaller --onefile --windowed --name HangoutPlanner main.py
   ```
3. File executable baru yang telah diperbarui akan dihasilkan kembali di dalam folder `dist/`.

---

## 📂 Struktur Folder Proyek

Proyek ini telah direfaktor menggunakan arsitektur **Model-View-Controller (MVC)** untuk meningkatkan modularitas, keterbacaan, dan pemeliharaan kode:

- `main.py`: Entrypoint utama aplikasi.
- `requirements.txt`: Daftar library eksternal yang dibutuhkan.
- `src/`: Direktori kode sumber utama.
  - `config.py`: Konfigurasi global aplikasi seperti judul aplikasi, ukuran jendela, dan lokasi database.
  - `models/`: Berisi logika data, interaksi database SQLite (`hangout_planner.db`), dan aturan bisnis.
    - `__init__.py`: Inisialisasi package models.
    - `database.py`: Inisialisasi skema database dan koneksi sqlite.
    - `auth.py`: Logika autentikasi user, password hashing, dan manajemen saldo.
    - `planner.py`: Logika rencana hangout, split bill, perhitungan score kesehatan anggaran, dan statistik.
  - `controllers/`: Bertindak sebagai perantara (bridge) untuk mengontrol aliran data antara model dan view.
    - `__init__.py`: Inisialisasi package controllers.
    - `auth_controller.py`: Menjembatani fungsi autentikasi user dan saldo ke tampilan antarmuka.
    - `planner_controller.py`: Menjembatani pengelolaan rencana, item estimasi, split bill, dan kalkulasi statistik ke tampilan antarmuka.
  - `views/`: Menangani visualisasi antarmuka pengguna (GUI) berbasis CustomTkinter.
    - `__init__.py`: Exporter seluruh view frames.
    - `components.py`: Kumpulan widget kustom (seperti `CardFrame`, `PrimaryButton`, `CustomEntry`, `CustomLabel`) dan skema warna/desain global.
    - `login.py`: Jendela masuk dan registrasi user.
    - `dashboard.py`: Jendela ringkasan, grafik Matplotlib, dan status keuangan terkini.
    - `create_plan.py`: Jendela formulir pembuatan rencana hangout baru.
    - `plan_detail.py`: Jendela kelola item pengeluaran, simulasi budget pintar, proyeksi mood, dan detail rencana.
    - `history.py`: Jendela riwayat rencana beserta perubahan status rencana.
    - `split_bill.py`: Jendela kelola pembagian tagihan dan status pelunasan teman.
    - `profile.py`: Jendela ubah saldo (top up) dan perubahan password.

---

## 💾 Penyimpanan Data
Aplikasi ini menggunakan database lokal **SQLite** (`hangout_planner.db`) untuk menyimpan semua informasi pengguna, rencana nongkrong, item estimasi, dan data split bill secara lokal di perangkat Anda.
