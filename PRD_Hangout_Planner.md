# Product Requirements Document (PRD)

## Hangout Planner

_Aplikasi Budget Planner Nongkrong — Desktop App (Python Tkinter)_

|                 |                            |
| --------------- | -------------------------- |
| **Nama Proyek** | Hangout Planner            |
| **Platform**    | Desktop (Python + Tkinter) |

---

## 1. Ringkasan Produk

Hangout Planner adalah aplikasi desktop berbasis Python Tkinter yang membantu pengguna merencanakan kegiatan nongkrong sambil mengelola anggaran (budget) secara realistis. Aplikasi ini menggabungkan perencanaan tempat, estimasi biaya, split bill, serta penilaian kesehatan finansial dalam satu tampilan yang sleek dan modern dengan skema warna gelap (dark) bernuansa biru.

Masalah yang ingin diselesaikan: pengguna sering kesulitan memperkirakan total pengeluaran saat nongkrong (terutama jika mengunjungi lebih dari satu tempat), tidak sadar bahwa suasana hati (mood) memengaruhi pola belanja, dan tidak punya gambaran cepat apakah rencana nongkrongnya "aman" secara finansial atau tidak.

### 1.1 Tujuan Produk

- Membantu pengguna membuat rencana nongkrong yang terstruktur (tempat, tanggal, jumlah teman, transportasi, budget).
- Memberikan estimasi biaya per item di tiap tempat agar total pengeluaran lebih akurat.
- Memudahkan pembagian tagihan (split bill) antar teman.
- Memberikan rekomendasi "aman/tidak" terhadap suatu rencana berdasarkan saldo (Smart Budget).
- Menyadarkan pengguna akan hubungan mood dan kebiasaan belanja (Mood Budget).
- Menyajikan statistik dan skor kesehatan anggaran (Budget Health Score) dari waktu ke waktu.

### 1.2 Target Pengguna

- Mahasiswa/pekerja muda usia 18–27 tahun yang sering nongkrong bersama teman.
- Pengguna yang ingin lebih disiplin mengatur uang jajan/hiburan bulanan.
- Pengguna yang kadang nongkrong sendirian (self-care/me-time) sehingga fitur "tanpa teman" tetap relevan.

### 1.3 Ruang Lingkup

**Termasuk dalam lingkup (in-scope):**

- Autentikasi multi-user (register & login) dengan penyimpanan lokal SQLite.
- Dashboard, pembuatan rencana nongkrong, estimasi harga, split bill, smart budget, mood budget, statistik, dan budget health score — sesuai 10 fitur pada bagian 5.
- Seluruh data (user, rencana, item, riwayat) disimpan di database SQLite lokal (file `.db`) pada perangkat pengguna.
- Mata uang yang digunakan adalah Rupiah (Rp/IDR) dengan format ribuan Indonesia.

**Di luar lingkup (out-of-scope):**

- Sinkronisasi cloud / akun lintas perangkat, backend server, atau REST API eksternal.
- Fitur sosial (chat, undangan real-time ke teman, notifikasi push).
- Integrasi pembayaran digital (e-wallet, payment gateway).
- Manajemen tim, milestone tim, atau proses pengembangan multi-developer — karena proyek ini dikerjakan solo dengan bantuan AI co-pilot.

---

## 2. Tumpukan Teknologi

| Komponen              | Pilihan                                   | Catatan                                                                                     |
| --------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------- |
| Bahasa                | Python 3.10+                              | Kompatibel dengan tkinter & pustaka data                                                    |
| GUI Framework         | Tkinter (+ ttk)                           | Custom styling untuk tampilan modern; opsional pustaka seperti customtkinter jika diizinkan |
| Database              | SQLite3 (built-in Python)                 | File database lokal, tanpa server terpisah                                                  |
| ORM/Akses Data        | sqlite3 module atau SQLAlchemy (opsional) | Query langsung sudah cukup untuk skala aplikasi ini                                         |
| Visualisasi Statistik | matplotlib (embed ke Tkinter Canvas)      | Untuk grafik tren pengeluaran & mood                                                        |
| Mata Uang             | Rupiah (IDR)                              | Format: Rp 150.000                                                                          |

