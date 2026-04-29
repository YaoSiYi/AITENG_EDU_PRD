#!/bin/bash

# ============================================
# Django 项目自动化部署脚本
# 支持一键部署、Cloudflare IP 更新、安全加固
# ============================================

# 确保脚本具有执行权限
chmod +x "$0"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 启用 BuildKit（推荐）
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_debug() {
    if [ "$DEBUG" = "true" ]; then
        echo -e "${PURPLE}[DEBUG]${NC} $1"
    fi
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装"
        exit 1
    fi
}

# 检查 Docker Compose 版本
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
        log_debug "使用 Docker Compose 命令: $DOCKER_COMPOSE_CMD"
    else
        log_error "Docker Compose 未安装"
        exit 1
    fi
}


# 获取容器 ID
get_container_id() {
    local service_name=$1
    $DOCKER_COMPOSE_CMD ps -q $service_name 2>/dev/null | head -1
}

# 更新 Cloudflare IP 列表到 Django 设置
update_cloudflare_ips() {
    log_info "更新 Cloudflare IP 列表到 Django 配置..."

    local CF_IPV4_URL="https://www.cloudflare.com/ips-v4/"
    local CF_IPV6_URL="https://www.cloudflare.com/ips-v6/"

    # 动态获取最新的 Cloudflare IP 列表
    log_info "从 Cloudflare 官方获取最新的 IP 列表..."

    # 获取 IPv4 列表
    IPV4_LIST=$(curl -s --connect-timeout 10 "$CF_IPV4_URL" 2>/dev/null | grep -E '^[0-9]' | head -30)
    if [ -z "$IPV4_LIST" ]; then
        log_warning "无法获取 Cloudflare IPv4 列表，使用备用列表"
        IPV4_LIST="173.245.48.0/20
103.21.244.0/22
103.22.200.0/22
103.31.4.0/22
141.101.64.0/18
108.162.192.0/18
190.93.240.0/20
188.114.96.0/20
197.234.240.0/22
198.41.128.0/17
162.158.0.0/15
104.16.0.0/13
104.24.0.0/14
172.64.0.0/13
131.0.72.0/22"
    fi

    # 获取 IPv6 列表
    IPV6_LIST=$(curl -s --connect-timeout 10 "$CF_IPV6_URL" 2>/dev/null | grep -E '^[0-9a-fA-F:]' | head -20)
    if [ -z "$IPV6_LIST" ]; then
        log_warning "无法获取 Cloudflare IPv6 列表，使用备用列表"
        IPV6_LIST="2400:cb00::/32
2606:4700::/32
2803:f800::/32
2405:b500::/32
2405:8100::/32
2a06:98c0::/29
2c0f:f248::/32"
    fi

    # 构建 Python 列表格式
    PYTHON_IP_LIST="# Cloudflare IP ranges - Auto updated on $(date '+%Y-%m-%d %H:%M:%S')\nCLOUDFLARE_IPS = ["

    # 添加 IPv4
    while IFS= read -r ip; do
        if [ -n "$ip" ]; then
            PYTHON_IP_LIST="$PYTHON_IP_LIST\n    '$ip',"
        fi
    done <<< "$IPV4_LIST"

    # 添加 IPv6
    while IFS= read -r ip; do
        if [ -n "$ip" ]; then
            PYTHON_IP_LIST="$PYTHON_IP_LIST\n    '$ip',"
        fi
    done <<< "$IPV6_LIST"

    PYTHON_IP_LIST="$PYTHON_IP_LIST\n]"

    # 保存到临时文件
    echo -e "$PYTHON_IP_LIST" > ./cloudflare_ips.py

    # 查找 Web 容器并更新 Django 设置
    local web_container=$(get_container_id "web")

    if [ -n "$web_container" ]; then
        log_info "更新 Django 中的 Cloudflare IP 配置..."

        # 将 IP 列表复制到容器中
        docker cp ./cloudflare_ips.py $web_container:/app/cloudflare_ips.py

        # 更新 settings.py 中的 CLOUDFLARE_IPS
        docker exec $web_container python -c "
import re

# 读取新的 IP 列表
with open('/app/cloudflare_ips.py', 'r') as f:
    new_ips = f.read()

# 读取当前 settings.py
with open('/app/DjangoProject/settings.py', 'r') as f:
    settings_content = f.read()

# 替换 CLOUDFLARE_IPS 部分
pattern = r'CLOUDFLARE_IPS = \[.*?\]'
if re.search(pattern, settings_content, re.DOTALL):
    settings_content = re.sub(pattern, new_ips.split('\n', 1)[1], settings_content, flags=re.DOTALL)
else:
    # 如果不存在，添加到文件末尾
    settings_content += '\n\n' + new_ips

# 写回文件
with open('/app/DjangoProject/settings.py', 'w') as f:
    f.write(settings_content)

print('Cloudflare IP 列表已更新到 Django 设置')
"

        if [ $? -eq 0 ]; then
            log_success "Cloudflare IP 列表已更新到 Django 配置"
            log_info "更新了 $(echo "$IPV4_LIST" | wc -l) 个 IPv4 范围和 $(echo "$IPV6_LIST" | wc -l) 个 IPv6 范围"
            
            # 重启 Web 服务以应用更改
            log_info "重启 Web 服务以应用 IP 列表更改..."
            $DOCKER_COMPOSE_CMD restart web
        else
            log_error "无法更新 Django 中的 Cloudflare IP 配置"
        fi

        # 清理临时文件
        rm -f ./cloudflare_ips.py
        docker exec $web_container rm -f /app/cloudflare_ips.py
    else
        log_warning "Web 容器未运行，跳过 Cloudflare IP 更新"
        log_info "Cloudflare IP 列表已保存到 ./cloudflare_ips.py"
    fi
}

