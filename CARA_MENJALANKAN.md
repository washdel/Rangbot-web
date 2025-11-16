# 🚀 Cara Menjalankan RangBot

## ⚡ Cara Tercepat (Recommended)

### Langkah 1: Jalankan Server
```
Double-click file: run_server.bat
```

### Langkah 2: Buka Browser
```
http://127.0.0.1:8000/
```

**SELESAI!** Landing page akan muncul! 🎉

---

## 📱 Cara Manual (Menggunakan Terminal)

### 1. Buka Terminal/CMD di folder ini

### 2. Aktifkan Virtual Environment
```bash
venv\Scripts\activate
```
*Anda akan lihat (venv) di awal prompt*

### 3. Jalankan Server
```bash
python manage.py runserver
```

### 4. Buka Browser
```
http://127.0.0.1:8000/
```

---

## 🛑 Cara Stop Server

Di terminal tempat server berjalan, tekan:
```
Ctrl + C
```

---

## 👨‍💼 Membuat Admin User

### Cara 1: Menggunakan Script
```
Double-click file: create_admin.bat
```

### Cara 2: Manual
```bash
venv\Scripts\activate
python manage.py createsuperuser
```

Ikuti prompt:
- Username: (pilih username Anda)
- Email: (opsional, bisa di-skip)
- Password: (pilih password, minimal 8 karakter)

Setelah dibuat, akses admin panel:
```
http://127.0.0.1:8000/admin/
```

---

## 📊 Struktur URL

| URL | Deskripsi |
|-----|-----------|
| `http://127.0.0.1:8000/` | Landing page (Home) |
| `http://127.0.0.1:8000/admin/` | Admin panel |

---

## 🔧 Jika Ada Masalah

### Setup Ulang (Jika Error)
```
Double-click file: setup.bat
```

Ini akan:
- Membuat ulang virtual environment
- Install ulang dependencies
- Setup ulang database

### Port 8000 Sudah Dipakai
Edit file `run_server.bat`, ganti baris:
```batch
python manage.py runserver
```
Menjadi:
```batch
python manage.py runserver 8080
```

Kemudian akses: `http://127.0.0.1:8080/`

### Server Tidak Jalan
1. Check apakah Python terinstall: `python --version`
2. Check apakah virtual environment aktif: lihat `(venv)` di prompt
3. Jalankan setup ulang: `setup.bat`

### Landing Page Tidak Muncul
1. Pastikan server jalan (check terminal)
2. Refresh browser (Ctrl + R)
3. Hard refresh (Ctrl + Shift + R)
4. Coba browser lain
5. Check console log browser (F12)

---

## 💻 Command Reference

### Server
```bash
# Start server (default port 8000)
python manage.py runserver

# Start dengan port custom
python manage.py runserver 8080

# Start dengan bind ke semua IP
python manage.py runserver 0.0.0.0:8000
```

### Database
```bash
# Run migrations
python manage.py migrate

# Create migrations (after model changes)
python manage.py makemigrations

# Reset database
python manage.py flush
```

### Admin
```bash
# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username
```

### Testing
```bash
# Run all tests
python manage.py test

# Check for issues
python manage.py check
```

---

## 📱 Test Responsive

1. Jalankan server
2. Buka browser
3. Tekan F12 untuk DevTools
4. Klik icon toggle device toolbar (atau Ctrl+Shift+M)
5. Pilih device:
   - iPhone SE (375px)
   - iPad (768px)
   - Desktop (1920px)

---

## ✅ Checklist Setelah Jalan

Pastikan:
- [ ] Server jalan tanpa error
- [ ] Landing page tampil dengan sempurna
- [ ] Navbar terlihat dan berfungsi
- [ ] Mobile menu berfungsi (resize window)
- [ ] FAQ accordion berfungsi (click pertanyaan)
- [ ] Smooth scroll berfungsi (click menu)
- [ ] Semua 10 section terlihat
- [ ] Footer tampil dengan benar
- [ ] Responsive di berbagai ukuran

---

## 🎉 Selesai!

Jika semua berjalan lancar, Anda sudah berhasil!

**Next Steps:**
1. Explore landing page
2. Baca dokumentasi di START_HERE.md
3. Mulai development fitur baru

**Happy Coding! 🚀**