---

## 3. Prinsip Desain UI/UX

Desain mengusung gaya sleek & modern dengan dark color scheme bernuansa biru (blue undertone). Prinsip berikut wajib diterapkan konsisten di seluruh halaman:

- Kontras tinggi antara latar gelap dan teks agar tetap terbaca nyaman (accessibility).
- Sudut membulat (rounded corner) pada kartu (card), tombol, dan input field untuk kesan modern.
- Aksen warna biru terang digunakan untuk elemen interaktif (tombol utama, status aktif, grafik) — bukan pada seluruh background agar tidak ramai.
- Hierarki tipografi jelas: judul tebal & besar, subjudul medium, body text ringan.
- Feedback visual untuk status: hijau/biru muda untuk "aman", kuning untuk "waspada", merah/oranye untuk "boros/tidak aman".
- Konsistensi spacing dan alignment antar halaman agar transisi antar-frame Tkinter terasa mulus.

### Palet Warna yang Disarankan

| Warna | Hex       | Kegunaan                                          |
| ----- | --------- | ------------------------------------------------- |
| 🔵    | `#0B1220` | Background utama (navy sangat gelap)              |
| 🔵    | `#13203A` | Background kartu/panel (biru gelap kebiruan)      |
| 🔵    | `#3B82F6` | Aksen biru terang (tombol, highlight, grafik)     |
| 🔵    | `#1D4ED8` | Aksen biru sedang (hover, border aktif)           |
| ⚪    | `#94A3B8` | Teks sekunder / muted (abu kebiruan)              |
| ⚪    | `#F8FAFC` | Teks utama di atas background gelap (putih pucat) |
| 🟢    | `#22C55E` | Status aman / positif                             |
| 🟡    | `#F59E0B` | Status waspada                                    |
| 🔴    | `#EF4444` | Status boros / tidak aman                         |

### Tipografi

- Font disarankan: Segoe UI / Inter / Poppins (sesuai ketersediaan sistem) — sans-serif modern, mudah dibaca di layar gelap.
- Ukuran: Judul halaman 22–26px, subjudul 16–18px, body 12–14px, caption/label 10–11px.

---

## 4. Struktur Halaman & Navigasi

Aplikasi terdiri dari beberapa frame/window utama yang berpindah melalui sidebar navigasi (setelah login):

1. Halaman Login / Register
2. Dashboard
3. Buat Rencana Nongkrong
4. Estimasi Harga per Item
5. Split Bill
6. Smart Budget
7. Mood Budget
8. Statistik
9. Budget Health Score
10. Riwayat
11. Profil

Navigasi utama (dashboard, riwayat, statistik, profil, buat rencana) diakses melalui sidebar tetap di sisi kiri; sub-halaman (estimasi harga, split bill, smart budget, mood budget, health score) diakses dari dalam alur pembuatan/detail rencana.

---

## 5. Requirement Fungsional Detail

### F1 — Halaman Login & Register

Deskripsi: Gerbang masuk aplikasi dengan dukungan multi-user, sehingga beberapa orang dapat memakai aplikasi yang sama di satu perangkat dengan data terpisah.

- Form Login: input username/email + password, tombol "Masuk", link ke halaman Register.
- Form Register: input nama, username/email, password, konfirmasi password.
- Password disimpan dalam bentuk hash (mis. hashlib/bcrypt), bukan plain text, di tabel `users` pada SQLite.
- Validasi input: field kosong, format email (jika email dipakai), password minimal 6 karakter, username/email unik.
- Pesan error ditampilkan inline dengan warna aksen merah, tanpa mengganggu tata letak form.
- Setelah login berhasil, session user aktif disimpan di memori aplikasi (bukan di database) untuk digunakan di halaman lain.

### F2 — Dashboard

Deskripsi: Halaman utama setelah login yang merangkum kondisi finansial dan akses cepat ke fitur lain.

