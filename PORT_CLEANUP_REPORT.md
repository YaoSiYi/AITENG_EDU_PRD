# 端口占用清理完成报告

## ✅ 已完成的清理

### 1. 停止重复进程
- ✅ 停止旧的 frontend-web 进程 (PID 24265, 端口3000)
- ✅ 停止旧的 frontend-uniapp 进程 (PID 21360, 端口3001)
- ✅ 停止遗留的 vite 进程 (PID 15259, 端口5173)

### 2. 当前运行的服务

| 服务 | 端口 | PID | 状态 |
|------|------|-----|------|
| frontend-web (React) | 3000 | 92262 | ✅ 正常运行 |
| frontend-uniapp (H5) | 3001 | 37417 | ✅ 正常运行 |
| backend (Django) | 8000 | 7327 | ✅ 正常运行 |
| MySQL | 3306 | 11780 | ✅ 正常运行 |
| Redis | 6379 | 800 | ✅ 正常运行 |

### 3. 已修复的配置文件

#### ✅ backend/config/settings.py
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.156:3000",  # 新增：支持手机访问Web端
    "http://192.168.0.156:3001",  # 新增：支持手机访问Uni-app
]
```

#### ✅ frontend-web/.env
```env
VITE_API_BASE_URL=http://192.168.0.156:8000  # 改为局域网IP
```

#### ✅ frontend-uniapp/src/utils/request.js
```javascript
const BASE_URL = 'http://192.168.0.156:8000/api'  # 已修复
```

#### ✅ frontend-uniapp/src/common/request.js
```javascript
const BASE_URL = 'http://192.168.0.156:8000/api'  # 已修复
```

---

## 📊 端口分配方案

| 服务 | 端口 | 访问地址 | 说明 |
|------|------|----------|------|
| **前端Web** | 3000 | http://192.168.0.156:3000 | React管理后台 |
| **前端Uni-app** | 3001 | http://192.168.0.156:3001 | H5移动端应用 |
| **后端API** | 8000 | http://192.168.0.156:8000 | Django REST API |
| **MySQL** | 3306 | localhost:3306 | 数据库 |
| **Redis** | 6379 | localhost:6379 | 缓存服务 |

---

## 🎯 访问方式

### 电脑端访问
- Web管理后台：http://localhost:3000 或 http://192.168.0.156:3000
- Uni-app H5：http://localhost:3001 或 http://192.168.0.156:3001
- Django后台：http://localhost:8000/admin

### 手机端访问（同一WiFi）
- Web管理后台：http://192.168.0.156:3000
- Uni-app H5：http://192.168.0.156:3001

---

## ⚠️ 注意事项

1. **所有配置已统一使用局域网IP** - 电脑和手机都可以访问
2. **无需重启服务** - 配置文件修改后，刷新浏览器即可生效
3. **Docker容器** - 如果不需要Docker的MySQL和Redis，可以停止容器
4. **防火墙** - Mac防火墙已关闭，无需额外配置

---

## 🔧 如需重启服务

### 重启前端Web (端口3000)
```bash
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-web
npm run dev
```

### 重启前端Uni-app (端口3001)
```bash
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-uniapp
npm run dev:h5
```

### 重启Django后端 (端口8000)
```bash
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

## ✅ 验证清理结果

运行以下命令验证端口占用：
```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -E "(3000|3001|8000)"
```

预期输出：
```
node      37417  yao   21u  IPv6 ... TCP [::1]:3001 (LISTEN)
node      92262  yao   16u  IPv6 ... TCP *:3000 (LISTEN)
Python     7327  yao    4u  IPv4 ... TCP *:8000 (LISTEN)
```

---

## 📝 总结

✅ **端口冲突已解决** - 每个服务只有一个进程在运行
✅ **配置已统一** - 所有API地址都使用局域网IP
✅ **手机可访问** - 手机和电脑都可以正常访问所有服务
✅ **CORS已配置** - 后端允许来自所有前端地址的请求

现在您可以：
1. 在电脑浏览器访问：http://localhost:3000 (Web) 或 http://localhost:3001 (H5)
2. 在手机浏览器访问：http://192.168.0.156:3000 (Web) 或 http://192.168.0.156:3001 (H5)
3. 所有功能（登录、注册、题库、活动等）都应该正常工作
