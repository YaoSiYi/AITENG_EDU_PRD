import { defineStore } from 'pinia'
import { ref } from 'vue'
import { statsApi } from '@/api'

export const useStatsStore = defineStore('stats', () => {
  const dashboard = ref(null)
  const loading = ref(false)

  // 获取首页统计
  async function fetchDashboard() {
    loading.value = true
    try {
      const data = await statsApi.getDashboard()
      dashboard.value = data
      return data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取学员分布
  async function fetchStudentDistribution(params = {}) {
    loading.value = true
    try {
      const data = await statsApi.getStudentDistribution(params)
      return data
    } catch (error) {
      console.error('获取学员分布失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取用户分布
  async function fetchUserDistribution() {
    loading.value = true
    try {
      const data = await statsApi.getUserDistribution()
      return data
    } catch (error) {
      console.error('获取用户分布失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取就业城市分布
  async function fetchEmploymentCities() {
    loading.value = true
    try {
      const data = await statsApi.getEmploymentCities()
      return data
    } catch (error) {
      console.error('获取就业城市失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取最高薪资
  async function fetchTopSalaries() {
    loading.value = true
    try {
      const data = await statsApi.getTopSalaries()
      return data
    } catch (error) {
      console.error('获取薪资数据失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    dashboard,
    loading,
    fetchDashboard,
    fetchStudentDistribution,
    fetchUserDistribution,
    fetchEmploymentCities,
    fetchTopSalaries
  }
})
