# RangBot - Sistem Deteksi Penyakit Stroberi

![RangBot](https://img.shields.io/badge/RangBot-v1.0.0-green)
![Django](https://img.shields.io/badge/Django-4.2.7-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

Sistem deteksi penyakit stroberi berbasis robot cerdas dengan teknologi AI menggunakan metode R-CNN, dilengkapi dengan monitoring real-time melalui Firebase Realtime Database.

## 📋 Daftar Isi

- [Tentang Proyek](#tentang-proyek)
- [Fitur Utama](#fitur-utama)
- [Teknologi](#teknologi)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Dokumentasi API](#dokumentasi-api)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## 🌟 Tentang Proyek

RangBot adalah sistem inovatif yang menggabungkan robotika dan kecerdasan buatan untuk membantu petani stroberi dalam mendeteksi penyakit tanaman secara dini. Robot bergerak pada rel di tengah blok kebun dan dapat dikontrol secara otomatis (berdasarkan jadwal) atau manual melalui website.

### Cara Kerja

1. **Robot Bergerak**: Robot dipasang pada rel di tengah blok kebun, dapat bergerak kanan-kiri
2. **Deteksi AI**: Kamera + AI R-CNN mendeteksi penyakit pada tanaman stroberi
3. **Data Real-time**: Sensor mengirim data ke Firebase Realtime Database
4. **Dashboard Web**: User dapat melihat data dan mengontrol robot melalui website

## ✨ Fitur Utama

### 🤖 Deteksi Penyakit AI
- Menggunakan teknologi R-CNN untuk deteksi akurat
- Real-time detection dengan akurasi 99%
- Mendukung berbagai jenis penyakit stroberi

### 🎮 Kontrol Robot
- **Mode Otomatis**: Berdasarkan jadwal yang ditentukan
- **Mode Manual**: Kontrol langsung kanan-kiri melalui website
- Monitoring posisi robot real-time

### 📊 Monitoring Real-time
- Data sensor suhu, kelembaban, kondisi tanaman
- Integrasi Firebase Realtime Database
- Dashboard analytics yang informatif

### 🗺️ Peta Navigasi Kebun
- Visualisasi pembagian blok kebun
- Posisi robot pada peta interaktif
- Status kesehatan tanaman per blok

### 📜 Riwayat Deteksi
- Log lengkap deteksi penyakit
- Analisis historis untuk optimasi
- Export data ke CSV/PDF

### 📢 Notifikasi Member
- Alert deteksi penyakit
- Notifikasi anomali sensor
- WhatsApp & Email integration

### 💬 Forum Komunitas
- Diskusi antar petani stroberi
- Berbagi tips dan pengalaman
- Tanya jawab dengan expert

## 🛠️ Teknologi

### Backend
- **Django 4.2.7**: Web framework Python
- **SQLite**: Database (dapat diganti PostgreSQL/MySQL)
- **Firebase Admin SDK**: Integrasi Firebase Realtime Database
- **Django REST Framework**: API development (optional)

### Frontend
- **HTML5**: Markup language
- **TailwindCSS 3.0**: Utility-first CSS framework
- **JavaScript (Vanilla)**: Interactivity
- **Font Awesome**: Icons

### AI & Robotics
- **R-CNN**: Object detection untuk penyakit tanaman
- **OpenCV**: Image processing
- **Firebase Realtime Database**: Data sensor real-time

## 📦 Instalasi

### Prerequisites

Pastikan Anda telah menginstall:
- Python 3.9 atau lebih tinggi
- pip (Python package manager)
- Git (optional, untuk clone repository)

### Langkah-langkah Instalasi

1. **Clone atau Download Repository**

```bash
# Jika menggunakan Git
git clone https://github.com/your-username/rangbot-web.git
cd rangbot-web

# Atau download dan extract ZIP file
```

2. **Buat Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**

Buat file `.env` di root folder dengan copy dari `.env.example`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit file `.env` dan sesuaikan dengan konfigurasi Anda.

5. **Migrasi Database**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Buat Superuser (Admin)**

```bash
python manage.py createsuperuser
```

7. **Collect Static Files (Production)**

```bash
python manage.py collectstatic
```

8. **Jalankan Development Server**

```bash
python manage.py runserver
```

Buka browser dan akses: `http://127.0.0.1:8000/`

## 🚀 Penggunaan

### Akses Landing Page

Buka browser dan akses:
```
http://127.0.0.1:8000/
```

Landing page akan menampilkan:
- Hero section dengan CTA
- Informasi tentang RangBot
- Fitur-fitur utama
- User roles
- Paket harga
- FAQ
- Forum preview
- Peta kebun
- Call to action

### Akses Admin Panel

```
http://127.0.0.1:8000/admin/
```

Login menggunakan superuser yang telah dibuat.

### Setup TailwindCSS (CDN)

Landing page sudah menggunakan TailwindCSS via CDN. Untuk production, disarankan untuk:

1. **Install TailwindCSS via npm** (optional):

```bash
npm install -D tailwindcss
npx tailwindcss init
```

2. **Konfigurasi `tailwind.config.js`**:

```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './main/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#22c55e',
          600: '#16a34a',
        }
      }
    },
  },
  plugins: [],
}
```

3. **Build CSS**:

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

## 📁 Struktur Proyek

```
Rangbot_Web/
│
├── rangbot_system/           # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Konfigurasi utama
│   ├── urls.py               # URL routing utama
│   ├── wsgi.py
│   └── asgi.py
│
├── main/                     # Main app untuk landing page
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py              # Views untuk landing page
│   ├── urls.py               # URL routing app
│   └── tests.py
│
├── templates/                # Template HTML
│   ├── base.html             # Base template
│   └── landing.html          # Landing page
│
├── static/                   # Static files
│   ├── css/
│   │   └── custom.css        # Custom CSS
│   └── img/                  # Images
│       └── placeholder.txt
│
├── media/                    # User uploaded files
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # Dokumentasi (file ini)
```

## 🎨 Customization

### Mengubah Warna Tema

Edit di `templates/base.html`:

```html
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    primary: {
                        500: '#22c55e',  // Ubah warna di sini
                        600: '#16a34a',
                    }
                }
            }
        }
    }
</script>
```

### Menambahkan Gambar

1. Letakkan gambar di folder `static/img/`
2. Referensikan di template:

```html
{% load static %}
<img src="{% static 'img/logo.png' %}" alt="Logo">
```

### Menambah Section Baru

Edit `templates/landing.html` dan tambahkan section baru:

```html
<section id="section-baru" class="py-20 bg-white">
    <div class="container mx-auto px-4">
        <!-- Konten section baru -->
    </div>
</section>
```

## 🔌 Dokumentasi API

### Integrasi Firebase

Untuk mengintegrasikan dengan Firebase Realtime Database:

1. Install Firebase Admin SDK (sudah ada di `requirements.txt`)
2. Download service account key dari Firebase Console
3. Simpan di root folder sebagai `firebase-credentials.json`
4. Update `settings.py`:

```python
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-app.firebaseio.com'
})
```

### REST API (Optional)

Untuk membuat REST API menggunakan Django REST Framework:

1. Tambahkan `rest_framework` di `INSTALLED_APPS`
2. Buat serializers dan viewsets
3. Dokumentasi lengkap: https://www.django-rest-framework.org/

## 🧪 Testing

Jalankan test:

```bash
python manage.py test
```

## 📱 Responsive Design

Landing page sudah fully responsive untuk:
- 📱 Mobile (320px - 640px)
- 📱 Tablet (641px - 1024px)
- 💻 Desktop (1025px+)

## 🚀 Deployment

### Deploy ke Heroku

```bash
# Install Heroku CLI
heroku login
heroku create rangbot-app

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
heroku run python manage.py migrate
```

### Deploy ke VPS (Ubuntu)

1. Install dependencies: Nginx, Gunicorn, PostgreSQL
2. Setup virtual environment
3. Configure Nginx as reverse proxy
4. Use systemd untuk service management
5. Setup SSL dengan Let's Encrypt

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` file for more information.

## 👥 Tim Pengembang

- **Frontend Developer**: [Your Name]
- **Backend Developer**: [Your Name]
- **AI Engineer**: [Your Name]
- **Robotics Engineer**: [Your Name]

## 📞 Kontak

- Email: info@rangbot.id
- Website: https://rangbot.id
- Phone: +62 812-3456-7890

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)
- [Firebase](https://firebase.google.com/)

---

**© 2025 RangBot. All rights reserved.**

#   R a n g b o t - w e b  
 