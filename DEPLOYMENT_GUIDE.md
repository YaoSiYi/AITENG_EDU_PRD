# 艾腾教育 - 生产环境部署指南

> **域名**: www.aitengjiaoyu.top  
> **版本**: v0.2.1  
> **更新日期**: 2026-05-05

---

## 📋 部署架构

### 域名配置
- **主站（Web管理后台）**: https://www.aitengjiaoyu.top
- **Uni-app H5**: https://h5.aitengjiaoyu.top

### 端口分配
| 服务 | 端口 | 说明 |
|------|------|------|
| Django后端 | 8011 | API服务 |
| 前端Web | 3011 | 管理后台 |
| Uni-app H5 | 3022 | 移动端H5 |
| MySQL | 3306 | 数据库 |
| Redis | 6379 | 缓存 |

### 数据库
- **数据库名**: education_prod
- **独立数据库**，不与其他项目共用

---

## 🚀 部署前准备

### 1. DNS配置

在域名服务商（如阿里云、腾讯云）配置DNS解析：

```
A记录:
www.aitengjiaoyu.top  →  服务器IP
h5.aitengjiaoyu.top   →  服务器IP
```

### 2. SSL证书申请

使用 Let's Encrypt 免费证书：

```bash
# 安装 certbot
sudo apt-get install certbot python3-certbot-nginx

# 申请证书（通配符证书）
sudo certbot certonly --manual --preferred-challenges dns \
  -d aitengjiaoyu.top -d *.aitengjiaoyu.top

# 或者分别申请
sudo certbot certonly --nginx -d www.aitengjiaoyu.top
sudo certbot certonly --nginx -d h5.aitengjiaoyu.top
```

证书路径：
- 证书: `/etc/letsencrypt/live/aitengjiaoyu.top/fullchain.pem`
- 私钥: `/etc/letsencrypt/live/aitengjiaoyu.top/privkey.pem`

### 3. 创建数据库

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE education_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选，建议使用独立用户）
CREATE USER 'aiteng'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON education_prod.* TO 'aiteng'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📦 部署步骤

### 第一步：上传代码到服务器

```bash
# 在服务器上创建项目目录
sudo mkdir -p /var/www/aiteng
cd /var/www/aiteng

# 克隆代码（或使用scp上传）
git clone <your-repo-url> .

# 或使用rsync上传
rsync -avz --exclude 'node_modules' --exclude '.git' \
  /Users/yao/Node_Project/Aiteng_Edu_Prd/ \
  user@server:/var/www/aiteng/
```

### 第二步：配置环境变量

```bash
# 复制生产环境配置
cp .env.production .env

# 编辑配置文件
nano .env
```

**必须修改的配置**：

```bash
# 1. Django密钥（生成随机字符串）
SECRET_KEY=your-random-secret-key-here

# 2. 数据库密码
DB_ROOT_PASS=your-database-password

# 3. 关闭调试模式
DEBUG=False
```

### 第三步：安装后端依赖

```bash
cd /var/www/aiteng/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 第四步：初始化数据库

```bash
cd /var/www/aiteng/backend
source venv/bin/activate

# 运行数据库迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

### 第五步：安装前端依赖并构建

```bash
# 前端Web管理后台
cd /var/www/aiteng/frontend-web
npm install
npm run build

# Uni-app H5
cd /var/www/aiteng/frontend-uniapp
npm install
npm run build:h5
```

### 第六步：配置Nginx

```bash
# 复制Nginx配置
sudo cp /var/www/aiteng/nginx/nginx.production.conf \
  /etc/nginx/sites-available/aiteng

# 创建软链接
sudo ln -s /etc/nginx/sites-available/aiteng \
  /etc/nginx/sites-enabled/aiteng

# 修改SSL证书路径（如果证书路径不同）
sudo nano /etc/nginx/sites-available/aiteng

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 第七步：配置Systemd服务

创建后端服务配置：

```bash
sudo nano /etc/systemd/system/aiteng-backend.service
```

内容：

```ini
[Unit]
Description=Aiteng Education Backend
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/aiteng/backend
Environment="PATH=/var/www/aiteng/backend/venv/bin"
ExecStart=/var/www/aiteng/backend/venv/bin/gunicorn \
  --bind 127.0.0.1:8011 \
  --workers 4 \
  --timeout 120 \
  --access-logfile /var/log/aiteng/access.log \
  --error-logfile /var/log/aiteng/error.log \
  config.wsgi:application

[Install]
WantedBy=multi-user.target
```

创建前端Web服务：

```bash
sudo nano /etc/systemd/system/aiteng-web.service
```

内容：

```ini
[Unit]
Description=Aiteng Education Web Frontend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/aiteng/frontend-web
ExecStart=/usr/bin/npm run preview -- --port 3011 --host 127.0.0.1

[Install]
WantedBy=multi-user.target
```

创建Uni-app H5服务：

```bash
sudo nano /etc/systemd/system/aiteng-h5.service
```

内容：

```ini
[Unit]
Description=Aiteng Education H5 App
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/aiteng/frontend-uniapp
ExecStart=/usr/bin/npm run dev:h5 -- --port 3022 --host 127.0.0.1

