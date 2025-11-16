# 📂 Struktur Proyek RangBot

Dokumentasi lengkap struktur file dan folder proyek RangBot Web System.

## 🌳 Tree Structure

```
Rangbot_Web/
│
├── 📁 rangbot_system/              # Django project configuration
│   ├── __init__.py                 # Python package marker
│   ├── settings.py                 # ⚙️ Konfigurasi Django utama
│   ├── urls.py                     # 🔗 URL routing level proyek
│   ├── wsgi.py                     # 🚀 WSGI entry point
│   └── asgi.py                     # 🚀 ASGI entry point (async)
│
├── 📁 main/                        # Main application
│   ├── 📁 migrations/              # Database migrations
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                    # 👨‍💼 Admin panel config
│   ├── apps.py                     # 📦 App configuration
│   ├── models.py                   # 🗄️ Database models
│   ├── views.py                    # 👁️ Views & business logic
│   ├── urls.py                     # 🔗 URL routing app level
│   └── tests.py                    # 🧪 Unit tests
│
├── 📁 templates/                   # HTML templates
│   ├── base.html                   # 📄 Base template (parent)
│   └── landing.html                # 🏠 Landing page (child)
│
├── 📁 static/                      # Static files (CSS, JS, Images)
│   ├── 📁 css/
│   │   └── custom.css              # 🎨 Custom CSS
│   ├── 📁 img/                     # 🖼️ Images
│   │   └── placeholder.txt         # Guide untuk gambar
│   └── 📁 js/                      # (akan dibuat nanti)
│
├── 📁 media/                       # User-uploaded files
│   └── (empty - akan terisi saat ada upload)
│
├── 📄 manage.py                    # 🔧 Django management script
├── 📄 requirements.txt             # 📦 Python dependencies
├── 📄 .gitignore                   # 🚫 Git ignore rules
├── 📄 .env.example                 # 🔐 Environment variables template
├── 📄 LICENSE                      # ⚖️ MIT License
│
├── 📘 README.md                    # 📖 Dokumentasi utama
├── 📘 SETUP_INSTRUCTIONS.md        # 🚀 Panduan setup detail
├── 📘 QUICKSTART.md                # ⚡ Quick start guide
├── 📘 CUSTOMIZATION_GUIDE.md       # 🎨 Panduan kustomisasi
├── 📘 CHANGELOG.md                 # 📝 Version history
└── 📘 PROJECT_STRUCTURE.md         # 📂 File ini
```

---

## 📑 Penjelasan Detail Per File/Folder

### 🔧 Root Level

#### `manage.py`
Script utama Django untuk menjalankan command-line operations:
```bash
python manage.py runserver      # Start server
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin
python manage.py collectstatic   # Collect static files
```

#### `requirements.txt`
Daftar semua Python packages yang dibutuhkan:
- Django 4.2.7
- django-cors-headers
- Pillow (untuk image processing)
- Firebase admin SDK
- Django REST Framework (optional)

**Install semua:** `pip install -r requirements.txt`

#### `.gitignore`
File yang tidak akan di-track oleh Git:
- `*.pyc` - Python compiled files
- `venv/` - Virtual environment
- `db.sqlite3` - Database (development)
- `.env` - Environment variables (sensitive)
- `__pycache__/` - Python cache

#### `.env.example`
Template untuk environment variables. Copy ke `.env` dan isi:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Development mode (True/False)
- `ALLOWED_HOSTS` - Domain yang diizinkan
- Firebase credentials (optional)
- Email config (optional)

---

### ⚙️ rangbot_system/ (Project Config)

#### `settings.py` ⭐
File konfigurasi utama Django. Berisi:

**Installed Apps:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',      # Admin panel
    'django.contrib.auth',       # Authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # Session management
    'django.contrib.messages',   # Messages framework
    'django.contrib.staticfiles',# Static files
    'main',                      # Our main app
]
```

**Database Config:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Static Files:**
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**Templates:**
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # Template directory
        ...
    }
]
```

