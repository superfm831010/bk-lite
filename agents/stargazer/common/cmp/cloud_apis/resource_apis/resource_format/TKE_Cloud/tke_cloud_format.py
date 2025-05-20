# -*- coding: utf-8 -*-
"""tke_cloud数据格式转换"""
import threading

from common.cmp.cloud_apis.cloud_object.base import TKECloudClusters, TKECloudNodeList
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource


class TKECloudResourceFormat(FormatResource):
    _instance_lock = threading.Lock()

    @staticmethod
    def format_node_list(object_json, **kwargs):
        return TKECloudNodeList(
            name=object_json["metadata"]["name"],
            generate_name=object_json["metadata"]["generateName"],
            self_link=object_json["metadata"]["selfLink"],
            uuid=object_json["metadata"]["uid"],
            creation_timestamp=object_json["metadata"]["creationTimestamp"],
            finalizers=object_json["spec"]["finalizers"],
            cluster_name=object_json["spec"]["clusterName"],
            type=object_json["spec"]["type"],
            ip=object_json["spec"]["ip"],
            port=object_json["spec"]["port"],
            username=object_json["spec"]["username"],
            phase=object_json["status"]["phase"],
        ).to_dict()

    @staticmethod
    def format_clusters(object_json, **kwargs):
        return TKECloudClusters(
            name=object_json["metadata"]["name"],
            self_link=object_json["metadata"]["selfLink"],
            uuid=object_json["metadata"]["uid"],
            creation_timestamp=object_json["metadata"]["creationTimestamp"],
            labels=object_json["metadata"]["labels"],
            finalizers=object_json["spec"]["finalizers"],
            tenant_id=object_json["spec"]["tenantID"],
            display_name=object_json["spec"]["displayName"],
            type=object_json["spec"]["type"],
            version=object_json["spec"]["version"],
            network_device=object_json["spec"]["networkDevice"],
            clusterCIDR=object_json["spec"]["clusterCIDR"],
            serviceCIDR=object_json["spec"]["serviceCIDR"],
            dns_domain=object_json["spec"]["dnsDomain"],
            public_alternative_names=object_json["spec"]["publicAlternativeNames"],
            features=object_json["spec"]["features"],
            properties=object_json["spec"]["properties"],
            machines=object_json["spec"]["machines"],
            kubelet_extra_args=object_json["spec"]["kubeletExtraArgs"],
            cluster_credential_ref=object_json["spec"]["clusterCredentialRef"],
            etcd=object_json["spec"]["etcd"],
        ).to_dict()
