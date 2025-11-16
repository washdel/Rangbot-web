# 🚀 Panduan Setup RangBot - Instalasi Cepat

Dokumen ini berisi langkah-langkah instalasi dan setup untuk RangBot Web System.

## 📋 Checklist Sebelum Memulai

- [ ] Python 3.9+ terinstall
- [ ] pip terinstall
- [ ] Virtual environment (venv) ready
- [ ] Git (optional)
- [ ] Code editor (VS Code, PyCharm, dll)

## ⚡ Quick Start (5 Menit)

### 1. Setup Virtual Environment

```bash
# Masuk ke folder proyek
cd "D:\Semester 5\RPL\Project\Rangbot_Web"

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install semua package yang dibutuhkan
pip install -r requirements.txt
```

### 3. Setup Database

```bash
# Buat migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 4. Buat Admin User

```bash
# Buat superuser untuk akses admin panel
python manage.py createsuperuser

# Ikuti prompt:
# Username: admin
# Email: admin@rangbot.id
# Password: (masukkan password Anda)
```

### 5. Jalankan Server

```bash
# Jalankan development server
python manage.py runserver

# Server akan berjalan di: http://127.0.0.1:8000/
```

### 6. Akses Website

Buka browser dan akses:
- **Landing Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🎯 Struktur File yang Sudah Dibuat

```
Rangbot_Web/
├── 📁 rangbot_system/        # Django project settings
│   ├── settings.py           ✅ Configured
│   ├── urls.py               ✅ URL routing
│   ├── wsgi.py               ✅ WSGI config
│   └── asgi.py               ✅ ASGI config
│
├── 📁 main/                  # Main application
│   ├── views.py              ✅ Landing page view
│   └── urls.py               ✅ App URLs
│
├── 📁 templates/             # HTML templates
│   ├── base.html             ✅ Base template with Tailwind
│   └── landing.html          ✅ Complete landing page
│
├── 📁 static/                # Static files
│   ├── css/custom.css        ✅ Custom CSS
│   └── img/                  ⚠️  Add your images here
│
├── manage.py                 ✅ Django management
├── requirements.txt          ✅ Dependencies list
├── .gitignore                ✅ Git ignore rules
└── README.md                 ✅ Documentation
```

## 🎨 Konten Landing Page

Landing page yang sudah dibuat mencakup:

### ✅ Section yang Tersedia:

1. **Hero Section**
   - Judul utama dan subjudul
   - 2 CTA buttons (Mulai Gunakan, Pelajari Sistem)
   - Ilustrasi robot placeholder

2. **Tentang RangBot**
   - Penjelasan sistem robot
   - Mode kontrol (otomatis & manual)
   - Deteksi AI R-CNN
   - Firebase integration
   - Diagram alur sistem

3. **Fitur Utama (6 Cards)**
   - Deteksi Penyakit AI
   - Kontrol Robot
   - Monitoring Real-time
   - Peta Navigasi
   - Riwayat Deteksi
   - Notifikasi Member

4. **User Roles (3 Cards)**
   - Admin
   - Member
   - Guest

5. **Pricing Table (3 Plans)**
   - Basic: Rp 2.500.000/bulan
   - Standard: Rp 4.500.000/bulan (Popular)
   - Premium: Rp 8.000.000/bulan

6. **FAQ (Accordion)**
   - 5 pertanyaan dengan jawaban lengkap
   - Collapsible/expandable

7. **Forum Preview**
   - 3 postingan dummy
   - Nama, tanggal, jumlah replies

8. **Peta Kebun**
   - Blok A dan Blok B
   - Robot di rel tengah
   - Status tanaman (sehat/sakit)
   - Legend interaktif

9. **Call to Action**
   - CTA "Daftar Sekarang"
   - Statistik (500+ kebun, 99% akurasi, 24/7)

10. **Footer**
    - Quick links
    - Support links
    - Contact info
    - Social media icons

## 🛠️ Konfigurasi Tambahan

### Mengganti Secret Key (PENTING untuk Production)

Edit `rangbot_system/settings.py`:

```python
# Generate secret key baru dengan:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

