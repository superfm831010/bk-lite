import { useMemo } from 'react';
import { Form, Input, InputNumber, Select, Switch } from 'antd';
import { RASA_CONFIG } from '@/app/mlops/constants';
import type { Option } from '@/app/mlops/types';

/**
 * RASA配置项的类型定义
 */
interface RasaConfigItem {
  name: string;
  type: string;
  options?: Option[];
  dest?: string;
}

/**
 * 表单字段值类型
 */
type FormFieldValue = string | number | boolean | null | undefined;

/**
 * 配置数据类型 - 用于存储RASA组件的配置参数
 */
type ConfigData = Record<string, FormFieldValue>;

/**
 * 表单数据类型 - 用于表单组件
 */
type FormData = Record<string, FormFieldValue>;

/**
 * RASA配置与表单互转的工具Hook
 */
export const useRasaParamsToForm = () => {
  
  /**
   * 将RASA配置数据转换为表单数据
   * @param componentName RASA组件名称 (如: 'DIETClassifier', 'TEDPolicy')
   * @param configData 配置数据对象
   * @returns 表单数据对象
   */
  const configToForm = useMemo(() => {
    return (componentName: string, configData: ConfigData): FormData => {
      const componentConfig = RASA_CONFIG[componentName];
      if (!componentConfig) {
        console.warn(`Unknown RASA component: ${componentName}`);
        return {};
      }

      const formData: FormData = {};
      
      componentConfig.forEach((configItem: RasaConfigItem) => {
        const { name, type } = configItem;
        const value = configData[name];
        
        if (value !== undefined) {
          switch (type) {
            case 'boolean':
              formData[name] = Boolean(value);
              break;
            case 'number':
              formData[name] = typeof value === 'string' ? parseFloat(value) : Number(value);
              break;
            case 'option':
              formData[name] = String(value);
              break;
            case 'string':
            case 'RegExp':
            default:
              formData[name] = String(value);
              break;
          }
        }
      });
      
      return formData;
    };
  }, []);

  /**
   * 将表单数据转换为RASA配置数据
   * @param componentName RASA组件名称
   * @param formData 表单数据对象
   * @returns 配置数据对象
   */
  const formToConfig = useMemo(() => {
    return (componentName: string, formData: FormData): ConfigData => {
      const componentConfig = RASA_CONFIG[componentName];
      if (!componentConfig) {
        console.warn(`Unknown RASA component: ${componentName}`);
        return {};
      }

      const configData: ConfigData = {};
      
      componentConfig.forEach((configItem: RasaConfigItem) => {
        const { name, type } = configItem;
        const value = formData[name];
        
        if (value !== undefined && value !== null && value !== '') {
          switch (type) {
            case 'boolean':
              configData[name] = Boolean(value);
              break;
            case 'number':
              configData[name] = Number(value);
              break;
            case 'option':
              // option类型保持字符串格式，特殊处理布尔值字符串
              if (value === 'True' || value === 'true') {
                configData[name] = true;
              } else if (value === 'False' || value === 'false') {
                configData[name] = false;
              } else {
                configData[name] = String(value);
              }
              break;
            case 'string':
            case 'RegExp':
            default:
              configData[name] = String(value);
              break;
          }
        }
      });
      
      return configData;
    };
  }, []);

  /**
   * 根据配置项生成对应的表单组件
   * @param componentName RASA组件名称
   * @param configItem 配置项定义
   * @returns 表单组件JSX
   */
  const generateFormField = useMemo(() => {
    const FormFieldGenerator = (
      componentName: string,
      configItem: RasaConfigItem
    ) => {
      const { name, type, options, dest } = configItem;
      const label = dest || name;
      
      switch (type) {
        case 'boolean':
          return (
            <Form.Item key={name} name={name} style={{ marginBottom: 0 }} valuePropName="checked">
              <div style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
                <span style={{ fontSize: '14px', color: '#666' }}>{label}</span>
                <Switch size="small" />
              </div>
            </Form.Item>
          );
          
        case 'number':
          return (
            <Form.Item key={name} name={name} style={{ marginBottom: 0 }}>
              <InputNumber
                size="small"
                style={{ width: '120px' }}
                placeholder={label}
              />
            </Form.Item>
          );
          
        case 'option':
          return (
            <Form.Item key={name} name={name} style={{ marginBottom: 0 }}>
              <Select
                size="small"
                style={{ width: '120px' }}
                placeholder={label}
                options={options}
              />
            </Form.Item>
          );
          
        case 'string':
        case 'RegExp':
        default:
          return (
            <Form.Item key={name} name={name} style={{ marginBottom: 0 }}>
              <Input
                size="small"
                style={{ width: '120px' }}
                placeholder={label}
              />
            </Form.Item>
          );
      }
    };
    
    return FormFieldGenerator;
  }, []);

  /**
   * 生成独立的表单字段组件（不依赖Antd Form）
   * @param componentName RASA组件名称
   * @param configItem 配置项定义
   * @param value 当前值
   * @param onChange 值变化回调
   * @returns 表单组件JSX
   */
  const generateStandaloneFormField = useMemo(() => {
    const StandaloneFormFieldGenerator = (
      componentName: string,
      configItem: RasaConfigItem,
      value?: FormFieldValue,
      onChange?: (value: FormFieldValue) => void
    ) => {
      const { name, type, options, dest } = configItem;
      const label = dest || name;
      
      switch (type) {
        case 'boolean':
          return (
            <div key={name} style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
              <span style={{ fontSize: '14px', color: '#666' }}>{label}</span>
              <Switch 
                size="small" 
                checked={Boolean(value)}
                onChange={onChange}
              />
            </div>
          );
          
        case 'number':
          return (
            <InputNumber
              key={name}
              size="small"
              style={{ width: '120px' }}
              min={0}
              value={typeof value === 'number' ? value : undefined}
              onChange={(val) => onChange?.(val)}
              placeholder={label}
            />
          );
          
        case 'option':
          return (
            <Select
              key={name}
              size="small"
              style={{ width: '120px' }}
              value={value as string}
              onChange={onChange}
              placeholder={label}
              options={options}
            />
          );
          
        case 'string':
        case 'RegExp':
        default:
          return (
            <Input
              key={name}
              size="small"
              style={{ width: '120px' }}
              value={value as string}
              onChange={(e) => onChange?.(e.target.value)}
              placeholder={label}
            />
          );
      }
    };
    
    return StandaloneFormFieldGenerator;
  }, []);

  /**
   * 生成独立表单字段列表（不依赖Antd Form）
   * @param componentName RASA组件名称
   * @param formData 表单数据
   * @param onFieldChange 字段变化回调
   * @returns 表单字段JSX数组
   */
  const generateStandaloneFormFields = useMemo(() => {
    return (
      componentName: string,
      formData: FormData = {},
      onFieldChange?: (fieldName: string, value: FormFieldValue) => void
    ) => {
      const componentConfig = RASA_CONFIG[componentName];
      if (!componentConfig) {
        return [];
      }

      return componentConfig.map((configItem: RasaConfigItem) => {
        return generateStandaloneFormField(
          componentName,
          configItem,
          formData[configItem.name],
          (value) => onFieldChange?.(configItem.name, value)
        );
      });
    };
  }, [generateStandaloneFormField]);

  /**
   * 生成完整的表单字段列表
   * @param componentName RASA组件名称
   * @returns 表单字段JSX数组
   */
  const generateFormFields = useMemo(() => {
    return (componentName: string) => {
      const componentConfig = RASA_CONFIG[componentName];
      if (!componentConfig) {
        return [];
      }

      return componentConfig.map((configItem: RasaConfigItem) => {
        return generateFormField(componentName, configItem);
      });
    };
  }, [generateFormField]);

  /**
   * 获取组件的所有可配置参数名称
   * @param componentName RASA组件名称
   * @returns 参数名称数组
   */
  const getConfigParamNames = useMemo(() => {
    return (componentName: string): string[] => {
      const componentConfig = RASA_CONFIG[componentName];
      if (!componentConfig) {
        return [];
      }
      return componentConfig.map(item => item.name);
    };
  }, []);

  /**
   * 获取所有支持的RASA组件名称
   * @returns 组件名称数组
   */
  const getSupportedComponents = useMemo(() => {
    return (): string[] => {
      return Object.keys(RASA_CONFIG);
    };
  }, []);

  /**
   * 验证配置数据的完整性
   * @param componentName RASA组件名称
   * @param configData 配置数据
   * @returns 验证结果和错误信息
   */
  const validateConfig = useMemo(() => {
    return (componentName: string, configData: ConfigData): { 
      isValid: boolean; 
      errors: string[] 
    } => {
      const componentConfig = RASA_CONFIG[componentName];
      if (!componentConfig) {
        return { isValid: false, errors: [`Unknown component: ${componentName}`] };
      }

      const errors: string[] = [];
      
      componentConfig.forEach((configItem: RasaConfigItem) => {
        const { name, type } = configItem;
        const value = configData[name];
        
        if (value !== undefined) {
          switch (type) {
            case 'boolean':
              if (typeof value !== 'boolean') {
                errors.push(`${name} should be a boolean`);
              }
              break;
            case 'number':
              if (typeof value !== 'number' || isNaN(value)) {
                errors.push(`${name} should be a valid number`);
              }
              break;
            case 'option':
              if (configItem.options && !configItem.options.some(opt => opt.value === value)) {
                errors.push(`${name} should be one of: ${configItem.options.map(opt => opt.value).join(', ')}`);
              }
              break;
          }
        }
      });
      
      return { isValid: errors.length === 0, errors };
    };
  }, []);

  return {
    configToForm,
    formToConfig,
    generateFormField,
    generateFormFields,
    generateStandaloneFormField,
    generateStandaloneFormFields,
    getConfigParamNames,
    getSupportedComponents,
    validateConfig
  };
};

// 导出类型定义供外部使用
export type { RasaConfigItem, FormFieldValue, ConfigData, FormData };

export default useRasaParamsToForm;
