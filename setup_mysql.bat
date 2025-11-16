@echo off
echo ========================================
echo    RangBot - MySQL Setup Script
echo ========================================
echo.

echo [1/4] Mengaktifkan Virtual Environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo.

echo [2/4] Install MySQL Driver...
echo Menginstall pymysql (pure Python, mudah diinstall)...
pip install pymysql
if %errorlevel% neq 0 (
    echo ERROR: Gagal menginstall pymysql
    pause
    exit /b 1
)
echo MySQL driver berhasil diinstall!
echo.

echo [3/4] Konfigurasi MySQL...
echo.
echo ========================================
echo   KONFIGURASI MYSQL LARAGON
echo ========================================
echo.
echo Pastikan MySQL di Laragon sudah running!
echo.
set /p DB_NAME="Nama Database (default: rangbot_db): "
if "%DB_NAME%"=="" set DB_NAME=rangbot_db
set /p DB_USER="Username MySQL (default: root): "
if "%DB_USER%"=="" set DB_USER=root
set /p DB_PASS="Password MySQL (default: kosong, tekan Enter): "
set /p DB_HOST="Host MySQL (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost
set /p DB_PORT="Port MySQL (default: 3306): "
if "%DB_PORT%"=="" set DB_PORT=3306
echo.

echo Membuat file konfigurasi MySQL...
(
echo # Konfigurasi MySQL untuk RangBot Web
echo # Dibuat otomatis oleh setup_mysql.bat
echo.
echo MYSQL_CONFIG = {
echo     'ENGINE': 'django.db.backends.mysql',
echo     'NAME': '%DB_NAME%',
echo     'USER': '%DB_USER%',
echo     'PASSWORD': '%DB_PASS%',
echo     'HOST': '%DB_HOST%',
echo     'PORT': '%DB_PORT%',
echo     'OPTIONS': {
echo         'charset': 'utf8mb4',
echo         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
echo     },
echo }
) > mysql_config.py
echo File mysql_config.py berhasil dibuat!
echo.

echo [4/4] Membuat Database MySQL...
echo.
echo ========================================
echo   BUAT DATABASE DI MYSQL
echo ========================================
echo.
echo Buka phpMyAdmin di Laragon atau MySQL Command Line
echo Jalankan perintah berikut:
echo.
echo CREATE DATABASE IF NOT EXISTS %DB_NAME% CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo.
echo Atau gunakan file setup_mysql.sql yang sudah disediakan
echo.
pause

echo.
echo ========================================
echo   AKTIFKAN MYSQL DI SETTINGS.PY
echo ========================================
echo.
echo Sekarang buka file: rangbot_system\settings.py
echo.
echo 1. Comment bagian SQLite (baris 72-77)
echo 2. Uncomment bagian MySQL (baris 79-106)
echo.
echo Setelah itu jalankan:
echo   python manage.py migrate
echo.
echo ========================================
echo           SETUP SELESAI!
echo ========================================
echo.
pause

