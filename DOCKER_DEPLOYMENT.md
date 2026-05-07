# Docker 容器化部署指南

> **域名**: www.aitengjiaoyu.top  
> **版本**: v0.2.1

---

## 部署架构

```
                    ┌─────────────┐
                    │   Nginx     │
                    │  (80/443)   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │ Frontend  │   │ Frontend  │   │  Backend  │
    │   Web     │   │   H5      │   │  (Django) │
    │  (3011)   │   │  (3022)   │   │  (8011)   │
    └───────────┘   └───────────┘   └─────┬─────┘
                                          │
                           ┌──────────────┼──────────────┐
                           │              │              │
                    ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
                    │    MySQL    │   │   Redis   │   │  Celery   │
                    │   (3306)    │   │  (6379)   │   │  Worker   │
                    └─────────────┘   └───────────┘   └───────────┘
```

---

## 前置要求

- Docker Engine 20.10+
- Docker Compose v2.0+
- 域名 SSL 证书（生产环境）

---

## 快速开始

### 1. 配置环境变量

```bash
# 复制配置文件
cp .env.production .env

# 编辑配置（必须修改）
nano .env
```

**必须修改的配置**：
- `SECRET_KEY` - Django 密钥（随机字符串）
- `DB_ROOT_PASS` - 数据库密码

### 2. 启动服务

```bash
# 构建并启动所有服务
docker compose -f docker-compose.production.yml up -d --build

# 查看服务状态
docker compose -f docker-compose.production.yml ps

# 查看日志
docker compose -f docker-compose.production.yml logs -f
```

### 3. 初始化数据

```bash
# 创建超级管理员
docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

---

## 服务端口

| 服务 | 容器端口 | 主机端口 | 说明 |
|------|----------|----------|------|
| Nginx | 80/443 | 80/443 | 反向代理入口 |
| Backend | 8000 | 8011 | Django API |
| Frontend Web | 80 | 3011 | 管理后台 |
| Frontend H5 | 80 | 3022 | 移动端 H5 |
| MySQL | 3306 | 3306 | 数据库 |
| Redis | 6379 | 6379 | 缓存 |

---

## 常用命令

```bash
# 启动服务
docker compose -f docker-compose.production.yml up -d

# 停止服务
docker compose -f docker-compose.production.yml down

# 重启服务
docker compose -f docker-compose.production.yml restart

# 重新构建并启动
docker compose -f docker-compose.production.yml up -d --build

# 查看日志
docker compose -f docker-compose.production.yml logs -f [service_name]

# 进入容器
docker compose -f docker-compose.production.yml exec backend bash
docker compose -f docker-compose.production.yml exec db mysql -u root -p

# 数据库备份
docker compose -f docker-compose.production.yml exec db mysqldump -u root -p education_prod > backup_$(date +%Y%m%d).sql

# 数据库恢复
docker compose -f docker-compose.production.yml exec -T db mysql -u root -p education_prod < backup.sql
```

---

## SSL 证书配置

### 方案一：使用 Let's Encrypt

```bash
# 安装 certbot
sudo apt-get install certbot

# 申请证书
sudo certbot certonly --standalone -d www.aitengjiaoyu.top -d aitengjiaoyu.top

# 证书路径
# /etc/letsencrypt/live/aitengjiaoyu.top/fullchain.pem
# /etc/letsencrypt/live/aitengjiaoyu.top/privkey.pem
```

### 方案二：使用云服务商证书

将证书文件放置到 `/etc/nginx/ssl/` 目录：
- `aitengjiaoyu.top.crt`
- `aitengjiaoyu.top.key`

---

## 数据持久化

Docker Volume 用于持久化存储：

| Volume | 说明 |
|--------|------|
| `mysql_data` | MySQL 数据 |
| `redis_data` | Redis 数据 |
| `static_data` | Django 静态文件 |
| `media_data` | 用户上传文件 |

---

## 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker compose -f docker-compose.production.yml logs [service_name]

# 检查容器状态
docker compose -f docker-compose.production.yml ps

# 检查资源使用
docker stats
```

### 数据库连接失败

```bash
# 检查数据库是否就绪
docker compose -f docker-compose.production.yml exec db mysqladmin ping

# 测试连接
docker compose -f docker-compose.production.yml exec backend python -c "import pymysql; pymysql.connect(host='db', user='root', password='YOUR_PASSWORD', database='education_prod')"
```

### 端口冲突

```bash
# 检查端口占用
sudo lsof -i :80
sudo lsof -i :443
sudo lsof -i :3306

# 修改 docker-compose.production.yml 中的端口映射
```

---

## 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker compose -f docker-compose.production.yml up -d --build

# 执行数据库迁移
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

---

## 生产环境建议

1. **修改默认密码**：确保修改所有默认密码
2. **配置防火墙**：只开放 80/443 端口
3. **定期备份**：配置自动备份脚本
4. **监控告警**：使用 Prometheus + Grafana 监控
5. **日志收集**：配置 ELK 或 Loki 收集日志
