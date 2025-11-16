@echo off
echo ========================================
echo    RangBot - Automatic Setup Script
echo ========================================
echo.

echo [1/5] Membuat Virtual Environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Gagal membuat virtual environment
    pause
    exit /b 1
)
echo Virtual environment berhasil dibuat!
echo.

echo [2/5] Mengaktifkan Virtual Environment...
call venv\Scripts\activate.bat
echo.

echo [3/5] Upgrade pip...
python -m pip install --upgrade pip
echo.

echo [4/5] Install Dependencies (ini mungkin memakan waktu beberapa menit)...
pip install Django==4.2.7
pip install django-cors-headers
pip install whitenoise
echo Dependencies utama berhasil diinstall!
echo.

echo [5/5] Setup Database...
python manage.py makemigrations
python manage.py migrate
echo Database berhasil di-setup!
echo.

echo ========================================
echo           SETUP SELESAI!
echo ========================================
echo.
echo Untuk menjalankan server:
echo 1. Buka terminal di folder ini
echo 2. Jalankan: run_server.bat
echo.
echo Atau manual:
echo 1. venv\Scripts\activate
echo 2. python manage.py runserver
echo.
pause

