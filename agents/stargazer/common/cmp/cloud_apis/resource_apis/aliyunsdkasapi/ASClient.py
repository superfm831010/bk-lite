# from aliyunsdkasapi.client import AcsClient
from common.cmp.cloud_apis.resource_apis.aliyunsdkasapi.client import AcsClient


class ASClient(AcsClient):
    def __init__(self, accessKeyId, accessKeySecret, regionId):
        self.client = AcsClient.__init__(
            self,
            accessKeyId,
            accessKeySecret,
            region_id=regionId,
            auto_retry=True,
            max_retry_time=3,
            user_agent=None,
            port=80,
            debug=True,
        )
