#!/bin/bash

# Django 开发环境设置和运行脚本

echo "Django 开发环境设置和运行脚本..."

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "警告: 未检测到虚拟环境。"
    echo "建议先创建并激活虚拟环境:"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate  # Linux/Mac"
    echo "  .venv\Scripts\activate     # Windows"
    echo ""
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 升级 pip
echo "升级 pip..."。/
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 检查是否存在开发环境配置文件
if [ ! -f ".env.dev" ]; then
    echo "创建开发环境配置文件..."
    cat > .env.dev << 'EOF'
# Django 设置
DEBUG=1
SECRET_KEY=your-local-development-secret-key

# 使用本地 SQLite 数据库（开发环境）
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# 安全设置
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1,http://0.0.0.0

# 服务器信息
SERVER_IP=127.0.0.1
EOF
fi

# 检查参数
if [ "$1" = "--external" ]; then
    BIND_ADDRESS="0.0.0.0:8000"
    echo "外部访问模式: 绑定到 $BIND_ADDRESS"
else
    BIND_ADDRESS="127.0.0.1:8000"
    echo "本地模式: 绑定到 $BIND_ADDRESS"
fi

# 加载环境变量
echo "加载开发环境变量..."
set -a
[ -f .env.dev ] && . .env.dev
set +a

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 创建超级用户
echo "创建/更新超级用户..."
python manage.py init_admin

# 运行开发服务器
echo ""
echo "启动开发服务器..."
echo "访问地址: http://$BIND_ADDRESS/"
echo "管理后台: http://$BIND_ADDRESS/admin/"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python manage.py runserver $BIND_ADDRESS