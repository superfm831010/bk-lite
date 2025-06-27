# -- coding: utf-8 --
# @File: base.py
# @Time: 2025/6/11 14:06
# @Author: windyzhao

class BaseNotify:
    """
    Base class for notification handlers.
    All notification handlers should inherit from this class.
    """

    def __init__(self, alert, user_list=[]):
        self.alert = alert
        self.user_list = user_list

    def notify(self):
        """
        Notify the alert.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the notify method.")
