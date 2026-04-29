#!/usr/bin/env python
"""
题库更新脚本 - 按难度分级导入
从题库文件夹中按照难度（简单、中等、困难）导入题目
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
        print(f"  创建新分类: {name}")
    return category


def parse_txt_file(file_path):
    """解析 txt 文件，提取题目内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            return None

        # 从文件名提取题目标题
        filename = file_path.stem
        # 移除编号前缀（如 0001.）
        if '.' in filename:
            parts = filename.split('.', 1)
            if len(parts) > 1 and parts[0].isdigit():
                title = parts[1]
            else:
                title = filename
        else:
            title = filename

        return {
            'title': title,
            'content': content
        }
    except Exception as e:
        print(f"  错误: 无法读取文件 {file_path.name} - {e}")
        return None


def get_subject_from_path(file_path):
    """从文件路径提取科目"""
    # 如果文件在子文件夹中，使用子文件夹名作为科目
    parent_dir = file_path.parent.name
    if parent_dir in ['简单', '中等', '困难']:
        # 如果父目录是难度目录，使用文件名前缀作为科目
        filename = file_path.stem
        if '.' in filename:
            parts = filename.split('.', 1)
            if len(parts) > 1:
                # 提取题目类型（如"测试流程"、"接口测试"等）
                title = parts[1]
                if '测试' in title:
                    return '软件测试'
                elif '接口' in title:
                    return '接口测试'
                elif 'bug' in title.lower() or 'Bug' in title or 'BUG' in title:
                    return '缺陷管理'
                else:
                    return '测试理论'
        return '测试理论'
    else:
        # 使用子文件夹名作为科目
        return parent_dir


def import_questions_from_directory(base_dir, difficulty, category_name):
    """从指定目录导入题目"""
    dir_path = Path(base_dir) / difficulty

    if not dir_path.exists():
        print(f"\n目录不存在: {dir_path}")
        return 0, 0

    print(f"\n正在处理 {difficulty} 难度题目...")

    # 获取所有 txt 文件
    txt_files = list(dir_path.rglob("*.txt"))

    if not txt_files:
        print(f"  未找到题目文件")
        return 0, 0

    imported_count = 0
    skipped_count = 0

    # 难度映射
    difficulty_map = {
        '简单': 'easy',
        '中等': 'medium',
        '困难': 'hard'
    }
    difficulty_value = difficulty_map.get(difficulty, 'medium')

    for file_path in sorted(txt_files):
        # 解析文件
        question_data = parse_txt_file(file_path)

        if not question_data:
            skipped_count += 1
            continue

        title = question_data['title']
        content = question_data['content']

        # 提取科目
        subject = get_subject_from_path(file_path)

        # 创建或获取分类
        category = get_or_create_category(subject)

        # 检查是否已存在（根据标题和内容前100个字符）
        content_preview = content[:100]
        existing = Question.objects.filter(
            content__startswith=content_preview
        ).first()

        if existing:
            skipped_count += 1
            continue

        # 创建题目
        Question.objects.create(
            stage=1,
            category=category,
            subject=subject,
            difficulty=difficulty_value,
            content=title,
            answer=content,
            explanation=''
        )
        imported_count += 1
        print(f"  ✓ 导入: {title[:50]}...")

    print(f"  {difficulty} 难度: 导入 {imported_count} 个，跳过 {skipped_count} 个")
    return imported_count, skipped_count


def clear_existing_questions():
    """清空现有题目"""
    count = Question.objects.count()
    if count > 0:
        Question.objects.all().delete()
        print(f"已清空 {count} 个旧题目")
        return True
    return False


def main():
    """主函数"""
    question_dir = Path(__file__).parent.parent / "题库"

    if not question_dir.exists():
        print(f"错误: 题库文件夹不存在: {question_dir}")
        return

    print("="*80)
    print("题库更新脚本 - 按难度分级导入")
    print("="*80)

    # 询问是否清空现有题目
    clear_existing_questions()

    total_imported = 0
    total_skipped = 0

    # 按难度导入
    difficulties = ['简单', '中等', '困难']

    for difficulty in difficulties:
        imported, skipped = import_questions_from_directory(
            question_dir, difficulty, difficulty
        )
        total_imported += imported
        total_skipped += skipped

    print("\n" + "="*80)
    print(f"导入完成！")
    print(f"总计导入: {total_imported} 个题目")
    print(f"总计跳过: {total_skipped} 个题目")
    print("="*80)

    # 显示统计信息
    print("\n题库统计:")
    print(f"  题目总数: {Question.objects.count()}")
    print(f"  分类总数: {QuestionCategory.objects.count()}")

    print("\n各难度题目数量:")
    for diff_name, diff_value in [('简单', 'easy'), ('中等', 'medium'), ('困难', 'hard')]:
        count = Question.objects.filter(difficulty=diff_value).count()
        print(f"  {diff_name}: {count} 个")

    print("\n各分类题目数量:")
    for cat in QuestionCategory.objects.all():
        count = Question.objects.filter(category=cat).count()
        if count > 0:
            print(f"  {cat.name}: {count} 个")


if __name__ == "__main__":
    main()
