#!/bin/bash

# 艾腾教育项目一键停止脚本
# 作者：Claude Sonnet 4.6
# 日期：2026-04-29

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 项目根目录
PROJECT_ROOT="/Users/yao/Node_Project/Aiteng_Edu_Prd"
LOG_DIR="$PROJECT_ROOT/logs"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印标题
print_header() {
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  艾腾教育项目停止脚本${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
}

# 停止服务
stop_service() {
    local service_name=$1
    local pid_file="$LOG_DIR/$2.pid"

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            print_info "正在停止 $service_name (PID: $pid)..."
            kill $pid 2>/dev/null || true
            sleep 2

            # 如果进程还在运行，强制停止
            if ps -p $pid > /dev/null 2>&1; then
                print_warning "进程未响应，强制停止..."
                kill -9 $pid 2>/dev/null || true
            fi

            print_success "$service_name 已停止"
        else
            print_warning "$service_name 进程不存在 (PID: $pid)"
        fi
        rm -f "$pid_file"
    else
        print_warning "$service_name PID文件不存在"
    fi
}

# 停止端口上的所有进程
stop_port() {
    local port=$1
    local service_name=$2

    local pids=$(lsof -nP -iTCP:$port -sTCP:LISTEN 2>/dev/null | grep LISTEN | awk '{print $2}' | sort -u)

    if [ -n "$pids" ]; then
        print_info "停止 $service_name (端口 $port)..."
        for pid in $pids; do
            kill $pid 2>/dev/null || true
        done
        sleep 2
        print_success "$service_name 已停止"
    fi
}

# 主函数
main() {
    print_header

    print_info "开始停止所有服务..."
    echo ""

    # 停止Django后端
    stop_service "Django后端" "backend"
    stop_port 8000 "Django后端"

    # 停止Web管理后台
    stop_service "Web管理后台" "web"
    stop_port 3000 "Web管理后台"

    # 停止Uni-app H5
    stop_service "Uni-app H5" "uniapp"
    stop_port 3001 "Uni-app H5"

    echo ""
    print_success "所有服务已停止"
    echo ""

    # 询问是否停止MySQL和Redis
    read -p "是否停止MySQL和Redis？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "停止MySQL..."
        brew services stop mysql 2>/dev/null || true

        print_info "停止Redis..."
        brew services stop redis 2>/dev/null || true

        print_success "MySQL和Redis已停止"
    fi

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  所有服务已停止${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "🚀 重新启动: ./start.sh"
    echo ""
}

# 运行主函数
main
