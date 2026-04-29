# Django Project

这是一个基于 Django 框架构建的 Web 应用程序，旨在提供模块化、可扩展的后端服务。

## 项目概述

- **项目名称**: Django Project
- **技术栈**: Django 4.2.24, Django REST Framework 3.16.1, Python 3.9+
- **主要功能**:
  - 用户身份验证与权限控制
  - RESTful API 接口支持
  - 自动登录功能
  - 多数据库连接支持（PostgreSQL、MongoDB、Redis）
  - 飞书API集成

## 目录结构

```
.
├── DjangoProject          # 项目主配置
├── authentication         # 认证模块
├── common                 # 通用工具
└── manage.py              # Django管理脚本
```

## 环境要求

- Python 3.9 或更高版本
- Django 4.2.24
- 其他依赖项见 [requirements.txt](requirements.txt)

## 安装说明

1. 克隆项目代码：
   ```bash
   git clone <项目地址>
   cd DjangoProject
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 数据库迁移：
   ```bash
   # 开发环境（使用本地 SQLite 数据库）
   set -a && source .env.dev && set +a
   python manage.py migrate
   
   # 生产环境（使用远程 PostgreSQL 数据库）
   # 确保 .env 文件配置正确后运行
   python manage.py migrate
   ```

5. 创建超级用户（可选）：
   ```bash
   python manage.py createsuperuser
   ```
   
   按照提示输入管理员信息（请使用强密码）

## 开发环境设置和运行

项目现在提供了一键设置和运行开发环境的脚本。

```bash
# 设置并运行开发环境
./devRun.sh

# 设置并运行开发环境（外部可访问）
./devRun.sh --external
```

该脚本会自动完成以下操作：
1. 检查虚拟环境
2. 升级 pip 并安装依赖
3. 创建开发环境配置文件（如果不存在）
4. 执行数据库迁移
5. 启动开发服务器

## Docker 工具

项目整合了 Docker 监控和清理功能到单一工具脚本中。

```bash
# 查看所有容器的状态和资源使用情况
./docker_tools.sh stats

# 实时监控容器资源使用情况
./docker_tools.sh live

# 显示容器进程信息
./docker_tools.sh top

# 查看容器日志
./docker_tools.sh logs [容器名称]

# 显示运行中的容器
./docker_tools.sh ps

# 显示所有容器（包括停止的）
./docker_tools.sh ps-all

# 清理无用镜像
./docker_tools.sh clean-images

# 清理构建缓存
./docker_tools.sh clean-cache

# 清理已停止的容器
./docker_tools.sh clean-containers

# 清理所有（镜像+缓存+容器）
./docker_tools.sh clean-all

# 执行全面清理（危险操作，会删除所有未使用的资源）
./docker_tools.sh prune
```

## 部署

### 使用 Docker Compose 部署（推荐）：

```bash
# 完整部署（包括更新Cloudflare IP和加固Nginx安全配置）
./deploy.sh

# 只更新 Cloudflare IP
./deploy.sh update

# 只加固 Nginx 安全配置
./deploy.sh security

# 查看服务日志
./deploy.sh logs

# 查看服务状态
./deploy.sh status
```

### Docker Secrets 使用指南

本文档介绍了如何在生产环境中使用 Docker Secrets 来安全地管理敏感信息。

#### 什么是 Docker Secrets？

Docker Secrets 是一种安全存储和管理敏感数据（如密码、API 密钥等）的机制。它确保敏感数据在传输和存储过程中得到加密保护，并且只能被授权的服务访问。

#### 如何使用 Docker Secrets

##### 1. 创建 Secrets 文件

在项目根目录下创建 `secrets` 目录，并在其中创建以下文件：

- `db_password.txt` - 数据库密码
- `db_user.txt` - 数据库用户名
- `secret_key.txt` - Django SECRET_KEY

示例：
```bash
mkdir -p secrets
echo "your_production_db_password" > secrets/db_password.txt
echo "your_production_db_user" > secrets/db_user.txt
echo "your_production_secret_key" > secrets/secret_key.txt
```

##### 2. 在 docker-compose.yml 中配置 Secrets

在 `docker-compose.yml` 文件中添加 secrets 配置：

```yaml
services:
  web:
    # ... 其他配置 ...
    secrets:
      - db_password
      - db_user
      - secret_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  db_user:
    file: ./secrets/db_user.txt
  secret_key:
    file: ./secrets/secret_key.txt
```

##### 3. 在环境变量中引用 Secrets

将环境变量指向 secrets 文件路径：

```yaml
environment:
  DB_USER: /run/secrets/db_user
  DB_PASSWORD: /run/secrets/db_password
  SECRET_KEY: /run/secrets/secret_key
