import { useVectorConfig } from '../collectors/syslog/vector';

export const useSyslogConfig = () => {
  const vector = useVectorConfig();
  const plugins = {
    Vector: vector,
  };

  return {
    type: 'syslog',
    plugins,
  };
};
