# from aliyunsdkasapi.request import RpcRequest
from common.cmp.cloud_apis.resource_apis.aliyunsdkasapi.request import RpcRequest


class AsapiRequest(RpcRequest):
    def __init__(self, product, version, action_name, asapi_gateway):
        RpcRequest.__init__(self, product, version, action_name)
        self.set_endpoint(asapi_gateway)
        self.set_accept_format("JSON")

    def __setitem__(self, k, v):
        self.k = v
