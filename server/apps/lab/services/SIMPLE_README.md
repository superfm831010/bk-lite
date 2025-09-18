# 🐳 Docker 容器编排 - MVP 版本

## 🎯 核心功能
- 启动/停止容器
- 同技术栈网络自动互通
- 日志查看和状态同步

## ⚙️ 配置

### 环境变量（可选）
```bash
# .env 文件
DOCKER_NETWORK_PREFIX=bk-lite
```

## 🚀 快速开始

### 1. 启动 MySQL 容器
```bash
POST /api/lab/infra-instances/
{
    "name": "lamp-mysql-01",
    "image": 1,
    "env_vars": {
        "MYSQL_ROOT_PASSWORD": "password123",
        "MYSQL_DATABASE": "app_db"
    },
    "port_mappings": {
        "3306": "33060"
    }
}

# 启动容器
POST /api/lab/infra-instances/{id}/start/
```

### 2. 启动 Apache 容器
```bash
POST /api/lab/infra-instances/
{
    "name": "lamp-apache-01",
    "image": 2,
    "port_mappings": {
        "80": "8080"
    }
}

# 启动容器
POST /api/lab/infra-instances/{id}/start/
```

### 3. 验证网络互通
```bash
# 两个容器在同一网络：bk-lite-lamp
# lamp-apache-01 可以通过 lamp-mysql-01:3306 访问数据库

docker network ls | grep bk-lite-lamp
docker exec lamp-apache-01 ping lamp-mysql-01
```

## 📋 API 接口

### 启动容器
```
POST /api/lab/infra-instances/{id}/start/
```

### 停止容器
```
POST /api/lab/infra-instances/{id}/stop/
```

### 查看日志
```
GET /api/lab/infra-instances/{id}/logs/?lines=100
```

### 同步状态
```
POST /api/lab/infra-instances/{id}/sync_status/
```

## 🌐 网络设计

### 网络命名规则
- 技术栈：`lamp`
- 网络名：`bk-lite-lamp`
- 容器1：`lamp-mysql-01`
- 容器2：`lamp-apache-01`

### 容器间通信
```bash
# 在 lamp-apache-01 中访问数据库
mysql -h lamp-mysql-01 -P 3306 -u root -p
```

## 🔧 技术栈示例

### LAMP 栈
- `lamp-apache-01` (Web服务器)
- `lamp-mysql-01` (数据库) 
- `lamp-php-01` (PHP处理器)

### Node.js + Redis 栈
- `nodejs-app-01` (应用服务器)
- `nodejs-redis-01` (缓存)

## 📝 注意事项

1. **容器名格式**: `{技术栈}-{服务}-{序号}`
2. **网络自动创建**: 首次启动时自动创建网络
3. **端口映射**: 容器端口映射到主机端口
4. **状态同步**: 使用 `sync_status` 获取最新状态

## 🐛 故障排除

### 容器启动失败
```bash
# 查看容器日志
GET /api/lab/infra-instances/{id}/logs/

# 检查 Docker 状态
docker ps -a
docker logs {container_name}
```

### 网络问题
```bash
# 查看网络
docker network ls
docker network inspect bk-lite-{stack_name}

# 测试连通性
docker exec {container1} ping {container2}
```