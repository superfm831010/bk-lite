#!/bin/bash

# 快速修复探针配置脚本
# 用途：修复云区域2的SERVER_URL配置问题

set -e

echo "=== 探针配置修复脚本 ==="
echo

# 1. 修复Sidecar配置文件
echo "1. 修复Sidecar配置文件..."
if [ -f /opt/fusion-collectors/sidecar.yml ]; then
    sed -i 's|server_url: "null/api/v1/node_mgmt/open_api/node"|server_url: "http://192.168.31.10:8080/api/v1/node_mgmt/open_api/node"|' /opt/fusion-collectors/sidecar.yml
    echo "✓ 配置文件已修复"
    echo "  新配置："
    grep server_url /opt/fusion-collectors/sidecar.yml
else
    echo "✗ 未找到配置文件 /opt/fusion-collectors/sidecar.yml"
    exit 1
fi
echo

# 2. 重启服务
echo "2. 重启Sidecar服务..."
if systemctl is-active --quiet sidecar.service 2>/dev/null; then
    systemctl restart sidecar.service
    echo "✓ 服务已重启"
elif systemctl is-enabled --quiet sidecar.service 2>/dev/null; then
    echo "服务存在但未运行，启动中..."
    systemctl start sidecar.service
    echo "✓ 服务已启动"
else
    echo "✗ 服务不存在，请先安装探针"
    exit 1
fi
echo

# 3. 等待服务启动
echo "3. 等待服务启动（5秒）..."
sleep 5
echo

# 4. 检查状态
echo "4. 检查服务状态..."
systemctl status sidecar.service --no-pager -l || true
echo

# 5. 查看最新日志
echo "5. 最新日志（最后20行）："
journalctl -u sidecar.service -n 20 --no-pager
echo

echo "=== 修复完成 ==="
echo
echo "如果服务状态显示 'active (running)'，说明修复成功"
echo "请等待30-60秒后刷新前端页面查看节点是否出现"
echo
echo "如果仍有问题，请查看日志："
echo "  journalctl -u sidecar.service -f"
