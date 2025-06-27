import { useJettyJmx } from '../../plugins/middleware/jettyJmx';

export const useJettyJmxConfig = () => {
  const clickJettyJmx = useJettyJmx();

  const plugins = {
    'Jetty-JMX': clickJettyJmx,
  };

  return {
    instance_type: 'jetty',
    dashboardDisplay: [],
    tableDiaplay: [],
    groupIds: {},
    plugins,
  };
};
