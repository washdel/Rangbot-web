@echo off
echo ========================================
echo     RangBot - Create Admin User
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

echo Membuat superuser untuk admin panel...
echo.
python manage.py createsuperuser

echo.
pause

