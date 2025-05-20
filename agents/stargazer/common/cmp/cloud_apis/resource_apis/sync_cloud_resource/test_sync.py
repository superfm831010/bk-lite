# from django.test import TestCase

from unittest import TestCase

from home_application.helpers.password_crypt import aes_decrypt
from home_application.models import AccountConfig

from common.cmp.cloud_apis.collection import SYNC_RESOURCE_MAPPING
from common.cmp.cloud_apis.resource_client import ResourceClient
from common.cmp.cloud_apis import sync_resource_data


class MyTestCase(TestCase):
    def setUp(self) -> None:
        # self.assertEqual(True, False)
        account_obj = AccountConfig.objects.get(id=16)
        client = ResourceClient(
            account_obj.account,
            aes_decrypt(account_obj.password),
            account_obj.region,
            account_obj.cloud_type,
            host=account_obj.host,
            project_id=account_obj.project_id,
            domain_id=account_obj.domain_id,
            endpoint=account_obj.endpoint,
            version=account_obj.version,
        ).cw
        self.sync_client = SYNC_RESOURCE_MAPPING[account_obj.cloud_type](client, account_obj)

    def test_sync(self):
        res = sync_resource_data([5])
        print(res)

    def test_sync_vm(self):
        res = getattr(self.sync_client, "sync_vm")()
        print(res)

    def test_sync_image(self):
        res = getattr(self.sync_client, "sync_image")()
        print(res)

    def test_sync_disk(self):
        res = getattr(self.sync_client, "sync_disk")()
        print(res)

    def test_sync_snapshot(self):
        res = getattr(self.sync_client, "sync_snapshot")()
        print(res)

    def test_sync_eip(self):
        res = getattr(self.sync_client, "sync_eip")()
        print(res)

    def test_sync_vpc(self):
        res = getattr(self.sync_client, "sync_vpc")()
        print(res)

    def test_sync_subnet(self):
        res = getattr(self.sync_client, "sync_subnet")()
        print(res)

    def test_sync_security_group(self):
        res = getattr(self.sync_client, "sync_security_group")()
        print(res)

    def test_sync_security_group_rule(self):
        res = getattr(self.sync_client, "sync_security_group_rule")(["043e6aad-09da-4eae-9971-775b8acef0de"])
        print(res)

    def test_sync_bucket(self):
        res = getattr(self.sync_client, "sync_bucket")()
        print(res)

    def test_sync_file_system(self):
        res = getattr(self.sync_client, "sync_file_system")()
        self.assertTrue(res["result"])

    def test_sync_private_bucket(self):
        res = getattr(self.sync_client, "sync_private_bucket")()
        self.assertTrue(res["result"])

    def test_sync_tdsql(self):
        res = getattr(self.sync_client, "sync_tdsql")()
        self.assertTrue(res["result"])

    def test_sync_mariadb(self):
        res = getattr(self.sync_client, "sync_mariadb")()
        self.assertTrue(res["result"])

    def test_sync_redis(self):
        res = getattr(self.sync_client, "sync_redis")()
        self.assertTrue(res["result"])

    def test_sync_load_balancer(self):
        res = getattr(self.sync_client, "sync_load_balancer")()
        print(res)


if __name__ == "__main__":
    pass
    # import os
    #
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # import django
    #
    # django.setup()
    # TestCase.main()
    # mt = MyTestCase()
    # mt.test_sync_eip()