# 加固 Nginx 安全配置
harden_nginx_security() {
    log_info "加固 Nginx 安全配置..."

    local nginx_container=$(get_container_id "nginx")
    if [ -z "$nginx_container" ]; then
        log_error "未找到运行中的 Nginx 容器"
        return 1
    fi

    # 安全头配置（移除 Cloudflare IP 限制，由 Django 中间件处理）
    local security_config='# Security Headers Configuration
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# 生产环境 CSP
add_header Content-Security-Policy "default-src '\''self'\''; script-src '\''self'\'' '\''unsafe-inline'\'' '\''unsafe-eval'\'' https://static.cloudflareinsights.com; style-src '\''self'\'' '\''unsafe-inline'\'' https://fonts.googleapis.com; img-src '\''self'\'' data: https:; font-src '\''self'\'' https://fonts.gstatic.com; connect-src '\''self'\''; frame-ancestors '\''self'\'';" always;

# Cloudflare 真实 IP 获取（保留用于日志记录）
set_real_ip_from 173.245.48.0/20;
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
set_real_ip_from 103.31.4.0/22;
set_real_ip_from 141.101.64.0/18;
set_real_ip_from 108.162.192.0/18;
set_real_ip_from 190.93.240.0/20;
set_real_ip_from 188.114.96.0/20;
set_real_ip_from 197.234.240.0/22;
set_real_ip_from 198.41.128.0/17;
set_real_ip_from 162.158.0.0/15;
set_real_ip_from 104.16.0.0/13;
set_real_ip_from 104.24.0.0/14;
set_real_ip_from 172.64.0.0/13;
set_real_ip_from 131.0.72.0/22;
set_real_ip_from 2400:cb00::/32;
set_real_ip_from 2606:4700::/32;
set_real_ip_from 2803:f800::/32;
set_real_ip_from 2405:b500::/32;
set_real_ip_from 2405:8100::/32;
set_real_ip_from 2a06:98c0::/29;
set_real_ip_from 2c0f:f248::/32;
real_ip_header CF-Connecting-IP;
real_ip_recursive on;'

    # 在 nginx 容器内创建安全头配置
    echo "$security_config" | docker exec -i $nginx_container sh -c 'cat > /etc/nginx/security-headers.conf'

    if [ $? -ne 0 ]; then
        log_error "无法写入安全头配置"
        return 1
    fi

    # 确保 nginx.conf 包含安全配置
    if ! docker exec $nginx_container grep -q "security-headers.conf" /etc/nginx/nginx.conf; then
        docker exec $nginx_container sed -i '/http {/a\    # Security headers configuration\n    include /etc/nginx/security-headers.conf;' /etc/nginx/nginx.conf
    fi

    # 测试并重新加载配置
    log_info "测试 Nginx 配置..."
    if docker exec $nginx_container nginx -t 2>/dev/null; then
        log_info "重新加载 Nginx 配置..."
        docker exec $nginx_container nginx -s reload 2>/dev/null
        log_success "Nginx 安全头配置已应用并重新加载"
        echo -e "${CYAN}📋 已应用的安全头:${NC}"
        echo "  - X-Frame-Options: SAMEORIGIN"
        echo "  - X-Content-Type-Options: nosniff"
        echo "  - X-XSS-Protection: 1; mode=block"
        echo "  - Referrer-Policy: strict-origin-when-cross-origin"
        echo "  - Permissions-Policy: 限制地理位置/麦克风/摄像头"
        echo "  - Strict-Transport-Security: 强制 HTTPS"
        echo "  - Content-Security-Policy: 生产级 CSP"
        echo "  - Cloudflare Real IP: 用于日志记录（IP 限制由 Django 处理）"
    else
        log_error "Nginx 配置测试失败"
        docker exec $nginx_container nginx -t
        return 1
    fi
}

