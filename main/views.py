from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from datetime import datetime
from django.db import models
from .models import ForumUser, ForumPost, ForumComment, Admin, PurchaseOrder, Member, RangBotDevice, DetectionHistory, Notification
from .forms import ForumLoginForm, ForumPostForm, ForumCommentForm
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Helper function untuk check admin
def is_staff_user(user):
    return user.is_staff or user.is_superuser


def member_login(request):
    """Login tunggal: Admin atau Member, diarahkan sesuai peran."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Mohon lengkapi username dan password.')
            return render(request, 'login.html', { 'page_title': 'Login - RangBot' })

        # 1) Coba sebagai Admin
        try:
            admin = Admin.objects.get(username=username, is_active=True)
            if admin.password and check_password(password, admin.password):
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                request.session['admin_name'] = admin.full_name
                admin.last_login = timezone.now()
                admin.save(update_fields=['last_login'])
                messages.success(request, f'Selamat datang, {admin.full_name}!')
                return redirect('main:admin_dashboard')
        except Admin.DoesNotExist:
            pass

        # 2) Coba sebagai Member terdaftar
        try:
            member = Member.objects.get(username=username, is_registered=True)
            if member.password and check_password(password, member.password):
                request.session['member_id'] = member.member_id
                request.session['member_username'] = member.username
                request.session['member_name'] = member.full_name
                member.last_login = timezone.now()
                member.save(update_fields=['last_login'])
                messages.success(request, f'Selamat datang, {member.full_name}!')
                return redirect('main:member_dashboard')
        except Member.DoesNotExist:
            pass

        # Jika gagal keduanya
        messages.error(request, 'Username atau password salah.')

    return render(request, 'login.html', { 'page_title': 'Login - RangBot' })

def landing_page(request):
    """
    View untuk menampilkan landing page RangBot.
    """
    context = {
        'page_title': 'RangBot - Sistem Deteksi Penyakit Stroberi',
        'features': [
            {
                'icon': '🤖',
                'title': 'Deteksi Penyakit Machine Learning',
                'description': 'Menggunakan teknologi R-CNN untuk mendeteksi penyakit stroberi secara akurat dan real-time.'
            },
            {
                'icon': '🎮',
                'title': 'Kontrol Robot',
                'description': 'Mode otomatis berdasarkan jadwal dan mode manual untuk kontrol langsung kanan-kiri.'
            },
            {
                'icon': '📊',
                'title': 'Monitoring Real-time',
                'description': 'Data sensor langsung dari Firebase Realtime Database untuk monitoring kebun Anda.'
            },
            {
                'icon': '🗺️',
                'title': 'Peta Navigasi',
                'description': 'Visualisasi lokasi robot dan pembagian blok kebun secara interaktif.'
            },
            {
                'icon': '📜',
                'title': 'Riwayat Deteksi',
                'description': 'Catat dan analisis riwayat deteksi penyakit untuk optimasi perawatan kebun.'
            },
            {
                'icon': '📢',
                'title': 'Notifikasi Member',
                'description': 'Dapatkan notifikasi instan ketika ada deteksi penyakit atau anomali di kebun.'
            },
        ],
        'pricing_plans': [
            {
                'name': 'Basic',
                'price': 'Rp 2.500.000',
                'period': '/bulan',
                'features': [
                    'Deteksi penyakit dasar',
                    '1 Robot untuk 1 blok',
                    'Monitoring real-time',
                    'Riwayat 30 hari',
                    'Email support'
                ],
                'highlight': False
            },
            {
                'name': 'Standard',
                'price': 'Rp 4.500.000',
                'period': '/bulan',
                'features': [
                    'Deteksi penyakit lanjutan',
                    '2 Robot untuk 2 blok',
                    'Monitoring & analitik',
                    'Riwayat unlimited',
                    'Priority support',
                    'Notifikasi WhatsApp'
                ],
                'highlight': True
            },
            {
                'name': 'Premium',
                'price': 'Rp 8.000.000',
                'period': '/bulan',
                'features': [
                    'Deteksi AI tingkat expert',
                    'Multi robot & multi blok',
                    'Dashboard analytics premium',
                    'Konsultasi agronomis',
                    'Dedicated support 24/7',
                    'Custom integration',
                    'API access'
                ],
                'highlight': False
            },
        ],
        'user_roles': [
            {
                'name': 'Admin',
                'icon': '👨‍💼',
                'description': 'Mengelola seluruh sistem, user, robot, dan data kebun.'
            },
            {
                'name': 'Member',
                'icon': '🌾',
                'description': 'Pemilik kebun yang dapat mengontrol robot dan melihat data kebun mereka.'
            },
            {
                'name': 'Guest',
                'icon': '👤',
                'description': 'Pengunjung yang dapat melihat informasi umum tentang RangBot.'
            },
        ],
        'faqs': [
            {
                'question': 'Bagaimana cara kerja RangBot?',
                'answer': 'RangBot adalah robot bergerak yang dipasang pada rel di tengah blok kebun stroberi. Robot bergerak kanan-kiri secara otomatis berdasarkan jadwal atau dapat dikontrol manual melalui website. Robot dilengkapi kamera AI yang mendeteksi penyakit dan sensor yang mengirim data ke Firebase.'
            },
            {
                'question': 'Berapa luas kebun yang bisa di-cover oleh satu robot?',
                'answer': 'Satu robot standar dapat meng-cover satu blok kebun dengan panjang rel hingga 50 meter. Untuk kebun yang lebih besar, Anda dapat menggunakan multiple robot dengan paket Standard atau Premium.'
            },
            {
                'question': 'Apa saja jenis penyakit yang bisa dideteksi?',
                'answer': 'RangBot dapat mendeteksi berbagai penyakit umum pada stroberi seperti bercak daun (leaf spot), busuk akar (root rot), embun tepung (powdery mildew), dan penyakit lainnya menggunakan model AI R-CNN yang telah dilatih.'
            },
            {
                'question': 'Apakah data sensor real-time?',
                'answer': 'Ya, semua data sensor (suhu, kelembaban, kondisi tanaman) dikirim secara real-time ke Firebase Realtime Database dan dapat Anda pantau melalui dashboard website kapan saja.'
            },
            {
                'question': 'Bagaimana cara berlangganan?',
                'answer': 'Anda dapat memilih paket yang sesuai, klik "Daftar Sekarang", isi form pendaftaran, dan tim kami akan menghubungi Anda untuk proses instalasi dan setup robot di kebun Anda.'
            },
        ],
        'forum_posts': [
            {
                'author': 'Budi Santoso',
                'date': '10 Nov 2025',
                'title': 'Tips Perawatan Stroberi di Musim Hujan',
                'excerpt': 'Berbagi pengalaman menggunakan RangBot untuk monitoring kelembaban saat musim hujan...',
                'replies': 12
            },
            {
                'author': 'Siti Nurhaliza',
                'date': '8 Nov 2025',
                'title': 'Hasil Deteksi Penyakit Bulan Pertama',
                'excerpt': 'Alhamdulillah setelah sebulan pakai RangBot, terdeteksi dini beberapa tanaman yang sakit...',
                'replies': 8
            },
            {
                'author': 'Ahmad Hidayat',
                'date': '5 Nov 2025',
                'title': 'Pertanyaan Setup Robot di Blok B',
                'excerpt': 'Halo teman-teman, ada yang punya pengalaman setup robot untuk dua blok sekaligus?...',
                'replies': 15
            },
        ]
    }
    
    return render(request, 'landing.html', context)


class LandingPageView(TemplateView):
    """
    Class-based view alternative untuk landing page
    """
    template_name = 'landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'RangBot - Sistem Deteksi Penyakit Stroberi'
        return context


def product_info(request):
    """
    View untuk halaman Informasi Produk (FAQ, Harga, Forum)
    """
    # Check for success notification from contact support
    show_success = request.GET.get('success') == '1'
    success_name = request.GET.get('name', '')
    success_ticket = request.GET.get('ticket', '')
    
    # Check for success notification from sales
    show_sales_success = request.GET.get('sales_success') == '1'
    sales_success_name = request.GET.get('sales_name', '')
    
    # Get latest forum posts (limit 3)
    try:
        forum_posts = ForumPost.objects.all()[:3]
        forum_posts_list = []
        for post in forum_posts:
            forum_posts_list.append({
                'title': post.title,
                'author': post.author.name,
                'date': post.created_at.strftime('%d %b %Y'),
                'excerpt': post.get_excerpt(100),
                'replies': post.get_comment_count(),
                'category': post.get_category_display(),
            })
    except:
        # If database tables don't exist yet, use empty list
        forum_posts_list = []
    
    context = {
        'page_title': 'Informasi Produk - RangBot',
        'show_success_notification': show_success,
        'success_name': success_name,
        'success_ticket': success_ticket,
        'show_sales_success': show_sales_success,
        'sales_success_name': sales_success_name,
        'faqs': [
            {
                'question': 'Apa itu RangBot dan bagaimana cara kerjanya?',
                'answer': 'RangBot adalah robot pintar yang bergerak otomatis di rel greenhouse menggunakan sistem AI untuk mendeteksi penyakit tanaman stroberi. Robot dilengkapi dengan kamera HD, sensor IoT untuk suhu dan kelembaban, serta terhubung ke cloud untuk monitoring real-time.'
            },
            {
                'question': 'Berapa tingkat akurasi deteksi penyakit RangBot?',
                'answer': 'RangBot menggunakan teknologi R-CNN dengan tingkat akurasi hingga 98% untuk mendeteksi berbagai jenis penyakit pada tanaman stroberi. Sistem terus belajar dan meningkatkan akurasi melalui machine learning.'
            },
            {
                'question': 'Apakah RangBot bisa dipasang di greenhouse yang sudah ada?',
                'answer': 'Ya, RangBot dirancang modular dan dapat dipasang di greenhouse existing. Sistem rel dapat disesuaikan dengan ukuran greenhouse Anda. Tim teknisi kami akan melakukan survei dan instalasi profesional.'
            },
            {
                'question': 'Bagaimana cara mengakses data dan dashboard?',
                'answer': 'Setelah pembelian, Anda akan mendapatkan ID Member yang memberikan akses ke dashboard web dan mobile app. Dashboard dapat diakses dari browser atau smartphone untuk melihat data real-time dan histori.'
            },
            {
                'question': 'Apakah perlu koneksi internet?',
                'answer': 'Ya, RangBot memerlukan koneksi internet untuk sinkronisasi data ke cloud. Robot tetap dapat beroperasi secara lokal jika koneksi terputus sementara, dan akan melakukan sinkronisasi otomatis ketika koneksi kembali.'
            },
            {
                'question': 'Berapa lama masa garansi RangBot?',
                'answer': 'RangBot dilengkapi dengan garansi 2 tahun untuk hardware dan lifetime support untuk software. Garansi mencakup perbaikan atau penggantian komponen yang rusak.'
            },
        ],
        'pricing_plans': [
            {
                'name': 'Basic',
                'price': '10.000.000',
                'description': 'Paket dasar untuk kebutuhan Anda',
                'features': [
                    '1 Unit RangBot',
                    'Garansi 1 tahun',
                    'Training Lengkap',
                    'Customer support'
                ],
                'highlight': False
            },
            {
                'name': 'Professional',
                'price': '15.000.000',
                'description': 'Paket profesional dengan dukungan prioritas',
                'features': [
                    '1 Unit RangBot Pro',
                    'Garansi 2 tahun',
                    'Training Lengkap',
                    'Priority customer support'
                ],
                'highlight': True
            },
        ],
        'forum_posts': forum_posts_list
    }
    
    return render(request, 'product_info.html', context)


def purchase(request):
    """
    View untuk halaman Pembelian/Pemesanan
    """
    from .models import PurchaseOrder
    from decimal import Decimal
    
    # Get selected package from URL parameter
    selected_package = request.GET.get('paket', '').lower()
    
    # Handle form submission
    if request.method == 'POST':
        try:
            # Get form data
            customer_name = request.POST.get('name', '').strip()
            customer_email = request.POST.get('email', '').strip()
            customer_phone = request.POST.get('phone', '').strip()
            company_name = request.POST.get('company', '').strip()
            customer_address = request.POST.get('address', '').strip()
            blocks = request.POST.get('blocks', '').strip()
            length = request.POST.get('length', '').strip()
            notes = request.POST.get('notes', '').strip()
            
            # Get package quantities
            qty_basic = int(request.POST.get('qty_basic', 0) or 0)
            qty_professional = int(request.POST.get('qty_professional', 0) or 0)
            
            # Validate
            if not customer_name or not customer_email or not customer_phone or not customer_address:
                messages.error(request, 'Mohon lengkapi semua field yang wajib diisi.')
                return redirect('main:purchase')
            
            if qty_basic == 0 and qty_professional == 0:
                messages.error(request, 'Mohon pilih minimal 1 paket (Basic atau Professional).')
                return redirect('main:purchase')
            
            # Calculate total price
            price_basic = Decimal('10000000')  # 10.000.000
            price_professional = Decimal('15000000')  # 15.000.000
            total_price = (qty_basic * price_basic) + (qty_professional * price_professional)
            
            # Create PurchaseOrder
            purchase_order = PurchaseOrder.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                customer_address=customer_address,
                company_name=company_name if company_name else None,
                qty_basic=qty_basic,
                qty_professional=qty_professional,
                total_price=total_price,
                notes=notes if notes else None,
                status='pending'
            )
            
            messages.success(request, 'Pesanan Anda telah dikirim! Tim kami akan menghubungi Anda dalam 1x24 jam untuk verifikasi.')
            return redirect('main:purchase')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat mengirim pesanan: {str(e)}')
            return redirect('main:purchase')
    
    context = {
        'page_title': 'Pemesanan RangBot',
        'selected_package': selected_package,
        'pricing_plans': [
            {
                'name': 'Basic',
                'price': '10.000.000',
                'description': 'Paket dasar untuk kebutuhan Anda',
                'features': [
                    '1 Unit RangBot',
                    'Garansi 1 tahun',
                    'Training Lengkap',
                    'Customer support'
                ],
                'highlight': False
            },
            {
                'name': 'Professional',
                'price': '15.000.000',
                'description': 'Paket profesional dengan dukungan prioritas',
                'features': [
                    '1 Unit RangBot Pro',
                    'Garansi 2 tahun',
                    'Training Lengkap',
                    'Priority customer support'
                ],
                'highlight': True
            },
        ]
    }
    
    return render(request, 'purchase.html', context)


def login_view(request):
    """
    View untuk halaman Login
    """
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '')
        
        if identifier and password:
            # Try to find member by username, member_id, or email
            member = None
            try:
                if identifier.startswith('RB-'):
                    member = Member.objects.get(member_id=identifier)
                else:
                    member = Member.objects.filter(
                        models.Q(username=identifier) | models.Q(email=identifier)
                    ).first()
            except Member.DoesNotExist:
                pass
            
            if member:
                # Check password
                if check_password(password, member.password):
                    # Login successful
                    request.session['member_id'] = member.member_id
                    request.session['member_name'] = member.full_name
                    request.session['member_username'] = member.username
                    messages.success(request, f'Selamat datang, {member.full_name}!')
                    return redirect('main:member_dashboard')
                else:
                    messages.error(request, 'Password salah.')
            else:
                messages.error(request, 'Username/ID Member/Email tidak ditemukan.')
        else:
            messages.error(request, 'Harap isi semua field.')
    
    context = {
        'page_title': 'Login - RangBot',
    }
    
    return render(request, 'login.html', context)


def register_view(request):
    """
    View untuk halaman Register
    """
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '').strip().upper()
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if not all([member_id, username, full_name, email, password, confirm_password]):
            messages.error(request, 'Harap isi semua field yang wajib.')
        elif password != confirm_password:
            messages.error(request, 'Password tidak cocok.')
        elif len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
        else:
            # Check if member_id or username already exists
            if Member.objects.filter(member_id=member_id).exists():
                messages.error(request, 'ID Member sudah terdaftar.')
            elif Member.objects.filter(username=username).exists():
                messages.error(request, 'Username sudah digunakan.')
            elif Member.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar.')
            else:
                # Create new member
                member = Member.objects.create(
                    member_id=member_id,
                    username=username,
                    full_name=full_name,
                    email=email,
                    phone=phone or None,
                    password=make_password(password),
                )
                
                messages.success(request, 'Registrasi berhasil! Silakan login.')
                return redirect('main:login')
    
    context = {
        'page_title': 'Register - RangBot',
    }
    
    return render(request, 'register.html', context)


def contact_support(request):
    """
    View untuk halaman Hubungi Support
    Menangani form submission dari guest dan mengarahkan ke dashboard customer service
    """
    if request.method == 'POST':
        # Handle form submission
        # In production, you would save to database and redirect to customer service dashboard
        # For now, we'll redirect to FAQ page with success notification
        
        # Generate ticket number (in production, this would come from database)
        ticket_number = f"RBT-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')[:4]}"
        
        # TODO: In production, save to database:
        # SupportTicket.objects.create(
        #     ticket_number=ticket_number,
        #     name=request.POST.get('name', ''),
        #     email=request.POST.get('email', ''),
        #     subject=request.POST.get('subject', ''),
        #     category=request.POST.get('category', ''),
        #     message=request.POST.get('message', ''),
        #     status='pending',
        #     created_at=datetime.now()
        # )
        
        # Redirect to product info page with success notification
        params = urlencode({
            'success': '1',
            'name': request.POST.get('name', ''),
            'ticket': ticket_number,
        })
        return redirect(f'/informasi-produk/?{params}')
    
    context = {
        'page_title': 'Hubungi Support - RangBot',
        'submitted': False,
    }
    
    return render(request, 'contact_support.html', context)


def contact_sales(request):
    """
    View untuk halaman Hubungi Sales (Custom Package Inquiry)
    Menangani form submission dari guest untuk konsultasi paket custom
    """
    if request.method == 'POST':
        # Handle form submission
        # In production, you would save to database and redirect to sales dashboard
        # For now, we'll redirect to product info page with success notification
        
        # TODO: In production, save to database:
        # SalesInquiry.objects.create(
        #     name=request.POST.get('name', ''),
        #     email=request.POST.get('email', ''),
        #     phone=request.POST.get('phone', ''),
        #     blocks=request.POST.get('blocks', ''),
        #     budget=request.POST.get('budget', ''),
        #     requirements=request.POST.get('requirements', ''),
        #     status='pending',
        #     created_at=datetime.now()
        # )
        
        # Redirect to product info page with success notification
        params = urlencode({
            'sales_success': '1',
            'sales_name': request.POST.get('name', ''),
        })
        return redirect(f'/informasi-produk/?{params}')
    
    context = {
        'page_title': 'Hubungi Sales - RangBot',
        'submitted': False,
    }
    
    return render(request, 'product_info.html', context)


# ==================== FORUM VIEWS ====================

def get_forum_user(request):
    """
    Helper function untuk mendapatkan forum user dari session
    """
    user_id = request.session.get('forum_user_id')
    if user_id:
        try:
            return ForumUser.objects.get(id=user_id)
        except ForumUser.DoesNotExist:
            return None
    return None


def forum_login(request):
    """
    Redirect forum login ke unified login system
    """
    next_url = request.GET.get('next', reverse('main:forum_list'))
    messages.info(request, 'Silakan login melalui sistem login utama untuk mengakses forum.')
    return redirect(f"{reverse('main:login')}?next={next_url}")


def forum_logout(request):
    """
    View untuk logout forum
    """
    request.session.pop('forum_user_id', None)
    request.session.pop('forum_user_name', None)
    request.session.pop('forum_user_email', None)
    messages.success(request, 'Anda telah logout dari forum.')
    return redirect('main:forum_list')


def forum_list(request):
    """
    View untuk menampilkan daftar postingan forum
    """
    posts = ForumPost.objects.all()
    
    # Filter by category jika ada
    category = request.GET.get('category', '')
    if category:
        posts = posts.filter(category=category)
    
    # Search jika ada
    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(title__icontains=search) | posts.filter(content__icontains=search)
    
    forum_user = get_forum_user(request)
    
    context = {
        'page_title': 'Forum RangBot',
        'posts': posts,
        'forum_user': forum_user,
        'current_category': category,
        'search_query': search,
    }
    return render(request, 'forum_list.html', context)


def forum_detail(request, post_id):
    """
    View untuk menampilkan detail postingan dan komentar
    """
    post = get_object_or_404(ForumPost, id=post_id)
    forum_user = get_forum_user(request)
    
    # Tambah view count
    post.views += 1
    post.save()
    
    # Handle comment form
    comment_form = None
    if forum_user:
        if request.method == 'POST' and 'comment' in request.POST:
            comment_form = ForumCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = forum_user
                comment.save()
                messages.success(request, 'Komentar berhasil ditambahkan!')
                return redirect('main:forum_detail', post_id=post_id)
        else:
            comment_form = ForumCommentForm()
    
    # Get comments
    comments = post.comments.all()
    
    context = {
        'page_title': f'{post.title} - Forum RangBot',
        'post': post,
        'comments': comments,
        'forum_user': forum_user,
        'comment_form': comment_form,
    }
    return render(request, 'forum_detail.html', context)


def forum_create(request):
    """
    View untuk membuat postingan baru (hanya untuk user yang login)
    """
    forum_user = get_forum_user(request)
    
    if not forum_user:
        messages.warning(request, 'Anda harus login terlebih dahulu untuk membuat postingan.')
        return redirect(f"{reverse('main:login')}?next={reverse('main:forum_create')}")
    
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = forum_user
            post.save()
            messages.success(request, 'Postingan berhasil dibuat!')
            return redirect('main:forum_detail', post_id=post.id)
    else:
        form = ForumPostForm()
    
    context = {
        'page_title': 'Buat Postingan Baru - Forum RangBot',
        'form': form,
        'forum_user': forum_user,
    }
    return render(request, 'forum_create.html', context)


def forum_edit(request, post_id):
    """
    View untuk mengedit postingan (hanya pemilik postingan)
    """
    post = get_object_or_404(ForumPost, id=post_id)
    forum_user = get_forum_user(request)
    
    if not forum_user:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect(f"{reverse('main:login')}?next={reverse('main:forum_edit', args=[post_id])}")
    
    if post.author != forum_user:
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit postingan ini.')
        return redirect('main:forum_detail', post_id=post_id)
    
    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Postingan berhasil diperbarui!')
            return redirect('main:forum_detail', post_id=post_id)
    else:
        form = ForumPostForm(instance=post)
    
    context = {
        'page_title': f'Edit: {post.title} - Forum RangBot',
        'form': form,
        'post': post,
        'forum_user': forum_user,
    }
    return render(request, 'forum_edit.html', context)


def forum_delete(request, post_id):
    """
    View untuk menghapus postingan (hanya pemilik postingan)
    """
    post = get_object_or_404(ForumPost, id=post_id)
    forum_user = get_forum_user(request)
    
    if not forum_user:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if post.author != forum_user:
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus postingan ini.')
        return redirect('main:forum_detail', post_id=post_id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Postingan berhasil dihapus!')
        return redirect('main:forum_list')
    
    context = {
        'page_title': 'Hapus Postingan - Forum RangBot',
        'post': post,
        'forum_user': forum_user,
    }
    return render(request, 'forum_delete.html', context)


# ==================== DASHBOARD MEMBER VIEWS ====================

def get_member(request):
    """Helper function untuk mendapatkan member dari session"""
    member_id = request.session.get('member_id')
    if member_id:
        try:
            return Member.objects.get(member_id=member_id)
        except Member.DoesNotExist:
            return None
    return None


def member_dashboard(request):
    """
    View untuk dashboard utama member
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Update last login
    member.last_login = timezone.now()
    member.save(update_fields=['last_login'])
    
    # Get devices
    devices = member.rangbot_devices.all()
    
    # Count active devices
    active_devices_count = devices.filter(status='active').count()
    
    # Get unread notifications
    unread_notifications = member.notifications.filter(is_read=False)[:5]
    
    # Get recent detections
    recent_detections = DetectionHistory.objects.filter(device__member=member)[:5]
    
    context = {
        'page_title': 'Dashboard Member - RangBot',
        'member': member,
        'devices': devices,
        'active_devices_count': active_devices_count,
        'unread_notifications': unread_notifications,
        'recent_detections': recent_detections,
    }
    return render(request, 'dashboard/dashboard.html', context)


