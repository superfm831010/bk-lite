# -*- coding: utf-8 -*-
# @File：pgsql_info.py
# @Time：2025/7/10 09:53
# @Author：bennie

from plugins.base import BaseSSHPlugin


class PgsqlInfo(BaseSSHPlugin):
    """Class for collecting pgsql information."""
    default_script_path = "plugins/shell/pgsql_default_discover.sh"
    plugin_type = "postgresql"