- Menampilkan saldo saat ini milik user yang login (card ringkasan besar di bagian atas).
- Tombol/aksi cepat: "Buat Rencana Nongkrong Baru".
- Ringkasan singkat: jumlah rencana aktif/akan datang, total pengeluaran bulan berjalan.
- Navigasi ke: Riwayat, Statistik, Profil.
- Preview Budget Health Score singkat (angka/skor + indikator warna) dengan tautan ke halaman detail.

### F3 — Buat Rencana Nongkrong

Deskripsi: Form untuk merancang satu sesi nongkrong baru.

- Tempat yang dikunjungi: input dinamis, dapat menambah lebih dari satu tempat (tombol "+ Tambah Tempat"), masing-masing tempat punya nama & opsional kategori (kafe, makan, karaoke, dll).
- Tanggal: date picker untuk tanggal rencana nongkrong.
- Jumlah teman: input angka, minimal 0 (0 = nongkrong sendirian); jika 0, label otomatis menampilkan "Solo Hangout".
- Budget: input nominal total budget yang dialokasikan untuk rencana ini (Rupiah).
- Transportasi: pilihan jenis transportasi (mis. motor pribadi, mobil pribadi, ojek online, transportasi umum, jalan kaki) beserta estimasi biaya transportasi opsional.
- Tombol "Simpan Rencana" menyimpan data ke tabel `plans` (dan `plan_locations`) di SQLite, lalu mengarahkan ke halaman Estimasi Harga per Item.

### F4 — Estimasi Harga per Item

Deskripsi: Rincian perkiraan biaya untuk tiap item yang akan dibeli, dikelompokkan per tempat yang sudah diinput pada F3.

- Untuk setiap tempat pada rencana, pengguna dapat menambahkan daftar item (nama item + estimasi harga satuan + jumlah).
- Subtotal otomatis dihitung per tempat, dan total keseluruhan dihitung otomatis di bagian bawah halaman.
- Total estimasi dibandingkan otomatis dengan budget yang diisi di F3; jika melebihi, tampilkan indikator peringatan (warna kuning/merah).
- Data item disimpan di tabel `plan_items` terhubung ke `plan_locations`.

### F5 — Split Bill

Deskripsi: Menghitung pembagian tagihan berdasarkan total pengeluaran aktual dan jumlah orang.

- Input: Total tagihan (bisa otomatis terisi dari total estimasi F4, dapat diedit manual) dan Jumlah orang (default = jumlah teman + 1 dari F3, dapat diubah).
- Output: nominal per orang (total ÷ jumlah orang), dibulatkan ke rupiah terdekat.
- Opsional: mode pembagian rata vs custom (per orang beda porsi) — ditampilkan sebagai pengembangan lanjutan (nice-to-have), bukan wajib di versi awal.
- Hasil split bill dapat disimpan sebagai bagian dari riwayat rencana.

### F6 — Smart Budget

Deskripsi: Ringkasan kesehatan finansial khusus untuk satu rencana, membandingkan saldo pengguna dengan biaya nongkrong yang direncanakan.

- Menampilkan: **Saldo** (saldo user saat ini), **Biaya Nongkrong** (total estimasi dari F4), dan **Status**.
- Status dihitung otomatis berdasarkan persentase biaya nongkrong terhadap saldo, contoh ambang batas (dapat disesuaikan):
  - < 30% saldo → "Aman"
  - 30–60% → "Cukup, tapi Perhatikan Pengeluaran Lain"
  - \> 60% → "Jangan Dipaksain"
- Output status ditampilkan singkat dan tidak menghakimi — bahasa yang suportif, contoh: "Aman, lanjut nongkrong! 🎉" atau "Agak berat nih, coba kurangi budget atau tunda dulu ya."
- Tidak memberi instruksi memaksa — aplikasi hanya memberi rekomendasi, keputusan akhir tetap di tangan pengguna.

### F7 — Mood Budget

Deskripsi: Slider mood yang menunjukkan potensi kenaikan/penurunan pengeluaran berdasarkan suasana hati pengguna saat merencanakan nongkrong.

