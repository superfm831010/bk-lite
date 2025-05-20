# -*- coding: utf-8 -*-
"""云插件格式化基础类"""
import threading

from common.cmp.cloud_apis.cloud_constant import CloudPlatform
from common.cmp.cloud_apis.resource_apis.resource_format.aliyun.aliyun_format import AliyunResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.amazonaws.amazonaws_format import AmazonAwsFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.cas.cas_format import CasFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.easystack.easystack_format import EasyStackFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.fusioncloud.fusioncloud_format import FusionCloudFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.huaweicloud.huaweicloud_format import HuaweicloudFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.openstack.openstack_format import OpenStackFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.qcloud.qcloud_format import QCloudResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.qingcloud.qingcloud_format import QingCloudFormatResource
from common.cmp.cloud_apis.resource_apis.resource_format.tce.tce_format import TCEResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.tdsql.tdsql_format import TDSQLResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.TKE_Cloud.tke_cloud_format import TKECloudResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.tsf.tsf_format import TSFResourceFormat
from common.cmp.cloud_apis.resource_apis.resource_format.vmware.vmware_format import VmWareResourceFormat


def get_format_method(cloud_type, resource, **kwargs):
    """
    获取格式化方法
    Args:
        cloud_type (str): 云平台类型 取值参照云平台枚举 Aliyun
        resource (str): 资源类型名 region
        **kwargs (): 需要添加的额外参数 如region_id等（这里不要传cloud_type）

    Returns:
        function obj
    """
    instance = _get_format_instance(cloud_type, **kwargs)
    method_name = "format_{}".format(resource)
    if not hasattr(instance, method_name):
        raise AttributeError("方法{}不存在于{}的格式化类中".format(method_name, cloud_type))
    return getattr(instance, method_name)


def _get_format_instance(cloud_type, **kwargs):
    """
    获取格式化资源数据的实例
    :param kwargs:  公共数据 如region、zone等，多个资源都需要。这里保留位置备用
    :type kwargs:
    :return:
    :rtype:
    """
    if not cloud_type:
        raise Exception("cloud_type参数不能为空")
    kwargs["cloud_type"] = cloud_type
    return FormatResourceFactory().create_cloud_format_obj(**kwargs)


class FormatResourceFactory:
    """根据云平台创建对应云平台格式化类实例"""

    _instance_lock = threading.Lock()

    def __init__(self):
        self.cloud_dict = {
            CloudPlatform.Aliyun: "_create_aliyun_instance",
            CloudPlatform.Apsara: "_create_aliyun_instance",  # 结构与阿里云一致
            CloudPlatform.QCloud: "_create_qcloud_instance",
            CloudPlatform.HuaweiCloud: "_create_huaweicloud_instance",
            CloudPlatform.VMware: "_create_vmware_instance",
            CloudPlatform.OpenStack: "_create_openstack_instance",
            CloudPlatform.TCE: "_create_tce_instance",
            CloudPlatform.FusionCloud: "_create_fusioncloud_instance",
            CloudPlatform.TKE_CLOUD: "_create_tkecloud_instance",
            CloudPlatform.TDSQL: "_create_tdsql_instance",
            CloudPlatform.EasyStack: "_create_easystack_instance",
            CloudPlatform.Cas: "_create_cas_instance",
            CloudPlatform.TSF: "_create_tsf_instance",
            CloudPlatform.QingCloud: "_create_qingcloud_instance",
            CloudPlatform.AmazonAws: "_create_amazonaws_instance",
            CloudPlatform.QingCloudPrivate: "_create_qingcloud_instance",
        }

    def __new__(cls, *args, **kwargs):
        """
        支持多线程的单例模式
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """
        if not hasattr(FormatResourceFactory, "_instance"):
            with FormatResourceFactory._instance_lock:
                if not hasattr(FormatResourceFactory, "_instance"):
                    FormatResourceFactory._instance = object.__new__(cls)
        return FormatResourceFactory._instance

    @staticmethod
    def _create_amazonaws_instance(**kwargs):
        return AmazonAwsFormatResource(**kwargs)

    @staticmethod
    def _create_qingcloud_instance(**kwargs):
        return QingCloudFormatResource(**kwargs)

    @staticmethod
    def _create_tsf_instance(**kwargs):
        return TSFResourceFormat(**kwargs)

    @staticmethod
    def _create_aliyun_instance(**kwargs):
        return AliyunResourceFormat(**kwargs)

    @staticmethod
    def _create_qcloud_instance(**kwargs):
        return QCloudResourceFormat(**kwargs)

    @staticmethod
    def _create_huaweicloud_instance(**kwargs):
        return HuaweicloudFormatResource(**kwargs)

    @staticmethod
    def _create_openstack_instance(**kwargs):
        return OpenStackFormatResource(**kwargs)

    @staticmethod
    def _create_tce_instance(**kwargs):
        return TCEResourceFormat(**kwargs)

    @staticmethod
    def _create_fusioncloud_instance(**kwargs):
        return FusionCloudFormatResource(**kwargs)

    @staticmethod
    def _create_tkecloud_instance(**kwargs):
        return TKECloudResourceFormat(**kwargs)

    @staticmethod
    def _create_easystack_instance(**kwargs):
        return EasyStackFormatResource(**kwargs)

    @staticmethod
    def _create_cas_instance(**kwargs):
        return CasFormatResource(**kwargs)

    @staticmethod
    def _create_vmware_instance(**kwargs):
        return VmWareResourceFormat(**kwargs)

    @staticmethod
    def _create_tdsql_instance(**kwargs):
        return TDSQLResourceFormat(**kwargs)

    def create_cloud_format_obj(self, **kwargs):
        cloud_type = kwargs["cloud_type"]
        if cloud_type not in self.cloud_dict:
            raise Exception("传入参数{}有误，无法找到对应云平台。请参照云平台枚举取值".format(cloud_type))
        return getattr(self, self.cloud_dict[cloud_type])(**kwargs)
