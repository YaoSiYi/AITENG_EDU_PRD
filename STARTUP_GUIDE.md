# 艾腾教育项目启动指南

## 📋 项目概述

艾腾教育是一个软件测试全栈工程师培训系统，包含：
- **Web管理后台** (React + Vite)
- **移动端H5应用** (Uni-app)
- **后端API服务** (Django REST Framework)

---

## 🚀 快速启动

### 方式1：一键启动（推荐）

```bash
# 进入项目根目录
cd /Users/yao/Node_Project/Aiteng_Edu_Prd

# 运行一键启动脚本
./start.sh
```

### 方式2：手动启动

参考下方的"详细启动步骤"。

---

## 📊 服务端口分配

| 服务 | 端口 | 电脑访问 | 手机访问（同WiFi） |
|------|------|----------|-------------------|
| **Web管理后台** | 3000 | http://localhost:3000 | http://192.168.0.156:3000 |
| **Uni-app H5** | 3001 | http://localhost:3001 | http://192.168.0.156:3001 |
| **Django API** | 8000 | http://localhost:8000 | http://192.168.0.156:8000 |
| **Django Admin** | 8000 | http://localhost:8000/admin | http://192.168.0.156:8000/admin |
| **MySQL** | 3306 | localhost:3306 | - |
| **Redis** | 6379 | localhost:6379 | - |

---

## 🔧 详细启动步骤

### 1. 启动基础服务

#### MySQL
```bash
# 检查MySQL是否运行
brew services list | grep mysql

# 如果未运行，启动MySQL
brew services start mysql
```

#### Redis
```bash
# 检查Redis是否运行
brew services list | grep redis

# 如果未运行，启动Redis
brew services start redis
```

### 2. 启动后端服务 (Django)

```bash
# 进入后端目录
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/backend

# 激活虚拟环境
source venv/bin/activate

# 启动Django开发服务器（监听所有网络接口，支持手机访问）
python manage.py runserver 0.0.0.0:8000
```

**访问地址**：
- API文档：http://localhost:8000/api/docs/
- 管理后台：http://localhost:8000/admin/
- 默认管理员账号：admin / admin123

### 3. 启动前端Web管理后台

```bash
# 新开一个终端窗口
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-web

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

**访问地址**：http://localhost:3000

### 4. 启动前端Uni-app H5应用

```bash
# 新开一个终端窗口
cd /Users/yao/Node_Project/Aiteng_Edu_Prd/frontend-uniapp

# 安装依赖（首次运行）
npm install

# 启动H5开发服务器
npm run dev:h5
```

**访问地址**：http://localhost:3001

---

## 📱 手机访问方式

### 前提条件
- 手机和电脑连接到同一个WiFi网络
- 电脑的局域网IP地址：`192.168.0.156`

### 访问地址
- **Web管理后台**：http://192.168.0.156:3000
- **Uni-app H5**：http://192.168.0.156:3001

### 测试功能
- ✅ 登录/注册
- ✅ 题库浏览
- ✅ 活动查看
- ✅ 个人中心

---

## 🔍 验证服务状态

### 检查所有服务是否正常运行

```bash
# 检查端口占用
lsof -nP -iTCP -sTCP:LISTEN | grep -E "(3000|3001|8000|3306|6379)"
```

**预期输出**：
```
node      xxxxx  yao   16u  IPv6 ... TCP *:3000 (LISTEN)      # Web管理后台
node      xxxxx  yao   16u  IPv4 ... TCP *:3001 (LISTEN)      # Uni-app H5
Python    xxxxx  yao    4u  IPv4 ... TCP *:8000 (LISTEN)      # Django API
mysqld    xxxxx  yao   21u  IPv6 ... TCP *:3306 (LISTEN)      # MySQL
redis-ser xxxxx  yao    6u  IPv4 ... TCP 127.0.0.1:6379 (LISTEN) # Redis
```

### 测试API连接

```bash
# 测试Django API
curl http://localhost:8000/api/

