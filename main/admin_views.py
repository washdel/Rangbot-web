"""
Admin views untuk sistem admin RangBot
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction, models
from .models import Admin, PurchaseOrder, Member, RangBotDevice
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
    View untuk dashboard admin
    """
    admin = get_admin(request)
    
    if not admin:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get statistics
    pending_orders = PurchaseOrder.objects.filter(status='pending').count()
    verified_orders = PurchaseOrder.objects.filter(status='verified').count()
    total_members = Member.objects.count()
    total_devices = RangBotDevice.objects.count()
    recent_orders = PurchaseOrder.objects.order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Dashboard Admin - RangBot',
        'admin': admin,
        'pending_orders': pending_orders,
        'verified_orders': verified_orders,
        'total_members': total_members,
        'total_devices': total_devices,
        'recent_orders': recent_orders,
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
        
        messages.success(request, 'Order telah ditolak.')
        return redirect('main:purchase_orders_list')
    
    return render(request, 'admin/reject_purchase.html', {
        'page_title': f'Tolak Order #{order.id} - Admin',
        'admin': admin,
        'order': order,
    })

