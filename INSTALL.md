# 🚀 Instalasi Super Mudah - RangBot

## ⚡ Cara Paling Mudah (Recommended)

### Langkah 1: Setup Otomatis
Double-click file ini:
```
setup.bat
```

**Setup script akan:**
- ✅ Membuat virtual environment
- ✅ Install Django dan dependencies
- ✅ Setup database
- ✅ Selesai dalam 2-3 menit!

### Langkah 2: Jalankan Server
Double-click file ini:
```
run_server.bat
```

Server akan jalan di: **http://127.0.0.1:8000/**

### Langkah 3 (Opsional): Buat Admin User
Double-click file ini:
```
create_admin.bat
```

Ikuti prompt untuk membuat username & password admin.

---

## 📝 Cara Manual (Jika Script Tidak Jalan)

### 1. Buat Virtual Environment
```bash
python -m venv venv
```

### 2. Aktifkan Virtual Environment
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

### 3. Install Dependencies Minimal
```bash
pip install Django==4.2.7
pip install django-cors-headers
pip install whitenoise
```

### 4. Setup Database
```bash
python manage.py migrate
```

### 5. Jalankan Server
```bash
python manage.py runserver
```

Buka browser: **http://127.0.0.1:8000/**

---

## 🎯 File Helper yang Tersedia

| File | Fungsi |
|------|--------|
| `setup.bat` | Setup otomatis (sekali jalan) |
| `run_server.bat` | Jalankan server |
| `create_admin.bat` | Buat user admin |

---

## 🐛 Troubleshooting

### Error: python tidak ditemukan
**Solusi:** Install Python 3.9+ dari python.org

### Error: pip tidak ditemukan
**Solusi:** 
```bash
python -m ensurepip --upgrade
```

### Virtual environment tidak aktif
**Tanda venv aktif:** Anda akan lihat `(venv)` di awal prompt
**Solusi:** Jalankan activate script lagi

### Port 8000 sudah digunakan
**Solusi:** Gunakan port lain:
```bash
python manage.py runserver 8080
```

### PowerShell execution policy error
**Solusi:** Gunakan CMD atau jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## ✅ Verifikasi Setup Berhasil

Setelah jalankan server, cek:
- [ ] Server jalan tanpa error
- [ ] http://127.0.0.1:8000/ menampilkan landing page
- [ ] Navbar terlihat dan berfungsi
- [ ] Semua section terlihat (Hero, Tentang, Fitur, dll)
- [ ] Mobile menu berfungsi (resize browser)
- [ ] FAQ accordion berfungsi

---

## 📱 Akses Landing Page

Setelah server jalan:

**Landing Page:**
```
http://127.0.0.1:8000/
```

**Admin Panel** (setelah create admin):
```
http://127.0.0.1:8000/admin/
```

---

## 💡 Tips

1. **Jangan tutup terminal** saat server berjalan
2. **Tekan Ctrl+C** untuk stop server
3. **Gunakan browser modern** (Chrome, Firefox, Edge)
4. **Test responsive** dengan resize browser
5. **Hard refresh** jika style tidak update (Ctrl+Shift+R)

---

## 🎉 Selesai!

Jika semua langkah berhasil, Anda sekarang bisa:
- ✅ Akses landing page
- ✅ Lihat semua fitur
- ✅ Test responsive design
- ✅ Mulai development

**Happy coding! 🚀**

