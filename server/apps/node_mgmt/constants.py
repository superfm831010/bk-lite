import os

NORMAL = "normal"
ABNORMAL = "abnormal"
NOT_INSTALLED = "not_installed"

SIDECAR_STATUS_ENUM = {
    NORMAL: "正常",
    ABNORMAL: "异常",
    NOT_INSTALLED: "未安装",
}

# 节点服务地址key
NODE_SERVER_URL_KEY = "NODE_SERVER_URL"

LINUX_OS = "linux"
WINDOWS_OS = "windows"

# 控制器下发目录
CONTROLLER_INSTALL_DIR = {
    LINUX_OS: {"storage_dir": "/tmp", "install_dir": "/tmp"},
    WINDOWS_OS: {"storage_dir": "/tmp", "install_dir": "C:\\gse"},
}

# 采集器下发目录
COLLECTOR_INSTALL_DIR = {
    LINUX_OS: "/opt/fusion-collectors/bin",
    WINDOWS_OS: "C:\\gse\\fusion-collectors\\bin",
}

# 设置权限并运行命令
RUN_COMMAND = {
    LINUX_OS: "sudo rm -rf /opt/fusion-collectors && sudo mv /tmp/fusion-collectors /opt/fusion-collectors && sudo chmod -R +x /opt/fusion-collectors/* && cd /opt/fusion-collectors && sudo bash ./install.sh {server_url}/api/v1/node_mgmt/open_api/node {server_token} {cloud} {group} {node_name} {node_id}",
    WINDOWS_OS: "powershell -command \"Set-ExecutionPolicy Unrestricted -Force; & '{}\\install.ps1' -ServerUrl {} -ServerToken {} -Cloud {} -Group {} -NodeName {} -NodeId {}\"",
}

# 卸载命令
UNINSTALL_COMMAND = {
    LINUX_OS: "cd /opt/fusion-collectors && ./uninstall.sh",
    WINDOWS_OS: "powershell -command \"Remove-Item -Path {} -Recurse\"",
}

# 控制器目录删除命令
CONTROLLER_DIR_DELETE_COMMAND = {
    LINUX_OS: "rm -rf /opt/fusion-collectors",
    WINDOWS_OS: "powershell -command \"Remove-Item -Path {} -Recurse\"",
}

CACHE_TIMEOUT = 60 * 5  # 5分钟

# 控制器默认更新时间
DEFAULT_UPDATE_INTERVAL = 30    # 30秒
