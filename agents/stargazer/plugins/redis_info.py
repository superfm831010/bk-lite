# -*- coding: utf-8 -*-
# @File: redis_info.py
# @Time: 2025/6/4 12:00
# @Author: bennie

from plugins.base import BaseSSHPlugin


class RedisInfo(BaseSSHPlugin):
    """Class for collecting Redis information."""
    default_script_path = "plugins/shell/redis_default_discover.sh"

    plugin_type = "redis"
