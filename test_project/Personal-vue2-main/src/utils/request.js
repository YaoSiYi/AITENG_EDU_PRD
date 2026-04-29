import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken, getRefreshToken, setToken, setRefreshToken } from '@/utils/auth'

// 存储待处理请求和刷新token的promise
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  
  failedQueue = []
}

// 创建axios实例
const service = axios.create({
  // 开发环境不设置baseURL，让代理处理跨域问题
  // 生产环境使用完整的baseURL
  baseURL: process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BASE_API : '',
  timeout: 60 * 1000
})

// 服务拦截器请求
service.interceptors.request.use(
  config => {
    // 开发环境使用/api前缀让代理处理跨域问题
    // 仅对不以/api开头的路径添加/api前缀，避免重复添加
    if (process.env.NODE_ENV !== 'production' && !config.url.startsWith('/api/')) {
      // 检查是否已经有/api前缀，如果没有才添加
      if (!config.url.startsWith('/api')) {
        config.url = '/api' + (config.url.startsWith('/') ? config.url : '/' + config.url)
      }
    }
    
    // 检查是否需要添加Authorization头（refreshToken请求不需要）
    if (store.getters.token && 
        config.headers && 
        config.headers['Authorization'] !== false &&
        !config.headers['Authorization']) {
      config.headers['Authorization'] = `Bearer ${getToken()}`
    }
    
    // 如果是FormData对象，不设置Content-Type头部，让浏览器自动设置boundary
    if (config.data instanceof FormData) {
      config.headers['Content-Type'] = undefined
    }
    
    return config
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)

// 服务拦截器响应
service.interceptors.response.use(
  response => {
    const res = response.data
    // 兼容 Django REST 等直接返回 JSON 的后端（无 code 字段时直接返回数据）
    if (response.status >= 200 && response.status < 300 && (res === null || typeof res !== 'object' || res.code === undefined)) {
      return res
    }
    if (res.code === 20000) {
      return res
    }
    if (res.code === 50008) {
      MessageBox.confirm('登录已经失效，请重新登录', '通知', {
        confirmButtonText: '重新登录',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        store.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      })
      return Promise.reject(new Error('登录已经失效，请重新登录'))
    }
    Message({
      message: res.msg,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(new Error(res.message || 'Error'))
  },
  async error => {
    const originalRequest = error.config
    
    if (error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`
          return service(originalRequest)
        }).catch(err => {
          return Promise.reject(err)
        })
      }
      
      originalRequest._retry = true
      isRefreshing = true
      
      try {
        const refreshTokenValue = getRefreshToken()
        if (!refreshTokenValue) {
          throw new Error('No refresh token')
        }
        
        // 根据环境决定使用哪种路径
        let refreshUrl = '/auth/token/refresh/'
        if (process.env.NODE_ENV !== 'production') {
          // 开发环境使用代理路径
          refreshUrl = '/api' + refreshUrl
        }
        
        // 直接调用axios而不是使用API函数，避免循环引用和认证头问题
        const response = await axios.post(refreshUrl, {
          refresh: refreshTokenValue
        })
        
        const { access, refresh } = response.data
        // 更新token
        store.commit('user/SET_TOKEN', access)
        // 保存新的token和refresh token
        setToken(access)
        setRefreshToken(refresh)
        
        processQueue(null, access)
        originalRequest.headers['Authorization'] = `Bearer ${access}`
        return service(originalRequest)
      } catch (err) {
        processQueue(err, null)
        store.dispatch('user/resetToken').then(() => {
          MessageBox.confirm('登录已经失效，请重新登录', '通知', {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            location.reload()
          })
        })
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }
    
    console.log(error)
    Message({
      message: '请求失败，请检查网络连接',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service