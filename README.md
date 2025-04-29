YouTube Downloader

**YouTube Downloader** adalah aplikasi web sederhana yang memungkinkan pengguna untuk mengunduh video dari YouTube dalam berbagai format. Aplikasi ini dibangun menggunakan antarmuka web dan memanfaatkan pustaka seperti `youtube-dl` atau `pytube` (tergantung bahasa dan arsitektur proyek).

## 🎯 Fitur Utama

- Input URL video YouTube.
- Pilihan format: MP4 (video), MP3 (audio).
- Proses download cepat dan mudah.
- Antarmuka sederhana dan responsif.

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python (Flask) / PHP Native
- **Library**: `pytube` / `youtube_dl`
- **Frontend**: HTML, CSS (Bootstrap / Custom), JavaScript
- **Server**: XAMPP (PHP) atau Virtualenv (Python)

## 🗂️ Struktur Direktori (Contoh Umum)

```bash
youtube-downloader/
│
├── index.php / app.py         # Halaman utama
├── download.php / downloader/ # Proses download
├── templates/                 # Template (jika Python Flask)
│   └── index.html
├── static/                    # CSS, JS, dll
│   ├── css/
│   └── js/
├── uploads/                   # Tempat menyimpan file hasil download
└── requirements.txt / composer.json # File dependensi
```

## 🚀 Cara Menjalankan Aplikasi

### Jika menggunakan **Python Flask**:
1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan server lokal:
   ```bash
   python app.py
   ```

3. Akses di browser:
   ```
   http://localhost:5000
   ```

### Jika menggunakan **PHP Native**:
1. Jalankan XAMPP dan aktifkan Apache.
2. Letakkan folder `youtube-downloader` di direktori `htdocs`.
3. Akses via browser:
   ```
   http://localhost/youtube-downloader/index.php
   ```

## ⚠️ Catatan

- Pastikan server memiliki akses internet agar bisa mengambil video dari YouTube.
- Perlu command-line tools atau ekstensi tertentu tergantung library (misalnya `ffmpeg`).
- Perhatikan Terms of Service YouTube: penggunaan downloader harus sesuai hukum yang berlaku.

## 📄 Lisensi

Proyek ini hanya untuk tujuan pembelajaran. Penggunaan secara publik harus mempertimbangkan legalitas konten dan kebijakan YouTube.

---

