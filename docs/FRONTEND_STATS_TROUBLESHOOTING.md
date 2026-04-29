# 前台学员统计数据显示问题排查与修复

## 问题描述

前台主页右侧悬浮展示框中的"学员统计"和"就业统计"显示为空或显示为 0。

---

## 排查结果

### 1. API 端点测试 ✅

**学员统计 API**:
```bash
curl http://localhost:8000/api/stats/student-stats/
```
**返回结果**:
```json
{
    "total": 6,
    "current": 5,
    "graduated": 1
}
```
✅ API 正常返回数据

**就业统计 API**:
```bash
curl http://localhost:8000/api/stats/employment-stats/
```
**返回结果**:
```json
{
    "rate": 85.0,
    "avg_salary": "25K",
    "max_salary": "32K"
}
```
✅ API 正常返回数据

### 2. 前端代码检查 ✅

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
const studentStats = ref({
  total: 0,
  current: 0,
  graduated: 0
})
```
⚠️ 初始值为 0，如果 API 调用失败会显示为空

### 3. 服务状态检查 ✅

- ✅ 前端服务器运行正常（端口 3000）
- ✅ 后端服务器运行正常（端口 8000）
- ✅ API 端点可以访问

---

## 可能的原因

### 1. 浏览器缓存问题 ⭐ (最可能)

前端页面可能使用了旧的缓存版本，没有加载最新的代码或数据。

**解决方案**:
- 强制刷新浏览器：`Ctrl + Shift + R` (Windows/Linux) 或 `Cmd + Shift + R` (Mac)
- 清除浏览器缓存
- 使用无痕模式访问

### 2. CORS 跨域问题

前端请求后端 API 时可能遇到 CORS 错误。

**检查方法**:
1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 查看是否有 CORS 错误信息

**可能的错误**:
```
Access to XMLHttpRequest at 'http://localhost:8000/api/stats/student-stats/' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

### 3. API 请求失败

前端请求 API 时可能遇到网络错误或超时。

**检查方法**:
1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 刷新页面
4. 查看 API 请求状态

**预期结果**:
- `student-stats` - 200 OK
- `employment-stats` - 200 OK
- `excellent-students` - 200 OK

### 4. 前端服务器未重启

前端代码修改后，Vite 开发服务器可能没有正确热更新。

**解决方案**:
```bash
# 停止前端服务器（Ctrl + C）
# 重新启动
cd frontend-web
npm run dev
```

---

## 解决步骤

### 步骤 1: 强制刷新浏览器 ⭐ (推荐首先尝试)

1. 访问首页：http://localhost:3000/
2. 按以下快捷键强制刷新：
   - **Windows/Linux**: `Ctrl + Shift + R` 或 `Ctrl + F5`
   - **Mac**: `Cmd + Shift + R`
3. 或者右键点击刷新按钮，选择"清空缓存并硬性重新加载"

### 步骤 2: 检查浏览器控制台

1. 打开浏览器开发者工具（F12）
2. 切换到 **Console** 标签
3. 查看是否有错误信息

**常见错误**:
- CORS 错误
- API 请求失败
- JavaScript 错误

### 步骤 3: 检查 Network 标签

1. 打开浏览器开发者工具（F12）
2. 切换到 **Network** 标签
3. 刷新页面
4. 查找以下请求：
   - `student-stats`
   - `employment-stats`
   - `excellent-students`
5. 点击请求查看：
   - **Status**: 应该是 200
   - **Response**: 应该有数据

### 步骤 4: 使用无痕模式测试

1. 打开浏览器的无痕/隐私模式
2. 访问：http://localhost:3000/
3. 查看数据是否正常显示

### 步骤 5: 重启前端服务器

如果以上方法都无效，尝试重启前端服务器：

```bash
# 停止当前的前端服务器（Ctrl + C）
# 然后重新启动
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-web
npm run dev
```

### 步骤 6: 清除浏览器缓存

