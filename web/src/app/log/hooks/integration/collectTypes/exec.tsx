import { useVectorConfig } from '../collectors/exec/vector';

export const useExecConfig = () => {
  const vector = useVectorConfig();
  const plugins = {
    Vector: vector,
  };

  return {
    type: 'exec',
    plugins,
  };
};
