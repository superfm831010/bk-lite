# -- coding: utf-8 --
# @File: view.py
# @Time: 2025/7/14 17:22
# @Author: windyzhao
from apps.core.utils.web_utils import WebUtils


def request_test(requests):
    print("Processing request:", requests)
    return WebUtils.response_success([])
