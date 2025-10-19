# dev.sh 脚本颜色输出修复记录

**修复时间:** 2025-10-19
**问题类型:** 终端输出显示异常
**影响范围:** dev.sh 管理脚本

## 问题描述

在运行 `./dev.sh` 脚本时，终端输出显示 ANSI 转义序列的原始字符，而不是显示为颜色。例如：

```
\033[0;36mBlueking Lite 本地开发环境管理工具\033[0m
\033[1;33m环境管理:\033[0m
```

导致输出难以阅读，用户体验较差。

## 问题原因分析

1. **终端兼容性问题**: 某些终端或环境不支持 ANSI 颜色代码
2. **echo -e 不可靠**: `echo -e` 在不同 shell 和环境中的行为可能不一致
3. **缺少终端检测**: 脚本没有检测终端是否支持颜色输出

## 解决方案

### 1. 添加终端颜色支持检测

在脚本开头添加终端检测逻辑，只在支持颜色的终端中启用颜色：

```bash
# 检测终端是否支持颜色
if [ -t 1 ] && command -v tput &> /dev/null && tput colors &> /dev/null && [ "$(tput colors)" -ge 8 ]; then
    USE_COLOR=true
else
    USE_COLOR=false
fi

# 允许通过环境变量禁用颜色
if [ "${NO_COLOR:-}" = "1" ] || [ "${TERM:-}" = "dumb" ]; then
    USE_COLOR=false
fi
```

检测条件说明：
- `[ -t 1 ]`: 检查标准输出是否连接到终端
- `command -v tput`: 检查 tput 命令是否可用
- `tput colors`: 获取终端支持的颜色数
- `[ "$(tput colors)" -ge 8 ]`: 至少支持 8 种颜色

### 2. 条件化颜色定义

根据检测结果决定是否使用颜色：

```bash
if [ "$USE_COLOR" = true ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    MAGENTA=''
    CYAN=''
    NC=''
fi
```

### 3. 使用 printf 替代 echo -e

将所有日志函数中的 `echo -e` 替换为更可靠的 `printf`：

**修改前:**
```bash
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}
```

**修改后:**
```bash
log_info() {
    printf "${BLUE}[INFO]${NC} %s\n" "$1"
}
```

### 4. 修复 show_status 和 show_help 函数

同样使用 `printf` 来输出带颜色的文本：

```bash
# show_status 中的修改
printf "${CYAN}基础设施服务:${NC}\n"
printf "${GREEN}● 运行中${NC} (PID: %s) - http://localhost:8001\n" "$(cat $PID_DIR/server.pid)"

# show_help 中的修改
printf "${CYAN}Blueking Lite 本地开发环境管理工具${NC}\n"
printf "${YELLOW}环境管理:${NC}\n"
```

## 修改文件

- `/home/soft/bk-lite/dev.sh`

## 修改内容总结

1. **第 7-36 行**: 添加终端颜色检测和条件化颜色定义
2. **第 54-72 行**: 将日志函数的 `echo -e` 改为 `printf`
3. **第 416-443 行**: 修复 `show_status` 函数中的颜色输出
4. **第 562-611 行**: 修复 `show_help` 函数中的颜色输出

## 验证结果

修复后运行 `./dev.sh help`，输出正常显示，没有乱码：

```
Blueking Lite 本地开发环境管理工具

用法:
    ./dev.sh <command> [options]

环境管理:
    check               检查开发环境是否就绪
    install             安装所有依赖 (Server + Web)
...
```

## 额外功能

修复后的脚本支持以下特性：

1. **自动检测**: 自动检测终端是否支持颜色
2. **环境变量控制**: 可通过 `NO_COLOR=1` 环境变量禁用颜色
3. **管道友好**: 输出重定向到文件或管道时自动禁用颜色
4. **更好的兼容性**: 使用 `printf` 确保跨平台兼容性

## 使用建议

### 正常使用
```bash
./dev.sh help
./dev.sh status
```

### 禁用颜色输出
```bash
NO_COLOR=1 ./dev.sh help
```

### 输出到文件（自动禁用颜色）
```bash
./dev.sh status > status.txt
```

## 技术要点

1. **printf vs echo -e**:
   - `printf` 是 POSIX 标准，行为一致
   - `echo -e` 在不同 shell 中可能有差异
   - `printf` 需要显式添加换行符 `\n`

2. **终端检测**:
   - `[ -t 1 ]` 是标准方法检测是否为交互式终端
   - `tput colors` 可获取终端颜色能力
   - 支持 `NO_COLOR` 环境变量是现代最佳实践

3. **颜色代码**:
   - `\033[0;31m` - 红色
   - `\033[0;32m` - 绿色
   - `\033[1;33m` - 黄色（粗体）
   - `\033[0;34m` - 蓝色
   - `\033[0;35m` - 品红色
   - `\033[0;36m` - 青色
   - `\033[0m` - 重置

## 参考资料

- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [NO_COLOR Standard](https://no-color.org/)
- [Bash Printf Command](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html#index-printf)

## 后续优化建议

1. 考虑使用 [tput](https://man7.org/linux/man-pages/man1/tput.1.html) 命令生成颜色代码，更加可移植
2. 可以添加更多颜色选项（如粗体、下划线等）
3. 考虑支持颜色主题配置文件

## 总结

通过添加终端检测和使用更可靠的 `printf` 命令，成功解决了 dev.sh 脚本在某些环境下的颜色输出显示异常问题。修复后的脚本在各种终端环境下都能正常工作，提升了用户体验。