# 清理 Docker 资源
cleanup_docker() {
    log_info "开始清理 Docker 资源（1G内存优化）..."

    local confirm="n"
    # CI环境或FORCE模式下自动确认
    if [ "$CI" = "true" ] || [ "$FORCE" = "true" ]; then
        confirm="y"
    else
        read -p "⚠️  确定要清理 Docker 资源吗？(y/N): " confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            log_info "取消清理操作"
            return
        fi
    fi

    # 停止所有容器以释放内存
    log_info "停止所有容器以释放内存..."
    docker stop $(docker ps -aq) 2>/dev/null || true

    # 清理构建缓存
    log_info "清理构建缓存..."
    DOCKER_BUILDKIT=1 docker builder prune -af

    # 删除未使用的镜像
    log_info "删除未使用的镜像..."
    docker image prune -af

    # 删除停止的容器
    log_info "删除停止的容器..."
    docker container prune -f

    # 删除未使用的网络
    log_info "删除未使用的网络..."
    docker network prune -f

    # 删除未使用的数据卷（需要确认，因为可能包含重要数据）
    log_info "清理未使用的数据卷..."
    docker volume prune -f

    # 系统级清理
    log_info "执行系统级Docker清理..."
    docker system prune -af --volumes

    log_success "Docker 资源清理完成"
}

