# Setup MySQL untuk RangBot Web

Panduan lengkap untuk mengkonfigurasi MySQL (Laragon) dengan Django RangBot Web.

## Prerequisites

1. **Laragon sudah terinstall dan MySQL running**
   - Pastikan Laragon sudah diinstall
   - Start MySQL dari Laragon (klik "Start All" atau start MySQL saja)

2. **Virtual Environment sudah aktif**
   - Jika belum, jalankan `setup.bat` terlebih dahulu

## Langkah-langkah Setup

### Opsi 1: Menggunakan Script Otomatis (Recommended)

1. **Jalankan script setup:**
   ```bash
   setup_mysql.bat
   ```

2. **Ikuti instruksi di script:**
   - Script akan menginstall `pymysql`
   - Script akan meminta konfigurasi MySQL (database name, username, password, dll)
   - Script akan membuat file `mysql_config.py`

3. **Buat database di MySQL:**
   - Buka **phpMyAdmin** di Laragon (biasanya: http://localhost/phpmyadmin)
   - Atau gunakan **MySQL Command Line**
   - Jalankan perintah:
     ```sql
     CREATE DATABASE IF NOT EXISTS rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     ```
   - Atau gunakan file `setup_mysql.sql` yang sudah disediakan

4. **Aktifkan MySQL di settings.py:**
   - Buka file `rangbot_system/settings.py`
   - **Comment** bagian SQLite (baris 72-77):
     ```python
     # DATABASES = {
     #     'default': {
     #         'ENGINE': 'django.db.backends.sqlite3',
     #         'NAME': BASE_DIR / 'db.sqlite3',
     #     }
     # }
     ```
   - **Uncomment** bagian MySQL (baris 79-106):
     ```python
     try:
         from mysql_config import MYSQL_CONFIG
         DATABASES = {
             'default': MYSQL_CONFIG
         }
         print("✓ Menggunakan MySQL database")
     except ImportError:
         print("⚠ mysql_config.py tidak ditemukan, menggunakan SQLite")
         DATABASES = {
             'default': {
                 'ENGINE': 'django.db.backends.sqlite3',
                 'NAME': BASE_DIR / 'db.sqlite3',
             }
         }
     except Exception as e:
         print(f"⚠ Error loading MySQL config: {e}, menggunakan SQLite")
         DATABASES = {
             'default': {
                 'ENGINE': 'django.db.backends.sqlite3',
                 'NAME': BASE_DIR / 'db.sqlite3',
             }
         }
     ```

5. **Jalankan migrasi:**
   ```bash
   python manage.py migrate
   ```

6. **Buat superuser (opsional):**
   ```bash
   python manage.py createsuperuser
   ```

### Opsi 2: Setup Manual

1. **Install MySQL driver:**
   ```bash
   # Aktifkan virtual environment terlebih dahulu
   venv\Scripts\activate
   
   # Install pymysql (recommended, mudah diinstall)
   pip install pymysql
   
   # ATAU install mysqlclient (lebih cepat, tapi butuh MySQL dev libraries)
   pip install mysqlclient
   ```

2. **Buat file `mysql_config.py` di root project:**
   ```python
   MYSQL_CONFIG = {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'rangbot_db',  # Nama database
       'USER': 'root',  # Username MySQL (default Laragon: root)
       'PASSWORD': '',  # Password MySQL (default Laragon: kosong)
       'HOST': 'localhost',  # Host MySQL
       'PORT': '3306',  # Port MySQL (default: 3306)
       'OPTIONS': {
           'charset': 'utf8mb4',
           'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
       },
   }
   ```

3. **Buat database di MySQL:**
   - Buka phpMyAdmin atau MySQL Command Line
   - Jalankan:
     ```sql
     CREATE DATABASE IF NOT EXISTS rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     ```

4. **Aktifkan MySQL di `settings.py`** (sama seperti Opsi 1, langkah 4)

5. **Jalankan migrasi:**
   ```bash
   python manage.py migrate
   ```

## Konfigurasi Default Laragon

Laragon biasanya menggunakan konfigurasi berikut:
- **Host:** `localhost`
- **Port:** `3306`
- **Username:** `root`
- **Password:** (kosong/default)

Jika Anda mengubah password root di Laragon, sesuaikan di `mysql_config.py`.

## Verifikasi Setup

Setelah setup selesai, jalankan server:
```bash
python manage.py runserver
```

Jika berhasil, Anda akan melihat pesan:
```
✓ Menggunakan MySQL database
```

Jika ada error, periksa:
1. MySQL di Laragon sudah running
2. Database sudah dibuat
3. Kredensial di `mysql_config.py` benar
4. MySQL driver sudah terinstall (`pymysql` atau `mysqlclient`)

## Troubleshooting

### Error: "No module named 'MySQLdb'"
**Solusi:** Install pymysql dan pastikan sudah di-import di `settings.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Error: "Access denied for user"
**Solusi:** Periksa username dan password di `mysql_config.py`

### Error: "Unknown database 'rangbot_db'"
**Solusi:** Buat database terlebih dahulu di MySQL

### Error: "Can't connect to MySQL server"
**Solusi:** 
- Pastikan MySQL di Laragon sudah running
- Periksa host dan port di `mysql_config.py`

## Kembali ke SQLite

Jika ingin kembali menggunakan SQLite:
1. Comment bagian MySQL di `settings.py`
2. Uncomment bagian SQLite
3. Restart server

## Catatan

- File `db.sqlite3` (SQLite) tidak akan terhapus, hanya tidak digunakan
- Data di SQLite dan MySQL terpisah
- Jika ingin migrasi data dari SQLite ke MySQL, gunakan Django's `dumpdata` dan `loaddata`

