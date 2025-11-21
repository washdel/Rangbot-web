@echo off
REM Script untuk memeriksa indentasi dan syntax error Python (Windows)
REM Usage: .python-lint-check.bat

echo Memeriksa indentasi dan syntax error pada file Python...

set ERROR_COUNT=0

REM Cari semua file Python (kecuali di venv dan migrations)
for /r %%f in (*.py) do (
    REM Skip venv dan migrations
    echo %%f | findstr /i "venv migrations __pycache__" >nul
    if errorlevel 1 (
        REM Cek syntax error
        python -m py_compile "%%f" 2>nul
        if errorlevel 1 (
            echo [ERROR] %%f memiliki syntax/indentation error!
            set /a ERROR_COUNT+=1
        )
    )
)

if %ERROR_COUNT%==0 (
    echo [OK] Semua file Python tidak memiliki error indentasi!
    exit /b 0
) else (
    echo [ERROR] Ditemukan %ERROR_COUNT% error!
    exit /b 1
)