**Important Settings:**
- `SECRET_KEY`: Kunci rahasia (HARUS diubah di production!)
- `DEBUG`: True untuk development, False untuk production
- `ALLOWED_HOSTS`: ['*'] untuk development, ['yourdomain.com'] untuk production
- `LANGUAGE_CODE`: 'id-id' (Bahasa Indonesia)
- `TIME_ZONE`: 'Asia/Jakarta'

#### `urls.py`
URL routing level proyek:
```python
urlpatterns = [
    path('admin/', admin.site.urls),      # Admin panel
    path('', include('main.urls')),       # Include main app URLs
]
```

#### `wsgi.py` & `asgi.py`
Entry points untuk deployment:
- **WSGI**: Web Server Gateway Interface (traditional)
- **ASGI**: Asynchronous Server Gateway Interface (modern, supports WebSockets)

---

### 📱 main/ (Main Application)

#### `views.py` ⭐
Contains all view functions/classes:

**Landing Page View:**
```python
def landing_page(request):
    context = {
        'page_title': 'RangBot...',
        'features': [...],
        'pricing_plans': [...],
        'user_roles': [...],
        'faqs': [...],
        'forum_posts': [...],
    }
    return render(request, 'landing.html', context)
```

**Alur kerja:**
1. Request masuk dari user
2. View function process data
3. Prepare context (data untuk template)
4. Render template dengan context
5. Return HTML response

#### `urls.py`
URL routing level app:
```python
urlpatterns = [
    path('', views.landing_page, name='landing'),
    # path('login/', views.login_view, name='login'),  # Future
    # path('dashboard/', views.dashboard, name='dashboard'),  # Future
]
```

**URL Pattern Format:**
- `path('', ...)` → http://domain.com/
- `path('about/', ...)` → http://domain.com/about/
- `path('blog/<int:id>/', ...)` → http://domain.com/blog/123/

#### `models.py`
Database models (currently empty, akan diisi nanti):
```python
# Contoh model yang akan dibuat:
class Robot(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class DetectionResult(models.Model):
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    disease_type = models.CharField(max_length=100)
    confidence = models.FloatField()
    image = models.ImageField(upload_to='detections/')
    detected_at = models.DateTimeField(auto_now_add=True)
```

#### `admin.py`
Register models ke admin panel:
```python
# Contoh (untuk nanti):
from django.contrib import admin
from .models import Robot, DetectionResult

@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'status', 'created_at']
    search_fields = ['name', 'serial_number']
```

#### `migrations/`
Database migration files. Akan terisi setelah:
```bash
python manage.py makemigrations
```

---

### 🎨 templates/

#### `base.html` ⭐
Template parent (base) yang digunakan semua halaman:

