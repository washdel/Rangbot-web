"""
Django management command untuk membuat akun admin default
Jalankan dengan: python manage.py create_admin
"""

from django.core.management.base import BaseCommand
from main.models import Admin
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Membuat akun admin default'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username untuk admin (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@rangbot.com',
            help='Email untuk admin (default: admin@rangbot.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password untuk admin (default: admin123)',
        )
        parser.add_argument(
            '--name',
            type=str,
            default='Administrator RangBot',
            help='Nama lengkap admin (default: Administrator RangBot)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        full_name = options['name']
        
        # Cek apakah admin sudah ada
        if Admin.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️  Admin dengan username '{username}' sudah ada!")
            )
            admin = Admin.objects.get(username=username)
            self.stdout.write(f"   Email: {admin.email}")
            self.stdout.write(f"   Nama: {admin.full_name}")
            self.stdout.write(
                self.style.WARNING("\n📝 Untuk reset password, gunakan Django Admin Panel atau hapus admin ini terlebih dahulu.")
            )
            return
        
        # Buat admin baru
        try:
            admin = Admin.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                full_name=full_name,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(self.style.SUCCESS("✅ AKUN ADMIN BERHASIL DIBUAT!"))
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(f"Username: {username}")
            self.stdout.write(f"Email: {email}")
            self.stdout.write(f"Password: {password}")
            self.stdout.write(f"Nama: {full_name}")
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(
                self.style.WARNING("\n⚠️  PENTING: Ganti password setelah login pertama kali!")
            )
            self.stdout.write(f"\n🔗 Login di: http://127.0.0.1:8000/login/")
            self.stdout.write(self.style.SUCCESS("=" * 60))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error saat membuat admin: {str(e)}")
            )

