"""
Script untuk membuat admin user default (username: admin, password: admin)
Jalankan: python create_default_admin.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rangbot_system.settings')
django.setup()

from main.models import Admin
from django.contrib.auth.hashers import make_password

def create_default_admin():
    print("=" * 60)
    print("  RangBot - Create Default Admin User")
    print("=" * 60)
    print()
    
    username = 'admin'
    password = 'admin'
    email = 'admin@rangbot.id'
    full_name = 'Administrator'
    
    # Check if admin already exists
    admin, created = Admin.objects.get_or_create(
        username=username,
        defaults={
            'full_name': full_name,
            'email': email,
            'password': make_password(password),
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Admin user berhasil dibuat!")
        print()
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print(f"Nama: {full_name}")
        print()
        print("Anda bisa login di: http://127.0.0.1:8000/admin/login/")
        print()
    else:
        # Update password if admin exists
        admin.password = make_password(password)
        admin.is_active = True
        admin.save()
        print(f"✓ Admin user sudah ada, password direset!")
        print()
        print(f"Username: {username}")
        print(f"Password: {password}")
        print()
        print("Anda bisa login di: http://127.0.0.1:8000/admin/login/")
        print()

if __name__ == '__main__':
    create_default_admin()

