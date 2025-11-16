"""
Script untuk membuat admin user pertama
Jalankan: python create_admin.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rangbot_system.settings')
django.setup()

from main.models import Admin
from django.contrib.auth.hashers import make_password

def create_admin():
    print("=" * 60)
    print("  RangBot - Create Admin User")
    print("=" * 60)
    print()
    
    # Check if admin already exists
    if Admin.objects.exists():
        print("⚠ Admin sudah ada di database.")
        print("\nDaftar admin:")
        for admin in Admin.objects.all():
            print(f"  - {admin.username} ({admin.full_name})")
        print("\nApakah Anda ingin membuat admin baru? (y/n): ", end="")
        response = input().strip().lower()
        if response != 'y':
            print("\n✓ Dibatalkan.")
            return
    
    # Get admin details
    print("Masukkan detail admin:")
    print()
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username tidak boleh kosong!")
        return
    
    if Admin.objects.filter(username=username).exists():
        print(f"❌ Username '{username}' sudah digunakan!")
        return
    
    full_name = input("Nama Lengkap: ").strip()
    if not full_name:
        print("❌ Nama lengkap tidak boleh kosong!")
        return
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email tidak boleh kosong!")
        return
    
    if Admin.objects.filter(email=email).exists():
        print(f"❌ Email '{email}' sudah digunakan!")
        return
    
    password = input("Password: ").strip()
    if not password:
        print("❌ Password tidak boleh kosong!")
        return
    
    if len(password) < 6:
        print("⚠ Password terlalu pendek (minimal 6 karakter)")
        confirm = input("Lanjutkan? (y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    # Create admin
    try:
        admin = Admin.objects.create(
            username=username,
            full_name=full_name,
            email=email,
            password=make_password(password),
            is_active=True
        )
        
        print()
        print("=" * 60)
        print("  ✓ Admin berhasil dibuat!")
        print("=" * 60)
        print()
        print(f"Username: {admin.username}")
        print(f"Nama: {admin.full_name}")
        print(f"Email: {admin.email}")
        print()
        print("Anda bisa login di: http://127.0.0.1:8000/admin/login/")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    create_admin()

