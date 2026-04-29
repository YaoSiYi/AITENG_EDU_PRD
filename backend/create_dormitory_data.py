#!/usr/bin/env python
"""
创建宿舍管理测试数据脚本
为现有学生用户创建宿舍信息
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.stats.models import Dormitory
from apps.users.models import User


def create_dormitory_data():
    """创建宿舍管理测试数据"""
    print('开始创建宿舍管理测试数据...')
    print('=' * 60)

    # 宿舍分配方案
    dormitory_assignments = [
        {'username': 'linai', 'dormitory': 'A栋101'},
        {'username': 'zhangwei', 'dormitory': 'A栋102'},
        {'username': 'wangqiang', 'dormitory': 'A栋103'},
        {'username': 'liufang', 'dormitory': 'B栋201'},
        {'username': 'zhaoli', 'dormitory': 'B栋202'},
        {'username': 'sunjie', 'dormitory': 'A栋104'},
        {'username': 'chenming', 'dormitory': 'A栋105'},
        {'username': 'zhoumin', 'dormitory': 'B栋203'},
        {'username': 'liuyuhang', 'dormitory': 'A栋106'},
        {'username': 'wangdachui', 'dormitory': 'A栋107'},
        {'username': 'testuser', 'dormitory': 'C栋301'},
        {'username': 'student01', 'dormitory': 'C栋302'},
        {'username': 'student02', 'dormitory': 'B栋204'},
        {'username': 'student03', 'dormitory': 'C栋303'},
        {'username': 'student04', 'dormitory': 'B栋205'},
    ]

    created_count = 0
    updated_count = 0
    skipped_count = 0

    for assignment in dormitory_assignments:
        username = assignment['username']
        dormitory = assignment['dormitory']

        print(f"\n处理用户: {username}")

        # 查找用户
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"  ⚠ 用户不存在，跳过")
            skipped_count += 1
            continue

        # 检查是否已有宿舍记录
        existing = Dormitory.objects.filter(student=user).first()

        if existing:
            # 更新宿舍号
            existing.dormitory = dormitory
            existing.save()
            print(f"  ✓ 更新宿舍记录: {dormitory}")
            updated_count += 1
        else:
            # 创建新宿舍记录
            dorm = Dormitory.objects.create(
                student=user,
                dormitory=dormitory
            )
            print(f"  ✓ 创建宿舍记录: {dormitory}")
            print(f"  ✓ 姓名: {dorm.student_name}")
            print(f"  ✓ 性别: {dorm.get_gender_display() or '未填写'}")
            print(f"  ✓ 期数: {dorm.period or '未填写'}")
            print(f"  ✓ 籍贯: {dorm.hometown or '未填写'}")
            print(f"  ✓ 手机号: {dorm.phone or '未填写'}")
            created_count += 1

    print('\n' + '=' * 60)
    print(f'创建完成！')
    print(f'  创建记录: {created_count} 条')
    print(f'  更新记录: {updated_count} 条')
    print(f'  跳过用户: {skipped_count} 个')


if __name__ == '__main__':
    create_dormitory_data()
