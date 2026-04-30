/**
 * 题库相关API
 */
import request from '@/utils/request'

/**
 * 获取题目列表
 * @param {Object} params - 查询参数 { stage, category, difficulty, page, page_size }
 */
export function getQuestionList(params) {
  return request.get('/questions/', params)
}

/**
 * 获取题目详情
 * @param {Number} id - 题目ID
 */
export function getQuestionDetail(id) {
  return request.get(`/questions/${id}/`)
}

/**
 * 获取随机题目
 * @param {Object} params - { stage, category, count }
 */
export function getRandomQuestions(params) {
  return request.get('/questions/random/', params)
}

/**
 * 获取题目分类
 * @param {Object} params - { stage }
 */
export function getCategories(params) {
  return request.get('/questions/categories/', params)
}

/**
 * 提交答案
 * @param {Number} id - 题目ID
 * @param {Object} data - { answer }
 */
export function submitAnswer(id, data) {
  return request.post(`/questions/${id}/submit/`, data)
}

/**
 * 获取错题本
 * @param {Object} params - 查询参数
 */
export function getWrongQuestions(params) {
  return request.get('/questions/wrong-book/', params)
}

/**
 * 添加到错题本
 * @param {Number} questionId - 题目ID
 */
export function addToWrongBook(questionId) {
  return request.post('/questions/wrong-book/', { question_id: questionId })
}

/**
 * 标记已掌握
 * @param {Number} id - 错题记录ID
 */
export function markAsMastered(id) {
  return request.put(`/questions/wrong-book/${id}/`, { is_mastered: true })
}

/**
 * 从错题本移除
 * @param {Number} id - 错题记录ID
 */
export function removeFromWrongBook(id) {
  return request.delete(`/questions/wrong-book/${id}/`)
}
