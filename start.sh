#!/bin/bash

# 艾腾教育项目一键启动脚本
# 作者：Claude Sonnet 4.6
# 日期：2026-04-29

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="/Users/yao/Node_Project/Aiteng_Edu_Prd"

# 日志文件目录
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

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
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  艾腾教育项目启动脚本${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查端口是否被占用
check_port() {
    local port=$1
    local service=$2
    if lsof -nP -iTCP:$port -sTCP:LISTEN &> /dev/null; then
        print_warning "$service 端口 $port 已被占用"
        read -p "是否停止占用该端口的进程？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            local pid=$(lsof -nP -iTCP:$port -sTCP:LISTEN | grep LISTEN | awk '{print $2}')
            kill $pid 2>/dev/null || true
            print_success "已停止进程 $pid"
            sleep 2
        else
            print_error "端口 $port 被占用，无法启动 $service"
            return 1
        fi
    fi
    return 0
}

# 检查MySQL是否运行
check_mysql() {
    print_info "检查MySQL服务..."
    if ! brew services list | grep mysql | grep started &> /dev/null; then
        print_warning "MySQL未运行，正在启动..."
        brew services start mysql
        sleep 3
        print_success "MySQL已启动"
    else
        print_success "MySQL正在运行"
    fi
}

# 检查Redis是否运行
check_redis() {
    print_info "检查Redis服务..."
    if ! brew services list | grep redis | grep started &> /dev/null; then
        print_warning "Redis未运行，正在启动..."
        brew services start redis
        sleep 2
        print_success "Redis已启动"
    else
        print_success "Redis正在运行"
    fi
}

# 启动Django后端
start_backend() {
    print_info "启动Django后端服务..."

    cd "$PROJECT_ROOT/backend"

    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        print_error "虚拟环境不存在，请先创建虚拟环境"
        exit 1
    fi

    # 检查端口
    if ! check_port 8000 "Django"; then
        return 1
    fi

    # 启动Django
    source venv/bin/activate
    nohup python manage.py runserver 0.0.0.0:8000 > "$LOG_DIR/backend.log" 2>&1 &
    echo $! > "$LOG_DIR/backend.pid"

    sleep 3

    # 验证启动
    if lsof -nP -iTCP:8000 -sTCP:LISTEN &> /dev/null; then
        print_success "Django后端已启动 (PID: $(cat $LOG_DIR/backend.pid))"
        print_info "访问地址: http://localhost:8000"
        print_info "管理后台: http://localhost:8000/admin"
        print_info "日志文件: $LOG_DIR/backend.log"
    else
        print_error "Django后端启动失败，请查看日志: $LOG_DIR/backend.log"
        return 1
    fi
}

# 启动Web管理后台
start_web() {
    print_info "启动Web管理后台..."

    cd "$PROJECT_ROOT/frontend-web"

    # 检查node_modules
    if [ ! -d "node_modules" ]; then
        print_warning "依赖未安装，正在安装..."
        npm install
    fi

    # 检查端口
    if ! check_port 3000 "Web管理后台"; then
        return 1
    fi

    # 启动Web
    nohup npm run dev > "$LOG_DIR/web.log" 2>&1 &
    echo $! > "$LOG_DIR/web.pid"

    sleep 5

    # 验证启动
    if lsof -nP -iTCP:3000 -sTCP:LISTEN &> /dev/null; then
        print_success "Web管理后台已启动 (PID: $(cat $LOG_DIR/web.pid))"
        print_info "访问地址: http://localhost:3000"
        print_info "手机访问: http://192.168.0.156:3000"
        print_info "日志文件: $LOG_DIR/web.log"
    else
        print_error "Web管理后台启动失败，请查看日志: $LOG_DIR/web.log"
        return 1
    fi
}

# 启动Uni-app H5
start_uniapp() {
    print_info "启动Uni-app H5应用..."

    cd "$PROJECT_ROOT/frontend-uniapp"

    # 检查node_modules
    if [ ! -d "node_modules" ]; then
        print_warning "依赖未安装，正在安装..."
        npm install
    fi

    # 检查端口
    if ! check_port 3001 "Uni-app H5"; then
        return 1
    fi

    # 启动Uni-app
    nohup npm run dev:h5 > "$LOG_DIR/uniapp.log" 2>&1 &
    echo $! > "$LOG_DIR/uniapp.pid"

    sleep 5

    # 验证启动
    if lsof -nP -iTCP:3001 -sTCP:LISTEN &> /dev/null; then
        print_success "Uni-app H5已启动 (PID: $(cat $LOG_DIR/uniapp.pid))"
        print_info "访问地址: http://localhost:3001"
        print_info "手机访问: http://192.168.0.156:3001"
        print_info "日志文件: $LOG_DIR/uniapp.log"
    else
        print_error "Uni-app H5启动失败，请查看日志: $LOG_DIR/uniapp.log"
        return 1
    fi
}

# 显示服务状态
show_status() {
    echo ""
    print_header
    echo -e "${GREEN}所有服务已启动成功！${NC}"
    echo ""
    echo "📊 服务状态："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Django
    if [ -f "$LOG_DIR/backend.pid" ]; then
        echo -e "✅ Django后端"
        echo "   PID: $(cat $LOG_DIR/backend.pid)"
        echo "   电脑访问: http://localhost:8000"
        echo "   手机访问: http://192.168.0.156:8000"
        echo "   管理后台: http://localhost:8000/admin"
        echo ""
    fi

    # Web
    if [ -f "$LOG_DIR/web.pid" ]; then
        echo -e "✅ Web管理后台"
        echo "   PID: $(cat $LOG_DIR/web.pid)"
        echo "   电脑访问: http://localhost:3000"
        echo "   手机访问: http://192.168.0.156:3000"
        echo ""
    fi

    # Uni-app
    if [ -f "$LOG_DIR/uniapp.pid" ]; then
        echo -e "✅ Uni-app H5"
        echo "   PID: $(cat $LOG_DIR/uniapp.pid)"
        echo "   电脑访问: http://localhost:3001"
        echo "   手机访问: http://192.168.0.156:3001"
        echo ""
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📝 日志文件位置: $LOG_DIR"
    echo "🛑 停止所有服务: ./stop.sh"
    echo ""
}

# 主函数
main() {
    print_header

    # 检查必要的命令
    print_info "检查系统环境..."
    check_command "node"
    check_command "npm"
    check_command "python3"
    check_command "mysql"
    check_command "redis-cli"
    check_command "brew"
    print_success "系统环境检查通过"

    # 检查基础服务
    check_mysql
    check_redis

    # 启动各个服务
    start_backend || exit 1
    start_web || exit 1
    start_uniapp || exit 1

    # 显示状态
    show_status
}

# 运行主函数
main
