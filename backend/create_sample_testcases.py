#!/usr/bin/env python
"""
创建测试用例示例数据
"""
import os
import sys
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.testcases.models import TestCase
from apps.users.models import User

# 获取或创建一个管理员用户作为创建者
admin_user = User.objects.filter(role='admin').first()
if not admin_user:
    admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    print("警告: 未找到管理员用户，将使用第一个用户")
    admin_user = User.objects.first()

if not admin_user:
    print("错误: 数据库中没有用户，请先创建用户")
    sys.exit(1)

print(f"使用用户: {admin_user.username} (ID: {admin_user.id})")

# 测试用例数据
test_cases = [
    # 教务管理系统 - 题库管理
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': '题目列表',
        'test_point': '分页功能',
        'title': '验证题目列表分页显示',
        'description': '测试题目列表的分页功能是否正常工作',
        'precondition': '1. 系统中已有超过20条题目\n2. 用户已登录系统',
        'steps': '1. 登录系统\n2. 进入题库管理模块\n3. 查看题目列表\n4. 点击下一页按钮\n5. 修改每页显示条数',
        'expected_result': '1. 默认每页显示20条题目\n2. 可以正常翻页\n3. 页码显示正确\n4. 修改每页条数后正常刷新',
        'priority': 'high',
        'status': 'active',
        'is_smoke': True,
        'case_type': '功能',
    },
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': '题目编辑',
        'test_point': '题目内容修改',
        'title': '编辑题目内容并保存',
        'description': '测试编辑题目内容的功能',
        'precondition': '1. 系统中已有题目\n2. 用户具有编辑权限',
        'steps': '1. 进入题目列表\n2. 点击某个题目的编辑按钮\n3. 修改题目标题\n4. 修改题目内容\n5. 点击保存按钮',
        'expected_result': '1. 编辑页面正常打开\n2. 可以修改题目信息\n3. 保存成功并提示\n4. 返回列表后显示修改后的内容',
        'priority': 'high',
        'status': 'active',
        'is_smoke': False,
        'case_type': '功能',
    },
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': '题目搜索',
        'test_point': '关键字搜索',
        'title': '使用关键字搜索题目',
        'description': '测试题目搜索功能的准确性',
        'precondition': '系统中已有多个题目',
        'steps': '1. 进入题目列表\n2. 在搜索框输入关键字\n3. 点击搜索按钮',
        'expected_result': '1. 显示包含关键字的题目\n2. 搜索结果准确\n3. 支持模糊搜索',
        'priority': 'medium',
        'status': 'active',
        'is_smoke': False,
        'case_type': '功能',
    },

    # 教务管理系统 - 用户管理
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': '用户注册',
        'test_point': '注册表单验证',
        'title': '验证用户注册表单的字段校验',
        'description': '测试注册表单的各项字段验证规则',
        'precondition': '访问注册页面',
        'steps': '1. 打开注册页面\n2. 输入无效的邮箱格式\n3. 输入过短的密码\n4. 输入不匹配的确认密码\n5. 提交表单',
        'expected_result': '1. 邮箱格式错误时显示提示\n2. 密码长度不足时显示提示\n3. 确认密码不匹配时显示提示\n4. 表单验证失败，不允许提交',
        'priority': 'critical',
        'status': 'active',
        'is_smoke': True,
        'case_type': '功能',
    },
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': '用户登录',
        'test_point': '登录功能',
        'title': '使用正确的用户名和密码登录',
        'description': '测试正常登录流程',
        'precondition': '1. 用户已注册\n2. 用户未登录',
        'steps': '1. 打开登录页面\n2. 输入正确的用户名\n3. 输入正确的密码\n4. 点击登录按钮',
        'expected_result': '1. 登录成功\n2. 跳转到首页\n3. 显示用户信息\n4. Token正确保存',
        'priority': 'critical',
        'status': 'active',
        'is_smoke': True,
        'case_type': '功能',
    },
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': '用户登录',
        'test_point': '登录失败处理',
        'title': '使用错误的密码登录',
        'description': '测试登录失败的错误提示',
        'precondition': '用户已注册',
        'steps': '1. 打开登录页面\n2. 输入正确的用户名\n3. 输入错误的密码\n4. 点击登录按钮',
        'expected_result': '1. 登录失败\n2. 显示错误提示信息\n3. 不跳转页面\n4. 密码输入框清空',
        'priority': 'high',
        'status': 'active',
        'is_smoke': True,
        'case_type': '功能',
    },

    # 教务管理系统 - 活动管理
    {
        'product': '教务管理系统',
        'module': '活动管理',
        'sub_module': '活动列表',
        'test_point': '活动展示',
        'title': '查看活动列表',
        'description': '测试活动列表的展示功能',
        'precondition': '系统中已有活动数据',
        'steps': '1. 登录系统\n2. 进入活动管理\n3. 查看活动列表',
        'expected_result': '1. 显示所有活动\n2. 活动信息完整\n3. 支持分页',
        'priority': 'medium',
        'status': 'active',
        'is_smoke': False,
        'case_type': '功能',
    },
    {
        'product': '教务管理系统',
        'module': '活动管理',
        'sub_module': '活动报名',
        'test_point': '报名功能',
        'title': '用户报名参加活动',
        'description': '测试活动报名流程',
        'precondition': '1. 用户已登录\n2. 活动正在报名中',
        'steps': '1. 进入活动详情页\n2. 点击报名按钮\n3. 确认报名信息\n4. 提交报名',
        'expected_result': '1. 报名成功\n2. 显示成功提示\n3. 报名状态更新\n4. 可以在个人中心查看',
        'priority': 'high',
        'status': 'active',
        'is_smoke': False,
        'case_type': '功能',
    },

    # 教务管理系统 - 错题本
    {
        'product': '教务管理系统',
        'module': '错题本',
        'sub_module': '错题收集',
        'test_point': '自动收集错题',
        'title': '答错题目后自动加入错题本',
        'description': '测试错题自动收集功能',
        'precondition': '用户已登录并开始答题',
        'steps': '1. 进入题库答题\n2. 选择错误答案\n3. 提交答案\n4. 进入错题本查看',
        'expected_result': '1. 答错的题目自动加入错题本\n2. 记录答题时间\n3. 记录错误答案\n4. 可以在错题本中查看',
        'priority': 'high',
        'status': 'active',
        'is_smoke': False,
        'case_type': '功能',
    },
    {
        'product': '教务管理系统',
        'module': '错题本',
        'sub_module': '错题练习',
        'test_point': '重做错题',
        'title': '在错题本中重新练习错题',
        'description': '测试错题重做功能',
        'precondition': '错题本中已有错题',
        'steps': '1. 进入错题本\n2. 选择一道错题\n3. 重新答题\n4. 提交答案',
        'expected_result': '1. 可以重新答题\n2. 答对后从错题本移除\n3. 记录练习次数\n4. 更新答题统计',
        'priority': 'medium',
        'status': 'active',
        'is_smoke': False,
        'case_type': '功能',
    },

    # 接口测试用例
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': 'API接口',
        'test_point': '题目列表接口',
        'title': '测试GET /api/questions/接口',
        'description': '测试题目列表查询接口的功能和性能',
        'precondition': '1. 后端服务正常运行\n2. 数据库中有测试数据',
        'steps': '1. 发送GET请求到/api/questions/\n2. 添加分页参数page=1&limit=20\n3. 添加筛选参数difficulty=easy\n4. 检查响应状态码\n5. 验证响应数据格式',
        'expected_result': '1. 返回状态码200\n2. 返回JSON格式数据\n3. 包含results和count字段\n4. 分页参数生效\n5. 筛选参数生效',
        'priority': 'high',
        'status': 'active',
        'is_smoke': True,
        'case_type': '接口',
    },
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': 'API接口',
        'test_point': '用户登录接口',
        'title': '测试POST /api/users/login/接口',
        'description': '测试用户登录接口',
        'precondition': '用户已注册',
        'steps': '1. 发送POST请求到/api/users/login/\n2. 请求体包含username和password\n3. 检查响应状态码\n4. 验证返回的token',
        'expected_result': '1. 返回状态码200\n2. 返回access和refresh token\n3. token格式正确\n4. 可以使用token访问受保护接口',
        'priority': 'critical',
        'status': 'active',
        'is_smoke': True,
        'case_type': '接口',
    },
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': 'API接口',
        'test_point': '接口性能',
        'title': '题目列表接口响应时间测试',
        'description': '测试接口在不同数据量下的响应时间',
        'precondition': '数据库中有大量测试数据',
        'steps': '1. 使用JMeter或Postman\n2. 发送100次并发请求\n3. 记录响应时间\n4. 分析性能指标',
        'expected_result': '1. 平均响应时间<500ms\n2. 95%请求<1s\n3. 无超时错误\n4. 服务器负载正常',
        'priority': 'medium',
        'status': 'active',
        'is_smoke': False,
        'case_type': '性能',
    },

    # 安全测试用例
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': '安全测试',
        'test_point': 'SQL注入防护',
        'title': '测试登录接口的SQL注入防护',
        'description': '验证系统是否能防御SQL注入攻击',
        'precondition': '系统正常运行',
        'steps': '1. 在用户名输入框输入SQL注入语句\n2. 例如: admin\' OR \'1\'=\'1\n3. 提交登录请求\n4. 观察系统响应',
        'expected_result': '1. 登录失败\n2. 不返回敏感信息\n3. 记录安全日志\n4. SQL注入被成功拦截',
        'priority': 'critical',
        'status': 'active',
        'is_smoke': False,
        'case_type': '安全',
    },
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': '安全测试',
        'test_point': 'XSS防护',
        'title': '测试题目内容的XSS防护',
        'description': '验证系统是否能防御XSS攻击',
        'precondition': '用户具有创建题目权限',
        'steps': '1. 创建新题目\n2. 在题目内容中输入<script>alert("XSS")</script>\n3. 保存题目\n4. 查看题目详情',
        'expected_result': '1. 脚本被转义或过滤\n2. 不执行JavaScript代码\n3. 显示为纯文本\n4. 其他用户查看时也安全',
        'priority': 'critical',
        'status': 'active',
        'is_smoke': False,
        'case_type': '安全',
    },
    {
        'product': '教务管理系统',
        'module': '用户管理',
        'sub_module': '安全测试',
        'test_point': '权限验证',
        'title': '测试未授权访问的拦截',
        'description': '验证系统的权限控制机制',
        'precondition': '1. 有普通用户账号\n2. 有管理员功能',
        'steps': '1. 使用普通用户登录\n2. 尝试访问管理员页面\n3. 尝试调用管理员API\n4. 观察系统响应',
        'expected_result': '1. 访问被拒绝\n2. 返回403或401状态码\n3. 显示权限不足提示\n4. 不泄露敏感信息',
        'priority': 'critical',
        'status': 'active',
        'is_smoke': True,
        'case_type': '安全',
    },

    # 兼容性测试
    {
        'product': '教务管理系统',
        'module': '前端界面',
        'sub_module': '浏览器兼容',
        'test_point': 'Chrome浏览器兼容性',
        'title': '在Chrome浏览器中测试系统功能',
        'description': '验证系统在Chrome浏览器中的兼容性',
        'precondition': '安装最新版Chrome浏览器',
        'steps': '1. 使用Chrome打开系统\n2. 测试登录功能\n3. 测试题库浏览\n4. 测试答题功能\n5. 测试各个模块',
        'expected_result': '1. 页面显示正常\n2. 功能运行正常\n3. 无JavaScript错误\n4. 样式显示正确',
        'priority': 'high',
        'status': 'active',
        'is_smoke': False,
        'case_type': '兼容性',
    },
    {
        'product': '教务管理系统',
        'module': '前端界面',
        'sub_module': '移动端适配',
        'test_point': '移动端响应式布局',
        'title': '测试移动端页面显示',
        'description': '验证系统在移动设备上的显示效果',
        'precondition': '使用移动设备或浏览器开发者工具',
        'steps': '1. 切换到移动端视图\n2. 测试导航菜单\n3. 测试题目列表\n4. 测试答题界面\n5. 测试各种屏幕尺寸',
        'expected_result': '1. 布局自适应\n2. 按钮大小合适\n3. 文字清晰可读\n4. 功能正常使用',
        'priority': 'medium',
        'status': 'active',
        'is_smoke': False,
        'case_type': '兼容性',
    },

    # 边界测试
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': '题目创建',
        'test_point': '字段长度限制',
        'title': '测试题目标题的最大长度限制',
        'description': '验证题目标题字段的长度限制',
        'precondition': '用户具有创建题目权限',
        'steps': '1. 创建新题目\n2. 输入超长标题（>200字符）\n3. 尝试保存\n4. 观察系统响应',
        'expected_result': '1. 显示长度限制提示\n2. 不允许保存\n3. 提示最大长度\n4. 用户体验友好',
        'priority': 'low',
        'status': 'active',
        'is_smoke': False,
        'case_type': '边界',
    },
    {
        'product': '教务管理系统',
        'module': '题库管理',
        'sub_module': '题目导入',
        'test_point': '批量导入限制',
        'title': '测试CSV导入的最大行数限制',
        'description': '验证批量导入功能的数量限制',
        'precondition': '准备超过5000行的CSV文件',
        'steps': '1. 进入题目导入页面\n2. 选择超大CSV文件\n3. 点击导入\n4. 观察系统响应',
        'expected_result': '1. 显示文件过大提示\n2. 提示最大行数限制\n3. 不执行导入\n4. 建议分批导入',
        'priority': 'medium',
        'status': 'active',
        'is_smoke': False,
        'case_type': '边界',
    },
]

