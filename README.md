# 🔵 Hangout Planner

**Hangout Planner** adalah aplikasi desktop berbasis GUI Python (menggunakan CustomTkinter) yang dirancang untuk membantu pengguna merencanakan kegiatan nongkrong (hangout) secara terstruktur sekaligus mengelola anggaran keuangan secara cerdas. 

Aplikasi ini mengintegrasikan estimasi pengeluaran di berbagai lokasi, pembagian tagihan (split bill), analisis budget cerdas, proyeksi pengeluaran berdasarkan suasana hati (mood), hingga perhitungan skor kesehatan anggaran pengguna secara berkala.

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

Sebelum menjalankan aplikasi, pastikan sistem Anda sudah terinstal:
- **Python** versi 3.10 atau yang lebih baru.
- Library pendukung (Dependencies) yang terdaftar di `requirements.txt`.

---

## 🚀 Cara Menjalankan Aplikasi

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer lokal Anda:

### 1. Kloning atau Unduh Repositori
Pastikan Anda berada di direktori utama proyek `hangout-planner`.

### 2. Buat & Aktifkan Virtual Environment (Opsional tetapi Sangat Disarankan)
Untuk menghindari konflik dengan library Python global di sistem Anda, buat virtual environment baru:

**Di Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Di Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Di macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instal Dependensi
Instal semua library yang dibutuhkan menggunakan `pip`:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
Jalankan file utama `main.py` menggunakan Python:
```bash
python main.py
```

Aplikasi Hangout Planner akan terbuka dalam jendela desktop baru.

---

## 📂 Struktur Folder Proyek

- `main.py`: Entrypoint utama aplikasi.
- `src/`: Direktori kode sumber utama.
- `src/database.py`: Inisialisasi dan konfigurasi database SQLite (`hangout_planner.db`).
- `src/auth.py`: Logika registrasi, login, dan autentikasi user.
- `src/components.py`: Kumpulan widget CustomTkinter khusus dan skema warna/desain.
- `src/views/`: Layout dan halaman-halaman antarmuka aplikasi (Dashboard, Login, Create Plan, History, Profile, Split Bill, dll).
- `requirements.txt`: Daftar library eksternal yang dibutuhkan.

---

## 💾 Penyimpanan Data
Aplikasi ini menggunakan database lokal **SQLite** (`hangout_planner.db`) untuk menyimpan semua informasi pengguna, rencana nongkrong, item estimasi, dan data split bill secara lokal di perangkat Anda.
