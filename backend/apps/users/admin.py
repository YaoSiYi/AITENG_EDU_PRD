from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponse
from .models import User
import csv
import io
from datetime import datetime


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['username', 'nickname', 'gender', 'phone', 'hometown', 'period', 'study_status', 'role', 'plain_password', 'is_active', 'get_dormitory_info', 'get_employment_info', 'created_at']
    list_filter = ['role', 'gender', 'period', 'study_status', 'is_active', 'created_at']
    search_fields = ['username', 'nickname', 'phone', 'hometown', 'period', 'qq']
    ordering = ['-created_at']
    actions = ['export_selected_users']

    # 编辑页面的字段配置
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'plain_password', 'nickname', 'phone', 'qq', 'wechat_openid')
        }),
        ('个人信息', {
            'fields': ('gender', 'hometown', 'password_hint', 'period', 'study_status', 'avatar')
        }),
        ('权限信息', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('时间信息', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # 添加用户时的字段
    add_fieldsets = (
        ('基本信息', {
            'fields': ('username', 'plain_password', 'nickname', 'phone')
        }),
        ('个人信息', {
            'fields': ('gender', 'hometown', 'password_hint', 'period', 'study_status')
        }),
        ('权限信息', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

    readonly_fields = ['last_login', 'date_joined', 'created_at', 'updated_at']

    def get_dormitory_info(self, obj):
        """显示宿舍信息"""
        from django.utils.html import format_html
        from django.utils.safestring import mark_safe
        from django.urls import reverse
        from django.core.exceptions import ObjectDoesNotExist

        try:
            dormitory = obj.dormitory_info
            url = reverse('admin:stats_dormitory_change', args=[dormitory.id])
            return format_html(
                '<a href="{}" style="color: #417690; font-weight: bold;">{}</a>',
                url,
                dormitory.dormitory
            )
        except ObjectDoesNotExist:
            return mark_safe('<span style="color: #999;">未分配</span>')
        except Exception:
            return mark_safe('<span style="color: #999;">未分配</span>')
    get_dormitory_info.short_description = '宿舍'

    def get_employment_info(self, obj):
        """显示就业信息"""
        from django.utils.html import format_html
        try:
            employment_records = obj.employment_records.all()
            if employment_records.exists():
                record = employment_records.first()
                return format_html(
                    '<span style="color: green;">✓ 已就业</span><br>{}（{}K）',
                    record.company,
                    record.salary // 1000
                )
        except Exception:
            pass
        return '-'
    get_employment_info.short_description = '就业信息'

    def save_model(self, request, obj, form, change):
        """保存模型时的处理"""
        # 如果明文密码被修改，同步更新哈希密码
        if 'plain_password' in form.changed_data and obj.plain_password:
            obj.set_password(obj.plain_password)
        super().save_model(request, obj, form, change)

    def get_urls(self):
        """添加自定义 URL"""
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='users_user_import_csv'),
            path('download-template/', self.admin_site.admin_view(self.download_template), name='users_user_download_template'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """重写列表视图，添加导入按钮"""
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def import_csv(self, request):
        """批量导入 CSV 文件"""
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')

            if not csv_file:
                messages.error(request, '请选择要导入的 CSV 文件')
                return redirect('..')

            if not csv_file.name.endswith('.csv'):
                messages.error(request, '文件格式错误，请上传 CSV 文件')
                return redirect('..')

            try:
                # 读取 CSV 文件
                decoded_file = csv_file.read().decode('utf-8-sig')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                success_count = 0
                error_count = 0
                error_messages = []

                for row_num, row in enumerate(reader, start=2):
                    try:
                        # 验证必填字段
                        username = row.get('username', '').strip()
                        password = row.get('password', '').strip()

                        if not username:
                            error_messages.append(f'第 {row_num} 行：用户名不能为空')
                            error_count += 1
                            continue

                        if not password:
                            error_messages.append(f'第 {row_num} 行：密码不能为空')
                            error_count += 1
                            continue

                        # 检查用户名是否已存在
                        if User.objects.filter(username=username).exists():
                            error_messages.append(f'第 {row_num} 行：用户名 {username} 已存在')
                            error_count += 1
                            continue

                        # 创建用户
                        user = User(
                            username=username,
                            plain_password=password,
                            nickname=row.get('nickname', '').strip(),
                            phone=row.get('phone', '').strip() or None,
                            qq=row.get('qq', '').strip(),
                            hometown=row.get('hometown', '').strip(),
                            password_hint=row.get('password_hint', '').strip(),
                            period=row.get('period', '').strip(),
                            study_status=row.get('study_status', 'studying').strip(),
                            role=row.get('role', 'student').strip(),
                            is_active=row.get('is_active', 'True').strip().lower() in ['true', '1', 'yes'],
                        )

                        # 设置密码
                        user.set_password(password)
                        user.save()

                        success_count += 1

                    except Exception as e:
                        error_messages.append(f'第 {row_num} 行：{str(e)}')
                        error_count += 1

                # 显示导入结果
                if success_count > 0:
                    messages.success(request, f'成功导入 {success_count} 个用户')

                if error_count > 0:
                    error_msg = f'导入失败 {error_count} 个用户：\n' + '\n'.join(error_messages[:10])
                    if len(error_messages) > 10:
                        error_msg += f'\n... 还有 {len(error_messages) - 10} 个错误'
                    messages.error(request, error_msg)

                return redirect('..')

            except Exception as e:
                messages.error(request, f'导入失败：{str(e)}')
                return redirect('..')

        # GET 请求，显示导入页面
        context = {
            'title': '批量导入用户',
            'site_title': '用户管理',
            'has_permission': True,
        }
        return render(request, 'admin/users/import_csv.html', context)

    def download_template(self, request):
        """下载 CSV 模板"""
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="user_import_template.csv"'

        # 添加 BOM 以支持 Excel 正确显示中文
        response.write('﻿')

        writer = csv.writer(response)

        # 写入表头
        writer.writerow([
            'username',
            'password',
            'nickname',
            'phone',
            'qq',
            'hometown',
            'password_hint',
            'period',
            'study_status',
            'role',
            'is_active'
        ])

        # 写入示例数据
        writer.writerow([
            'student001',
            'password123',
            '张三',
            '13800138000',
            '123456789',
            '广东省深圳市',
            '我的生日',
            '2024-01-01期学员',
            'studying',
            'student',
            'True'
        ])

        writer.writerow([
            'student002',
            'password456',
            '李四',
            '13800138001',
            '987654321',
            '北京市北京市',
            '我的宠物名',
            '2024-01-01期学员',
            'graduated',
            'student',
            'True'
        ])

        return response

    def export_selected_users(self, request, queryset):
        """批量导出所选用户"""
        # 创建 CSV 响应
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="users_export_{timestamp}.csv"'

        # 添加 BOM 以支持 Excel 正确显示中文
        response.write('﻿')

        writer = csv.writer(response)

        # 写入表头
        writer.writerow([
            '用户名',
            '昵称',
            '手机号',
            'QQ号',
            '微信OpenID',
            '籍贯',
            '密码提示',
            '期数',
            '学习状态',
            '角色',
            '是否激活',
            '是否员工',
            '是否超级用户',
            '最后登录时间',
            '注册时间',
            '创建时间',
            '更新时间'
        ])

        # 写入数据
        for user in queryset:
            writer.writerow([
                user.username,
                user.nickname or '',
                user.phone or '',
                user.qq or '',
                user.wechat_openid or '',
                user.hometown or '',
                user.password_hint or '',
                user.period or '',
                user.get_study_status_display(),
                user.get_role_display(),
                '是' if user.is_active else '否',
                '是' if user.is_staff else '否',
                '是' if user.is_superuser else '否',
                user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
                user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
                user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
                user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else '',
            ])

        # 显示成功消息
        self.message_user(request, f'成功导出 {queryset.count()} 个用户')

        return response

    export_selected_users.short_description = '导出所选用户'
