from django.urls import path
from . import views
from . import admin_views

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
    path('forum/login/', views.forum_login, name='forum_login'),  # Redirects to unified login
    path('forum/logout/', views.forum_logout, name='forum_logout'),
    path('forum/create/', views.forum_create, name='forum_create'),
    path('forum/<int:post_id>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:post_id>/edit/', views.forum_edit, name='forum_edit'),
    path('forum/<int:post_id>/delete/', views.forum_delete, name='forum_delete'),
    
    # Dashboard Member URLs
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('dashboard/logout/', views.member_logout, name='member_logout'),
    path('dashboard/profile/', views.member_profile, name='member_profile'),
    path('dashboard/notifications/', views.member_notifications, name='member_notifications'),
    path('dashboard/add-device/', views.add_device, name='add_device'),
    path('dashboard/manual-detection/', views.manual_detection, name='manual_detection'),
    path('dashboard/device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('dashboard/device/<int:device_id>/control/', views.device_control, name='device_control'),
    path('dashboard/device/<int:device_id>/streaming/', views.device_streaming, name='device_streaming'),
    path('dashboard/device/<int:device_id>/sensor/', views.device_sensor, name='device_sensor'),
    path('dashboard/device/<int:device_id>/detection-history/', views.device_detection_history, name='device_detection_history'),
    
    # Admin URLs (unified login - no separate admin login)
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin/purchase-orders/', admin_views.purchase_orders_list, name='purchase_orders_list'),
    path('admin/purchase-orders/<int:order_id>/', admin_views.purchase_order_detail, name='purchase_order_detail'),
    path('admin/purchase-orders/<int:order_id>/verify/', admin_views.verify_purchase, name='verify_purchase'),
    path('admin/purchase-orders/<int:order_id>/reject/', admin_views.reject_purchase, name='reject_purchase'),
]

