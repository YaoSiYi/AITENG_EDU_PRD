/**
 * HTTP请求封装
 * 统一处理API请求、Token认证、错误处理
 */

const BASE_URL = 'http://localhost:8000/api'

/**
 * 发起HTTP请求
 * @param {Object} options - 请求配置
 * @param {String} options.url - 请求路径
 * @param {String} options.method - 请求方法
 * @param {Object} options.data - 请求数据
 * @param {Boolean} options.auth - 是否需要认证
 */
function request(options) {
  return new Promise((resolve, reject) => {
    // 获取Token
    const token = uni.getStorageSync('token')

    // 构建请求头
    const header = {
      'Content-Type': 'application/json'
    }

    // 如果需要认证且有token，添加Authorization头
    if (options.auth !== false && token) {
      header['Authorization'] = `Bearer ${token}`
    }

    // 显示加载提示
    if (options.loading !== false) {
      uni.showLoading({
        title: '加载中...',
        mask: true
      })
    }

    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: header,
      timeout: options.timeout || 10000,
      success: (res) => {
        // 隐藏加载提示
        if (options.loading !== false) {
          uni.hideLoading()
        }

        // 请求成功
        if (res.statusCode === 200 || res.statusCode === 201) {
          resolve(res.data)
        }
        // Token过期或无效
        else if (res.statusCode === 401) {
          uni.showToast({
            title: '登录已过期，请重新登录',
            icon: 'none',
            duration: 2000
          })

          // 清除token并跳转到登录页
          uni.removeStorageSync('token')
          uni.removeStorageSync('userInfo')

          setTimeout(() => {
            uni.reLaunch({
              url: '/pages/login/login'
            })
          }, 2000)

          reject(new Error('Token expired'))
        }
        // 其他错误
        else {
          const errorMsg = res.data?.message || res.data?.detail || '请求失败'
          uni.showToast({
            title: errorMsg,
            icon: 'none',
            duration: 2000
          })
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        // 隐藏加载提示
        if (options.loading !== false) {
          uni.hideLoading()
        }

        // 网络错误
        uni.showToast({
          title: '网络连接失败',
          icon: 'none',
          duration: 2000
        })

        reject(err)
      }
    })
  })
}

// 导出便捷方法
export default {
  get(url, data, options = {}) {
    return request({
      url,
      method: 'GET',
      data,
      ...options
    })
  },

  post(url, data, options = {}) {
    return request({
      url,
      method: 'POST',
      data,
      ...options
    })
  },

  put(url, data, options = {}) {
    return request({
      url,
      method: 'PUT',
      data,
      ...options
    })
  },

  delete(url, data, options = {}) {
    return request({
      url,
      method: 'DELETE',
      data,
      ...options
    })
  },

  // 原始request方法
  request
}