# 检查环境
check_environment() {
    log_info "检查部署环境（1G内存优化）..."

    # 检查系统内存
    local total_mem=$(free -m 2>/dev/null | awk 'NR==2{printf "%.0f", $2}' || echo "unknown")
    if [ "$total_mem" != "unknown" ]; then
        log_info "检测到系统内存: ${total_mem}MB"
        if [ "$total_mem" -lt 900 ]; then
            log_error "系统内存不足1GB，当前: ${total_mem}MB"
            exit 1
        elif [ "$total_mem" -lt 1200 ]; then
            log_warning "系统内存较低: ${total_mem}MB，将使用优化配置"
        fi
    fi

    # 检查 Docker
    check_command docker

    # 检查 Docker Compose
    check_docker_compose

    # 检查 curl
    check_command curl

    # 优化系统设置
    optimize_system_for_1g

    # 检查 .env 文件
    if [ ! -f ".env" ]; then
        log_warning ".env 文件不存在"

        cat > .env.example << 'ENV_EOF'
# ========================================
# Django 环境配置文件 (1G内存优化)
# 请复制为 .env 并修改配置
# ========================================

# Django 核心设置
DEBUG=0
SECRET_KEY=your-secret-key-here-change-this
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,your-domain.com

# 数据库配置 (建议使用SQLite以节省内存)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
# 如果使用PostgreSQL，请取消注释以下配置
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=mydatabase
# DB_USER=mydbuser
# DB_PASSWORD=your-strong-password-here
# DB_HOST=db
# DB_PORT=5432

# Redis 缓存配置（可选，内存充足时使用）
# REDIS_URL=redis://redis:6379/0

# JWT 登录 Token 签名密钥（务必设置，否则重启后旧 Token 失效）
# 可与 SECRET_KEY 相同，或单独生成：openssl rand -base64 48
JWT_SIGNING_KEY=your-jwt-signing-key-change-this

# 是否暴露 API 文档 /swagger/ /redoc/（0=关闭 1=开启，生产建议 0）
ENABLE_API_DOCS=0

# CORS 设置
DJANGO_CORS_ALLOWED_ORIGINS=https://your-domain.com
# 内网访问 admin 时，把访问地址加到这里，如 http://192.168.1.10；HTTPS 公网用 https://your-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com
# 内网用 HTTP 访问 admin 时设为 0，否则会 403 CSRF
# CSRF_COOKIE_SECURE=0
# SESSION_COOKIE_SECURE=0

# 静态文件设置
STATIC_URL=/static/
MEDIA_URL=/media/
ENV_EOF

        log_error "请创建 .env 文件并配置环境变量"
        log_info "可以使用: cp .env.example .env"
        log_info "然后编辑 .env 文件配置正确的值"
        exit 1
    else
        # 检查关键配置是否已修改
        if grep -q "change-this-to-a-random-secret-key" .env || \
           grep -q "your_password_here" .env || \
           grep -q "your_domain.com" .env; then
            log_warning ".env 文件中包含默认值，请确保已修改为实际配置"
            read -p "按 Enter 继续，或 Ctrl+C 退出修改配置: " dummy
        fi
    fi

    # 检查 docker-compose.yml 文件
    if [ ! -f "docker-compose.yml" ] && [ ! -f "docker-compose.yaml" ]; then
        log_error "未找到 docker-compose.yml 文件"
        exit 1
    fi

    log_success "环境检查完成"
}

# 停止现有服务
stop_services() {
    log_info "停止现有服务..."
    $DOCKER_COMPOSE_CMD down
}


# 构建和启动服务
start_services() {
    log_info "构建和启动 Docker 服务..."

    # 构建镜像
    log_info "构建 Docker 镜像..."
    DOCKER_BUILDKIT=1 $DOCKER_COMPOSE_CMD build --no-cache

    if [ $? -ne 0 ]; then
        log_error "Docker 镜像构建失败"
        exit 1
    fi

    # 启动服务
    log_info "启动服务..."
    timeout 120 $DOCKER_COMPOSE_CMD up -d --force-recreate

    if [ $? -ne 0 ]; then
        log_error "服务启动失败"
        exit 1
    fi

    # 等待服务启动
    log_info "等待服务启动..."
    local attempts=30
    local count=0
    while [ $count -lt $attempts ]; do
        if $DOCKER_COMPOSE_CMD ps | grep -q "Up.*healthy"; then
            log_success "服务启动成功"
            break
        fi
        echo -n "."
        sleep 2
        count=$((count+1))
        if [ $count -eq $attempts ]; then
            log_warning "服务启动超时，但继续执行后续步骤"
            break
        fi
    done
    echo ""
}

# 执行数据库迁移
run_migrations() {
    log_info "检查容器状态（迁移已在容器启动时自动执行）..."

    local web_container=$(get_container_id "web")
    if [ -z "$web_container" ]; then
        log_error "Web 服务未运行"
        log_info "检查容器日志..."
        $DOCKER_COMPOSE_CMD logs --tail=50 web
        return 1
    fi

    # 检查容器是否在反复重启
    log_info "等待容器稳定运行..."
    local restart_count=0
    for i in {1..30}; do
        local status=$(docker inspect --format='{{.State.Status}}' $web_container 2>/dev/null)
        if [ "$status" = "running" ]; then
            log_success "容器运行正常"
            return 0
        elif [ "$status" = "restarting" ]; then
            restart_count=$((restart_count+1))
            if [ $restart_count -gt 5 ]; then
                log_error "容器反复重启，查看日志排查问题"
                $DOCKER_COMPOSE_CMD logs --tail=100 web
                return 1
            fi
        fi
        sleep 2
    done

    log_error "容器启动超时或异常"
    return 1
}

