# 🎯 DOCKER COMMAND REFERENCE CARD

## 🚀 Getting Started

```bash
# Navigate to project
cd C:\Users\kiaman\kuliah\S5\RPL\Rangbot_Web

# First time setup
docker-compose build

# Start services
docker-compose up

# Or background
docker-compose up -d

# Stop services
docker-compose down

# Reset everything (delete data)
docker-compose down -v
```

## 📊 Monitoring

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web          # Django
docker-compose logs -f db           # MySQL

# Check status
docker-compose ps

# Inspect service
docker-compose exec web bash
docker-compose exec db bash
```

## 🛠️ Django Management

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Make migrations
docker-compose exec web python manage.py makemigrations

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Django shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic

# Create test data
docker-compose exec web python manage.py shell
# Inside shell: run your fixture commands

# View all users
docker-compose exec web python manage.py shell << END
from django.contrib.auth.models import User
User.objects.all()
END
```

## 🗄️ Database Management

```bash
# Access MySQL CLI
docker-compose exec db mysql -u rangbot_user -p rangbot_db
# Password: rangbot_pass

# Backup database
docker-compose exec db mysqldump -u rangbot_user -p rangbot_db > backup.sql
# Password: rangbot_pass

# Import database
docker-compose exec -T db mysql -u rangbot_user -p rangbot_db < backup.sql
# Password: rangbot_pass

# List databases
docker-compose exec db mysql -u root -proot123 -e "SHOW DATABASES;"

# Show tables
docker-compose exec db mysql -u rangbot_user -p rangbot_db -e "SHOW TABLES;"
# Password: rangbot_pass
```

## 🔧 Build & Rebuild

```bash
# Build with no cache
docker-compose build --no-cache

# Rebuild specific service
docker-compose build --no-cache web
docker-compose build --no-cache db

# Rebuild and start
docker-compose up --build

# Force recreate
docker-compose up --force-recreate --build
```

## 🧹 Cleanup

```bash
# Remove dangling images
docker image prune -f

# Remove dangling volumes
docker volume prune -f

# Remove everything unused
docker system prune -a

# Remove specific container
docker rm rangbot-web
docker rm rangbot-mysql

# Remove specific image
docker rmi rangbot:latest
```

## 🔐 Environment Variables

```bash
# View current .env
cat .env

# Copy template
cp .env.example .env

# Edit .env
# Windows: notepad .env
# Linux: nano .env
# macOS: open .env
```

## 🚨 Troubleshooting

```bash
# Check if ports are in use
netstat -ano | findstr :8000    # Django
netstat -ano | findstr :3306    # MySQL

# View error details
docker-compose logs --tail 100 web
docker-compose logs --tail 100 db

# Reset database (WARNING: loses all data)
docker-compose down -v
docker-compose up --build

# Verify setup
docker-compose exec web python manage.py check

# Test database connection
docker-compose exec web python manage.py dbshell
```

## 📱 Access Points

```
Django App:        http://localhost:8000
Admin Panel:       http://localhost:8000/admin
API (if exists):   http://localhost:8000/api

MySQL:             localhost:3306
User:              rangbot_user
Password:          rangbot_pass
Database:          rangbot_db

Root MySQL:
User:              root
Password:          root123
```

## 📚 Useful Docker Commands

```bash
# List all containers
docker ps -a

# List all images
docker images

# Get container IP
docker inspect rangbot-web | grep "IPAddress"

# Copy file from container
docker cp rangbot-web:/app/file.txt ./

# Execute command in container
docker-compose exec web ls -la

# Restart specific service
docker-compose restart web

# Pause/Unpause
docker-compose pause
docker-compose unpause
```

## 🎓 Advanced

```bash
# Use production Dockerfile
docker build -f Dockerfile.prod -t rangbot:prod .

# Tag image
docker tag rangbot:latest rangbot:1.0.0

# Push to registry
docker tag rangbot:latest myregistry/rangbot:latest
docker push myregistry/rangbot:latest

# Run in detached mode with custom name
docker-compose up -d --project-name my-project

# Scale services
docker-compose up --scale web=2

# Run specific service only
docker-compose up web

# Run without Docker Compose
docker network create rangbot-network
docker run -d --name rangbot-mysql --network rangbot-network mysql:8.0
docker run -d --name rangbot-web -p 8000:8000 --network rangbot-network rangbot:latest
```

---

**Quick Tip**: Simpan file ini dan bookmark untuk referensi cepat! 🔖
