"""
Google 验证器 (TOTP) 工具：生成密钥、验证码、QR 用的 otpauth URI
"""
import pyotp
from django.core.cache import cache
from django.conf import settings


def get_totp_secret():
    """生成新的 TOTP 密钥（base32）"""
    return pyotp.random_base32()


def get_provisioning_uri(secret, username, issuer_name=None):
    """生成 otpauth URI，供前端生成二维码或手动输入"""
    issuer = issuer_name or getattr(settings, 'TOTP_ISSUER_NAME', 'DjangoProject')
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)


def verify_totp(secret, code):
    """验证 6 位 TOTP 验证码，允许当前及前后 1 个时间窗（约 ±30 秒）"""
    if not secret or not code or len(code) != 6:
        return False
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


# 缓存 key 前缀与过期时间
TOTP_SETUP_PREFIX = '2fa_setup_'
TOTP_SETUP_TIMEOUT = 600  # 10 分钟
TOTP_PENDING_PREFIX = '2fa_pending_'
TOTP_PENDING_TIMEOUT = 300  # 5 分钟


def set_pending_setup(user_id, secret):
    """开启 2FA 流程：将待确认的 secret 放入缓存"""
    cache.set(f'{TOTP_SETUP_PREFIX}{user_id}', secret, timeout=TOTP_SETUP_TIMEOUT)


def get_pending_setup(user_id):
    """获取待确认的 secret，用后可由调用方决定是否删除"""
    return cache.get(f'{TOTP_SETUP_PREFIX}{user_id}')


def delete_pending_setup(user_id):
    cache.delete(f'{TOTP_SETUP_PREFIX}{user_id}')


def set_pending_login(temp_token, user_id):
    """登录时需二次验证：临时 token -> user_id"""
    cache.set(f'{TOTP_PENDING_PREFIX}{temp_token}', user_id, timeout=TOTP_PENDING_TIMEOUT)


def get_pending_login(temp_token):
    """根据临时 token 取 user_id，验证成功后应删除"""
    return cache.get(f'{TOTP_PENDING_PREFIX}{temp_token}')


def delete_pending_login(temp_token):
    cache.delete(f'{TOTP_PENDING_PREFIX}{temp_token}')
