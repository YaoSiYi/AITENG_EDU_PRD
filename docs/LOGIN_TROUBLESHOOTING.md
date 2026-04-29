# 🔧 前端登录问题诊断和解决方案

## 问题描述
前端访问登录页面时出现 404 错误

## 诊断结果

### ✅ 已确认正常的部分
1. **后端服务正常** - Django 运行在 http://localhost:8000
2. **后端登录API正常** - `/api/users/login/` 可以正常返回 Token
3. **前端服务正常** - Vite 运行在 http://localhost:3000
4. **登录页面文件存在** - `src/views/Login.vue` 文件存在
5. **路由配置正确** - `/login` 路由已配置

### 🔍 可能的问题原因

#### 1. 浏览器缓存问题
前端是单页应用（SPA），如果浏览器缓存了旧版本，可能导致路由不工作。

**解决方案**：
- 按 `Ctrl + Shift + R` (Windows/Linux) 或 `Cmd + Shift + R` (Mac) 强制刷新
- 或者清除浏览器缓存

#### 2. API 基础 URL 配置错误
`.env` 文件中的 `VITE_API_BASE_URL` 配置错误。

**已修复**：
```bash
# 修改前（错误）
VITE_API_BASE_URL=http://localhost:8000/api

# 修改后（正确）
VITE_API_BASE_URL=http://localhost:8000
```

#### 3. 前端服务未重启
修改 `.env` 文件后，需要重启前端服务才能生效。

**已执行**：前端服务已重启

## 📋 完整的访问步骤

### 1. 确认服务状态

```bash
# 检查后端服务（应该在 8000 端口）
curl http://localhost:8000/api/users/login/

# 检查前端服务（应该在 3000 端口）
curl http://localhost:3000/
```

### 2. 访问前端

打开浏览器，访问：
```
http://localhost:3000
```

### 3. 导航到登录页面

方式一：直接访问登录页面
```
http://localhost:3000/login
```

方式二：从首页点击「登录」按钮

### 4. 登录系统

使用管理员账号：
- **用户名**：`admin`
- **密码**：`admin123`

### 5. 访问测试用例管理

登录成功后，点击顶部导航栏的「测试用例」菜单

## 🐛 调试方法

### 方法1：浏览器开发者工具

1. 打开浏览器开发者工具（F12）
2. 切换到 **Console** 标签
3. 查看是否有 JavaScript 错误
4. 切换到 **Network** 标签
5. 刷新页面，查看网络请求
6. 检查是否有失败的请求（红色）

### 方法2：检查 API 请求

在浏览器 Console 中执行：

```javascript
// 检查 Token
console.log('Token:', localStorage.getItem('token'))

// 测试登录 API
fetch('/api/users/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
})
.then(r => r.json())
.then(data => {
  console.log('登录成功:', data)
  localStorage.setItem('token', data.access)
})
.catch(err => console.error('登录失败:', err))

// 测试测试用例 API
fetch('/api/testcases/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})
.then(r => r.json())
.then(data => console.log('测试用例数据:', data))
.catch(err => console.error('获取失败:', err))
```

### 方法3：检查路由

在浏览器 Console 中执行：

```javascript
// 检查当前路由
console.log('当前路由:', window.location.pathname)

// 检查 Vue Router
console.log('Vue Router:', window.__VUE_ROUTER__)
```

## 🔄 重启服务的正确方法

### 重启前端服务

```bash
# 1. 停止当前服务
# 在运行 npm run dev 的终端按 Ctrl+C

# 2. 重新启动
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-web
npm run dev

# 3. 等待服务启动
# 看到 "Local: http://localhost:3000/" 表示启动成功
```

### 重启后端服务（如果需要）

```bash
# 1. 停止当前服务
# 在运行 manage.py runserver 的终端按 Ctrl+C

# 2. 重新启动
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/backend
source venv/bin/activate
python manage.py runserver 8000
```

## ✅ 验证清单

- [ ] 后端服务运行在 http://localhost:8000
- [ ] 前端服务运行在 http://localhost:3000
- [ ] 可以访问首页 http://localhost:3000
- [ ] 可以访问登录页面 http://localhost:3000/login
- [ ] 可以成功登录
- [ ] 登录后可以看到「测试用例」和「数据看板」菜单
- [ ] 点击「测试用例」可以看到 20 条测试用例数据

## 🎯 常见错误和解决方案

### 错误1：404 Not Found

**可能原因**：
- 前端服务未启动
- 访问了错误的端口
- 浏览器缓存问题

**解决方案**：
1. 确认前端服务正在运行
2. 确认访问的是 http://localhost:3000（不是 5173）
3. 强制刷新浏览器（Ctrl+Shift+R）

### 错误2：401 Unauthorized

**可能原因**：
- 未登录
- Token 过期
- Token 未正确传递

**解决方案**：
1. 重新登录
2. 检查 localStorage 中是否有 token
3. 检查 Network 标签中请求头是否包含 Authorization

### 错误3：页面空白

**可能原因**：
- JavaScript 错误
- API 请求失败
- 组件加载失败

**解决方案**：
1. 打开 Console 查看错误信息
2. 检查 Network 标签查看失败的请求
3. 重启前端服务

### 错误4：CORS 错误

**可能原因**：
- 后端 CORS 配置问题
- API 基础 URL 配置错误

**解决方案**：
1. 确认 `.env` 中 `VITE_API_BASE_URL=http://localhost:8000`
2. 确认后端 `settings.py` 中 CORS 配置正确

## 📞 需要帮助？

如果以上方法都无法解决问题，请提供以下信息：

1. 浏览器 Console 中的错误信息（截图）
2. Network 标签中失败的请求（截图）
3. 访问的具体 URL
4. 前端和后端服务的启动日志

---

**最后更新**: 2024-04-22  
**状态**: 前端服务已重启，配置已修复
