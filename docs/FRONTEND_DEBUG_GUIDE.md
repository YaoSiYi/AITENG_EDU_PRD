# 测试用例管理模块 - 前端调试指南

## 问题诊断

### 1. 检查后端API是否正常
```bash
# 测试登录获取Token
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 使用Token测试测试用例API
TOKEN="your_access_token_here"
curl http://localhost:8000/api/testcases/ \
  -H "Authorization: Bearer $TOKEN"
```

### 2. 检查前端配置

**环境变量配置** (`.env`):
```
VITE_API_BASE_URL=http://localhost:8000
```

**注意**: 不要在 `VITE_API_BASE_URL` 后面加 `/api`，因为 `request.js` 中已经配置了 `baseURL: '/api'`

### 3. 前端访问流程

1. 用户登录 → 获取 JWT Token → 存储到 localStorage
2. 访问 `/testcases` 页面
3. 前端调用 `getTestcaseList()` → `request.js` 拦截器添加 Token
4. 请求发送到 `/api/testcases/`
5. Vite 代理转发到 `http://localhost:8000/api/testcases/`
6. 后端验证 Token → 返回数据

### 4. 常见问题

**问题1: 页面显示为空**
- 原因: 未登录或 Token 过期
- 解决: 先登录系统，确保 localStorage 中有 token

**问题2: API 401 错误**
- 原因: Token 无效或未传递
- 解决: 检查 localStorage 中的 token，重新登录

**问题3: API 404 错误**
- 原因: API 路径错误
- 解决: 检查 `.env` 配置和 Vite 代理配置

### 5. 调试步骤

1. 打开浏览器开发者工具 (F12)
2. 切换到 Console 标签，查看错误信息
3. 切换到 Network 标签，查看 API 请求
4. 检查请求头是否包含 `Authorization: Bearer xxx`
5. 检查响应状态码和响应内容

### 6. 手动测试

在浏览器 Console 中执行:
```javascript
// 检查是否有 token
console.log('Token:', localStorage.getItem('token'))

// 手动调用 API
fetch('/api/testcases/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})
.then(r => r.json())
.then(data => console.log('API Response:', data))
.catch(err => console.error('API Error:', err))
```

### 7. 重启服务

如果修改了配置文件，需要重启前端服务:
```bash
cd frontend-web
# 停止当前服务 (Ctrl+C)
npm run dev
```

---

**最后更新**: 2024-04-22
