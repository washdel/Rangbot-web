"""
Admin views untuk sistem admin RangBot
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction, models
from .models import Admin, PurchaseOrder, Member, RangBotDevice, CustomerService, ProductInfo, FAQ, Article, ActivityLog
from .utils import generate_member_id, generate_serial_number, get_next_serial_sequence
from django.contrib.auth.hashers import make_password


def get_admin(request):
    """Helper function untuk mendapatkan admin dari session"""
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            return Admin.objects.get(id=admin_id, is_active=True)
        except Admin.DoesNotExist:
            return None
    return None


# admin_login function removed - now using unified login at /login/


def admin_logout(request):
    """
    View untuk logout admin
    """
    request.session.flush()
    messages.success(request, 'Anda telah logout.')
    return redirect('main:login')


def admin_dashboard(request):
    """
    View untuk dashboard admin - Pusat kendali utama sistem
    """
    admin = get_admin(request)
    
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get statistics
    pending_orders = PurchaseOrder.objects.filter(status='pending').count()
    verified_orders = PurchaseOrder.objects.filter(status='verified').count()
    rejected_orders = PurchaseOrder.objects.filter(status='rejected').count()
    total_members = Member.objects.count()
    registered_members = Member.objects.filter(is_registered=True).count()
    unregistered_members = Member.objects.filter(is_registered=False).count()
    total_devices = RangBotDevice.objects.count()
    active_devices = RangBotDevice.objects.filter(status='active', is_active=True).count()
    inactive_devices = RangBotDevice.objects.filter(status='inactive').count()
    total_admins = Admin.objects.filter(is_active=True).count()
    total_cs = CustomerService.objects.filter(is_active=True).count()
    
    # Recent data
    recent_orders = PurchaseOrder.objects.order_by('-created_at')[:5]
    try:
        recent_activities = ActivityLog.objects.order_by('-created_at')[:10]
    except Exception:
        recent_activities = []
    recent_members = Member.objects.order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Dashboard Admin - RangBot',
        'admin': admin,
        'pending_orders': pending_orders,
        'verified_orders': verified_orders,
        'rejected_orders': rejected_orders,
        'total_members': total_members,
        'registered_members': registered_members,
        'unregistered_members': unregistered_members,
        'total_devices': total_devices,
        'active_devices': active_devices,
        'inactive_devices': inactive_devices,
        'total_admins': total_admins,
        'total_cs': total_cs,
        'recent_orders': recent_orders,
        'recent_activities': recent_activities,
        'recent_members': recent_members,
    }
    
    return render(request, 'admin/dashboard.html', context)


def purchase_orders_list(request):
    """
    View untuk menampilkan daftar purchase orders
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '').strip()
    
    # Get orders
    orders = PurchaseOrder.objects.all()
    
    # Apply filters
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if search_query:
        orders = orders.filter(
            models.Q(customer_name__icontains=search_query) |
            models.Q(customer_email__icontains=search_query) |
            models.Q(customer_phone__icontains=search_query) |
            models.Q(member_id__icontains=search_query)
        )
    
    orders = orders.order_by('-created_at')
    
    context = {
        'page_title': 'Daftar Purchase Orders - Admin',
        'admin': admin,
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/purchase_orders.html', context)


def purchase_order_detail(request, order_id):
    """
    View untuk menampilkan detail purchase order
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    order = get_object_or_404(PurchaseOrder, id=order_id)
    
    # Get related data
    member = None
    devices = []
    if order.member_id:
        try:
            member = Member.objects.get(member_id=order.member_id)
            devices = RangBotDevice.objects.filter(member=member, purchase_order=order)
        except Member.DoesNotExist:
            pass
    
    context = {
        'page_title': f'Detail Order #{order.id} - Admin',
        'admin': admin,
        'order': order,
        'member': member,
        'devices': devices,
    }
    
    return render(request, 'admin/purchase_order_detail.html', context)


@transaction.atomic
def verify_purchase(request, order_id):
    """
    View untuk verifikasi purchase order
    Generate Member ID dan Serial Numbers
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    order = get_object_or_404(PurchaseOrder, id=order_id)
    
    if order.status != 'pending':
        messages.error(request, 'Order ini sudah diverifikasi atau ditolak.')
        return redirect('main:purchase_order_detail', order_id=order_id)
    
    try:
        # Check if this is a reorder
        is_reorder = False
        original_member_id = None
        
        if order.is_reorder and order.original_member_id:
            # This is a reorder - use existing member
            is_reorder = True
            original_member_id = order.original_member_id
            try:
                member = Member.objects.get(member_id=original_member_id)
            except Member.DoesNotExist:
                messages.error(request, f'Member ID {original_member_id} tidak ditemukan untuk pembelian ulang.')
                return redirect('main:purchase_order_detail', order_id=order_id)
        else:
            # New purchase - generate Member ID
            member_id = generate_member_id()
            
            # Check if Member ID already exists
            if Member.objects.filter(member_id=member_id).exists():
                # Regenerate if exists (shouldn't happen, but just in case)
                member_id = generate_member_id()
            
            # Create Member record (belum registrasi)
            member = Member.objects.create(
                member_id=member_id,
                full_name=order.customer_name,
                email=order.customer_email,
                phone=order.customer_phone,
                purchase_order=order,
                is_registered=False
            )
            
            order.member_id = member_id
        
        # Generate Serial Numbers
        total_units = order.get_total_units()
        if total_units == 0:
            messages.error(request, 'Jumlah unit tidak valid.')
            return redirect('main:purchase_order_detail', order_id=order_id)
        
        # Get starting sequence
        start_sequence = get_next_serial_sequence()
        
        # Generate devices
        devices_created = []
        sequence = start_sequence
        
        # Basic packages
        for i in range(order.qty_basic):
            serial_number = generate_serial_number(sequence)
            device = RangBotDevice.objects.create(
                serial_number=serial_number,
                member=member,
                purchase_order=order,
                device_name=f'RangBot Basic {i+1}',
                status='offline',
                is_active=True
            )
            devices_created.append(device)
            sequence += 1
        
        # Professional packages
        for i in range(order.qty_professional):
            serial_number = generate_serial_number(sequence)
            device = RangBotDevice.objects.create(
                serial_number=serial_number,
                member=member,
                purchase_order=order,
                device_name=f'RangBot Pro {i+1}',
                status='offline',
                is_active=True
            )
            devices_created.append(device)
            sequence += 1
        
        # Update order status
        order.status = 'verified'
        order.verified_at = timezone.now()
        order.verified_by = admin
        if is_reorder:
            order.original_member_id = original_member_id
        order.save()
        
        # Create activity log
        ActivityLog.objects.create(
            action_type='order_verified',
            description=f'Order #{order.id} diverifikasi. Member ID: {order.member_id}, {len(devices_created)} device(s) dibuat.',
            performed_by=admin,
            related_order=order,
            related_member=member,
            metadata={
                'member_id': order.member_id,
                'devices_count': len(devices_created),
                'is_reorder': is_reorder,
            }
        )
        
        # Log member creation if new
        if not is_reorder:
            ActivityLog.objects.create(
                action_type='member_created',
                description=f'Member ID {order.member_id} dibuat untuk {order.customer_name}',
                performed_by=admin,
                related_order=order,
                related_member=member,
            )
        
        # Log serial number creation
        for device in devices_created:
            ActivityLog.objects.create(
                action_type='serial_created',
                description=f'Nomor seri {device.serial_number} dibuat untuk Member {order.member_id}',
                performed_by=admin,
                related_order=order,
                related_member=member,
                related_device=device,
            )
        
        messages.success(request, f'Order berhasil diverifikasi! Member ID: {order.member_id}, {len(devices_created)} device(s) dibuat.')
        return redirect('main:purchase_order_detail', order_id=order_id)
        
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan saat verifikasi: {str(e)}')
        return redirect('main:purchase_order_detail', order_id=order_id)


def reject_purchase(request, order_id):
    """
    View untuk menolak purchase order
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    order = get_object_or_404(PurchaseOrder, id=order_id)
    
    if order.status != 'pending':
        messages.error(request, 'Order ini sudah diverifikasi atau ditolak.')
        return redirect('main:purchase_order_detail', order_id=order_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        order.status = 'rejected'
        order.verified_by = admin
        order.verified_at = timezone.now()
        if reason:
            # Store rejection reason in notes
            order.notes = f"[DITOLAK] {reason}\n\n{order.notes or ''}"
        order.save()
        
        # Create activity log
        ActivityLog.objects.create(
            action_type='order_rejected',
            description=f'Order #{order.id} ditolak. Alasan: {reason or "Tidak disebutkan"}',
            performed_by=admin,
            related_order=order,
            metadata={'reason': reason}
        )
        
        messages.success(request, 'Order telah ditolak.')
        return redirect('main:purchase_orders_list')
    
    return render(request, 'admin/reject_purchase.html', {
        'page_title': f'Tolak Order #{order.id} - Admin',
        'admin': admin,
        'order': order,
    })


# ==================== MEMBER MANAGEMENT ====================

def members_list(request):
    """
    View untuk menampilkan daftar semua member
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    registered_filter = request.GET.get('registered', '')
    
    # Get members
    members = Member.objects.all()
    
    # Apply filters
    if search_query:
        members = members.filter(
            models.Q(member_id__icontains=search_query) |
            models.Q(username__icontains=search_query) |
            models.Q(full_name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    if registered_filter == 'yes':
        members = members.filter(is_registered=True)
    elif registered_filter == 'no':
        members = members.filter(is_registered=False)
    
    members = members.order_by('-created_at')
    
    context = {
        'page_title': 'Manajemen Member - Admin',
        'admin': admin,
        'members': members,
        'search_query': search_query,
        'registered_filter': registered_filter,
    }
    
    return render(request, 'admin/members_list.html', context)


def member_detail(request, member_id):
    """
    View untuk menampilkan detail member
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    devices = member.rangbot_devices.all()
    purchase_orders = PurchaseOrder.objects.filter(member_id=member_id)
    
    context = {
        'page_title': f'Detail Member {member.member_id} - Admin',
        'admin': admin,
        'member': member,
        'devices': devices,
        'purchase_orders': purchase_orders,
    }
    
    return render(request, 'admin/member_detail.html', context)


def member_toggle_active(request, member_id):
    """
    View untuk freeze/activate member
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == 'POST':
        # Toggle is_registered (freeze/activate)
        old_status = member.is_registered
        member.is_registered = not member.is_registered
        member.save()
        
        # Create activity log
        action_type = 'member_activated' if member.is_registered else 'member_deactivated'
        ActivityLog.objects.create(
            action_type=action_type,
            description=f'Member {member.member_id} ({member.full_name}) {"diaktifkan" if member.is_registered else "dinonaktifkan"}',
            performed_by=admin,
            related_member=member,
        )
        
        status = 'diaktifkan' if member.is_registered else 'dibekukan'
        messages.success(request, f'Member {member.member_id} berhasil {status}.')
        return redirect('main:member_detail', member_id=member_id)
    
    return redirect('main:members_list')


def member_edit(request, member_id):
    """
    View untuk edit data member
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        username = request.POST.get('username', '').strip()
        
        # Validation
        if not full_name or not email:
            messages.error(request, 'Nama lengkap dan email wajib diisi.')
        else:
            # Check if username or email already used by another member
            if username and Member.objects.filter(username=username).exclude(member_id=member_id).exists():
                messages.error(request, 'Username sudah digunakan oleh member lain.')
            elif Member.objects.filter(email=email).exclude(member_id=member_id).exists():
                messages.error(request, 'Email sudah digunakan oleh member lain.')
            else:
                member.full_name = full_name
                member.email = email
                member.phone = phone or None
                if username:
                    member.username = username
                member.save()
                
                # Create activity log
                ActivityLog.objects.create(
                    action_type='member_updated',
                    description=f'Data member {member.member_id} diperbarui',
                    performed_by=admin,
                    related_member=member,
                )
                
                messages.success(request, 'Data member berhasil diperbarui.')
                return redirect('main:member_detail', member_id=member_id)
    
    context = {
        'page_title': f'Edit Member {member.member_id} - Admin',
        'admin': admin,
        'member': member,
    }
    
    return render(request, 'admin/member_edit.html', context)


# ==================== SERIAL NUMBER MANAGEMENT ====================

def serial_numbers_list(request):
    """
    View untuk menampilkan daftar semua nomor seri
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')
    member_filter = request.GET.get('member', '').strip()
    
    # Get devices
    devices = RangBotDevice.objects.all()
    
    # Apply filters
    if search_query:
        devices = devices.filter(
            models.Q(serial_number__icontains=search_query) |
            models.Q(device_name__icontains=search_query) |
            models.Q(member__member_id__icontains=search_query) |
            models.Q(member__username__icontains=search_query)
        )
    
    if status_filter:
        devices = devices.filter(status=status_filter)
    
    if member_filter:
        devices = devices.filter(member__member_id__icontains=member_filter)
    
    devices = devices.order_by('-created_at')
    
    context = {
        'page_title': 'Manajemen Nomor Seri - Admin',
        'admin': admin,
        'devices': devices,
        'search_query': search_query,
        'status_filter': status_filter,
        'member_filter': member_filter,
    }
    
    return render(request, 'admin/serial_numbers_list.html', context)


def serial_number_detail(request, device_id):
    """
    View untuk detail nomor seri
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    device = get_object_or_404(RangBotDevice, id=device_id)
    
    context = {
        'page_title': f'Detail Nomor Seri {device.serial_number} - Admin',
        'admin': admin,
        'device': device,
    }
    
    return render(request, 'admin/serial_number_detail.html', context)


# ==================== CUSTOMER SERVICE MANAGEMENT ====================

def cs_list(request):
    """
    View untuk menampilkan daftar Customer Service
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    search_query = request.GET.get('search', '').strip()
    
    cs_list = CustomerService.objects.all()
    
    if search_query:
        cs_list = cs_list.filter(
            models.Q(username__icontains=search_query) |
            models.Q(full_name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    cs_list = cs_list.order_by('-created_at')
    
    context = {
        'page_title': 'Manajemen Customer Service - Admin',
        'admin': admin,
        'cs_list': cs_list,
        'search_query': search_query,
    }
    
    return render(request, 'admin/cs_list.html', context)


def cs_add(request):
    """
    View untuk menambahkan Customer Service baru
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validation
        if not all([username, email, full_name, password]):
            messages.error(request, 'Harap lengkapi semua field.')
        elif len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
        elif CustomerService.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
        elif CustomerService.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar.')
        else:
            cs = CustomerService.objects.create(
                username=username,
                email=email,
                full_name=full_name,
                password=make_password(password),
                is_active=True
            )
            
            # Create activity log
            ActivityLog.objects.create(
                action_type='cs_created',
                description=f'Customer Service {cs.full_name} ({cs.username}) berhasil ditambahkan',
                performed_by=admin,
                metadata={'cs_id': cs.id, 'username': cs.username}
            )
            
            messages.success(request, f'Customer Service {cs.full_name} berhasil ditambahkan.')
            return redirect('main:cs_list')
    
    context = {
        'page_title': 'Tambah Customer Service - Admin',
        'admin': admin,
    }
    
    return render(request, 'admin/cs_add.html', context)


def cs_delete(request, cs_id):
    """
    View untuk menghapus Customer Service
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    cs = get_object_or_404(CustomerService, id=cs_id)
    
    if request.method == 'POST':
        cs_name = cs.full_name
        cs_username = cs.username
        
        # Create activity log before deletion
        ActivityLog.objects.create(
            action_type='cs_deleted',
            description=f'Customer Service {cs_name} ({cs_username}) dihapus',
            performed_by=admin,
            metadata={'cs_username': cs_username}
        )
        
        cs.delete()
        messages.success(request, f'Customer Service {cs_name} berhasil dihapus.')
        return redirect('main:cs_list')
    
    context = {
        'page_title': f'Hapus Customer Service - Admin',
        'admin': admin,
        'cs': cs,
    }
    
    return render(request, 'admin/cs_delete.html', context)


# ==================== PRODUCT & LANDING PAGE MANAGEMENT ====================

def product_info_list(request):
    """
    View untuk menampilkan daftar informasi produk
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    products = ProductInfo.objects.all()
    
    context = {
        'page_title': 'Manajemen Produk - Admin',
        'admin': admin,
        'products': products,
    }
    
    return render(request, 'admin/product_info_list.html', context)


def product_info_edit(request, product_id):
    """
    View untuk edit informasi produk
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    product = get_object_or_404(ProductInfo, id=product_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()
        features = request.POST.get('features', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        # Validation
        if not name or not price:
            messages.error(request, 'Nama dan harga wajib diisi.')
        else:
            try:
                price_decimal = float(price.replace(',', '').replace('.', ''))
                product.name = name
                product.price = price_decimal
                product.description = description or None
                product.features = features or None
                product.is_active = is_active
                product.updated_by = admin
                product.save()
                
                messages.success(request, 'Informasi produk berhasil diperbarui.')
                return redirect('main:product_info_list')
            except ValueError:
                messages.error(request, 'Format harga tidak valid.')
    
    context = {
        'page_title': f'Edit Produk {product.name} - Admin',
        'admin': admin,
        'product': product,
    }
    
    return render(request, 'admin/product_info_edit.html', context)


def faq_list(request):
    """
    View untuk menampilkan daftar FAQ
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    faqs = FAQ.objects.all()
    
    context = {
        'page_title': 'Manajemen FAQ - Admin',
        'admin': admin,
        'faqs': faqs,
    }
    
    return render(request, 'admin/faq_list.html', context)


def faq_add(request):
    """
    View untuk menambahkan FAQ baru
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        answer = request.POST.get('answer', '').strip()
        order = request.POST.get('order', '0').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        if not question or not answer:
            messages.error(request, 'Pertanyaan dan jawaban wajib diisi.')
        else:
            try:
                order_int = int(order) if order else 0
                faq = FAQ.objects.create(
                    question=question,
                    answer=answer,
                    order=order_int,
                    is_active=is_active
                )
                messages.success(request, 'FAQ berhasil ditambahkan.')
                return redirect('main:faq_list')
            except ValueError:
                messages.error(request, 'Format urutan tidak valid.')
    
    context = {
        'page_title': 'Tambah FAQ - Admin',
        'admin': admin,
    }
    
    return render(request, 'admin/faq_add.html', context)


def faq_edit(request, faq_id):
    """
    View untuk edit FAQ
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        answer = request.POST.get('answer', '').strip()
        order = request.POST.get('order', '0').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        if not question or not answer:
            messages.error(request, 'Pertanyaan dan jawaban wajib diisi.')
        else:
            try:
                order_int = int(order) if order else 0
                faq.question = question
                faq.answer = answer
                faq.order = order_int
                faq.is_active = is_active
                faq.save()
                
                messages.success(request, 'FAQ berhasil diperbarui.')
                return redirect('main:faq_list')
            except ValueError:
                messages.error(request, 'Format urutan tidak valid.')
    
    context = {
        'page_title': 'Edit FAQ - Admin',
        'admin': admin,
        'faq': faq,
    }
    
    return render(request, 'admin/faq_edit.html', context)


def faq_delete(request, faq_id):
    """
    View untuk menghapus FAQ
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ berhasil dihapus.')
        return redirect('main:faq_list')
    
    context = {
        'page_title': 'Hapus FAQ - Admin',
        'admin': admin,
        'faq': faq,
    }
    
    return render(request, 'admin/faq_delete.html', context)


def articles_list(request):
    """
    View untuk menampilkan daftar artikel
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    articles = Article.objects.all()
    
    context = {
        'page_title': 'Manajemen Artikel - Admin',
        'admin': admin,
        'articles': articles,
    }
    
    return render(request, 'admin/articles_list.html', context)


def article_add(request):
    """
    View untuk menambahkan artikel baru
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        
        if not title or not content:
            messages.error(request, 'Judul dan isi artikel wajib diisi.')
        else:
            article = Article.objects.create(
                title=title,
                content=content,
                image_url=image_url or None,
                is_published=is_published,
                created_by=admin
            )
            messages.success(request, 'Artikel berhasil ditambahkan.')
            return redirect('main:articles_list')
    
    context = {
        'page_title': 'Tambah Artikel - Admin',
        'admin': admin,
    }
    
    return render(request, 'admin/article_add.html', context)


def article_edit(request, article_id):
    """
    View untuk edit artikel
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        
        if not title or not content:
            messages.error(request, 'Judul dan isi artikel wajib diisi.')
        else:
            article.title = title
            article.content = content
            article.image_url = image_url or None
            article.is_published = is_published
            article.save()
            
            messages.success(request, 'Artikel berhasil diperbarui.')
            return redirect('main:articles_list')
    
    context = {
        'page_title': 'Edit Artikel - Admin',
        'admin': admin,
        'article': article,
    }
    
    return render(request, 'admin/article_edit.html', context)


def article_delete(request, article_id):
    """
    View untuk menghapus artikel
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artikel berhasil dihapus.')
        return redirect('main:articles_list')
    
    context = {
        'page_title': 'Hapus Artikel - Admin',
        'admin': admin,
        'article': article,
    }
    
    return render(request, 'admin/article_delete.html', context)


# ==================== ADMIN MANAGEMENT ====================

def admin_list(request):
    """
    View untuk menampilkan daftar Admin
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    search_query = request.GET.get('search', '').strip()
    
    admin_list = Admin.objects.all()
    
    if search_query:
        admin_list = admin_list.filter(
            models.Q(username__icontains=search_query) |
            models.Q(full_name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    admin_list = admin_list.order_by('-created_at')
    
    context = {
        'page_title': 'Manajemen Admin - Admin',
        'admin': admin,
        'admin_list': admin_list,
        'search_query': search_query,
    }
    
    return render(request, 'admin/admin_list.html', context)


def admin_add(request):
    """
    View untuk menambahkan Admin baru
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validation
        if not all([username, email, full_name, password]):
            messages.error(request, 'Harap lengkapi semua field.')
        elif len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
        elif Admin.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
        elif Admin.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar.')
        else:
            new_admin = Admin.objects.create(
                username=username,
                email=email,
                full_name=full_name,
                password=make_password(password),
                is_active=True
            )
            
            # Create activity log
            ActivityLog.objects.create(
                action_type='admin_created',
                description=f'Admin {new_admin.full_name} ({new_admin.username}) berhasil ditambahkan',
                performed_by=admin,
                metadata={'admin_id': new_admin.id, 'username': new_admin.username}
            )
            
            messages.success(request, f'Admin {new_admin.full_name} berhasil ditambahkan.')
            return redirect('main:admin_list')
    
    context = {
        'page_title': 'Tambah Admin - Admin',
        'admin': admin,
    }
    
    return render(request, 'admin/admin_add.html', context)


def admin_toggle_active(request, admin_id):
    """
    View untuk mengaktifkan/nonaktifkan Admin
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    target_admin = get_object_or_404(Admin, id=admin_id)
    
    # Prevent self-deactivation
    if target_admin.id == admin.id:
        messages.error(request, 'Anda tidak dapat menonaktifkan akun sendiri.')
        return redirect('main:admin_list')
    
    if request.method == 'POST':
        target_admin.is_active = not target_admin.is_active
        target_admin.save()
        
        # Create activity log
        action_type = 'admin_deactivated' if not target_admin.is_active else 'admin_created'
        ActivityLog.objects.create(
            action_type=action_type,
            description=f'Admin {target_admin.full_name} ({target_admin.username}) {"dinonaktifkan" if not target_admin.is_active else "diaktifkan"}',
            performed_by=admin,
            metadata={'admin_id': target_admin.id, 'username': target_admin.username}
        )
        
        status = 'dinonaktifkan' if not target_admin.is_active else 'diaktifkan'
        messages.success(request, f'Admin {target_admin.full_name} berhasil {status}.')
        return redirect('main:admin_list')
    
    return redirect('main:admin_list')


# ==================== ACTIVITY LOG ====================

def activity_log_list(request):
    """
    View untuk menampilkan riwayat aktivitas sistem
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    action_filter = request.GET.get('action_type', '')
    search_query = request.GET.get('search', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    
    # Get logs
    logs = ActivityLog.objects.all()
    
    # Apply filters
    if action_filter:
        logs = logs.filter(action_type=action_filter)
    
    if search_query:
        logs = logs.filter(
            models.Q(description__icontains=search_query) |
            models.Q(performed_by__full_name__icontains=search_query) |
            models.Q(performed_by__username__icontains=search_query)
        )
    
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            logs = logs.filter(created_at__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            from datetime import datetime
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            logs = logs.filter(created_at__lte=date_to_obj)
        except ValueError:
            pass
    
    logs = logs.order_by('-created_at')
    
    context = {
        'page_title': 'Riwayat Aktivitas Sistem - Admin',
        'admin': admin,
        'logs': logs,
        'action_filter': action_filter,
        'search_query': search_query,
        'date_from': date_from,
        'date_to': date_to,
        'action_types': ActivityLog.ACTION_TYPES,
    }
    
    return render(request, 'admin/activity_log_list.html', context)


def activity_log_delete(request, log_id):
    """
    View untuk menghapus log aktivitas
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    log = get_object_or_404(ActivityLog, id=log_id)
    
    if request.method == 'POST':
        log_description = log.description[:50] + ('...' if len(log.description) > 50 else '')
        log.delete()
        messages.success(request, f'Log aktivitas berhasil dihapus: {log_description}')
        return redirect('main:activity_log_list')
    
    # If GET request, redirect to list (should not happen, but safety)
    return redirect('main:activity_log_list')


def activity_log_delete_all(request):
    """
    View untuk menghapus semua log aktivitas
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        count = ActivityLog.objects.count()
        ActivityLog.objects.all().delete()
        messages.success(request, f'Semua log aktivitas ({count} log) berhasil dihapus.')
        return redirect('main:activity_log_list')
    
    # If GET request, redirect to list
    return redirect('main:activity_log_list')

