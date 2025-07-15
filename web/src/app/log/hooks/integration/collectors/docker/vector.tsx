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
          getFormItems: (configForm: TableDataItem) => {
            const sources =
              configForm.child?.content?.sources?.[
                pluginConfig.collect_type + '_' + configForm.rowId
              ];
            const transforms =
              configForm?.child?.content?.transforms?.[
                `multiline_${configForm.rowId}`
              ];
            return commonFormItems.getCommonFormItems({
              hiddenFormItems: {
                include_containers: !sources?.include_containers,
                exclude_containers: !sources?.exclude_containers,
                start_pattern:
                  !transforms?.start_pattern &&
                  transforms?.start_pattern !== '',
              },
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
              start_pattern: multiline.start_pattern || null,
            };
          },
          getParams: (formData: TableDataItem, configForm: TableDataItem) => {
            const sources = configForm.child.content.sources;
            const transforms =
              configForm.child.content.transforms[
                `multiline_${formData.rowId}`
              ];
            const key = pluginConfig.collect_type + '_' + formData.rowId;
            sources[key].docker_host = formData.docker_host;
            sources[key].include_containers = formData.include_containers;
            sources[key].exclude_containers = formData.exclude_containers;
            if (transforms) {
              transforms.start_pattern = formData.start_pattern;
            }
            return configForm;
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