| Mood | Label               | Efek Estimasi Pengeluaran           | Keterangan                                                                                                                   |
| ---- | ------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 😍   | Sangat Senang       | **+35%**                            | Ditentukan pengguna (Almaidah) — nilai final.                                                                                |
| 🤩   | Excited/Bersemangat | +25% _(asumsi)_                     | Perlu dikonfirmasi Almaidah.                                                                                                 |
| 🙂   | Senang              | +10% _(asumsi)_                     | Perlu dikonfirmasi Almaidah.                                                                                                 |
| 😐   | Netral              | 0% (baseline)                       | Titik tengah slider, tanpa penyesuaian.                                                                                      |
| 😭   | Sedih/Stres         | _Arah & besaran perlu dikonfirmasi_ | Sedih bisa membuat orang menahan diri (efek negatif) ATAU justru belanja impulsif (efek positif) — perlu keputusan Almaidah. |

Catatan implementasi: slider horizontal dengan 5 titik (mapping ke 5 emoji di atas). Saat pengguna menggeser slider, aplikasi menampilkan teks penjelasan otomatis (contoh: "Biasanya kalau lagi senang, pengeluaran meningkat 35%") dan mengalikan estimasi/biaya nongkrong pada F4/F6 dengan persentase mood yang dipilih sebagai simulasi "proyeksi pengeluaran realistis", ditampilkan berdampingan dengan estimasi normal (bukan menggantikannya).

### F8 — Statistik

Deskripsi: Visualisasi tren nongkrong dan pengeluaran pengguna dari waktu ke waktu, menggunakan matplotlib yang di-embed ke Tkinter.

- Grafik total pengeluaran per bulan (bar chart atau line chart).
- Distribusi pengeluaran per kategori tempat (pie chart / bar chart): kafe, makan, hiburan, transportasi, dll.
- Rata-rata pengeluaran per sesi nongkrong dan per orang.
- Korelasi mood vs pengeluaran (opsional lanjutan): menampilkan rata-rata pengeluaran berdasarkan mood yang paling sering dipilih.
- Filter periode: minggu ini, bulan ini, 3 bulan terakhir, semua waktu.

### F9 — Budget Health Score

Deskripsi: Skor tunggal (misal skala 0–100) yang merangkum kesehatan kebiasaan nongkrong & finansial pengguna secara keseluruhan (bukan per rencana seperti Smart Budget di F6).

- Komponen skor (dapat dikombinasikan dengan bobot tertentu): rasio rata-rata pengeluaran nongkrong terhadap saldo/pendapatan, frekuensi nongkrong per bulan, konsistensi tidak melebihi budget yang direncanakan, dan tren pengeluaran (naik/turun dibanding bulan lalu).
- Visualisasi: gauge/meter melingkar dengan warna sesuai skor (merah <40, kuning 40–70, hijau >70), ditampilkan di Dashboard (ringkas) dan halaman khusus (detail + breakdown komponen skor).
- Menyertakan 1-2 kalimat rekomendasi otomatis singkat berdasarkan skor, dengan nada suportif (bukan menghakimi).

### F10 — Riwayat & Profil

Deskripsi: Dua halaman pelengkap yang diakses dari dashboard, disebutkan pada requirement awal sebagai bagian dari dashboard.

**Riwayat**

- Daftar seluruh rencana nongkrong yang sudah lewat/selesai, urut dari terbaru.
- Setiap item riwayat menampilkan: tanggal, tempat (ringkas), total biaya aktual, status split bill.
- Dapat diklik untuk melihat detail lengkap (tempat, item, split bill, mood saat itu).

**Profil**

- Menampilkan data akun: nama, username/email, saldo saat ini (dapat diedit/top-up manual oleh pengguna).
- Opsi ubah password dan logout.

---

## 6. Struktur Data (Skema SQLite)

Skema berikut menjadi acuan implementasi database lokal (`hangout_planner.db`). Nama tabel dan kolom dapat disesuaikan selama pengembangan, namun relasi inti berikut wajib dipertahankan.

### 6.1 Entity Relationship Diagram (ERD)

