# 教务管理系统 - 项目启动指南

## 🚀 快速启动（推荐：本地开发模式）

### 前置要求
- Python 3.12+
- MySQL 8.0+ (或使用 Docker 单独运行 MySQL)
- Redis 7.0+
- Node.js 20+

### 方式一：本地开发模式（最稳定）

#### 1. 启动基础服务（MySQL + Redis）

```bash
# 只启动 MySQL 和 Redis
docker compose up -d db redis

# 等待 MySQL 就绪
docker compose exec db mysql -uroot -peducation123 -e "SELECT 1"
```

#### 2. 启动 Django 后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

#### 3. 启动 Celery（另开终端）

```bash
cd backend
source venv/bin/activate

# 启动 Celery Worker
celery -A config worker -l info

# 启动 Celery Beat（另开终端）
celery -A config beat -l info
```

#### 4. 启动 Vue 前端（另开终端）

```bash
cd frontend-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问地址

- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **API 文档**: http://localhost:8000/api/docs/

---

## 🐳 方式二：Docker Compose 完整部署

### 问题说明

当前 Docker 部署存在数据库迁移问题，需要手动初始化。

### 解决步骤

```bash
# 1. 完全清理环境
docker compose down -v
docker volume prune -f

# 2. 只启动数据库和 Redis
docker compose up -d db redis

# 3. 等待 MySQL 完全启动（约 30 秒）
sleep 30

# 4. 手动运行迁移
docker compose run --rm backend sh -c "
  python manage.py makemigrations &&
  python manage.py migrate &&
  python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
"

# 5. 启动所有服务
docker compose up -d

# 6. 查看日志
docker compose logs -f backend
```

### 设置管理员密码

```bash
docker compose exec backend python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
admin = User.objects.get(username='admin');
admin.set_password('admin123');
admin.save();
print('管理员密码已设置为: admin123')
"
```

---

## 🔧 常见问题排查

### 1. 数据库连接失败

```bash
# 检查 MySQL 是否运行
docker compose ps db

# 测试数据库连接
docker compose exec db mysql -uroot -peducation123 -e "SHOW DATABASES;"
```

### 2. 端口冲突

```bash
# 检查端口占用
lsof -i :8000  # 后端
lsof -i :3000  # 前端
lsof -i :3307  # MySQL
lsof -i :6379  # Redis
```

### 3. 清理并重新开始

```bash
# 停止所有服务
docker compose down -v

# 删除 Python 缓存
find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find backend -type f -name "*.pyc" -delete

# 删除 Node 模块
rm -rf frontend-web/node_modules

# 重新开始
docker compose up -d db redis
```

---

## 📝 开发建议

### 推荐开发流程

1. **使用本地开发模式**进行日常开发（热重载、调试方便）
2. **Docker 仅用于生产部署**或测试完整环境
3. **数据库和 Redis 用 Docker**，应用层本地运行

### 为什么推荐本地开发？

- ✅ **启动快**：无需等待容器构建
- ✅ **调试方便**：直接使用 IDE 断点调试
- ✅ **热重载**：代码修改立即生效
- ✅ **日志清晰**：直接在终端查看输出
- ✅ **避免 Docker 卷问题**：数据库迁移更稳定

---

## 🎯 下一步

### 1. 初始化数据

```bash
# 进入 Django shell
python manage.py shell

# 创建测试数据
from apps.users.models import User
from apps.questions.models import Question, QuestionCategory

# 创建分类
category = QuestionCategory.objects.create(name="Python基础")

# 创建题目
Question.objects.create(
    stage=1,
    category=category,
    subject="Python",
    difficulty="easy",
    content="什么是Python？",
    answer="Python是一种高级编程语言"
)
```

### 2. 测试 API

```bash
# 获取 API 文档
curl http://localhost:8000/api/docs/

# 注册用户
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "test123",
    "confirm_password": "test123",
    "phone": "13800138000",
    "nickname": "测试用户",
    "hometown": "北京"
  }'

# 登录获取 Token
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "test123"
  }'
```

### 3. 前端开发

```bash
cd frontend-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

---

## 📚 相关文档

- [需求文档](./教务管理系统-需求文档.md)
- [API 文档](http://localhost:8000/api/docs/) (启动后访问)
- [Django 官方文档](https://docs.djangoproject.com/)
- [Vue 3 官方文档](https://vuejs.org/)

---

**最后更新**: 2026-04-21  
**状态**: ✅ 代码已生成，推荐使用本地开发模式启动
