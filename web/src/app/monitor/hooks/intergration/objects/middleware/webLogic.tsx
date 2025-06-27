import { useWebLogicJmx } from '../../plugins/middleware/webLogicJmx';

export const useWebLogicConfig = () => {
  const webLogicPlugin = useWebLogicJmx();

  const plugins = {
    'WebLogic-JMX': webLogicPlugin,
  };

  return {
    instance_type: 'weblogic',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins,
  };
};
