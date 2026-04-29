import ipaddress
import logging
from django.http import HttpResponseForbidden
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('cloudflare_middleware')


class CloudflareOnlyMiddleware(MiddlewareMixin):
    """
    只允许 Cloudflare IP 访问的中间件
    """
    
    def process_request(self, request):
        # 开发环境跳过检查
        if settings.DEBUG:
            return None
            
        # 本地访问跳过检查
        client_ip = self.get_client_ip(request)
        if client_ip in ['127.0.0.1', 'localhost', '::1']:
            return None
            
        # 健康检查端点不受限制
        if request.path == '/health/':
            return None
            
        # OPTIONS 请求（CORS 预检）不受限制
        if request.method == 'OPTIONS':
            return None
        
        # 检查是否有Cloudflare特有的头部
        if self.has_cloudflare_headers(request):
            logger.info(f"Cloudflare 头部检查通过 - CF-Connecting-IP: {request.META.get('HTTP_CF_CONNECTING_IP')}")
            return None
        
        # 记录访问信息用于调试
        logger.info(f"Cloudflare 访问检查 - 路径: {request.path}, 客户端 IP: {client_ip}")
        logger.info(f"CF-Connecting-IP: {request.META.get('HTTP_CF_CONNECTING_IP')}")
        logger.info(f"X-Forwarded-For: {request.META.get('HTTP_X_FORWARDED_FOR')}")
        logger.info(f"X-Real-IP: {request.META.get('HTTP_X_REAL_IP')}")
        logger.info(f"REMOTE_ADDR: {request.META.get('REMOTE_ADDR')}")
            
        # 检查是否为 Cloudflare IP
        if not self.is_cloudflare_ip(client_ip):
            logger.warning(f"Cloudflare IP 检查失败 - IP: {client_ip} 不在 Cloudflare 范围内")
            return HttpResponseForbidden("Access denied: Only Cloudflare access allowed")
        
        logger.info(f"Cloudflare IP 检查通过 - IP: {client_ip}")
        return None
    
    def has_cloudflare_headers(self, request):
        """检查是否有Cloudflare特有的头部"""
        # Cloudflare 会添加这些特有的头部
        cf_headers = [
            'HTTP_CF_CONNECTING_IP',
            'HTTP_CF_RAY',
            'HTTP_CF_VISITOR',
            'HTTP_CF_IPCOUNTRY'
        ]
        
        for header in cf_headers:
            if request.META.get(header):
                return True
        return False
    
    def get_client_ip(self, request):
        """获取客户端真实 IP"""
        # 优先从 CF-Connecting-IP 获取（Cloudflare 专用头）
        cf_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        if cf_ip:
            return cf_ip
            
        # 从 X-Forwarded-For 获取
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
            
        # 从 X-Real-IP 获取
        x_real_ip = request.META.get('HTTP_X_REAL_IP')
        if x_real_ip:
            return x_real_ip
            
        # 最后使用 REMOTE_ADDR
        return request.META.get('REMOTE_ADDR')
    
    def is_cloudflare_ip(self, ip):
        """检查 IP 是否属于 Cloudflare"""
        try:
            client_ip = ipaddress.ip_address(ip)
            
            for cf_range in settings.CLOUDFLARE_IPS:
                if client_ip in ipaddress.ip_network(cf_range):
                    return True
                    
            return False
        except (ValueError, ipaddress.AddressValueError):
            # IP 格式错误，拒绝访问
            return False