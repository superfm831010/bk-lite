#!/bin/bash
#
# BlueKing Lite 采集器包初始化脚本
# 用途: 为采集器创建包版本记录（复用 Controller 包文件）
# 说明: Telegraf、Vector、NATS-Executor 等采集器的二进制文件都包含在 fusion-collectors 包中
#       但前端需要为每个采集器单独显示包版本，所以需要创建对应的 PackageVersion 记录
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
CONTAINER_NAME="bklite-server-prod"
POSTGRES_CONTAINER="bklite-postgres-prod"
CONTROLLER_PACKAGE_FILE="fusion-collectors-linux-amd64.zip"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}BlueKing Lite 采集器包初始化脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 Controller 包是否存在
check_controller_package() {
    echo -e "${BLUE}[检查]${NC} 检查 Controller 包是否已上传..."

    local count=$(docker exec ${POSTGRES_CONTAINER} env PGPASSWORD=bklite psql -U postgres -d bklite -t -c \
        "SELECT COUNT(*) FROM node_mgmt_packageversion WHERE type='controller' AND object='Controller';" | tr -d ' ')

    if [ "$count" -eq 0 ]; then
        echo -e "${RED}错误: Controller 包尚未上传${NC}"
        echo -e "${YELLOW}请先运行: ./init-probe-packages.sh --auto${NC}"
        exit 1
    fi

    echo -e "${GREEN}✓${NC} Controller 包已存在"
}

# 为采集器创建包记录
create_collector_package() {
    local os=$1
    local object=$2
    local version=$3
    local package_name=$4

    echo -e "${BLUE}[创建]${NC} ${object} (${os}) 包记录..."

    # 检查是否已存在
    local exists=$(docker exec ${POSTGRES_CONTAINER} env PGPASSWORD=bklite psql -U postgres -d bklite -t -c \
        "SELECT COUNT(*) FROM node_mgmt_packageversion WHERE os='${os}' AND object='${object}' AND version='${version}';" | tr -d ' ')

    if [ "$exists" -gt 0 ]; then
        echo -e "${YELLOW}  已存在，跳过${NC}"
        return 0
    fi

    # 插入记录（复用 Controller 包文件）
    docker exec ${POSTGRES_CONTAINER} env PGPASSWORD=bklite psql -U postgres -d bklite -c \
        "INSERT INTO node_mgmt_packageversion (type, os, object, version, name, description, created_by, updated_by, domain, updated_by_domain, created_at, updated_at)
         VALUES ('collector', '${os}', '${object}', '${version}', '${package_name}', '采集器包（包含在 fusion-collectors 中）', 'system', 'system', 'domain.com', 'domain.com', NOW(), NOW());" > /dev/null

    echo -e "${GREEN}  ✓ 创建成功${NC}"
}

# 主函数
main() {
    # 检查环境
    echo -e "${BLUE}[环境检查]${NC}"
    if ! docker ps --format '{{.Names}}' | grep -q "^${POSTGRES_CONTAINER}$"; then
        echo -e "${RED}错误: 容器 ${POSTGRES_CONTAINER} 未运行${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ 环境检查通过${NC}"
    echo ""

    # 检查 Controller 包
    check_controller_package
    echo ""

    # 为主要采集器创建包记录
    echo -e "${BLUE}[初始化采集器包]${NC}"
    echo ""

    # Linux 采集器
    create_collector_package "linux" "Telegraf" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"
    create_collector_package "linux" "Vector" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"
    create_collector_package "linux" "NATS-Executor" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"
    create_collector_package "linux" "Metricbeat" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"
    create_collector_package "linux" "Filebeat" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"
    create_collector_package "linux" "Packetbeat" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"
    create_collector_package "linux" "Auditbeat" "1.0.0" "${CONTROLLER_PACKAGE_FILE}"

    echo ""

    # Windows 采集器（如果需要）
    # create_collector_package "windows" "Telegraf" "1.0.0" "fusion-collectors-windows-amd64.zip"
    # create_collector_package "windows" "NATS-Executor" "1.0.0" "fusion-collectors-windows-amd64.zip"

    # 验证结果
    echo -e "${BLUE}[验证]${NC} 检查采集器包记录..."
    docker exec ${POSTGRES_CONTAINER} env PGPASSWORD=bklite psql -U postgres -d bklite -c \
        "SELECT type, os, object, version, name FROM node_mgmt_packageversion ORDER BY type, os, object;"

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}采集器包初始化完成！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}说明：${NC}"
    echo -e "1. 采集器的二进制文件都包含在 Controller 包中："
    echo -e "   - /opt/fusion-collectors/bin/telegraf"
    echo -e "   - /opt/fusion-collectors/bin/vector"
    echo -e "   - /opt/fusion-collectors/bin/nats-executor"
    echo ""
    echo -e "2. 为每个采集器创建的包记录指向同一个文件"
    echo -e "   这样前端可以为每个采集器显示版本信息"
    echo ""
    echo -e "3. 现在您可以在 Web 界面查看采集器的包列表："
    echo -e "   ${YELLOW}节点管理 -> 探针管理 -> 采集器 -> 点击任一采集器${NC}"
    echo ""
}

# 执行主函数
main "$@"
