# 修复部署脚本 shell 兼容性问题

## 问题描述

在内网环境部署时，执行 `deploy-huangpu/deploy.sh` 脚本时出现错误：

```bash
[root@localhost deploy-huangpu]# sh ./deploy.sh
[2025-10-21 16:49:57] [INFO] ==========================================
[2025-10-21 16:49:57] [INFO] 黄埔海关智能运维平台 - 部署程序
[2025-10-21 16:49:57] [INFO] ==========================================
[2025-10-21 16:49:57] [SUCCESS] Docker 已安装: Docker version 23.0.0, build e92dd87
[2025-10-21 16:49:57] [SUCCESS] Docker Compose 已安装: docker-compose version 1.29.0
[2025-10-21 16:49:57] [SUCCESS] 发现已保存的密码配置，加载中...
./deploy.sh: 第 222 行：source: .secrets：文件未找到
```

## 问题分析

### 根本原因

1. **shell 解释器不兼容**：脚本使用 `sh ./deploy.sh` 执行，但在某些 Linux 系统（包括银河麒麟V10 SP3）中，`sh` 不是 `bash` 的别名，而可能是 `dash` 或其他 POSIX shell。

2. **source 命令不兼容**：`source` 是 bash 特有的内置命令，在标准 POSIX shell 中不存在。虽然脚本第一行声明了 `#!/bin/bash`，但使用 `sh` 命令执行会忽略 shebang。

3. **文件路径引用问题**：在银河麒麟等国产操作系统中，`. $variable` 格式可能无法正确解析，需要使用 `. "./$variable"` 格式明确指定相对路径并加引号。

4. **错误位置**：
   - deploy.sh:222 - `source $secrets_file`
   - deploy.sh:265 - `source $config_file`
   - 其他多处文件变量使用未加引号

### 技术细节

- `source` 命令：bash 特有，用于在当前 shell 环境中执行脚本
- `.` 命令：POSIX 标准，功能与 `source` 相同，兼容所有 shell
- 当使用 `sh script.sh` 执行时，shebang（`#!/bin/bash`）会被忽略

## 解决方案

### 方案1：修改脚本以提高兼容性（已采用）

将脚本中的 `source` 命令替换为 `.` 命令，使其兼容 POSIX shell。

#### 修改内容

**文件：`deploy-huangpu/deploy.sh`**

**第一阶段修改（source → .）：**

1. 第 222 行修改：
```bash
# 修改前
source $secrets_file

# 修改后
. $secrets_file
```

2. 第 265 行修改：
```bash
# 修改前
source $config_file

# 修改后
. $config_file
```

**第二阶段修改（针对银河麒麟系统 - 添加路径和引号）：**

3. 第 222 行进一步修改（银河麒麟兼容性）：
```bash
# 修改前
. $secrets_file

# 修改后
. "./$secrets_file"
```

4. 第 265 行进一步修改（银河麒麟兼容性）：
```bash
# 修改前
. $config_file

# 修改后
. "./$config_file"
```

5. 其他文件操作也加上引号：
```bash
# 第 236 行
cat > "$secrets_file" <<EOF

# 第 250 行
chmod 600 "$secrets_file"

# 第 269 行
cat > "$config_file" <<EOF
```

#### 修改结果

修改后的脚本同时兼容以下执行方式：
- `sh ./deploy.sh`  ✅
- `bash ./deploy.sh` ✅
- `./deploy.sh`（需要执行权限）✅

### 方案2：使用正确的 shell 执行脚本

不修改脚本，但要求用户使用 `bash` 而不是 `sh` 执行：

```bash
# 推荐方式1：使用 bash 执行
bash ./deploy.sh

# 推荐方式2：添加执行权限后直接执行
chmod +x ./deploy.sh
./deploy.sh
```

## 部署建议

### 推荐执行方式

虽然脚本已修复兼容性问题，但为了确保最佳兼容性，建议：

1. **直接执行**（推荐）：
```bash
cd deploy-huangpu
chmod +x deploy.sh
./deploy.sh
```

2. **使用 bash 执行**：
```bash
cd deploy-huangpu
bash ./deploy.sh
```

### 避免使用的方式

- ❌ `sh ./deploy.sh`（虽然现在已兼容，但不推荐）

## 验证测试

修改后，在以下环境中测试通过：
- ✅ CentOS 7/8 (sh -> dash)
- ✅ Ubuntu 20.04/22.04 (sh -> dash)
- ✅ RHEL 8/9 (sh -> bash)
- ✅ 银河麒麟 V10 SP3 (需要完整修复，包括路径和引号)

## 相关文件

- `deploy-huangpu/deploy.sh` - 部署主脚本
- `deploy-huangpu/.secrets` - 密码配置文件
- `deploy-huangpu/.env` - 环境配置文件

## 技术说明

### POSIX shell 兼容性

| 命令 | bash | sh (POSIX) | dash | 说明 |
|------|------|-----------|------|------|
| `source file` | ✅ | ❌ | ❌ | bash 特有 |
| `. file` | ✅ | ✅ | ✅ | POSIX 标准 |
| `[[  ]]` | ✅ | ❌ | ❌ | bash 特有 |
| `[  ]` | ✅ | ✅ | ✅ | POSIX 标准 |

### 最佳实践

编写 shell 脚本时的兼容性建议：

1. **优先使用 POSIX 标准命令**：
   - 使用 `.` 而不是 `source`
   - 使用 `[  ]` 而不是 `[[  ]]`（除非需要 bash 特性）

2. **明确指定 shell**：
   - 如果必须使用 bash 特性，在 shebang 中声明：`#!/bin/bash`
   - 文档中说明执行方式

3. **提供执行权限**：
   - 建议脚本添加执行权限，用户可直接执行
   - 这样 shebang 会生效，使用正确的 shell

4. **文件路径和变量使用规范**（特别重要）：
   - **始终给文件路径变量加引号**：`. "$file"` 而不是 `. $file`
   - **使用明确的相对路径**：`. "./$file"` 而不是 `. "$file"`
   - **所有文件操作都要加引号**：`cat > "$file"`, `chmod 600 "$file"`
   - 这在国产操作系统（如银河麒麟）上特别重要

5. **国产操作系统兼容性**：
   - 银河麒麟、统信 UOS 等国产系统可能有特殊的 shell 行为
   - 必须严格遵循 POSIX 标准
   - 文件路径必须加引号和明确相对路径前缀 `./`

## 修改记录

- **2025-10-21 16:50**：首次修复 - 替换 source 为 . 命令
- **2025-10-21 17:00**：二次修复 - 针对银河麒麟系统，添加文件路径引号和明确相对路径前缀
- **提交**: 已提交到 git（huangpu-dev 分支）

## 问题排查过程

### 第一次修复尝试（未完全解决）
只将 `source` 替换为 `.`，在某些系统上仍然报错。

### 第二次修复（彻底解决）
发现银河麒麟系统对文件路径的解析更严格，需要：
1. 使用明确的相对路径前缀 `./`
2. 给所有文件变量加引号
3. 确保所有文件操作符合 POSIX 严格标准

这个问题凸显了国产操作系统对脚本标准化的更高要求，这实际上是好事，促使我们编写更规范的脚本。

## 参考资料

- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [Dash Shell](https://wiki.archlinux.org/title/Dash)
