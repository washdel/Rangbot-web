FROM python:3.9-slim

WORKDIR /app

# Install system dependencies untuk Pillow & MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh project
COPY . .

# Create necessary directories
RUN mkdir -p static/
RUN mkdir -p media/

# Collect static files (non-blocking)
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || echo "Static files collection skipped"

# Expose port Django
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
