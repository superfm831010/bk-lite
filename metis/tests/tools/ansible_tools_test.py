from src.tools.ansible_tools_plus import ansible_adhoc
import os

import logging

logger = logging.getLogger(__name__)


# def test_ansible_adhoc_module_tools():
#     result1 = ansible_adhoc.run('', config={
#         'configurable': {
#             "module": "ansible.builtin.pip",
#             "module_args": "name=pymysql",
#         }
#     })
#     logger.info(result1)
#     result2 = ansible_adhoc.run('', config={
#         'configurable': {
#             "module": "mysql_info",
#             "module_args": "login_user=root login_host=127.0.0.1 login_password=123456",
#         }
#     })  # type: ignore
#
#     logger.info(result2)


# def test_ansible_adhoc_inventory_tools():
#     result = ansible_adhoc.run('', config={
#         'configurable': {
#             "inventory": os.environ['TEST_ANSIBLE_INVENTORY'],
#             "module": "command",
#             "module_args": "hostname",
#         }
#     })  # type: ignore
#
#     logger.info(result)
