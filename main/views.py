from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from datetime import datetime
from django.db import models
from .models import ForumUser, ForumPost, ForumComment, Admin, CustomerService, PurchaseOrder, Member, RangBotDevice, DetectionHistory, Notification, FAQ, ProductInfo, ContactMessage
from .forms import ForumLoginForm, ForumPostForm, ForumCommentForm
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Helper function untuk check admin
def is_staff_user(user):
    return user.is_staff or user.is_superuser


def member_login(request):
    """Login tunggal: Admin, Member, atau CS - diarahkan sesuai peran."""
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
                request.session['user_role'] = 'admin'
                admin.last_login = timezone.now()
                admin.save(update_fields=['last_login'])
                # Tidak menampilkan pesan welcome untuk admin
                return redirect('main:admin_dashboard')
        except Admin.DoesNotExist:
            pass

        # 2) Coba sebagai Customer Service (CS)
        try:
            cs = CustomerService.objects.get(username=username, is_active=True)
            if cs.password and check_password(password, cs.password):
                request.session['cs_id'] = cs.id
                request.session['cs_username'] = cs.username
                request.session['cs_name'] = cs.full_name
                request.session['user_role'] = 'cs'
                cs.last_login = timezone.now()
                cs.save(update_fields=['last_login'])
                messages.success(request, f'Selamat datang, {cs.full_name}!')
                return redirect('main:cs_dashboard')
        except CustomerService.DoesNotExist:
            pass

        # 3) Coba sebagai Member terdaftar
        try:
            member = Member.objects.get(username=username, is_registered=True)
            if not member.is_active:
                messages.error(request, 'Akun Anda telah dinonaktifkan. Silakan hubungi admin untuk informasi lebih lanjut.')
                return render(request, 'login.html', { 'page_title': 'Login - RangBot' })
            if member.password and check_password(password, member.password):
                request.session['member_id'] = member.member_id
                request.session['member_username'] = member.username
                request.session['member_name'] = member.full_name
                request.session['user_role'] = 'member'
                member.last_login = timezone.now()
                member.save(update_fields=['last_login'])
                messages.success(request, f'Selamat datang, {member.full_name}!')
                return redirect('main:member_dashboard')
        except Member.DoesNotExist:
            pass

        # Jika gagal semua
        messages.error(request, 'Username atau password salah.')

    return render(request, 'login.html', { 'page_title': 'Login - RangBot' })

def landing_page(request):
    """
    View untuk menampilkan landing page RangBot.
    """
    # Get FAQ from database (only active ones, ordered by order field)
    try:
        faqs_queryset = FAQ.objects.filter(is_active=True).order_by('order', 'created_at')
        faqs_list = []
        for faq in faqs_queryset:
            faqs_list.append({
                'question': faq.question,
                'answer': faq.answer,
            })
    except:
        # If database tables don't exist yet, use empty list
        faqs_list = []
    
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
        'faqs': faqs_list,
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
    # Check for success notification from contact support (from session)
    contact_form_name = request.session.get('contact_form_name', '')
    contact_form_email = request.session.get('contact_form_email', '')
    
    # Clear session data after reading (one-time use)
    if contact_form_name or contact_form_email:
        request.session.pop('contact_form_name', None)
        request.session.pop('contact_form_email', None)
    
    # Check for success notification from contact support (legacy GET params)
    show_success = request.GET.get('success') == '1'
    success_name = request.GET.get('name', '')
    success_ticket = request.GET.get('ticket', '')
    
    # Check for success notification from sales
    show_sales_success = request.GET.get('sales_success') == '1'
    sales_success_name = request.GET.get('sales_name', '')
    
    # Get FAQ from database (only active ones)
    try:
        faqs_queryset = FAQ.objects.filter(is_active=True).order_by('order', 'created_at')
        faqs_list = []
        for faq in faqs_queryset:
            faqs_list.append({
                'question': faq.question,
                'answer': faq.answer,
            })
    except:
        # If database tables don't exist yet, use empty list
        faqs_list = []
    
    # Get pricing plans from database (only active ones)
    try:
        products_queryset = ProductInfo.objects.filter(is_active=True).order_by('package_type')
        pricing_plans_list = []
        for product in products_queryset:
            features = product.get_features_list() if hasattr(product, 'get_features_list') else []
            pricing_plans_list.append({
                'name': product.name,
                'price': f"{product.price:,.0f}".replace(',', '.'),
                'description': product.description or 'Paket untuk kebutuhan Anda',
                'features': features if features else [],
                'highlight': product.package_type == 'professional',  # Professional is highlighted
            })
    except:
        # If database tables don't exist yet, use empty list
        pricing_plans_list = []
    
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
        'contact_form_name': contact_form_name,
        'contact_form_email': contact_form_email,
        'show_sales_success': show_sales_success,
        'sales_success_name': sales_success_name,
        'faqs': faqs_list,
        'pricing_plans': pricing_plans_list,
        'forum_posts': forum_posts_list
    }
    
    return render(request, 'product_info.html', context)


