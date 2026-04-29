/**
 * 认证工具函数
 * 处理Token、用户信息的存储和获取
 */

/**
 * 保存Token
 * @param {String} token - JWT Token
 */
export function setToken(token) {
  uni.setStorageSync('token', token)
}

/**
 * 获取Token
 * @returns {String} token
 */
export function getToken() {
  return uni.getStorageSync('token') || ''
}

/**
 * 移除Token
 */
export function removeToken() {
  uni.removeStorageSync('token')
}

/**
 * 保存用户信息
 * @param {Object} userInfo - 用户信息对象
 */
export function setUserInfo(userInfo) {
  uni.setStorageSync('userInfo', JSON.stringify(userInfo))
}

/**
 * 获取用户信息
 * @returns {Object} userInfo
 */
export function getUserInfo() {
  const userInfo = uni.getStorageSync('userInfo')
  return userInfo ? JSON.parse(userInfo) : null
}

/**
 * 移除用户信息
 */
export function removeUserInfo() {
  uni.removeStorageSync('userInfo')
}

/**
 * 检查是否已登录
 * @returns {Boolean}
 */
export function isLoggedIn() {
  return !!getToken()
}

/**
 * 清除所有认证信息
 */
export function clearAuth() {
  removeToken()
  removeUserInfo()
}

/**
 * 登出
 */
export function logout() {
  clearAuth()
  uni.reLaunch({
    url: '/pages/login/login'
  })
}
