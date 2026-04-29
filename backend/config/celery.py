import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('education')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 定时任务配置
app.conf.beat_schedule = {
    'backup-database-daily': {
        'task': 'apps.stats.tasks.backup_database',
        'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点执行
    },
}
