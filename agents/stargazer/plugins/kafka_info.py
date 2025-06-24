# -*- coding: utf-8 -*-
# @File：kafka_info.py
# @Time：2025/6/9 12:02
# @Author：bennie


from plugins.base import BaseSSHPlugin


class KafkaInfo(BaseSSHPlugin):
    """Class for collecting kafka information."""
    default_script_path = "plugins/shell/kafka_default_discover.sh"

    plugin_type = "kafka"
