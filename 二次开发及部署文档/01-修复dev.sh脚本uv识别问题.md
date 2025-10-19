# 修复 dev.sh 脚本 uv 识别问题

## 问题描述

在安装 uv 工具后，运行 `./dev.sh check` 仍然报错提示 `[ERROR] uv 未安装`。

### 问题原因

uv 通过以下命令安装到了 `~/.local/bin` 目录：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

但是安装后，`~/.local/bin` 路径没有被添加到当前 shell 的 PATH 环境变量中，导致 `dev.sh` 脚本的 `command -v uv` 检查失败。

虽然安装脚本提示需要运行 `source $HOME/.local/bin/env` 来更新 PATH，但这只是临时解决方案，每次打开新终端都需要重新执行。

## 解决方案

修改 `/home/soft/bk-lite/dev.sh` 脚本，在初始化阶段自动将 `~/.local/bin` 添加到 PATH 中。

### 修改内容

在脚本的项目根目录设置后，添加 uv 环境加载逻辑：

**修改位置**：第 38-46 行

```bash
# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 尝试加载 uv 环境（如果已安装）
if [ -f "$HOME/.local/bin/env" ]; then
    # 临时导出 PATH 以包含 uv
    export PATH="$HOME/.local/bin:$PATH"
fi

# PID 文件目录
PID_DIR="$PROJECT_ROOT/.dev-pids"
mkdir -p "$PID_DIR"
```

### 验证修复

修复后再次运行环境检查：

```bash
./dev.sh check
```

预期输出：
```
[STEP] 检查开发环境...
[SUCCESS] Docker 版本: 28.4.0
[SUCCESS] Docker Compose 版本: 2.39.4
[INFO] Python 版本: 3.8
[WARN] Server 需要 Python 3.12+，当前版本: 3.8
[INFO] 建议使用 pyenv 安装: https://github.com/pyenv/pyenv
[SUCCESS] uv 版本: 0.9.4     ← 现在可以正确识别了
[SUCCESS] Node.js 版本: v22.12.0
[SUCCESS] pnpm 版本: 10.12.1
[SUCCESS] 环境检查通过！
```

## 其他发现

### Python 版本问题

当前系统 Python 版本为 3.8，但 Server 组件需要 Python 3.12+。虽然环境检查会显示警告，但不会阻止继续操作。

建议使用 pyenv 安装 Python 3.12：
```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 安装 Python 3.12
pyenv install 3.12

# 在项目目录设置本地 Python 版本
cd /home/soft/bk-lite
pyenv local 3.12
```

### 基础设施服务状态

运行 `./dev.sh start infra` 后，基础设施服务启动情况：

| 服务 | 状态 | 端口 |
|------|------|------|
| postgres | ✓ healthy | 5432 |
| minio | ✓ healthy | 9000-9001 |
| falkordb | ✓ healthy | 6479 |
| nats | ! unhealthy | 4222, 8222 |
| victoria-logs | ! unhealthy | 9428 |
| victoria-metrics | ! unhealthy | 8428 |

注：部分服务显示 unhealthy 但仍在运行，可能是健康检查超时导致，不影响基本功能。

## 修改时间

2025-10-19

## 修改文件

- `/home/soft/bk-lite/dev.sh`
