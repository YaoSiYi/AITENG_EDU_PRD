/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { login, getUserProfile, updateUserProfile } from '@/api/user'
import { setToken, getToken, removeToken, setUserInfo, getUserInfo, removeUserInfo } from '@/utils/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getToken() || '',
    userInfo: getUserInfo() || null,
    isLoggedIn: false
  }),

  getters: {
    // 是否已登录
    hasLogin: (state) => !!state.token,

    // 用户角色
    userRole: (state) => state.userInfo?.role || 'guest',

    // 用户昵称
    nickname: (state) => state.userInfo?.nickname || '游客',

    // 用户头像
    avatar: (state) => state.userInfo?.avatar || '/static/images/default-avatar.png'
  },

  actions: {
    /**
     * 登录
     * @param {Object} loginForm - { username, password }
     */
    async login(loginForm) {
      try {
        const res = await login(loginForm)

        // 保存token
        this.token = res.access
        setToken(res.access)

        // 保存用户信息
        this.userInfo = res.user
        setUserInfo(res.user)

        this.isLoggedIn = true

        return res
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },

    /**
     * 微信登录
     * @param {String} code - 微信授权code
     */
    async wechatLogin(code) {
      try {
        // TODO: 调用微信登录接口
        const res = await login({ code, login_type: 'wechat' })

        this.token = res.access
        setToken(res.access)

        this.userInfo = res.user
        setUserInfo(res.user)

        this.isLoggedIn = true

        return res
      } catch (error) {
        console.error('Wechat login error:', error)
        throw error
      }
    },

    /**
     * 获取用户信息
     */
    async fetchUserInfo() {
      try {
        const res = await getUserProfile()
        this.userInfo = res
        setUserInfo(res)
        return res
      } catch (error) {
        console.error('Fetch user info error:', error)
        throw error
      }
    },

    /**
     * 更新用户信息
     * @param {Object} data - 用户信息
     */
    async updateProfile(data) {
      try {
        const res = await updateUserProfile(data)
        this.userInfo = res
        setUserInfo(res)
        return res
      } catch (error) {
        console.error('Update profile error:', error)
        throw error
      }
    },

    /**
     * 登出
     */
    logout() {
      this.token = ''
      this.userInfo = null
      this.isLoggedIn = false

      removeToken()
      removeUserInfo()

      // 跳转到登录页
      uni.reLaunch({
        url: '/pages/login/login'
      })
    },

    /**
     * 检查登录状态
     */
    checkLogin() {
      const token = getToken()
      const userInfo = getUserInfo()

      if (token && userInfo) {
        this.token = token
        this.userInfo = userInfo
        this.isLoggedIn = true
        return true
      }

      return false
    }
  }
})
