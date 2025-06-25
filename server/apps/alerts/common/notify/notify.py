# -- coding: utf-8 --
# @File: notify.py
# @Time: 2025/6/11 14:06
# @Author: windyzhao
from apps.alerts.utils.system_mgmt_util import SystemMgmtUtils
from apps.core.logger import alert_logger as logger


class Notify:
    """
    Notify class for handling alert notifications.
    This class should be extended by specific notification handlers.
    """

    def __init__(self, username_list, channel, title, content):
        self.title = title
        self.content = content
        self.channel = channel
        self.user_list = self.get_user_list(username_list)

    @staticmethod
    def get_user_list(username_list):
        """
        Get the list of users to notify.
        This method should be implemented by subclasses if needed.
        """
        result = []
        all_users = SystemMgmtUtils.get_user_all()
        user_map = {i["username"]: i for i in all_users}
        for username in username_list:
            user_info = user_map.get(username)
            if user_info:
                result.append(user_info)
        return result

    def get_channel_id(self):
        result = SystemMgmtUtils.search_channel_list(channel_type=self.channel)
        if result:
            return result[0]["id"]

        return

    def get_user_emails(self):
        emails = [user["email"] for user in self.user_list]
        return emails

    def email(self):
        """
        Notify via email.
        This method should be implemented by subclasses.
        """
        channel_id = self.get_channel_id()
        if not channel_id:
            logger.warning(f"Channel {self.channel} does not exist.")
            return

        send_result = SystemMgmtUtils.send_msg_with_channel(
            channel_id=channel_id,
            title=self.title,
            content=self.content,
            receivers=self.get_user_emails()
        )
        logger.info(f"Email notification sent: {send_result}")
        return send_result

    def enterprise_wechat(self):
        """
        Notify via enterprise WeChat.
        This method should be implemented by subclasses.
        """
        channel_id = self.get_channel_id()
        if not channel_id:
            logger.warning(f"Channel {self.channel} does not exist.")
            return

        send_result = SystemMgmtUtils.send_msg_with_channel(
            channel_id=channel_id,
            title=self.title,
            content=self.content,
            receivers=[user["id"] for user in self.user_list]
        )
        logger.info(f"Enterprise WeChat notification sent: {send_result}")
        return send_result

    def notify(self):
        """
        Notify the alert.
        This method should be implemented by subclasses.
        """

        notify = getattr(self, self.channel, None)
        if notify and callable(notify):
            return notify()
        else:
            logger.error(f"Notification method {self.channel} is not implemented or invalid.")
            raise NotImplementedError(f"Notification method {self.channel} is not implemented.")
