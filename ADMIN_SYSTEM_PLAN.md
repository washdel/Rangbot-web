# Rencana Implementasi Sistem Admin

## Alur Sistem (Sudah Dipahami)

### 1. Pembelian Awal (Non-Member)
- Customer mengisi form pembelian
- Data masuk ke PurchaseOrder (status: pending)
- Belum ada Member ID

### 2. Admin Verifikasi
- Admin melihat PurchaseOrder di dashboard
- Admin verifikasi → status menjadi "verified"
- Sistem otomatis generate:
  - Member ID (format: MBR-2025-00492)
  - Serial Numbers (format: RBT-SN-01-88401, sebanyak jumlah unit)

### 3. Admin Kirim Info
- Admin kirim Member ID + link registrasi ke customer

### 4. Customer Registrasi
- Register dengan Member ID
- Validasi: Member ID valid dan belum digunakan

### 5. Dashboard Member
- Customer login → lihat semua serial numbers

### 6. Pembelian Ulang
- Member beli lagi → PurchaseOrder baru
- Admin verifikasi → generate serial numbers tambahan
- Serial numbers dihubungkan ke Member ID yang sama

## Database Models yang Dibutuhkan

### 1. PurchaseOrder (BARU)
```python
- customer_name
- customer_email
- customer_phone
- customer_address
- package_type (basic/professional)
- qty_basic
- qty_professional
- total_price
- notes
- status (pending/verified/rejected)
- member_id (nullable, diisi setelah verifikasi)
- is_reorder (boolean, untuk pembelian ulang)
- original_member_id (nullable, untuk reorder)
- created_at
- verified_at
- verified_by (Admin)
```

### 2. Admin (BARU)
```python
- username
- email
- password (hashed)
- full_name
- is_active
- created_at
- last_login
```

### 3. Member (UPDATE)
```python
- member_id (unique)
- username
- full_name
- email
- phone
- password
- is_registered (boolean, true jika sudah registrasi)
- purchase_order (ForeignKey ke PurchaseOrder, nullable)
- created_at
- last_login
```

### 4. RangBotDevice (UPDATE)
```python
- serial_number (unique)
- member (ForeignKey)
- purchase_order (ForeignKey ke PurchaseOrder, untuk tracking)
- device_name
- covered_blocks
- status
- is_active
- last_data_update
- created_at
```

## Functions yang Dibutuhkan

### 1. Generate Member ID
```python
def generate_member_id():
    # Format: MBR-YYYY-NNNNN
    # Contoh: MBR-2025-00492
    year = timezone.now().year
    last_order = PurchaseOrder.objects.filter(
        member_id__isnull=False
    ).order_by('-id').first()
    
    if last_order and last_order.member_id:
        # Extract number from last Member ID
        last_num = int(last_order.member_id.split('-')[-1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f"MBR-{year}-{str(new_num).zfill(5)}"
```

### 2. Generate Serial Number
```python
def generate_serial_number(sequence):
    # Format: RBT-SN-01-XXXXX
    # Contoh: RBT-SN-01-88401
    # sequence: nomor urut (1, 2, 3, ...)
    base_num = 88400  # Starting number
    serial_num = base_num + sequence
    return f"RBT-SN-01-{serial_num}"
```

## Views yang Dibutuhkan

### Admin Views
1. `admin_login` - Login admin
2. `admin_dashboard` - Dashboard admin
3. `admin_logout` - Logout admin
4. `purchase_orders_list` - Daftar purchase orders
5. `purchase_order_detail` - Detail purchase order
6. `verify_purchase` - Verifikasi pembelian (generate Member ID & Serial Numbers)
7. `reject_purchase` - Tolak pembelian

### Purchase View (UPDATE)
- `purchase` - Form pembelian (update untuk save ke database)

## Templates yang Dibutuhkan

1. `admin/login.html` - Login admin
2. `admin/dashboard.html` - Dashboard admin
3. `admin/purchase_orders.html` - List purchase orders
4. `admin/purchase_order_detail.html` - Detail purchase order

## URL Patterns

```python
# Admin URLs
path('admin/login/', admin_login, name='admin_login'),
path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
path('admin/logout/', admin_logout, name='admin_logout'),
path('admin/purchase-orders/', purchase_orders_list, name='purchase_orders_list'),
path('admin/purchase-orders/<int:order_id>/', purchase_order_detail, name='purchase_order_detail'),
path('admin/purchase-orders/<int:order_id>/verify/', verify_purchase, name='verify_purchase'),
path('admin/purchase-orders/<int:order_id>/reject/', reject_purchase, name='reject_purchase'),
```

## Urutan Implementasi

1. ✅ Buat models (PurchaseOrder, Admin)
2. ✅ Update models (Member, RangBotDevice)
3. ✅ Buat migrations
4. ✅ Buat helper functions (generate Member ID, Serial Number)
5. ✅ Update purchase view untuk save ke database
6. ✅ Buat admin views
7. ✅ Buat admin templates
8. ✅ Buat admin URLs
9. ✅ Testing

## Catatan Penting

- Database menggunakan MySQL
- Member ID harus unique
- Serial Number harus unique
- Setelah verifikasi, Member ID dan Serial Numbers langsung dibuat
- Member ID bisa digunakan untuk registrasi (satu kali)
- Pembelian ulang tidak membuat Member ID baru, hanya Serial Numbers tambahan