```

##### 4. 在 Django 设置中读取 Secrets

Django 应用程序会自动从文件中读取 secrets 内容。

#### 安全最佳实践

1. **永远不要将 secrets 文件提交到代码仓库**
   - 确保 `secrets/` 目录在 `.gitignore` 文件中被忽略
   
2. **使用强密码和密钥**
   - 为所有 secrets 使用强随机值
   
3. **定期轮换 secrets**
   - 定期更改密码和密钥以降低安全风险
   
4. **限制文件权限**
   - 设置 secrets 文件的适当权限，确保只有必要的用户可以访问：
   ```bash
   chmod 600 secrets/*
   ```

5. **在生产环境中使用**
   - 仅在生产或预生产环境中使用真正的 secrets
   - 开发环境中使用环境变量或示例值

#### 故障排除

##### 1. Secrets 文件未找到
确保 secrets 文件存在于指定路径，并且 Docker Compose 有足够的权限读取它们。

##### 2. 权限问题
检查 secrets 文件的权限设置，确保它们只能被所有者读取。

##### 3. 应用程序无法读取 secrets
确认 Django settings.py 中的 `get_secret` 函数正确实现了从文件读取 secrets 的逻辑。

## Django Admin 用户管理指南

本文档介绍了如何使用 Django Admin 管理通过注册功能创建的用户账户。

### 访问 Admin 后台

1. 启动 Django 服务:
   ```bash
   python manage.py runserver
   ```

2. 访问 Admin 登录页面:
   在浏览器中打开 `http://127.0.0.1:8000/admin/`

3. 使用超级用户账户登录:
   - 如果尚未创建超级用户，请运行:
     ```bash
     python manage.py createsuperuser
     ```

### 用户管理功能

#### 查看用户列表

登录后，在 Admin 首页可以看到 "AUTHENTICATION AND AUTHORIZATION" 部分下的 "Users" 链接。点击进入可以看到所有用户列表，包括通过注册功能创建的用户。

列表显示字段：
- Username（用户名）
- Email address（邮箱）
- First name（名字）
- Last name（姓氏）
- Staff status（员工状态）
- Active（激活状态）

#### 搜索和过滤用户

- **搜索功能**：在搜索框中输入用户名、邮箱、姓名等关键词进行搜索
- **过滤功能**：使用右侧的过滤器按以下条件筛选用户：
  - Staff status（是否为员工）
  - Superuser status（是否为超级用户）
  - Active（是否激活）
  - Date joined（注册日期）

#### 编辑用户信息

点击任意用户名可以进入用户详情编辑页面，可以修改：

1. **基本信息**：
   - Username（用户名）
   - First name（名字）
   - Last name（姓氏）
   - Email（邮箱）

2. **权限设置**：
   - Active（激活状态）：取消勾选可禁用账户
   - Staff status（员工状态）：勾选后用户可以登录 Admin（但不能访问敏感区域）
   - Superuser status（超级用户状态）：勾选后用户拥有所有权限

3. **组和权限**：
   - Groups（组）：将用户分配到不同的组
   - User permissions（用户权限）：为用户分配特定权限

4. **重要日期**：
   - Last login（最后登录时间）
   - Date joined（注册时间）

#### 更改用户密码

在用户编辑页面底部有 "Change password" 链接，点击可以安全地更改用户密码。

#### 删除用户

在用户编辑页面底部有 "Delete" 按钮，点击可以删除用户。系统会提示确认删除操作。

#### 创建新用户

在用户列表页面顶部有 "Add user" 按钮，点击可以创建新用户。需要填写：
1. Username（用户名）
2. Password（密码）两次确认
3. 其他可选信息可以在创建后编辑

### 通过注册接口创建可登录 Admin 的用户

要通过注册接口创建可以直接登录 Admin 的用户，需要在注册时设置 `is_staff=true` 参数：

```bash
curl -X POST \
  http://localhost:8000/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "<your_username>",
    "password": "<secure_password>",
    "email": "<your_email>",
    "is_staff": true
  }'
```

设置了 `is_staff=true` 的用户就可以登录 Admin 后台了。但请注意，默认情况下他们只能查看和操作被授权的部分，除非同时设置为超级用户（`is_superuser=true`）。

### 注意事项

1. 通过注册接口创建的用户与通过 Admin 创建的用户没有区别，都可以在 Admin 中进行相同的管理操作。

2. 用户注册时会自动生成 Token，用于 API 认证。

3. 可以随时激活或禁用任何用户账户，而无需删除它们。

4. 用户权限管理是 Django Admin 的强大功能，可以根据业务需求灵活配置。

5. 仅为可信用户设置 `is_staff=true`，以免造成安全风险。

## JWT 认证使用指南

本文档介绍了系统中JWT认证的使用方法。

### 获取访问令牌

要获取JWT令牌对（访问令牌和刷新令牌），向`/auth/token/`端点发送POST请求：

```bash
curl -X POST \
  http://localhost:8000/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "<your_username>",
    "password": "<your_password>"
  }'
```

响应示例：
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTE2MjQ0MywiaWF0IjoxNjQ1MDc2MDQzLCJqdGkiOiJjZjk0MWZlM2U4YTE0MDQ4OTQ5Yzc4ODQyZWYwYzAwMCIsInVzZXJfaWQiOjF9.8B6vJtT4Q7hF3q4lR2tE3p5q6w7R8y9T0u1i2o3p4q5",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MDgwMDQzLCJpYXQiOjE2NDUwNzYwNDMsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### 刷新访问令牌

当访问令牌过期时，可以使用刷新令牌获取新的访问令牌。向`/auth/token/refresh/`端点发送POST请求：

```bash
curl -X POST \
  http://localhost:8000/auth/token/refresh/ \
  -H 'Content-Type: application/json' \
  -d '{
    "refresh": "your_refresh_token"
  }'
```

响应示例：
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MDgwMDQzLCJpYXQiOjE2NDUwNzYwNDMsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### 使用访问令牌

获取到访问令牌后，在需要认证的API请求中将其放在Authorization头部：

```bash
curl -X GET \
  http://localhost:8000/api/some-protected-endpoint/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

### 令牌生命周期

- 访问令牌默认有效期：5分钟
- 刷新令牌默认有效期：1天

这些值可以在`settings.py`中的`SIMPLE_JWT`配置中进行调整。