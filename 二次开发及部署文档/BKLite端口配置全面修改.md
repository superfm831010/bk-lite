# BKLite 端口配置全面修改

## 修改日期
2025-10-19

## 修改背景

为避免BKLite与其他系统端口冲突，对所有对外暴露的端口进行了统一调整。采用1xxxx系列端口号，降低与常用服务冲突的可能性。

## 端口映射方案

### 基础设施服务（Docker容器）

| 服务名称 | 原端口 | 新端口 | 说明 | 是否暴露 |
|---------|-------|-------|------|---------|
| **PostgreSQL** | 5432 | 15432 | 数据库服务 | ✓ |
| **Redis** | 6379 → 6380 | 16380 | 缓存和消息队列 | ✓ |
| **MinIO API** | 9000 | 19000 | 对象存储API | ✓ |
| **MinIO Console** | 9001 | 19001 | MinIO管理界面 | ✓ |
| **NATS** | 4222 | 14222 | 消息服务器 | ✓ |
| **NATS Monitor** | 8222 | - | 监控端口 | ✗ (不暴露) |
| **Victoria Metrics** | 8428 | 18428 | 时序数据库 | ✓ |
| **Victoria Logs** | 9428 | 19428 | 日志存储 | ✓ |
| **FalkorDB** | 6479 | 16479 | 图数据库 | ✓ |
| **MLflow** | 5000 | 15000 | ML实验跟踪 | ✓ |

### 应用服务（主机进程）

| 服务名称 | 原端口 | 新端口 | 说明 |
|---------|-------|-------|------|
| **Server (Django)** | 8001 | 18001 | 后端API服务 |
| **Web (Next.js)** | 3000 | 3011 | 前端Web应用 |
| **Mobile (Next.js)** | 3001 | 13001 | 移动端应用(待配置) |

## 修改的文件清单

### 1. Docker Compose配置
**文件**: `docker-compose.dev.yml`

修改内容：
- PostgreSQL: `5432:5432` → `15432:5432`
- Redis: `6380:6379` → `16380:6379`
- MinIO API: `9000:9000` → `19000:9000`
- MinIO Console: `9001:9001` → `19001:9001`
- NATS: `4222:4222` → `14222:4222`
- NATS Monitor: `8222:8222` → 移除（不暴露）
- Victoria Metrics: `8428:8428` → `18428:8428`
- Victoria Logs: `9428:9428` → `19428:9428`
- FalkorDB: `6479:6379` → `16479:6379`
- MLflow: `5000:5000` → `15000:5000`

### 2. Server配置文件

#### `server/.env.dev` 和 `server/.env`
```bash
# 数据库端口
DB_PORT=5432 → 15432

# Redis端口
REDIS_CACHE_URL=redis://:bklite_redis_pass@localhost:6380/0 → localhost:16380/0
CELERY_BROKER_URL=redis://:bklite_redis_pass@localhost:6380/1 → localhost:16380/1
CELERY_RESULT_BACKEND=redis://:bklite_redis_pass@localhost:6380/1 → localhost:16380/1

# NATS端口
NATS_SERVERS=nats://localhost:4222 → localhost:14222

# MinIO端口
MINIO_ENDPOINT=localhost:9000 → localhost:19000
MLFLOW_S3_ENDPOINT_URL=http://localhost:9000 → localhost:19000

# Victoria Metrics端口
VICTORIAMETRICS_HOST=http://localhost:8428 → localhost:18428

# Victoria Logs端口
VICTORIALOGS_HOST=http://localhost:9428 → localhost:19428

# MLflow端口
MLFLOW_TRACKER_URL=http://localhost:5000 → localhost:15000

# FalkorDB端口
FALKORDB_PORT=6479 → 16479
```

#### `server/Makefile`
```makefile
# dev目标端口
--port 8001 → --port 18001
```

### 3. Web配置文件

#### `web/package.json`
```json
"dev": "next dev" → "next dev -p 3011"
```

#### `web/.env.local` 和 `web/.env.local.dev`
```bash
# NextAuth URL
NEXTAUTH_URL=http://localhost:3000 → http://localhost:3011

# 后端API地址
NEXTAPI_URL=http://localhost:8001 → http://localhost:18001

# 微信回调地址
WECHAT_APP_REDIRECT_URI=http://localhost:3000 → http://localhost:3011
```

### 4. 开发脚本

#### `dev.sh`
```bash
# Server启动端口
--port 8001 → --port 18001

# 访问地址提示
http://localhost:3000 → http://localhost:3011
http://localhost:8001 → http://localhost:18001
http://localhost:9001 → http://localhost:19001
http://localhost:5000 → http://localhost:15000
```

## 服务启动验证

### 启动所有服务
```bash
# 停止所有服务
./dev.sh stop all

# 启动基础设施
./dev.sh start infra

# 启动应用服务
./dev.sh start all

# 查看状态
./dev.sh status
```

### 验证端口监听
```bash
# 检查Redis
redis-cli -h localhost -p 16380 -a bklite_redis_pass ping

# 检查PostgreSQL
docker exec bklite-postgres-dev pg_isready -U postgres

# 检查MinIO
curl -s http://localhost:19000/minio/health/live

# 检查Server
lsof -i:18001

# 检查Web
lsof -i:3011
```

## 访问地址更新

开发环境各服务访问地址：

### 主要应用
- **Web前端**: http://localhost:3011
- **Server API**: http://localhost:18001

### 管理界面
- **MinIO控制台**: http://localhost:19001
  - 用户名: minioadmin
  - 密码: minioadmin123
- **MLflow**: http://localhost:15000

### 数据库连接
```bash
# PostgreSQL
Host: localhost
Port: 15432
User: postgres
Password: bklite_dev_pass
Database: bklite

# Redis
Host: localhost
Port: 16380
Password: bklite_redis_pass

# FalkorDB
Host: localhost
Port: 16479
Password: bklite_falkordb_pass
```

## 注意事项

### 1. 端口冲突排查
如果服务启动失败，检查端口占用：
```bash
# 检查具体端口
lsof -i:端口号

# 杀死占用进程
kill -9 PID
```

### 2. 容器端口vs宿主端口
- **容器内部端口**: 保持不变（如Redis容器内仍是6379）
- **宿主机映射端口**: 已修改为1xxxx系列（如16380）
- **配置文件引用**: 使用宿主机端口

### 3. 不暴露的端口
NATS Monitor端口(8222)未对外暴露，仅容器间访问。如需访问监控界面，可以临时添加端口映射或使用`docker exec`。

### 4. 环境文件
`.env`和`.env.local`文件不在版本控制中，修改后仅本地生效。团队其他成员需手动更新本地配置文件。

### 5. MLflow健康问题
MLflow容器可能因缺少`psycopg2`模块持续重启，不影响核心开发功能。如需使用MLflow，需要在MLflow镜像中安装psycopg2-binary。

## 回滚方案

如需回滚到原端口配置，参考以下命令：
```bash
# 停止所有服务
./dev.sh stop all

# Git回滚配置文件
git checkout HEAD~1 -- docker-compose.dev.yml dev.sh server/Makefile web/package.json

# 手动恢复.env文件（未纳入版本控制）
# 参考.env.example中的端口配置

# 重启服务
./dev.sh start all
```

## 相关文档
- [Redis端口配置修改.md](./Redis端口配置修改.md) - 初始Redis端口修改记录
- [DEVELOPMENT.md](../DEVELOPMENT.md) - 本地开发指南
