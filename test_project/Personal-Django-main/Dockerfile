FROM python:3.9-slim

WORKDIR /app

# 安装最小化的系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean

# 复制并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# 复制项目代码
COPY . .

# 创建非root用户
RUN useradd -m -s /bin/sh appuser

# 创建必要目录
RUN mkdir -p logs media staticfiles
RUN chown -R appuser:appuser logs media staticfiles /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "DjangoProject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--worker-class", "sync", "--max-requests", "500", "--timeout", "30", "--keep-alive", "2"]