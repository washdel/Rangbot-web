# 📚 Dokumentasi RangBot System

## 🎯 Overview
**RangBot** adalah sistem deteksi penyakit stroberi berbasis robot cerdas dengan teknologi **Machine Learning** untuk monitoring greenhouse yang efisien dan otomatis.

---

## 🚀 Teknologi Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: MySQL 8.0 (Docker)
- **ORM**: Django ORM dengan PyMySQL
- **Authentication**: Django Auth System
- **API**: Django REST Framework (optional)

### Frontend
- **CSS Framework**: Tailwind CSS 3.0
- **Template Engine**: Django Templates (Jinja2-style)
- **Icons**: Font Awesome, Custom SVG
- **JavaScript**: Vanilla JS untuk interaktivitas

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Django Development Server (production: Gunicorn)
- **Database**: MySQL 8.0 dalam Docker Container
- **Python**: 3.9-slim

### Machine Learning
- **Framework**: TensorFlow/PyTorch (untuk model deteksi)
- **Model**: R-CNN untuk object detection
- **Processing**: Real-time image processing
- **IoT Integration**: Firebase Realtime Database (optional)

---

## 📁 Struktur Project

```
Rangbot_Web/
├── 🐳 Docker Configuration
│   ├── .env                      # Environment variables (MYSQL credentials)
│   ├── .env.example              # Template environment variables
│   ├── docker-compose.yml        # Multi-container orchestration
│   ├── Dockerfile                # Development container
│   ├── Dockerfile.prod           # Production-optimized container
│   ├── .dockerignore             # Files excluded from Docker build
│   ├── entrypoint.sh             # Container startup script
│   └── init.sql                  # MySQL initialization script
│
├── 📄 Documentation
│   ├── RANGBOT_DOCS.md           # Dokumentasi lengkap (this file)
│   ├── DOCKER_QUICKSTART.md      # Quick start Docker guide
│   ├── DOCKER_SETUP_SUMMARY.md   # Detailed Docker setup
│   ├── CUSTOMIZATION_GUIDE.md    # Panduan kustomisasi
│   ├── DATABASE_INFO.md          # Database schema info
│   └── IMPLEMENTATION_STATUS.md  # Status implementasi fitur
│
├── 🎨 Frontend Assets
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css        # Custom styling
│   │   ├── img/                  # Images & placeholders
│   │   └── Logo/                 # Logo files
│   │
│   └── templates/
│       ├── base.html             # Base template dengan navbar & footer
│       ├── landing.html          # Landing page utama
│       ├── login.html            # Member login
│       ├── register.html         # Member registration
│       ├── product_info.html     # Informasi produk
│       ├── purchase.html         # Form pembelian
│       ├── contact_support.html  # Halaman support
│       │
│       ├── dashboard/            # Member Dashboard
│       │   ├── dashboard.html            # Dashboard utama
│       │   ├── device_control.html       # Kontrol robot
│       │   ├── device_detail.html        # Detail device
│       │   ├── device_detection_history.html  # Riwayat deteksi
│       │   ├── device_sensor.html        # Data sensor
│       │   ├── device_streaming.html     # Live camera feed
│       │   ├── manual_detection.html     # Upload image manual
│       │   ├── member_profile.html       # Profile member
│       │   ├── notifications.html        # Notifikasi member
│       │   └── add_device.html           # Tambah device baru
│       │
│       ├── admin/                # Admin Panel
│       │   ├── login.html               # Admin login
│       │   ├── dashboard.html           # Admin dashboard
│       │   ├── purchase_orders.html     # Daftar pesanan
│       │   ├── purchase_order_detail.html  # Detail pesanan
│       │   └── reject_purchase.html     # Form reject pesanan
│       │
│       └── forum/                # Forum Discussion
│           ├── forum_list.html          # Daftar diskusi
│           ├── forum_detail.html        # Thread diskusi
│           ├── forum_create.html        # Buat thread baru
│           ├── forum_edit.html          # Edit thread
│           └── forum_delete.html        # Hapus thread
│
├── 🔧 Django Apps
│   ├── main/                     # Main application
│   │   ├── models.py             # Database models
│   │   ├── views.py              # View functions
│   │   ├── admin_views.py        # Admin-specific views
│   │   ├── urls.py               # URL routing
│   │   ├── forms.py              # Django forms
│   │   ├── admin.py              # Django admin config
│   │   └── utils.py              # Helper functions
│   │
│   └── rangbot_system/           # Project settings
│       ├── settings.py           # Django configuration
│       ├── urls.py               # Root URL config
│       ├── wsgi.py               # WSGI config
│       └── asgi.py               # ASGI config
│
├── 🗃️ Database
│   ├── db.sqlite3                # SQLite (fallback, tidak digunakan)
│   └── migrations/               # Database migrations
│
└── 📦 Dependencies
    ├── requirements.txt          # Python packages
    ├── manage.py                 # Django management script
    └── README.md                 # Project README
```

