# -- coding: utf-8 --
# @File: util.py
# @Time: 2025/5/14 13:44
# @Author: windyzhao
from functools import wraps

from django.utils.crypto import get_random_string

from apps.core.backends import logger


def gen_app_secret():
    """生成app_secret方法"""
    return get_random_string(32)


def catch_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            logger.exception(f"[catch_exception] method name:{func.__name__} error")

        return None

    return wrapper


def split_list(_list, count=100):
    n = len(_list)
    sublists = [_list[i: i + count] for i in range(0, n, count)]
    return sublists
