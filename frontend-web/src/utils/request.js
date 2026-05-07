import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      const { status, data } = error.response

      if (status === 401) {
        // 如果当前在登录页面，不自动重定向，让登录页面自己处理错误
        if (window.location.pathname === '/login') {
          ElMessage.error(data.detail || '用户名或密码错误')
        } else {
          localStorage.removeItem('token')
          window.location.href = '/login'
          ElMessage.error('登录已过期,请重新登录')
        }
      } else if (status === 403) {
        ElMessage.error('没有权限访问')
      } else if (status === 404) {
        ElMessage.error('请求的资源不存在')
      } else if (status >= 500) {
        ElMessage.error('服务器错误,请稍后重试')
      } else {
        ElMessage.error(data.message || '请求失败')
      }
    } else {
      ElMessage.error('网络错误,请检查网络连接')
    }

    return Promise.reject(error)
  }
)

export default api
