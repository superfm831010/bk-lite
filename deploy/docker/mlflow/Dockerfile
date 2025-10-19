FROM ghcr.io/mlflow/mlflow:latest

# 安装PostgreSQL客户端库
RUN pip install --no-cache-dir psycopg2-binary

# 使用原镜像的入口点
ENTRYPOINT ["mlflow"]
