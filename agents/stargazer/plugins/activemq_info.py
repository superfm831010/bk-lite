# -*- coding: utf-8 -*-
# @File：activemq_info.py
# @Time：2025/7/9 10:25
# @Author：bennie

from plugins.base import BaseSSHPlugin


class ActiveMQInfo(BaseSSHPlugin):
    """Class for collecting active information."""
    default_script_path = "plugins/shell/activemq_default_discover.sh"
    plugin_type = "activemq"