# -- coding: utf-8 --
# @File: base.py
# @Time: 2025/8/5 14:46
# @Author: windyzhao
from apps.system_mgmt.models import Channel, ChannelChoices


def get_default_first_channel_id(channel_type):
    """
    查询默认的通知渠道
    :param channel_type: 渠道类型
    """
    channel = Channel.objects.filter(channel_type=channel_type).first()
    if channel:
        return channel.id
    return


def get_default_notify_params():
    """
    获取默认的通知参数格式
    :return: 默认的通知参数格式
    """
    channel = ChannelChoices.EMAIL
    channel_id = get_default_first_channel_id(channel_type=channel)
    return channel, channel_id
