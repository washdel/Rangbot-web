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
from .models import (
    CustomerService, ContactMessage, FAQ, ForumPost, ForumComment,
    Member, RangBotDevice, ProductInfo
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
    
    # FAQ statistics
    total_faqs = FAQ.objects.filter(is_active=True).count()
    recent_faqs = FAQ.objects.filter(is_active=True).order_by('-updated_at')[:5]
    
    # Member statistics (for info)
    total_members = Member.objects.filter(is_active=True).count()
    total_devices = RangBotDevice.objects.filter(is_active=True).count()
    
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
        'total_faqs': total_faqs,
        'recent_faqs': recent_faqs,
        'total_members': total_members,
        'total_devices': total_devices,
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
                    messages.success(request, f'Balasan untuk {message.name} telah dikirim.')
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
    
    # Get FAQs
    faqs = FAQ.objects.all().order_by('order', '-created_at')
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'FAQ Management - CS Dashboard',
        'faqs': faqs,
    })
    
    return render(request, 'cs/faq.html', context)


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
    CS melihat informasi member dan nomor seri untuk membantu pengguna
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    member_filter = request.GET.get('member', '').strip()
    
    # Get members
    members = Member.objects.filter(rangbot_devices__isnull=False).distinct()
    
    if search_query:
        members = members.filter(
            Q(member_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(rangbot_devices__serial_number__icontains=search_query)
        ).distinct()
    
    if member_filter:
        members = members.filter(member_id__icontains=member_filter)
    
    # Get member statistics
    members_with_stats = []
    for member in members.order_by('-created_at')[:50]:  # Limit untuk performa
        all_devices = member.rangbot_devices.all()
        pro_count = sum(1 for d in all_devices if 'pro' in (d.device_name or '').lower() or 'professional' in (d.device_name or '').lower())
        basic_count = all_devices.count() - pro_count
        
        members_with_stats.append({
            'member': member,
            'total_devices': all_devices.count(),
            'pro_count': pro_count,
            'basic_count': basic_count,
        })
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Informasi Member - CS Dashboard',
        'members_with_stats': members_with_stats,
        'search_query': search_query,
        'member_filter': member_filter,
    })
    
    return render(request, 'cs/members.html', context)


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


def cs_settings(request):
    """
    Menu Pengaturan Akun CS
    CS dapat mengubah password dan profil
    """
    cs = get_cs(request)
    if not cs:
        messages.warning(request, 'Anda harus login terlebih dahulu.')
        return redirect('main:login')
    
    context = get_cs_base_context(cs)
    context.update({
        'page_title': 'Pengaturan Akun - CS Dashboard',
    })
    
    return render(request, 'cs/settings.html', context)

