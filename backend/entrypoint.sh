#!/bin/bash
set -e

echo "等待数据库就绪..."
python << END
import sys
import time
import pymysql

for i in range(30):
    try:
        conn = pymysql.connect(
            host='db',
            user='root',
            password='education123',
            database='education'
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
python manage.py makemigrations
python manage.py migrate

echo "收集静态文件..."
python manage.py collectstatic --noinput

echo "启动 Gunicorn..."
exec gunicorn --workers 4 --bind 0.0.0.0:8000 config.wsgi:application
