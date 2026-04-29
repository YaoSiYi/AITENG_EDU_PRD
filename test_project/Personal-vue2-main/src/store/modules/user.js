import { login, logout, refreshToken, getUserInfo, verifyLogin2FA } from '@/api/user'
import { getToken, getRefreshToken, setToken, setRefreshToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'
import watermark from '@/watermark'
const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    roles: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username, password: password }).then(response => {
        const data = (response && response.data !== undefined) ? response.data : response
        if (data.require_2fa && data.temp_token) {
          resolve({ require2fa: true, tempToken: data.temp_token })
          return
        }
        const access = data.token || data.access
        const refresh = data.refresh
        if (access) {
          commit('SET_TOKEN', access)
          setToken(access)
          setRefreshToken(refresh)
        }
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 2FA 验证登录：temp_token + code 换 JWT
  loginWith2FA({ commit }, { tempToken, code }) {
    return new Promise((resolve, reject) => {
      verifyLogin2FA(tempToken, code).then(response => {
        const data = (response && response.data !== undefined) ? response.data : response
        const access = data.token || data.access
        const refresh = data.refresh
        if (access) {
          commit('SET_TOKEN', access)
          setToken(access)
          setRefreshToken(refresh)
        }
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // refresh token
  refreshToken({ commit }) {
    return new Promise((resolve, reject) => {
      const refreshTokenValue = getRefreshToken()
      if (!refreshTokenValue) {
        reject(new Error('No refresh token found'))
        return
      }
      
      refreshToken(refreshTokenValue).then(response => {
        const { data } = response
        commit('SET_TOKEN', data.access)
        setToken(data.access)
        setRefreshToken(data.refresh)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getUserInfo(state.token).then(response => {
        const { data } = response
        
        const now = new Date() // Get current time
        const time_str = now.getFullYear() + '.' + (now.getMonth() + 1) + '.' + now.getDate() // Format time as string
        watermark.set(data.name + '\n' + time_str)

        const { roles, name } = data

        if (!roles || roles.length <= 0) {
          console.error('getInfo: roles must be a non-null array!')
          // 添加提示信息，告诉用户缺少角色信息
          this.$message && this.$message.error('用户角色信息缺失，无法进入系统，请联系管理员')
          reject('getInfo: roles must be a non-null array!')
        }

        commit('SET_ROLES', roles)
        commit('SET_NAME', name)
        resolve(data)
      }).catch(error => {
        console.error('获取用户信息失败:', error)
        this.$message && this.$message.error('获取用户信息失败，请重试')
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout().then(() => {
        removeToken() // Must remove token first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch((error) => {
        // Even without backend interface, we should logout normally
        console.error('Logout error:', error)
        removeToken()
        resetRouter()
        commit('RESET_STATE')
        resolve()
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // Must remove token first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}