import useApiClient from '@/utils/request';
import React from 'react';
import {
  SearchParams,
  NodeConfigInfo,
  TreeSortData,
  IntergrationMonitoredObject,
  InstanceInfo,
  SourceFeild,
} from '@/app/monitor/types/monitor';

interface OrderParam {
  id: number;
  sort_order: number;
  [key: string]: any;
}

interface NodeConfigParam {
  configs?: any;
  collect_type?: string;
  monitor_object_id?: number;
  instances?: Omit<IntergrationMonitoredObject, 'key'>[];
}

interface MetricsParam {
  monitor_object_id?: React.Key;
  monitor_plugin_id?: string | number;
  monitor_object_name?: string;
  name?: string;
}

interface InstanceParam {
  page?: number;
  page_size?: number;
  add_metrics?: boolean;
  name?: string;
  vm_params?: any;
}

const useMonitorApi = () => {
  const {
    get,
    post,
    del,
    // put,
    patch,
  } = useApiClient();

  const getMonitorMetrics = async (params: MetricsParam = {}) => {
    return await get(`/monitor/api/metrics/`, {
      params,
    });
  };

  const getMetricsGroup = async (params: MetricsParam = {}) => {
    return await get(`/monitor/api/metrics_group/`, {
      params,
    });
  };

  const getMonitorObject = async (
    params: {
      name?: string;
      add_instance_count?: boolean;
      add_policy_count?: boolean;
    } = {}
  ) => {
    return await get('/monitor/api/monitor_object/', {
      params,
    });
  };

  const getMonitorAlert = async (
    params: {
      status_in?: string[];
      level_in?: string;
      monitor_instance_id?: string;
      monitor_objects?: React.Key;
      content?: string;
      page?: number;
      page_size?: number;
      created_at_after?: string;
      created_at_before?: string;
    } = {}
  ) => {
    return await get(`/monitor/api/monitor_alert/`, {
      params,
    });
  };

  const getMonitorEventDetail = async (
    id?: string | number,
    params: {
      page?: number;
      page_size?: number;
    } = {}
  ) => {
    return await get(`/monitor/api/monitor_event/query/${id}/`, {
      params,
    });
  };

  const getEventRaw = async (id?: string | number) => {
    return await get(`/monitor/api/monitor_event/raw_data/${id}/`);
  };

  const getInstanceQuery = async (
    params: SearchParams = {
      query: '',
    }
  ) => {
    return await get(`/monitor/api/metrics_instance/query_range/`, {
      params,
    });
  };

  const getInstanceList = async (
    objectId?: React.Key,
    params: InstanceParam = {}
  ) => {
    return await get(`/monitor/api/monitor_instance/${objectId}/list/`, {
      params,
    });
  };

  const getInstanceSearch = async (
    objectId: React.Key,
    data: InstanceParam
  ) => {
    return await post(
      `/monitor/api/monitor_instance/${objectId}/search/`,
      data
    );
  };

  const getInstanceGroupRule = async (
    params: {
      monitor_object_id?: React.Key;
    } = {}
  ) => {
    return await get(`/monitor/api/organization_rule/`, {
      params,
    });
  };

  const getInstanceChildConfig = async (data: {
    instance_id?: string | number;
    instance_type?: string;
  }) => {
    return await post(`/monitor/api/node_mgmt/get_instance_asso_config/`, data);
  };

  const getInstanceQueryParams = async (
    name: string,
    params: {
      monitor_object_id?: React.Key;
    } = {}
  ) => {
    return await get(
      `/monitor/api/monitor_instance/query_params_enum/${name}/`,
      {
        params,
      }
    );
  };

  const getMonitorPolicy = async (
    id?: any,
    params: {
      name?: string;
      page?: number;
      page_size?: number;
      monitor_object_id?: React.Key;
    } = {}
  ) => {
    return await get(`/monitor/api/monitor_policy/${id}`, {
      params,
    });
  };

  const getPolicyTemplate = async (params: {
    monitor_object_name?: string | null;
  }) => {
    return await post('/monitor/api/monitor_policy/template/', params);
  };

  const getMonitorPlugin = async (
    params: {
      monitor_object_id?: React.Key | null;
      name?: string;
    } = {}
  ) => {
    return await get('/monitor/api/monitor_plugin/', {
      params,
    });
  };

  const getMonitorNodeList = async (data: {
    cloud_region_id?: number;
    page?: number;
    page_size?: number;
    is_active?: boolean;
  }) => {
    return await post('/monitor/api/node_mgmt/nodes/', data);
  };

  const getSystemChannelList = async () => {
    return await get('/monitor/api/system_mgmt/search_channel_list/');
  };

  const patchMonitorAlert = async (
    id: string | number,
    data: {
      status?: string;
    }
  ) => {
    return await patch(`/monitor/api/monitor_alert/${id}/`, data);
  };

  const patchMonitorPolicy = async (
    id: number,
    data: {
      enable?: boolean;
      source?: SourceFeild;
    }
  ) => {
    return await patch(`/monitor/api/monitor_policy/${id}/`, data);
  };

  const updateInstanceChildConfig = async (data: NodeConfigInfo) => {
    return await post(
      '/monitor/api/node_mgmt/update_instance_child_config/',
      data
    );
  };

  const updateMonitorObject = async (data: TreeSortData[]) => {
    return await post(`/monitor/api/monitor_object/order/`, data);
  };

  const importMonitorPlugin = async (data: any) => {
    return await post(`/monitor/api/monitor_plugin/import/`, data);
  };

  const updateMetricsGroup = async (data: OrderParam[]) => {
    return await post('/monitor/api/metrics_group/set_order/', data);
  };

  const updateMonitorMetrics = async (data: OrderParam[]) => {
    return await post('/monitor/api/metrics/set_order/', data);
  };

  const updateNodeChildConfig = async (data: NodeConfigParam) => {
    return await post(
      '/monitor/api/node_mgmt/batch_setting_node_child_config/',
      data
    );
  };

  const checkMonitorInstance = async (
    id: string,
    data: {
      instance_id: string | number;
      instance_name: string;
    }
  ) => {
    return await post(
      `/monitor/api/monitor_instance/${id}/check_monitor_instance/`,
      data
    );
  };

  const deleteMonitorPolicy = async (id: number | string) => {
    return await del(`/monitor/api/monitor_policy/${id}/`);
  };

  const deleteInstanceGroupRule = async (
    id: number | string,
    params: {
      del_instance_org: boolean;
    }
  ) => {
    return await del(`/monitor/api/organization_rule/${id}/`, { params });
  };

  const setInstancesGroup = async (data: {
    instance_ids: React.Key[];
    organizations: React.Key[];
  }) => {
    return await post(
      `/monitor/api/monitor_instance/set_instances_organizations/`,
      data
    );
  };

  const deleteMonitorInstance = async (data: {
    instance_ids: any;
    clean_child_config: boolean;
  }) => {
    return await post(
      `/monitor/api/monitor_instance/remove_monitor_instance/`,
      data
    );
  };

  const deleteMonitorMetrics = async (id: string | number) => {
    return await del(`/monitor/api/metrics/${id}/`);
  };

  const deleteMetricsGroup = async (id: string | number) => {
    return await del(`/monitor/api/metrics_group/${id}/`);
  };

  const getConfigContent = async (data: { ids: string[] }) => {
    return await post('/monitor/api/node_mgmt/get_config_content/', data);
  };

  const updateMonitorInstance = async (data: InstanceInfo) => {
    return await post(
      '/monitor/api/monitor_instance/update_monitor_instance/',
      data
    );
  };

  const getTemplateObjects = async () => {
    return await get('/monitor/api/monitor_policy/template/monitor_object/');
  };

  const getSnapshot = async (
    params: {
      id?: React.Key;
      page?: number;
      page_size?: number;
    } = {}
  ) => {
    const { id, ...rest } = params;
    return await get(
      `/monitor/api/monitor_alert_metric_snapshot/query/${id}/`,
      {
        params: rest,
      }
    );
  };

  return {
    getMonitorMetrics,
    getMetricsGroup,
    getMonitorObject,
    getMonitorAlert,
    getMonitorEventDetail,
    getEventRaw,
    getInstanceQuery,
    getInstanceList,
    getInstanceSearch,
    getInstanceGroupRule,
    getInstanceChildConfig,
    getInstanceQueryParams,
    getMonitorPolicy,
    getPolicyTemplate,
    getSystemChannelList,
    getMonitorPlugin,
    getMonitorNodeList,
    patchMonitorAlert,
    patchMonitorPolicy,
    updateInstanceChildConfig,
    updateMonitorObject,
    importMonitorPlugin,
    updateMetricsGroup,
    updateMonitorMetrics,
    updateNodeChildConfig,
    checkMonitorInstance,
    deleteMonitorPolicy,
    deleteInstanceGroupRule,
    deleteMonitorInstance,
    deleteMonitorMetrics,
    deleteMetricsGroup,
    getConfigContent,
    updateMonitorInstance,
    setInstancesGroup,
    getTemplateObjects,
    getSnapshot,
  };
};

export default useMonitorApi;
