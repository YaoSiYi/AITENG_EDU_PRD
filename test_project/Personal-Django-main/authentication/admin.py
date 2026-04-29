from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# 重新注册 User 模型以自定义显示
# 首先取消注册默认的 UserAdmin
admin.site.unregister(User)

# 然后重新注册自定义的 UserAdmin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 在列表页显示的字段
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # 可以搜索的字段
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # 可以过滤的字段
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    # 按日期层级显示
    date_hierarchy = 'date_joined'
    
    # 保持原有的字段集配置
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email')}),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    # 添加新用户时的字段集
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # 处理可能的异常，防止500错误
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 确保所有用户都有配置文件
        for user in qs:
            try:
                user.profile
            except:
                from authentication.models import UserProfile
                UserProfile.objects.get_or_create(user=user)
        return qs