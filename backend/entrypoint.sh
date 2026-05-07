#!/bin/bash
set -e

echo "等待数据库就绪..."
python << END
import sys
import time
import os
import pymysql

db_host = os.environ.get('DB_HOST', 'db')
db_port = int(os.environ.get('DB_PORT', 3306))
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_ROOT_PASS', os.environ.get('MYSQL_ROOT_PASSWORD', 'education123'))
db_name = os.environ.get('DB_NAME', 'education')

for i in range(30):
    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        conn.close()
        print("数据库连接成功!")
        sys.exit(0)
    except Exception as e:
        print(f"等待数据库... ({i+1}/30)")
        time.sleep(2)

print("数据库连接超时!")
sys.exit(1)
END

echo "运行数据库迁移..."
python manage.py makemigrations --noinput --skip-checks
python manage.py migrate --noinput --skip-checks

echo "收集静态文件..."
python manage.py collectstatic --noinput --skip-checks

echo "启动 Gunicorn..."
exec gunicorn --workers ${GUNICORN_WORKERS:-4} \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    config.wsgi:application
