# 🔧 Command Reference - RangBot

Daftar lengkap command yang sering digunakan untuk development RangBot.

## 📋 Table of Contents
- [Virtual Environment](#virtual-environment)
- [Django Management](#django-management)
- [Database](#database)
- [Static Files](#static-files)
- [Users & Auth](#users--auth)
- [Development Server](#development-server)
- [Testing](#testing)
- [Git Commands](#git-commands)
- [Deployment](#deployment)

---

## 🐍 Virtual Environment

### Membuat Virtual Environment
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Aktivasi Virtual Environment
```bash
# Windows (PowerShell)
venv\Scripts\activate

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Install Dependencies
```bash
# Install semua dari requirements.txt
pip install -r requirements.txt

# Install package tertentu
pip install django==4.2.7

# Install dengan save ke requirements
pip freeze > requirements.txt
```

---

## ⚙️ Django Management

### Check Django Version
```bash
python manage.py --version
# atau
django-admin --version
```

### Help Command
```bash
# Lihat semua command yang tersedia
python manage.py help

# Help untuk command tertentu
python manage.py help migrate
```

### Create New App
```bash
python manage.py startapp nama_app
```

### Django Shell
```bash
# Interactive Python shell dengan Django context
python manage.py shell

# Contoh usage:
>>> from main.models import Robot
>>> robots = Robot.objects.all()
```

---

## 🗄️ Database

### Migrations

#### Create Migrations
```bash
# Buat migration untuk semua apps
python manage.py makemigrations

# Buat migration untuk app tertentu
python manage.py makemigrations main

# Buat migration kosong (untuk custom migration)
python manage.py makemigrations --empty main
```

#### Apply Migrations
```bash
# Apply semua migrations
python manage.py migrate

# Apply migration untuk app tertentu
python manage.py migrate main

# Apply sampai migration tertentu
python manage.py migrate main 0003
```

#### Check Migrations
```bash
# Lihat status migrations
python manage.py showmigrations

# Lihat SQL yang akan dijalankan
python manage.py sqlmigrate main 0001
```

#### Rollback Migration
```bash
# Rollback ke migration sebelumnya
python manage.py migrate main 0001

# Rollback semua migrations dari app
python manage.py migrate main zero
```

### Database Operations

#### Flush Database
```bash
# HATI-HATI: Hapus semua data!
python manage.py flush
```

#### DB Shell
```bash
# Access database shell
python manage.py dbshell
```

#### Load/Dump Data
```bash
# Export data ke JSON
python manage.py dumpdata > data.json
python manage.py dumpdata main > main_data.json

# Import data dari JSON
python manage.py loaddata data.json
```

---

## 📁 Static Files

### Collect Static Files
```bash
# Kumpulkan semua static files ke STATIC_ROOT
python manage.py collectstatic

# Without confirmation
python manage.py collectstatic --noinput

# Clear existing files first
python manage.py collectstatic --clear --noinput
```

### Find Static Files
```bash
# Cari lokasi static file tertentu
python manage.py findstatic css/custom.css
```

---

## 👤 Users & Auth

### Create Superuser
```bash
# Interactive mode
python manage.py createsuperuser

# Non-interactive (for scripts)
python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
```

### Change Password
```bash
# Change password untuk user tertentu
python manage.py changepassword admin
```

---

## 🚀 Development Server

### Run Server
```bash
# Default (127.0.0.1:8000)
python manage.py runserver

# Custom port
python manage.py runserver 8080

# Custom host dan port
python manage.py runserver 0.0.0.0:8000

# Specific IP
python manage.py runserver 192.168.1.100:8000
```

### Stop Server
```
Ctrl + C
```

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run tests untuk app tertentu
python manage.py test main

# Run specific test file
python manage.py test main.tests.test_views

# Run dengan verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

### Coverage (jika installed)
```bash
# Install coverage
pip install coverage

# Run tests dengan coverage
coverage run --source='.' manage.py test

# Lihat report
coverage report

# Generate HTML report
coverage html
```

---

## 📝 Git Commands

### Initial Setup
```bash
# Initialize Git
git init

# Add remote
git remote add origin https://github.com/username/rangbot-web.git

# Check remote
git remote -v
```

### Basic Workflow
```bash
# Check status
git status

# Add files
git add .
git add specific_file.py

# Commit
git commit -m "Add landing page"

# Push
git push origin main

# Pull
git pull origin main
```

### Branching
```bash
# Create new branch
git checkout -b feature/login

# Switch branch
git checkout main

# List branches
git branch

# Delete branch
git branch -d feature/login
```

### Undo Changes
```bash
# Discard changes (belum staged)
git checkout -- filename.py

# Unstage file
git reset HEAD filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## 🚢 Deployment

### Heroku

```bash
# Login
heroku login

# Create app
heroku create rangbot-app

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail

# Open app
heroku open
```

### VPS (Ubuntu)

```bash
# Connect via SSH
ssh user@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & pip
sudo apt install python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Setup project
cd /var/www/
git clone your-repo.git
cd your-repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Collect static
python manage.py collectstatic

# Setup Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 rangbot_system.wsgi

# Setup systemd service
sudo nano /etc/systemd/system/rangbot.service

# Restart services
sudo systemctl restart rangbot
sudo systemctl restart nginx
```

---

## 🛠️ Troubleshooting Commands

### Clear Python Cache
```bash
# Windows
for /r %i in (__pycache__) do @rd /s /q "%i"

# Linux/Mac
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Check for Issues
```bash
# Check for common problems
python manage.py check

# Check with tags
python manage.py check --tag models
python manage.py check --tag urls
```

### Debug Information
```bash
# Print Django settings
python manage.py diffsettings

# Print environment
python manage.py shell -c "import os; print(os.environ)"
```

---

## 📦 Package Management

### Pip Commands
```bash
# List installed packages
pip list

# Show package info
pip show django

# Upgrade package
pip install --upgrade django

# Uninstall package
pip uninstall package-name

# Install specific version
pip install django==4.2.7

# Install from requirements
pip install -r requirements.txt

# Create requirements.txt
pip freeze > requirements.txt
```

---

## 🔍 Useful One-Liners

```bash
# Count lines of Python code
find . -name "*.py" | xargs wc -l

# Find TODO comments
grep -r "TODO" --include="*.py"

# Find print statements (should use logging)
grep -r "print(" --include="*.py"

# Check Django version in project
python -c "import django; print(django.get_version())"

# List all URLs
python manage.py show_urls  # Requires django-extensions

# Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📱 Quick Reference Card

### Most Used Commands

| Command | Description |
|---------|-------------|
| `venv\Scripts\activate` | Activate venv (Windows) |
| `python manage.py runserver` | Start dev server |
| `python manage.py makemigrations` | Create migrations |
| `python manage.py migrate` | Apply migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py collectstatic` | Collect static files |
| `python manage.py test` | Run tests |
| `pip install -r requirements.txt` | Install dependencies |
| `git status` | Check git status |
| `git add . && git commit -m "msg"` | Commit changes |

---

## 💡 Pro Tips

1. **Always activate venv** before running Django commands
2. **Use `--help`** for any command to see options
3. **Create migrations** after changing models
4. **Test locally** before deploying
5. **Use git** to track changes
6. **Read error messages** carefully
7. **Check documentation** when stuck

---

## 📚 Documentation Links

- [Django Management Commands](https://docs.djangoproject.com/en/4.2/ref/django-admin/)
- [Django Migrations](https://docs.djangoproject.com/en/4.2/topics/migrations/)
- [Git Documentation](https://git-scm.com/doc)
- [Pip Documentation](https://pip.pypa.io/en/stable/)

---

**Keep this handy for quick reference! 🚀**

