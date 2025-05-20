# -*- coding: utf-8 -*-
from common.cmp.cloud_apis.cloud_object.base import Application
from common.cmp.cloud_apis.resource_apis.resource_format.tce.tce_format import TCEResourceFormat


class TSFResourceFormat(TCEResourceFormat):
    def format_application(self, object_json, **kwargs):
        return Application(
            resource_id=object_json.ApplicationId,
            resource_name=object_json.ApplicationName,
            cloud_type=self.cloud_type,
            application_type=object_json.ApplicationType,
            microservice_type=object_json.MicroserviceType,
            prog_lang=object_json.ProgLang,
            application_runtime_type=object_json.ApplicationRuntimeType or "",
            application_resource_type=object_json.ApplicationResourceType,
            create_time=object_json.CreateTime,
            update_time=object_json.UpdateTime,
            apigateway_service_id=object_json.ApigatewayServiceId or "",
            group_count=object_json.GroupCount,
            instance_count=object_json.InstanceCount,
            runinstance_count=object_json.RunInstanceCount,
        ).to_dict()