# 收集静态文件
collect_static() {
    log_info "收集静态文件..."

    local web_container=$(get_container_id "web")
    if [ -n "$web_container" ]; then
        $DOCKER_COMPOSE_CMD exec web python manage.py collectstatic --noinput --clear

        if [ $? -eq 0 ]; then
            log_success "静态文件收集完成"
        else
            log_error "静态文件收集失败"
        fi
    else
        log_error "Web 服务未运行，无法收集静态文件"
    fi
}

# 创建超级用户（可选）
create_superuser() {
    if [ "$CREATE_SUPERUSER" = "true" ]; then
        log_info "检查是否需要创建超级用户..."

        local web_container=$(get_container_id "web")
        if [ -n "$web_container" ]; then
            # 检查是否已存在超级用户
            if docker exec $web_container python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(is_superuser=True).exists():
    print('exists')
else:
    print('not_exists')
" 2>/dev/null | grep -q "not_exists"; then
                log_info "创建超级用户..."
                echo -e "${YELLOW}请输入超级用户信息:${NC}"
                read -p "用户名 (默认: admin): " username
                username=${username:-admin}
                read -p "邮箱: " email
                read -sp "密码: " password
                echo

                docker exec $web_container python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    user = User.objects.create_superuser('$username', '$email', '$password')
    print('超级用户创建成功')
except Exception as e:
    print(f'创建失败: {e}')
" 2>/dev/null
            else
                log_info "超级用户已存在，跳过创建"
            fi
        fi
    fi
}

# 优化1G内存系统设置
optimize_system_for_1g() {
    log_info "优化1G内存系统设置..."
    
    # 检查并创建swap（如果没有且有权限）
    if [ ! -f /swapfile ] && [ "$(id -u)" = "0" ]; then
        log_info "创建512MB swap文件..."
        fallocate -l 512M /swapfile 2>/dev/null || dd if=/dev/zero of=/swapfile bs=1M count=512
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        echo '/swapfile none swap sw 0 0' >> /etc/fstab
        log_success "Swap文件创建完成"
    elif [ ! -f /swapfile ]; then
        log_warning "无root权限，无法创建swap文件，建议手动创建"
    fi
    
    # 设置Docker daemon优化（如果有权限）
    if [ -w /etc/docker ] || [ -w /etc/docker/daemon.json ]; then
        log_info "优化Docker daemon配置..."
        cat > /tmp/daemon.json << 'DOCKER_EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
DOCKER_EOF
        
        if [ -w /etc/docker ]; then
            cp /tmp/daemon.json /etc/docker/daemon.json
            systemctl reload docker 2>/dev/null || service docker reload 2>/dev/null || true
            log_success "Docker daemon配置已优化"
        fi
        rm -f /tmp/daemon.json
    fi
}

# 健康检查
health_check() {
    log_info "执行健康检查（1G内存监控）..."

    echo -e "\n${CYAN}====== 服务状态 ======${NC}"
    $DOCKER_COMPOSE_CMD ps

    echo -e "\n${CYAN}====== 系统内存使用 ======${NC}"
    free -h

    echo -e "\n${CYAN}====== 容器资源使用情况 ======${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" | head -10

    echo -e "\n${CYAN}====== 磁盘使用情况 ======${NC}"
    df -h | head -5

    echo -e "\n${CYAN}====== 最近日志 ======${NC}"
    $DOCKER_COMPOSE_CMD logs --tail=5 --timestamps

    # 检查内存使用警告
    local mem_usage=$(free | awk 'NR==2{printf "%.0f", $3/$2*100}')
    if [ "$mem_usage" -gt 85 ]; then
        log_warning "内存使用率较高: ${mem_usage}%"
    fi

    # 检查 Web 服务健康端点
    local web_container=$(get_container_id "web")
    if [ -n "$web_container" ]; then
        echo -e "\n${CYAN}====== Web 服务健康检查 ======${NC}"
        if docker exec $web_container curl -s -f http://localhost:8000/admin/ > /dev/null 2>&1; then
            log_success "Web 服务健康检查通过"
        else
            log_warning "Web 服务健康检查失败，检查服务状态"
        fi
    fi
}



