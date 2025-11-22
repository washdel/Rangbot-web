"""
Views untuk Dashboard Customer Service (CS)
CS fokus pada layanan, interaksi, dan manajemen informasi forum & FAQ
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from urllib.parse import urlencode
from django.db import models
from .models import (
    CustomerService, ContactMessage, FAQ, ForumPost, ForumComment,
    Member, RangBotDevice, ProductInfo, ActivityLog
)


def get_cs(request):
    """Helper function untuk mendapatkan CS dari session"""
    cs_id = request.session.get('cs_id')
    if cs_id:
        try:
            return CustomerService.objects.get(id=cs_id, is_active=True)
        except CustomerService.DoesNotExist:
            return None
    return None


def get_cs_base_context(cs):
    """Helper function untuk mendapatkan context dasar yang digunakan di semua template CS"""
    return {
        'cs': cs,
        'new_messages_count': ContactMessage.objects.filter(status='new').count(),
    }


def cs_logout(request):
    """View untuk logout CS"""
    request.session.flush()
    messages.success(request, 'Anda telah logout.')
    return redirect('main:login')


def cs_dashboard(request):
    """
    Beranda Dashboard CS
    Menampilkan informasi ringkas yang relevan bagi CS
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get statistics
    new_messages = ContactMessage.objects.filter(status='new').count()
    unread_messages = ContactMessage.objects.filter(status__in=['new', 'read']).count()
    total_messages = ContactMessage.objects.count()
    archived_messages = ContactMessage.objects.filter(status='archived').count()
    
    # Recent messages (last 5)
    recent_messages = ContactMessage.objects.filter(status__in=['new', 'read']).order_by('-created_at')[:5]
    
    # Forum statistics
    new_forum_posts = ForumPost.objects.filter(created_at__gte=timezone.now().replace(hour=0, minute=0, second=0)).count()
    recent_forum_posts = ForumPost.objects.order_by('-created_at')[:5]
    recent_forum_comments = ForumComment.objects.order_by('-created_at')[:5]
    
    # Member statistics (for info)
    total_members = Member.objects.filter(is_active=True).count()
    total_devices = RangBotDevice.objects.filter(is_active=True).count()
    
    # Recent activity logs (last 5) - same as admin dashboard
    recent_notifications = list(ActivityLog.objects.select_related(
        'performed_by', 'related_order', 'related_member'
    ).order_by('-created_at')[:5])
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Dashboard Customer Service - RangBot',
        'new_messages': new_messages,
        'unread_messages': unread_messages,
        'total_messages': total_messages,
        'archived_messages': archived_messages,
        'recent_messages': recent_messages,
        'new_forum_posts': new_forum_posts,
        'recent_forum_posts': recent_forum_posts,
        'recent_forum_comments': recent_forum_comments,
        'total_members': total_members,
        'total_devices': total_devices,
        'recent_notifications': recent_notifications,
    })
    
    return render(request, 'cs/dashboard.html', context)


def cs_messages(request):
    """
    Menu Hubungi Customer Service
    Melihat dan membalas pesan dari pengguna
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Handle POST actions
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        action = request.POST.get('action')
        
        try:
            message = ContactMessage.objects.get(id=message_id)
            
            if action == 'mark_read':
                message.status = 'read'
                message.save()
                messages.success(request, f'Pesan dari {message.name} telah ditandai sebagai sudah dibaca.')
            
            elif action == 'reply':
                reply_message = request.POST.get('reply_message', '').strip()
                if reply_message:
                    message.status = 'replied'
                    message.replied_by = cs
                    message.replied_at = timezone.now()
                    message.reply_message = reply_message
                    message.save()
                    
                    # Send email to customer
                    try:
                        from django.core.mail import send_mail, EmailMessage
                        from django.conf import settings
                        from django.template.loader import render_to_string
                        
                        email_subject = f'Re: {message.subject}'
                        
                        # Create email body
                        email_body_plain = f"""Halo {message.name},

Terima kasih telah menghubungi Customer Service RangBot.

Berikut adalah balasan untuk pertanyaan/pesan Anda:

---
Pesan Asli:
Subjek: {message.subject}
Pesan: {message.message}
---

Balasan:
{reply_message}

