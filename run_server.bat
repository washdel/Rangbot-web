@echo off
echo ========================================
echo      RangBot - Development Server
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

echo Starting Django development server...
echo.
echo Server akan berjalan di: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo.
echo Tekan Ctrl+C untuk stop server
echo ========================================
echo.

REM Run server
python manage.py runserver

pause