```
┌───────────────────┐
│      users         │
│─────────────────── │
│ PK id               │
│    nama             │
│    username (UQ)    │
│    email (UQ)       │
│    password_hash    │
│    saldo            │
│    created_at       │
└─────────┬───────────┘
          │ 1
          │
          │ N
┌─────────▼───────────┐        1        N ┌──────────────────────┐
│       plans           │──────────────────▶│    plan_locations      │
│───────────────────────│                    │────────────────────────│
│ PK id                  │                    │ PK id                   │
│ FK user_id             │                    │ FK plan_id              │
│    nama_rencana        │                    │    nama_tempat          │
│    tanggal              │                    │    kategori             │
│    jumlah_teman         │                    │    urutan               │
│    budget                │                    └────────────┬────────────┘
│    transportasi          │                                 │ 1
│    transport_cost        │                                 │
│    mood                   │                                 │ N
│    mood_efek_persen       │                    ┌────────────▼────────────┐
│    status                  │                    │      plan_items          │
│    created_at              │                    │──────────────────────── │
└──────┬───────────┬────────┘                    │ PK id                    │
       │ 1          │ 1                          │ FK location_id           │
       │            │                            │    nama_item             │
       │ 1          │ N                          │    harga_satuan          │
┌──────▼──────┐  ┌──▼────────────┐               │    jumlah                │
│ split_bills  │  │  mood_logs     │               └──────────────────────────┘
│─────────────│  │───────────────│
│ PK id        │  │ PK id          │
│ FK plan_id   │  │ FK plan_id     │
│    total_    │  │    mood        │
│    tagihan   │  │    efek_persen │
│    jumlah_   │  │    catatan     │
│    orang     │  │    created_at  │
│    per_orang │  └────────────────┘
│    created_at│
└──────────────┘

┌──────────────────────────┐
│   budget_health_scores     │
│──────────────────────────│
│ PK id                       │
│ FK user_id                  │
│    periode (YYYY-MM)        │
│    score                    │
│    breakdown_json           │
│    created_at                │
└──────────────────────────┘
        ▲ N
        │
        │ 1
   (users.id)
```

**Ringkasan relasi:**

- `users` 1—N `plans` (satu user punya banyak rencana nongkrong)
- `plans` 1—N `plan_locations` (satu rencana punya banyak tempat)
- `plan_locations` 1—N `plan_items` (satu tempat punya banyak item estimasi)
- `plans` 1—1 `split_bills` (satu rencana punya satu hasil split bill)
- `plans` 1—N `mood_logs` (histori/penyesuaian mood untuk satu rencana; mood aktif tersimpan juga di `plans.mood`)
- `users` 1—N `budget_health_scores` (skor kesehatan anggaran dihitung & disimpan per periode/bulan)

### 6.2 Rincian Kolom per Tabel

**`users`** — data akun & saldo pengguna

| Kolom         | Tipe    | Constraint                | Keterangan                       |
| ------------- | ------- | ------------------------- | -------------------------------- |
| id            | INTEGER | PRIMARY KEY AUTOINCREMENT | ID unik user                     |
| nama          | TEXT    | NOT NULL                  | Nama tampilan                    |
| username      | TEXT    | NOT NULL, UNIQUE          | Dipakai untuk login              |
| email         | TEXT    | UNIQUE                    | Opsional, untuk login alternatif |
| password_hash | TEXT    | NOT NULL                  | Hash password (bcrypt/hashlib)   |
| saldo         | INTEGER | NOT NULL, DEFAULT 0       | Saldo pengguna saat ini (Rupiah) |
| created_at    | TEXT    | DEFAULT CURRENT_TIMESTAMP | Waktu akun dibuat                |

**`plans`** — satu baris = satu rencana nongkrong

