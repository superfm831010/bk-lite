# -*- coding: utf-8 -*-
# @File：rabbitmq_info.py.py
# @Time：2025/6/24 17:40
# @Author：bennie
from plugins.base import BaseSSHPlugin


class RabbitMQInfo(BaseSSHPlugin):
    """Class for collecting RabbitMQ information."""
    default_script_path = "plugins/shell/rabbitmq_default_discover.sh"

    plugin_type = "rabbitmq"
