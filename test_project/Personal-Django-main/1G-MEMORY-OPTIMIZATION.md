# 1G内存服务器Docker部署优化指南

## 优化概述

针对1G内存服务器的Docker部署进行了全面优化，主要包括：

### 1. 镜像优化
- **基础镜像**: 从 `python:3.9-slim` 改为 `python:3.9-alpine`，减少约60%镜像大小
- **多阶段构建**: 分离构建和运行环境，减少最终镜像大小
- **依赖清理**: 及时清理构建缓存和临时文件

### 2. 内存限制优化
- **Web容器**: 限制400M内存，预留200M
- **Nginx容器**: 限制100M内存，预留50M
- **总内存使用**: 约500M，为系统保留500M

### 3. Gunicorn配置优化
```bash
--workers 1                    # 单进程，避免内存浪费
--worker-class sync           # 同步工作模式，内存效率高
--max-requests 300            # 降低请求数，减少内存泄漏
--timeout 30                  # 合理超时时间
--keep-alive 2               # 短连接保持时间
--preload                    # 预加载应用，减少内存占用
--worker-tmp-dir /dev/shm    # 使用内存文件系统
```

### 4. Nginx优化
- **缓冲区优化**: 减少缓冲区大小，降低内存使用
- **连接优化**: 合理设置keepalive参数
- **压缩配置**: 启用gzip压缩，减少传输量

### 5. 系统级优化
- **Swap配置**: 自动创建512MB swap文件
- **Docker优化**: 限制日志大小，优化存储驱动
- **内存监控**: 实时监控内存使用情况

## 部署步骤

### 1. 环境准备
```bash
# 确保系统内存至少900MB
free -h

# 检查Docker和Docker Compose
docker --version
docker-compose --version
```

### 2. 配置环境变量
```bash
# 复制环境配置模板
cp .env.example .env

# 编辑配置文件（建议使用SQLite以节省内存）
vim .env
```

推荐的1G内存服务器配置：
```env
DEBUG=0
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=your-domain.com

# 使用SQLite节省内存
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# 如果内存充足可以启用Redis
# REDIS_URL=redis://redis:6379/0
```

### 3. 执行部署
```bash
# 一键部署（包含所有优化）
./deploy.sh

# 或者分步执行
./deploy.sh cleanup    # 清理资源
./deploy.sh deploy     # 开始部署
./deploy.sh monitor    # 监控资源
```

## 监控和维护

### 1. 资源监控
```bash
# 查看系统资源使用
./deploy.sh monitor

# 实时监控容器资源
docker stats

# 查看内存使用详情
free -h
```

### 2. 日志管理
```bash
# 查看服务日志
./deploy.sh logs

# 查看特定服务日志
docker-compose logs web -f
```

### 3. 性能调优
```bash
# 重启服务释放内存
./deploy.sh restart

# 清理Docker资源
./deploy.sh cleanup
```

## 内存使用分析

### 预期内存分配
- **系统**: ~200MB
- **Docker daemon**: ~50MB
- **Web容器**: ~300-400MB
- **Nginx容器**: ~50-80MB
- **缓冲区**: ~100MB
- **总计**: ~700-830MB

### 内存警告阈值
- **85%以上**: 高内存使用警告
- **90%以上**: 建议重启服务
- **95%以上**: 系统可能不稳定

## 故障排除

### 1. 内存不足
```bash
# 检查内存使用
free -h
docker stats --no-stream

# 清理系统缓存
sync && echo 3 > /proc/sys/vm/drop_caches

# 重启服务
./deploy.sh restart
```

### 2. 容器启动失败
```bash
# 查看详细日志
docker-compose logs web

# 检查资源限制
docker inspect <container_id> | grep -i memory
```

### 3. 性能问题
```bash
# 检查swap使用
swapon --show

# 监控IO等待
iostat -x 1

# 检查网络连接
netstat -tuln
```

## 最佳实践

### 1. 定期维护
- 每周执行一次 `./deploy.sh cleanup`
- 定期检查日志文件大小
- 监控磁盘空间使用

### 2. 数据库选择
- **SQLite**: 适合小型应用，无额外内存开销
- **PostgreSQL**: 如需要，建议使用外部数据库服务

### 3. 缓存策略
- 避免使用Redis（除非内存充足）
- 利用Django内置缓存框架
- 使用文件系统缓存

### 4. 静态文件
- 启用nginx gzip压缩
- 设置合理的缓存策略
- 考虑使用CDN

## 扩展建议

当应用增长超出1G内存限制时：

1. **升级服务器**: 增加到2G或4G内存
2. **服务分离**: 将数据库迁移到独立服务器
3. **负载均衡**: 使用多个小内存实例
4. **缓存优化**: 引入Redis或Memcached

## 监控脚本

可以使用以下脚本监控内存使用：

```bash
#!/bin/bash
# memory_monitor.sh
while true; do
    mem_usage=$(free | awk 'NR==2{printf "%.0f", $3/$2*100}')
    if [ "$mem_usage" -gt 85 ]; then
        echo "$(date): 内存使用率高: ${mem_usage}%"
        # 可以添加告警逻辑
    fi
    sleep 60
done
```

通过这些优化，你的Django应用可以在1G内存服务器上稳定运行，同时保持良好的性能表现。