| Kolom            | Tipe    | Constraint                | Keterangan                               |
| ---------------- | ------- | ------------------------- | ---------------------------------------- |
| id               | INTEGER | PRIMARY KEY AUTOINCREMENT | ID unik rencana                          |
| user_id          | INTEGER | NOT NULL, FK → users(id)  | Pemilik rencana                          |
| nama_rencana     | TEXT    |                           | Label opsional, mis. "Buka Puasa Bareng" |
| tanggal          | TEXT    | NOT NULL                  | Format ISO: YYYY-MM-DD                   |
| jumlah_teman     | INTEGER | NOT NULL, DEFAULT 0       | 0 = solo hangout                         |
| budget           | INTEGER | NOT NULL                  | Budget total (Rupiah)                    |
| transportasi     | TEXT    |                           | mis. motor pribadi, ojek online, dll     |
| transport_cost   | INTEGER | DEFAULT 0                 | Estimasi biaya transportasi              |
| mood             | TEXT    | DEFAULT '😐'              | Emoji mood terpilih                      |
| mood_efek_persen | REAL    | DEFAULT 0                 | Persentase efek mood (mis. 0.35)         |
| status           | TEXT    | DEFAULT 'draft'           | draft / berjalan / selesai / dibatalkan  |
| created_at       | TEXT    | DEFAULT CURRENT_TIMESTAMP | Waktu rencana dibuat                     |

**`plan_locations`** — tempat-tempat dalam satu rencana

| Kolom       | Tipe    | Constraint                                 | Keterangan                                 |
| ----------- | ------- | ------------------------------------------ | ------------------------------------------ |
| id          | INTEGER | PRIMARY KEY AUTOINCREMENT                  | ID unik tempat                             |
| plan_id     | INTEGER | NOT NULL, FK → plans(id) ON DELETE CASCADE | Rencana terkait                            |
| nama_tempat | TEXT    | NOT NULL                                   | Nama tempat (input bebas)                  |
| kategori    | TEXT    |                                            | kafe / makan / karaoke / hiburan / lainnya |
| urutan      | INTEGER | DEFAULT 0                                  | Urutan kunjungan (untuk sorting tampilan)  |

**`plan_items`** — item estimasi per tempat

| Kolom        | Tipe    | Constraint                                          | Keterangan                      |
| ------------ | ------- | --------------------------------------------------- | ------------------------------- |
| id           | INTEGER | PRIMARY KEY AUTOINCREMENT                           | ID unik item                    |
| location_id  | INTEGER | NOT NULL, FK → plan_locations(id) ON DELETE CASCADE | Tempat terkait                  |
| nama_item    | TEXT    | NOT NULL                                            | mis. "Kopi Susu", "Nasi Goreng" |
| harga_satuan | INTEGER | NOT NULL                                            | Harga per unit (Rupiah)         |
| jumlah       | INTEGER | NOT NULL, DEFAULT 1                                 | Jumlah unit dibeli              |

_Subtotal per item (`harga_satuan × jumlah`) dan total per tempat/rencana dihitung di level aplikasi (tidak disimpan sebagai kolom fisik) agar selalu konsisten dengan data terbaru._

**`split_bills`** — hasil pembagian tagihan per rencana

| Kolom         | Tipe    | Constraint                                         | Keterangan                        |
| ------------- | ------- | -------------------------------------------------- | --------------------------------- |
| id            | INTEGER | PRIMARY KEY AUTOINCREMENT                          | ID unik split bill                |
| plan_id       | INTEGER | NOT NULL, UNIQUE, FK → plans(id) ON DELETE CASCADE | Satu rencana = satu split bill    |
| total_tagihan | INTEGER | NOT NULL                                           | Total tagihan aktual (Rupiah)     |
| jumlah_orang  | INTEGER | NOT NULL                                           | Jumlah orang yang membagi tagihan |
| per_orang     | INTEGER | NOT NULL                                           | Hasil total ÷ jumlah_orang        |
| created_at    | TEXT    | DEFAULT CURRENT_TIMESTAMP                          | Waktu split bill dihitung         |

**`mood_logs`** — histori mood yang dipilih untuk suatu rencana

