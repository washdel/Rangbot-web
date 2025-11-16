# ⚡ QUICKSTART - RangBot Web

Panduan super cepat untuk menjalankan RangBot dalam 3 menit!

## 🎯 3 Langkah Mudah

### 1️⃣ Setup Environment (1 menit)

```bash
# Masuk ke folder proyek
cd "D:\Semester 5\RPL\Project\Rangbot_Web"

# Buat dan aktifkan virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Setup Database (30 detik)

```bash
# Migrasi database
python manage.py migrate

# Buat admin user (opsional tapi recommended)
python manage.py createsuperuser
```

### 3️⃣ Jalankan Server (10 detik)

```bash
python manage.py runserver
```

## 🎉 Selesai!

Buka browser dan akses:
- **Landing Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📸 Screenshot Checklist

Pastikan Anda melihat:
- ✅ Hero section dengan gradient hijau
- ✅ Navbar yang sticky di atas
- ✅ Section "Tentang RangBot" dengan 4 poin
- ✅ 6 kartu fitur utama
- ✅ 3 kartu user roles
- ✅ 3 paket pricing (Standard highlighted)
- ✅ FAQ accordion yang bisa diklik
- ✅ 3 forum posts preview
- ✅ Peta kebun dengan Blok A & B
- ✅ CTA section dengan statistik
- ✅ Footer lengkap

## 🐛 Troubleshooting Cepat

### Error: ModuleNotFoundError

```bash
pip install django==4.2.7
```

### Port sudah digunakan

```bash
python manage.py runserver 8080
```

### Virtual environment tidak aktif

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## 📱 Test Responsive

1. Buka DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test di berbagai ukuran:
   - iPhone SE (375px)
   - iPad (768px)
   - Desktop (1920px)

## ✨ Fitur yang Bisa Langsung Dicoba

1. **Mobile Menu**
   - Klik hamburger icon di mobile view
   - Menu akan slide down

2. **FAQ Accordion**
   - Scroll ke section FAQ
   - Klik pertanyaan untuk expand/collapse

3. **Smooth Scroll**
   - Klik link di navbar
   - Page akan smooth scroll ke section

4. **Scroll to Top**
   - Scroll down ke bawah
   - Klik tombol hijau di kanan bawah

## 🚀 Next Steps

Setelah landing page jalan:

1. **Explore Admin Panel**
   ```
   http://127.0.0.1:8000/admin/
   ```

2. **Baca Dokumentasi Lengkap**
   - README.md → Overview & fitur lengkap
   - SETUP_INSTRUCTIONS.md → Panduan detail

3. **Mulai Development**
   - Tambah fitur login/register
   - Buat dashboard
   - Integrasi Firebase

## 💡 Tips

- Gunakan `Ctrl+C` untuk stop server
- Gunakan `Ctrl+Shift+R` untuk hard refresh browser
- Check console log jika ada error
- Baca error message dengan teliti

## 📞 Butuh Bantuan?

Jika ada masalah:
1. Baca SETUP_INSTRUCTIONS.md untuk troubleshooting detail
2. Check bahwa virtual environment aktif
3. Pastikan semua dependencies terinstall
4. Restart server jika perlu

---

**Happy Coding! 🎉**

