"""
DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Django Project API",
      default_version='v1',
      description="Django 项目 API 文档",
      contact=openapi.Contact(email="baiyila2022@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

def health_check(request):
    """健康检查端点（不受 Cloudflare IP 限制）"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Service is running normally',
        'timestamp': request.META.get('HTTP_DATE', 'N/A')
    })


@require_GET
def api_login_placeholder(request):
    """
    占位登录页：Django 默认 LOGIN_URL 为 /accounts/login/，Swagger 等会跳转至此。
    本 API 使用 JWT，不在此页做表单登录；若开启了 API 文档则跳转到 Swagger，否则返回说明。
    """
    from django.http import HttpResponseRedirect
    next_url = (request.GET.get('next') or '').strip().lstrip('/')
    if (next_url.startswith('swagger') or next_url.startswith('redoc') or next_url == '') and getattr(settings, 'ENABLE_API_DOCS', False):
        return HttpResponseRedirect('/swagger/')
    if next_url == 'admin' or next_url.startswith('admin/'):
        return HttpResponseRedirect('/admin/')
    return JsonResponse({
        'message': '本 API 使用 JWT 认证',
        'login_api': '/api/auth/login/',
        'usage': '请求头携带 Authorization: Bearer <access_token>',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', api_login_placeholder, name='login'),
    path('api/auth/', include('authentication.urls')),
    path('auth/', include('authentication.urls')),  # 兼容旧路径
    path('api/testcases/', include('testcases.urls')),
    path('health/', health_check, name='health-check'),
]

# 仅当 ENABLE_API_DOCS 为 True 时暴露 Swagger/Redoc，避免线上暴露接口结构（默认与 DEBUG 一致）
if getattr(settings, 'ENABLE_API_DOCS', False):
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

# 在生产环境中也提供静态文件
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)