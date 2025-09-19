# -*- coding: utf-8 -*-
"""
异步工具函数
用于在 Django 视图中安全地运行异步代码
"""

import asyncio
import functools
import threading
from typing import Awaitable, TypeVar

T = TypeVar('T')


def run_async_in_thread(coro: Awaitable[T]) -> T:
    """
    在新线程中运行异步代码
    避免与 Django 的同步视图产生冲突
    
    Args:
        coro: 异步协程
        
    Returns:
        T: 协程的返回值
    """
    result = None
    exception = None
    
    def run_in_thread():
        nonlocal result, exception
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(coro)
            finally:
                loop.close()
        except Exception as e:
            exception = e
    
    # 在新线程中运行
    thread = threading.Thread(target=run_in_thread)
    thread.start()
    thread.join()
    
    if exception:
        raise exception
    
    return result


def async_to_sync(func):
    """
    装饰器：将异步函数转换为同步函数
    
    Usage:
        @async_to_sync
        async def my_async_function():
            await some_async_operation()
            return result
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        coro = func(*args, **kwargs)
        return run_async_in_thread(coro)
    
    return wrapper