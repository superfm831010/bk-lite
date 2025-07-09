import { useVectorConfig } from '../collectors/docker/vector';

export const useDockerConfig = () => {
  const vector = useVectorConfig();
  const plugins = {
    Vector: vector,
  };

  return {
    type: 'docker',
    plugins,
  };
};
