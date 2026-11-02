# Sistem Manajemen Perpustakaan

## Deskripsi Aplikasi

Sistem Manajemen Perpustakaan adalah aplikasi desktop berbasis Python yang dibangun dengan arsitektur Model-View-Controller (MVC). Aplikasi digunakan untuk mengelola data koleksi buku dan anggota perpustakaan melalui antarmuka grafis (GUI) dengan data tersimpan di basis data MySQL. Aplikasi dilengkapi autentikasi login, otorisasi berbasis peran (admin dan anggota), pengujian otomatis, serta pipeline CI menggunakan GitHub Actions.

## Fitur

- Login dengan password ter-hash (SHA-256)
- Otorisasi berbasis peran: admin dapat menambah, mengubah, dan menghapus data; anggota hanya dapat melihat data
- CRUD data buku dan data anggota
- Unit test dengan pytest dan CI otomatis dengan GitHub Actions

## Struktur Direktori MVC

```
Modul3/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml
├── config/
│   └── database.py
├── models/
│   ├── buku_model.py
│   ├── anggota_model.py
│   └── user_model.py
├── views/
│   ├── buku_view.py
│   ├── anggota_view.py
│   └── login_view.py
├── controllers/
│   ├── buku_controller.py
│   ├── anggota_controller.py
│   └── auth_controller.py
├── tests/
│   ├── test_buku.py
│   └── test_auth.py
├── .gitignore
├── main.py
├── requirements.txt
├── test_model.py
├── test_register.py
└── README.md
```

## Panduan Instalasi dan Konfigurasi

### 1. Prasyarat

- Python 3.x
- Laragon (MySQL)
- Git

### 2. Clone repositori dan siapkan virtual environment

```
git clone https://github.com/username-anda/nama-repositori.git
cd nama-repositori
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

### 3. Konfigurasi database MySQL

Jalankan MySQL pada Laragon, buka Terminal Laragon, lalu masuk ke MySQL:

```
mysql -u root -p
```

Buat database dan tabel:

```sql
CREATE DATABASE perpustakaan;
USE perpustakaan;

CREATE TABLE buku (
    id_buku INT PRIMARY KEY AUTO_INCREMENT,
    judul VARCHAR(100) NOT NULL,
    penulis VARCHAR(100) NOT NULL,
    tahun_terbit YEAR
);

CREATE TABLE anggota (
    id_anggota INT PRIMARY KEY AUTO_INCREMENT,
    nama VARCHAR(100) NOT NULL,
    alamat TEXT
);

CREATE TABLE peminjaman (
    id_pinjam INT PRIMARY KEY AUTO_INCREMENT,
    id_buku INT NOT NULL,
    id_anggota INT NOT NULL,
    tanggal_pinjam DATE NOT NULL,
    tanggal_kembali DATE,
    FOREIGN KEY (id_buku) REFERENCES buku(id_buku),
    FOREIGN KEY (id_anggota) REFERENCES anggota(id_anggota)
);

CREATE TABLE users (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
);

INSERT INTO users (username, password, role) VALUES
('petugas', SHA2('admin123', 256), 'admin'),
('mahasiswa', SHA2('user123', 256), 'anggota');
```

Pengaturan koneksi (host, user, password) dapat disesuaikan pada file `config/database.py`.

## Cara Menjalankan Aplikasi

```
python main.py
```

Akun uji coba:

| Peran | Username | Password |
|---|---|---|
| Admin | petugas | admin123 |
| Anggota | mahasiswa | user123 |

Menjalankan pengujian otomatis:

```
python -m pytest -v
```

Membuat berkas eksekusi (.exe):

```
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```