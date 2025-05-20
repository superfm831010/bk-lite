# -- coding: utf-8 --
# @File: nats_rpc.py
# @Time: 2025/4/25 16:29
# @Author: windyzhao
import asyncio
import json
from datetime import datetime
from typing import Dict, Callable, Any, Awaitable
from nats.aio.client import Client as NATS
from sanic import Sanic


class NatsIntegration:
    def __init__(
            self,
            app: Sanic,
            service_name: str,
            nats_servers: list = None,
            auto_discovery: bool = True,
            connect_timeout: int = 5,
            max_reconnect_attempts: int = 5
    ):
        self.app = app
        self.service_name = service_name
        self.nats_servers = nats_servers or ["nats://localhost:4222"]
        self.nc = NATS()
        self.handlers: Dict[str, Callable] = {}
        self.auto_discovery = auto_discovery
        self.connect_timeout = connect_timeout
        self.max_reconnect_attempts = max_reconnect_attempts
        self._is_connecting = False
        self._shutting_down = False

        # 设置日志

        # 注册Sanic生命周期事件
        self._register_sanic_events()

    def _register_sanic_events(self):
        """注册Sanic生命周期事件"""

        @self.app.listener('before_server_start')
        async def before_server_start(app, loop):
            print("Sanic before_server_start event triggered")
            await self._start_nats_service()

        @self.app.listener('after_server_stop')
        async def after_server_stop(app, loop):
            print("Sanic after_server_stop event triggered")
            await self._stop_nats_service()

        @self.app.listener('main_process_ready')
        async def main_process_ready(app, loop):
            print("Sanic main_process_ready event triggered")

    async def _start_nats_service(self):
        """启动NATS服务连接"""
        if self._is_connecting:
            print("NATS service is already connecting")
            return

        self._is_connecting = True
        self._shutting_down = False

        try:
            print(f"Connecting to NATS servers")

            await self.nc.connect(
                servers=self.nats_servers,
                connect_timeout=self.connect_timeout,
                max_reconnect_attempts=self.max_reconnect_attempts,
                reconnect_time_wait=2,
                name=self.service_name,
                closed_cb=self._connection_closed_callback,
                disconnected_cb=self._disconnected_callback,
                reconnected_cb=self._reconnected_callback,
                error_cb=self._error_callback
            )

            self.app.ctx.nats_connected = True
            self.app.ctx.nats_client = self

            print("NATS service successfully started")

        except Exception as e:
            print(f"Failed to start NATS service: {str(e)}")
            self.app.ctx.nats_connected = False
            raise
        finally:
            self._is_connecting = False

    async def _stop_nats_service(self):
        """停止NATS服务连接"""
        if self._shutting_down or self.nc.is_closed:
            return

        self._shutting_down = True
        print("Shutting down NATS service...")

        try:
            # 发送服务下线通知
            await self.nc.publish(
                "service.unregister",
                json.dumps({"name": self.service_name}).encode()
            )

            await self.nc.drain()
            print("NATS service gracefully stopped")
        except Exception as e:
            print(f"Error during NATS shutdown: {str(e)}")
            try:
                await self.nc.close()
            except:
                pass
        finally:
            self.app.ctx.nats_connected = False

    # NATS 事件回调
    async def _connection_closed_callback(self):
        if not self._shutting_down:
            print("NATS connection was closed unexpectedly")
            self.app.ctx.nats_connected = False

    async def _disconnected_callback(self):
        print("Disconnected from NATS server")
        self.app.ctx.nats_connected = False

    async def _reconnected_callback(self):
        print("Reconnected to NATS server")
        self.app.ctx.nats_connected = True
        await self.register_service()

    async def _error_callback(self, e):
        print(f"NATS error: {str(e)}")

    async def register_service(self):
        """手动注册当前服务"""
        service_info = {
            "name": self.service_name,
            "timestamp": datetime.now().isoformat(),
            "endpoints": list(self.handlers.keys()),
            "status": "online"
        }
        await self.nc.publish("service.register", json.dumps(service_info).encode())
        print(f"Service {self.service_name} registered")

    def register_handler(self, subject: str, queue: str = None):
        """装饰器：注册消息处理器"""

        def decorator(handler: Callable[[dict], Awaitable[dict]]):
            async def wrapped_handler(msg):
                try:
                    data = json.loads(msg.data.decode()) if msg.data else {}
                    reply = msg.reply

                    print(f"Received message on {msg.subject}: {data}")

                    result = await handler(data)

                    if reply:
                        result["success"] = True
                        await self.nc.publish(reply, json.dumps(result).encode())

                except Exception as e:
                    print(f"Error processing message {msg.subject}: {str(e)}")
                    if reply:
                        await self.nc.publish(
                            reply,
                            json.dumps({
                                "success":False,
                                "status": "error",
                                "message": str(e)
                            }).encode()
                        )

            self.handlers[subject] = wrapped_handler

            async def subscribe():
                try:
                    await self.nc.subscribe(subject, queue=queue, cb=wrapped_handler)
                    print(f"Subscribed to {subject} (queue: {queue or 'default'})")
                except Exception as e:
                    print(f"Failed to subscribe to {subject}: {str(e)}")

            # 确保在连接成功后调用
            if not self.nc.is_closed:
                print(f"Subscribing to {subject} immediately")
                asyncio.create_task(subscribe())

            return handler

        return decorator

    async def publish(self, subject: str, data: Any):
        """发布消息"""
        if self.nc.is_closed:
            raise ConnectionError("NATS connection is closed")
        await self.nc.publish(subject, json.dumps(data).encode())

    async def request(self, subject: str, data: Any, timeout: float = 2.0) -> Any:
        """发送请求并等待响应"""
        if self.nc.is_closed:
            raise ConnectionError("NATS connection is closed")
        msg = await self.nc.request(
            subject,
            json.dumps(data).encode(),
            timeout=timeout
        )
        return json.loads(msg.data.decode())

    def is_connected(self) -> bool:
        """检查NATS连接状态"""
        return not self.nc.is_closed and hasattr(self.app.ctx, 'nats_connected') and self.app.ctx.nats_connected

    async def register_handler_safe(self, subject, handler):
        """在事件循环运行时安全注册处理器"""
        # 生成完整的主题名
        full_subject = f"{self.service_name}.{subject}"

        # 注册处理函数
        async def subscriber_callback(msg):
            try:
                data = json.loads(msg.data.decode()) if msg.data else {}
                reply = msg.reply

                print(f"Received message on {msg.subject}: {data}")

                result = await handler(data)

                if reply:
                    result["success"] = True
                    await self.nc.publish(reply, json.dumps(result).encode())

            except Exception as e:
                print(f"Error processing message {msg.subject}: {str(e)}")
                if reply:
                    await self.nc.publish(
                        reply,
                        json.dumps({
                            "success": False,
                            "status": "error",
                            "message": str(e)
                        }).encode()
                    )

        # 直接订阅，因为此时事件循环已经运行
        await self.nc.subscribe(full_subject, cb=subscriber_callback)
        return handler
