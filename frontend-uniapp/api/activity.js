/**
 * 活动相关API
 */
import request from '@/utils/request'

/**
 * 获取活动列表
 * @param {Object} params - 查询参数 { status, page, page_size }
 */
export function getActivityList(params) {
  return request.get('/activities/', params)
}

/**
 * 获取活动详情
 * @param {Number} id - 活动ID
 */
export function getActivityDetail(id) {
  return request.get(`/activities/${id}/`)
}

/**
 * 创建活动
 * @param {Object} data - 活动信息
 */
export function createActivity(data) {
  return request.post('/activities/', data)
}

/**
 * 参与活动
 * @param {Number} id - 活动ID
 */
export function joinActivity(id) {
  return request.post(`/activities/${id}/join/`)
}

/**
 * 取消参与
 * @param {Number} id - 活动ID
 */
export function cancelActivity(id) {
  return request.post(`/activities/${id}/cancel/`)
}

/**
 * 活动签到
 * @param {Number} id - 活动ID
 */
export function checkInActivity(id) {
  return request.post(`/activities/${id}/checkin/`)
}

/**
 * 获取我参与的活动
 * @param {Object} params - 查询参数
 */
export function getMyActivities(params) {
  return request.get('/activities/my/', params)
}
