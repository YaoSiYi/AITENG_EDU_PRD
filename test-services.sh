#!/bin/bash

# 教务管理系统 - 快速测试脚本

echo "================================"
echo "教务管理系统 - 服务状态检查"
echo "================================"
echo ""

# 检查 Docker 服务状态
echo "📦 Docker 服务状态:"
docker compose ps
echo ""

# 检查数据库连接
echo "🗄️  数据库连接测试:"
docker compose exec -T db mysql -uroot -peducation123 -e "SELECT 'Database OK' as status;" 2>/dev/null && echo "✅ MySQL 连接成功" || echo "❌ MySQL 连接失败"
echo ""

# 检查 Redis 连接
echo "🔴 Redis 连接测试:"
docker compose exec -T redis redis-cli ping 2>/dev/null && echo "✅ Redis 连接成功" || echo "❌ Redis 连接失败"
echo ""

# 检查后端 API
echo "🚀 后端 API 测试:"
curl -s http://localhost:8000/api/docs/ > /dev/null && echo "✅ API 文档可访问" || echo "❌ API 文档不可访问"
echo ""

# 显示访问地址
echo "================================"
echo "📍 访问地址:"
echo "================================"
echo "后端 API: http://localhost:8000/api/"
echo "Django Admin: http://localhost:8000/admin/"
echo "API 文档: http://localhost:8000/api/docs/"
echo ""
echo "数据库: localhost:3307"
echo "Redis: localhost:6379"
echo ""
