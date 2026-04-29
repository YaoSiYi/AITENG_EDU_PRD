#!/usr/bin/env python
"""
题库导入脚本
从 Word 文档中解析题目并导入到数据库
"""
import os
import sys
import re
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from docx import Document
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


def parse_questions_from_docx(file_path):
    """从 docx 文件中解析题目"""
    print(f"\n正在解析: {file_path.name}")

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"  错误: 无法打开文件 - {e}")
        return []

    questions = []
    current_question = None
    current_answer = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # 判断是否是问题（以问号结尾）
        if text.endswith('？') or text.endswith('?'):
            # 保存上一个问题
            if current_question:
                questions.append({
                    'content': current_question,
                    'answer': '\n'.join(current_answer).strip()
                })

            # 开始新问题
            current_question = text
            current_answer = []
        else:
            # 累积答案
            if current_question:
                current_answer.append(text)

    # 保存最后一个问题
    if current_question:
        questions.append({
            'content': current_question,
            'answer': '\n'.join(current_answer).strip()
        })

    print(f"  解析到 {len(questions)} 个题目")
    return questions


def import_questions_from_file(file_path, category_name, subject):
    """从文件导入题目到数据库"""
    # 创建分类
    category = get_or_create_category(category_name)

    # 解析题目
    questions = parse_questions_from_docx(file_path)

    # 导入到数据库
    imported_count = 0
    skipped_count = 0

    for q_data in questions:
        content = q_data['content']
        answer = q_data['answer']

        # 跳过没有答案的题目
        if not answer:
            skipped_count += 1
            continue

        # 检查是否已存在
        if Question.objects.filter(content=content).exists():
            skipped_count += 1
            continue

        # 创建题目
        Question.objects.create(
            stage=1,  # 默认阶段1
            category=category,
            subject=subject,
            difficulty='medium',  # 默认中等难度
            content=content,
            answer=answer,
            explanation=''
        )
        imported_count += 1

    print(f"  导入 {imported_count} 个题目，跳过 {skipped_count} 个")
    return imported_count, skipped_count


def main():
    """主函数"""
    question_dir = Path(__file__).parent.parent / "题库"

    if not question_dir.exists():
        print(f"错误: 题库文件夹不存在: {question_dir}")
        return

    # 定义文件和对应的分类、科目
    file_mappings = [
        ("python基础面试题+自动化.docx", "Python", "Python基础"),
        ("python自动化面试题补充.docx", "Python", "Python自动化测试"),
        ("程序.网络.数据库.安全性测试知识点.docx", "测试理论", "综合测试知识"),
        ("软测高频面试题.doc", "测试理论", "软件测试"),
        ("APP测试.doc", "测试理论", "APP测试"),
        ("实物测试点.docx", "测试理论", "实物测试"),
        ("接口自动化实现接口关联.docx", "接口测试", "接口自动化"),
        ("项目介绍.docx", "项目经验", "项目介绍"),
    ]

    total_imported = 0
    total_skipped = 0

    print("="*80)
    print("开始导入题库")
    print("="*80)

    for filename, category_name, subject in file_mappings:
        file_path = question_dir / filename
        if file_path.exists():
            imported, skipped = import_questions_from_file(
                file_path, category_name, subject
            )
            total_imported += imported
            total_skipped += skipped
        else:
            print(f"\n文件不存在: {filename}")

    print("\n" + "="*80)
    print(f"导入完成！")
    print(f"总计导入: {total_imported} 个题目")
    print(f"总计跳过: {total_skipped} 个题目")
    print("="*80)


if __name__ == "__main__":
    main()
