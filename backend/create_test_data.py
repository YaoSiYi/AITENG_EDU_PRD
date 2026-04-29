#!/usr/bin/env python
"""
创建测试数据脚本
为就业统计记录创建对应的用户，并关联数据
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.stats.models import EmploymentStats
from apps.users.models import User


def create_test_users_and_sync():
    """创建测试用户并同步数据"""
    print('开始创建测试用户并同步数据...')
    print('=' * 60)

    # 就业统计记录与用户信息的映射
    employment_user_mapping = [
        {'name': '李娜', 'username': 'linai', 'period': '2024-01-01期学员', 'gender': 'female'},
        {'name': '张伟', 'username': 'zhangwei', 'period': '2024-02-01期学员', 'gender': 'male'},
        {'name': '王强', 'username': 'wangqiang', 'period': '2024-03-01期学员', 'gender': 'male'},
        {'name': '刘芳', 'username': 'liufang', 'period': '2024-04-01期学员', 'gender': 'female'},
        {'name': '赵丽', 'username': 'zhaoli', 'period': '2024-05-01期学员', 'gender': 'female'},
        {'name': '孙杰', 'username': 'sunjie', 'period': '2024-06-01期学员', 'gender': 'male'},
        {'name': '陈明', 'username': 'chenming', 'period': '2024-07-01期学员', 'gender': 'male'},
        {'name': '周敏', 'username': 'zhoumin', 'period': '2024-08-01期学员', 'gender': 'female'},
        {'name': '刘宇航', 'username': 'liuyuhang', 'period': '2024-09-01期学员', 'gender': 'male'},
        {'name': '王大锤', 'username': 'wangdachui', 'period': '2024-10-01期学员', 'gender': 'male'},
    ]

    created_count = 0
    updated_count = 0

    for mapping in employment_user_mapping:
        print(f"\n处理: {mapping['name']}")

        # 查找就业统计记录
        emp_records = EmploymentStats.objects.filter(student_name=mapping['name'])
        if not emp_records.exists():
            print(f"  ⚠ 未找到就业统计记录")
            continue

        emp = emp_records.first()

        # 检查用户是否已存在
        user = User.objects.filter(username=mapping['username']).first()

        if not user:
            # 创建新用户
            user = User.objects.create(
                username=mapping['username'],
                nickname=mapping['name'],
                period=mapping['period'],
                gender=mapping['gender'],
                role='student',
                plain_password='password123',
                is_active=True
            )
            user.set_password('password123')
            user.save()
            print(f"  ✓ 创建用户: {user.username}")
            created_count += 1
        else:
            # 更新现有用户
            user.nickname = mapping['name']
            user.period = mapping['period']
            user.gender = mapping['gender']
            user.save()
            print(f"  ✓ 更新用户: {user.username}")

        # 关联就业统计记录
        emp.student = user
        emp.save()  # save() 方法会自动同步期数和性别
        print(f"  ✓ 关联就业统计记录")
        print(f"  ✓ 同步期数: {emp.period}")
        print(f"  ✓ 同步性别: {emp.get_gender_display()}")
        updated_count += 1

    print('\n' + '=' * 60)
    print(f'同步完成！')
    print(f'  创建用户: {created_count} 个')
    print(f'  更新记录: {updated_count} 条')


if __name__ == '__main__':
    create_test_users_and_sync()