**Struktur:**
```html
<!DOCTYPE html>
<html>
<head>
    <!-- TailwindCSS CDN -->
    <!-- Font Awesome -->
    <!-- Google Fonts -->
    <!-- Custom Config -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar (fixed) -->
    <nav>...</nav>
    
    <!-- Main Content (from child template) -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>...</footer>
    
    <!-- Scripts -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Features:**
- Navbar responsive dengan mobile menu
- Footer lengkap dengan links
- Scroll to top button
- Smooth scroll functionality
- Custom Tailwind config
- Font Awesome icons
- Google Fonts (Inter)

#### `landing.html` ⭐
Landing page yang extends base.html:

```html
{% extends 'base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
    <!-- Hero Section -->
    <section id="hero">...</section>
    
    <!-- Tentang RangBot -->
    <section id="tentang">...</section>
    
    <!-- Fitur Utama -->
    <section id="fitur">...</section>
    
    <!-- ... 7 sections lainnya ... -->
{% endblock %}

{% block extra_js %}
    <!-- FAQ accordion script -->
    <!-- Smooth scroll script -->
{% endblock %}
```

**10 Sections:**
1. Hero
2. Tentang RangBot
3. Fitur Utama
4. User Roles
5. Pricing
6. FAQ
7. Forum Preview
8. Peta Kebun
9. Call to Action
10. (Footer di base.html)

---

### 🎨 static/

#### `css/custom.css`
Custom CSS untuk styling tambahan:

**Contains:**
- Custom animations (float, pulse-slow)
- Gradient utilities
- Card shadows
- Loading spinner
- Responsive utilities
- Print styles

**Usage:**
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/custom.css' %}">
```

#### `img/`
Folder untuk menyimpan gambar:
- Logo
- Illustrations
- Icons
- Background images
- Product images

**Recommended sizes:**
- Logo: 512x512 px (PNG transparent)
- Hero images: 800x800 px
- Backgrounds: 1920x1080 px
- Icons: 128x128 px

**Usage:**
```html
{% load static %}
<img src="{% static 'img/logo.png' %}" alt="Logo">
```

---

### 📁 media/

Folder untuk user-uploaded files:
- Profile pictures
- Detection images
- Documents
- User content

**Auto-created by Django when:**
```python
# User uploads file
image = models.ImageField(upload_to='profiles/')
```

**Access in template:**
```html
<img src="{{ user.profile_image.url }}" alt="Profile">
```

---

## 🔄 Request/Response Flow

```
1. User → http://127.0.0.1:8000/
   ↓
2. Django URLs → rangbot_system/urls.py
   ↓
3. Include main.urls → main/urls.py
   ↓
4. Match path('') → views.landing_page
   ↓
5. View Function → Process data, prepare context
   ↓
6. Render Template → templates/landing.html
   ↓
7. Extend base.html → Inject content into {% block %}
   ↓
8. Load Static Files → CSS, JS, Images
   ↓
9. Return HTML Response → Browser renders page
```

---

## 📊 File Size Reference

```
rangbot_system/settings.py    ~4 KB   (konfigurasi)
main/views.py                  ~8 KB   (logic + data)
templates/base.html            ~12 KB  (struktur utama)
templates/landing.html         ~25 KB  (konten lengkap)
static/css/custom.css          ~2 KB   (styling)
requirements.txt               ~1 KB   (dependencies)
README.md                      ~15 KB  (dokumentasi)
```

**Total Project Size:** ~100 KB (tanpa dependencies & database)

---

## 🎯 Best Practices

### Struktur File
✅ **DO:**
- Pisahkan concerns (views, models, templates)
- Gunakan template inheritance
- Organize static files by type
- Keep views thin, models fat

❌ **DON'T:**
- Hardcode values (use settings)
- Mix business logic in templates
- Put everything in one file
- Ignore Django conventions

### Naming Conventions
```python
# Views (snake_case)
def landing_page(request):
    ...

# Models (PascalCase)
class Robot(models.Model):
    ...

# URLs (kebab-case)
path('detection-history/', ...)

# Templates (lowercase.html)
landing.html, user_profile.html
```

### Security
🔒 **Important:**
- Never commit `.env` file
- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Validate user inputs
- Use HTTPS in production

---

## 🚀 Future Structure (Planned)

```
Rangbot_Web/
├── main/              (landing, home)
├── accounts/          (login, register, profile)
├── dashboard/         (admin & member dashboard)
├── robot/             (robot control, status)
├── detection/         (AI detection, history)
├── forum/             (community forum)
├── api/               (REST API endpoints)
└── realtime/          (WebSocket, Firebase integration)
```

---

## 📚 Dokumentasi Terkait

- [README.md](README.md) - Overview proyek
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Panduan instalasi
- [QUICKSTART.md](QUICKSTART.md) - Quick start 3 menit
- [CUSTOMIZATION_GUIDE.md](CUSTOMIZATION_GUIDE.md) - Panduan kustomisasi
- [CHANGELOG.md](CHANGELOG.md) - Version history

---

**Last Updated:** 2025-11-14  
**Version:** 1.0.0

