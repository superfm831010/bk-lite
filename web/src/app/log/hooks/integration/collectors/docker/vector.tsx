import React from 'react';
import { IntegrationLogInstance } from '@/app/log/types/integration';
import { TableDataItem } from '@/app/log/types';
import { useDockerVectorFormItems } from '../../common/dockerVectorFormItems';
import { cloneDeep } from 'lodash';

export const useVectorConfig = () => {
  const commonFormItems = useDockerVectorFormItems();
  const pluginConfig = {
    collector: 'Vector',
    collect_type: 'docker',
    icon: 'docker-run-to-docker-compose',
  };

  return {
    getConfig: (extra: {
      dataSource?: IntegrationLogInstance[];
      mode: 'manual' | 'auto' | 'edit';
      onTableDataChange?: (data: IntegrationLogInstance[]) => void;
    }) => {
      const disabledForm = {
        command: false,
      };
      const formItems = <>{commonFormItems.getCommonFormItems(disabledForm)}</>;
      const configs = {
        auto: {
          formItems: commonFormItems.getCommonFormItems(),
          initTableItems: {},
          defaultForm: {
            docker_host: 'unix:///var/run/docker.sock',
          },
          columns: [],
          getParams: (row: IntegrationLogInstance, config: TableDataItem) => {
            const dataSource = cloneDeep(config.dataSource || []);
            return {
              collector: pluginConfig.collector,
              collect_type: pluginConfig.collect_type,
              configs: [row],
              instances: dataSource.map((item: TableDataItem) => {
                return {
                  ...item,
                  node_ids: [item.node_ids].flat(),
                };
              }),
            };
          },
        },
        edit: {
          formItems,
          getDefaultForm: (formData: TableDataItem) => {
            const host =
              formData?.content?.sources?.[
                pluginConfig.collect_type + '_' + formData.rowId
              ]?.docker_host || null;
            return {
              docker_host: host,
            };
          },
          getParams: (formData: TableDataItem, configForm: TableDataItem) => {
            configForm.content.sources[
              pluginConfig.collect_type + '_' + formData.rowId
            ].docker_host = formData.docker_host;
            return configForm;
          },
        },
        manual: {
          defaultForm: {},
          formItems,
          getParams: (row: TableDataItem) => {
            return {
              instance_name: row.instance_name,
              instance_id: row.instance_id,
            };
          },
          getConfigText: () => '--',
        },
      };
      return {
        ...pluginConfig,
        ...configs[extra.mode],
      };
    },
  };
};
