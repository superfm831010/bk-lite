# Docker 部署指南

本项目包含了完整的 Docker 配置，支持生产环境部署和开发环境运行。

## 文件说明

- `Dockerfile` - 生产环境多阶段构建配置
- `Dockerfile.dev` - 开发环境配置
- `docker-compose.yml` - Docker Compose 配置
- `nginx.conf` - 自定义 Nginx 配置
- `.dockerignore` - Docker 构建忽略文件

## 快速开始

### 生产环境部署

```bash
# 构建并启动生产环境
docker-compose up -d

# 访问应用
# http://localhost:3000
```

### 开发环境运行

```bash
# 启动开发环境
docker-compose --profile dev up docs-dev

# 访问开发服务器
# http://localhost:3001
```

## 手动构建

### 生产环境

```bash
# 构建生产镜像
docker build -t docs-site:latest .

# 运行生产容器
docker run -d -p 3000:80 --name docs-site docs-site:latest
```

### 开发环境

```bash
# 构建开发镜像
docker build -f Dockerfile.dev -t docs-site:dev .

# 运行开发容器（带文件监听）
docker run -d -p 3001:3000 -v $(pwd):/app -v /app/node_modules --name docs-site-dev docs-site:dev
```

## 镜像特性

### 生产镜像特性
- 多阶段构建，最小化镜像大小
- 使用 Nginx 作为 Web 服务器
- 启用 Gzip 压缩
- 静态资源缓存优化
- 支持 SPA 路由
- 健康检查端点 `/health`

### 开发镜像特性
- 热重载支持
- 文件监听
- 开发模式优化

## 环境变量

可以通过环境变量配置应用：

```bash
# 设置环境变量
docker run -e NODE_ENV=production -p 3000:80 docs-site:latest
```

## 健康检查

生产环境容器提供健康检查端点：

```bash
curl http://localhost:3000/health
```

## 日志查看

```bash
# 查看容器日志
docker logs docs-site

# 实时查看日志
docker logs -f docs-site
```

## 停止和清理

```bash
# 停止所有服务
docker-compose down

# 停止并删除卷
docker-compose down -v

# 清理镜像
docker rmi docs-site:latest docs-site:dev
```
