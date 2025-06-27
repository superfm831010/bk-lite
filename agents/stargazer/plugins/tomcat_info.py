# -*- coding: utf-8 -*-
# @File：tomcat_info.py.py
# @Time：2025/6/25 12:14
# @Author：bennie
from plugins.base import BaseSSHPlugin


class TomcatInfo(BaseSSHPlugin):
    """Class for collecting Tomcat information."""
    default_script_path = "plugins/shell/tomcat_default_discover.sh"

    plugin_type = "tomcat"
