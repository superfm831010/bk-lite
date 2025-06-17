# -*- coding: utf-8 -*-
# @File：nginx_info.py.py
# @Time：2025/6/5 16:13
# @Author：bennie


from plugins.base import BaseSSHPlugin


class NginxInfo(BaseSSHPlugin):
    """Class for collecting Nginx information."""
    default_script_path = "plugins/shell/nginx_default_discover.sh"
    plugin_type = "nginx"
