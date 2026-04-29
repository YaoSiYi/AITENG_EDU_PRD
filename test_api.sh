#!/bin/bash

echo "=== 测试 API 接口 ==="
echo ""

# 1. 测试登录
echo "1. 测试登录接口..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

echo "登录响应: $LOGIN_RESPONSE"
echo ""

# 提取 access token
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])" 2>/dev/null)

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ 登录失败，无法获取 token"
  exit 1
fi

echo "✅ 登录成功，获取到 token"
echo ""

# 2. 测试获取测试用例列表
echo "2. 测试获取测试用例列表..."
TESTCASES_RESPONSE=$(curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/testcases/)

echo "测试用例数量: $(echo $TESTCASES_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])" 2>/dev/null)"
echo ""

# 3. 检查第一条测试用例的字段
echo "3. 检查第一条测试用例的字段..."
FIRST_CASE=$(echo $TESTCASES_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data['results'][0], indent=2, ensure_ascii=False))" 2>/dev/null)

echo "$FIRST_CASE" | grep -E "(stage|title|status)" | head -5
echo ""

echo "=== 测试完成 ==="
