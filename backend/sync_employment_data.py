#!/usr/bin/env python
"""
同步就业统计数据脚本
将就业统计中的学员信息与用户管理中的数据对齐
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.stats.models import EmploymentStats
from apps.users.models import User


def sync_employment_data():
    """同步就业统计数据"""
    print('开始同步就业统计数据...')
    print('=' * 60)

    updated_count = 0
    not_found_count = 0

    for emp in EmploymentStats.objects.all():
        print(f'\n处理记录 #{emp.id}: {emp.student_name}')

        # 如果已经关联了用户，跳过
        if emp.student:
            print(f'  ✓ 已关联用户: {emp.student.nickname or emp.student.username}')
            # 强制同步期数和性别
            emp.save()
            updated_count += 1
            continue

        # 尝试通过姓名匹配用户
        matching_users = User.objects.filter(nickname=emp.student_name)

        if not matching_users.exists():
            # 尝试通过用户名匹配
            matching_users = User.objects.filter(username=emp.student_name)

        if matching_users.exists():
            user = matching_users.first()
            emp.student = user
            emp.save()  # save() 方法会自动同步期数和性别
            print(f'  ✓ 关联用户: {user.nickname or user.username}')
            print(f'  ✓ 同步期数: {emp.period or "未填写"}')
            print(f'  ✓ 同步性别: {emp.get_gender_display() or "未填写"}')
            updated_count += 1
        else:
            print(f'  ⚠ 未找到匹配的用户')
            not_found_count += 1

    print('\n' + '=' * 60)
    print(f'同步完成！')
    print(f'  成功更新: {updated_count} 条记录')
    print(f'  未找到用户: {not_found_count} 条记录')


if __name__ == '__main__':
    sync_employment_data()
