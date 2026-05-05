// ⚠️ 此文件已废弃，请使用 utils/request.js
// 为了兼容性保留，但建议统一使用 utils/request.js

const BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://www.aitengjiaoyu.top/api'
  : 'http://192.168.0.156:8000/api'

class Request {
  request(options) {
    return new Promise((resolve, reject) => {
      const token = uni.getStorageSync('token')

      uni.request({
        url: BASE_URL + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
          ...options.header
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data)
          } else if (res.statusCode === 401) {
            uni.removeStorageSync('token')
            uni.showToast({
              title: '登录已过期',
              icon: 'none'
            })
            uni.navigateTo({
              url: '/pages/login/login'
            })
            reject(res)
          } else {
            uni.showToast({
              title: res.data.message || '请求失败',
              icon: 'none'
            })
            reject(res)
          }
        },
        fail: (err) => {
          uni.showToast({
            title: '网络错误',
            icon: 'none'
          })
          reject(err)
        }
      })
    })
  }

  get(url, data) {
    return this.request({
      url,
      method: 'GET',
      data
    })
  }

  post(url, data) {
    return this.request({
      url,
      method: 'POST',
      data
    })
  }

  put(url, data) {
    return this.request({
      url,
      method: 'PUT',
      data
    })
  }

  delete(url, data) {
    return this.request({
      url,
      method: 'DELETE',
      data
    })
  }
}

export default new Request()