# 测试MySQL连接
mysql -u root -p -e "SHOW DATABASES;"

# 测试Redis连接
redis-cli ping
```

---

## 🛑 停止服务

### 停止前端服务
在运行前端服务的终端窗口中按 `Ctrl + C`

### 停止Django服务
在运行Django的终端窗口中按 `Ctrl + C`

### 停止MySQL和Redis
```bash
# 停止MySQL
brew services stop mysql

# 停止Redis
brew services stop redis
```

### 一键停止所有服务
```bash
./stop.sh
```

---

## 🐛 常见问题

### 1. 端口被占用

**问题**：启动服务时提示端口已被占用

**解决方案**：
```bash
# 查看占用端口的进程
lsof -nP -iTCP:3000 -sTCP:LISTEN  # 替换3000为实际端口

# 停止占用端口的进程
kill <PID>
```

### 2. 手机无法访问

**问题**：手机访问 http://192.168.0.156:3000 失败

**解决方案**：
1. 确认手机和电脑在同一WiFi
2. 检查电脑防火墙设置
3. 确认IP地址是否正确：
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
4. 清除手机浏览器缓存

### 3. API请求失败

**问题**：前端无法连接后端API

**解决方案**：
1. 确认Django服务正在运行
2. 检查CORS配置（backend/config/settings.py）
3. 查看Django日志输出

### 4. 数据库连接失败

**问题**：Django无法连接MySQL

**解决方案**：
```bash
# 检查MySQL是否运行
brew services list | grep mysql

# 启动MySQL
brew services start mysql

# 测试连接
mysql -u root -p
```

### 5. 依赖安装失败

**问题**：npm install 或 pip install 失败

**解决方案**：
```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install

# Python依赖
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📦 项目结构

```
Aiteng_Edu_Prd/
├── backend/                 # Django后端
│   ├── apps/               # 应用模块
│   ├── config/             # 配置文件
│   ├── manage.py           # Django管理脚本
│   └── requirements.txt    # Python依赖
├── frontend-web/           # React Web管理后台
│   ├── src/               # 源代码
│   ├── package.json       # npm依赖
│   └── vite.config.js     # Vite配置
├── frontend-uniapp/       # Uni-app H5应用
│   ├── src/               # 源代码
│   ├── package.json       # npm依赖
│   └── vite.config.js     # Vite配置
├── start.sh               # 一键启动脚本
├── stop.sh                # 一键停止脚本
└── STARTUP_GUIDE.md       # 本文档
```

---

## 🔐 默认账号

### Django管理后台
- 用户名：`admin`
- 密码：`admin123`
- 访问地址：http://localhost:8000/admin/

### 测试账号
- 用户名：`test`
- 密码：`test123`

---

## 📝 开发建议

### 1. 代码规范
- 前端：使用ESLint和Prettier
- 后端：使用Black和Flake8

### 2. Git提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

### 3. 分支管理
- `main`: 主分支（生产环境）
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

---

## 🚀 部署到生产环境

### 1. 修改配置文件

**frontend-web/.env.production**
```env
VITE_API_BASE_URL=https://api.aiteng.com
```

**frontend-uniapp/src/utils/request.js**
```javascript
const BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.aiteng.com/api'
  : 'http://192.168.0.156:8000/api'
```

**backend/config/settings.py**
```python
DEBUG = False
ALLOWED_HOSTS = ['api.aiteng.com', 'www.aiteng.com']
CORS_ALLOWED_ORIGINS = [
    "https://www.aiteng.com",
    "https://m.aiteng.com",
]
```

### 2. 构建前端

```bash
# Web管理后台
cd frontend-web
npm run build

# Uni-app H5
cd frontend-uniapp
npm run build:h5
```

### 3. 部署后端

```bash
# 收集静态文件
python manage.py collectstatic

# 使用Gunicorn运行
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📞 技术支持

如有问题，请联系：
- 邮箱：support@aiteng.com
- 文档：https://docs.aiteng.com

---

**最后更新**：2026-04-29
**版本**：v1.0.0