def device_detail(request, device_id):
    """
    View untuk detail perangkat RangBot
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id, member=member)
    
    # Get recent detections for this device
    detections = device.detections.all()[:10]
    
    context = {
        'page_title': f'{device.device_name or device.serial_number} - Dashboard',
        'member': member,
        'device': device,
        'detections': detections,
    }
    return render(request, 'dashboard/device_detail.html', context)


def device_control(request, device_id):
    """
    View untuk kontrol perangkat RangBot
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id, member=member)
    
    context = {
        'page_title': f'Kontrol {device.device_name or device.serial_number}',
        'member': member,
        'device': device,
    }
    return render(request, 'dashboard/device_control.html', context)


def device_streaming(request, device_id):
    """
    View untuk streaming kamera perangkat
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id, member=member)
    
    context = {
        'page_title': f'Streaming {device.device_name or device.serial_number}',
        'member': member,
        'device': device,
    }
    return render(request, 'dashboard/device_streaming.html', context)


def device_sensor(request, device_id):
    """
    View untuk data sensor perangkat (Firebase)
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id, member=member)
    
    context = {
        'page_title': f'Data Sensor {device.device_name or device.serial_number}',
        'member': member,
        'device': device,
    }
    return render(request, 'dashboard/device_sensor.html', context)


