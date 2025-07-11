# -*- coding: utf-8 -*-
# @File：mongodb_info.py.py
# @Time：2025/7/8 14:36
# @Author：bennie

from plugins.base import BaseSSHPlugin


class MongoDBInfo(BaseSSHPlugin):
    """Class for collecting mongodb information."""
    default_script_path = "plugins/shell/mongodb_default_discover.sh"

    plugin_type = "mongodb"
