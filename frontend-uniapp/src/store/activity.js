/**
 * 活动状态管理
 */
import { defineStore } from 'pinia'
import {
  getActivityList,
  getActivityDetail,
  createActivity,
  joinActivity,
  cancelActivity,
  checkInActivity,
  getMyActivities
} from '@/api/activity'

export const useActivityStore = defineStore('activity', {
  state: () => ({
    // 活动列表
    activityList: [],
    // 当前活动
    currentActivity: null,
    // 我的活动
    myActivities: [],
    // 加载状态
    loading: false,
    // 分页信息
    pagination: {
      page: 1,
      pageSize: 20,
      total: 0
    }
  }),

  getters: {
    // 是否有更多数据
    hasMore: (state) => {
      return state.pagination.page * state.pagination.pageSize < state.pagination.total
    }
  },

  actions: {
    /**
     * 获取活动列表
     * @param {Object} params - 查询参数
     */
    async fetchActivityList(params = {}) {
      try {
        this.loading = true
        const res = await getActivityList({
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          ...params
        })

        if (params.page === 1) {
          this.activityList = res.results
        } else {
          this.activityList.push(...res.results)
        }

        this.pagination.total = res.count
        this.pagination.page = params.page || 1

        return res
      } catch (error) {
        console.error('Fetch activity list error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 加载更多活动
     */
    async loadMore(params = {}) {
      if (!this.hasMore || this.loading) return

      this.pagination.page += 1
      return this.fetchActivityList({
        ...params,
        page: this.pagination.page
      })
    },

    /**
     * 获取活动详情
     * @param {Number} id - 活动ID
     */
    async fetchActivityDetail(id) {
      try {
        const res = await getActivityDetail(id)
        this.currentActivity = res
        return res
      } catch (error) {
        console.error('Fetch activity detail error:', error)
        throw error
      }
    },

    /**
     * 创建活动
     * @param {Object} data - 活动信息
     */
    async create(data) {
      try {
        const res = await createActivity(data)
        uni.showToast({
          title: '活动创建成功',
          icon: 'success'
        })
        return res
      } catch (error) {
        console.error('Create activity error:', error)
        throw error
      }
    },

    /**
     * 参与活动
     * @param {Number} id - 活动ID
     */
    async join(id) {
      try {
        const res = await joinActivity(id)

        // 更新本地数据
        const activity = this.activityList.find(item => item.id === id)
        if (activity) {
          activity.is_joined = true
          activity.participant_count += 1
        }

        uni.showToast({
          title: '报名成功',
          icon: 'success'
        })

        return res
      } catch (error) {
        console.error('Join activity error:', error)
        throw error
      }
    },

    /**
     * 取消参与
     * @param {Number} id - 活动ID
     */
    async cancel(id) {
      try {
        const res = await cancelActivity(id)

        // 更新本地数据
        const activity = this.activityList.find(item => item.id === id)
        if (activity) {
          activity.is_joined = false
          activity.participant_count -= 1
        }

        uni.showToast({
          title: '已取消报名',
          icon: 'success'
        })

        return res
      } catch (error) {
        console.error('Cancel activity error:', error)
        throw error
      }
    },

    /**
     * 活动签到
     * @param {Number} id - 活动ID
     */
    async checkIn(id) {
      try {
        const res = await checkInActivity(id)
        uni.showToast({
          title: '签到成功',
          icon: 'success'
        })
        return res
      } catch (error) {
        console.error('Check in activity error:', error)
        throw error
      }
    },

    /**
     * 获取我的活动
     */
    async fetchMyActivities() {
      try {
        const res = await getMyActivities()
        this.myActivities = res.results || res
        return res
      } catch (error) {
        console.error('Fetch my activities error:', error)
        throw error
      }
    }
  }
})