Jika Anda memiliki pertanyaan lebih lanjut, jangan ragu untuk menghubungi kami kembali melalui:
- Email: {settings.DEFAULT_FROM_EMAIL}
- Website: http://localhost:8000/hubungi-support/

Salam,
{cs.full_name}
Customer Service RangBot

---
Email ini dikirim sebagai balasan untuk pesan Anda pada {message.created_at.strftime('%d %B %Y, %H:%M WIB')}.
"""
                        
                        # Try to send email
                        send_mail(
                            subject=email_subject,
                            message=email_body_plain,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[message.email],
                            fail_silently=False,
                        )
                        messages.success(request, f'Balasan untuk {message.name} telah dikirim ke email {message.email}.')
                    except Exception as e:
                        # If email fails, still save the reply but show warning
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Failed to send email: {str(e)}")
                        messages.warning(request, f'Balasan telah disimpan, namun gagal mengirim email ke {message.email}. Error: {str(e)}')
                else:
                    messages.error(request, 'Balasan tidak boleh kosong.')
            
            elif action == 'archive':
                message.status = 'archived'
                message.save()
                messages.success(request, f'Pesan dari {message.name} telah diarsipkan.')
            
            elif action == 'unarchive':
                message.status = 'read'
                message.save()
                messages.success(request, f'Pesan dari {message.name} telah dikembalikan dari arsip.')
            
            elif action == 'delete':
                message_name = message.name
                message.delete()
                messages.success(request, f'Pesan dari {message_name} telah dihapus.')
        
        except ContactMessage.DoesNotExist:
            messages.error(request, 'Pesan tidak ditemukan.')
        
        # Redirect to maintain filters
        from django.urls import reverse
        
        redirect_url = reverse('main:cs_messages')
        params = []
        if request.GET.get('status'):
            params.append(f"status={request.GET.get('status')}")
        if request.GET.get('search'):
            params.append(f"search={request.GET.get('search')}")
        if request.GET.get('page'):
            params.append(f"page={request.GET.get('page')}")
        if params:
            redirect_url += '?' + '&'.join(params)
        
        return redirect(redirect_url)
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '').strip()
    
    # Get messages
    messages_list = ContactMessage.objects.all()
    
    if status_filter:
        messages_list = messages_list.filter(status=status_filter)
    
    if search_query:
        messages_list = messages_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    messages_list = messages_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    new_count = ContactMessage.objects.filter(status='new').count()
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Pesan Customer Service - CS Dashboard',
        'messages': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    })
    
    return render(request, 'cs/messages.html', context)


def cs_faq(request):
    """
    Menu FAQ Management
    CS dapat menambah, mengedit, dan menghapus FAQ
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get FAQs ordered by order field then created_at
    faqs = FAQ.objects.all().order_by('order', 'created_at')
    active_faqs_count = FAQ.objects.filter(is_active=True).count()
    total_faqs_count = faqs.count()
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'FAQ Management - CS Dashboard',
        'faqs': faqs,
        'active_faqs_count': active_faqs_count,
        'total_faqs_count': total_faqs_count,
    })
    
    return render(request, 'cs/faq.html', context)


def cs_faq_add(request):
    """
    View untuk menambahkan FAQ baru (CS)
    """
    cs = get_cs(request)
    if not cs:
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
                return redirect('main:cs_faq')
            except ValueError:
                messages.error(request, 'Format urutan tidak valid.')
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Tambah FAQ - CS Dashboard',
    })
    
    return render(request, 'cs/faq_add.html', context)


def cs_faq_edit(request, faq_id):
    """
    View untuk edit FAQ (CS)
    """
    cs = get_cs(request)
    if not cs:
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
                return redirect('main:cs_faq')
            except ValueError:
                messages.error(request, 'Format urutan tidak valid.')
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Edit FAQ - CS Dashboard',
        'faq': faq,
    })
    
    return render(request, 'cs/faq_edit.html', context)


