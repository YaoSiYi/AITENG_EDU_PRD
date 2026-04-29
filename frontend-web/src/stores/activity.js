import { defineStore } from 'pinia'
import { ref } from 'vue'
import { activityApi } from '@/api'

export const useActivityStore = defineStore('activity', () => {
  const activities = ref([])
  const loading = ref(false)

  // 获取活动列表
  async function fetchActivities(params = {}) {
    loading.value = true
    try {
      const data = await activityApi.getActivities(params)
      activities.value = data.results || data
      return data
    } catch (error) {
      console.error('获取活动列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取活动详情
  async function fetchActivityDetail(id) {
    loading.value = true
    try {
      const data = await activityApi.getActivity(id)
      return data
    } catch (error) {
      console.error('获取活动详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建活动
  async function createActivity(activityData) {
    loading.value = true
    try {
      const data = await activityApi.createActivity(activityData)
      return data
    } catch (error) {
      console.error('创建活动失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 参与活动
  async function participateActivity(id, formData) {
    loading.value = true
    try {
      const data = await activityApi.participate(id, formData)
      return data
    } catch (error) {
      console.error('参与活动失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    activities,
    loading,
    fetchActivities,
    fetchActivityDetail,
    createActivity,
    participateActivity
  }
})
