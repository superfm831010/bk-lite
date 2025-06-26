# -*- coding: utf-8 -*-
# @File：etcd_info.py
# @Time：2025/6/24 10:05
# @Author：bennie

from plugins.base import BaseSSHPlugin


class EtcdInfo(BaseSSHPlugin):
    """Class for collecting etcd information."""
    default_script_path = "plugins/shell/etcd_default_discover.sh"
    plugin_type = "etcd"