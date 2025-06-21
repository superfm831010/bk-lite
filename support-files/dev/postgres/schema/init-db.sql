-- 创建所需的数据库
CREATE DATABASE bklite;
CREATE DATABASE airflow;
CREATE DATABASE mlflow;


-- 为每个数据库设置默认用户权限
GRANT ALL PRIVILEGES ON DATABASE airflow TO postgres;
GRANT ALL PRIVILEGES ON DATABASE mlflow TO postgres;
GRANT ALL PRIVILEGES ON DATABASE mlflow TO postgres;
