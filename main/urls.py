from django.urls import path
from . import views
from . import admin_views
from . import cs_views

app_name = 'main'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('informasi-produk/', views.product_info, name='product_info'),
    path('pembelian/', views.purchase, name='purchase'),
    path('login/', views.member_login, name='login'),
    path('register/', views.register_view, name='register'),
    path('hubungi-support/', views.contact_support, name='contact_support'),
    path('hubungi-sales/', views.contact_sales, name='contact_sales'),
    
    # Forum URLs
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/login/', views.forum_login, name='forum_login'),
    path('forum/register/', views.forum_register, name='forum_register'),
    path('forum/logout/', views.forum_logout, name='forum_logout'),
    path('forum/profile/', views.forum_profile, name='forum_profile'),
    path('forum/create/', views.forum_create, name='forum_create'),
    path('forum/<int:post_id>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:post_id>/edit/', views.forum_edit, name='forum_edit'),
    path('forum/<int:post_id>/delete/', views.forum_delete, name='forum_delete'),
    
    # Dashboard Member URLs
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('dashboard/logout/', views.member_logout, name='member_logout'),
    path('dashboard/profile/', views.member_profile, name='member_profile'),
    path('dashboard/notifications/', views.member_notifications, name='member_notifications'),
    path('dashboard/devices/', views.member_devices, name='member_devices'),
    path('dashboard/add-device/', views.member_add_device, name='member_add_device'),
    path('dashboard/purchase/', views.member_purchase, name='member_purchase'),
    path('dashboard/device/<int:device_id>/', views.member_device_management, name='member_device_management'),
    path('dashboard/manual-detection/', views.manual_detection, name='manual_detection'),
    path('dashboard/usage-guide/', views.member_usage_guide, name='member_usage_guide'),
    path('dashboard/daily-tips/', views.member_daily_tips, name='member_daily_tips'),
    path('dashboard/disease-classification/', views.member_disease_classification, name='member_disease_classification'),
    # Legacy URLs for backward compatibility
    path('dashboard/device/<int:device_id>/control/', views.device_control, name='device_control'),
    path('dashboard/device/<int:device_id>/streaming/', views.device_streaming, name='device_streaming'),
    path('dashboard/device/<int:device_id>/sensor/', views.device_sensor, name='device_sensor'),
    path('dashboard/device/<int:device_id>/detection-history/', views.device_detection_history, name='device_detection_history'),
    
    # Admin URLs (unified login - no separate admin login)
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_views.admin_logout, name='admin_logout'),
    
    # Purchase Orders
    path('admin/purchase-orders/', admin_views.purchase_orders_list, name='purchase_orders_list'),
    path('admin/purchase-orders/<int:order_id>/', admin_views.purchase_order_detail, name='purchase_order_detail'),
    path('admin/purchase-orders/<int:order_id>/verify/', admin_views.verify_purchase, name='verify_purchase'),
    path('admin/purchase-orders/<int:order_id>/reject/', admin_views.reject_purchase, name='reject_purchase'),
    path('admin/purchase-orders/<int:order_id>/delete-data/', admin_views.delete_purchase_order_data, name='delete_purchase_order_data'),
    
    # Member Management
    path('admin/members/', admin_views.members_list, name='members_list'),
    path('admin/members/<str:member_id>/', admin_views.member_detail, name='member_detail'),
    path('admin/members/<str:member_id>/toggle-active/', admin_views.member_toggle_active, name='member_toggle_active'),
    path('admin/members/<str:member_id>/delete/', admin_views.member_delete, name='member_delete'),
    path('admin/members/<str:member_id>/edit/', admin_views.member_edit, name='member_edit'),
    
    # Serial Number Management
    path('admin/serial-numbers/', admin_views.serial_numbers_list, name='serial_numbers_list'),
    path('admin/serial-numbers/<str:member_id>/', admin_views.serial_number_detail, name='serial_number_detail'),
    
    # Customer Service Management
    path('admin/customer-service/', admin_views.cs_list, name='cs_list'),
    path('admin/customer-service/add/', admin_views.cs_add, name='cs_add'),
    path('admin/customer-service/<int:cs_id>/delete/', admin_views.cs_delete, name='cs_delete'),
    
    # Admin Management
    path('admin/admins/', admin_views.admin_list, name='admin_list'),
    path('admin/admins/add/', admin_views.admin_add, name='admin_add'),
    path('admin/admins/<int:admin_id>/toggle-active/', admin_views.admin_toggle_active, name='admin_toggle_active'),
    
    # Notifications
    path('admin/notifications/', admin_views.admin_notifications_list, name='admin_notifications_list'),
    
    # Activity Log
    path('admin/activity-log/', admin_views.activity_log_list, name='activity_log_list'),
    path('admin/activity-log/<int:log_id>/delete/', admin_views.activity_log_delete, name='activity_log_delete'),
    path('admin/activity-log/delete-all/', admin_views.activity_log_delete_all, name='activity_log_delete_all'),
    
    # Product & Landing Page Management
    path('admin/products/', admin_views.product_info_list, name='product_info_list'),
    path('admin/products/add/', admin_views.product_add, name='product_add'),
    path('admin/products/<int:product_id>/edit/', admin_views.product_info_edit, name='product_info_edit'),
    # Forum Management
    path('admin/forum/post/<int:post_id>/delete/', admin_views.forum_post_delete, name='forum_post_delete'),
    path('admin/forum/comment/<int:comment_id>/delete/', admin_views.forum_comment_delete, name='forum_comment_delete'),
    path('admin/faq/', admin_views.faq_list, name='faq_list'),
    path('admin/faq/add/', admin_views.faq_add, name='faq_add'),
    path('admin/faq/<int:faq_id>/edit/', admin_views.faq_edit, name='faq_edit'),
    path('admin/faq/<int:faq_id>/delete/', admin_views.faq_delete, name='faq_delete'),
    path('admin/articles/', admin_views.articles_list, name='articles_list'),
    path('admin/articles/add/', admin_views.article_add, name='article_add'),
    path('admin/articles/<int:article_id>/edit/', admin_views.article_edit, name='article_edit'),
    path('admin/articles/<int:article_id>/delete/', admin_views.article_delete, name='article_delete'),
    
    # Customer Service URLs
    path('cs/dashboard/', cs_views.cs_dashboard, name='cs_dashboard'),
    path('cs/logout/', cs_views.cs_logout, name='cs_logout'),
    path('cs/messages/', cs_views.cs_messages, name='cs_messages'),
    path('cs/faq/', cs_views.cs_faq, name='cs_faq'),
    path('cs/faq/add/', cs_views.cs_faq_add, name='cs_faq_add'),
    path('cs/faq/<int:faq_id>/edit/', cs_views.cs_faq_edit, name='cs_faq_edit'),
    path('cs/faq/<int:faq_id>/delete/', cs_views.cs_faq_delete, name='cs_faq_delete'),
    path('cs/forum/', cs_views.cs_forum, name='cs_forum'),
    path('cs/members/', cs_views.cs_members, name='cs_members'),
    path('cs/members/<str:member_id>/', cs_views.cs_member_detail, name='cs_member_detail'),
    path('cs/notifications/', cs_views.cs_notifications, name='cs_notifications'),
    path('cs/activity-log/', cs_views.cs_activity_log_list, name='cs_activity_log_list'),
    path('cs/settings/', cs_views.cs_settings, name='cs_settings'),
]

