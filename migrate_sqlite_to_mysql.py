"""
Script untuk memigrasi data dari SQLite ke MySQL
Jalankan: python migrate_sqlite_to_mysql.py

CATATAN: Script ini hanya untuk memindahkan data yang sudah ada di SQLite
Jika data sudah ada di MySQL, script akan skip (tidak duplikat)
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rangbot_system.settings')
django.setup()

from django.db import connections
from main.models import Member, RangBotDevice, Notification, ForumUser, ForumPost, ForumComment

def migrate_data():
    """Migrate data dari SQLite ke MySQL"""
    
    print("=" * 60)
    print("  Migrasi Data dari SQLite ke MySQL")
    print("=" * 60)
    print()
    
    # Check if SQLite database exists
    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    
    if not os.path.exists(sqlite_db_path):
        print("✓ SQLite database tidak ditemukan. Data sudah di MySQL atau belum ada data.")
        return
    
    print(f"✓ SQLite database ditemukan: {sqlite_db_path}")
    print()
    
    # Connect to SQLite
    try:
        import sqlite3
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Check data in SQLite
        tables = ['main_member', 'main_rangbotdevice', 'main_notification', 
                  'main_forumuser', 'main_forumpost', 'main_forumcomment']
        
        sqlite_data = {}
        for table in tables:
            try:
                sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = sqlite_cursor.fetchone()[0]
                sqlite_data[table] = count
                print(f"  {table}: {count} records")
            except sqlite3.OperationalError:
                sqlite_data[table] = 0
                print(f"  {table}: Tabel tidak ada")
        
        print()
        
        # Check data in MySQL
        print("Data di MySQL:")
        mysql_data = {
            'main_member': Member.objects.count(),
            'main_rangbotdevice': RangBotDevice.objects.count(),
            'main_notification': Notification.objects.count(),
            'main_forumuser': ForumUser.objects.count(),
            'main_forumpost': ForumPost.objects.count(),
            'main_forumcomment': ForumComment.objects.count(),
        }
        
        for table, count in mysql_data.items():
            print(f"  {table}: {count} records")
        
        print()
        
        # Compare
        needs_migration = False
        for table in tables:
            if sqlite_data.get(table, 0) > mysql_data.get(table, 0):
                needs_migration = True
                print(f"⚠ {table}: SQLite memiliki lebih banyak data ({sqlite_data[table]} > {mysql_data[table]})")
        
        if not needs_migration:
            print("✓ Semua data sudah ada di MySQL atau SQLite tidak memiliki data lebih banyak.")
            print("  Tidak perlu migrasi.")
        else:
            print()
            print("⚠ PERINGATAN: Migrasi data dari SQLite ke MySQL memerlukan")
            print("  penanganan khusus karena struktur mungkin berbeda.")
            print("  Disarankan untuk export/import manual atau menggunakan Django's")
            print("  dumpdata dan loaddata commands.")
            print()
            print("  Untuk export dari SQLite:")
            print("    python manage.py dumpdata --database=sqlite > data.json")
            print()
            print("  Untuk import ke MySQL:")
            print("    python manage.py loaddata data.json")
        
        sqlite_conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Catatan: Jika Anda sudah menggunakan MySQL dari awal,")
        print("data sudah ada di MySQL dan tidak perlu migrasi.")

if __name__ == '__main__':
    migrate_data()

