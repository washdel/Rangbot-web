# Quick Start Guide untuk Docker

## Prerequisites
- Docker Desktop installed
- Docker Compose installed

## 📋 Setup Steps

### 1. Copy environment file
```bash
cp .env.example .env
```

### 2. Build Docker images
```bash
docker-compose build
```

### 3. Start services (MySQL + Django)
```bash
docker-compose up
```

Aplikasi akan berjalan di: **http://localhost:8000**

### 4. Run migrations (jika belum otomatis)
```bash
docker-compose exec web python manage.py migrate
```

### 5. Create superuser (untuk admin panel)
```bash
docker-compose exec web python manage.py createsuperuser
```

## 🛠️ Useful Commands

### View logs
```bash
docker-compose logs -f web      # Django logs
docker-compose logs -f db       # MySQL logs
```

### Access MySQL directly
```bash
docker-compose exec db mysql -u rangbot_user -p rangbot_db
# Password: rangbot_pass
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Stop services
```bash
docker-compose down
```

### Reset everything (including data)
```bash
docker-compose down -v
docker-compose up --build
```

## 📚 Project Structure

```
.
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-container setup
├── .env                    # Environment variables (don't commit)
├── .env.example            # Template untuk .env
├── init.sql                # MySQL initialization
├── entrypoint.sh           # Container startup script
├── requirements.txt        # Python dependencies
├── manage.py              # Django management
├── rangbot_system/        # Django project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI application
├── main/                 # Main Django app
├── templates/            # HTML templates
└── static/              # CSS, JS, images
```

## 🐛 Troubleshooting

### "Connection refused" error
- Pastikan MySQL service sudah healthy
- Check logs: `docker-compose logs db`
- Wait 30 seconds setelah start container

### Port already in use
- Django (8000): `netstat -ano | findstr :8000`
- MySQL (3306): `netstat -ano | findstr :3306`
- Kill process atau ubah port di docker-compose.yml

### Database migration error
- Pastikan .env file sudah correct
- Reset database: `docker-compose down -v && docker-compose up --build`

## 📞 Support

Untuk bantuan lebih lanjut, lihat:
- README.md
- CARA_MENJALANKAN.md
- PROJECT_STRUCTURE.md
