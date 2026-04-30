/**
 * 题库状态管理
 */
import { defineStore } from 'pinia'
import {
  getQuestionList,
  getQuestionDetail,
  getRandomQuestions,
  getCategories,
  getWrongQuestions,
  addToWrongBook,
  markAsMastered,
  removeFromWrongBook
} from '@/api/question'

export const useQuestionStore = defineStore('question', {
  state: () => ({
    // 题目列表
    questionList: [],
    // 当前题目
    currentQuestion: null,
    // 分类列表
    categories: [],
    // 错题本
    wrongQuestions: [],
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
     * 获取题目列表
     * @param {Object} params - 查询参数
     */
    async fetchQuestionList(params = {}) {
      try {
        this.loading = true
        const res = await getQuestionList({
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          ...params
        })

        if (params.page === 1) {
          this.questionList = res.results
        } else {
          this.questionList.push(...res.results)
        }

        this.pagination.total = res.count
        this.pagination.page = params.page || 1

        return res
      } catch (error) {
        console.error('Fetch question list error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    /**
     * 加载更多题目
     */
    async loadMore(params = {}) {
      if (!this.hasMore || this.loading) return

      this.pagination.page += 1
      return this.fetchQuestionList({
        ...params,
        page: this.pagination.page
      })
    },

    /**
     * 获取题目详情
     * @param {Number} id - 题目ID
     */
    async fetchQuestionDetail(id) {
      try {
        const res = await getQuestionDetail(id)
        this.currentQuestion = res
        return res
      } catch (error) {
        console.error('Fetch question detail error:', error)
        throw error
      }
    },

    /**
     * 获取随机题目
     * @param {Object} params - { stage, category, count }
     */
    async fetchRandomQuestions(params) {
      try {
        const res = await getRandomQuestions(params)
        return res
      } catch (error) {
        console.error('Fetch random questions error:', error)
        throw error
      }
    },

    /**
     * 获取分类列表
     * @param {Number} stage - 阶段
     */
    async fetchCategories(stage) {
      try {
        const res = await getCategories({ stage })
        this.categories = res
        return res
      } catch (error) {
        console.error('Fetch categories error:', error)
        throw error
      }
    },

    /**
     * 获取错题本
     * @param {Object} params - 查询参数
     */
    async fetchWrongQuestions(params = {}) {
      try {
        const res = await getWrongQuestions(params)
        this.wrongQuestions = res.results || res
        return res
      } catch (error) {
        console.error('Fetch wrong questions error:', error)
        throw error
      }
    },

    /**
     * 添加到错题本
     * @param {Number} questionId - 题目ID
     */
    async addToWrong(questionId) {
      try {
        const res = await addToWrongBook(questionId)
        uni.showToast({
          title: '已加入错题本',
          icon: 'success'
        })
        return res
      } catch (error) {
        console.error('Add to wrong book error:', error)
        throw error
      }
    },

    /**
     * 标记已掌握
     * @param {Number} id - 错题记录ID
     */
    async markMastered(id) {
      try {
        const res = await markAsMastered(id)

        // 更新本地数据
        const index = this.wrongQuestions.findIndex(item => item.id === id)
        if (index !== -1) {
          this.wrongQuestions[index].is_mastered = true
        }

        uni.showToast({
          title: '已标记为掌握',
          icon: 'success'
        })

        return res
      } catch (error) {
        console.error('Mark as mastered error:', error)
        throw error
      }
    },

    /**
     * 从错题本移除
     * @param {Number} id - 错题记录ID
     */
    async removeFromWrong(id) {
      try {
        await removeFromWrongBook(id)

        // 更新本地数据
        this.wrongQuestions = this.wrongQuestions.filter(item => item.id !== id)

        uni.showToast({
          title: '已移出错题本',
          icon: 'success'
        })
      } catch (error) {
        console.error('Remove from wrong book error:', error)
        throw error
      }
    }
  }
})
