# Blueking Lite 本地开发环境指南

本文档提供 Blueking Lite 本地开发环境的完整搭建和使用指南。

## 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [开发工具安装](#开发工具安装)
- [使用 dev.sh 管理脚本](#使用-devsh-管理脚本)
- [手动操作指南](#手动操作指南)
- [常见问题](#常见问题)
- [开发工作流](#开发工作流)

---

## 系统要求

### 必需软件

| 软件 | 版本要求 | 用途 |
|------|---------|------|
| Docker | >= 20.10.23 | 运行基础设施服务 |
| Docker Compose | >= 2.27.0 | 编排 Docker 服务 |
| Python | >= 3.12 | Server 后端开发 |
| Node.js | >= 18.0 | Web 前端开发 |
| pnpm | 最新版 | 前端包管理器 |
| uv | 最新版 | Python 包管理器 |

### 推荐软件

- Git >= 2.0
- Visual Studio Code 或其他代码编辑器
- Postman 或 curl (API 测试)

### 硬件要求

- CPU: 4 核心及以上
- 内存: 8GB 及以上 (推荐 16GB)
- 硬盘: 20GB 可用空间

---

## 快速开始

### 一键启动开发环境

```bash
# 1. 克隆代码仓库
git clone https://github.com/TencentBlueKing/bk-lite.git
cd bk-lite

# 2. 检查环境
./dev.sh check

# 3. 安装依赖
./dev.sh install

# 4. 启动基础设施
./dev.sh start infra

# 5. 初始化数据库
./dev.sh db init

# 6. 启动所有服务
./dev.sh start all

# 7. 查看状态
./dev.sh status
```

完成后访问：
- **Web 前端**: http://localhost:3000
- **Server API**: http://localhost:8001
- **管理员账号**: admin / password

---

## 开发工具安装

### Python 3.12+ 和 uv

#### 使用 pyenv (推荐)

```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 安装 Python 3.12
pyenv install 3.12
pyenv global 3.12

# 验证
python3 --version
```

#### 安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证
uv --version
```

### Node.js 18+ 和 pnpm

#### 使用 nvm (推荐)

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 安装 Node.js
nvm install 18
nvm use 18

# 验证
node --version
```

#### 安装 pnpm

```bash
npm install -g pnpm

# 验证
pnpm --version
```

### Docker 和 Docker Compose

参考官方文档：https://docs.docker.com/get-docker/

---

## 使用 dev.sh 管理脚本

`dev.sh` 是统一的开发环境管理工具，提供以下功能：

### 环境检查

```bash
# 检查所有必需工具是否已安装
./dev.sh check
```

### 安装依赖

```bash
# 安装 Server 和 Web 的所有依赖
./dev.sh install
```

### 服务管理

```bash
# 启动服务
./dev.sh start all          # 启动所有服务（基础设施 + Server + Web）
./dev.sh start infra        # 只启动基础设施（Docker）
./dev.sh start server       # 只启动 Server
./dev.sh start web          # 只启动 Web

# 停止服务
./dev.sh stop all           # 停止所有服务
./dev.sh stop server        # 停止 Server
./dev.sh stop web           # 停止 Web
./dev.sh stop infra         # 停止基础设施

# 重启服务
./dev.sh restart all        # 重启所有服务
./dev.sh restart server     # 重启 Server
./dev.sh restart web        # 重启 Web

# 查看状态
./dev.sh status             # 查看所有服务状态
```

### 查看日志

```bash
# 查看 Server 日志
./dev.sh logs server

# 查看 Web 日志
./dev.sh logs web

# 查看基础设施日志
./dev.sh logs infra

# 查看特定基础设施服务日志
./dev.sh logs infra postgres
./dev.sh logs infra redis
```

### 数据库管理

```bash
# 初始化数据库（首次使用）
./dev.sh db init

# 运行数据库迁移
./dev.sh db migrate

# 重置数据库（警告：会删除所有数据）
./dev.sh db reset

# 打开数据库 Shell
./dev.sh db shell
```

### Git 管理

```bash
# 配置 Git 凭证和远程仓库
./dev.sh git-setup

# 提交并推送代码到 GitHub
./dev.sh git-push
```

### 查看帮助

```bash
./dev.sh help
```

---

## 手动操作指南

如果您不使用 `dev.sh`，也可以手动管理各个服务。

### 启动基础设施

```bash
# 启动所有基础设施服务
docker compose -f docker-compose.dev.yml up -d

# 查看状态
docker compose -f docker-compose.dev.yml ps

# 查看日志
docker compose -f docker-compose.dev.yml logs -f

# 停止服务
docker compose -f docker-compose.dev.yml stop

# 删除服务和数据
docker compose -f docker-compose.dev.yml down -v
```

### Server 开发

```bash
cd server

# 安装依赖
uv sync --all-groups --all-extras

# 配置环境变量
cp .env.dev .env
# 根据需要编辑 .env

# 数据库迁移
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py createcachetable django_cache

# 初始化数据
uv run python manage.py init_realm_resource
uv run python manage.py init_login_settings
uv run python manage.py create_user admin password --email=admin@bklite.net --is_superuser
uv run python manage.py model_init
uv run python manage.py plugin_init
uv run python manage.py node_init
uv run python manage.py log_init
uv run python manage.py init_bot
uv run python manage.py init_channel
uv run python manage.py init_llm
uv run python manage.py create_builtin_rules --update

# 启动开发服务器
uv run uvicorn asgi:application --host 0.0.0.0 --port 8001 --reload

# 启动 Celery (新终端)
uv run celery -A apps.core.celery worker -B --loglevel=info --pool threads

# Django Shell
uv run python manage.py shell_plus

# 运行测试
uv run pytest
```

### Web 开发

```bash
cd web

# 安装依赖
pnpm install

# 配置环境变量
cp .env.local.dev .env.local
# 根据需要编辑 .env.local

# 启动开发服务器
pnpm dev

# 类型检查
pnpm type-check

# 代码检查
pnpm lint

# 构建生产版本
pnpm build

# 启动 Storybook
pnpm storybook
```

---

## 常见问题

### 1. 端口冲突

**问题**: 启动服务时提示端口已被占用

**解决方案**:
```bash
# 查看端口占用情况
lsof -i :3000    # Web
lsof -i :8001    # Server
lsof -i :5432    # PostgreSQL
lsof -i :6379    # Redis

# 杀掉占用端口的进程
kill -9 <PID>

# 或者修改配置文件中的端口
```

### 2. Python 版本过低

**问题**: Server 需要 Python 3.12+，但系统版本过低

**解决方案**:
```bash
# 使用 pyenv 安装多个 Python 版本
pyenv install 3.12
pyenv local 3.12

# 或者使用 Python 虚拟环境
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. 数据库连接失败

**问题**: Server 无法连接到 PostgreSQL

**解决方案**:
```bash
# 检查 PostgreSQL 容器是否运行
docker compose -f docker-compose.dev.yml ps postgres

# 检查数据库日志
docker compose -f docker-compose.dev.yml logs postgres

# 重启数据库
docker compose -f docker-compose.dev.yml restart postgres

# 检查 server/.env 中的数据库配置
```

### 4. pnpm 安装依赖失败

**问题**: Web 依赖安装失败

**解决方案**:
```bash
cd web

# 清理缓存
pnpm store prune

# 删除 node_modules 和 lockfile
rm -rf node_modules pnpm-lock.yaml

# 重新安装
pnpm install
```

### 5. Docker 资源不足

**问题**: Docker 容器运行缓慢或崩溃

**解决方案**:
- 在 Docker Desktop 中增加内存限制（至少 8GB）
- 清理未使用的 Docker 资源：
  ```bash
  docker system prune -a
  docker volume prune
  ```

### 6. 权限问题

**问题**: 运行脚本提示权限不足

**解决方案**:
```bash
# 给脚本添加执行权限
chmod +x dev.sh

# 确保 Docker 命令不需要 sudo
sudo usermod -aG docker $USER
# 重新登录生效
```

---

## 开发工作流

### 日常开发流程

```bash
# 1. 拉取最新代码
git pull origin master

# 2. 启动开发环境
./dev.sh start all

# 3. 开始开发
#    - Server 代码修改会自动重载 (uvicorn --reload)
#    - Web 代码修改会热更新 (Next.js HMR)

# 4. 修改数据库模型后
cd server
uv run python manage.py makemigrations
uv run python manage.py migrate

# 5. 前端添加新依赖
cd web
pnpm add <package-name>

# 6. 后端添加新依赖
cd server
uv add <package-name>

# 7. 提交代码
git add .
git commit -m "feat: 添加新功能"

# 8. 推送到 GitHub
./dev.sh git-push
```

### 调试技巧

#### Server 调试

```bash
# 使用 Django Shell
./dev.sh db shell
# 或
cd server && uv run python manage.py shell_plus

# 查看实时日志
./dev.sh logs server

# 查看 SQL 查询
# 在 server/.env 中设置: DEBUG=True
# Django Debug Toolbar 会自动启用
```

#### Web 调试

```bash
# 查看实时日志
./dev.sh logs web

# 使用 React DevTools
# 浏览器中安装 React DevTools 扩展

# 查看网络请求
# 浏览器开发者工具 -> Network 标签
```

### 测试

```bash
# Server 单元测试
cd server
uv run pytest

# Server 代码覆盖率
uv run pytest --cov

# Web 组件测试 (使用 Storybook)
cd web
pnpm storybook
```

---

## 服务访问地址

| 服务 | 地址 | 用途 |
|-----|------|------|
| Web 前端 | http://localhost:3000 | 用户界面 |
| Server API | http://localhost:8001 | 后端 API |
| PostgreSQL | localhost:5432 | 主数据库 |
| Redis | localhost:6379 | 缓存 |
| MinIO Console | http://localhost:9001 | 对象存储管理 |
| MLflow | http://localhost:5000 | ML 实验跟踪 |
| Victoria Metrics | http://localhost:8428 | 监控数据 |
| Victoria Logs | http://localhost:9428 | 日志存储 |
| FalkorDB | localhost:6479 | 图数据库 |
| NATS | localhost:4222 | 消息队列 |

### 默认账号密码

| 服务 | 用户名 | 密码 |
|-----|--------|------|
| BKLite 管理员 | admin | password |
| PostgreSQL | postgres | bklite_dev_pass |
| Redis | - | bklite_redis_pass |
| MinIO | minioadmin | minioadmin123 |
| FalkorDB | - | bklite_falkordb_pass |

---

## 项目结构

```
bk-lite/
├── dev.sh                      # 开发环境管理脚本
├── docker-compose.dev.yml      # Docker Compose 配置
├── DEVELOPMENT.md              # 本文档
├── CLAUDE.md                   # Claude Code AI 助手指南
├── server/                     # Django 后端
│   ├── .env.dev                # 开发环境配置模板
│   ├── apps/                   # 应用模块
│   ├── config/                 # Django 配置
│   └── manage.py               # Django 管理命令
├── web/                        # Next.js 前端
│   ├── .env.local.dev          # 开发环境配置模板
│   ├── src/                    # 源代码
│   └── package.json            # 依赖配置
├── pilot/                      # Rasa AI 助手
├── metis/                      # ML/AI 服务
├── neco/                       # 共享库
└── agents/                     # 数据采集 Agent
```

---

## 获取帮助

- **文档**: 查看 [README.md](./Readme.md) 和 [CLAUDE.md](./CLAUDE.md)
- **Issues**: https://github.com/TencentBlueKing/bk-lite/issues
- **讨论**: https://github.com/TencentBlueKing/bk-lite/discussions

---

## 贡献指南

请参考 [CONTRIBUTING.md](./docs/CONTRIBUTING.md)

---

**Happy Coding! 🚀**