SECRET_KEY = 'your-new-secret-key-here'
```

### Setup Static Files untuk Production

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Menambahkan Gambar

1. Letakkan gambar di `static/img/`
2. Format yang didukung: JPG, PNG, SVG, WebP
3. Update template jika perlu:

```html
{% load static %}
<img src="{% static 'img/robot-illustration.png' %}" alt="Robot">
```

## 🎨 Kustomisasi TailwindCSS

Landing page menggunakan TailwindCSS via CDN. Konfigurasi custom:

```javascript
// Di base.html
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    500: '#22c55e',  // Hijau utama
                    600: '#16a34a',  // Hijau gelap
                }
            }
        }
    }
}
```

Untuk mengubah warna tema, edit nilai di atas.

## 🔥 Fitur JavaScript yang Sudah Aktif

- ✅ Mobile menu toggle
- ✅ Navbar shadow on scroll
- ✅ Smooth scroll ke section
- ✅ FAQ accordion
- ✅ Scroll to top button
- ✅ Responsive design

## 📱 Responsiveness

Landing page fully responsive untuk:
- 📱 Mobile: 320px - 640px
- 📱 Tablet: 641px - 1024px
- 💻 Desktop: 1025px+

## 🐛 Troubleshooting

### Error: "django-admin tidak dikenali"

**Solusi**: Django belum terinstall. Jalankan:
```bash
pip install django==4.2.7
```

### Error: "No module named 'django'"

**Solusi**: Virtual environment belum diaktifkan. Jalankan:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Error: "TemplateDoesNotExist"

**Solusi**: Pastikan folder `templates/` ada di root proyek dan `settings.py` sudah dikonfigurasi dengan benar:
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

### Error: "Static files not loading"

**Solusi**: Jalankan dalam mode debug atau collect static:
```bash
python manage.py collectstatic
```

### Port 8000 sudah digunakan

**Solusi**: Gunakan port lain:
```bash
python manage.py runserver 8080
```

## 🚀 Next Steps

Setelah landing page berjalan, Anda bisa:

1. **Membuat fitur login/register**
   - Create views untuk authentication
   - Buat template login.html dan register.html

2. **Membuat dashboard**
   - Dashboard untuk admin
   - Dashboard untuk member
   - Integrasi Firebase

3. **Membuat sistem deteksi**
   - Upload image
   - AI detection integration
   - Display results

4. **Membuat kontrol robot**
   - Manual control (kanan/kiri)
   - Auto schedule
   - Real-time status

5. **Membuat forum**
   - CRUD posts
   - Comments & replies
   - User profiles

6. **Integrasi Firebase**
   - Setup Firebase project
   - Real-time database
   - Sensor data display

## 📚 Referensi

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Firebase Python SDK](https://firebase.google.com/docs/admin/setup)

## 💡 Tips Development

1. Selalu aktifkan virtual environment sebelum coding
2. Commit changes ke Git secara berkala
3. Test di berbagai device/screen size
4. Gunakan browser DevTools untuk debugging
5. Baca error message dengan teliti

## ✅ Verification Checklist

Setelah setup, pastikan:

- [ ] Server berjalan tanpa error
- [ ] Landing page tampil sempurna
- [ ] Navbar berfungsi (mobile & desktop)
- [ ] Semua link berfungsi
- [ ] FAQ accordion berfungsi
- [ ] Scroll smooth berfungsi
- [ ] Footer tampil dengan benar
- [ ] Admin panel bisa diakses
- [ ] Responsive di mobile

## 🎉 Selesai!

Jika semua langkah di atas berhasil, landing page RangBot sudah siap digunakan!

Untuk bantuan lebih lanjut, silakan hubungi:
- Email: info@rangbot.id
- WhatsApp: +62 812-3456-7890

---

**Happy Coding! 🚀**

