# Quick Setup MySQL untuk RangBot Web

## Langkah Cepat (3 Langkah)

### 1. Install MySQL Driver
```bash
# Aktifkan virtual environment
venv\Scripts\activate

# Install pymysql
pip install pymysql
```

### 2. Buat Database di MySQL
Buka **phpMyAdmin** di Laragon (http://localhost/phpmyadmin) atau MySQL Command Line, lalu jalankan:

```sql
CREATE DATABASE IF NOT EXISTS rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Atau gunakan file `setup_mysql.sql` yang sudah disediakan.

### 3. Konfigurasi dan Aktifkan MySQL

**Opsi A: Menggunakan Script Otomatis (Recommended)**
```bash
# Edit mysql_config.py sesuai kredensial MySQL Anda
# Default Laragon: USER='root', PASSWORD='', HOST='localhost', PORT='3306'

# Aktifkan MySQL di settings.py
python enable_mysql.py
```

**Opsi B: Manual Edit**
1. Buka `rangbot_system/settings.py`
2. **Comment** bagian SQLite (baris 79-84)
3. **Uncomment** bagian MySQL (hapus `"""` di baris 90 dan 115)

### 4. Jalankan Migrasi
```bash
python manage.py migrate
```

## Konfigurasi Default Laragon

File `mysql_config.py` sudah dikonfigurasi untuk Laragon default:
- **Database:** `rangbot_db`
- **User:** `root`
- **Password:** (kosong)
- **Host:** `localhost`
- **Port:** `3306`

Jika Anda mengubah password root, edit file `mysql_config.py`.

## Verifikasi

Jalankan server:
```bash
python manage.py runserver
```

Jika berhasil, Anda akan melihat:
```
✓ Menggunakan MySQL database
```

## Troubleshooting

**Error: "No module named 'MySQLdb'"**
→ Install pymysql: `pip install pymysql`

**Error: "Access denied"**
→ Periksa username/password di `mysql_config.py`

**Error: "Unknown database"**
→ Buat database terlebih dahulu (langkah 2)

**Error: "Can't connect to MySQL server"**
→ Pastikan MySQL di Laragon sudah running

## File-file yang Dibuat

- `mysql_config.py` - Konfigurasi MySQL
- `setup_mysql.sql` - Script SQL untuk membuat database
- `enable_mysql.py` - Script untuk mengaktifkan MySQL
- `MYSQL_SETUP.md` - Dokumentasi lengkap

