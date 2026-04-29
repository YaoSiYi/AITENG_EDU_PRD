import request from '@/utils/request'

/**
 * 测试用例 CRUD API
 * - list: GET /api/testcases/  列表
 * - create: POST /api/testcases/  新建
 * - retrieve: GET /api/testcases/{id}/  详情
 * - update: PUT /api/testcases/{id}/  全量更新
 * - partial_update: PATCH /api/testcases/{id}/  部分更新
 * - destroy: DELETE /api/testcases/{id}/  删除
 */

/** 列表 GET /api/testcases/ */
export function getTestcaseList(params) {
  return request({
    url: '/api/testcases/',
    method: 'get',
    params
  })
}

/** 新建 POST /api/testcases/ */
export function createTestcase(data) {
  return request({
    url: '/api/testcases/',
    method: 'post',
    data
  })
}

/** 详情 GET /api/testcases/{id}/ */
export function getTestcaseDetail(id) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'get'
  })
}

/** 全量更新 PUT /api/testcases/{id}/ */
export function updateTestcase(id, data) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'put',
    data
  })
}

/** 部分更新 PATCH /api/testcases/{id}/ */
export function partialUpdateTestcase(id, data) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'patch',
    data
  })
}

/** 删除 DELETE /api/testcases/{id}/ */
export function deleteTestcase(id) {
  return request({
    url: `/api/testcases/${id}/`,
    method: 'delete'
  })
}

/** 导出 GET /api/testcases/export/，带当前筛选 query，返回文件流 */
export function exportTestcases(params) {
  return request({
    url: '/api/testcases/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/** 模板下载 GET /api/testcases/template/ */
export function downloadTestcaseTemplate() {
  return request({
    url: '/api/testcases/template/',
    method: 'get',
    responseType: 'blob'
  })
}

/** 导入 POST /api/testcases/import/，FormData 含 file 字段，返回 { created, failed, errors } */
export function importTestcases(formData) {
  return request({
    url: '/api/testcases/import/',
    method: 'post',
    data: formData
  })
}
