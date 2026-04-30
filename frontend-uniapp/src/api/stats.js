/**
 * 统计相关API
 */
import request from '@/utils/request'

/**
 * 获取首页统计数据
 */
export function getHomeStats() {
  return request.get('/stats/home/')
}

/**
 * 获取学员地域分布
 * @param {Object} params - { period }
 */
export function getStudentDistribution(params) {
  return request.get('/stats/student-distribution/', params)
}

/**
 * 获取就业城市分布
 */
export function getEmploymentCities() {
  return request.get('/stats/employment-cities/')
}

/**
 * 获取最高薪资排行
 * @param {Object} params - { limit }
 */
export function getTopSalaries(params) {
  return request.get('/stats/top-salaries/', params)
}

/**
 * 获取优秀学员
 * @param {Object} params - { limit }
 */
export function getExcellentStudents(params) {
  return request.get('/stats/excellent-students/', params)
}

/**
 * 获取高频面试题
 * @param {Object} params - { limit }
 */
export function getFrequentQuestions(params) {
  return request.get('/stats/frequent-questions/', params)
}

/**
 * 获取用户学习统计
 */
export function getUserStats() {
  return request.get('/stats/user/')
}
