import { LevelMap,  } from "@/app/mlops/types";
import { AlgorithmParam } from "@/app/mlops/types/task"; 

const LEVEL_MAP: LevelMap = {
  critical: '#F43B2C',
  error: '#D97007',
  warning: '#FFAD42',
};

const TRAIN_STATUS_MAP = { 
  pending: 'default',
  running: 'processing',
  completed: 'success',
  failed: 'error'
};

const TYPE_CONTENT: Record<string, any> = { 
  is_test_data: 'test',
  is_train_data: 'train',
  is_val_data: 'validate',
};

const TYPE_COLOR: Record<string, any> = { 
  is_test_data: 'orange',
  is_train_data: 'blue',
  is_val_data: 'green',
};

const TRAIN_TEXT = { 
  pending: 'notStarted',
  running: 'inProgress',
  completed: 'completed',
  failed: 'failed'
};

const ALGORITHMS_PARAMS: Record<string, AlgorithmParam[]> = { 
  'RandomForest': [
    { name: 'n_estimators', type: 'randint', default: [100, 500] },
    { name: 'max_depth', type: 'randint', default: [10, 50] },
    { name: 'min_samples_split', type: 'randint', default: [2, 10] },
    { name: 'min_samples_leaf', type: 'randint', default: [1, 10] },
    {
      name: 'max_features',
      type: 'choice',
      default: ['none'],
      options: [
        { label: 'sqrt', value: 'sqrt' },
        { label: 'log2', value: 'log2' },
        { label: 'none', value: 'none' },
      ]
    },
    {
      name: 'bootstrap',
      type: 'choice',
      default: ['false'],
      options: [
        { label: 'true', value: 'true' },
        { label: 'false', value: 'false' },
      ]
    },
    {
      name: 'class_weight',
      type: 'choice',
      default: ['none'],
      options: [
        { label: 'balanced', value: 'balanced' },
        { label: 'balanced_subsample', value: 'balanced_subsample' },
        { label: 'none', value: 'none' },
      ]
    },
  ]
};

const ALGORITHMS_TYPE: Record<string, any> = { 
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
  TRAIN_STATUS_MAP,
  TRAIN_TEXT,
  TYPE_CONTENT,
  ALGORITHMS_PARAMS,
  ALGORITHMS_TYPE,
  type TRAIN_STATUS,
  TYPE_COLOR
}