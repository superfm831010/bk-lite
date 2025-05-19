import os

NORMAL = "normal"
ABNORMAL = "abnormal"
NOT_INSTALLED = "not_installed"

SIDECAR_STATUS_ENUM = {
    NORMAL: "正常",
    ABNORMAL: "异常",
    NOT_INSTALLED: "未安装",
}

# 本服务的地址
LOCAL_HOST = os.getenv("WEB_SERVER_URL")

# 节点服务地址key
NODE_SERVER_URL_KEY = "NODE_SERVER_URL"

LINUX_OS = "linux"
WINDOWS_OS = "windows"

W_SIDECAR_DOWNLOAD_URL = f"{LOCAL_HOST}/openapi/sidecar/download_file/?file_name=sidecar_windows.zip"
L_SIDECAR_DOWNLOAD_URL = f"{LOCAL_HOST}/openapi/sidecar/download_file/?file_name=sidecar_linux.tar.gz"
L_INSTALL_DOWNLOAD_URL = f"{LOCAL_HOST}/openapi/sidecar/download_file/?file_name=install_sidecar.sh"

# 控制器下发目录
CONTROLLER_INSTALL_DIR = {
    LINUX_OS: {"storage_dir": "/tmp", "install_dir": "/opt"},
    WINDOWS_OS: {"storage_dir": "/tmp", "install_dir": "C:\\gse"},
}

# 采集器下发目录
COLLECTOR_INSTALL_DIR = {
    LINUX_OS: "/opt/fusion-collectors/bin",
    WINDOWS_OS: "C:\\gse\\fusion-collectors\\bin",
}

# 设置权限并运行命令
RUN_COMMAND = {
    LINUX_OS: "chmod -R +x /opt/fusion-collectors && cd /opt/fusion-collectors && ./install.sh {server_url}/node_mgmt/open_api/node {server_token}",
    WINDOWS_OS: "powershell -command \"cd C:\\gse\\fusion-collectors && .\\install.ps1 {server_url} {server_token}\"",
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