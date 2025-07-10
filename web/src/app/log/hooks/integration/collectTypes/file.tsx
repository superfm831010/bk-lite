import { useVectorConfig } from '../collectors/file/vector';

export const useFileConfig = () => {
  const vector = useVectorConfig();
  const plugins = {
    Vector: vector,
  };

  return {
    type: 'file',
    plugins,
  };
};