---

## 🗄️ Database Schema

### Models Utama

#### 1. **Member**
```python
- username: CharField (unique)
- email: EmailField
- password: CharField (hashed)
- phone: CharField
- address: TextField
- is_registered: BooleanField
- registration_date: DateTimeField
```

#### 2. **Admin**
```python
- username: CharField (unique)
- password: CharField (hashed)
- email: EmailField
- created_at: DateTimeField
```

#### 3. **RangbotDevice**
```python
- member: ForeignKey(Member)
- device_name: CharField
- device_id: CharField (unique)
- status: CharField (choices: active/inactive/maintenance)
- battery_level: IntegerField (0-100)
- last_online: DateTimeField
- total_blocks: IntegerField
- covered_blocks: IntegerField
- detection_count: IntegerField
```

#### 4. **DetectionHistory**
```python
- device: ForeignKey(RangbotDevice)
- image: ImageField
- detection_result: JSONField
- confidence_score: FloatField
- disease_detected: CharField
- detection_date: DateTimeField
- notes: TextField
```

#### 5. **Notification**
```python
- member: ForeignKey(Member)
- title: CharField
- message: TextField
- notification_type: CharField (info/warning/critical)
- is_read: BooleanField
- created_at: DateTimeField
```

#### 6. **PurchaseOrder**
```python
- member: ForeignKey(Member)
- product_type: CharField
- quantity: IntegerField
- total_price: DecimalField
- status: CharField (pending/approved/rejected/completed)
- order_date: DateTimeField
- notes: TextField
```

---

## 🔐 Authentication & Authorization

### Member Authentication
- **Login**: `/login/`
- **Register**: `/register/`
- **Logout**: `/logout/`
- **Profile**: `/dashboard/profile/`

### Admin Authentication
- **Admin Login**: `/admin/login/`
- **Admin Panel**: `/admin/dashboard/`
- **Django Admin**: `/admin/` (Django default)

### Permission System
- **Public**: Landing page, Product info
- **Member Only**: Dashboard, Device control, Notifications
- **Admin Only**: Admin dashboard, Purchase order management

---

## 🌐 URL Routing

### Public Pages
```
/                           → Landing page
/product-info/              → Product information
/purchase/                  → Purchase form
/contact-support/           → Contact support
/login/                     → Member login
/register/                  → Member registration
```

### Member Dashboard
```
/dashboard/                                 → Dashboard home
/dashboard/device/<device_id>/              → Device detail
/dashboard/device/<device_id>/control/      → Device control
/dashboard/device/<device_id>/sensor/       → Sensor data
/dashboard/device/<device_id>/streaming/    → Live camera
/dashboard/device/<device_id>/history/      → Detection history
/dashboard/manual-detection/                → Upload image
/dashboard/add-device/                      → Add new device
/dashboard/profile/                         → Member profile
/dashboard/notifications/                   → Notifications
```

### Admin Panel
```
/admin/login/                   → Admin login
/admin/dashboard/               → Admin dashboard
/admin/purchase-orders/         → Purchase orders list
/admin/purchase-orders/<id>/    → Order detail
/admin/purchase-orders/<id>/reject/  → Reject order
```

---

## 🐳 Docker Deployment

### Quick Start
```bash
# 1. Clone repository
git clone <repository-url>
cd Rangbot_Web

# 2. Setup environment
cp .env.example .env
# Edit .env sesuai kebutuhan

# 3. Build and run
docker-compose up --build

# 4. Access application
# Web: http://localhost:8000
# MySQL: localhost:3306 (internal to containers)
```

### Docker Commands
```bash
# Start containers
docker-compose up

# Start in background
docker-compose up -d

# Stop containers
docker-compose down

# Rebuild containers
docker-compose up --build

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Reset database
docker-compose down -v
docker-compose up --build
```

### Environment Variables
```env
# MySQL Configuration
MYSQL_HOST=db
MYSQL_DATABASE=rangbot_db
MYSQL_USER=rangbot_user
MYSQL_PASSWORD=rangbot_pass
MYSQL_PORT=3306
MYSQL_ROOT_PASSWORD=root_password

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*
```

---

## 🎨 Frontend Features

### Landing Page Components
1. **Hero Section**: Animasi robot, CTA buttons
2. **Features**: 6 fitur utama dengan icons
3. **How It Works**: 4 langkah workflow
4. **Specifications**: Technical specs
5. **Technology Gallery**: Image showcase
6. **Statistics**: Live stats display
7. **Footer**: Company info, links, social media

