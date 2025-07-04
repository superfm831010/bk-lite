import { LevelMap, AlgorithmParam } from "@/app/mlops/types";

const LEVEL_MAP: LevelMap = {
  critical: '#F43B2C',
  error: '#D97007',
  warning: '#FFAD42',
};

const TrainStatus = {
  pending: 'default',
  running: 'processing',
  completed: 'success',
  failed: 'error'
};

const TypeContent: Record<string, any> = {
  is_test_data: 'test',
  is_train_data: 'train',
  is_val_data: 'validate',
};

const TrainText = {
  pending: 'notStarted',
  running: 'inProgress',
  completed: 'completed',
  failed: 'failed'
};

const AlgorithmsParams: Record<string, AlgorithmParam[]> = {
  'RandomForest': [
    { name: 'n_estimators', type: 'randint', default: [100, 500] },
    { name: 'max_depth', type: 'randint', default: [10, 50] },
    { name: 'min_samples_split', type: 'randint', default: [2, 10] },
    { name: 'min_samples_leaf', type: 'randint', default: [1, 10] },
    {
      name: 'max_features',
      type: 'choice',
      default: 'none',
      options: [
        { label: 'sqrt', value: 'sqrt' },
        { label: 'log2', value: 'log2' },
        { label: 'none', value: 'none' },
      ]
    },
    {
      name: 'bootstrap',
      type: 'choice',
      default: 'false',
      options: [
        { label: 'true', value: 'true' },
        { label: 'false', value: 'false' },
      ]
    },
    {
      name: 'class_weight',
      type: 'choice',
      default: 'none',
      options: [
        { label: 'balanced', value: 'balanced' },
        { label: 'balanced_subsample', value: 'balanced_subsample' },
        { label: 'none', value: 'none' },
      ]
    },
  ]
};

const AlgorithmsType: Record<string, any> = {
  'RandomForest': {
    n_estimators: 'randint',
    max_depth: 'randint',
    min_samples_split: 'randint',
    min_samples_leaf: 'randint',
    max_features: 'choice',
    bootstrap: 'choice',
    class_weight: 'choice'
  }
};

type TRAIN_STATUS = 'not_started' | 'in_progress' | 'completed' | 'failed';



export {
  LEVEL_MAP,
  TrainStatus,
  TrainText,
  TypeContent,
  AlgorithmsParams,
  AlgorithmsType,
  type TRAIN_STATUS
}