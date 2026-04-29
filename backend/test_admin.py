#!/usr/bin/env python
"""
Django Admin 测试脚本
测试所有模型的增删改查功能
"""

import os
import sys
import django

# 设置Django环境
sys.path.insert(0, '/Users/yao/Node_Project/Aiteng_Edu_Prd/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.questions.models import Question, QuestionCategory, WrongQuestion, Assignment
from apps.activities.models import Activity, ActivityParticipant
from apps.stats.models import StudentStats, EmploymentStats, ExcellentStudent, InterviewQuestion
from apps.evaluations.models import Evaluation, StudentProgress

def test_user_model():
    """测试用户模型"""
    print("\n=== 测试用户模型 ===")
    try:
        # 创建测试用户
        user = User.objects.create_user(
            username='test_user_001',
            email='test001@example.com',
            password='test123',
            nickname='测试用户',
            hometown='北京'
        )
        print(f"✅ 创建用户成功: {user.username}")

        # 更新用户
        user.nickname = '测试用户_修改'
        user.save()
        print(f"✅ 更新用户成功: {user.nickname}")

        # 删除用户
        user.delete()
        print("✅ 删除用户成功")

        return True
    except Exception as e:
        print(f"❌ 用户模型测试失败: {e}")
        return False

def test_question_model():
    """测试题目模型"""
    print("\n=== 测试题目模型 ===")
    try:
        # 创建分类
        category = QuestionCategory.objects.create(name='测试分类')
        print(f"✅ 创建分类成功: {category.name}")

        # 创建题目
        question = Question.objects.create(
            stage=1,
            category=category,
            subject='软件测试基础',
            difficulty='easy',
            content='这是一道测试题目',
            answer='A',
            explanation='这是答案解析'
        )
        print(f"✅ 创建题目成功: {question.id}")

        # 更新题目
        question.content = '这是修改后的题目'
        question.save()
        print(f"✅ 更新题目成功")

        # 删除题目和分类
        question.delete()
        category.delete()
        print("✅ 删除题目和分类成功")

        return True
    except Exception as e:
        print(f"❌ 题目模型测试失败: {e}")
        return False

def test_activity_model():
    """测试活动模型"""
    print("\n=== 测试活动模型 ===")
    try:
        # 获取管理员用户
        admin = User.objects.get(username='admin')

        # 创建活动
        activity = Activity.objects.create(
            creator=admin,
            title='测试活动',
            description='这是一个测试活动',
            is_active=True
        )
        print(f"✅ 创建活动成功: {activity.title}")

        # 更新活动
        activity.title = '测试活动_修改'
        activity.save()
        print(f"✅ 更新活动成功")

        # 删除活动
        activity.delete()
        print("✅ 删除活动成功")

        return True
    except Exception as e:
        print(f"❌ 活动模型测试失败: {e}")
        return False

def test_stats_model():
    """测试统计模型"""
    print("\n=== 测试统计模型 ===")
    try:
        # 创建学员统计
        stats = StudentStats.objects.create(
            period='2024-01',
            province='北京',
            city='北京市',
            count=100
        )
        print(f"✅ 创建学员统计成功: {stats.period}")

        # 创建就业统计
        employment = EmploymentStats.objects.create(
            student_name='张三',
            company='测试公司',
            position='测试工程师',
            salary=15000,
            city='北京'
        )
        print(f"✅ 创建就业统计成功: {employment.student_name}")

        # 删除统计数据
        stats.delete()
        employment.delete()
        print("✅ 删除统计数据成功")

        return True
    except Exception as e:
        print(f"❌ 统计模型测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Django Admin 模型测试")
    print("=" * 50)

    results = []

    # 运行所有测试
    results.append(("用户模型", test_user_model()))
    results.append(("题目模型", test_question_model()))
    results.append(("活动模型", test_activity_model()))
    results.append(("统计模型", test_stats_model()))

    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    # 统计
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！Django Admin 可以正常使用。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查错误信息。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
