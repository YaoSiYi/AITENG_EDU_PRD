#!/usr/bin/env python
"""
题库数据库备份导出脚本
将数据库中的题目导出为JSON格式，便于备份和迁移
"""
import os
import sys
import json
import django
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.questions.models import Question, QuestionCategory


def export_questions_to_json(output_file=None):
    """导出所有题目到JSON文件"""

    if output_file is None:
        # 默认文件名包含时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'question_bank_backup_{timestamp}.json'

    output_path = Path(output_file)

    print(f"\n{'='*60}")
    print(f"题库数据导出")
    print(f"{'='*60}\n")

    # 导出分类
    categories_data = []
    for cat in QuestionCategory.objects.all():
        categories_data.append({
            'id': cat.id,
            'name': cat.name,
            'parent_id': cat.parent_id,
            'created_at': cat.created_at.isoformat()
        })

    # 导出题目
    questions_data = []
    for q in Question.objects.all():
        questions_data.append({
            'id': q.id,
            'stage': q.stage,
            'category_id': q.category_id,
            'category_name': q.category.name if q.category else None,
            'subject': q.subject,
            'difficulty': q.difficulty,
            'content': q.content,
            'answer': q.answer,
            'explanation': q.explanation,
            'created_at': q.created_at.isoformat(),
            'updated_at': q.updated_at.isoformat()
        })

    # 组装数据
    export_data = {
        'export_time': datetime.now().isoformat(),
        'version': '1.0',
        'statistics': {
            'total_categories': len(categories_data),
            'total_questions': len(questions_data),
            'by_difficulty': {
                'easy': Question.objects.filter(difficulty='easy').count(),
                'medium': Question.objects.filter(difficulty='medium').count(),
                'hard': Question.objects.filter(difficulty='hard').count()
            }
        },
        'categories': categories_data,
        'questions': questions_data
    }

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"✓ 导出成功: {output_path}")
    print(f"  - 分类数: {len(categories_data)}")
    print(f"  - 题目数: {len(questions_data)}")
    print(f"  - 文件大小: {output_path.stat().st_size / 1024:.2f} KB")
    print(f"\n{'='*60}\n")

    return str(output_path)


def import_questions_from_json(input_file):
    """从JSON文件导入题目（用于恢复备份）"""

    input_path = Path(input_file)

    if not input_path.exists():
        print(f"❌ 错误: 文件不存在 - {input_file}")
        return

    print(f"\n{'='*60}")
    print(f"从备份恢复题库数据")
    print(f"{'='*60}\n")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"备份信息:")
    print(f"  - 导出时间: {data['export_time']}")
    print(f"  - 版本: {data['version']}")
    print(f"  - 分类数: {data['statistics']['total_categories']}")
    print(f"  - 题目数: {data['statistics']['total_questions']}")

    # 询问是否继续
    response = input("\n是否继续导入？这将覆盖现有数据 (y/n): ")
    if response.lower() != 'y':
        print("取消导入")
        return

    # 清空现有数据
    print("\n清空现有数据...")
    Question.objects.all().delete()
    QuestionCategory.objects.all().delete()

    # 导入分类
    print("导入分类...")
    category_map = {}
    for cat_data in data['categories']:
        cat = QuestionCategory.objects.create(
            name=cat_data['name'],
            parent_id=cat_data['parent_id']
        )
        category_map[cat_data['id']] = cat.id

    # 导入题目
    print("导入题目...")
    for q_data in data['questions']:
        Question.objects.create(
            stage=q_data['stage'],
            category_id=category_map.get(q_data['category_id']),
            subject=q_data['subject'],
            difficulty=q_data['difficulty'],
            content=q_data['content'],
            answer=q_data['answer'],
            explanation=q_data['explanation']
        )

    print(f"\n✓ 导入完成")
    print(f"  - 分类数: {QuestionCategory.objects.count()}")
    print(f"  - 题目数: {Question.objects.count()}")
    print(f"\n{'='*60}\n")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='题库数据备份和恢复工具')
    parser.add_argument('action', choices=['export', 'import'], help='操作类型: export(导出) 或 import(导入)')
    parser.add_argument('--file', '-f', help='文件路径')

    args = parser.parse_args()

    if args.action == 'export':
        export_questions_to_json(args.file)
    elif args.action == 'import':
        if not args.file:
            print("❌ 错误: 导入操作需要指定文件路径 (--file)")
            sys.exit(1)
        import_questions_from_json(args.file)
