# -*- coding: utf-8 -*-
# @File：es_info.py.py
# @Time：2025/7/7 11:43
# @Author：bennie
from plugins.base import BaseSSHPlugin

class ESInfo(BaseSSHPlugin):
    """Class for collecting es information."""
    default_script_path = "plugins/shell/es_default_discover.sh"
    plugin_type = "es"