1. 打开浏览器设置
2. 找到"清除浏览数据"或"清除缓存"
3. 选择"缓存的图片和文件"
4. 清除
5. 重新访问页面

---

## 验证方法

### 方法 1: 直接测试 API

在浏览器中直接访问 API 端点：

```
http://localhost:8000/api/stats/student-stats/
```

**预期结果**:
```json
{
    "total": 6,
    "current": 5,
    "graduated": 1
}
```

### 方法 2: 使用 curl 测试

```bash
# 测试学员统计
curl http://localhost:8000/api/stats/student-stats/

# 测试就业统计
curl http://localhost:8000/api/stats/employment-stats/

# 测试优秀学员
curl http://localhost:8000/api/stats/excellent-students/
```

### 方法 3: 检查前端页面源代码

1. 访问 http://localhost:3000/
2. 右键点击页面，选择"查看页面源代码"
3. 搜索 `studentStats`
4. 确认代码是否包含数据加载逻辑

---

## 预期显示效果

刷新后，右侧悬浮展示框应该显示：

### 学员统计
```
┌─────────────────────┐
│ 👥 学员统计         │
├─────────────────────┤
│ 累计学员        6   │
│ 在读学员        5   │
│ 毕业学员        1   │
└─────────────────────┘
```

### 就业统计
```
┌─────────────────────┐
│ 💼 就业统计         │
├─────────────────────┤
│ 就业率       85.0%  │
│ 平均薪资       25K  │
│ 最高薪资       32K  │
└─────────────────────┘
```

---

## 调试技巧

### 1. 查看 API 请求详情

在浏览器 Network 标签中：
1. 找到 `student-stats` 请求
2. 点击查看详情
3. 查看 **Headers** 标签：
   - Request URL
   - Status Code
   - Request Method
4. 查看 **Response** 标签：
   - 确认返回的数据

### 2. 查看 Console 日志

在浏览器 Console 标签中：
1. 查找 `加载学员统计失败` 或 `加载就业统计失败` 的错误信息
2. 查看错误详情
3. 根据错误信息排查问题

### 3. 手动调用 API

在浏览器 Console 中手动调用 API：

```javascript
// 测试学员统计 API
fetch('http://localhost:8000/api/stats/student-stats/')
  .then(res => res.json())
  .then(data => console.log('学员统计:', data))
  .catch(err => console.error('错误:', err))

// 测试就业统计 API
fetch('http://localhost:8000/api/stats/employment-stats/')
  .then(res => res.json())
  .then(data => console.log('就业统计:', data))
  .catch(err => console.error('错误:', err))
```

---

## 常见问题

### Q1: 页面显示为 0 或空白

**原因**: 浏览器缓存了旧版本的页面

**解决**: 强制刷新浏览器（Ctrl + Shift + R）

### Q2: API 返回 404 错误

**原因**: 后端服务器未正确加载新的 API 端点

**解决**: 重启后端服务器
```bash
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

### Q3: CORS 错误

**原因**: 跨域请求被阻止

**解决**: 检查 Django 的 CORS 配置
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]
```

### Q4: 数据不更新

**原因**: 前端缓存了 API 响应

**解决**: 
1. 清除浏览器缓存
2. 使用无痕模式测试
3. 在 API 请求中添加时间戳参数

---

## 最终检查清单

- [ ] 后端服务器运行正常（http://localhost:8000）
- [ ] 前端服务器运行正常（http://localhost:3000）
- [ ] API 端点返回正确数据
- [ ] 浏览器已强制刷新
- [ ] 浏览器控制台无错误
- [ ] Network 标签显示 API 请求成功（200 OK）
- [ ] 页面显示正确的统计数据

---

## 联系支持

如果以上所有方法都无效，请提供以下信息：

1. 浏览器类型和版本
2. 浏览器 Console 的错误信息（截图）
3. Network 标签中 API 请求的状态（截图）
4. 当前访问的 URL
5. 是否使用了代理或 VPN

---

**更新时间**: 2026-04-24  
**文档版本**: v1.0
