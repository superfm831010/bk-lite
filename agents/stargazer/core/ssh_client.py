# -- coding: utf-8 --
# @File: ssh_client.py
# @Time: 2025/4/30 15:59
# @Author: windyzhao
import time

import paramiko
from typing import Optional
from dataclasses import dataclass


# from sanic.log import logger


@dataclass
class SSHResult:
    """SSH命令执行结果"""
    stdout: str
    stderr: str
    exit_status: int
    exec_time: float


class SSHClient:
    """封装的Paramiko SSH客户端"""

    def __init__(self, timeout: int = 30):
        """
        初始化SSH客户端

        :param timeout: 连接和操作超时时间(秒)
        """
        self.timeout = timeout
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, host: str, username: str,
                password: Optional[str] = None, port: int = 22,
                key_filename: Optional[str] = None) -> None:
        """
        建立SSH连接

        :raises: ConnectionError 如果连接失败
        """
        try:
            print(f"Connecting to {host}:{port} as {username}...")
            self._client.connect(
                hostname=host,
                port=port,
                username=username,
                password=password,
                key_filename=key_filename,
                timeout=self.timeout,
                banner_timeout=self.timeout,
                allow_agent=False,
                look_for_keys=False
            )
            print(f"Connected to {host} successfully")
        except Exception as e:
            self.close()
            raise ConnectionError(f"SSH connection failed to {host}: {str(e)}")

    # 修改 SSHClient 类的 execute_command 方法

    def execute_command(self, command, timeout=None):
        """
        在远程主机上执行命令并获取结果

        :param command: 要执行的命令
        :param timeout: 命令执行超时时间(秒)
        :return: SSHResult对象
        """
        # 检查连接
        if not self._client or not self._client.get_transport() or not self._client.get_transport().is_active():
            raise Exception("Not connected")

        # 创建会话
        channel = self._client.get_transport().open_session()

        # 获取伪终端（有时需要这个来确保输出正确）
        channel.get_pty()

        # 设置超时
        if timeout:
            channel.settimeout(timeout)

        # 执行命令
        start_time = time.time()
        channel.exec_command(command)

        # 读取输出
        stdout_data = channel.makefile('r').read()
        stderr_data = channel.makefile_stderr('r').read()

        # 等待命令完成
        exit_status = channel.recv_exit_status()

        # 关闭通道
        channel.close()

        # 记录命令执行时间
        exec_time = time.time() - start_time
        print(f"Command executed in {exec_time:.2f}s")

        # 如果输出是二进制，转换为字符串
        if isinstance(stdout_data, bytes):
            stdout_data = stdout_data.decode('utf-8', errors='replace')
        if isinstance(stderr_data, bytes):
            stderr_data = stderr_data.decode('utf-8', errors='replace')

        # 打印原始输出大小以便调试
        print(f"DEBUG: Raw stdout size: {len(stdout_data)}, stderr size: {len(stderr_data)}")

        return SSHResult(stdout_data, stderr_data, exit_status, exec_time)

    def close(self) -> None:
        """关闭SSH连接"""
        if hasattr(self, '_client') and self._client:
            self._client.close()
            self._client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
