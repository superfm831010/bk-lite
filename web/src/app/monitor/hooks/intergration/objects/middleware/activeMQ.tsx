import { useActiveMQTelegraf } from '../../plugins/middleware/activeMQTelegraf';
import { useActiveMQJmx } from '../../plugins/middleware/activeMQJmx';

export const useActiveMQConfig = () => {
  const activeMQPlugin = useActiveMQTelegraf();
  const activeMQJmxPlugin = useActiveMQJmx();

  const plugins = {
    ActiveMQ: activeMQPlugin,
    'ActiveMQ-JMX': activeMQJmxPlugin,
  };

  return {
    instance_type: 'activemq',
    dashboardDisplay: [],
    tableDiaplay: [{ type: 'value', key: 'activemq_topic_consumer_count' }],
    groupIds: {},
    plugins,
  };
};
