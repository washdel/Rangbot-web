"""
Admin views untuk sistem admin RangBot
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction, models
from .models import Admin, PurchaseOrder, Member, RangBotDevice, CustomerService, ProductInfo, FAQ, Article, ActivityLog, ForumPost, ForumComment, Notification
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
    total_orders = PurchaseOrder.objects.count()
    from django.db.models import Sum
    total_revenue = PurchaseOrder.objects.filter(status='verified').aggregate(total=Sum('total_price'))['total'] or 0
    total_members = Member.objects.count()
    registered_members = Member.objects.filter(is_registered=True).count()
    unregistered_members = Member.objects.filter(is_registered=False).count()
    total_devices = RangBotDevice.objects.count()
    active_devices = RangBotDevice.objects.filter(status='active', is_active=True).count()
    inactive_devices = RangBotDevice.objects.filter(status='inactive').count()
    total_admins = Admin.objects.filter(is_active=True).count()
    total_cs = CustomerService.objects.filter(is_active=True).count()
    
    # Recent data - ensure queries are evaluated properly
    try:
        recent_orders = list(PurchaseOrder.objects.order_by('-created_at')[:5])
    except Exception:
        recent_orders = []
    
    try:
        recent_activities = list(ActivityLog.objects.select_related('performed_by', 'related_order', 'related_member').order_by('-created_at')[:10])
    except Exception:
        recent_activities = []
    
    try:
        recent_members = list(Member.objects.order_by('-created_at')[:5])
    except Exception:
        recent_members = []
    
    # Recent notifications - use ActivityLog as system notifications for admin
    # These are notifications about purchase orders, forum activities, and user registrations
    # Show 5 most recent activity logs
    try:
        recent_notifications = list(ActivityLog.objects.select_related(
            'performed_by', 'related_order', 'related_member'
        ).filter(
            models.Q(action_type='order_created') |
            models.Q(action_type='order_verified') |
            models.Q(action_type='order_rejected') |
            models.Q(action_type='member_created') |
            models.Q(action_type='member_registered') |
            models.Q(action_type='forum_post_created') |
            models.Q(action_type='forum_comment_created')
        ).order_by('-created_at')[:5])
    except Exception:
        recent_notifications = []
    
    context = {
        'page_title': 'Dashboard Admin - RangBot',
        'admin': admin,
        'pending_orders': pending_orders,
        'verified_orders': verified_orders,
        'rejected_orders': rejected_orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
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
        'recent_notifications': recent_notifications,
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
    
    # Get orders - ensure we get all orders with proper error handling
    try:
        orders_queryset = PurchaseOrder.objects.all().order_by('-created_at')
        
        # Apply filters
        if status_filter:
            orders_queryset = orders_queryset.filter(status=status_filter)
        
        if search_query:
            orders_queryset = orders_queryset.filter(
                models.Q(customer_name__icontains=search_query) |
                models.Q(customer_email__icontains=search_query) |
                models.Q(customer_phone__icontains=search_query) |
                models.Q(member_id__icontains=search_query) |
                models.Q(id__icontains=search_query)
            )
        
        # Evaluate queryset to list to ensure data is retrieved
        orders = list(orders_queryset)
        
        # Check for each order if member exists
        # Jika member sudah dihapus, order.member_id akan tetap ada tapi member tidak ada di database
        orders_with_member_status = []
        for order in orders:
            member_exists = False
            member_is_active = False
            if order.member_id:
                try:
                    member = Member.objects.get(member_id=order.member_id)
                    member_exists = True
                    member_is_active = member.is_active
                except Member.DoesNotExist:
                    # Member sudah dihapus dari database
                    member_exists = False
                    member_is_active = False
            orders_with_member_status.append({
                'order': order,
                'member_exists': member_exists,
                'member_is_active': member_is_active
            })
    except Exception as e:
        # If there's any error, log it and return empty list
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching purchase orders: {str(e)}")
        orders_with_member_status = []
        messages.error(request, f'Terjadi kesalahan saat memuat data purchase orders: {str(e)}')
    
    # Debug: Log the count of orders
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Purchase Orders List - Total orders: {len(orders_with_member_status)}")
    
    context = {
        'page_title': 'Daftar Purchase Orders - Admin',
        'admin': admin,
        'orders_with_status': orders_with_member_status,
        'status_filter': status_filter,
        'search_query': search_query,
        'orders_count': len(orders_with_member_status),  # Add count for debugging
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
    member_exists = False
    member_is_active = False
    devices = []
    if order.member_id:
        try:
            member = Member.objects.get(member_id=order.member_id)
            member_exists = True
            member_is_active = member.is_active
            devices = RangBotDevice.objects.filter(member=member, purchase_order=order)
        except Member.DoesNotExist:
            # Member sudah dihapus dari database
            member_exists = False
            member_is_active = False
    
    context = {
        'page_title': f'Detail Order #{order.id} - Admin',
        'admin': admin,
        'order': order,
        'member': member,
        'member_exists': member_exists,
        'member_is_active': member_is_active,
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
        # Toggle is_active (freeze/activate)
        old_status = member.is_active
        member.is_active = not member.is_active
        member.save()
        
        # Create activity log
        action_type = 'member_activated' if member.is_active else 'member_deactivated'
        ActivityLog.objects.create(
            action_type=action_type,
            description=f'Member {member.member_id} ({member.full_name}) {"diaktifkan" if member.is_active else "dinonaktifkan"}',
            performed_by=admin,
            related_member=member,
        )
        
        status = 'diaktifkan' if member.is_active else 'dinonaktifkan'
        messages.success(request, f'Member {member.member_id} berhasil {status}.')
        return redirect('main:member_detail', member_id=member_id)
    
    return redirect('main:members_list')


@transaction.atomic
def member_delete(request, member_id):
    """
    View untuk menghapus member secara permanen dari database
    Data member akan benar-benar dihapus, bukan hanya dinonaktifkan
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == 'POST':
        member_name = member.full_name
        member_id_str = member.member_id
        
        # Hapus semua devices terkait
        devices = RangBotDevice.objects.filter(member=member)
        devices_count = devices.count()
        devices.delete()
        
        # Create activity log sebelum menghapus member
        ActivityLog.objects.create(
            action_type='member_deleted',
            description=f'Member {member_id_str} ({member_name}) dihapus secara permanen. {devices_count} device(s) dihapus.',
            performed_by=admin,
        )
        
        # Hapus member secara permanen
        member.delete()
        
        messages.success(request, f'Member {member_id_str} telah dihapus secara permanen. {devices_count} device(s) juga dihapus.')
        return redirect('main:members_list')
    
    return redirect('main:member_detail', member_id=member_id)


