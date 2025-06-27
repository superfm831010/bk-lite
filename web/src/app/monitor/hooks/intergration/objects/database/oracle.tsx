import { useOracleExporter } from '../../plugins/database/oracleExporter';

export const useOracleConfig = () => {
  const oraclePlugin = useOracleExporter();
  const plugins = {
    'Oracle-Exporter': oraclePlugin,
  };

  return {
    instance_type: 'oracle',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins,
  };
};
