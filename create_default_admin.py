"""
Script untuk membuat akun admin default
Jalankan dengan: python manage.py shell < create_default_admin.py
atau: python create_default_admin.py
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rangbot_system.settings')
django.setup()

from main.models import Admin
from django.contrib.auth.hashers import make_password

def create_default_admin():
    """
    Membuat akun admin default jika belum ada
    """
    username = 'admin'
    email = 'admin@rangbot.com'
    password = 'admin123'  # Password default - HARUS DIGANTI SETELAH LOGIN PERTAMA!
    full_name = 'Administrator RangBot'
    
    # Cek apakah admin sudah ada
    if Admin.objects.filter(username=username).exists():
        print(f"❌ Admin dengan username '{username}' sudah ada!")
        admin = Admin.objects.get(username=username)
        print(f"   Email: {admin.email}")
        print(f"   Nama: {admin.full_name}")
        print(f"\n📝 Untuk reset password, gunakan Django Admin Panel atau hapus admin ini terlebih dahulu.")
        return False
    
    # Buat admin baru
    try:
        admin = Admin.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            full_name=full_name,
            is_active=True
        )
        print("=" * 60)
        print("✅ AKUN ADMIN BERHASIL DIBUAT!")
        print("=" * 60)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Nama: {full_name}")
        print("=" * 60)
        print("\n⚠️  PENTING: Ganti password setelah login pertama kali!")
        print(f"\n🔗 Login di: http://127.0.0.1:8000/login/")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"❌ Error saat membuat admin: {str(e)}")
        return False

if __name__ == '__main__':
    create_default_admin()

