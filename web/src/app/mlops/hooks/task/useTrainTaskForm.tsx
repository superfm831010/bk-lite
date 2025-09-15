import { useAnomalyForm, useRasaForm } from './forms';
import type { Option } from '@/types';

// 统一的任务表单 hooks 出入口
interface UseTaskFormProps {
  datasetOptions: Option[];
  activeTag: string[];
  onSuccess: () => void;
}

const useTaskForm = ({ datasetOptions, activeTag, onSuccess }: UseTaskFormProps) => {
  const [activeType] = activeTag;

  // 始终调用所有可能的 hooks，避免条件调用
  const anomalyFormResult = useAnomalyForm({ datasetOptions, activeTag, onSuccess });
  const rasaFormResult = useRasaForm({ datasetOptions, activeTag, onSuccess });

  // 根据 activeTag 返回对应的结果，但不在条件中调用 hooks
  switch (activeType) {
    case 'anomaly':
      return anomalyFormResult;
    case 'rasa':
      return rasaFormResult;
    default:
      // 默认使用异常检测表单
      return anomalyFormResult;
  }
};

export {
  useTaskForm,
  useAnomalyForm
};
