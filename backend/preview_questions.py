#!/usr/bin/env python
"""
题库导入脚本 - 查看文档格式
"""
import os
import sys
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from docx import Document


def preview_docx(file_path, num_paras=60):
    """预览 docx 文件内容"""
    print(f"\n{'='*80}")
    print(f"文件: {Path(file_path).name}")
    print(f"{'='*80}")
    doc = Document(file_path)

    count = 0
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip():
            print(f"[{i}] {para.text[:120]}")
            count += 1
            if count >= num_paras:
                break


def main():
    question_dir = Path(__file__).parent.parent / "题库"
    docx_files = sorted(question_dir.glob("*.docx"))

    for f in docx_files:
        preview_docx(f, 40)
        print()


if __name__ == "__main__":
    main()
