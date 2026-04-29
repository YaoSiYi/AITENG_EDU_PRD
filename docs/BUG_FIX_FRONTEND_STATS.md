# Bug 修复记录 - 前台学员统计数据显示问题

## 更新日期：2026-04-24

---

## Bug 信息

### Bug ID: 28

### Bug 标题
[BUG] 前台主页学员统计数据显示为空

### 严重程度
高

### 优先级
高

### 状态
已关闭

### 模块
前端-首页

---

## 问题描述

前台主页右侧悬浮展示框中的"学员统计"和"就业统计"显示为空或显示为0，无法正常显示后端返回的数据。

---

## 前置条件

1. 后端服务器运行正常
2. 前端服务器运行正常
3. API 端点返回正确数据
4. 访问前台主页

---

## 复现步骤

1. 访问 http://localhost:3000/
2. 查看右侧悬浮展示框
3. 观察"学员统计"和"就业统计"的数据显示
4. 打开浏览器开发者工具（F12）
5. 查看 Console 和 Network 标签

---

## 预期结果

右侧悬浮展示框正确显示学员统计和就业统计数据：

**学员统计**：
- 累计学员：6
- 在读学员：5
- 毕业学员：1

**就业统计**：
- 就业率：85.0%
- 平均薪资：25K
- 最高薪资：32K

---

## 实际结果

右侧悬浮展示框显示为空或显示为 0：

**学员统计**：
- 累计学员：0
- 在读学员：0
- 毕业学员：0

**就业统计**：
- 就业率：0%
- 平均薪资：0K
- 最高薪资：0K

**浏览器状态**：
- Console 无错误信息
- Network 标签显示 API 请求成功（200 OK）
- 但数据未正确显示在页面上

---

## 问题原因

### 根本原因

前端代码中访问 API 响应数据的方式不正确。

### 详细分析

1. **响应拦截器返回 `response.data`**
   ```javascript
   // request.js
   api.interceptors.response.use(
     response => {
       return response.data  // 这里已经返回了 data
     },
     ...
   )
   ```

2. **前端代码又访问 `response.data`**
   ```javascript
   // Home.vue
   const response = await api.get('/api/stats/student-stats/')
   if (response.data) {  // ❌ 错误：response 已经是 data
     studentStats.value = {
       total: response.data.total,  // 实际访问的是 undefined
       ...
     }
   }
   ```

3. **实际访问的是 `response.data.data`（不存在）**
   - API 返回：`{total: 6, current: 5, graduated: 1}`
   - 响应拦截器返回：`{total: 6, current: 5, graduated: 1}`
   - 前端访问：`response.data.total` → `undefined`

4. **导致数据无法正确赋值**
   - `studentStats.value.total` 被赋值为 `undefined || 0` → `0`
   - 页面显示为空或 0

---

## 修复方案

### 修复内容

#### 1. 修复学员统计数据加载

**修复前**：
```javascript
const loadStudentStats = async () => {
  try {
    const response = await api.get('/api/stats/student-stats/')
    if (response.data) {  // ❌ 错误
      studentStats.value = {
        total: response.data.total || 0,
        current: response.data.current || 0,
        graduated: response.data.graduated || 0
      }
    }
  } catch (error) {
    console.error('加载学员统计失败:', error)
  }
}
```

**修复后**：
```javascript
const loadStudentStats = async () => {
  try {
    const response = await api.get('/api/stats/student-stats/')
    console.log('学员统计 API 响应:', response)
    if (response) {  // ✅ 正确
      studentStats.value = {
        total: response.total || 0,
        current: response.current || 0,
        graduated: response.graduated || 0
      }
      console.log('学员统计数据已更新:', studentStats.value)
    }
  } catch (error) {
    console.error('加载学员统计失败:', error)
  }
}
```

#### 2. 修复就业统计数据加载

**修复前**：
```javascript
const loadEmploymentStats = async () => {
  try {
    const response = await api.get('/api/stats/employment-stats/')
    if (response.data) {  // ❌ 错误
      employmentStats.value = {
        rate: response.data.rate || 0,
        avgSalary: response.data.avg_salary || '0K',
        maxSalary: response.data.max_salary || '0K'
      }
    }
  } catch (error) {
    console.error('加载就业统计失败:', error)
  }
}
```

**修复后**：
```javascript
const loadEmploymentStats = async () => {
  try {
    const response = await api.get('/api/stats/employment-stats/')
    console.log('就业统计 API 响应:', response)
    if (response) {  // ✅ 正确
      employmentStats.value = {
        rate: response.rate || 0,
        avgSalary: response.avg_salary || '0K',
        maxSalary: response.max_salary || '0K'
      }
      console.log('就业统计数据已更新:', employmentStats.value)
    }
  } catch (error) {
    console.error('加载就业统计失败:', error)
  }
}
```

