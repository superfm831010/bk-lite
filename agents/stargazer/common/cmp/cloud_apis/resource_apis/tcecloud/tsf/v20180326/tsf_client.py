import json

from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_client import AbstractClient
from common.cmp.cloud_apis.resource_apis.tcecloud.common.exception.tce_cloud_sdk_exception import TceCloudSDKException
from common.cmp.cloud_apis.resource_apis.tcecloud.tsf.v20180326 import models


class TsfClient(AbstractClient):
    _apiVersion = "2018-03-26"
    _endpoint = "tsf.api3.{{conf.main_domain}}"

    def DescribeApplicationAttribute(self, request):
        try:
            params = request._serialize()
            body = self.call("DescribeApplicationAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)

    def DescribeApplications(self, request):
        try:
            params = request._serialize()
            body = self.call("DescribeApplications", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeApplicationsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TceCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TceCloudSDKException):
                raise
            else:
                raise TceCloudSDKException(e.message, e.message)
