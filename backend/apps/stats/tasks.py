from celery import shared_task
import subprocess
import os
from datetime import datetime
from django.conf import settings


@shared_task
def backup_database():
    """数据库备份任务"""
    backup_dir = '/backup'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'{backup_dir}/education_backup_{timestamp}.sql'

    try:
        # 执行 mysqldump
        cmd = [
            'mysqldump',
            '-h', os.getenv('DB_HOST', 'db'),
            '-u', os.getenv('DB_USER', 'root'),
            f'-p{os.getenv("DB_ROOT_PASS", "education123")}',
            os.getenv('DB_NAME', 'education'),
            '--result-file', backup_file
        ]

        subprocess.run(cmd, check=True)

        # 压缩备份文件
        subprocess.run(['gzip', backup_file], check=True)

        return f'数据库备份成功: {backup_file}.gz'
    except Exception as e:
        return f'数据库备份失败: {str(e)}'