#### 3. 修复优秀学员数据加载

**修复前**：
```javascript
const loadExcellentStudents = async () => {
  try {
    const response = await api.get('/api/stats/excellent-students/')
    if (response.data && response.data.length > 0) {  // ❌ 错误
      excellentStudents.value = response.data.slice(0, 3)
    }
  } catch (error) {
    console.error('加载优秀学员失败:', error)
  }
}
```

**修复后**：
```javascript
const loadExcellentStudents = async () => {
  try {
    const response = await api.get('/api/stats/excellent-students/')
    console.log('优秀学员 API 响应:', response)
    if (response && response.length > 0) {  // ✅ 正确
      excellentStudents.value = response.slice(0, 3)
      console.log('优秀学员数据已更新:', excellentStudents.value)
    }
  } catch (error) {
    console.error('加载优秀学员失败:', error)
  }
}
```

---

## 修复文件

### 前端文件（1个）

**文件路径**：`frontend-web/src/views/Home.vue`

**修改内容**：
1. 修复 `loadStudentStats` 方法
2. 修复 `loadEmploymentStats` 方法
3. 修复 `loadExcellentStudents` 方法
4. 添加 console.log 调试信息

---

## 验证方法

### 1. API 测试

```bash
# 测试学员统计 API
curl http://localhost:8000/api/stats/student-stats/
# 预期返回: {"total":6,"current":5,"graduated":1}

# 测试就业统计 API
curl http://localhost:8000/api/stats/employment-stats/
# 预期返回: {"rate":85.0,"avg_salary":"25K","max_salary":"32K"}
```

### 2. 前端页面测试

1. 访问 http://localhost:3000/
2. 查看右侧悬浮展示框
3. 确认显示正确数据：
   - 学员统计：累计学员 6，在读学员 5，毕业学员 1
   - 就业统计：就业率 85.0%，平均薪资 25K，最高薪资 32K

### 3. 浏览器开发者工具测试

1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 刷新页面
4. 查看日志输出：
   ```
   学员统计 API 响应: {total: 6, current: 5, graduated: 1}
   学员统计数据已更新: {total: 6, current: 5, graduated: 1}
   就业统计 API 响应: {rate: 85.0, avg_salary: '25K', max_salary: '32K'}
   就业统计数据已更新: {rate: 85.0, avgSalary: '25K', maxSalary: '32K'}
   ```

### 4. Network 标签测试

1. 切换到 Network 标签
2. 刷新页面
3. 查找以下请求：
   - `student-stats` - 200 OK
   - `employment-stats` - 200 OK
   - `excellent-students` - 200 OK
4. 点击请求查看 Response，确认返回正确数据

---

## 测试结果

### 修复前

- ❌ 学员统计显示为 0
- ❌ 就业统计显示为 0
- ❌ 数据无法正确显示

### 修复后

- ✅ 学员统计显示正确：累计 6，在读 5，毕业 1
- ✅ 就业统计显示正确：就业率 85.0%，平均薪资 25K，最高薪资 32K
- ✅ 数据正确加载和显示

---

## 技术要点

### 响应拦截器的作用

```javascript
// request.js
api.interceptors.response.use(
  response => {
    return response.data  // 自动提取 data 字段
  },
  error => {
    // 错误处理
    return Promise.reject(error)
  }
)
```

**说明**：
- 响应拦截器已经返回了 `response.data`
- 在业务代码中直接使用 `response` 即可
- 不需要再访问 `response.data`

### 正确的数据访问方式

```javascript
// ✅ 正确
const response = await api.get('/api/stats/student-stats/')
const total = response.total

// ❌ 错误
const response = await api.get('/api/stats/student-stats/')
const total = response.data.total  // response.data 是 undefined
```

---

## 相关 Bug

本次修复是以下功能的延续：

1. ✅ Bug 1: Home.vue 语法错误（测试用例 ID: 24）
2. ✅ Bug 2: 统计 API 端点 404 错误（测试用例 ID: 25）
3. ✅ Bug 3: Activities.vue 导入错误（测试用例 ID: 26）
4. ✅ Bug 4: Stats.vue Element Plus 警告（测试用例 ID: 27）
5. ✅ Bug 5: 前台学员统计数据显示为空（测试用例 ID: 28）⭐ 本次修复

---

## 总结

已成功修复前台学员统计数据显示问题：

1. ✅ **问题定位**：响应数据访问方式不正确
2. ✅ **修复代码**：移除多余的 `.data` 访问
3. ✅ **添加日志**：方便后续排查问题
4. ✅ **验证通过**：数据正确显示
5. ✅ **测试用例**：已导入到用例管理系统（ID: 28）

---

**修复时间**: 2026-04-24  
**修复人**: Claude Sonnet 4.6  
**测试用例 ID**: 28  
**版本**: v0.3.0
