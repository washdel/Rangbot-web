from django.contrib import admin
from .models import ForumUser, ForumPost, ForumComment, Admin, CustomerService, PurchaseOrder, Member, RangBotDevice, DetectionHistory, Notification, ProductInfo, FAQ, Article, ActivityLog


@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'created_at', 'last_login')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at', 'last_login')


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'views', 'created_at', 'get_comment_count')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author__name', 'author__email')
    readonly_fields = ('created_at', 'updated_at', 'views')
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    get_comment_count.short_description = 'Komentar'


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__name', 'post__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'username', 'full_name', 'email', 'get_device_count', 'created_at', 'last_login')
    list_filter = ('created_at',)
    search_fields = ('member_id', 'username', 'full_name', 'email')
    readonly_fields = ('created_at', 'last_login')
    
    def get_device_count(self, obj):
        return obj.get_device_count()
    get_device_count.short_description = 'Jumlah Perangkat'


@admin.register(RangBotDevice)
class RangBotDeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'device_name', 'covered_blocks', 'member', 'status', 'is_active', 'last_data_update', 'created_at')
    list_filter = ('status', 'is_active', 'created_at')
    search_fields = ('serial_number', 'device_name', 'covered_blocks', 'member__member_id', 'member__username')
    readonly_fields = ('created_at',)


@admin.register(DetectionHistory)
class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ('device', 'disease_detected', 'detection_type', 'confidence', 'created_at')
    list_filter = ('detection_type', 'created_at')
    search_fields = ('device__serial_number', 'disease_detected', 'location')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('member', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'member__member_id')
    readonly_fields = ('created_at',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'is_active', 'created_at', 'last_login')
    list_filter = ('is_active', 'created_at')
    search_fields = ('username', 'email', 'full_name')
    readonly_fields = ('created_at', 'last_login')


@admin.register(CustomerService)
class CustomerServiceAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'is_active', 'created_at', 'last_login')
    list_filter = ('is_active', 'created_at')
    search_fields = ('username', 'email', 'full_name')
    readonly_fields = ('created_at', 'last_login')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'qty_basic', 'qty_professional', 'total_price', 'status', 'member_id', 'is_reorder', 'created_at', 'verified_at')
    list_filter = ('status', 'is_reorder', 'created_at', 'verified_at')
    search_fields = ('customer_name', 'customer_email', 'customer_phone', 'member_id', 'original_member_id')
    readonly_fields = ('created_at', 'verified_at')
    date_hierarchy = 'created_at'


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_type', 'price', 'is_active', 'updated_at')
    list_filter = ('package_type', 'is_active', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('updated_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'created_by')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'description', 'performed_by', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('description', 'performed_by__full_name', 'performed_by__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
