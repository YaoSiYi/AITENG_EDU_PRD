/**
 * 本地存储工具函数
 * 封装uni.storage API，提供更便捷的使用方式
 */

/**
 * 设置存储
 * @param {String} key - 键名
 * @param {Any} value - 值（自动JSON序列化）
 */
export function setStorage(key, value) {
  try {
    const data = typeof value === 'object' ? JSON.stringify(value) : value
    uni.setStorageSync(key, data)
    return true
  } catch (e) {
    console.error('setStorage error:', e)
    return false
  }
}

/**
 * 获取存储
 * @param {String} key - 键名
 * @param {Any} defaultValue - 默认值
 * @returns {Any}
 */
export function getStorage(key, defaultValue = null) {
  try {
    const value = uni.getStorageSync(key)
    if (!value) return defaultValue

    // 尝试解析JSON
    try {
      return JSON.parse(value)
    } catch {
      return value
    }
  } catch (e) {
    console.error('getStorage error:', e)
    return defaultValue
  }
}

/**
 * 移除存储
 * @param {String} key - 键名
 */
export function removeStorage(key) {
  try {
    uni.removeStorageSync(key)
    return true
  } catch (e) {
    console.error('removeStorage error:', e)
    return false
  }
}

/**
 * 清空所有存储
 */
export function clearStorage() {
  try {
    uni.clearStorageSync()
    return true
  } catch (e) {
    console.error('clearStorage error:', e)
    return false
  }
}

/**
 * 获取存储信息
 * @returns {Object} { keys, currentSize, limitSize }
 */
export function getStorageInfo() {
  try {
    return uni.getStorageInfoSync()
  } catch (e) {
    console.error('getStorageInfo error:', e)
    return null
  }
}
