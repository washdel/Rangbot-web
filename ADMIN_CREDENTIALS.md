# Kredensial Admin Dashboard RangBot

## Akun Admin Default

Setelah menjalankan migration dan membuat akun admin, gunakan kredensial berikut untuk login:

### Kredensial Default:
```
Username: admin
Password: admin123
Email: admin@rangbot.com
```

### Cara Membuat Akun Admin:

#### Metode 1: Menggunakan Django Management Command
```bash
cd Rangbot-web
python manage.py create_admin
```

Atau dengan custom username/password:
```bash
python manage.py create_admin --username admin --password admin123 --email admin@rangbot.com --name "Administrator RangBot"
```

#### Metode 2: Menggunakan Django Admin Panel
1. Akses Django Admin Panel: `http://127.0.0.1:8000/django-admin/`
2. Login dengan superuser Django (jika ada)
3. Buka menu **Admins** di sidebar
4. Klik **Add Admin**
5. Isi form:
   - Username: `admin`
   - Email: `admin@rangbot.com`
   - Password: `admin123` (akan di-hash otomatis)
   - Full Name: `Administrator RangBot`
   - Is Active: ✓ (centang)
6. Klik **Save**

#### Metode 3: Menggunakan Python Shell
```bash
cd Rangbot-web
python manage.py shell
```

Kemudian jalankan:
```python
from main.models import Admin
from django.contrib.auth.hashers import make_password

admin = Admin.objects.create(
    username='admin',
    email='admin@rangbot.com',
    password=make_password('admin123'),
    full_name='Administrator RangBot',
    is_active=True
)
print(f"Admin created: {admin.username}")
```

### Login ke Dashboard Admin:

1. Buka browser dan akses: `http://127.0.0.1:8000/login/`
2. Masukkan:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Klik **Login**
4. Anda akan diarahkan ke Dashboard Admin: `http://127.0.0.1:8000/admin/dashboard/`

### ⚠️ PENTING - Keamanan:

**GANTI PASSWORD SETELAH LOGIN PERTAMA KALI!**

Untuk mengganti password:
1. Login ke Dashboard Admin
2. Buka Django Admin Panel: `http://127.0.0.1:8000/django-admin/`
3. Buka menu **Admins**
4. Pilih admin yang ingin diubah password
5. Edit password di form
6. Save

### Fitur Dashboard Admin:

Setelah login, Anda dapat mengakses:

- **Dashboard Utama**: Ringkasan statistik sistem
- **Verifikasi Pembelian**: Verifikasi purchase orders dan generate Member ID
- **Manajemen Member**: Lihat, edit, freeze/activate member
- **Manajemen Nomor Seri**: Lihat semua nomor seri RangBot
- **Manajemen Customer Service**: Tambah/hapus akun CS
- **Manajemen Produk**: Edit harga, deskripsi produk
- **Manajemen FAQ**: Tambah/edit/hapus FAQ
- **Manajemen Artikel**: Tambah/edit/hapus artikel/tips

### Troubleshooting:

Jika tidak bisa login:
1. Pastikan database sudah di-migrate: `python manage.py migrate`
2. Pastikan akun admin sudah dibuat (gunakan salah satu metode di atas)
3. Cek apakah password sudah di-hash dengan benar
4. Pastikan `is_active=True` pada akun admin

### Catatan:

- Password disimpan dalam bentuk hash (tidak bisa dilihat langsung)
- Jika lupa password, reset melalui Django Admin Panel atau hapus dan buat ulang admin
- Untuk production, gunakan password yang kuat dan unik

