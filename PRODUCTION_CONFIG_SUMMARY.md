# 生产环境配置总结

> **配置日期**: 2026-05-05  
> **版本**: v0.2.1  
> **部署方案**: 子域名方案

---

## 📋 配置概览

### 域名配置
| 服务 | 域名 | 端口 |
|------|------|------|
| Web管理后台 | https://www.aitengjiaoyu.top | 3011 |
| Uni-app H5 | https://h5.aitengjiaoyu.top | 3022 |
| Django后端 | (内部) | 8011 |

### 数据库配置
- **数据库名**: education_prod
- **独立数据库**，不与其他项目共用
- **端口**: 3306

---

## 📁 新增配置文件

### 1. 环境变量配置
- ✅ `.env.production` - 生产环境变量配置
- ✅ `frontend-web/.env.production` - Web前端生产配置
- ✅ `frontend-uniapp/.env.production` - Uni-app生产配置

### 2. Nginx配置
- ✅ `nginx/nginx.production.conf` - 生产环境Nginx配置
  - 支持HTTPS
  - 配置了主站和H5子域名
  - 包含SSL证书配置
  - 配置了静态文件和媒体文件路径

### 3. 部署文档
- ✅ `DEPLOYMENT_GUIDE.md` - 详细部署指南
- ✅ `deploy-production.sh` - 自动化部署脚本
- ✅ `PRODUCTION_CONFIG_SUMMARY.md` - 本文档

---

## 🔧 已修改的文件

### 前端配置修改

1. **frontend-uniapp/src/utils/request.js**
   - 修改生产环境API地址: `https://www.aitengjiaoyu.top/api`
   - 保持开发环境地址: `http://192.168.0.156:8000/api`

2. **frontend-uniapp/src/common/request.js**
   - 添加环境判断逻辑
   - 标记为废弃文件，建议使用 `utils/request.js`

3. **frontend-uniapp/src/manifest.json**
   - 更新版本号: `0.2.1`
   - 版本代码: `021`

### 清理工作

1. **删除测试页面**
   - ✅ 删除 `frontend-uniapp/src/pages/test/` 目录
   - 测试页面不应出现在生产环境

---

## 🚀 部署前检查清单

### 必须完成的配置

- [ ] **DNS解析**: 配置 www.aitengjiaoyu.top 和 h5.aitengjiaoyu.top
- [ ] **SSL证书**: 申请并配置SSL证书
- [ ] **数据库**: 创建 education_prod 数据库
- [ ] **环境变量**: 修改 .env.production 中的密钥和密码
  - [ ] SECRET_KEY (生成随机字符串)
  - [ ] DB_ROOT_PASS (数据库密码)
  - [ ] DEBUG=False (关闭调试模式)

### 可选配置

- [ ] **微信小程序AppID**: 如果要发布小程序
- [ ] **短信服务**: 阿里云短信配置
- [ ] **文件存储**: OSS配置（如需要）
- [ ] **高德地图**: API Key配置（如需要）

---

## 📝 部署步骤（简要）

1. **上传代码到服务器**
   ```bash
   rsync -avz /Users/yao/Node_Project/Aiteng_Edu_Prd/ user@server:/var/www/aiteng/
   ```

2. **配置环境变量**
   ```bash
   cp .env.production .env
   nano .env  # 修改密钥和密码
   ```

3. **运行部署脚本**
   ```bash
   ./deploy-production.sh
   ```

4. **配置Nginx和Systemd**
   - 按照 DEPLOYMENT_GUIDE.md 完成配置

5. **启动服务**
   ```bash
   sudo systemctl start aiteng-backend
   sudo systemctl start aiteng-web
   sudo systemctl start aiteng-h5
   ```

详细步骤请参考: **DEPLOYMENT_GUIDE.md**

---

## 🔐 安全注意事项

### 生产环境必须修改

1. **SECRET_KEY**: 生成随机字符串
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **数据库密码**: 使用强密码

3. **DEBUG模式**: 必须设置为 False

4. **ALLOWED_HOSTS**: 只允许指定域名访问

### 不要提交到Git

以下文件包含敏感信息，不应提交到Git：
- `.env`
- `.env.production` (如果包含真实密码)
- SSL证书文件

---

## 🔄 与其他项目的区分

### 端口区分
- 后端: 8011 (避免与其他项目的8000等端口冲突)
- Web前端: 3011 (避免与其他项目的3000等端口冲突)
- H5前端: 3022 (独立端口)

### 域名区分
- 使用独立子域名: www.aitengjiaoyu.top
- H5使用子域名: h5.aitengjiaoyu.top

### 数据库区分
- 独立数据库: education_prod
- 不与其他项目共用数据库

### 服务名称区分
- Systemd服务名: aiteng-backend, aiteng-web, aiteng-h5
- 日志目录: /var/log/aiteng/
- 项目目录: /var/www/aiteng/

---

## 📊 监控和维护

### 日志位置
- Nginx访问日志: `/var/log/nginx/aiteng_access.log`
- Nginx错误日志: `/var/log/nginx/aiteng_error.log`
- 后端日志: `/var/log/aiteng/access.log` 和 `/var/log/aiteng/error.log`
- Systemd日志: `journalctl -u aiteng-backend`

### 常用命令
```bash
# 查看服务状态
sudo systemctl status aiteng-backend
sudo systemctl status aiteng-web
sudo systemctl status aiteng-h5

# 重启服务
sudo systemctl restart aiteng-backend
sudo systemctl restart aiteng-web
sudo systemctl restart aiteng-h5

# 查看日志
sudo tail -f /var/log/aiteng/error.log
sudo journalctl -u aiteng-backend -f

# 检查端口
sudo netstat -tlnp | grep -E '8011|3011|3022'
```

---

## ✅ 配置完成状态

- ✅ 生产环境配置文件已创建
- ✅ 前端API地址已更新
- ✅ Nginx配置已准备
- ✅ 部署文档已完成
- ✅ 部署脚本已创建
- ✅ 测试代码已清理
- ✅ 版本号已统一

**下一步**: 按照 DEPLOYMENT_GUIDE.md 进行实际部署

---

**配置完成时间**: 2026-05-05  
**配置人员**: YaoSiYi + Claude Sonnet 4.6
