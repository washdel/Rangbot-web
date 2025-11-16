from django.db import models
from django.utils import timezone


class ForumUser(models.Model):
    """
    Model untuk pengguna forum (login sederhana dengan email)
    """
    ROLE_CHOICES = [
        ('petani', 'Petani'),
        ('mahasiswa', 'Mahasiswa'),
        ('peneliti', 'Peneliti'),
        ('siswa', 'Siswa'),
        ('lainnya', 'Lainnya'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, verbose_name='Nama')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='petani', verbose_name='Peran')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Login terakhir')
    
    class Meta:
        verbose_name = 'Pengguna Forum'
        verbose_name_plural = 'Pengguna Forum'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class ForumPost(models.Model):
    """
    Model untuk postingan forum
    """
    CATEGORY_CHOICES = [
        ('penyakit', 'Penyakit Stroberi'),
        ('perawatan', 'Tips Perawatan'),
        ('pengalaman', 'Pengalaman Lapangan'),
        ('teknis', 'Pertanyaan Teknis'),
        ('umum', 'Diskusi Umum'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Judul')
    content = models.TextField(verbose_name='Isi Postingan')
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name='posts', verbose_name='Penulis')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='umum', verbose_name='Kategori')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')
    views = models.IntegerField(default=0, verbose_name='Jumlah Dilihat')
    
    class Meta:
        verbose_name = 'Postingan Forum'
        verbose_name_plural = 'Postingan Forum'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_excerpt(self, length=150):
        """Mengambil excerpt dari content"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'
    
    def get_comment_count(self):
        """Menghitung jumlah komentar"""
        return self.comments.count()


class ForumComment(models.Model):
    """
    Model untuk komentar pada postingan forum
    """
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments', verbose_name='Postingan')
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name='comments', verbose_name='Penulis')
    content = models.TextField(verbose_name='Isi Komentar')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')
    
    class Meta:
        verbose_name = 'Komentar Forum'
        verbose_name_plural = 'Komentar Forum'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Komentar oleh {self.author.name} pada {self.post.title}"


class Admin(models.Model):
    """
    Model untuk admin sistem
    """
    username = models.CharField(max_length=100, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=255, verbose_name='Password')  # Hashed password
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Login terakhir')
    
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.username})"


class PurchaseOrder(models.Model):
    """
    Model untuk order pembelian RangBot
    """
    STATUS_CHOICES = [
        ('pending', 'Menunggu Verifikasi'),
        ('verified', 'Terverifikasi'),
        ('rejected', 'Ditolak'),
    ]
    
    PACKAGE_CHOICES = [
        ('basic', 'Basic'),
        ('professional', 'Professional'),
    ]
    
    # Customer Information
    customer_name = models.CharField(max_length=200, verbose_name='Nama Customer')
    customer_email = models.EmailField(verbose_name='Email Customer')
    customer_phone = models.CharField(max_length=20, verbose_name='Nomor Telepon')
    customer_address = models.TextField(verbose_name='Alamat Instalasi')
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nama Greenhouse/Perusahaan')
    
    # Order Details
    qty_basic = models.IntegerField(default=0, verbose_name='Jumlah Paket Basic')
    qty_professional = models.IntegerField(default=0, verbose_name='Jumlah Paket Professional')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total Harga')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    member_id = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='Member ID', help_text='Diisi otomatis setelah verifikasi')
    is_reorder = models.BooleanField(default=False, verbose_name='Pembelian Ulang')
    original_member_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='Member ID Asal', help_text='Untuk pembelian ulang')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name='Diverifikasi pada')
    verified_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_orders', verbose_name='Diverifikasi oleh')
    
    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.status})"
    
    def get_total_units(self):
        """Menghitung total unit yang dibeli"""
        return self.qty_basic + self.qty_professional
    
    def is_verified(self):
        """Cek apakah order sudah terverifikasi"""
        return self.status == 'verified'


class Member(models.Model):
    """
    Model untuk member yang sudah membeli RangBot
    Member ID dibuat otomatis saat admin verifikasi purchase order
    """
    member_id = models.CharField(max_length=20, unique=True, verbose_name='ID Member')
    username = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Username')
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nomor Telepon')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='Password')  # Hashed password, nullable karena belum registrasi
    is_registered = models.BooleanField(default=False, verbose_name='Sudah Registrasi', help_text='True jika sudah melakukan registrasi dengan Member ID')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='members', verbose_name='Purchase Order')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Login terakhir')
    
    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.member_id})"
    
    def get_device_count(self):
        """Menghitung jumlah perangkat RangBot yang dimiliki"""
        return self.rangbot_devices.count()


class RangBotDevice(models.Model):
    """
    Model untuk perangkat RangBot yang dimiliki member
    1 robot bisa mencakup beberapa blok menggunakan rail/trail
    Serial number dibuat otomatis saat admin verifikasi purchase order
    """
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('offline', 'Offline'),
    ]
    
    serial_number = models.CharField(max_length=50, unique=True, verbose_name='Nomor Seri')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='rangbot_devices', verbose_name='Member')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='devices', verbose_name='Purchase Order', help_text='Order yang menghasilkan device ini')
    device_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Perangkat', help_text='Contoh: RangBot 1, RangBot 2')
    covered_blocks = models.CharField(max_length=200, blank=True, null=True, verbose_name='Blok yang Dicakup', help_text='Contoh: A, B atau C, D')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline', verbose_name='Status')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    last_data_update = models.DateTimeField(null=True, blank=True, verbose_name='Update Data Terakhir')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ditambahkan pada')
    
    class Meta:
        verbose_name = 'Perangkat RangBot'
        verbose_name_plural = 'Perangkat RangBot'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.device_name or self.serial_number} ({self.member.member_id})"
    
    def get_display_name(self):
        """Mengembalikan nama display untuk perangkat"""
        if self.device_name:
            return self.device_name
        # Jika tidak ada device_name, gunakan format "RangBot [nomor urut]"
        device_count = self.member.rangbot_devices.filter(created_at__lte=self.created_at).count()
        return f"RangBot {device_count}"
    
    def get_blocks_display(self):
        """Mengembalikan informasi blok yang dicakup"""
        if self.covered_blocks:
            blocks = [b.strip() for b in self.covered_blocks.split(',')]
            return f"Mencakup Blok {', '.join(blocks)}"
        return "Blok belum ditentukan"


class DetectionHistory(models.Model):
    """
    Model untuk riwayat deteksi penyakit stroberi
    """
    device = models.ForeignKey(RangBotDevice, on_delete=models.CASCADE, related_name='detections', verbose_name='Perangkat')
    image_url = models.URLField(verbose_name='URL Gambar')
    disease_detected = models.CharField(max_length=200, blank=True, null=True, verbose_name='Penyakit Terdeteksi')
    confidence = models.FloatField(null=True, blank=True, verbose_name='Tingkat Keyakinan')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='Lokasi')
    detection_type = models.CharField(max_length=20, choices=[('auto', 'Otomatis'), ('manual', 'Manual')], default='auto', verbose_name='Tipe Deteksi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Deteksi')
    
    class Meta:
        verbose_name = 'Riwayat Deteksi'
        verbose_name_plural = 'Riwayat Deteksi'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Deteksi {self.detection_type} - {self.device.serial_number} ({self.created_at})"


class Notification(models.Model):
    """
    Model untuk notifikasi member
    """
    NOTIFICATION_TYPES = [
        ('sensor_update', 'Update Sensor'),
        ('detection_new', 'Deteksi Baru'),
        ('sensor_warning', 'Peringatan Sensor'),
        ('device_offline', 'Perangkat Offline'),
        ('device_added', 'Perangkat Ditambahkan'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='notifications', verbose_name='Member')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='Tipe Notifikasi')
    title = models.CharField(max_length=200, verbose_name='Judul')
    message = models.TextField(verbose_name='Pesan')
    is_read = models.BooleanField(default=False, verbose_name='Sudah Dibaca')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    
    class Meta:
        verbose_name = 'Notifikasi'
        verbose_name_plural = 'Notifikasi'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.member.member_id}"