def cs_faq_delete(request, faq_id):
    """
    View untuk menghapus FAQ (CS)
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ berhasil dihapus.')
        return redirect('main:cs_faq')
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Hapus FAQ - CS Dashboard',
        'faq': faq,
    })
    
    return render(request, 'cs/faq_delete.html', context)


def cs_forum(request):
    """
    Menu Forum Monitoring
    CS melihat dan memantau postingan forum dengan fitur lengkap
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters (needed for redirect after POST)
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    sort_by = request.GET.get('sort', 'newest')
    
    # Handle POST requests (delete, add note)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Delete post
        if action == 'delete_post':
            post_id = request.POST.get('post_id')
            try:
                post = ForumPost.objects.get(id=post_id)
                post_title = post.title
                post.delete()  # This will cascade delete all comments
                messages.success(request, f'Postingan "{post_title}" berhasil dihapus.')
            except ForumPost.DoesNotExist:
                messages.error(request, 'Postingan tidak ditemukan.')
        
        # Delete comment
        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id')
            try:
                comment = ForumComment.objects.get(id=comment_id)
                comment.delete()
                messages.success(request, 'Komentar berhasil dihapus.')
            except ForumComment.DoesNotExist:
                messages.error(request, 'Komentar tidak ditemukan.')
        
        # Add CS note
        elif action == 'add_cs_note':
            post_id = request.POST.get('post_id')
            note_content = request.POST.get('note_content', '').strip()
            
            if not note_content:
                messages.error(request, 'Catatan tidak boleh kosong.')
            else:
                try:
                    post = ForumPost.objects.get(id=post_id)
                    ForumComment.objects.create(
                        post=post,
                        author=None,  # CS note doesn't have forum user author
                        content=note_content,
                        is_cs_note=True,
                        replied_by_cs=cs
                    )
                    messages.success(request, 'Catatan CS berhasil ditambahkan.')
                except ForumPost.DoesNotExist:
                    messages.error(request, 'Postingan tidak ditemukan.')
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')
        
        # Add regular comment from CS
        elif action == 'add_comment':
            post_id = request.POST.get('post_id')
            comment_content = request.POST.get('comment_content', '').strip()
            
            if not comment_content:
                messages.error(request, 'Komentar tidak boleh kosong.')
            else:
                try:
                    post = ForumPost.objects.get(id=post_id)
                    ForumComment.objects.create(
                        post=post,
                        author=None,  # CS comment doesn't have forum user author
                        content=comment_content,
                        is_cs_note=False,  # Regular comment, not official note
                        replied_by_cs=cs
                    )
                    messages.success(request, 'Komentar berhasil ditambahkan.')
                except ForumPost.DoesNotExist:
                    messages.error(request, 'Postingan tidak ditemukan.')
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')
        
        # Preserve filter parameters in redirect
        params = {}
        if request.GET.get('search'):
            params['search'] = request.GET.get('search')
        if request.GET.get('category'):
            params['category'] = request.GET.get('category')
        if request.GET.get('sort'):
            params['sort'] = request.GET.get('sort')
        if params:
            return redirect(f"{reverse('main:cs_forum')}?{urlencode(params)}")
        return redirect('main:cs_forum')
    
    # Get forum posts with their comments (prefetch for efficiency)
    posts = ForumPost.objects.select_related('author').prefetch_related('comments', 'comments__author', 'comments__replied_by_cs').all()
    
    # Apply search filter
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        posts = posts.filter(category=category_filter)
    
    # Apply sorting
    if sort_by == 'oldest':
        posts = posts.order_by('created_at')
    else:  # newest (default)
        posts = posts.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts per page
    page = request.GET.get('page', 1)
    try:
        posts_page = paginator.get_page(page)
    except:
        posts_page = paginator.get_page(1)
    
    # Get category choices for filter
    category_choices = ForumPost.CATEGORY_CHOICES
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Forum Monitoring - CS Dashboard',
        'posts': posts_page,
        'search_query': search_query,
        'category_filter': category_filter,
        'sort_by': sort_by,
        'category_choices': category_choices,
    })
    
    return render(request, 'cs/forum.html', context)


