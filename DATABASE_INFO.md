# Informasi Database RangBot Web

## Database yang Digunakan

### Saat Ini: SQLite (Default Django)

Proyek RangBot Web saat ini menggunakan **SQLite** sebagai database default Django. SQLite adalah database file-based yang cocok untuk development dan aplikasi kecil hingga menengah.

**Lokasi Database:**
- File: `db.sqlite3` (di root project)
- Path: `D:\Semester 5\RPL\Project\Rangbot_Web\db.sqlite3`

**Konfigurasi di `settings.py`:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Model Database yang Ada

1. **Forum Models:**
   - `ForumUser` - Data pengguna forum (email, nama, peran)
   - `ForumPost` - Postingan di forum
   - `ForumComment` - Komentar pada postingan

2. **Member Models:**
   - `Member` - Data member yang membeli RangBot
   - `RangBotDevice` - Perangkat RangBot yang dimiliki member
   - `DetectionHistory` - Riwayat deteksi penyakit stroberi
   - `Notification` - Notifikasi untuk member

### Migrasi Database

Untuk membuat/mengupdate struktur database:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Migrasi ke MySQL (Opsional)

Jika ingin menggunakan MySQL untuk production, ikuti langkah berikut:

### 1. Install MySQL Client untuk Python

```bash
pip install mysqlclient
# atau
pip install pymysql
```

### 2. Buat Database MySQL

```sql
CREATE DATABASE rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rangbot_user'@'localhost' IDENTIFIED BY 'password_anda';
GRANT ALL PRIVILEGES ON rangbot_db.* TO 'rangbot_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Update `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rangbot_db',
        'USER': 'rangbot_user',
        'PASSWORD': 'password_anda',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 4. Jalankan Migrasi

```bash
python manage.py migrate
```

## Migrasi ke PostgreSQL (Opsional)

Jika ingin menggunakan PostgreSQL:

### 1. Install PostgreSQL Client

```bash
pip install psycopg2-binary
```

### 2. Update `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rangbot_db',
        'USER': 'rangbot_user',
        'PASSWORD': 'password_anda',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Backup Database

### SQLite
```bash
# Copy file database
cp db.sqlite3 db.sqlite3.backup
```

### MySQL
```bash
mysqldump -u rangbot_user -p rangbot_db > backup.sql
```

### PostgreSQL
```bash
pg_dump -U rangbot_user rangbot_db > backup.sql
```

## Catatan Penting

1. **SQLite** cocok untuk development dan testing
2. **MySQL/PostgreSQL** direkomendasikan untuk production dengan traffic tinggi
3. Pastikan backup database dilakukan secara berkala
4. Jangan commit file `db.sqlite3` ke Git (tambahkan ke `.gitignore`)

