# BUG-003: 数据看板未同步测试用例实时数据

**日期**: 2026-04-22  
**严重程度**: 🟡 Medium  
**状态**: ✅ 已解决  
**影响范围**: 数据看板页面显示静态数据，未实时获取测试用例统计

---

## 问题现象

数据看板页面（`/dashboard`）中：
1. 测试用例优先级分布图显示的是写死的模拟数据
2. 测试用例状态统计图显示的是写死的模拟数据
3. 统计卡片中的"测试用例数"能正确显示，但图表数据未同步

---

## 根因分析

`frontend-web/src/views/Dashboard.vue` 中的图表初始化函数使用了硬编码的模拟数据：

```javascript
// 优先级分布 - 硬编码数据
data: [
  { value: 10, name: '紧急' },
  { value: 25, name: '高' },
  { value: 45, name: '中' },
  { value: 20, name: '低' }
]

// 状态统计 - 硬编码数据
data: [
  { value: 30, itemStyle: { color: '#909399' } }, // 草稿
  { value: 65, itemStyle: { color: '#67c23a' } }, // 有效
  { value: 5, itemStyle: { color: '#e6a23c' } }   // 已废弃
]
```

未从后端 API 获取真实的测试用例数据进行统计。

---

## 修复内容

### 1) 增强 `loadStats` 函数

**文件**: `frontend-web/src/views/Dashboard.vue`

修改前：
```javascript
const loadStats = async () => {
  const [questions, testcases] = await Promise.allSettled([
    request({ url: '/api/questions/', method: 'get', params: { limit: 1 } }),
    request({ url: '/api/testcases/', method: 'get', params: { limit: 1 } })
  ])
  // 只更新统计卡片，不更新图表
}
```

修改后：
```javascript
const loadStats = async () => {
  const [questions, users, activities, testcases, testcaseStats, userRoles] = await Promise.allSettled([
    request({ url: '/api/questions/', method: 'get', params: { limit: 1 } }),
    request({ url: '/api/users/', method: 'get', params: { limit: 1 } }),
    request({ url: '/api/activities/', method: 'get', params: { limit: 1 } }),
    request({ url: '/api/testcases/', method: 'get', params: { limit: 1 } }),
    request({ url: '/api/testcases/', method: 'get', params: { limit: 10000 } }), // 获取所有数据用于统计
    request({ url: '/api/stats/user_distribution/', method: 'get' })
  ])
  
  // 更新所有统计卡片
  // 更新测试用例图表
  if (testcaseStats.status === 'fulfilled') {
    updateTestcaseCharts(testcaseStats.value.results)
  }
}
```

### 2) 新增 `updateTestcaseCharts` 函数

实时统计测试用例的优先级和状态分布：

```javascript
const updateTestcaseCharts = (testcases) => {
  // 统计优先级分布
  const priorityCount = { critical: 0, high: 0, medium: 0, low: 0 }
  const statusCount = { draft: 0, active: 0, deprecated: 0 }

  testcases.forEach(tc => {
    priorityCount[tc.priority] = (priorityCount[tc.priority] || 0) + 1
    statusCount[tc.status] = (statusCount[tc.status] || 0) + 1
  })

  // 动态更新图表数据
  charts[0].setOption({ series: [{ data: [...] }] })
  charts[1].setOption({ series: [{ data: [...] }] })
}
```

### 3) 更新所有统计卡片

现在所有4个统计卡片都从真实API获取数据：
- 题目总数：`/api/questions/`
- 用户总数：`/api/users/`
- 活动总数：`/api/activities/`
- 测试用例数：`/api/testcases/`

---

## 验证结果

- ✅ 统计卡片显示真实数据
- ✅ 测试用例优先级分布图显示真实数据（6个紧急、7个高、6个中、1个低）
- ✅ 测试用例状态统计图显示真实数据（0个草稿、20个有效、0个已废弃）
- ✅ 数据实时同步，刷新页面后显示最新数据

---

## 预防措施

1. 所有统计图表应从真实API获取数据，避免使用硬编码的模拟数据
2. 在开发阶段使用模拟数据时，应添加 TODO 注释标记
3. 数据看板应定期刷新数据，或提供手动刷新按钮

---

## 相关问题

- BUG-002: 前端登录接口 404（已解决）
- 所有 API 路径已统一添加 `/api` 前缀

---

**修复人**: Claude Sonnet 4.6  
**最后更新**: 2026-04-22
