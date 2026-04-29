#!/bin/bash

# Docker工具箱脚本
# 集成了监控和清理功能

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示使用说明
show_usage() {
    echo "Docker工具箱脚本"
    echo ""
    echo "监控功能:"
    echo "  ./docker_tools.sh stats         - 显示所有容器的状态和资源使用情况"
    echo "  ./docker_tools.sh live          - 实时监控容器资源使用情况"
    echo "  ./docker_tools.sh top           - 显示容器进程信息"
    echo "  ./docker_tools.sh ps            - 显示运行中的容器"
    echo "  ./docker_tools.sh ps-all        - 显示所有容器（包括停止的）"
    echo "  ./docker_tools.sh logs [name]   - 查看指定容器日志"
    echo "  ./docker_tools.sh inspect       - 显示容器详细信息"
    echo ""
    echo "清理功能:"
    echo "  ./docker_tools.sh clean-images      - 清理无用镜像"
    echo "  ./docker_tools.sh clean-cache       - 清理构建缓存"
    echo "  ./docker_tools.sh clean-containers  - 清理已停止的容器"
    echo "  ./docker_tools.sh clean-all         - 清理所有（镜像+缓存+容器）"
    echo "  ./docker_tools.sh prune             - 执行全面清理（危险操作）"
    echo ""
}

# 检查Docker是否运行
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装或未在PATH中"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker守护进程未运行"
        exit 1
    fi
}

# ========================
# 监控功能部分
# ========================

# 显示所有容器状态和资源使用情况
show_container_stats() {
    log_info "正在获取容器资源使用情况..."
    echo ""
    
    # 显示容器列表
    log_info "容器列表:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    
    # 显示资源使用情况（单次）
    log_info "资源使用情况快照:"
    docker stats --no-stream --format "table {{.Container}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}"
}

# 实时监控资源使用情况
live_stats() {
    log_info "实时监控容器资源使用情况 (按Ctrl+C退出)"
    echo ""
    docker stats --format "table {{.Container}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}"
}

# 显示容器进程信息
show_top() {
    log_info "容器进程信息:"
    echo ""
    
    # 获取所有运行中的容器
    containers=$(docker ps -q)
    
    if [ -z "$containers" ]; then
        log_warning "没有运行中的容器"
        return
    fi
    
    for container in $containers; do
        name=$(docker inspect --format='{{.Name}}' $container | sed 's/\///')
        log_info "容器: $name ($container)"
        docker top $container
        echo ""
    done
}

# 显示运行中的容器
show_running_containers() {
    log_info "运行中的容器:"
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.CreatedAt}}"
}

# 显示所有容器
show_all_containers() {
    log_info "所有容器 (包括已停止的):"
    docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.CreatedAt}}"
}

# 查看容器日志
show_logs() {
    container_name=$1
    
    if [ -z "$container_name" ]; then
        # 如果没有指定容器名，显示所有容器的日志选项
        log_info "请选择要查看日志的容器:"
        docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
        echo ""
        read -p "请输入容器名称: " container_name
        
        if [ -z "$container_name" ]; then
            log_error "未指定容器名称"
            return 1
        fi
    fi
    
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${container_name}$"; then
        log_error "容器 '$container_name' 不存在"
        return 1
    fi
    
    log_info "显示容器 '$container_name' 的日志 (最近50行):"
    docker logs --tail 50 $container_name
}

# 显示容器详细信息
show_inspect() {
    log_info "容器详细信息:"
    echo ""
    
    containers=$(docker ps -q)
    
    if [ -z "$containers" ]; then
        log_warning "没有运行中的容器"
        return
    fi
    
    for container in $containers; do
        name=$(docker inspect --format='{{.Name}}' $container | sed 's/\///')
        log_info "容器详细信息: $name ($container)"
        docker inspect $container
        echo ""
    done
}

# ========================
# 清理功能部分
# ========================

# 清理无用镜像
cleanup_images() {
    log_info "正在清理无用镜像..."
    
    # 删除悬空镜像（dangling images）
    dangling_count=$(docker images -f "dangling=true" -q | wc -l | tr -d ' ')
    if [ "$dangling_count" -gt 0 ]; then
        log_info "发现 $dangling_count 个悬空镜像，正在删除..."
        docker rmi $(docker images -f "dangling=true" -q) 2>/dev/null || true
        log_success "悬空镜像清理完成"
    else
        log_info "未发现悬空镜像"
    fi
}

# 清理构建缓存
cleanup_build_cache() {
    log_info "正在清理构建缓存..."
    
    # 清理构建缓存
    docker builder prune -f
    log_success "构建缓存清理完成"
}

# 清理所有停止的容器
cleanup_containers() {
    log_info "正在清理已停止的容器..."
    
    # 删除所有已停止的容器
    stopped_containers=$(docker ps -aq -f status=exited)
    if [ -n "$stopped_containers" ]; then
        count=$(echo "$stopped_containers" | wc -l | tr -d ' ')
        log_info "发现 $count 个已停止的容器，正在删除..."
        docker rm $stopped_containers 2>/dev/null || true
        log_success "已停止的容器清理完成"
    else
        log_info "未发现已停止的容器"
    fi
}

# 清理所有内容
cleanup_all() {
    log_info "正在执行完整清理..."
    cleanup_images
    cleanup_build_cache
    cleanup_containers
    log_success "完整清理完成"
}

# 全面系统清理（谨慎使用）
full_prune() {
    log_warning "即将执行全面系统清理，这将删除："
    log_warning "  - 所有已停止的容器"
    log_warning "  - 所有未使用的网络"
    log_warning "  - 所有未使用的镜像"
    log_warning "  - 所有未使用的构建缓存"
    echo ""
    read -p "确认执行？(输入 'YES' 确认): " confirm
    
    if [ "$confirm" != "YES" ]; then
        log_info "取消全面清理操作"
        return
    fi
    
    log_info "开始全面系统清理..."
    docker system prune -a -f
    log_success "全面系统清理完成"
}

# 显示磁盘使用情况
show_disk_usage() {
    log_info "当前Docker磁盘使用情况:"
    docker system df -v
}

# 主函数
main() {
    check_docker
    
    case "$1" in
        # 监控功能
        "stats")
            show_container_stats
            ;;
        "live"|"live-stats")
            live_stats
            ;;
        "top")
            show_top
            ;;
        "ps")
            show_running_containers
            ;;
        "ps-all")
            show_all_containers
            ;;
        "logs")
            show_logs "$2"
            ;;
        "inspect")
            show_inspect
            ;;
        # 清理功能
        "clean-images")
            cleanup_images
            show_disk_usage
            ;;
        "clean-cache")
            cleanup_build_cache
            show_disk_usage
            ;;
        "clean-containers")
            cleanup_containers
            show_disk_usage
            ;;
        "clean-all")
            cleanup_all
            show_disk_usage
            ;;
        "prune")
            full_prune
            show_disk_usage
            ;;
        # 帮助
        "help"|"-h"|"--help")
            show_usage
            ;;
        "")
            show_container_stats
            ;;
        *)
            log_error "未知参数: $1"
            show_usage
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"