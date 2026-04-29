import re
import secrets
from rest_framework import status
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import UserSerializer
from .renderers import CustomJSONRenderer
from .totp_utils import (
    get_totp_secret,
    get_provisioning_uri,
    verify_totp,
    set_pending_setup,
    get_pending_setup,
    delete_pending_setup,
    set_pending_login,
    get_pending_login,
    delete_pending_login,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

# 路径遍历字符常量
PATH_TRAVERSAL_CHARS = ['..', '/', '\\', '%2e%2e', '%2f', '%5c']

# 配置日志
logger = logging.getLogger('authentication')


def sanitize_for_log(value):
    """清理用户输入以防止日志注入"""
    if not value:
        return 'None'
    return str(value).replace('\n', '').replace('\r', '').replace('\t', '')


def validate_password_strength(password):
    """
    验证密码强度
    要求：
    1. 至少8个字符
    2. 包含字母和数字
    3. 包含特殊字符
    """
    if len(password) < 8:
        return False, "密码长度至少8位"
    
    if not re.search(r"[A-Za-z]", password):
        return False, "密码必须包含字母"
        
    if not re.search(r"\d", password):
        return False, "密码必须包含数字"
        
    # 强制要求特殊字符
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "密码必须包含特殊字符"
        
    return True, "密码强度符合要求"


def validate_username(username):
    """
    验证用户名安全性
    """
    if not username or len(username.strip()) == 0:
        return False, "用户名不能为空"
    
    if len(username) < 3 or len(username) > 30:
        return False, "用户名长度必须在3-30个字符之间"
    
    # 只允许字母、数字和下划线
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "用户名只能包含字母、数字和下划线"
    
    return True, "用户名符合要求"


def ratelimited(request, exception):
    """
    速率限制响应处理
    """
    return Response({'error': 'Too Many Requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)


def get_client_ip(request):
    """
    获取客户端IP地址
    """
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
            if ip:
                return ip
        
        remote_addr = request.META.get('REMOTE_ADDR')
        if remote_addr:
            return remote_addr.strip()
            
        return '0.0.0.0'
    except Exception:
        return '0.0.0.0'


def check_login_attempts(request):
    """
    检查登录尝试次数
    """
    try:
        ip = get_client_ip(request)
        if not ip:
            logger.warning("无法获取客户端IP地址")
            return True, ""
            
        cache_key = f"login_attempts_{ip}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:  # 最多允许5次尝试
            return False, "登录失败次数过多，请稍后再试"
        
        return True, ""
    except Exception as e:
        # 缓存失败时允许登录但记录具体错误
        logger.warning(f"缓存服务异常，跳过登录次数检查 - 错误类型: {type(e).__name__}")
        return True, ""


def increment_login_attempts(request):
    """
    增加登录失败次数
    """
    try:
        ip = get_client_ip(request)
        cache_key = f"login_attempts_{ip}"
        attempts = cache.get(cache_key, 0)
        attempts += 1
        # 10分钟内最多5次尝试
        cache.set(cache_key, attempts, 600)
    except Exception:
        logger.warning("缓存服务不可用，无法记录登录失败次数")
        pass


def reset_login_attempts(request):
    """
    重置登录失败次数
    """
    try:
        ip = get_client_ip(request)
        cache_key = f"login_attempts_{ip}"
        cache.delete(cache_key)
    except Exception:
        logger.warning("缓存服务不可用，无法重置登录失败次数")
        pass


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [CustomJSONRenderer]

    @swagger_auto_schema(
        operation_description="用户登录",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response('登录成功', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'msg': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT访问令牌'),
                            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT刷新令牌'),
                        }
                    )
                }
            )),
            400: '请求参数错误',
            404: '用户名或密码错误'
        }
    )
    def post(self, request, *args, **kwargs):
        client_ip = get_client_ip(request)
        username = request.data.get('username')
        
        # 优化性能：一次性处理用户名清理
        sanitized_username = sanitize_for_log(username)
        
        # 检查登录尝试次数
        allowed, message = check_login_attempts(request)
        if not allowed:
            logger.warning(f"登录失败次数过多 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 40000, 'error': message},
                            status=status.HTTP_400_BAD_REQUEST)
        
        password = request.data.get('password')

        if not username or not password:
            logger.warning(f"登录参数不完整 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 20000, 'error': '请提供用户名和密码'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            # 增加失败次数
            increment_login_attempts(request)
            logger.warning(f"登录失败 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 20000, 'error': '检查账号密码正确性'},
                            status=status.HTTP_404_NOT_FOUND)

        # 重置失败次数
        reset_login_attempts(request)

        # 若已开启 Google 验证器，要求二次验证后再发 JWT
        profile = getattr(user, 'profile', None)
        if profile and getattr(profile, 'totp_enabled', False):
            temp_token = secrets.token_urlsafe(32)
            set_pending_login(temp_token, user.id)
            logger.info(f"登录需二次验证 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({
                'code': 20000,
                'msg': 'require_2fa',
                'require_2fa': True,
                'temp_token': temp_token,
            }, status=status.HTTP_200_OK)

        # 生成JWT Token
        refresh = RefreshToken.for_user(user)
        logger.info(f"用户登录成功 - IP: {client_ip}, 用户名: {sanitized_username}, 用户ID: {user.id}")

        return Response({
            'code': 20000,
            'msg': 'Success',
            'user': username,
            'data': {
                'token': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [CustomJSONRenderer]

    def _get_user_public_id(self, user):
        """获取用户公开ID"""
        if hasattr(user, 'profile') and user.profile and hasattr(user.profile, 'public_id'):
            return str(user.profile.public_id)
        return None

    def _validate_registration_data(self, username, password, email, client_ip, sanitized_username):
        """验证注册数据"""
        # 检查必填字段
        if not username or not password:
            logger.warning(f"注册参数不完整 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 40000, 'error': '用户名和密码为必填项'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证用户名安全性
        is_valid_username, username_message = validate_username(username)
        if not is_valid_username:
            logger.warning(f"注册失败-用户名不符合要求 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 40000, 'error': username_message}, status=status.HTTP_400_BAD_REQUEST)

        # 验证密码强度
        is_valid, message = validate_password_strength(password)
        if not is_valid:
            logger.warning(f"注册失败-密码强度不符合要求 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 40000, 'error': message}, status=status.HTTP_400_BAD_REQUEST)

        return None

    def _check_existing_user(self, username, email, client_ip, sanitized_username):
        """检查用户是否已存在"""
        if User.objects.filter(username=username).exists():
            logger.warning(f"注册失败-用户名已存在 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 40000, 'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

        if email and User.objects.filter(email=email).exists():
            logger.warning(f"注册失败-邮箱已被注册 - IP: {client_ip}")
            return Response({'code': 40000, 'error': '邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)

        return None

    def _validate_email(self, email, client_ip, sanitized_username):
        """验证邮箱格式"""
        if not email:
            return None
            
        if any(char in email.lower() for char in PATH_TRAVERSAL_CHARS):
            logger.warning(f"注册失败-邮箱包含非法字符 - IP: {client_ip}, 用户名: {sanitized_username}")
            return Response({'code': 40000, 'error': '邮箱格式不正确'}, status=status.HTTP_400_BAD_REQUEST)
        return None

    @swagger_auto_schema(
        operation_description="用户注册",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
                'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否为管理员'),
            },
            required=['username', 'password']
        ),
        responses={
            201: '注册成功',
            400: '请求参数错误或用户已存在'
        }
    )
    def post(self, request, *args, **kwargs):
        client_ip = get_client_ip(request)
        
        # Define allowed fields to prevent mass assignment
        allowed_fields = {'username', 'password', 'email'}
        filtered_data = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        username = filtered_data.get('username')
        email = filtered_data.get('email')
        password = filtered_data.get('password')
        sanitized_username = sanitize_for_log(username)
        
        logger.info(f"用户注册尝试 - IP: {client_ip}, 用户名: {sanitized_username}")
        
        # Only allow is_staff for superusers
        is_staff = request.user.is_authenticated and request.user.is_superuser and request.data.get('is_staff', False)

        # 验证注册数据
        validation_error = self._validate_registration_data(username, password, email, client_ip, sanitized_username)
        if validation_error:
            return validation_error

        # 检查用户是否已存在
        existing_user_error = self._check_existing_user(username, email, client_ip, sanitized_username)
        if existing_user_error:
            return existing_user_error

        # 验证邮箱格式
        email_error = self._validate_email(email, client_ip, sanitized_username)
        if email_error:
            return email_error

        # 创建用户
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email if email else ''
            )
            
            if is_staff:
                user.is_staff = True
                user.save()
                logger.info(f"用户注册成功(管理员) - IP: {client_ip}, 用户名: {sanitized_username}, 用户ID: {user.id}")
            else:
                logger.info(f"用户注册成功 - IP: {client_ip}, 用户名: {sanitized_username}, 用户ID: {user.id}")
            
            return Response({
                'code': 20000,
                'msg': '注册成功',
                'user': username,
                'data': {
                    'public_id': self._get_user_public_id(user)
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"用户注册失败 - IP: {client_ip}, 用户名: {sanitized_username}, 错误类型: {type(e).__name__}")
            return Response({'code': 50000, 'error': '注册失败，请稍后重试'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserInfoView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            s = UserSerializer(instance=user)
            public_id = str(user.profile.public_id) if hasattr(user, 'profile') and user.profile and hasattr(user.profile, 'public_id') else None
            return Response({'code': 20000, 'msg': "Success",
                             "data": {"roles": s.data.get('user_permissions', []), 'email': user.email, "name": user.username, 'public_id': public_id}})
        except Exception as e:
            user_id = getattr(getattr(request, 'user', None), 'id', 'Unknown')
            logger.error(f"获取用户信息失败 - 用户ID: {user_id}, 错误类型: {type(e).__name__}")
            return Response({'code': 50000, 'error': '获取用户信息失败'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentUserProfileView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            public_id = str(user.profile.public_id) if hasattr(user, 'profile') and user.profile and hasattr(user.profile, 'public_id') else None
            return Response({
                'code': 20000,
                'msg': 'Success',
                'data': {
                    'public_id': public_id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined,
                    'last_login': user.last_login,
                }
            })
        except Exception as e:
            user_id = getattr(getattr(request, 'user', None), 'id', 'Unknown')
            logger.error(f"获取用户配置失败 - 用户ID: {user_id}, 错误类型: {type(e).__name__}")
            return Response({'code': 50000, 'error': '获取用户配置失败'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 对于JWT，前端应负责删除token，后端不需要特殊处理
            client_ip = get_client_ip(request)
            user_id = getattr(getattr(request, 'user', None), 'id', 'Anonymous')
            logger.info(f"用户注销请求 - IP: {client_ip}, 用户ID: {user_id}")
            
            return Response({"code": 20000, "msg": "注销成功"})
        except Exception as e:
            logger.error(f"用户注销异常 - 错误类型: {type(e).__name__}")
            return Response({'code': 50000, 'error': '注销失败，请稍后重试'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------- Google 验证器 (2FA) ----------

class TwoFactorStatusView(APIView):
    """GET：当前用户是否已开启 2FA"""
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        enabled = bool(profile and getattr(profile, 'totp_enabled', False))
        return Response({'code': 20000, 'data': {'enabled': enabled}})


class TwoFactorSetupView(APIView):
    """POST：发起开启 2FA，返回 secret 与 qr_uri，供前端展示二维码；用户扫码后调用 confirm 提交验证码"""
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Response({'code': 40000, 'error': '用户配置不存在'}, status=status.HTTP_400_BAD_REQUEST)
        if getattr(profile, 'totp_enabled', False):
            return Response({'code': 40000, 'error': '已开启双因素认证，无需重复开启'}, status=status.HTTP_400_BAD_REQUEST)
        secret = get_totp_secret()
        set_pending_setup(user.id, secret)
        qr_uri = get_provisioning_uri(secret, user.username)
        return Response({
            'code': 20000,
            'data': {
                'secret': secret,
                'qr_uri': qr_uri,
            },
        })


class TwoFactorConfirmView(APIView):
    """POST：提交 6 位验证码，确认后正式开启 2FA"""
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        code = (request.data.get('code') or '').strip()
        if len(code) != 6:
            return Response({'code': 40000, 'error': '请输入 6 位验证码'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        profile = getattr(user, 'profile', None)
        if not profile:
            return Response({'code': 40000, 'error': '用户配置不存在'}, status=status.HTTP_400_BAD_REQUEST)
        secret = get_pending_setup(user.id)
        if not secret:
            return Response({'code': 40000, 'error': '请先调用开启接口获取二维码'}, status=status.HTTP_400_BAD_REQUEST)
        if not verify_totp(secret, code):
            return Response({'code': 40000, 'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        profile.totp_secret = secret
        profile.totp_enabled = True
        profile.save()
        delete_pending_setup(user.id)
        return Response({'code': 20000, 'msg': '双因素认证已开启'})


class TwoFactorVerifyLoginView(APIView):
    """POST：登录时密码通过后，用 temp_token + code 换取 JWT"""
    permission_classes = [AllowAny]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        temp_token = request.data.get('temp_token')
        code = (request.data.get('code') or '').strip()
        if not temp_token:
            return Response({'code': 40000, 'error': '缺少 temp_token'}, status=status.HTTP_400_BAD_REQUEST)
        if len(code) != 6:
            return Response({'code': 40000, 'error': '请输入 6 位验证码'}, status=status.HTTP_400_BAD_REQUEST)
        user_id = get_pending_login(temp_token)
        if not user_id:
            return Response({'code': 40000, 'error': '临时凭证无效或已过期，请重新登录'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            delete_pending_login(temp_token)
            return Response({'code': 40000, 'error': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
        profile = getattr(user, 'profile', None)
        if not profile or not getattr(profile, 'totp_secret', None):
            delete_pending_login(temp_token)
            return Response({'code': 40000, 'error': '未开启双因素认证'}, status=status.HTTP_400_BAD_REQUEST)
        if not verify_totp(profile.totp_secret, code):
            return Response({'code': 40000, 'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        delete_pending_login(temp_token)
        refresh = RefreshToken.for_user(user)
        return Response({
            'code': 20000,
            'msg': 'Success',
            'user': user.username,
            'data': {
                'token': str(refresh.access_token),
                'refresh': str(refresh),
            },
        }, status=status.HTTP_200_OK)


class TwoFactorDisableView(APIView):
    """POST：关闭 2FA，需提交当前密码 + 6 位验证码"""
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        password = request.data.get('password')
        code = (request.data.get('code') or '').strip()
        if not password:
            return Response({'code': 40000, 'error': '请输入当前密码'}, status=status.HTTP_400_BAD_REQUEST)
        if len(code) != 6:
            return Response({'code': 40000, 'error': '请输入 6 位验证码'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if not user.check_password(password):
            return Response({'code': 40000, 'error': '密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        profile = getattr(user, 'profile', None)
        if not profile or not getattr(profile, 'totp_enabled', False):
            return Response({'code': 40000, 'error': '未开启双因素认证'}, status=status.HTTP_400_BAD_REQUEST)
        if not verify_totp(profile.totp_secret, code):
            return Response({'code': 40000, 'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        profile.totp_secret = ''
        profile.totp_enabled = False
        profile.save()
        return Response({'code': 20000, 'msg': '双因素认证已关闭'})