[Install]
WantedBy=multi-user.target
```

启动所有服务：

```bash
# 创建日志目录
sudo mkdir -p /var/log/aiteng
sudo chown www-data:www-data /var/log/aiteng

# 重载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start aiteng-backend
sudo systemctl start aiteng-web
sudo systemctl start aiteng-h5

# 设置开机自启
sudo systemctl enable aiteng-backend
sudo systemctl enable aiteng-web
sudo systemctl enable aiteng-h5

# 查看服务状态
sudo systemctl status aiteng-backend
sudo systemctl status aiteng-web
sudo systemctl status aiteng-h5
```

---

## ✅ 验证部署

### 1. 检查服务状态

```bash
# 检查端口监听
sudo netstat -tlnp | grep -E '8011|3011|3022'

# 应该看到：
# 8011 - gunicorn (后端)
# 3011 - node (Web前端)
# 3022 - node (H5前端)
```

### 2. 测试访问

- **Web管理后台**: https://www.aitengjiaoyu.top
- **H5移动端**: https://h5.aitengjiaoyu.top
- **API接口**: https://www.aitengjiaoyu.top/api/
- **Django Admin**: https://www.aitengjiaoyu.top/admin/

### 3. 检查日志

```bash
# Nginx日志
sudo tail -f /var/log/nginx/aiteng_access.log
sudo tail -f /var/log/nginx/aiteng_error.log

# 后端日志
sudo tail -f /var/log/aiteng/access.log
sudo tail -f /var/log/aiteng/error.log

# Systemd服务日志
sudo journalctl -u aiteng-backend -f
sudo journalctl -u aiteng-web -f
sudo journalctl -u aiteng-h5 -f
```

---

## 🔧 常见问题

### 1. 502 Bad Gateway

**原因**: 后端服务未启动或端口不正确

**解决**:
```bash
sudo systemctl status aiteng-backend
sudo systemctl restart aiteng-backend
```

### 2. 静态文件404

**原因**: 静态文件未收集或路径配置错误

**解决**:
```bash
cd /var/www/aiteng/backend
source venv/bin/activate
python manage.py collectstatic --noinput
```

### 3. 数据库连接失败

**原因**: 数据库配置错误或数据库未启动

**解决**:
```bash
# 检查MySQL状态
sudo systemctl status mysql

# 测试数据库连接
mysql -u root -p -e "USE education_prod;"
```

### 4. SSL证书错误

**原因**: 证书路径不正确或证书过期

**解决**:
```bash
# 检查证书
sudo certbot certificates

# 续期证书
sudo certbot renew
```

---

## 🔄 更新部署

### 更新代码

```bash
cd /var/www/aiteng

# 拉取最新代码
git pull origin main

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# 更新前端Web
cd ../frontend-web
npm install
npm run build

# 更新Uni-app H5
cd ../frontend-uniapp
npm install
npm run build:h5

# 重启服务
sudo systemctl restart aiteng-backend
sudo systemctl restart aiteng-web
sudo systemctl restart aiteng-h5
```

---

## 📊 监控和维护

### 1. 设置定时任务

```bash
# 编辑crontab
sudo crontab -e

# 添加以下任务：

# 每天凌晨2点备份数据库
0 2 * * * mysqldump -u root -p'password' education_prod > /backup/education_$(date +\%Y\%m\%d).sql

# 每周日凌晨3点清理旧日志
0 3 * * 0 find /var/log/aiteng -name "*.log" -mtime +30 -delete

# 每月1号检查SSL证书
0 0 1 * * certbot renew --quiet
```

### 2. 监控服务

使用工具如 Prometheus + Grafana 或简单的监控脚本：

```bash
#!/bin/bash
# /usr/local/bin/check_aiteng.sh

services=("aiteng-backend" "aiteng-web" "aiteng-h5")

for service in "${services[@]}"; do
  if ! systemctl is-active --quiet $service; then
    echo "$service is down, restarting..."
    systemctl restart $service
    # 发送告警邮件或通知
  fi
done
```

---

## 🔐 安全建议

1. **防火墙配置**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **定期更新系统**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **备份策略**
   - 每天自动备份数据库
   - 每周备份代码和配置文件
   - 备份保留30天

4. **日志轮转**
```bash
sudo nano /etc/logrotate.d/aiteng
```

内容：
```
/var/log/aiteng/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload aiteng-backend > /dev/null 2>&1 || true
    endscript
}
```

---

## 📞 技术支持

如遇问题，请检查：
1. 服务状态: `sudo systemctl status aiteng-*`
2. 日志文件: `/var/log/aiteng/` 和 `/var/log/nginx/`
3. 端口占用: `sudo netstat -tlnp`
4. 磁盘空间: `df -h`

---

**部署完成！** 🎉

访问 https://www.aitengjiaoyu.top 开始使用系统。
