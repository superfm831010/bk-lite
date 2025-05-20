# -*- coding: UTF-8 -*-
"""
调用方法：
client = ResourceClient(account, password, region, resourcetype, host="", **kwargs)
vm_info = client.cw.get_vms(**kwargs)
"""
import importlib
from functools import partial, wraps

from .collection import RESOURCE_COLLECTIONS


class ResourceClient(object):
    collection = {}

    def __init__(self, account, password, region, cloud_type, host="", **kwargs):
        self.account = account
        self.password = password
        self.region = region
        self.cloud_type = cloud_type
        self.host = host
        self.kwargs = kwargs

    @classmethod
    def set_component(cls, resource_component):
        cls.collection = resource_component

    @classmethod
    def update_component(cls, key, component_cls):
        cls.collection.update({key: component_cls})

    def __call__(self):
        pass

    def __getattr__(self, item):
        key = item + "_" + self.cloud_type.lower()
        if key in self.collection:
            class_path = self.collection[key]
            # 通过路径获取获取类
            module_name, class_name = class_path.rsplit(".", 1)
            _module = importlib.import_module(module_name)
            cls = getattr(_module, class_name)
            if not cls:
                raise AttributeError(f"Cloud:{self.cloud_type} not define method `{item}`")
            return cls(self.account, self.password, self.region, host=self.host, **self.kwargs)


ResourceClient.set_component(RESOURCE_COLLECTIONS)


def register(func=None, key="", **kwargs):
    if func is None:
        return partial(register, key=key)
    key = key or f"cw_{func.__name__[2:].lower()}"
    class_path = f"{func.__module__}.{func.__name__}"
    ResourceClient.update_component(key, class_path)

    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner
