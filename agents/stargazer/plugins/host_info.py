# -- coding: utf-8 --
# @File: host_info.py
# @Time: 2025/5/6 17:48
# @Author: windyzhao
# !/usr/bin/python
# -*- coding: utf-8 -*-
import json

from core.nast_request import NATSClient
from plugins.base_utils import convert_to_prometheus_format
from sanic.log import logger


class HostInfo:
    """Class for collecting host information."""

    def __init__(self, params: dict):
        self.node_id = params["node_id"]
        self.username = params.get("username")
        self.password = params.get("password")
        self.time_out = int(params.get("execute_timeout", 60))
        self.command = params.get("command", self.script)
        self.nats_client = NATSClient()

    @property
    def script(self) -> str:
        """
        采集脚本
        权限要求
            SSH访问权限:
            需要有SSH登录目标主机的权限
            建议创建一个专用的只读账号用于信息采集
            命令执行权限:
            需要执行以下命令的权限:
            uname
            cat /etc/os-release
            lscpu
            free
            df
            ip 或 ifconfig
            文件读取权限:
            需要读取 /etc/os-release 文件的权限
            需要读取 /proc/cpuinfo 和 /proc/meminfo 的权限 (通过命令间接访问)
        """
        result = """
#!/bin/bash
set -e  # 遇到错误立即退出

unknown_or() {
    "$@" 2>/dev/null || echo "unknown"
}

# 主机名称
system_info_hostname=$(unknown_or hostname -f || unknown_or hostname)

# 操作系统类型 (Linux/Windows/BSD)
system_info_os_type=$(unknown_or uname -o)

# 操作系统名称 (Ubuntu/CentOS/RedHat)
system_info_os_name=$(
    (unknown_or grep -E '^NAME=' /etc/os-release || 
     unknown_or grep -E '^DISTRIB_ID=' /etc/lsb-release || 
     unknown_or grep -E '^ID=' /etc/os-release) | head -n1 | cut -d '=' -f 2 | tr -d '"'
)

# 操作系统版本 (20.04/7/11)
system_info_os_version=$(
    (unknown_or grep -E '^VERSION_ID=' /etc/os-release || 
     unknown_or grep -E '^DISTRIB_RELEASE=' /etc/lsb-release) | head -n1 | cut -d '=' -f 2 | tr -d '"'
)

# 操作系统位数 (32-bit/64-bit)
if [ "$(unknown_or uname -m)" = "x86_64" ] || [ "$(unknown_or uname -m)" = "aarch64" ]; then
    system_info_os_bits="64-bit"
elif [ "$(unknown_or uname -m)" = "i386" ] || [ "$(unknown_or uname -m)" = "i686" ]; then
    system_info_os_bits="32-bit"
else
    system_info_os_bits="unknown"
fi

# CPU 架构 (x86_64/arm64)
system_info_cpu_architecture=$(unknown_or uname -m)

# CPU 型号
system_info_cpu_model=$(
    if unknown_or which lscpu >/dev/null; then
        unknown_or lscpu | grep -i 'model name' | awk -F: '{print $2}' | xargs
    else
        unknown_or grep -m1 -i 'model name' /proc/cpuinfo | awk -F: '{print $2}' | xargs
    fi
)

# CPU 核数
system_info_cpu_cores=$(
    if unknown_or which lscpu >/dev/null; then
        unknown_or lscpu | grep -i '^CPU(s):' | awk -F: '{print $2}' | xargs
    else
        unknown_or grep -c '^processor' /proc/cpuinfo
    fi
)

# 内存 (GB)
system_info_memory_gb=$(
    if unknown_or which free >/dev/null; then
        mem_mb=$(unknown_or free -m | awk '/Mem:/{print $2}')
        printf "%.1f" $(echo "$mem_mb / 1024" | bc -l)
    else
        mem_kb=$(unknown_or awk '/MemTotal/{print $2}' /proc/meminfo)
        printf "%.1f" $(echo "$mem_kb / 1024 / 1024" | bc -l)
    fi
)

# 磁盘 (GB)
system_info_disk_gb=$(
    if unknown_or which df >/dev/null; then
        disk_kb=$(unknown_or df -k --exclude-type=tmpfs --exclude-type=devtmpfs --exclude-type=overlay 2>/dev/null | awk 'NR>1 {sum+=$2} END {print sum}')
        printf "%.1f" $(echo "$disk_kb / 1024 / 1024" | bc -l)
    else
        echo "unknown"
    fi
)

# 内网 MAC 地址
system_info_mac_address=$(
    (unknown_or ip link show || unknown_or ifconfig -a) 2>/dev/null | 
    awk '/ether/{print $2; exit}' || 
    echo "unknown"
)

# 输出 JSON
cat <<EOF
{
    "hostname": "$system_info_hostname",
    "os_type": "$system_info_os_type",
    "os_name": "$system_info_os_name",
    "os_version": "$system_info_os_version",
    "os_bits": "$system_info_os_bits",
    "cpu_architecture": "$system_info_cpu_architecture",
    "cpu_model": "$system_info_cpu_model",
    "cpu_cores": "$system_info_cpu_cores",
    "memory_gb": "$system_info_memory_gb",
    "disk_gb": "$system_info_disk_gb",
    "mac_address": "$system_info_mac_address"
}
EOF
    """
        return result

    async def connect_nats(self):
        """异步连接 NATS"""
        await self.nats_client.connect()

    async def close_nats(self):
        """异步关闭 NATS"""
        await self.nats_client.close()

    @property
    def nast_id(self):
        """
        生成NATS ID
        :return:
        """
        return "ssh.execute" if self.username else "local.execute"

    def format_params(self):
        """
        格式化参数
        :return:
        """
        script_params = {
            "command": self.command,
        }
        if self.username:
            script_params["username"] = self.username
            script_params["password"] = self.password
        if self.time_out:
            script_params["execute_timeout"] = self.time_out
        return script_params

    async def exec_script(self):
        """
        调用 NATS 执行脚本
        """
        exec_params = {
            "args": [self.format_params()],
            "kwargs": {}
        }
        subject = f"{self.nast_id}.{self.node_id}"
        response = await self.nats_client.request(subject=subject, params=exec_params)  # 使用 await 调用异步方法
        return json.loads(response["result"])

    async def list_all_resources(self):
        """
        Convert collected data to a standard format.
        """
        try:
            await self.connect_nats()  # 异步连接 NATS
            data = await self.exec_script()  # 使用 await 获取执行结果
            prometheus_data = convert_to_prometheus_format({"host": [data]})
            return prometheus_data
        except Exception as err:
            import traceback
            logger.error(f"host_info main error! {traceback.format_exc()}")
        finally:
            await self.close_nats()  # 异步关闭 NATS
