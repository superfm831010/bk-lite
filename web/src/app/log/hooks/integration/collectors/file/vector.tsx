import React from 'react';
import { IntegrationLogInstance } from '@/app/log/types/integration';
import { TableDataItem } from '@/app/log/types';
import { useFileVectorFormItems } from '../../common/fileVectorFormItems';
import { cloneDeep } from 'lodash';

export const useVectorConfig = () => {
  const commonFormItems = useFileVectorFormItems();
  const pluginConfig = {
    collector: 'Vector',
    collect_type: 'file',
    icon: 'jiaoxuerizhiPC',
  };

  return {
    getConfig: (extra: {
      dataSource?: IntegrationLogInstance[];
      mode: 'manual' | 'auto' | 'edit';
      onTableDataChange?: (data: IntegrationLogInstance[]) => void;
    }) => {
      const disabledForm = {
        file_path: false,
      };
      const formItems = <>{commonFormItems.getCommonFormItems(disabledForm)}</>;
      const configs = {
        auto: {
          formItems: commonFormItems.getCommonFormItems(),
          initTableItems: {},
          defaultForm: {},
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
            const path =
              formData?.child?.content?.sources?.[
                pluginConfig.collect_type + '_' + formData.rowId
              ]?.include?.[0] || null;
            return {
              file_path: path,
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
