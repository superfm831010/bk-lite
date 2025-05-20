from common.cmp.cloud_apis.resource_apis.tcecloud.common.abstract_model import AbstractModel


class ApplicationAttribute(AbstractModel):
    """应用列表其它字段返回参数"""

    def __init__(self):
        """
        :param GroupCount: 应用ID
        :type GroupCount: int
        :param InstanceCount: 应用ID
        :type InstanceCount: int
        :param RunInstanceCount: 应用ID
        :type RunInstanceCount: int
        """
        self.GroupCount = None
        self.InstanceCount = None
        self.RunInstanceCount = None

    def _deserialize(self, params):
        self.GroupCount = params.get("GroupCount")
        self.InstanceCount = params.get("InstanceCount")
        self.RunInstanceCount = params.get("RunInstanceCount")


class DescribeApplicationAttributeRequest(AbstractModel):
    """DescribeApplicationAttribute请求参数结构体"""

    def __init__(self):
        """
        :param ApplicationId: 应用ID
        :type ApplicationId: str
        """
        self.ApplicationId = None

    def _deserialize(self, params):
        self.ApplicationId = params.get("ApplicationId")


class DescribeApplicationAttributeResponse(AbstractModel):
    """DescribeApplicationAttribute返回参数结构体"""

    def __init__(self):
        """
        :param Result: 应用列表其它字段返回参数
        :type Result: ApplicationAttribute
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Result") is not None:
            self.Result = ApplicationAttribute()
            self.Result._deserialize(params.get("Result"))
        self.RequestId = params.get("RequestId")


class DescribeApplicationsRequest(AbstractModel):
    """DescribeApplications请求参数结构体"""

    def __init__(self):
        """
        :param SearchWord: 搜索字段
        :type SearchWord: str
        :param OrderBy: 排序字段
        :type OrderBy: str
        :param OrderType: 排序类型
        :type OrderType: Integer
        :param Offset: 偏移量
        :type Offset: Integer
        :param Limit: 分页个数
        :type Limit: Integer
        :param ApplicationType: 应用类型
        :type ApplicationType: str
        :param MicroserviceType: 应用的微服务类型
        :type MicroserviceType: str
        :param ApplicationResourceTypeList: 应用资源类型数组
        :type ApplicationResourceTypeList: List of Str
        :param ApplicationIdList: IdList
        :type ApplicationIdList: List of Str
        """
        self.SearchWord = None
        self.OrderBy = None
        self.OrderType = None
        self.Offset = None
        self.Limit = None
        self.ApplicationType = None
        self.MicroserviceType = None
        self.ApplicationResourceTypeList = None
        self.ApplicationIdList = None

    def _deserialize(self, params):
        self.SearchWord = params.get("SearchWord")
        self.OrderBy = params.get("OrderBy")
        self.OrderType = params.get("OrderType")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.ApplicationType = params.get("ApplicationType")
        self.MicroserviceType = params.get("MicroserviceType")
        self.ApplicationResourceTypeList = params.get("ApplicationResourceTypeList")
        self.ApplicationIdList = params.get("ApplicationIdList")


class DescribeApplicationsResponse(AbstractModel):
    """DescribeApplications返回参数结构体"""

    def __init__(self):
        """
        :param Result: 应用分页列表信息
        :type Result: TsfPageApplication
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Result = None
        self.RequestId = None

    def _deserialize(self, params):
        if params.get("Result") is not None:
            self.Result = TsfPageApplication()
            self.Result._deserialize(params.get("Result"))
        self.RequestId = params.get("RequestId")


class TsfPageApplication(AbstractModel):
    """应用分页信息"""

    def __init__(self):
        """
        :param TotalCount: 应用总数目
        :type TotalCount: int
        :param Content: 应用信息列表
        :type Content: List of ApplicationForPage
        """
        self.TotalCount = None
        self.Content = None

    def _deserialize(self, params):
        if params.get("Content") is not None:
            self.Content = []
            for item in params.get("Content"):
                obj = ApplicationForPage()
                obj._deserialize(item)
                self.Content.append(obj)
        self.TotalCount = params.get("RequestId")


class ApplicationForPage(AbstractModel):
    """分页的应用描述信息字段"""

    def __init__(self):
        """
        :param ApplicationId: 应用ID
        :type ApplicationId: str
        :param ApplicationName: 应用名称
        :type ApplicationName: str
        :param ApplicationDesc: 应用描述
        :type ApplicationDesc: str
        :param ApplicationType: 应用类型
        :type ApplicationType: str
        :param MicroserviceType: 微服务类型
        :type MicroserviceType: str
        :param ProgLang: 编程语言
        :type ProgLang: str
        :param ApplicationRuntimeType: 	应用runtime类型
        :type ApplicationRuntimeType: str
        :param ApplicationResourceType: 	应用资源类型
        :type ApplicationResourceType: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param ApigatewayServiceId: Apigateway的serviceId
        :type ApigatewayServiceId: str
        """
        self.ApplicationId = None
        self.ApplicationName = None
        self.ApplicationDesc = None
        self.ApplicationType = None
        self.MicroserviceType = None
        self.ProgLang = None
        self.ApplicationRuntimeType = None
        self.ApplicationResourceType = None
        self.CreateTime = None
        self.UpdateTime = None
        self.ApigatewayServiceId = None

    def _deserialize(self, params):
        self.ApplicationId = params.get("ApplicationId")
        self.ApplicationName = params.get("ApplicationName")
        self.ApplicationDesc = params.get("ApplicationDesc")
        self.ApplicationType = params.get("ApplicationType")
        self.MicroserviceType = params.get("MicroserviceType")
        self.ProgLang = params.get("ProgLang")
        self.ApplicationRuntimeType = params.get("ApplicationRuntimeType")
        self.ApplicationResourceType = params.get("ApplicationResourceType")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.ApigatewayServiceId = params.get("ApigatewayServiceId")