def device_detection_history(request, device_id):
    """
    View untuk riwayat deteksi perangkat
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id, member=member)
    detections = device.detections.all()
    
    context = {
        'page_title': f'Riwayat Deteksi {device.device_name or device.serial_number}',
        'member': member,
        'device': device,
        'detections': detections,
    }
    return render(request, 'dashboard/device_detection_history.html', context)


def manual_detection(request):
    """
    View untuk deteksi manual menggunakan R-CNN
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        # Handle file upload and detection
        # TODO: Implement R-CNN detection logic
        messages.success(request, 'Deteksi manual berhasil dilakukan!')
        return redirect('main:member_dashboard')
    
    context = {
        'page_title': 'Deteksi Manual - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/manual_detection.html', context)


def add_device(request):
    """
    View untuk menambahkan nomor seri perangkat baru
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number', '').strip()
        device_name = request.POST.get('device_name', '').strip()
        covered_blocks = request.POST.get('covered_blocks', '').strip()
        
        if not serial_number:
            messages.error(request, 'Nomor seri tidak boleh kosong.')
        else:
            # Check if serial number already exists
            if RangBotDevice.objects.filter(serial_number=serial_number).exists():
                messages.error(request, 'Nomor seri sudah terdaftar.')
            else:
                # Create new device
                device = RangBotDevice.objects.create(
                    serial_number=serial_number,
                    member=member,
                    device_name=device_name or None,
                    covered_blocks=covered_blocks or None,
                    status='offline',
                )
                
                # Create notification
                Notification.objects.create(
                    member=member,
                    notification_type='device_added',
                    title='Perangkat Ditambahkan',
                    message=f'Perangkat {device.get_display_name()} berhasil ditambahkan ke akun Anda.',
                )
                
                messages.success(request, 'Perangkat berhasil ditambahkan!')
                return redirect('main:member_dashboard')
    
    context = {
        'page_title': 'Tambah Perangkat - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/add_device.html', context)


def member_profile(request):
    """
    View untuk profil member sederhana
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    context = {
        'page_title': 'Profil - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/member_profile.html', context)


def member_notifications(request):
    """
    View untuk melihat semua notifikasi
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    notifications = member.notifications.all()
    
    # Mark as read if requested
    if request.method == 'POST' and 'mark_read' in request.POST:
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, member=member)
                notification.is_read = True
                notification.save()
                messages.success(request, 'Notifikasi ditandai sebagai sudah dibaca.')
            except Notification.DoesNotExist:
                pass
    
    context = {
        'page_title': 'Notifikasi - Dashboard',
        'member': member,
        'notifications': notifications,
    }
    return render(request, 'dashboard/notifications.html', context)


def member_logout(request):
    """
    Logout member
    """
    request.session.flush()
    messages.success(request, 'Anda telah logout.')
    return redirect('main:login')