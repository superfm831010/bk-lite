import { useMemo } from 'react';
import { TableDataItem } from '@/app/log/types';
import { useFileConfig } from './collectTypes/file';
import { useExecConfig } from './collectTypes/exec';
import { useSyslogConfig } from './collectTypes/syslog';
import { useDockerConfig } from './collectTypes/docker';

export const useCollectTypeConfig = () => {
  const fileConfig = useFileConfig();
  const execConfig = useExecConfig();
  const syslogConfig = useSyslogConfig();
  const dockerConfig = useDockerConfig();

  const configs: any = useMemo(
    () => ({
      file: fileConfig,
      exec: execConfig,
      syslog: syslogConfig,
      docker: dockerConfig,
    }),
    []
  );

  // 获取指定插件的手动/自动/编辑配置模式
  const getCollectTypeConfig = (data: {
    mode: 'manual' | 'auto' | 'edit';
    type: string;
    collector: string;
    dataSource?: TableDataItem[];
    onTableDataChange?: (data: TableDataItem[]) => void;
  }) => {
    const collectTypeCfg =
      configs[data.type]?.plugins?.[data.collector]?.getConfig(data);
    const config = {
      collector: '',
      icon: '',
    };
    let defaultCollectTypeCfg: any = {
      getParams: () => ({
        instance_id: '',
        instance_name: '',
      }),
      getFormItems: () => null,
      configText: '',
    };
    if (data.mode === 'auto') {
      defaultCollectTypeCfg = {
        formItems: null,
        initTableItems: {},
        defaultForm: {},
        columns: [],
        getParams: () => ({}),
      };
    }
    return (
      collectTypeCfg || {
        ...config,
        ...defaultCollectTypeCfg,
      }
    );
  };

  return {
    configs,
    getCollectTypeConfig,
  };
};
