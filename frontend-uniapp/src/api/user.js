/**
 * 用户相关API
 */
import request from '@/utils/request'

/**
 * 用户注册
 * @param {Object} data - 注册信息
 */
export function register(data) {
  return request.post('/users/register/', data, { auth: false })
}

/**
 * 用户登录
 * @param {Object} data - 登录信息 { username, password }
 */
export function login(data) {
  return request.post('/users/login/', data, { auth: false })
}

/**
 * 获取用户信息
 */
export function getUserProfile() {
  return request.get('/users/profile/')
}

/**
 * 更新用户信息
 * @param {Object} data - 用户信息
 */
export function updateUserProfile(data) {
  return request.put('/users/profile/', data)
}

/**
 * 修改密码
 * @param {Object} data - { old_password, new_password, confirm_password }
 */
export function changePassword(data) {
  return request.post('/users/change-password/', data)
}

/**
 * 获取用户列表（管理员）
 * @param {Object} params - 查询参数
 */
export function getUserList(params) {
  return request.get('/users/', params)
}