def remove_member_from_order(request, order_id):
    """
    View untuk menghapus member_id dari purchase order
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    order = get_object_or_404(PurchaseOrder, id=order_id)
    
    if request.method == 'POST':
        old_member_id = order.member_id
        
        # Update purchase order - remove member_id and reset status
        order.member_id = None
        if order.status == 'verified':
            order.status = 'pending'
            order.verified_at = None
            order.verified_by = None
        order.save()
        
        # Create activity log
        ActivityLog.objects.create(
            action_type='order_updated',
            description=f'Member ID {old_member_id} dihapus dari Order #{order.id} ({order.customer_name})',
            performed_by=admin,
            related_order=order,
        )
        
        messages.success(request, f'Member ID telah dihapus dari Order #{order.id}. Status diubah menjadi pending.')
        return redirect('main:purchase_orders_list')
    
    return redirect('main:purchase_order_detail', order_id=order_id)


@transaction.atomic
def delete_purchase_order_data(request, order_id):
    """
    View untuk menghapus data purchase order dan menonaktifkan member serta devices
    Proses final: menghapus purchase order, menonaktifkan member, dan menonaktifkan devices
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    order = get_object_or_404(PurchaseOrder, id=order_id)
    
    if request.method == 'POST':
        customer_name = order.customer_name
        member_id_str = order.member_id
        
        # Nonaktifkan member jika ada
        member = None
        if member_id_str:
            try:
                member = Member.objects.get(member_id=member_id_str)
                member.is_active = False
                member.save()
            except Member.DoesNotExist:
                pass
        
        # Nonaktifkan semua devices terkait dengan purchase order
        devices = RangBotDevice.objects.filter(purchase_order=order)
        devices_count = devices.count()
        devices.update(is_active=False)
        
        # Jika ada member, nonaktifkan semua devices member tersebut juga
        if member:
            member_devices = RangBotDevice.objects.filter(member=member)
            member_devices.update(is_active=False)
        
        # Create activity log sebelum menghapus
        ActivityLog.objects.create(
            action_type='order_deleted',
            description=f'Purchase Order #{order.id} ({customer_name}) dihapus. Member {member_id_str or "N/A"} dinonaktifkan. {devices_count} device(s) dinonaktifkan.',
            performed_by=admin,
        )
        
        # Hapus purchase order
        order.delete()
        
        messages.success(request, f'Data Purchase Order #{order.id} telah dihapus. Member {member_id_str or "N/A"} dan {devices_count} device(s) telah dinonaktifkan.')
        return redirect('main:purchase_orders_list')
    
    return redirect('main:purchase_order_detail', order_id=order_id)


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
    View untuk menampilkan daftar semua member dengan nomor seri
    Setiap member ditampilkan sebagai satu baris di tabel utama
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    member_filter = request.GET.get('member', '').strip()
    
    # Get all members that have devices - use prefetch_related for optimization
    members = Member.objects.filter(rangbot_devices__isnull=False).prefetch_related('rangbot_devices').distinct()
    
    # Apply filters
    if search_query:
        members = members.filter(
            models.Q(member_id__icontains=search_query) |
            models.Q(full_name__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(username__icontains=search_query) |
            models.Q(rangbot_devices__serial_number__icontains=search_query) |
            models.Q(rangbot_devices__device_name__icontains=search_query)
        ).distinct()
    
    if member_filter:
        members = members.filter(member_id__icontains=member_filter)
    
    # Get member statistics (device counts by type)
    members_with_stats = []
    for member in members.order_by('-created_at'):
        all_devices = member.rangbot_devices.all()
        pro_count = 0
        basic_count = 0
        total_count = all_devices.count()
        
        for device in all_devices:
            device_name_lower = (device.device_name or '').lower()
            if 'pro' in device_name_lower or 'professional' in device_name_lower:
                pro_count += 1
            else:
                basic_count += 1
        
        members_with_stats.append({
            'member': member,
            'total_devices': total_count,
            'pro_count': pro_count,
            'basic_count': basic_count,
        })
    
    context = {
        'page_title': 'Manajemen Nomor Seri - Admin',
        'admin': admin,
        'members_with_stats': members_with_stats,
        'search_query': search_query,
        'member_filter': member_filter,
    }
    
    return render(request, 'admin/serial_numbers_list.html', context)


def serial_number_detail(request, member_id):
    """
    View untuk detail semua nomor seri milik member
    Dikelompokkan berdasarkan tipe lisensi (PRO dan BASIC)
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    
    # Get all devices for this member
    all_devices = member.rangbot_devices.all().order_by('-created_at')
    
    # Separate devices by license type
    pro_devices = []
    basic_devices = []
    
    for device in all_devices:
        device_name_lower = (device.device_name or '').lower()
        if 'pro' in device_name_lower or 'professional' in device_name_lower:
            pro_devices.append(device)
        else:
            basic_devices.append(device)
    
    # Calculate totals
    pro_count = len(pro_devices)
    basic_count = len(basic_devices)
    total_devices = pro_count + basic_count
    
    context = {
        'page_title': f'Detail Nomor Seri - {member.member_id} - Admin',
        'admin': admin,
        'member': member,
        'pro_devices': pro_devices,
        'basic_devices': basic_devices,
        'pro_count': pro_count,
        'basic_count': basic_count,
        'total_devices': total_devices,
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
    
    # Get all CS - ensure we get all CS
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
    View untuk menampilkan manajemen informasi produk (FAQ, Forum, Harga)
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get all data (including inactive ones - admin can see everything)
    # FAQ: Show all, ordered by order field then created_at
    faqs = FAQ.objects.all().order_by('order', 'created_at')
    
    # Forum: Show latest 50 posts and comments
    forum_posts = ForumPost.objects.all().order_by('-created_at')[:50]
    forum_comments = ForumComment.objects.all().order_by('-created_at')[:50]
    
    # Products: Show all products - ensure we get all products
    products = ProductInfo.objects.all().order_by('package_type')
    
    # Count active items (for display info)
    active_faqs_count = FAQ.objects.filter(is_active=True).count()
    active_products_count = ProductInfo.objects.filter(is_active=True).count()
    
    context = {
        'page_title': 'Manajemen Informasi Produk - Admin',
        'admin': admin,
        'faqs': faqs,
        'forum_posts': forum_posts,
        'forum_comments': forum_comments,
        'products': products,
        'active_faqs_count': active_faqs_count,
        'active_products_count': active_products_count,
        'total_faqs_count': faqs.count(),
        'total_products_count': products.count(),
    }
    
    return render(request, 'admin/product_info_list.html', context)


def product_add(request):
    """
    View untuk menambahkan produk baru
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    if request.method == 'POST':
        package_type = request.POST.get('package_type', '').strip()
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()
        features = request.POST.get('features', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        # Validation
        if not package_type or not name or not price:
            messages.error(request, 'Tipe paket, nama, dan harga wajib diisi.')
        else:
            # Check if package_type already exists
            if ProductInfo.objects.filter(package_type=package_type).exists():
                messages.error(request, f'Paket {package_type} sudah ada. Pilih tipe paket lain atau edit paket yang sudah ada.')
            else:
                try:
                    price_decimal = float(price.replace(',', '').replace('.', ''))
                    product = ProductInfo.objects.create(
                        package_type=package_type,
                        name=name,
                        price=price_decimal,
                        description=description or None,
                        features=features or None,
                        is_active=is_active,
                        updated_by=admin
                    )
                    messages.success(request, 'Produk berhasil ditambahkan.')
                    return redirect('main:product_info_list')
                except ValueError:
                    messages.error(request, 'Format harga tidak valid.')
    
    context = {
        'page_title': 'Tambah Produk - Admin',
        'admin': admin,
    }
    
    return render(request, 'admin/product_add.html', context)


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
                return redirect('main:product_info_list')
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
                return redirect('main:product_info_list')
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
    
    # Get logs with related objects
    logs = ActivityLog.objects.select_related('performed_by', 'related_order', 'related_member', 'related_device').all()
    
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


# ==================== FORUM MANAGEMENT ====================

def forum_post_delete(request, post_id):
    """
    View untuk menghapus postingan forum
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    post = get_object_or_404(ForumPost, id=post_id)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Postingan "{post_title}" berhasil dihapus.')
        return redirect('main:product_info_list')
    
    # If GET request, show confirmation via POST redirect
    # For now, just redirect to product_info_list with a message
    messages.warning(request, f'Konfirmasi penghapusan postingan: {post.title}')
    return redirect('main:product_info_list')


def forum_comment_delete(request, comment_id):
    """
    View untuk menghapus komentar forum
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    comment = get_object_or_404(ForumComment, id=comment_id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Komentar berhasil dihapus.')
        return redirect('main:product_info_list')
    
    # Simple confirmation - redirect to product_info_list
    messages.warning(request, 'Silakan konfirmasi penghapusan komentar.')
    return redirect('main:product_info_list')


# ==================== NOTIFICATIONS MANAGEMENT ====================

def admin_notifications_list(request):
    """
    View untuk menampilkan daftar semua notifikasi member di admin dashboard
    """
    admin = get_admin(request)
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    notification_type_filter = request.GET.get('notification_type', '')
    is_read_filter = request.GET.get('is_read', '')
    member_filter = request.GET.get('member', '').strip()
    
    # Get all notifications
    notifications = Notification.objects.select_related('member').all()
    
    # Apply filters
    if search_query:
        notifications = notifications.filter(
            models.Q(title__icontains=search_query) |
            models.Q(message__icontains=search_query) |
            models.Q(member__member_id__icontains=search_query) |
            models.Q(member__full_name__icontains=search_query)
        )
    
    if notification_type_filter:
        notifications = notifications.filter(notification_type=notification_type_filter)
    
    if is_read_filter == 'yes':
        notifications = notifications.filter(is_read=True)
    elif is_read_filter == 'no':
        notifications = notifications.filter(is_read=False)
    
    if member_filter:
        notifications = notifications.filter(
            models.Q(member__member_id__icontains=member_filter) |
            models.Q(member__full_name__icontains=member_filter)
        )
    
    notifications = notifications.order_by('-created_at')
    
    # Get statistics
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    read_notifications = Notification.objects.filter(is_read=True).count()
    
    context = {
        'page_title': 'Manajemen Notifikasi - Admin',
        'admin': admin,
        'notifications': notifications,
        'search_query': search_query,
        'notification_type_filter': notification_type_filter,
        'is_read_filter': is_read_filter,
        'member_filter': member_filter,
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'notification_types': Notification.NOTIFICATION_TYPES,
    }
    
    return render(request, 'admin/notifications_list.html', context)

