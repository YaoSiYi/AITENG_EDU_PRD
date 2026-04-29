import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')

  async function login(credentials) {
    const response = await api.post('/api/users/login/', credentials)
    token.value = response.access
    localStorage.setItem('token', response.access)
    user.value = response.user
    return response
  }

  async function register(userData) {
    const response = await api.post('/api/users/register/', userData)
    return response
  }

  async function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  async function checkAuth() {
    try {
      const response = await api.get('/api/users/profile/')
      user.value = response
    } catch (error) {
      logout()
    }
  }

  async function updateProfile(data) {
    const response = await api.put('/api/users/update_profile/', data)
    user.value = response
    return response
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    isTeacher,
    isStudent,
    login,
    register,
    logout,
    checkAuth,
    updateProfile
  }
})