### Dashboard Features
1. **Device Management**
   - Add new device
   - View device status
   - Control robot movement
   - View sensor data (temperature, humidity)
   - Live camera streaming

2. **Detection System**
   - Automatic detection history
   - Manual image upload
   - Detection results visualization
   - Confidence scores

3. **Notifications**
   - Real-time alerts
   - Disease warnings
   - System updates
   - Maintenance reminders

4. **Profile Management**
   - Edit member info
   - Change password
   - View subscription status

### Responsive Design
- **Mobile First**: Optimized for mobile devices
- **Tablet**: Adapted layouts for tablets
- **Desktop**: Full feature desktop experience
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)

---

## 🔧 Development Setup

### Local Development (Without Docker)
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver

# Access: http://127.0.0.1:8000
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate main 0001
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic

# Clear collected files
python manage.py collectstatic --clear
```

---

## 🤖 Machine Learning Integration

### Detection Pipeline
1. **Image Capture**: Camera captures strawberry image
2. **Preprocessing**: Resize, normalize, augment
3. **Model Inference**: R-CNN model prediction
4. **Post-processing**: Filter low confidence, draw bounding boxes
5. **Result Storage**: Save to database with metadata

### Model Configuration
```python
# settings.py
ML_MODEL_PATH = 'models/rcnn_strawberry_disease.h5'
ML_CONFIDENCE_THRESHOLD = 0.75
ML_IMAGE_SIZE = (640, 640)
ML_CLASSES = ['Healthy', 'Leaf Spot', 'Powdery Mildew', 'Botrytis']
```

### API Endpoints (Future)
```
POST /api/detect/           → Upload image for detection
GET  /api/devices/          → List all devices
GET  /api/devices/<id>/     → Device detail
POST /api/devices/<id>/move/ → Send movement command
GET  /api/history/          → Detection history
```

---

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test main

# Specific test case
python manage.py test main.tests.TestMemberModel

# With coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Production Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in settings
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use Gunicorn/uWSGI
- [ ] Setup Nginx as reverse proxy
- [ ] Enable HTTPS (SSL certificate)
- [ ] Configure database backups
- [ ] Setup monitoring (Sentry)
- [ ] Configure logging
- [ ] Setup firewall rules

### Docker Production
```bash
# Build production image
docker build -f Dockerfile.prod -t rangbot-web:latest .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📝 Future Features (TODO)

### Phase 1 - Core Functionality
- [x] Landing page design
- [x] Member authentication system
- [x] Device management dashboard
- [x] Basic detection history
- [ ] Real-time sensor data (Firebase integration)
- [ ] Live camera streaming (WebRTC)

### Phase 2 - Machine Learning
- [ ] Train R-CNN model for strawberry diseases
- [ ] Implement real-time detection
- [ ] Model versioning & deployment
- [ ] API for model inference
- [ ] Batch processing for historical images

### Phase 3 - IoT Integration
- [ ] Firebase Realtime Database connection
- [ ] MQTT protocol for device communication
- [ ] WebSocket for real-time updates
- [ ] Device firmware updates (OTA)
- [ ] Remote diagnostics

### Phase 4 - Advanced Features
- [ ] Analytics dashboard with charts
- [ ] Predictive maintenance
- [ ] Multi-language support (i18n)
- [ ] Mobile app (React Native)
- [ ] Export reports (PDF/Excel)
- [ ] Email notifications
- [ ] SMS alerts for critical events

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Docker Connection Error
```bash
# Problem: Can't connect to MySQL
# Solution: Check if MySQL container is running
docker-compose ps
docker-compose logs db

# Restart containers
docker-compose down -v
docker-compose up --build
```

#### 2. Port Already in Use
```bash
# Problem: Port 8000 or 3306 already in use
# Solution: Stop conflicting services
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
```

#### 3. Migration Errors
```bash
# Problem: Migration conflicts
# Solution: Reset migrations
docker-compose exec web python manage.py migrate --fake main zero
docker-compose exec web python manage.py migrate
```

#### 4. Static Files Not Loading
```bash
# Problem: CSS/JS not loading
# Solution: Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL in settings.py
```

---

## 📞 Support & Contact

### Development Team
- **Project**: RangBot Strawberry Disease Detection System
- **Version**: 1.0.0
- **License**: Proprietary
- **Repository**: https://github.com/washdel/Rangbot-web

### Getting Help
1. Check documentation in `/docs/` folder
2. Review `IMPLEMENTATION_STATUS.md` for feature status
3. Check Docker logs: `docker-compose logs -f`
4. Contact support via `/contact-support/` page

---

## 📄 License
Copyright © 2025 RangBot Team. All rights reserved.

---

**Last Updated**: November 17, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
