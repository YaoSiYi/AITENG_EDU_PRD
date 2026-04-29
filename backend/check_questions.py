#!/usr/bin/env python
"""查看题库统计信息"""
import os
import sys
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.questions.models import Question, QuestionCategory


def main():
    print("="*80)
    print("题库统计信息")
    print("="*80)

    total_questions = Question.objects.count()
    total_categories = QuestionCategory.objects.count()

    print(f"\n题目总数: {total_questions}")
    print(f"分类总数: {total_categories}")

    print("\n各分类题目数量:")
    for cat in QuestionCategory.objects.all():
        count = Question.objects.filter(category=cat).count()
        print(f"  {cat.name}: {count} 个题目")

    print("\n各科目题目数量:")
    subjects = Question.objects.values_list('subject', flat=True).distinct()
    for subject in subjects:
        count = Question.objects.filter(subject=subject).count()
        print(f"  {subject}: {count} 个题目")

    print("\n最近导入的 5 个题目:")
    for q in Question.objects.all()[:5]:
        print(f"  [{q.subject}] {q.content[:50]}...")

    print("="*80)


if __name__ == "__main__":
    main()
