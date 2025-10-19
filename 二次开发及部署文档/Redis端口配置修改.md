# Redis端口配置修改

## 修改日期
2025-10-19

## 问题描述
在启动本地开发环境时，Docker容器启动失败，错误信息显示：
```
Error response from daemon: failed to set up container networking:
driver failed programming external connectivity on endpoint bklite-redis-dev:
failed to bind host port for 0.0.0.0:6379:172.20.0.8:6379/tcp: address already in use
```

原因是宿主机的6379端口已被占用（可能是系统已运行其他Redis实例）。

## 解决方案
将BKLite开发环境的Redis端口映射从6379修改为6380。

## 修改的文件

### 1. docker-compose.dev.yml
**位置**: 第47行
**修改内容**:
```yaml
# 修改前
ports:
  - "6379:6379"

# 修改后
ports:
  - "6380:6379"
```

### 2. server/.env.dev
**位置**: 第18、22、23行
**修改内容**: 所有Redis连接URL的端口从6379改为6380
```bash
# 修改前
REDIS_CACHE_URL=redis://:bklite_redis_pass@localhost:6379/0
CELERY_BROKER_URL=redis://:bklite_redis_pass@localhost:6379/1
CELERY_RESULT_BACKEND=redis://:bklite_redis_pass@localhost:6379/1

# 修改后
REDIS_CACHE_URL=redis://:bklite_redis_pass@localhost:6380/0
CELERY_BROKER_URL=redis://:bklite_redis_pass@localhost:6380/1
CELERY_RESULT_BACKEND=redis://:bklite_redis_pass@localhost:6380/1
```

### 3. server/.env
**位置**: 第18、22、23行
**修改内容**: 与.env.dev相同

## 验证步骤

### 1. 停止旧的服务
```bash
./dev.sh stop infra
```

### 2. 启动新配置的服务
```bash
./dev.sh start infra
```

### 3. 验证Redis连接
```bash
redis-cli -h localhost -p 6380 -a bklite_redis_pass ping
# 应返回: PONG
```

### 4. 查看端口映射
```bash
docker ps | grep redis
# 应显示: 0.0.0.0:6380->6379/tcp
```

## 注意事项

1. **端口说明**:
   - 宿主机端口: 6380（从外部访问Redis使用此端口）
   - 容器内部端口: 6379（容器内部Redis仍使用默认端口）

2. **影响范围**:
   - Server应用的Redis缓存连接
   - Celery消息队列和结果后端
   - 所有使用Redis的本地开发服务

3. **生产环境**: 此修改仅影响本地开发环境（docker-compose.dev.yml），生产环境配置不受影响。

4. **其他服务**: 如果有其他服务也需要连接Redis，需要相应更新其配置文件中的端口号。

## 相关文件参考
- Docker Compose配置: `docker-compose.dev.yml`
- Server环境配置: `server/.env.dev`, `server/.env`
- 开发脚本: `dev.sh`
