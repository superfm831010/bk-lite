# 修复 NATS JetStream 持久化配置问题

## 问题描述

**现象：** 内网初始化上传控制器包后，Docker 重启后包文件消失

**影响范围：**
- 探针管理中上传的控制器包（fusion-collectors）
- 采集器包版本记录
- 所有通过 NATS JetStream Object Store 存储的文件

## 问题分析

### 1. 文件存储机制

BlueKing Lite 使用 NATS JetStream Object Store 来存储探针和采集器包文件：

```python
# server/apps/node_mgmt/services/package.py
class PackageService:
    @staticmethod
    def upload_file(file: ContentFile, data):
        # 上传到 NATS JetStream Object Store
        s3_file_path = f"{data['os']}/{data['object']}/{data['version']}/{data['name']}"
        async_to_sync(upload_file_to_s3)(file, s3_file_path)
```

```python
# server/apps/rpc/jetstream.py
class JetStreamService:
    def __init__(self, bucket_name=NATS_NAMESPACE):
        self.bucket_name = bucket_name  # 默认 'bklite'

    async def put(self, key, data, description=None):
        # 数据存储到 JetStream Object Store
        info = await self.object_store.put(key, data, meta=meta)
```

### 2. NATS JetStream 配置

NATS 配置文件 (`deploy-huangpu/conf/nats/nats.conf`):

```conf
jetstream {
  store_dir: /data/jetstream    # ← JetStream 数据存储目录
  max_mem: 1G
  max_file: 10G
}
```

### 3. Docker Compose 挂载配置（问题所在）

**修复前的配置** (`deploy-huangpu/docker-compose.yml`):

```yaml
nats:
  image: nats:2.10.25
  container_name: bklite-nats-prod
  volumes:
    - ./conf/nats/nats.conf:/etc/nats/nats.conf:ro
    - ./conf/certs:/etc/nats/certs:ro
    - huangpu_nats:/nats    # ❌ 挂载到 /nats，但 JetStream 使用 /data
```

**问题根因：**
- NATS JetStream 将数据存储在 `/data/jetstream` 目录
- Docker Compose 将 volume 挂载到 `/nats` 目录
- `/data` 目录没有挂载到 volume，是容器内的临时目录
- Docker 容器重启后，`/data/jetstream` 中的数据丢失

### 4. 完整数据流程

```
1. 用户上传控制器包
   ↓
2. Web 前端发送文件到 Server API (/api/v1/node/package/)
   ↓
3. PackageService.upload_file() 调用
   ↓
4. JetStreamService.put() 存储到 NATS JetStream
   ↓
5. NATS 将数据写入 /data/jetstream/ 目录
   ↓
6. ❌ 容器重启，/data 目录内容丢失
```

## 全面持久化配置检查

为确保没有其他服务存在类似问题，对所有服务进行了全面检查：

| 服务 | 数据目录 | Volume 挂载 | 状态 |
|------|----------|-------------|------|
| PostgreSQL | `/var/lib/postgresql/data` | `huangpu_postgres:/var/lib/postgresql/data` | ✅ 正确 |
| Redis | `/data` | `huangpu_redis:/data` | ✅ 正确 |
| **NATS** | `/data/jetstream` | ~~`huangpu_nats:/nats`~~ | ❌ **错误** |
| Victoria Metrics | `/victoria-metrics-data` | `huangpu_victoria_metrics:/victoria-metrics-data` | ✅ 正确 |
| Victoria Logs | `/vlogs` | `huangpu_victoria_logs:/vlogs` | ✅ 正确 |
| MinIO | `/data` | `huangpu_minio:/data` | ✅ 正确 |
| FalkorDB | `/var/lib/falkordb/data` | `huangpu_falkordb:/var/lib/falkordb/data` | ✅ 正确 |
| MLflow | PostgreSQL + MinIO | - | ✅ 正确 |

**检查方法：**

```bash
# 查看 FalkorDB 镜像配置（示例）
docker inspect falkordb/falkordb:v4.12.4 --format='{{range .Config.Env}}{{println .}}{{end}}'
# 输出: FALKORDB_DATA_PATH=/var/lib/falkordb/data

# 查看声明的 volumes
docker inspect falkordb/falkordb:v4.12.4 --format='{{.Config.Volumes}}'
```

