import pytest
from django.contrib.auth.hashers import make_password
from apps.system_mgmt.models import User
from apps.system_mgmt.nats_api import get_all_users
import logging

logger = logging.getLogger(__name__)


def create_test_users():
    """创建测试用户数据"""
    test_users = [
        {
            "username": "test_user1",
            "display_name": "测试用户1",
            "email": "test1@example.com",
            "password": make_password("password123"),
            "locale": "zh-Hans",
        },
        {
            "username": "test_user2",
            "display_name": "测试用户2",
            "email": "test2@example.com",
            "password": make_password("password123"),
            "locale": "en-US",
        }
    ]

    # 创建测试用户并返回创建的用户列表
    created_users = []
    for user_data in test_users:
        user = User.objects.create(**user_data)
        created_users.append(user)

    return created_users


@pytest.mark.django_db
def test_get_all_users():
    # 初始化测试用户数据
    create_test_users()

    # 调用被测函数
    result = get_all_users()
    logger.info(result)

    # 验证结果
    assert result["result"] is True
    assert len(result["data"]) >= 2  # 至少包含我们创建的两个用户

    # 验证返回的用户数据包含我们创建的用户
    usernames = [user["username"] for user in result["data"]]
    assert "test_user1" in usernames
    assert "test_user2" in usernames
