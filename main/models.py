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


class CustomerService(models.Model):
    """
    Model untuk Customer Service (CS)
    """
    username = models.CharField(max_length=100, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=255, verbose_name='Password')  # Hashed password
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Login terakhir')
    
    class Meta:
        verbose_name = 'Customer Service'
        verbose_name_plural = 'Customer Services'
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
    
    # Payment Information
    PAYMENT_METHOD_CHOICES = [
        ('transfer', 'Transfer Bank'),
        ('credit', 'Kartu Kredit'),
        ('installment', 'Cicilan'),
        ('leasing', 'Leasing'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, verbose_name='Metode Pembayaran')
    
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
    
    def get_order_number(self):
        """Generate nomor order unik dengan format: ORD-YYYYMMDD-HHMMSS-ID"""
        year = self.created_at.strftime('%Y')
        month = self.created_at.strftime('%m')
        day = self.created_at.strftime('%d')
        hour = self.created_at.strftime('%H')
        minute = self.created_at.strftime('%M')
        second = self.created_at.strftime('%S')
        return f"ORD-{year}{month}{day}-{hour}{minute}{second}-{str(self.id).zfill(5)}"


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
    is_active = models.BooleanField(default=True, verbose_name='Aktif', help_text='False jika member dinonaktifkan dan tidak bisa login')
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


class ProductInfo(models.Model):
    """
    Model untuk informasi produk dan landing page
    Dapat dikelola oleh admin
    """
    PACKAGE_CHOICES = [
        ('basic', 'Basic'),
        ('professional', 'Professional'),
    ]
    
    package_type = models.CharField(max_length=20, choices=PACKAGE_CHOICES, unique=True, verbose_name='Tipe Paket')
    name = models.CharField(max_length=200, verbose_name='Nama Paket')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Harga')
    description = models.TextField(blank=True, null=True, verbose_name='Deskripsi')
    features = models.TextField(blank=True, null=True, verbose_name='Fitur', help_text='Satu fitur per baris')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')
    updated_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Diperbarui oleh')
    
    class Meta:
        verbose_name = 'Informasi Produk'
        verbose_name_plural = 'Informasi Produk'
        ordering = ['package_type']
    
    def __str__(self):
        return f"{self.name} - Rp {self.price:,.0f}"
    
    def get_features_list(self):
        """Mengembalikan list fitur"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []


class FAQ(models.Model):
    """
    Model untuk FAQ (Frequently Asked Questions)
    Dapat dikelola oleh admin
    """
    question = models.CharField(max_length=500, verbose_name='Pertanyaan')
    answer = models.TextField(verbose_name='Jawaban')
    order = models.IntegerField(default=0, verbose_name='Urutan', help_text='Urutan tampil (0 = pertama)')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.question[:50] + ('...' if len(self.question) > 50 else '')


class Article(models.Model):
    """
    Model untuk artikel/tips harian tentang stroberi
    Dapat dikelola oleh admin
    """
    title = models.CharField(max_length=200, verbose_name='Judul')
    content = models.TextField(verbose_name='Isi Artikel')
    image_url = models.URLField(blank=True, null=True, verbose_name='URL Gambar')
    is_published = models.BooleanField(default=False, verbose_name='Dipublikasikan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name='Dibuat oleh')
    
    class Meta:
        verbose_name = 'Artikel'
        verbose_name_plural = 'Artikel'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ActivityLog(models.Model):
    """
    Model untuk log aktivitas sistem
    Mencatat semua aktivitas penting yang dilakukan admin
    """
    ACTION_TYPES = [
        ('order_verified', 'Verifikasi Pembelian'),
        ('order_rejected', 'Pembelian Ditolak'),
        ('member_created', 'Member ID Dibuat'),
        ('serial_created', 'Nomor Seri Dibuat'),
        ('member_updated', 'Data Member Diperbarui'),
        ('member_deactivated', 'Member Dinonaktifkan'),
        ('member_activated', 'Member Diaktifkan'),
        ('serial_updated', 'Nomor Seri Diperbarui'),
        ('product_updated', 'Produk Diperbarui'),
        ('admin_created', 'Admin Dibuat'),
        ('admin_deactivated', 'Admin Dinonaktifkan'),
        ('cs_created', 'Customer Service Dibuat'),
        ('cs_deleted', 'Customer Service Dihapus'),
        ('system_error', 'Error Sistem'),
    ]
    
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES, verbose_name='Tipe Aksi')
    description = models.TextField(verbose_name='Deskripsi')
    performed_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs', verbose_name='Dilakukan oleh')
    related_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs', verbose_name='Purchase Order Terkait')
    related_member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs', verbose_name='Member Terkait')
    related_device = models.ForeignKey(RangBotDevice, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs', verbose_name='Device Terkait')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='Metadata', help_text='Data tambahan dalam format JSON')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu')
    
    class Meta:
        verbose_name = 'Log Aktivitas'
        verbose_name_plural = 'Log Aktivitas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['action_type']),
        ]
    
    def __str__(self):
        return f"{self.get_action_type_display()} - {self.created_at.strftime('%d %b %Y %H:%M')}"


class ContactMessage(models.Model):
    """
    Model untuk pesan dari fitur "Hubungi Customer Service" di landing page
    """
    STATUS_CHOICES = [
        ('new', 'Baru'),
        ('read', 'Sudah Dibaca'),
        ('replied', 'Sudah Dibalas'),
        ('archived', 'Diarsipkan'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nama')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Subjek')
    message = models.TextField(verbose_name='Pesan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Status')
    replied_by = models.ForeignKey(CustomerService, on_delete=models.SET_NULL, null=True, blank=True, related_name='replied_messages', verbose_name='Dibalas oleh')
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Dibalas')
    reply_message = models.TextField(blank=True, null=True, verbose_name='Balasan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')
    
    class Meta:
        verbose_name = 'Pesan Customer Service'
        verbose_name_plural = 'Pesan Customer Service'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"
