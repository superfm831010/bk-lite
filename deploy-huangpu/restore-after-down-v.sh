#!/bin/bash
#
# BlueKing Lite 数据丢失快速恢复脚本
# 用途: 在执行 docker-compose down -v 后恢复探针包数据
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

echo -e "${RED}========================================${NC}"
echo -e "${RED}⚠️  数据丢失快速恢复脚本${NC}"
echo -e "${RED}========================================${NC}"
echo ""
echo -e "${YELLOW}此脚本用于恢复因 'docker-compose down -v' 导致的数据丢失${NC}"
echo ""

# 检查是否真的需要恢复
check_need_restore() {
    echo -e "${BLUE}[检查]${NC} 检测数据是否丢失..."

    local pkg_count=$(docker exec bklite-postgres-prod env PGPASSWORD=bklite psql -U postgres -d bklite -t -c \
        "SELECT COUNT(*) FROM node_mgmt_packageversion;" 2>/dev/null | tr -d ' ')

    if [ -z "$pkg_count" ]; then
        echo -e "${RED}错误: 无法连接到数据库，请确保服务正在运行${NC}"
        exit 1
    fi

    if [ "$pkg_count" -gt 0 ]; then
        echo -e "${GREEN}✓${NC} 数据完整，探针包数量: ${pkg_count}"
        echo -e "${YELLOW}提示: 如果您确认需要重新初始化，请先清空数据库${NC}"
        read -p "是否继续执行恢复？(yes/no) " confirm
        if [ "$confirm" != "yes" ]; then
            echo "已取消"
            exit 0
        fi
    else
        echo -e "${YELLOW}⚠️  检测到探针包数据丢失 (数量: 0)${NC}"
        echo -e "${YELLOW}   开始自动恢复...${NC}"
    fi
}

# 显示影响说明
show_impact() {
    echo ""
    echo -e "${BLUE}[影响评估]${NC}"
    echo -e "${RED}以下数据已丢失：${NC}"
    echo -e "  - ❌ 探针包版本记录"
    echo -e "  - ❌ 已安装的节点记录"
    echo -e "  - ❌ 采集器安装状态"
    echo -e "  - ❌ 历史安装任务"
    echo -e "  - ❌ 自定义配置"
    echo ""
    echo -e "${GREEN}以下数据仍保留：${NC}"
    echo -e "  - ✅ 系统预置的采集器定义"
    echo -e "  - ✅ 系统预置的控制器定义"
    echo -e "  - ✅ 云区域配置"
    echo ""
}

# 执行恢复
perform_restore() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}开始恢复数据${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""

    # 1. 恢复控制器包
    echo -e "${BLUE}[步骤 1/3]${NC} 恢复控制器包..."
    if [ -f "./init-probe-packages.sh" ]; then
        ./init-probe-packages.sh --auto
    else
        echo -e "${RED}错误: init-probe-packages.sh 不存在${NC}"
        exit 1
    fi

    echo ""

    # 2. 恢复采集器包
    echo -e "${BLUE}[步骤 2/3]${NC} 恢复采集器包..."
    if [ -f "./init-collector-packages.sh" ]; then
        ./init-collector-packages.sh
    else
        echo -e "${RED}错误: init-collector-packages.sh 不存在${NC}"
        exit 1
    fi

    echo ""

    # 3. 验证恢复结果
    echo -e "${BLUE}[步骤 3/3]${NC} 验证恢复结果..."
    local pkg_count=$(docker exec bklite-postgres-prod env PGPASSWORD=bklite psql -U postgres -d bklite -t -c \
        "SELECT COUNT(*) FROM node_mgmt_packageversion;" | tr -d ' ')

    if [ "$pkg_count" -gt 0 ]; then
        echo -e "${GREEN}✓ 恢复成功！探针包数量: ${pkg_count}${NC}"
    else
        echo -e "${RED}✗ 恢复失败，请检查日志${NC}"
        exit 1
    fi
}

# 显示后续步骤
show_next_steps() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ 数据恢复完成${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}后续需要手动完成的步骤：${NC}"
    echo ""
    echo -e "${YELLOW}1. 验证 Web 界面${NC}"
    echo -e "   访问: http://<服务器IP>:8080"
    echo -e "   检查: 节点管理 -> 探针管理 -> 控制器"
    echo -e "   确认探针包列表显示正常"
    echo ""
    echo -e "${YELLOW}2. 重新安装探针到目标节点${NC}"
    echo -e "   - 之前安装的节点已失联"
    echo -e "   - 需要重新执行探针安装流程"
    echo -e "   - 或者在目标节点上重新运行安装脚本"
    echo ""
    echo -e "${YELLOW}3. 重新配置采集器${NC}"
    echo -e "   - 自定义的采集器配置已丢失"
    echo -e "   - 需要重新配置采集任务"
    echo ""
    echo -e "${YELLOW}4. 重建监控视图和告警规则${NC}"
    echo -e "   - 自定义的监控视图需要重建"
    echo -e "   - 告警规则需要重新配置"
    echo ""
    echo -e "${RED}⚠️  重要提醒：${NC}"
    echo -e "   以后请使用 'docker-compose restart' 进行日常重启"
    echo -e "   避免使用 'docker-compose down -v'，因为它会删除所有数据！"
    echo ""
}

# 主函数
main() {
    # 检查是否需要恢复
    check_need_restore

    # 显示影响
    show_impact

    # 执行恢复
    perform_restore

    # 显示后续步骤
    show_next_steps
}

# 执行主函数
main "$@"
