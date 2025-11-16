"""
Script untuk mengaktifkan MySQL di settings.py
Jalankan: python enable_mysql.py
"""

import os
import re

SETTINGS_FILE = 'rangbot_system/settings.py'

def enable_mysql():
    """Mengaktifkan MySQL di settings.py"""
    
    if not os.path.exists(SETTINGS_FILE):
        print(f"❌ File {SETTINGS_FILE} tidak ditemukan!")
        return False
    
    # Baca file settings.py
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    sqlite_commented = False
    mysql_uncommented = False
    in_mysql_block = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Deteksi bagian SQLite Configuration
        if '# SQLite Configuration' in line:
            new_lines.append('# SQLite Configuration (Commented - Using MySQL)\n')
            i += 1
            # Comment semua baris sampai closing brace
            brace_count = 0
            while i < len(lines):
                current_line = lines[i]
                if '{' in current_line:
                    brace_count += current_line.count('{')
                if '}' in current_line:
                    brace_count -= current_line.count('}')
                
                if 'ENGINE' in current_line and 'sqlite3' in current_line:
                    new_lines.append('# ' + current_line)
                elif 'DATABASES' in current_line and '{' in current_line:
                    new_lines.append('# ' + current_line)
                elif 'NAME' in current_line and 'db.sqlite3' in current_line:
                    new_lines.append('# ' + current_line)
                elif '}' in current_line and brace_count == 0:
                    new_lines.append('# ' + current_line)
                    i += 1
                    break
                else:
                    new_lines.append('# ' + current_line)
                i += 1
            sqlite_commented = True
            continue
        
        # Deteksi bagian MySQL Configuration (dalam triple quotes)
        if '# MySQL Configuration' in line:
            new_lines.append(line)
            i += 1
            # Skip comment lines
            while i < len(lines) and ('# Uncomment' in lines[i] or '# Pastikan' in lines[i] or lines[i].strip() == ''):
                new_lines.append(lines[i])
                i += 1
            
            # Uncomment MySQL block
            if i < len(lines) and '"""' in lines[i]:
                i += 1  # Skip opening """
                # Baca semua baris sampai closing """
                mysql_lines = []
                while i < len(lines):
                    if '"""' in lines[i]:
                        # Found closing """
                        break
                    mysql_lines.append(lines[i])
                    i += 1
                i += 1  # Skip closing """
                
                # Add uncommented MySQL code
                new_lines.extend(mysql_lines)
                mysql_uncommented = True
                continue
        
        new_lines.append(line)
        i += 1
    
    # Tulis kembali ke file
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    if sqlite_commented and mysql_uncommented:
        print("✓ MySQL berhasil diaktifkan di settings.py!")
        print("\nSelanjutnya:")
        print("1. Pastikan MySQL di Laragon sudah running")
        print("2. Buat database: CREATE DATABASE rangbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("3. Jalankan: python manage.py migrate")
        return True
    else:
        print("⚠ Perubahan mungkin tidak lengkap. Silakan edit manual di settings.py")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("  RangBot - Enable MySQL Configuration")
    print("=" * 50)
    print()
    
    if enable_mysql():
        print("\n✓ Setup selesai!")
    else:
        print("\n❌ Setup gagal!")

