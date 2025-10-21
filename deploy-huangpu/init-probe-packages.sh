#!/bin/bash
#
# BlueKing Lite 探针包初始化脚本
# 用途: 在离线环境中初始化探针包到系统
# 作者: Claude Code
# 版本: 1.0.0
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 配置
CONTAINER_NAME="bklite-server-prod"
POSTGRES_CONTAINER="bklite-postgres-prod"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}BlueKing Lite 探针包初始化脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 Docker 是否运行
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker 未安装或未在 PATH 中${NC}"
        exit 1
    fi

    if ! docker ps &> /dev/null; then
        echo -e "${RED}错误: Docker 服务未运行或权限不足${NC}"
        exit 1
    fi
}

# 检查容器是否运行
check_container() {
    local container=$1
    if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo -e "${RED}错误: 容器 ${container} 未运行${NC}"
        echo -e "${YELLOW}提示: 请先启动 BlueKing Lite 服务${NC}"
        exit 1
    fi
}

# 检查探针包文件是否存在
check_probe_file() {
    local file=$1
    if [ ! -f "$file" ]; then
        echo -e "${RED}错误: 探针包文件不存在: ${file}${NC}"
        return 1
    fi
    echo -e "${GREEN}✓${NC} 找到探针包: ${file}"
    return 0
}

# 上传探针包
upload_probe_package() {
    local file_path=$1
    local file_name=$(basename "$file_path")
    local os=$2
    local object=$3
    local version=$4
    local type=$5

    echo ""
    echo -e "${BLUE}[上传探针包]${NC}"
    echo -e "  文件名: ${YELLOW}${file_name}${NC}"
    echo -e "  操作系统: ${YELLOW}${os}${NC}"
    echo -e "  对象类型: ${YELLOW}${object}${NC}"
    echo -e "  版本号: ${YELLOW}${version}${NC}"
    echo -e "  包类型: ${YELLOW}${type}${NC}"
    echo ""

    # 复制文件到容器
    echo -e "${BLUE}[1/3]${NC} 复制文件到容器..."
    docker cp "$file_path" "${CONTAINER_NAME}:/tmp/${file_name}"

    # 检查是否已存在
    echo -e "${BLUE}[2/3]${NC} 检查是否已存在相同版本..."
    local exists=$(docker exec ${POSTGRES_CONTAINER} env PGPASSWORD=bklite psql -U postgres -d bklite -t -c \
        "SELECT COUNT(*) FROM node_mgmt_packageversion WHERE os='${os}' AND object='${object}' AND version='${version}';")

    if [ $(echo $exists | tr -d ' ') -gt 0 ]; then
        echo -e "${YELLOW}  警告: 已存在相同版本的探针包，跳过上传${NC}"
        docker exec ${CONTAINER_NAME} rm -f "/tmp/${file_name}"
        return 0
    fi

    # 上传到系统
    echo -e "${BLUE}[3/3]${NC} 上传到 NATS Object Store..."
    local cmd="controller_package_init"
    if [ "$type" = "collector" ]; then
        cmd="collector_package_init"
    fi

    docker exec ${CONTAINER_NAME} bash -c \
        "cd /apps && source .venv/bin/activate && \
        python manage.py ${cmd} \
        --os ${os} \
        --object ${object} \
        --pk_version ${version} \
        --file_path /tmp/${file_name}" 2>&1 | grep -E "INFO|ERROR|WARNING" || true

    # 清理临时文件
    docker exec ${CONTAINER_NAME} rm -f "/tmp/${file_name}"

    echo -e "${GREEN}✓ 上传完成${NC}"
}

# 验证上传结果
verify_upload() {
    echo ""
    echo -e "${BLUE}[验证]${NC} 检查数据库记录..."
    docker exec ${POSTGRES_CONTAINER} env PGPASSWORD=bklite psql -U postgres -d bklite -c \
        "SELECT id, type, os, object, version, name FROM node_mgmt_packageversion ORDER BY created_at DESC LIMIT 5;"
}

# 显示使用说明
show_usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --auto              自动初始化当前目录下的所有探针包"
    echo "  --file <文件>       指定单个探针包文件"
    echo "  --os <系统>         操作系统 (默认: linux)"
    echo "  --object <对象>     包对象名称 (默认: Controller)"
    echo "  --version <版本>    版本号 (默认: 1.0.0)"
    echo "  --type <类型>       包类型 controller 或 collector (默认: controller)"
    echo "  -h, --help          显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --auto                           # 自动初始化"
    echo "  $0 --file fusion-collectors.zip     # 初始化指定文件"
    echo "  $0 --file xxx.zip --version 2.0.0   # 指定版本号"
}

# 自动初始化模式
auto_init() {
    echo -e "${GREEN}[自动初始化模式]${NC}"
    echo ""

    local count=0

    # 查找 Controller 包
    for file in fusion-collectors*.zip fusion-collectors*.tar.gz; do
        if check_probe_file "$file" 2>/dev/null; then
            upload_probe_package "$file" "linux" "Controller" "1.0.0" "controller"
            count=$((count + 1))
        fi
    done

    if [ $count -eq 0 ]; then
        echo -e "${YELLOW}警告: 未找到任何探针包文件${NC}"
        echo -e "${YELLOW}提示: 请将探针包文件放在 ${SCRIPT_DIR} 目录下${NC}"
        echo -e "${YELLOW}      支持的文件名格式: fusion-collectors*.zip 或 fusion-collectors*.tar.gz${NC}"
        return 1
    fi

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}已初始化 ${count} 个探针包${NC}"
    echo -e "${GREEN}========================================${NC}"
}

# 主函数
main() {
    # 解析参数
    local mode="auto"
    local file=""
    local os="linux"
    local object="Controller"
    local version="1.0.0"
    local type="controller"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --auto)
                mode="auto"
                shift
                ;;
            --file)
                mode="manual"
                file="$2"
                shift 2
                ;;
            --os)
                os="$2"
                shift 2
                ;;
            --object)
                object="$2"
                shift 2
                ;;
            --version)
                version="$2"
                shift 2
                ;;
            --type)
                type="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                echo -e "${RED}错误: 未知参数 $1${NC}"
                show_usage
                exit 1
                ;;
        esac
    done

    # 检查环境
    echo -e "${BLUE}[检查环境]${NC}"
    check_docker
    check_container "${CONTAINER_NAME}"
    check_container "${POSTGRES_CONTAINER}"
    echo -e "${GREEN}✓ 环境检查通过${NC}"
    echo ""

    # 执行初始化
    if [ "$mode" = "auto" ]; then
        auto_init
    else
        if [ -z "$file" ]; then
            echo -e "${RED}错误: 请指定文件 (--file)${NC}"
            exit 1
        fi
        if ! check_probe_file "$file"; then
            exit 1
        fi
        upload_probe_package "$file" "$os" "$object" "$version" "$type"
    fi

    # 验证结果
    verify_upload

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}探针包初始化完成！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}下一步操作：${NC}"
    echo -e "1. 访问 Web 界面查看探针包列表"
    echo -e "   ${YELLOW}节点管理 -> 探针管理 -> 控制器${NC}"
    echo ""
    echo -e "2. 或通过 API 查询："
    echo -e "   ${YELLOW}curl http://localhost:18001/api/v1/node_mgmt/api/package/${NC}"
    echo ""
}

# 执行主函数
main "$@"
