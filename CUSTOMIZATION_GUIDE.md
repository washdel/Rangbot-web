# 🎨 Panduan Kustomisasi RangBot

Dokumen ini menjelaskan cara mengkustomisasi landing page RangBot sesuai kebutuhan Anda.

## 📑 Daftar Isi

- [Mengubah Warna Tema](#mengubah-warna-tema)
- [Menambah/Mengurangi Konten](#menambahmengurangi-konten)
- [Mengubah Gambar](#mengubah-gambar)
- [Menambah Section Baru](#menambah-section-baru)
- [Mengubah Font](#mengubah-font)
- [Modifikasi Navbar](#modifikasi-navbar)
- [Kustomisasi Footer](#kustomisasi-footer)
- [Mengubah Animasi](#mengubah-animasi)

---

## 🎨 Mengubah Warna Tema

### Warna Utama (Primary)

Edit file `templates/base.html`, cari bagian `tailwind.config`:

```html
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    primary: {
                        50: '#f0fdf4',   // Hijau sangat terang
                        100: '#dcfce7',  // Hijau terang
                        200: '#bbf7d0',
                        300: '#86efac',
                        400: '#4ade80',
                        500: '#22c55e',  // ← UBAH INI untuk warna utama
                        600: '#16a34a',  // ← UBAH INI untuk warna hover
                        700: '#15803d',
                        800: '#166534',
                        900: '#14532d',
                    }
                }
            }
        }
    }
</script>
```

### Contoh Warna Alternatif

**Tema Biru:**
```javascript
primary: {
    500: '#3b82f6',  // Blue
    600: '#2563eb',
}
```

**Tema Ungu:**
```javascript
primary: {
    500: '#a855f7',  // Purple
    600: '#9333ea',
}
```

**Tema Merah:**
```javascript
primary: {
    500: '#ef4444',  // Red
    600: '#dc2626',
}
```

### Gradient Background

Edit di `templates/landing.html`, cari class `gradient-bg`:

```css
/* Di base.html, section <style> */
.gradient-bg {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    /* Ubah #22c55e dan #16a34a dengan warna pilihan Anda */
}
```

---

## 📝 Menambah/Mengurangi Konten

### Menambah Fitur di Section "Fitur Utama"

Edit file `main/views.py`, tambahkan item di array `features`:

```python
'features': [
    # ... fitur yang sudah ada ...
    {
        'icon': '🎯',  # Emoji atau gunakan <i> untuk Font Awesome
        'title': 'Fitur Baru Saya',
        'description': 'Deskripsi fitur baru yang amazing.'
    },
]
```

### Menambah Paket Pricing

Edit file `main/views.py`, tambahkan di array `pricing_plans`:

```python
'pricing_plans': [
    # ... paket yang sudah ada ...
    {
        'name': 'Enterprise',
        'price': 'Rp 15.000.000',
        'period': '/bulan',
        'features': [
            'Semua fitur Premium',
            'Unlimited robots',
            'White label solution',
            'Custom development',
            'Dedicated team'
        ],
        'highlight': False
    },
]
```

### Menambah FAQ

Edit file `main/views.py`, tambahkan di array `faqs`:

```python
'faqs': [
    # ... FAQ yang sudah ada ...
    {
        'question': 'Pertanyaan baru saya?',
        'answer': 'Jawaban lengkap untuk pertanyaan baru...'
    },
]
```

### Mengurangi Section

Untuk menghilangkan section yang tidak diperlukan, hapus atau comment block HTML di `templates/landing.html`:

```html
<!-- COMMENT THIS SECTION TO HIDE
<section id="forum" class="py-20 bg-gray-50">
    ...
</section>
-->
```

---

## 🖼️ Mengubah Gambar

### Menambahkan Logo Custom

1. Simpan logo di `static/img/logo.png`
2. Edit `templates/base.html`, ganti icon robot dengan image:

```html
<!-- BEFORE -->
<div class="w-10 h-10 md:w-12 md:h-12 bg-gradient-to-br from-green-500 to-green-700 rounded-lg flex items-center justify-center">
    <i class="fas fa-robot text-white text-xl md:text-2xl"></i>
</div>

<!-- AFTER -->
{% load static %}
<img src="{% static 'img/logo.png' %}" alt="RangBot Logo" class="w-10 h-10 md:w-12 md:h-12">
```

### Mengganti Ilustrasi Robot di Hero

Edit `templates/landing.html`, bagian Hero Section:

```html
<!-- BEFORE (placeholder dengan icon) -->
<div class="aspect-square bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center">
    <i class="fas fa-robot text-white text-9xl opacity-80"></i>
</div>

<!-- AFTER (dengan gambar real) -->
{% load static %}
<img src="{% static 'img/robot-illustration.png' %}" alt="RangBot Robot" class="w-full h-full object-contain">
```

### Menambah Background Image

```html
<section class="py-20 bg-cover bg-center" style="background-image: url('{% static "img/strawberry-farm.jpg" %}');">
    <div class="bg-black bg-opacity-50 py-20">
        <!-- Konten section -->
    </div>
</section>
```

---

## ➕ Menambah Section Baru

### Template Section Baru

Edit `templates/landing.html`, tambahkan section baru:

```html
<!-- Section Testimoni (contoh) -->
<section id="testimoni" class="py-20 bg-white">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Testimoni Pengguna
            </h2>
            <p class="text-lg text-gray-600 max-w-3xl mx-auto">
                Apa kata mereka yang sudah menggunakan RangBot
            </p>
        </div>
        
        <!-- Content -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Testimoni Card 1 -->
            <div class="bg-gray-50 rounded-xl p-6">
                <div class="flex items-center space-x-3 mb-4">
                    <img src="..." alt="User" class="w-12 h-12 rounded-full">
                    <div>
                        <h4 class="font-semibold">Nama User</h4>
                        <p class="text-sm text-gray-600">Pemilik Kebun</p>
                    </div>
                </div>
                <p class="text-gray-700">
                    "Testimoni lengkap dari pengguna tentang pengalaman mereka..."
                </p>
            </div>
            
            <!-- Testimoni Card 2 & 3 ... -->
        </div>
    </div>
</section>
```

### Menambahkan Link di Navbar

Edit `templates/base.html`, bagian Desktop Menu:

```html
<div class="hidden md:flex items-center space-x-8">
    <a href="#tentang" class="text-gray-600 hover:text-green-600 transition">Tentang</a>
    <a href="#fitur" class="text-gray-600 hover:text-green-600 transition">Fitur</a>
    <!-- TAMBAHKAN DI SINI -->
    <a href="#testimoni" class="text-gray-600 hover:text-green-600 transition">Testimoni</a>
    <a href="#harga" class="text-gray-600 hover:text-green-600 transition">Harga</a>
    <!-- ... -->
</div>
```

Jangan lupa tambahkan juga di mobile menu!

---

## 🔤 Mengubah Font

### Mengganti Font dari Google Fonts

Edit `templates/base.html`, ganti link Google Fonts:

```html
<!-- BEFORE -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<!-- AFTER (contoh: Poppins) -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

Update CSS:

```css
<style>
    * {
        font-family: 'Poppins', sans-serif;  /* Ubah dari Inter ke Poppins */
    }
</style>
```

### Font Populer untuk Web:

- **Inter** - Modern, clean (current)
- **Poppins** - Friendly, rounded
- **Roboto** - Professional, neutral
- **Montserrat** - Bold, impactful
- **Open Sans** - Readable, versatile

---

## 🧭 Modifikasi Navbar

### Mengubah Warna Navbar

Edit `templates/base.html`:

```html
<!-- BEFORE (navbar putih) -->
<nav id="navbar" class="fixed w-full top-0 z-50 bg-white transition-all duration-300">

<!-- AFTER (navbar dengan gradient) -->
<nav id="navbar" class="fixed w-full top-0 z-50 gradient-bg transition-all duration-300">
```

### Navbar Transparan yang Berubah Saat Scroll

Tambahkan JavaScript di `base.html`:

```javascript
<script>
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.remove('bg-transparent');
            navbar.classList.add('bg-white', 'navbar-scrolled');
        } else {
            navbar.classList.add('bg-transparent');
            navbar.classList.remove('bg-white', 'navbar-scrolled');
        }
    });
</script>
```

---

## 🦶 Kustomisasi Footer

### Menambah Kolom di Footer

Edit `templates/base.html`, bagian footer:

```html
<div class="grid grid-cols-1 md:grid-cols-5 gap-8 mb-8">
    <!-- ... kolom yang sudah ada ... -->
    
    <!-- Kolom Baru: Social Media -->
    <div>
        <h3 class="text-white font-semibold mb-4">Follow Us</h3>
        <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 hover:text-green-500 transition">Facebook</a></li>
            <li><a href="#" class="text-gray-400 hover:text-green-500 transition">Instagram</a></li>
            <li><a href="#" class="text-gray-400 hover:text-green-500 transition">Twitter</a></li>
            <li><a href="#" class="text-gray-400 hover:text-green-500 transition">YouTube</a></li>
        </ul>
    </div>
</div>
```

### Mengubah Warna Footer

```html
<!-- BEFORE (footer gelap) -->
<footer class="bg-gray-900 text-gray-300 py-12">

<!-- AFTER (footer hijau) -->
<footer class="gradient-bg text-white py-12">
```

---

## ✨ Mengubah Animasi

### Mempercepat/Memperlambat Animasi

Edit `static/css/custom.css`:

```css
/* BEFORE */
.card-hover {
    transition: all 0.3s ease;
}

/* AFTER (lebih cepat) */
.card-hover {
    transition: all 0.15s ease;
}

/* AFTER (lebih lambat) */
.card-hover {
    transition: all 0.6s ease;
}
```

### Menambah Hover Effect Custom

```css
/* Di static/css/custom.css */
.custom-hover {
    transition: all 0.3s ease;
}

.custom-hover:hover {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}
```

Gunakan di HTML:

```html
<div class="custom-hover">
    <!-- Konten -->
</div>
```

### Menambah Fade-in Animation saat Scroll

Tambahkan library AOS (Animate On Scroll):

```html
<!-- Di base.html, sebelum </head> -->
<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">

<!-- Sebelum </body> -->
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script>
    AOS.init({
        duration: 800,
        once: true,
    });
</script>
```

Gunakan di HTML:

```html
<div data-aos="fade-up" data-aos-delay="100">
    <!-- Konten akan fade-up saat scroll -->
</div>
```

---

## 🎯 Tips Kustomisasi

1. **Backup Before Edit**: Selalu backup file sebelum mengubah
2. **Test Responsive**: Selalu test di berbagai ukuran layar
3. **Browser DevTools**: Gunakan untuk experiment warna/spacing
4. **Consistent Design**: Pertahankan konsistensi visual
5. **Performance**: Jangan terlalu banyak animasi berat
6. **Accessibility**: Pastikan kontras warna memadai

## 🔧 Tools yang Berguna

- **Color Picker**: [Coolors.co](https://coolors.co/)
- **Gradient Generator**: [CSS Gradient](https://cssgradient.io/)
- **Icon Library**: [Font Awesome](https://fontawesome.com/icons)
- **Google Fonts**: [fonts.google.com](https://fonts.google.com/)
- **Tailwind Playground**: [play.tailwindcss.com](https://play.tailwindcss.com/)

---

## 📚 Referensi

- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Django Templates Guide](https://docs.djangoproject.com/en/4.2/topics/templates/)
- [CSS Tricks](https://css-tricks.com/)

---

**Selamat Mengkustomisasi! 🎨**