def cs_members(request):
    """
    Informasi Member (Read-only)
    CS melihat informasi member yang sudah melakukan pembelian dan telah diverifikasi
    Hanya menampilkan member dengan purchase order status 'verified'
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    member_filter = request.GET.get('member', '').strip()
    
    # Get members yang memiliki purchase order dengan status 'verified'
    from .models import PurchaseOrder
    verified_member_ids = PurchaseOrder.objects.filter(
        status='verified',
        member_id__isnull=False
    ).values_list('member_id', flat=True).distinct()
    
    # Get members berdasarkan verified member IDs
    members = Member.objects.filter(
        member_id__in=verified_member_ids
    ).distinct()
    
    if search_query:
        members = members.filter(
            Q(member_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(rangbot_devices__serial_number__icontains=search_query)
        ).distinct()
    
    if member_filter:
        members = members.filter(member_id__icontains=member_filter)
    
    # Get member statistics dengan purchase order data
    members_with_stats = []
    for member in members.order_by('-created_at')[:100]:  # Limit untuk performa
        # Get verified purchase orders untuk member ini
        verified_orders = PurchaseOrder.objects.filter(
            member_id=member.member_id,
            status='verified'
        ).order_by('-verified_at')
        
        # Skip jika tidak ada verified orders
        if not verified_orders.exists():
            continue
        
        all_devices = member.rangbot_devices.all()
        pro_count = sum(1 for d in all_devices if 'pro' in (d.device_name or '').lower() or 'professional' in (d.device_name or '').lower())
        basic_count = all_devices.count() - pro_count
        
        # Get total purchase info
        total_orders = verified_orders.count()
        latest_order = verified_orders.first()
        
        members_with_stats.append({
            'member': member,
            'total_devices': all_devices.count(),
            'pro_count': pro_count,
            'basic_count': basic_count,
            'total_orders': total_orders,
            'latest_order': latest_order,
        })
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Informasi Member - CS Dashboard',
        'members_with_stats': members_with_stats,
        'search_query': search_query,
        'member_filter': member_filter,
    })
    
    return render(request, 'cs/members.html', context)


def cs_member_detail(request, member_id):
    """
    Detail Member untuk CS (Read-only)
    Menampilkan informasi lengkap member dan purchase orders yang sudah verified
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    
    # Get verified purchase orders untuk member ini
    from .models import PurchaseOrder
    verified_orders = PurchaseOrder.objects.filter(
        member_id=member_id,
        status='verified'
    ).order_by('-verified_at')
    
    # Get devices dari verified orders
    devices = member.rangbot_devices.filter(
        purchase_order__status='verified'
    ).order_by('-created_at')
    
    # Get order details dengan device info
    orders_with_details = []
    for order in verified_orders:
        order_devices = devices.filter(purchase_order=order)
        orders_with_details.append({
            'order': order,
            'devices': order_devices,
            'device_count': order_devices.count(),
        })
    
    # Calculate total investment
    from django.db.models import Sum
    total_investment = verified_orders.aggregate(total=Sum('total_price'))['total'] or 0
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': f'Detail Member {member_id} - CS Dashboard',
        'member': member,
        'verified_orders': verified_orders,
        'orders_with_details': orders_with_details,
        'devices': devices,
        'total_investment': total_investment,
    })
    
    return render(request, 'cs/member_detail.html', context)


def cs_notifications(request):
    """
    Menu Notifikasi
    CS melihat notifikasi aktivitas penting
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get recent activities that might need CS attention
    new_messages = ContactMessage.objects.filter(status='new').order_by('-created_at')[:10]
    recent_forum_posts = ForumPost.objects.order_by('-created_at')[:10]
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Notifikasi - CS Dashboard',
        'new_messages': new_messages,
        'recent_forum_posts': recent_forum_posts,
    })
    
    return render(request, 'cs/notifications.html', context)


def cs_activity_log_list(request):
    """
    View untuk menampilkan riwayat aktivitas sistem (Riwayat Log)
    Mirip dengan activity_log_list di admin, tapi untuk CS
    """
    cs = get_cs(request)
    if not cs:
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
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Riwayat Log - CS Dashboard',
        'logs': logs,
        'action_filter': action_filter,
        'search_query': search_query,
        'date_from': date_from,
        'date_to': date_to,
        'action_types': ActivityLog.ACTION_TYPES,
    })
    
    return render(request, 'cs/activity_log_list.html', context)


def cs_settings(request):
    """
    Menu Informasi Profil CS
    Menampilkan informasi profil CS (read-only)
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Informasi Profil - CS Dashboard',
    })
    
    return render(request, 'cs/settings.html', context)

