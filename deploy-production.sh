#!/bin/bash

# 艾腾教育 - 生产环境部署脚本
# 域名: www.aitengjiaoyu.top
# 版本: v0.2.1

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  艾腾教育 - 生产环境部署脚本"
echo "  域名: www.aitengjiaoyu.top"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [ ! -f "DEPLOYMENT_GUIDE.md" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env.production" ]; then
    echo -e "${RED}错误: 未找到 .env.production 文件${NC}"
    echo "请先创建 .env.production 文件并配置生产环境变量"
    exit 1
fi

echo -e "${YELLOW}步骤 1/7: 检查依赖...${NC}"
# 检查必要的命令
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}错误: 未安装 python3${NC}"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo -e "${RED}错误: 未安装 npm${NC}"; exit 1; }
command -v mysql >/dev/null 2>&1 || { echo -e "${RED}错误: 未安装 mysql${NC}"; exit 1; }
echo -e "${GREEN}✓ 依赖检查通过${NC}"
echo ""

echo -e "${YELLOW}步骤 2/7: 安装后端依赖...${NC}"
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
echo -e "${GREEN}✓ 后端依赖安装完成${NC}"
cd ..
echo ""

echo -e "${YELLOW}步骤 3/7: 数据库迁移...${NC}"
cd backend
source venv/bin/activate
cp ../.env.production ../.env
python manage.py migrate
echo -e "${GREEN}✓ 数据库迁移完成${NC}"
cd ..
echo ""

echo -e "${YELLOW}步骤 4/7: 收集静态文件...${NC}"
cd backend
source venv/bin/activate
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ 静态文件收集完成${NC}"
cd ..
echo ""

echo -e "${YELLOW}步骤 5/7: 构建前端Web...${NC}"
cd frontend-web
if [ ! -d "node_modules" ]; then
    npm install
fi
npm run build
echo -e "${GREEN}✓ 前端Web构建完成${NC}"
cd ..
echo ""

echo -e "${YELLOW}步骤 6/7: 构建Uni-app H5...${NC}"
cd frontend-uniapp
if [ ! -d "node_modules" ]; then
    npm install
fi
npm run build:h5
echo -e "${GREEN}✓ Uni-app H5构建完成${NC}"
cd ..
echo ""

echo -e "${YELLOW}步骤 7/7: 生成部署包...${NC}"
DEPLOY_DIR="deploy_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEPLOY_DIR"

# 复制必要文件
cp -r backend "$DEPLOY_DIR/"
cp -r frontend-web/dist "$DEPLOY_DIR/frontend-web"
cp -r frontend-uniapp/dist/build/h5 "$DEPLOY_DIR/frontend-uniapp"
cp .env.production "$DEPLOY_DIR/.env"
cp nginx/nginx.production.conf "$DEPLOY_DIR/nginx.conf"
cp DEPLOYMENT_GUIDE.md "$DEPLOY_DIR/"

# 创建README
cat > "$DEPLOY_DIR/README.txt" << 'EOF'
艾腾教育 - 生产环境部署包

部署步骤：
1. 上传此目录到服务器 /var/www/aiteng/
2. 配置 .env 文件中的密钥和密码
3. 按照 DEPLOYMENT_GUIDE.md 完成部署

目录说明：
- backend/          后端代码
- frontend-web/     前端Web构建产物
- frontend-uniapp/  Uni-app H5构建产物
- nginx.conf        Nginx配置文件
- .env              环境变量配置
EOF

echo -e "${GREEN}✓ 部署包已生成: $DEPLOY_DIR${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}部署准备完成！${NC}"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 上传 $DEPLOY_DIR 目录到服务器"
echo "2. 修改 .env 文件中的密钥和密码"
echo "3. 按照 DEPLOYMENT_GUIDE.md 完成部署"
echo ""
echo "部署文档: DEPLOYMENT_GUIDE.md"
echo ""
