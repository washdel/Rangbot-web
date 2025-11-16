"""
Script untuk membuat database MySQL melalui Python
Jalankan: python create_mysql_database.py
"""

import pymysql
from mysql_config import MYSQL_CONFIG

def create_database():
    """Membuat database MySQL jika belum ada"""
    
    try:
        # Koneksi ke MySQL tanpa database (untuk membuat database)
        connection = pymysql.connect(
            host=MYSQL_CONFIG['HOST'],
            port=int(MYSQL_CONFIG['PORT']),
            user=MYSQL_CONFIG['USER'],
            password=MYSQL_CONFIG['PASSWORD'],
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Buat database
            db_name = MYSQL_CONFIG['NAME']
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{db_name}' berhasil dibuat atau sudah ada")
            
            # Tampilkan daftar database
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\nDaftar database:")
            for db in databases:
                if db[0] == db_name:
                    print(f"  ✓ {db[0]} (database yang digunakan)")
                else:
                    print(f"    {db[0]}")
        
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error: {e}")
        print("\nPastikan:")
        print("1. MySQL di Laragon sudah running")
        print("2. Kredensial di mysql_config.py benar")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("  RangBot - Create MySQL Database")
    print("=" * 50)
    print()
    
    if create_database():
        print("\n✓ Database siap digunakan!")
        print("\nSelanjutnya jalankan:")
        print("  python manage.py migrate")
    else:
        print("\n❌ Gagal membuat database!")