| Kolom       | Tipe    | Constraint                                 | Keterangan                        |
| ----------- | ------- | ------------------------------------------ | --------------------------------- |
| id          | INTEGER | PRIMARY KEY AUTOINCREMENT                  | ID unik log                       |
| plan_id     | INTEGER | NOT NULL, FK → plans(id) ON DELETE CASCADE | Rencana terkait                   |
| mood        | TEXT    | NOT NULL                                   | Emoji mood                        |
| efek_persen | REAL    | NOT NULL                                   | Persentase efek terhadap estimasi |
| catatan     | TEXT    |                                            | Catatan bebas opsional            |
| created_at  | TEXT    | DEFAULT CURRENT_TIMESTAMP                  | Waktu mood dicatat                |

**`budget_health_scores`** — histori skor kesehatan anggaran per periode

| Kolom          | Tipe    | Constraint                                 | Keterangan                          |
| -------------- | ------- | ------------------------------------------ | ----------------------------------- |
| id             | INTEGER | PRIMARY KEY AUTOINCREMENT                  | ID unik skor                        |
| user_id        | INTEGER | NOT NULL, FK → users(id) ON DELETE CASCADE | Pemilik skor                        |
| periode        | TEXT    | NOT NULL                                   | Format: YYYY-MM                     |
| score          | INTEGER | NOT NULL                                   | Skor 0–100                          |
| breakdown_json | TEXT    |                                            | Rincian komponen skor (JSON string) |
| created_at     | TEXT    | DEFAULT CURRENT_TIMESTAMP                  | Waktu skor dihitung                 |

### 6.3 DDL — Skrip SQLite Siap Pakai

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nama            TEXT NOT NULL,
    username        TEXT NOT NULL UNIQUE,
    email           TEXT UNIQUE,
    password_hash   TEXT NOT NULL,
    saldo           INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plans (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER NOT NULL,
    nama_rencana        TEXT,
    tanggal             TEXT NOT NULL,
    jumlah_teman        INTEGER NOT NULL DEFAULT 0,
    budget              INTEGER NOT NULL,
    transportasi        TEXT,
    transport_cost      INTEGER DEFAULT 0,
    mood                TEXT DEFAULT '😐',
    mood_efek_persen    REAL DEFAULT 0,
    status              TEXT DEFAULT 'draft',
    created_at          TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE plan_locations (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id      INTEGER NOT NULL,
    nama_tempat  TEXT NOT NULL,
    kategori     TEXT,
    urutan       INTEGER DEFAULT 0,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
);

CREATE TABLE plan_items (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id    INTEGER NOT NULL,
    nama_item      TEXT NOT NULL,
    harga_satuan   INTEGER NOT NULL,
    jumlah         INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (location_id) REFERENCES plan_locations(id) ON DELETE CASCADE
);

CREATE TABLE split_bills (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id         INTEGER NOT NULL UNIQUE,
    total_tagihan   INTEGER NOT NULL,
    jumlah_orang    INTEGER NOT NULL,
    per_orang       INTEGER NOT NULL,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
);

CREATE TABLE mood_logs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id       INTEGER NOT NULL,
    mood          TEXT NOT NULL,
    efek_persen   REAL NOT NULL,
    catatan       TEXT,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
);

