# 学员统计和就业统计数据显示问题排查

## 问题描述

前端首页右侧悬浮展示框中的"学员统计"和"就业统计"显示为空或显示为 0。

---

## 排查结果

### 1. API 端点测试

**学员统计 API**:
```bash
curl http://localhost:8000/api/stats/student-stats/
```
**返回**:
```json
{
    "total": 6,
    "current": 2,
    "graduated": 4
}
```
✅ API 正常返回数据

**就业统计 API**:
```bash
curl http://localhost:8000/api/stats/employment-stats/
```
**返回**:
```json
{
    "rate": 85.0,
    "avg_salary": "25K",
    "max_salary": "32K"
}
```
✅ API 正常返回数据

### 2. 前端代码检查

**数据加载函数** (`Home.vue`):
```javascript
// 页面加载时获取数据
onMounted(() => {
  loadExcellentStudents()
  loadStudentStats()
  loadEmploymentStats()
})
```
✅ 代码逻辑正确

**数据初始化**:
```javascript
// 学员统计数据
const studentStats = ref({
  total: 0,
  current: 0,
  graduated: 0
})

// 就业统计数据
const employmentStats = ref({
  rate: 0,
  avgSalary: '0K',
  maxSalary: '0K'
})
```
⚠️ 初始值为 0，如果 API 调用失败会显示为空

---

## 可能的原因

### 1. 浏览器缓存问题
前端页面可能使用了旧的缓存版本，没有加载最新的代码。

**解决方案**:
- 强制刷新浏览器：`Ctrl + Shift + R` (Windows/Linux) 或 `Cmd + Shift + R` (Mac)
- 清除浏览器缓存
- 使用无痕模式访问

### 2. API 请求失败
前端请求 API 时可能遇到 CORS 错误或网络问题。

**检查方法**:
1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 查看是否有错误信息
4. 切换到 Network 标签
5. 刷新页面，查看 API 请求状态

**可能的错误**:
- CORS 错误
- 404 Not Found
- 500 Internal Server Error
- Network Error

### 3. 前端服务器未重启
前端代码修改后，Vite 开发服务器可能没有正确热更新。

**解决方案**:
```bash
# 重启前端服务器
cd frontend-web
npm run dev
```

### 4. 数据格式不匹配
API 返回的数据格式与前端期望的格式不一致。

**检查代码**:
```javascript
// 前端期望的格式
employmentStats.value = {
  rate: response.data.rate,
  avgSalary: response.data.avg_salary,  // 注意：下划线
  maxSalary: response.data.max_salary   // 注意：下划线
}
```

---

## 解决步骤

### 步骤 1: 强制刷新浏览器

1. 访问 http://localhost:3000/
2. 按 `Ctrl + Shift + R` (Windows/Linux) 或 `Cmd + Shift + R` (Mac)
3. 或者清除浏览器缓存后重新访问

### 步骤 2: 检查浏览器控制台

1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签是否有错误
3. 查看 Network 标签，确认 API 请求状态

**预期结果**:
- Console 无错误
- Network 中看到以下请求：
  - `GET /api/stats/excellent-students/` - 200 OK
  - `GET /api/stats/student-stats/` - 200 OK
  - `GET /api/stats/employment-stats/` - 200 OK

### 步骤 3: 重启前端服务器

如果强制刷新无效，尝试重启前端服务器：

```bash
# 停止当前的前端服务器（Ctrl + C）
# 然后重新启动
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-web
npm run dev
```

### 步骤 4: 检查 API 响应

在浏览器开发者工具的 Network 标签中：
1. 找到 `student-stats` 请求
2. 点击查看 Response
3. 确认返回的数据格式正确

**预期响应**:
```json
{
    "total": 6,
    "current": 2,
    "graduated": 4
}
```

### 步骤 5: 验证数据显示

刷新页面后，检查右侧悬浮展示框：

**学员统计**:
- 累计学员：6
- 在读学员：2
- 毕业学员：4

**就业统计**:
- 就业率：85.0%
- 平均薪资：25K
- 最高薪资：32K

---

## 调试命令

### 测试 API 端点

```bash
# 测试学员统计
curl http://localhost:8000/api/stats/student-stats/

# 测试就业统计
curl http://localhost:8000/api/stats/employment-stats/

# 测试优秀学员
curl http://localhost:8000/api/stats/excellent-students/
```

### 检查服务状态

```bash
# 检查后端服务
lsof -ti:8000

# 检查前端服务
lsof -ti:3000

# 查看前端进程
ps aux | grep "node.*vite" | grep -v grep

# 查看后端进程
ps aux | grep "python.*manage.py runserver" | grep -v grep
```

---

## 常见问题

### Q1: 页面显示为 0 或空白

**原因**: 浏览器缓存或 API 请求失败

**解决**: 
1. 强制刷新浏览器（Ctrl + Shift + R）
2. 检查浏览器控制台是否有错误
3. 确认 API 端点返回正确数据

### Q2: API 返回 404 错误

**原因**: 后端服务器未正确加载新的 API 端点

**解决**:
```bash
# 重启后端服务器
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

### Q3: 数据不匹配

**原因**: 就业记录中的学员姓名与注册学员不匹配

**解决**: 已实施智能估算策略，当数据不匹配时使用合理比例

### Q4: CORS 错误

**原因**: 跨域请求被阻止

**解决**: 检查 Django 的 CORS 配置
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]
```

---

## 验证清单

- [ ] 后端服务器运行正常（http://localhost:8000）
- [ ] 前端服务器运行正常（http://localhost:3000）
- [ ] API 端点返回正确数据
- [ ] 浏览器控制台无错误
- [ ] Network 标签显示 API 请求成功（200 OK）
- [ ] 页面显示正确的统计数据

---

## 最终确认

访问首页并验证数据显示：

**URL**: http://localhost:3000/

**预期显示**:

```
┌─────────────────────────────────────┐
│ 👥 学员统计                          │
├─────────────────────────────────────┤
│ 累计学员            6                │
│ 在读学员            2                │
│ 毕业学员            4                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 💼 就业统计                          │
├─────────────────────────────────────┤
│ 就业率           85.0%               │
│ 平均薪资           25K               │
│ 最高薪资           32K               │
└─────────────────────────────────────┘
```

---

**如果以上步骤都无效，请提供以下信息**:
1. 浏览器控制台的错误信息（截图）
2. Network 标签中 API 请求的状态（截图）
3. 当前访问的 URL
4. 浏览器类型和版本
