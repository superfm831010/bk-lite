# -*- coding: utf-8 -*-
# @File：apache_info.py.py
# @Time：2025/7/8 16:22
# @Author：bennie

from plugins.base import BaseSSHPlugin


class ApacheInfo(BaseSSHPlugin):
    """Class for collecting apache information."""
    default_script_path = "plugins/shell/apache_default_discover.sh"
    plugin_type = "apache"