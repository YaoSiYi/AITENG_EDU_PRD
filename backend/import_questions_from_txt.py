#!/usr/bin/env python
"""
题库导入脚本 - 从txt文件导入
实施方案A：以数据库为主的题库管理
"""
import os
import sys
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.questions.models import Question, QuestionCategory


def get_or_create_category(name, parent=None):
    """获取或创建分类"""
    category, created = QuestionCategory.objects.get_or_create(
        name=name,
        parent=parent
    )
    if created:
        print(f"  ✓ 创建新分类: {name}")
    return category


def parse_filename(filename):
    """
    从文件名解析题目信息
    格式: 0001.测试流程.txt
    返回: (序号, 标题)
    """
    name = filename.replace('.txt', '')
    parts = name.split('.', 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return None, name


def determine_subject(content, filepath):
    """根据内容和路径判断科目"""
    content_lower = content.lower()
    path_str = str(filepath).lower()

    # 根据路径判断
    if '安全测试' in path_str:
        return '安全测试'
    if '接口测试' in path_str:
        return '接口测试'

    # 根据内容关键词判断
    if any(kw in content for kw in ['接口', 'API', 'postman', 'requests']):
        return '接口测试'
    if any(kw in content for kw in ['安全', '漏洞', '权限', '加密']):
        return '安全测试'
    if any(kw in content for kw in ['测试用例', '测试计划', '测试流程', 'bug']):
        return '软件测试基础'
    if any(kw in content for kw in ['电商', '业务流程', '订单']):
        return '业务测试'

    return '软件测试基础'


def import_questions_from_directory(base_dir):
    """从目录导入所有题目"""
    base_path = Path(base_dir)

    if not base_path.exists():
        print(f"❌ 错误: 目录不存在 - {base_dir}")
        return

    # 统计信息
    stats = {
        'total': 0,
        'imported': 0,
        'skipped': 0,
        'errors': 0
    }

    # 难度映射
    difficulty_map = {
        '简单': 'easy',
        '中等': 'medium',
        '困难': 'hard'
    }

    print(f"\n{'='*60}")
    print(f"开始导入题库: {base_dir}")
    print(f"{'='*60}\n")

    # 遍历所有txt文件
    for txt_file in base_path.rglob('*.txt'):
        stats['total'] += 1

        # 确定难度
        difficulty = 'easy'
        for diff_name, diff_value in difficulty_map.items():
            if diff_name in str(txt_file):
                difficulty = diff_value
                break

        try:
            # 读取文件内容
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                print(f"⚠️  跳过空文件: {txt_file.name}")
                stats['skipped'] += 1
                continue

            # 解析文件名
            seq_num, title = parse_filename(txt_file.name)

            # 提取题目和答案
            # 假设第一行或第一段是题目，其余是答案
            lines = content.split('\n', 1)
            if len(lines) == 2:
                question_content = lines[0].strip()
                answer_content = lines[1].strip()
            else:
                # 如果没有明显分隔，使用标题作为题目，内容作为答案
                question_content = title
                answer_content = content

            # 去除题目内容中的冒号和空格
            question_content = question_content.rstrip('：:').strip()

            # 检查是否已存在（根据content去重）
            if Question.objects.filter(content=question_content).exists():
                print(f"⊘  已存在: {txt_file.name}")
                stats['skipped'] += 1
                continue

            # 判断科目
            subject = determine_subject(content, txt_file)

            # 创建或获取分类
            category = get_or_create_category(subject)

            # 创建题目
            question = Question.objects.create(
                stage=1,  # 默认阶段1
                category=category,
                subject=subject,
                difficulty=difficulty,
                content=question_content,
                answer=answer_content,
                explanation=''
            )

            print(f"✓  导入成功: {txt_file.name} [{difficulty}] [{subject}]")
            stats['imported'] += 1

        except Exception as e:
            print(f"❌ 导入失败: {txt_file.name} - {e}")
            stats['errors'] += 1

    # 打印统计信息
    print(f"\n{'='*60}")
    print(f"导入完成统计:")
    print(f"{'='*60}")
    print(f"  总文件数: {stats['total']}")
    print(f"  成功导入: {stats['imported']}")
    print(f"  跳过重复: {stats['skipped']}")
    print(f"  导入失败: {stats['errors']}")
    print(f"{'='*60}\n")

    # 显示数据库当前状态
    total_questions = Question.objects.count()
    print(f"数据库中题目总数: {total_questions}")

    print("\n按难度分布:")
    for diff_value, diff_label in Question.DIFFICULTY_CHOICES:
        count = Question.objects.filter(difficulty=diff_value).count()
        print(f"  {diff_label}: {count}题")

    print("\n按科目分布:")
    subjects = Question.objects.values_list('subject', flat=True).distinct()
    for subject in subjects:
        count = Question.objects.filter(subject=subject).count()
        print(f"  {subject}: {count}题")


if __name__ == '__main__':
    # 题库目录路径
    question_bank_dir = Path(__file__).parent.parent / '题库'

    # 执行导入
    import_questions_from_directory(question_bank_dir)

    print("\n✅ 导入流程完成！")
    print("💡 提示: 现在可以通过 Django Admin 后台管理题目")
    print("   访问: http://localhost:8000/admin/questions/question/")