CREATE TABLE budget_health_scores (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL,
    periode          TEXT NOT NULL,
    score            INTEGER NOT NULL,
    breakdown_json   TEXT,
    created_at       TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index untuk mempercepat query yang sering dipakai
CREATE INDEX idx_plans_user_id ON plans(user_id);
CREATE INDEX idx_plan_locations_plan_id ON plan_locations(plan_id);
CREATE INDEX idx_plan_items_location_id ON plan_items(location_id);
CREATE INDEX idx_mood_logs_plan_id ON mood_logs(plan_id);
CREATE INDEX idx_health_scores_user_periode ON budget_health_scores(user_id, periode);
```

### 6.4 Catatan Desain Skema

- `ON DELETE CASCADE` dipasang di semua foreign key turunan (`plan_locations`, `plan_items`, `split_bills`, `mood_logs`) agar menghapus satu rencana otomatis membersihkan seluruh data anaknya, tanpa data "yatim" (orphan record) yang membebani query statistik.
- `plans.mood` menyimpan mood **aktif/terakhir** untuk akses cepat (dipakai di F6 Smart Budget & F2 Dashboard), sedangkan `mood_logs` menyimpan **histori** jika pengguna mengubah mood beberapa kali sebelum menyimpan rencana — berguna untuk analitik korelasi mood-pengeluaran di F8.
- `split_bills.plan_id` diberi `UNIQUE` karena satu rencana hanya boleh punya satu hasil split bill aktif (relasi 1—1), sesuai F5.
- `budget_health_scores` dipisah dari `plans` karena skornya bersifat agregat bulanan lintas rencana (F9), bukan melekat pada satu rencana saja.
- Semua nominal uang disimpan sebagai `INTEGER` (bukan `REAL`) dalam satuan Rupiah penuh (bukan sen) untuk menghindari galat pembulatan angka desimal.

---

## 7. Requirement Non-Fungsional

- **Performa:** transisi antar-frame Tkinter harus terasa instan (<300ms) untuk data dengan skala wajar (puluhan rencana, ratusan item).
- **Keamanan data lokal:** password di-hash; file database SQLite sebaiknya disimpan di folder data aplikasi pengguna, bukan di folder instalasi.
- **Usability:** seluruh label, pesan error, dan status ditulis dalam Bahasa Indonesia yang ramah dan tidak menghakimi (sesuai nada suportif pada Smart Budget & Health Score).
- **Portabilitas:** aplikasi berjalan di Windows sebagai target utama (umumnya lingkungan Tkinter mahasiswa), dengan kemungkinan berjalan di macOS/Linux tanpa perubahan besar.
- **Maintainability:** struktur folder rapi, pemisahan antara UI (views), logika (services/controllers), dan akses data (SQLite) agar mudah dikembangkan lebih lanjut dengan bantuan AI co-pilot.

---

## 8. Asumsi & Batasan

- Proyek dikerjakan solo dengan bantuan AI co-pilot, sehingga dokumen ini tidak memuat pembagian tim, milestone tim, maupun proses manajemen proyek formal (mis. sprint, RACI).
- Nilai efek mood selain 😍 (+35%) pada F7 masih berupa asumsi awal dan perlu dikonfirmasi/disesuaikan oleh Almaidah sebelum implementasi final.
- Ambang batas status pada Smart Budget (F6) dan bobot komponen Budget Health Score (F9) merupakan usulan awal yang dapat disesuaikan berdasarkan preferensi pengguna.
- Tidak ada integrasi pihak ketiga (peta, pembayaran, dsb.); nama tempat pada F3 berupa input teks bebas, bukan hasil pencarian lokasi otomatis.

---

## 9. Kriteria Penerimaan (Definition of Done)

- [ ] Pengguna dapat register, login, dan logout dengan data tersimpan persisten di SQLite antar sesi aplikasi.
- [ ] Pengguna dapat membuat rencana nongkrong dengan minimal satu tempat, dan dapat menambah tempat lebih dari satu tanpa error.
- [ ] Total estimasi pada F4 terhitung otomatis dan konsisten dengan input item di setiap tempat.
- [ ] Split bill menghasilkan nominal per orang yang benar secara matematis untuk berbagai kombinasi total & jumlah orang, termasuk jumlah orang = 1 (solo).
- [ ] Smart Budget menampilkan status yang berubah secara konsisten sesuai ambang batas yang ditentukan, tanpa bahasa yang memaksa.
- [ ] Slider Mood Budget berfungsi untuk 5 titik emoji dan memengaruhi angka proyeksi pengeluaran sesuai persentase yang dikonfigurasi.
- [ ] Statistik menampilkan minimal satu grafik yang merefleksikan data riwayat pengguna secara akurat.
- [ ] Budget Health Score menghasilkan angka 0–100 dengan indikator warna yang konsisten dengan nilai skor.
- [ ] Tampilan seluruh halaman menggunakan dark color scheme bernuansa biru secara konsisten sesuai palet pada bagian 3.

---

_— Akhir Dokumen —_
