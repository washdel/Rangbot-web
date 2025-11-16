#!/bin/bash
# Entrypoint script untuk Docker container

set -e

echo "🚀 Starting RangBot Docker setup..."

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to be ready..."
while ! mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent 2>/dev/null; do
    echo "MySQL is unavailable - sleeping"
    sleep 1
done
echo "✅ MySQL is up!"

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || true

# Create superuser (optional)
# echo "👤 Creating superuser..."
# python manage.py shell << END
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
#     print("Superuser created!")
# else:
#     print("Superuser already exists!")
# END

echo "🎉 Setup complete!"
echo "Starting Django development server..."

# Run the server
exec python manage.py runserver 0.0.0.0:8000
