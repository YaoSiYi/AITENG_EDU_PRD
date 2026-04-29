import { defineStore } from 'pinia'
import { ref } from 'vue'
import { questionApi } from '@/api'

export const useQuestionStore = defineStore('question', () => {
  const questions = ref([])
  const categories = ref([])
  const wrongQuestions = ref([])
  const loading = ref(false)

  // 获取题目列表
  async function fetchQuestions(params = {}) {
    loading.value = true
    try {
      const data = await questionApi.getQuestions(params)
      questions.value = data.results || data
      return data
    } catch (error) {
      console.error('获取题目列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取随机题目
  async function fetchRandomQuestions(params = {}) {
    loading.value = true
    try {
      const data = await questionApi.getRandomQuestions(params)
      return data
    } catch (error) {
      console.error('获取随机题目失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取题目详情
  async function fetchQuestionDetail(id) {
    loading.value = true
    try {
      const data = await questionApi.getQuestion(id)
      return data
    } catch (error) {
      console.error('获取题目详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取分类列表
  async function fetchCategories() {
    try {
      const data = await questionApi.getCategories()
      categories.value = data
      return data
    } catch (error) {
      console.error('获取分类列表失败:', error)
      throw error
    }
  }

  // 获取错题本
  async function fetchWrongQuestions() {
    loading.value = true
    try {
      const data = await questionApi.getWrongQuestions()
      wrongQuestions.value = data.results || data
      return data
    } catch (error) {
      console.error('获取错题本失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 添加错题
  async function addWrongQuestion(questionId) {
    try {
      const data = await questionApi.addWrongQuestion({ question_id: questionId })
      return data
    } catch (error) {
      console.error('添加错题失败:', error)
      throw error
    }
  }

  // 标记错题为已掌握
  async function markQuestionCorrect(id) {
    try {
      const data = await questionApi.markCorrect(id)
      return data
    } catch (error) {
      console.error('标记错题失败:', error)
      throw error
    }
  }

  return {
    questions,
    categories,
    wrongQuestions,
    loading,
    fetchQuestions,
    fetchRandomQuestions,
    fetchQuestionDetail,
    fetchCategories,
    fetchWrongQuestions,
    addWrongQuestion,
    markQuestionCorrect
  }
})
