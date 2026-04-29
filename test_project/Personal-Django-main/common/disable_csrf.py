import re
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 定义不需要禁用CSRF的路径模式
        # 使用正则表达式定义例外路径
        protected_paths = [
            r'^/admin/.*',  # Django管理后台
            # 可以在这里添加其他需要CSRF保护的路径
        ]
        
        # 检查当前路径是否在保护列表中
        current_path = request.path
        for pattern in protected_paths:
            if re.match(pattern, current_path):
                # 如果匹配，则启用CSRF验证
                return None
        
        # 对于不在保护列表中的路径，禁用CSRF验证
        request._dont_enforce_csrf_checks = True