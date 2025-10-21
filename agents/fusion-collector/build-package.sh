#!/bin/bash
#
# Fusion Collector 探针打包脚本
# 用途: 将 fusion-collector 打包为可部署的 zip 文件
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 版本号（可通过参数传入）
VERSION="${1:-1.0.0}"

# 输出目录
OUTPUT_DIR="${SCRIPT_DIR}/build"
PACKAGE_NAME="fusion-collectors"
PACKAGE_FILE="${OUTPUT_DIR}/fusion-collectors-${VERSION}.zip"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Fusion Collector 探针打包脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "版本号: ${YELLOW}${VERSION}${NC}"
echo -e "输出文件: ${YELLOW}${PACKAGE_FILE}${NC}"
echo ""

# 创建输出目录
mkdir -p "${OUTPUT_DIR}"

# 创建临时打包目录
TEMP_DIR="${OUTPUT_DIR}/temp-${PACKAGE_NAME}"
rm -rf "${TEMP_DIR}"
mkdir -p "${TEMP_DIR}/${PACKAGE_NAME}"

echo -e "${GREEN}[1/5]${NC} 准备打包目录..."

# 复制必要的文件
echo -e "${GREEN}[2/5]${NC} 复制文件..."

# 复制 misc 目录（安装脚本等）
if [ -d "misc" ]; then
    echo "  - 复制 misc/ (安装脚本、配置文件)"
    cp -r misc/* "${TEMP_DIR}/${PACKAGE_NAME}/"
else
    echo -e "${RED}  错误: misc/ 目录不存在${NC}"
    exit 1
fi

# 复制 agent 目录
if [ -d "agent" ]; then
    echo "  - 复制 agent/ (核心探针程序)"
    cp -r agent "${TEMP_DIR}/${PACKAGE_NAME}/"
else
    echo -e "${YELLOW}  警告: agent/ 目录不存在${NC}"
fi

# 复制 telegraf 目录
if [ -d "telegraf" ]; then
    echo "  - 复制 telegraf/ (Telegraf 配置)"
    cp -r telegraf "${TEMP_DIR}/${PACKAGE_NAME}/"
else
    echo -e "${YELLOW}  警告: telegraf/ 目录不存在${NC}"
fi

# 复制 support-files 目录
if [ -d "support-files" ]; then
    echo "  - 复制 support-files/ (支持文件)"
    cp -r support-files "${TEMP_DIR}/${PACKAGE_NAME}/"
else
    echo -e "${YELLOW}  警告: support-files/ 目录不存在${NC}"
fi

# 设置脚本执行权限
echo -e "${GREEN}[3/5]${NC} 设置脚本执行权限..."
find "${TEMP_DIR}/${PACKAGE_NAME}" -name "*.sh" -exec chmod +x {} \;

# 创建版本信息文件
echo -e "${GREEN}[4/5]${NC} 创建版本信息文件..."
cat > "${TEMP_DIR}/${PACKAGE_NAME}/VERSION" <<EOF
{
  "name": "fusion-collectors",
  "version": "${VERSION}",
  "type": "controller",
  "os": "linux",
  "build_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "description": "Fusion Collector - BlueKing Lite 探针控制器"
}
EOF

# 打包
echo -e "${GREEN}[5/5]${NC} 打包文件..."
cd "${TEMP_DIR}"

# 检查是否有 zip 命令，如果没有则使用 tar
if command -v zip &> /dev/null; then
    echo "  使用 zip 格式打包..."
    PACKAGE_FILE="${OUTPUT_DIR}/fusion-collectors-${VERSION}.zip"
    zip -r "${PACKAGE_FILE}" "${PACKAGE_NAME}" > /dev/null
else
    echo "  使用 tar.gz 格式打包..."
    PACKAGE_FILE="${OUTPUT_DIR}/fusion-collectors-${VERSION}.tar.gz"
    tar czf "${PACKAGE_FILE}" "${PACKAGE_NAME}"
fi

# 清理临时目录
rm -rf "${TEMP_DIR}"

# 计算文件大小
FILE_SIZE=$(du -h "${PACKAGE_FILE}" | cut -f1)

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "输出文件: ${YELLOW}${PACKAGE_FILE}${NC}"
echo -e "文件大小: ${YELLOW}${FILE_SIZE}${NC}"
echo ""
echo -e "${GREEN}下一步操作：${NC}"
echo -e "1. 将包文件上传到 BKLite 系统："
echo -e "   ${YELLOW}cd /home/soft/bk-lite/server${NC}"
echo -e "   ${YELLOW}docker exec -it bklite-server-prod python manage.py controller_package_init \\${NC}"
echo -e "   ${YELLOW}     --os linux \\${NC}"
echo -e "   ${YELLOW}     --object Controller \\${NC}"
echo -e "   ${YELLOW}     --pk_version ${VERSION} \\${NC}"
echo -e "   ${YELLOW}     --file_path ${PACKAGE_FILE}${NC}"
echo ""
echo -e "2. 或通过 Web 界面上传："
echo -e "   ${YELLOW}节点管理 -> 探针管理 -> 控制器 -> 上传包${NC}"
echo ""