print(f"\n准备创建 {len(test_cases)} 条测试用例...")

created_count = 0
for idx, case_data in enumerate(test_cases, 1):
    try:
        test_case = TestCase.objects.create(
            creator=admin_user,
            updater=admin_user,
            **case_data
        )
        created_count += 1
        print(f"[{idx}/{len(test_cases)}] ✓ 创建成功: {test_case.title}")
    except Exception as e:
        print(f"[{idx}/{len(test_cases)}] ✗ 创建失败: {case_data['title']} - {e}")

print(f"\n{'='*60}")
print(f"创建完成统计:")
print(f"{'='*60}")
print(f"  成功创建: {created_count} 条")
print(f"  创建失败: {len(test_cases) - created_count} 条")
print(f"{'='*60}")

# 显示统计信息
print(f"\n数据库中测试用例总数: {TestCase.objects.count()}")

print("\n按优先级分布:")
for priority_value, priority_label in TestCase.Priority.choices:
    count = TestCase.objects.filter(priority=priority_value).count()
    print(f"  {priority_label}: {count}条")

print("\n按状态分布:")
for status_value, status_label in TestCase.Status.choices:
    count = TestCase.objects.filter(status=status_value).count()
    print(f"  {status_label}: {count}条")

print("\n按产品分布:")
from django.db.models import Count
products = TestCase.objects.values('product').annotate(count=Count('id')).order_by('-count')
for p in products:
    print(f"  {p['product']}: {p['count']}条")

print("\n按用例类型分布:")
case_types = TestCase.objects.values('case_type').annotate(count=Count('id')).order_by('-count')
for ct in case_types:
    print(f"  {ct['case_type']}: {ct['count']}条")

print("\n✅ 示例数据创建完成！")
print("💡 提示: 现在可以访问 http://localhost:5173/testcases 查看测试用例")