def purchase(request):
    """
    View untuk halaman Pembelian/Pemesanan
    """
    from decimal import Decimal
    
    # Get selected package from URL parameter
    selected_package = request.GET.get('paket', '').lower()
    
    # Get pricing plans from database (only active ones)
    try:
        products_queryset = ProductInfo.objects.filter(is_active=True).order_by('package_type')
        pricing_plans_list = []
        products_dict = {}  # Store products by package_type for price calculation
        
        for product in products_queryset:
            features = product.get_features_list() if hasattr(product, 'get_features_list') else []
            pricing_plans_list.append({
                'name': product.name,
                'package_type': product.package_type,  # Add package_type for reference
                'price': f"{product.price:,.0f}".replace(',', '.'),
                'price_decimal': product.price,  # Store decimal for calculation
                'description': product.description or 'Paket untuk kebutuhan Anda',
                'features': features if features else [],
                'highlight': product.package_type == 'professional',  # Professional is highlighted
            })
            # Store product for price lookup
            products_dict[product.package_type] = product
    except:
        # If database tables don't exist yet, use empty list
        pricing_plans_list = []
        products_dict = {}
    
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
            payment_method = request.POST.get('payment_method', '').strip()
            
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
            
            # Validate payment method if provided
            valid_payment_methods = ['transfer', 'credit', 'installment', 'leasing']
            if payment_method and payment_method not in valid_payment_methods:
                messages.error(request, 'Metode pembayaran tidak valid.')
                return redirect('main:purchase')
            
            # Calculate total price from database
            price_basic = Decimal('0')
            price_professional = Decimal('0')
            
            if 'basic' in products_dict:
                price_basic = Decimal(str(products_dict['basic'].price))
            if 'professional' in products_dict:
                price_professional = Decimal(str(products_dict['professional'].price))
            
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
                payment_method=payment_method if payment_method else None,
                status='pending'
            )
            
            # Create ActivityLog for new purchase order (system notification for admin)
            from .models import ActivityLog
            ActivityLog.objects.create(
                action_type='order_created',
                description=f'Pembelian baru: Order #{purchase_order.id} dari {customer_name} ({customer_email}). Total: {purchase_order.get_total_units()} unit (Basic: {qty_basic}, Pro: {qty_professional}). Total harga: Rp {total_price:,.0f}',
                performed_by=None,  # Created by customer, not admin
                related_order=purchase_order,
                metadata={
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'total_units': purchase_order.get_total_units(),
                    'qty_basic': qty_basic,
                    'qty_professional': qty_professional,
                    'total_price': float(total_price),
                }
            )
            
            messages.success(request, 'Pesanan Anda telah dikirim! Tim kami akan menghubungi Anda dalam 1x24 jam untuk verifikasi.')
            return redirect('main:purchase')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat mengirim pesanan: {str(e)}')
            return redirect('main:purchase')
    
    context = {
        'page_title': 'Pemesanan RangBot',
        'selected_package': selected_package,
        'pricing_plans': pricing_plans_list,
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
    Member ID harus sudah ada di database (dibuat saat admin verifikasi purchase order)
    Customer tidak bisa membuat Member ID sendiri
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
            # Validasi Member ID: harus sudah ada di database dan belum terdaftar
            try:
                member = Member.objects.get(member_id=member_id)
                
                # Cek apakah sudah terdaftar
                if member.is_registered:
                    messages.error(request, 'ID Member ini sudah terdaftar. Silakan login.')
                    return redirect('main:login')
                
                # Validasi email harus sesuai dengan email di purchase order
                if member.email.lower() != email.lower():
                    messages.error(request, f'Email tidak sesuai dengan email yang terdaftar di pembelian. Email yang benar: {member.email}')
                    return render(request, 'register.html', {
                        'page_title': 'Register - RangBot',
                        'member_id': member_id,
                        'username': username,
                        'full_name': full_name,
                        'email': email,
                        'phone': phone,
                    })
                
                # Cek username dan email tidak digunakan oleh member lain
                if Member.objects.filter(username=username).exclude(member_id=member_id).exists():
                    messages.error(request, 'Username sudah digunakan.')
                    return render(request, 'register.html', {
                        'page_title': 'Register - RangBot',
                        'member_id': member_id,
                        'username': username,
                        'full_name': full_name,
                        'email': email,
                        'phone': phone,
                    })
                elif Member.objects.filter(email=email).exclude(member_id=member_id).exists():
                    messages.error(request, 'Email sudah terdaftar.')
                    return render(request, 'register.html', {
                        'page_title': 'Register - RangBot',
                        'member_id': member_id,
                        'username': username,
                        'full_name': full_name,
                        'email': email,
                        'phone': phone,
                    })
                
                # Update member dengan data registrasi
                member.username = username
                member.full_name = full_name
                member.phone = phone or member.phone
                member.password = make_password(password)
                member.is_registered = True
                member.save()
                
                # Create ActivityLog for user registration (system notification for admin)
                from .models import ActivityLog
                ActivityLog.objects.create(
                    action_type='member_registered',
                    description=f'Member {member.member_id} ({full_name}) berhasil terdaftar dengan username: {username}',
                    performed_by=None,  # Registered by user, not admin
                    related_member=member,
                    metadata={
                        'member_id': member.member_id,
                        'username': username,
                        'full_name': full_name,
                        'email': email,
                    }
                )
                
                messages.success(request, 'Registrasi berhasil! Silakan login.')
                return redirect('main:login')
                    
            except Member.DoesNotExist:
                messages.error(request, 'ID Member tidak valid atau tidak ditemukan. Pastikan Anda menggunakan Member ID yang diberikan oleh admin setelah verifikasi pembelian.')
    
    context = {
        'page_title': 'Register - RangBot',
    }
    
    return render(request, 'register.html', context)


def contact_support(request):
    """
    View untuk halaman Hubungi Support
    Menyimpan pesan ke database untuk ditangani oleh Customer Service
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not all([name, email, subject, message]):
            messages.error(request, 'Mohon lengkapi semua field yang wajib diisi.')
            return redirect('main:contact_support')
        
        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            status='new'
        )
        
        # Set success flag in session for popup
        request.session['contact_form_success'] = True
        request.session['contact_form_name'] = name
        request.session['contact_form_email'] = email
        
        # Check if form was submitted from modal (product_info page)
        if request.POST.get('from_modal') == 'true':
            messages.success(request, 'Pesan Anda telah dikirim! Tim Customer Service akan menghubungi Anda segera.')
            # Keep session data for popup
            return redirect('main:product_info')
        
        # For contact_support.html page, redirect to same page to show popup
        return redirect('main:contact_support')
    
    # Check for success flag
    show_success_popup = request.session.pop('contact_form_success', False)
    contact_name = request.session.pop('contact_form_name', '')
    contact_email = request.session.pop('contact_form_email', '')
    
    context = {
        'page_title': 'Hubungi Support - RangBot',
        'submitted': False,
        'show_success_popup': show_success_popup,
        'contact_name': contact_name,
        'contact_email': contact_email,
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


def forum_register(request):
    """
    View untuk registrasi forum user baru
    Sistem terpisah dari login utama
    """
    if request.method == 'POST':
        from .forms import ForumRegisterForm
        form = ForumRegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            email = form.cleaned_data['email'].strip().lower()
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            
            # Cek username sudah digunakan (handle if username field doesn't exist yet)
            username_exists = False
            try:
                username_exists = ForumUser.objects.filter(username=username).exists()
            except Exception:
                # If username field doesn't exist in database yet, skip this check
                pass
            
            if username_exists:
                messages.error(request, 'Username sudah digunakan. Silakan pilih username lain.')
            # Cek email sudah digunakan
            elif ForumUser.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar. Silakan login atau gunakan email lain.')
            else:
                # Buat user baru
                user_data = {
                    'email': email,
                    'name': username,  # Default name = username, bisa diubah nanti
                    'role': role,
                    'password': make_password(password)
                }
                # Only add username if field exists in database
                try:
                    # Test if username field exists by trying to filter
                    ForumUser.objects.filter(username__isnull=False).exists()
                    user_data['username'] = username
                except Exception:
                    # Username field doesn't exist yet, skip it
                    pass
                forum_user = ForumUser.objects.create(**user_data)
                
                messages.success(request, 'Registrasi berhasil! Silakan login untuk melanjutkan.')
                return redirect('main:forum_login')
    else:
        from .forms import ForumRegisterForm
        form = ForumRegisterForm()
    
    context = {
        'page_title': 'Daftar Forum - RangBot',
        'form': form,
    }
    return render(request, 'forum_register.html', context)


def forum_login(request):
    """
    View untuk login forum
    Sistem terpisah dari login utama
    """
    next_url = request.GET.get('next', reverse('main:forum_list'))
    
    if request.method == 'POST':
        from .forms import ForumLoginForm
        form = ForumLoginForm(request.POST)
        
        if form.is_valid():
            identifier = form.cleaned_data['identifier'].strip()
            password = form.cleaned_data['password']
            
            # Coba login dengan email atau username
            try:
                if '@' in identifier:
                    forum_user = ForumUser.objects.get(email=identifier.lower())
                else:
                    # Try username, but handle if username field doesn't exist yet
                    try:
                        forum_user = ForumUser.objects.get(username=identifier)
                    except Exception:
                        # Fallback: try by email if username search fails
                        forum_user = ForumUser.objects.get(email=identifier.lower())
                
                # Cek password (handle if password field doesn't exist yet)
                if forum_user.password and check_password(password, forum_user.password):
                    # Set session
                    request.session['forum_user_id'] = forum_user.id
                    request.session['forum_user_username'] = forum_user.get_display_name()
                    request.session['forum_user_name'] = forum_user.name
                    request.session['forum_user_email'] = forum_user.email
                    request.session['forum_user_role'] = forum_user.role
                    
                    # Update last login
                    forum_user.last_login = timezone.now()
                    forum_user.save(update_fields=['last_login'])
                    
                    messages.success(request, f'Selamat datang kembali, {forum_user.get_display_name()}!')
                    # Redirect ke forum_list jika next_url tidak valid atau kosong
                    if next_url and next_url != reverse('main:forum_login'):
                        return redirect(next_url)
                    else:
                        return redirect('main:forum_list')
                else:
                    messages.error(request, 'Password salah.')
            except ForumUser.DoesNotExist:
                messages.error(request, 'Email/Username tidak ditemukan.')
    else:
        from .forms import ForumLoginForm
        form = ForumLoginForm()
    
    context = {
        'page_title': 'Login Forum - RangBot',
        'form': form,
        'next_url': next_url,
    }
    return render(request, 'forum_login.html', context)


def forum_profile(request):
    """
    View untuk menampilkan data diri forum user
    """
    forum_user = get_forum_user(request)
    
    if not forum_user:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:forum_login')
    
    context = {
        'page_title': 'Data Diri - Forum RangBot',
        'forum_user': forum_user,
    }
    return render(request, 'forum_profile.html', context)


def forum_logout(request):
    """
    View untuk logout forum
    """
    request.session.pop('forum_user_id', None)
    request.session.pop('forum_user_username', None)
    request.session.pop('forum_user_name', None)
    request.session.pop('forum_user_email', None)
    request.session.pop('forum_user_role', None)
    messages.success(request, 'Anda telah logout dari forum.')
    return redirect('main:forum_list')


def forum_list(request):
    """
    View untuk menampilkan daftar postingan forum
    Hanya user yang sudah login yang bisa membuat postingan
    """
    forum_user = get_forum_user(request)
    
    # Handle form submission (hanya untuk user yang login)
    if request.method == 'POST':
        if not forum_user:
            messages.error(request, 'Anda harus login terlebih dahulu untuk membuat postingan.')
            return redirect('main:forum_login')
        
        from .forms import ForumPostForm
        form = ForumPostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = forum_user
            post.save()
            messages.success(request, 'Postingan berhasil dibuat!')
            return redirect('main:forum_list')
        else:
            messages.error(request, 'Mohon lengkapi semua field yang wajib.')
    
    # Get posts
    posts = ForumPost.objects.all()
    
    # Filter by category jika ada
    category = request.GET.get('category', '')
    if category:
        posts = posts.filter(category=category)
    
    # Search jika ada
    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(title__icontains=search) | posts.filter(content__icontains=search)
    
    # Form untuk posting (hanya jika user login)
    from .forms import ForumPostForm
    post_form = ForumPostForm() if forum_user else None
    
    context = {
        'page_title': 'Forum RangBot',
        'posts': posts,
        'forum_user': forum_user,
        'current_category': category,
        'search_query': search,
        'form': post_form,
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
                
                # Create ActivityLog for new forum comment (system notification for admin)
                from .models import ActivityLog
                ActivityLog.objects.create(
                    action_type='forum_comment_created',
                    description=f'Komentar baru pada postingan "{post.title}" oleh {forum_user.get_display_name()} ({forum_user.email})',
                    performed_by=None,  # Created by forum user, not admin
                    metadata={
                        'post_id': post.id,
                        'post_title': post.title,
                        'comment_id': comment.id,
                        'author_name': forum_user.get_display_name(),
                        'author_email': forum_user.email,
                    }
                )
                
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
            
            # Create ActivityLog for new forum post (system notification for admin)
            from .models import ActivityLog
            ActivityLog.objects.create(
                action_type='forum_post_created',
                description=f'Postingan forum baru: "{post.title}" oleh {forum_user.get_display_name()} ({forum_user.email}) di kategori {post.get_category_display()}',
                performed_by=None,  # Created by forum user, not admin
                metadata={
                    'post_id': post.id,
                    'post_title': post.title,
                    'author_name': forum_user.get_display_name(),
                    'author_email': forum_user.email,
                    'category': post.category,
                }
            )
            
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


def member_devices(request):
    """
    View untuk halaman Manajemen Rangbot - menampilkan daftar nomor seri perangkat
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get all devices for this member
    devices = member.rangbot_devices.all().order_by('-created_at')
    
    context = {
        'page_title': 'Manajemen Rangbot - Dashboard',
        'member': member,
        'devices': devices,
    }
    return render(request, 'dashboard/devices_list.html', context)


def member_add_device(request):
    """
    View untuk fitur Pembelian Rangbot Tambahan - menambahkan nomor seri baru ke akun
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
                existing_device = RangBotDevice.objects.get(serial_number=serial_number)
                if existing_device.member == member:
                    messages.error(request, 'Nomor seri ini sudah terdaftar di akun Anda.')
                else:
                    messages.error(request, 'Nomor seri sudah terdaftar pada akun lain.')
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
                
                messages.success(request, f'Perangkat {device.get_display_name()} berhasil ditambahkan!')
                return redirect('main:member_devices')
    
    context = {
        'page_title': 'Tambah Rangbot - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/add_device.html', context)


def member_purchase(request):
    """
    View untuk pembelian Rangbot tambahan dari dashboard member
    Membuat PurchaseOrder dengan is_reorder=True dan original_member_id=member.member_id
    Setelah diverifikasi admin, serial number baru akan otomatis ditambahkan ke member yang sama
    """
    from decimal import Decimal
    
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get pricing plans from database (only active ones)
    try:
        products_queryset = ProductInfo.objects.filter(is_active=True).order_by('package_type')
        pricing_plans_list = []
        products_dict = {}
        
        for product in products_queryset:
            features = product.get_features_list() if hasattr(product, 'get_features_list') else []
            pricing_plans_list.append({
                'name': product.name,
                'package_type': product.package_type,
                'price': f"{product.price:,.0f}".replace(',', '.'),
                'price_value': product.price,
                'description': product.description or '',
                'features': features,
                'highlight': product.package_type == 'professional',
            })
            products_dict[product.package_type] = product
    except:
        pricing_plans_list = []
        products_dict = {}
    
    # Handle form submission
    if request.method == 'POST':
        try:
            # Get form data (pre-filled with member data, but allow editing)
            customer_name = request.POST.get('name', member.full_name).strip()
            customer_email = request.POST.get('email', member.email).strip()
            customer_phone = request.POST.get('phone', member.phone).strip()
            company_name = request.POST.get('company', '').strip()
            customer_address = request.POST.get('address', '').strip()
            notes = request.POST.get('notes', '').strip()
            payment_method = request.POST.get('payment_method', '').strip()
            
            # Get package quantities
            qty_basic = int(request.POST.get('qty_basic', 0) or 0)
            qty_professional = int(request.POST.get('qty_professional', 0) or 0)
            
            # Validate
            if not customer_name or not customer_email or not customer_phone or not customer_address:
                messages.error(request, 'Mohon lengkapi semua field yang wajib diisi.')
                return redirect('main:member_purchase')
            
            if qty_basic == 0 and qty_professional == 0:
                messages.error(request, 'Mohon pilih minimal 1 paket (Basic atau Professional).')
                return redirect('main:member_purchase')
            
            # Validate payment method if provided
            valid_payment_methods = ['transfer', 'credit', 'installment', 'leasing']
            if payment_method and payment_method not in valid_payment_methods:
                messages.error(request, 'Metode pembayaran tidak valid.')
                return redirect('main:member_purchase')
            
            # Calculate total price from database
            price_basic = Decimal('0')
            price_professional = Decimal('0')
            
            if 'basic' in products_dict:
                price_basic = Decimal(str(products_dict['basic'].price))
            if 'professional' in products_dict:
                price_professional = Decimal(str(products_dict['professional'].price))
            
            total_price = (price_basic * qty_basic) + (price_professional * qty_professional)
            
            if total_price <= 0:
                messages.error(request, 'Total harga tidak valid.')
                return redirect('main:member_purchase')
            
            # Create PurchaseOrder with is_reorder=True
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
                payment_method=payment_method if payment_method else None,
                status='pending',
                is_reorder=True,  # Mark as reorder
                original_member_id=member.member_id,  # Link to existing member
            )
            
            # Create ActivityLog for new purchase order
            from .models import ActivityLog
            ActivityLog.objects.create(
                action_type='order_created',
                description=f'Pembelian tambahan: Order #{purchase_order.id} dari {customer_name} ({customer_email}) - Member ID: {member.member_id}. Total: {purchase_order.get_total_units()} unit (Basic: {qty_basic}, Pro: {qty_professional}). Total harga: Rp {total_price:,.0f}',
                performed_by=None,
                related_order=purchase_order,
                metadata={
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'member_id': member.member_id,
                    'is_reorder': True,
                    'total_units': purchase_order.get_total_units(),
                    'qty_basic': qty_basic,
                    'qty_professional': qty_professional,
                    'total_price': float(total_price),
                }
            )
            
            messages.success(request, 'Pesanan pembelian tambahan Anda telah dikirim! Tim kami akan menghubungi Anda dalam 1x24 jam untuk verifikasi. Setelah diverifikasi, perangkat baru akan otomatis ditambahkan ke akun Anda.')
            return redirect('main:member_purchase')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat mengirim pesanan: {str(e)}')
            return redirect('main:member_purchase')
    
    context = {
        'page_title': 'Pembelian Rangbot - Dashboard',
        'member': member,
        'pricing_plans': pricing_plans_list,
    }
    
    return render(request, 'dashboard/member_purchase.html', context)


def member_device_management(request, device_id):
    """
    View untuk halaman Manajemen Perangkat (detail) dengan semua fitur:
    - Kontrol Rangbot via website
    - Streaming Kamera
    - Upload Foto untuk deteksi
    - Histori Data dan Grafik Sensor
    - Riwayat Deteksi Penyakit Stroberi (CRUD)
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id, member=member)
    
    # Handle POST requests for detection CRUD
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'save_detection':
            detection_id = request.POST.get('detection_id')
            disease_detected = request.POST.get('disease_detected', '').strip()
            confidence = request.POST.get('confidence')
            location = request.POST.get('location', '').strip()
            
            if detection_id:
                # Update existing detection
                detection = get_object_or_404(DetectionHistory, id=detection_id, device=device)
                detection.disease_detected = disease_detected or None
                detection.confidence = float(confidence) if confidence else None
                detection.location = location or None
                detection.save()
                messages.success(request, 'Deteksi berhasil diperbarui.')
            else:
                # Create new detection
                DetectionHistory.objects.create(
                    device=device,
                    disease_detected=disease_detected or None,
                    confidence=float(confidence) if confidence else None,
                    location=location or None,
                    detection_type='manual',
                    image_url='',  # TODO: Handle image upload
                )
                messages.success(request, 'Deteksi berhasil ditambahkan.')
        
        elif action == 'delete_detection':
            detection_id = request.POST.get('detection_id')
            detection = get_object_or_404(DetectionHistory, id=detection_id, device=device)
            detection.delete()
            messages.success(request, 'Deteksi berhasil dihapus.')
        
        elif action == 'detect':
            # Handle image upload and detection
            # TODO: Implement YOLO detection logic
            messages.success(request, 'Deteksi berhasil dilakukan!')
        
        return redirect('main:member_device_management', device_id=device_id)
    
    # Get all detections for this device
    detections = device.detections.all().order_by('-created_at')
    
    # Get sensor data (placeholder - integrate with actual sensor data source)
    sensor_data = []  # TODO: Integrate with Firebase or sensor API
    
    context = {
        'page_title': f'Manajemen {device.get_display_name()} - Dashboard',
        'member': member,
        'device': device,
        'detections': detections,
        'sensor_data': sensor_data,
    }
    return render(request, 'dashboard/device_management.html', context)


def member_usage_guide(request):
    """
    View untuk menu Cara Penggunaan Alat
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    context = {
        'page_title': 'Cara Penggunaan Alat - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/usage_guide.html', context)


def member_daily_tips(request):
    """
    View untuk menu Tips Harian Merawat Stroberi
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    context = {
        'page_title': 'Tips Harian Merawat Stroberi - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/daily_tips.html', context)


def member_disease_classification(request):
    """
    View untuk menu Klasifikasi Umum Penyakit Stroberi
    """
    member = get_member(request)
    
    if not member:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    context = {
        'page_title': 'Klasifikasi Penyakit Stroberi - Dashboard',
        'member': member,
    }
    return render(request, 'dashboard/disease_classification.html', context)


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