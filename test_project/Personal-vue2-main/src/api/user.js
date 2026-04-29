import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/auth/login/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    }
  })
}

export function register(data) {
  return request({
    url: '/api/auth/register/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password,
      email: data.email
    }
  })
}

export function refreshToken(refreshToken) {
  return request({
    url: '/api/auth/token/refresh/',
    method: 'post',
    data: {
      refresh: refreshToken
    }
  })
}

export function getUserInfo(token) {
  return request({
    url: '/api/auth/info/',
    method: 'get',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
}

export function logout() {
  return request({
    url: '/api/auth/logout/',
    method: 'post'
  })
}

export function healthCheck() {
  return request({
    url: '/health/',
    method: 'get'
  })
}

// ---------- 2FA ----------

/** 是否已开启 2FA（需登录） */
export function get2FAStatus() {
  return request({
    url: '/api/auth/2fa/status/',
    method: 'get'
  })
}

/** 发起开启 2FA，返回 secret、qr_uri（需登录） */
export function setup2FA() {
  return request({
    url: '/api/auth/2fa/setup/',
    method: 'post'
  })
}

/** 提交 6 位验证码确认开启 2FA（需登录） */
export function confirm2FA(code) {
  return request({
    url: '/api/auth/2fa/confirm/',
    method: 'post',
    data: { code }
  })
}

/** 登录二次验证：temp_token + code 换 JWT（无需登录） */
export function verifyLogin2FA(tempToken, code) {
  return request({
    url: '/api/auth/2fa/verify-login/',
    method: 'post',
    data: { temp_token: tempToken, code }
  })
}

/** 关闭 2FA：当前密码 + 6 位验证码（需登录） */
export function disable2FA(password, code) {
  return request({
    url: '/api/auth/2fa/disable/',
    method: 'post',
    data: { password, code }
  })
}