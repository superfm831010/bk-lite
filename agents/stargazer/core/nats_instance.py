# -- coding: utf-8 --
# @File: nats_instance.py.py
# @Time: 2025/4/25 17:49
# @Author: windyzhao
import os
from dotenv import load_dotenv

load_dotenv()

nats = None
handlers_to_register = []  # 存储需要在服务器启动时注册的处理器


def initialize_nats(app):
    """初始化NATS实例"""
    from core.nats_rpc import NatsIntegration

    global nats
    nats = NatsIntegration(
        app=app,
        service_name="stargazer",
        nats_servers=[os.getenv("NATS_URLS")],
    )

    # 添加一个在服务器启动前执行的listener来注册所有处理器
    @app.listener('before_server_start')
    async def register_all_handlers(app, loop):
        global handlers_to_register
        for subject, handler in handlers_to_register:
            await nats.register_handler_safe(subject, handler)

    return nats


def get_nats():
    """获取NATS实例"""
    global nats
    if nats is None:
        raise RuntimeError("NATS尚未初始化")
    return nats


def register_handler(subject):
    """处理器注册装饰器，将处理器暂存而不是立即注册"""
    global handlers_to_register

    def decorator(handler):
        handlers_to_register.append((subject, handler))
        return handler

    return decorator
