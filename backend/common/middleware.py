from django.utils.deprecation import MiddlewareMixin

class CloudflareProxyMiddleware(MiddlewareMixin):
    """
    Cloudflare Tunnel 代理中间件
    处理 X-Forwarded-Proto 和 X-Forwarded-Host 头
    """
    def process_request(self, request):
        # 处理 X-Forwarded-Proto
        proto = request.META.get('HTTP_X_FORWARDED_PROTO')
        if proto:
            request.META['wsgi.url_scheme'] = proto
        
        # 处理 X-Forwarded-Host
        host = request.META.get('HTTP_X_FORWARDED_HOST')
        if host:
            request.META['HTTP_HOST'] = host
        
        return None
