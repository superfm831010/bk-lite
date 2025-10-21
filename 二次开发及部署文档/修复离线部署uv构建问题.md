# 修复离线部署时 server 容器 uv 构建问题

## 问题描述

在内网离线环境部署时，server 容器启动失败，所有 supervisor 管理的进程都无法启动，日志显示 uv 尝试从 PyPI 下载 `setuptools` 和 `wheel` 包失败。

### 错误日志

```
bklite-server-prod  |    Building server @ file:///apps
bklite-server-prod  |   × Failed to build `server @ file:///apps`
bklite-server-prod  |   ├─? Failed to resolve requirements from `build-system.requires`
bklite-server-prod  |   ├─? No solution found when resolving: `setuptools>=45`, `wheel`
bklite-server-prod  |   ├─? Failed to fetch: `https://pypi.org/simple/setuptools/`
bklite-server-prod  |   ├─? Request failed after 3 retries
bklite-server-prod  |   ├─? error sending request for url (https://pypi.org/simple/setuptools/)
bklite-server-prod  |   ├─? client error (Connect)
bklite-server-prod  |   ├─? dns error
bklite-server-prod  |   ╰─? failed to lookup address information: Temporary failure in name resolution
```

## 问题原因

### 根本原因

1. **pyproject.toml 定义了构建依赖**：
   ```toml
   [build-system]
   requires = ["setuptools>=45", "wheel"]
   build-backend = "setuptools.build_meta"
   ```

2. **supervisor 配置使用 `uv run` 命令**：
   - `app.conf`: `uv run uvicorn ...`
   - `beat.conf`: `uv run celery ...`
   - `celery.conf`: `uv run celery ...`
   - `nats.conf`: `uv run python ...`

3. **uv run 行为**：
   - 当使用 `uv run` 启动命令时，uv 会检测到项目是一个可安装的包
   - uv 尝试构建项目包以确保所有依赖都可用
   - 构建过程需要下载 `setuptools` 和 `wheel`
   - 在离线环境中无法访问 PyPI，导致失败

### 为什么构建时没问题？

- 在构建镜像时（`RUN uv sync --all-groups`），环境可以访问网络
- 所有依赖包（包括 setuptools 和 wheel）都被正确安装到 `.venv` 目录
- 但运行时使用 `uv run` 会重新触发包构建检查

## 解决方案

### 修改思路

将 supervisor 配置中的 `uv run` 命令改为直接使用虚拟环境中的可执行文件，避免触发包构建过程。

### 修改文件

1. **server/support-files/release/supervisor/app.conf**
   ```diff
   - command=uv run uvicorn asgi:application --workers %(ENV_APP_WORKERS)s --host 0.0.0.0 --port 8000 --timeout-keep-alive 90 --backlog 2048
   + command=.venv/bin/uvicorn asgi:application --workers %(ENV_APP_WORKERS)s --host 0.0.0.0 --port 8000 --timeout-keep-alive 90 --backlog 2048
   ```

2. **server/support-files/release/supervisor/beat.conf**
   ```diff
   - command=uv run celery -A apps.core.celery beat --loglevel=info --scheduler django_celery_beat.schedulers.DatabaseScheduler
   + command=.venv/bin/celery -A apps.core.celery beat --loglevel=info --scheduler django_celery_beat.schedulers.DatabaseScheduler
   ```

3. **server/support-files/release/supervisor/celery.conf**
   ```diff
   - command=uv run celery -A apps.core.celery worker --loglevel=info --pool threads --concurrency=%(ENV_CELERY_CONCURRENCY)s
   + command=.venv/bin/celery -A apps.core.celery worker --loglevel=info --pool threads --concurrency=%(ENV_CELERY_CONCURRENCY)s
   ```

4. **server/support-files/release/supervisor/nats.conf**
   ```diff
   - command=uv run python manage.py nats_listener
   + command=.venv/bin/python manage.py nats_listener
   ```

### 实施步骤

1. **修改配置文件**：按上述修改所有 4 个 supervisor 配置文件

2. **重新构建镜像**：
   ```bash
   cd server
   docker build -f support-files/release/Dockerfile -t bklite/server:huangpu-v1.0 .
   ```

3. **导出镜像**：
   ```bash
   docker save bklite/server:huangpu-v1.0 -o /path/to/deploy-huangpu/images/bklite-server-huangpu-v1.0.tar
   ```

4. **测试部署**：
   ```bash
   cd deploy-huangpu
   docker compose down server
   docker compose up -d server
   docker logs -f bklite-server-prod
   ```

## 验证结果

### 成功标志

1. **启动日志正常**：
   - ✅ 没有 "Building server @ file:///apps" 消息
   - ✅ 没有 "Failed to fetch" 或 "pypi.org" 错误
   - ✅ 没有 DNS 解析失败

2. **所有进程正常启动**：
   ```
   2025-10-21 11:30:23,235 INFO success: app entered RUNNING state
   2025-10-21 11:30:23,235 INFO success: beat entered RUNNING state
   2025-10-21 11:30:23,235 INFO success: celery entered RUNNING state
   2025-10-21 11:30:23,235 INFO success: nats_00 entered RUNNING state
   2025-10-21 11:30:23,235 INFO success: nats_01 entered RUNNING state
   2025-10-21 11:30:23,235 INFO success: nats_02 entered RUNNING state
   2025-10-21 11:30:23,235 INFO success: nats_03 entered RUNNING state
   ```

3. **Uvicorn 正常运行**：
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```

4. **API 正常响应**：
   ```bash
   $ curl -s http://localhost:18001/api/v1/core/api/login_info/
   {"result": false, "message": "please provide Token"}
   ```

## 技术原理

### uv run vs 直接调用

- **uv run command**：
  - uv 会检查项目是否为可安装包（检查 pyproject.toml 中的 [project] 或 [build-system]）
  - 如果是，会尝试构建并安装到临时环境
  - 需要访问 PyPI 下载构建依赖

- **直接调用 .venv/bin/command**：
  - 直接使用构建时已安装的可执行文件
  - 不会触发包构建流程
  - 完全离线可用

### 为什么之前使用 uv run？

开发环境中使用 `uv run` 的优点：
- 自动管理虚拟环境
- 确保使用项目的 Python 环境
- 方便快捷

但在生产环境（特别是离线环境）中：
- 环境已经固定（Docker 容器）
- 不需要动态环境管理
- 直接调用更加可靠

## 影响范围

### 修改影响

- **仅影响生产环境镜像**：修改位于 `server/support-files/release/` 目录
- **不影响开发环境**：开发环境仍然可以使用 `make dev` 等命令
- **向后兼容**：对已有功能没有影响

### 需要更新的文件

- ✅ server/support-files/release/supervisor/app.conf
- ✅ server/support-files/release/supervisor/beat.conf
- ✅ server/support-files/release/supervisor/celery.conf
- ✅ server/support-files/release/supervisor/nats.conf
- ✅ deploy-huangpu/images/bklite-server-huangpu-v1.0.tar （重新导出）

## 注意事项

1. **镜像版本**：修改后需要重新构建镜像并更新版本标签
2. **离线部署**：确保导出的 tar 文件包含最新的修复
3. **测试验证**：在目标环境（银河麒麟 V10 SP3）进行完整测试

## 相关问题

### 与 shell 兼容性问题的关系

本问题与之前的 [修复部署脚本的 shell 兼容性问题](./修复部署脚本的shell兼容性问题.md) 是两个独立的问题：

- **Shell 兼容性**：deploy.sh 脚本在银河麒麟系统上无法找到 .secrets 文件
- **uv 构建问题**：server 容器在离线环境中无法启动服务

两个问题需要分别修复。

## 参考资料

- [uv 官方文档 - uv run](https://github.com/astral-sh/uv)
- [Python 包构建系统 - PEP 517](https://peps.python.org/pep-0517/)
- [Supervisor 配置文档](http://supervisord.org/configuration.html)

---

**修复日期**：2025-10-21
**修复版本**：v1.0
**测试环境**：Ubuntu 开发环境（模拟离线）
**目标环境**：银河麒麟 V10 SP3（内网离线）