## 解决方案

### 修复内容

修改 `deploy-huangpu/docker-compose.yml` 第 96 行：

```yaml
# 修复前
nats:
  volumes:
    - huangpu_nats:/nats

# 修复后
nats:
  volumes:
    - huangpu_nats:/data
```

### 修复原理

- NATS JetStream 配置的 `store_dir: /data/jetstream`
- Docker volume `huangpu_nats` 挂载到 `/data`
- JetStream 数据写入 `/data/jetstream`，实际存储在 Docker volume 中
- 容器重启后，`huangpu_nats` volume 中的数据得以保留

## 部署后验证

### 1. 重新部署服务

```bash
cd /path/to/deploy-huangpu

# 停止服务
docker compose down

# 启动服务（会使用新的挂载配置）
docker compose up -d nats

# 等待 NATS 启动
docker logs -f bklite-nats-prod
```

### 2. 验证持久化

```bash
# 进入 NATS 容器检查
docker exec -it bklite-nats-prod sh

# 检查 JetStream 数据目录
ls -la /data/jetstream/

# 退出容器
exit
```

### 3. 测试上传控制器包

1. 登录 Web 界面
2. 进入"节点管理 -> 探针管理 -> 控制器"
3. 点击"上传包"，上传 `fusion-collectors-linux-amd64.zip`
4. 上传成功后，检查数据库记录：

```bash
docker exec bklite-postgres-prod env PGPASSWORD=bklite \
  psql -U postgres -d bklite -c \
  "SELECT id, type, os, object, version, name FROM node_mgmt_packageversion WHERE type='controller';"
```

5. 重启 NATS 容器：

```bash
docker restart bklite-nats-prod
```

6. 重启后，重新检查控制器包是否仍然存在：
   - Web 界面可以查看包列表
   - 可以下载包文件
   - 数据库记录完整

### 4. 验证 JetStream Object Store

```bash
# 使用 nats CLI 工具检查（如果已安装）
docker exec -it bklite-nats-prod /bin/sh -c "nats object ls bklite"
```

## 注意事项

### 1. 现有数据迁移

如果修复前已经上传过包，重新挂载后这些数据会丢失（因为之前的数据在 `/nats` 目录中）。

**解决方法：**
- 重新运行初始化脚本：`./init-probe-packages.sh --auto`
- 重新上传控制器包

### 2. Volume 清理

如果需要清理旧数据：

```bash
# 停止服务
docker compose down

# 删除 NATS volume（会删除所有 JetStream 数据）
docker volume rm bklite-prod-huangpu_huangpu_nats

# 重新启动
docker compose up -d
```

### 3. 备份建议

定期备份 NATS JetStream 数据：

```bash
# 备份 volume
docker run --rm -v bklite-prod-huangpu_huangpu_nats:/data \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/nats-jetstream-$(date +%Y%m%d).tar.gz /data

# 恢复 volume
docker run --rm -v bklite-prod-huangpu_huangpu_nats:/data \
  -v $(pwd)/backup:/backup \
  alpine tar xzf /backup/nats-jetstream-20251021.tar.gz -C /
```

## 相关文件

- `deploy-huangpu/docker-compose.yml` - Docker Compose 配置（已修改）
- `deploy-huangpu/conf/nats/nats.conf` - NATS 配置文件
- `server/apps/node_mgmt/services/package.py` - 包上传服务
- `server/apps/rpc/jetstream.py` - JetStream 客户端
- `server/apps/node_mgmt/utils/s3.py` - 文件存储工具

## 修改记录

- **日期**: 2025-10-21
- **问题**: NATS JetStream 持久化配置不匹配导致重启后数据丢失
- **修复**: 将 NATS volume 挂载点从 `/nats` 改为 `/data`
- **影响**: 控制器包和采集器包上传后可正常持久化
- **验证**: 全面检查所有服务的持久化配置，仅 NATS 存在此问题
