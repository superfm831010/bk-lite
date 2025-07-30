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
          getFormItems: () => {
            return commonFormItems.getCommonFormItems({
              hiddenFormItems: {},
              disabledFormItems: {},
            });
          },
          getDefaultForm: (formData: TableDataItem) => {
            const sources =
              formData?.child?.content?.sources?.[
                pluginConfig.collect_type + '_' + formData.rowId
              ] || {};
            const multiline =
              formData?.child?.content?.transforms?.[
                'multiline_' + formData.rowId
              ] || {};
            return {
              docker_host: sources.docker_host || null,
              include_containers: sources.include_containers || null,
              exclude_containers: sources.exclude_containers || null,
              start_pattern: multiline.start_pattern || '',
            };
          },
          getParams: (formData: TableDataItem, configForm: TableDataItem) => {
            return {
              child: {
                id: configForm.child.id,
                content_data: formData,
              },
            };
          },
        },
        manual: {
          defaultForm: {},
          formItems: commonFormItems.getCommonFormItems(),
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
