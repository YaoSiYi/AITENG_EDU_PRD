import request from '@/utils/request'

/**
 * 测试用例管理 API
 */

// 获取测试用例列表
export function getTestcaseList(params) {
  return request({
    url: '/api/testcases/',
    method: 'get',
    params
  })
}

// 创建测试用例
export function createTestcase(data) {
  return request({
    url: '/api/testcases/',
    method: 'post',
    data
  })
}

// 获取测试用例详情
export function getTestcaseDetail(id) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'get'
  })
}

// 更新测试用例
export function updateTestcase(id, data) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'put',
    data
  })
}

// 部分更新测试用例
export function partialUpdateTestcase(id, data) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'patch',
    data
  })
}

// 删除测试用例
export function deleteTestcase(id) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'delete'
  })
}

// 导出测试用例
export function exportTestcases(params) {
  return request({
    url: '/api/testcases/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// 下载导入模板
export function downloadTestcaseTemplate() {
  return request({
    url: '/api/testcases/template/',
    method: 'get',
    responseType: 'blob'
  })
}

// 导入测试用例
export function importTestcases(formData) {
  return request({
    url: '/api/testcases/import/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取可指派的用户列表
export function getAssignableUsers() {
  return request({
    url: '/api/testcases/users/',
    method: 'get'
  })
}