# 主部署函数
main_deploy() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}  Django 1G内存优化部署脚本   ${NC}"
    echo -e "${CYAN}================================${NC}"

    # 设置调试模式
    if [ "$1" = "--debug" ]; then
        DEBUG="true"
        log_debug "调试模式已启用"
    fi

    # 检查环境
    check_environment

    # 停止现有服务
    stop_services

    # 清理 Docker 资源
    cleanup_docker

    # 启动服务
    start_services

    # 执行数据库迁移
    run_migrations || {
        log_error "部署失败：数据库迁移出错"
        exit 1
    }

    # 收集静态文件
    collect_static

    # 更新 Cloudflare IP
    update_cloudflare_ips

    # 加固 Nginx 安全配置
    harden_nginx_security

    # 创建超级用户（可选）
    create_superuser

    # 健康检查
    health_check

    echo -e "\n${GREEN}🎉 1G内存优化部署完成！${NC}"
    echo -e "${CYAN}════════════════════════════════${NC}"
    echo -e "${BLUE}📊 查看实时日志:${NC} $DOCKER_COMPOSE_CMD logs -f"
    echo -e "${BLUE}🛑 停止服务:${NC} $DOCKER_COMPOSE_CMD down"
    echo -e "${BLUE}🔧 进入 Web 容器:${NC} $DOCKER_COMPOSE_CMD exec web sh"
    echo -e "${BLUE}🔄 重启服务:${NC} $DOCKER_COMPOSE_CMD restart"
    echo -e "${BLUE}📈 监控资源:${NC} ./deploy.sh monitor"
    echo -e "${CYAN}════════════════════════════════${NC}"
}

# 显示使用说明
show_usage() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}    Django 部署脚本使用说明     ${NC}"
    echo -e "${CYAN}================================${NC}"
    echo ""
    echo -e "${GREEN}使用方法:${NC}"
    echo "  $0 [命令] [选项]"
    echo ""
    echo -e "${GREEN}命令:${NC}"
    echo "  deploy          完整部署（默认）"
    echo "  update          更新 Cloudflare IP 列表"
    echo "  security        加固 Nginx 安全配置"
    echo "  backup          备份数据库"
    echo "  cleanup         清理 Docker 资源"
    echo "  logs            查看服务日志"
    echo "  status          查看服务状态"
    echo "  restart         重启服务"
    echo "  stop            停止服务"
    echo "  help            显示此帮助信息"
    echo ""
    echo -e "${GREEN}选项:${NC}"
    echo "  --debug         启用调试模式"
    echo "  --force         强制操作（不确认）"
    echo "  --create-admin  创建超级用户"
    echo ""
    echo -e "${GREEN}示例:${NC}"
    echo "  $0                    # 完整部署"
    echo "  $0 deploy --debug     # 调试模式部署"
    echo "  $0 update             # 更新 Cloudflare IP"
    echo "  $0 logs -f            # 查看实时日志"
}

# 解析命令行参数
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --debug)
                DEBUG="true"
                shift
                ;;
            --force)
                FORCE="true"
                shift
                ;;
            --create-admin)
                CREATE_SUPERUSER="true"
                shift
                ;;
            *)
                COMMAND="$1"
                shift
                ;;
        esac
    done
}

# 主执行逻辑
main() {
    # 解析参数
    parse_arguments "$@"

    # 检查 Docker Compose 命令
    check_docker_compose

    # 根据命令执行相应操作
    case "${COMMAND}" in
        "update")
            update_cloudflare_ips
            ;;
        "security")
            harden_nginx_security
            ;;
        "cleanup")
            cleanup_docker
            ;;
        "monitor")
            health_check
            ;;
        "logs")
            shift
            $DOCKER_COMPOSE_CMD logs "$@"
            ;;
        "status")
            $DOCKER_COMPOSE_CMD ps
            ;;
        "restart")
            log_info "重启服务..."
            $DOCKER_COMPOSE_CMD restart
            health_check
            ;;
        "stop")
            log_info "停止服务..."
            $DOCKER_COMPOSE_CMD down
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        "deploy"|"")
            main_deploy "$@"
            ;;
        *)
            log_error "未知命令: $COMMAND"
            show_usage
            exit 1
            ;;
    esac
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi