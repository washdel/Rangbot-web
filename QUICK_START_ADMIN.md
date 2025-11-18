# Quick Start - Setup Admin Dashboard

## Langkah Cepat Setup Admin

### 1. Pastikan Database Sudah Siap
```bash
cd Rangbot-web
python manage.py migrate
```

### 2. Buat Akun Admin
```bash
python manage.py create_admin
```

Output yang diharapkan:
```
============================================================
✅ AKUN ADMIN BERHASIL DIBUAT!
============================================================
Username: admin
Email: admin@rangbot.com
Password: admin123
Nama: Administrator RangBot
============================================================

⚠️  PENTING: Ganti password setelah login pertama kali!

🔗 Login di: http://127.0.0.1:8000/login/
============================================================
```

### 3. Login ke Dashboard

1. Buka: `http://127.0.0.1:8000/login/`
2. Username: `admin`
3. Password: `admin123`
4. Klik **Login**

### 4. Akses Dashboard Admin

Setelah login, Anda akan diarahkan ke:
`http://127.0.0.1:8000/admin/dashboard/`

## Kredensial Default

```
Username: admin
Password: admin123
```

**⚠️ GANTI PASSWORD SETELAH LOGIN PERTAMA KALI!**

