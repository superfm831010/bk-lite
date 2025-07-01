import React, { useMemo, useCallback, useEffect, useState } from 'react';
import { TreeSelect } from 'antd';
import { useUserInfoContext } from '@/context/userInfo';
import { convertGroupTreeToTreeSelectData, getAllTreeKeys } from '@/utils/index';
import { useTranslation } from '@/utils/i18n';

interface GroupTreeSelectProps {
  value?: number[];
  onChange?: (value: number[]) => void;
  placeholder?: string;
  multiple?: boolean;
  disabled?: boolean;
  allowClear?: boolean;
  style?: React.CSSProperties;
  maxTagCount?: number | "responsive";
}

const GroupTreeSelect: React.FC<GroupTreeSelectProps> = ({
  value = [],
  onChange,
  placeholder,
  multiple = true,
  disabled = false,
  allowClear = true,
  style = { width: '100%' },
  maxTagCount = "responsive",
  ...restProps
}) => {
  const { t } = useTranslation();
  const { groupTree } = useUserInfoContext();
  const [internalValue, setInternalValue] = useState<number[]>([]);

  const treeSelectData = useMemo(() => {
    return convertGroupTreeToTreeSelectData(groupTree);
  }, [groupTree]);

  const defaultExpandedKeys = useMemo(() => {
    return getAllTreeKeys(treeSelectData);
  }, [treeSelectData]);

  // Recursively find label by ID
  const findLabelById = useCallback((treeData: any[], targetId: number): string => {
    for (const item of treeData) {
      if (item.value === targetId) {
        return item.title;
      }
      if (item.children) {
        const found = findLabelById(item.children, targetId);
        if (found !== targetId.toString()) {
          return found;
        }
      }
    }
    return targetId.toString();
  }, []);

  // Validate if the target ID exists in the tree data
  const isValidValue = useCallback((targetId: number): boolean => {
    const checkNode = (nodes: any[]): boolean => {
      return nodes.some(node => 
        node.value === targetId || (node.children && checkNode(node.children))
      );
    };
    return checkNode(treeSelectData);
  }, [treeSelectData]);

  // Convert any value to number array safely
  const normalizeValue = useCallback((val: any): number[] => {
    if (!val) return [];
    if (Array.isArray(val)) {
      return val.filter(id => id != null && !isNaN(Number(id))).map(Number);
    }
    const numVal = Number(val);
    return !isNaN(numVal) ? [numVal] : [];
  }, []);

  const valueString = useMemo(() => JSON.stringify(value), [value]);
  
  useEffect(() => {
    if (!treeSelectData.length) return;
    
    const normalizedValue = normalizeValue(value);
    const validValues = normalizedValue.filter(id => isValidValue(id));
    
    // Update internal state only when value actually changes
    const currentValueString = JSON.stringify(internalValue);
    const newValueString = JSON.stringify(validValues);
    
    if (currentValueString !== newValueString) {
      setInternalValue(validValues);
    }
  }, [valueString, treeSelectData, isValidValue, normalizeValue]);

  // Handle value changes
  const handleChange = useCallback((newValue: any) => {
    if (!onChange) return;

    let resultValue: number[] = [];

    if (!newValue || (Array.isArray(newValue) && newValue.length === 0)) {
      resultValue = [];
    } else if (Array.isArray(newValue)) {
      resultValue = newValue
        .map(item => typeof item === 'object' && 'value' in item ? Number(item.value) : Number(item))
        .filter(val => !isNaN(val) && isValidValue(val));
    } else {
      const singleValue = typeof newValue === 'object' && 'value' in newValue 
        ? Number(newValue.value) 
        : Number(newValue);
      
      if (!isNaN(singleValue) && isValidValue(singleValue)) {
        resultValue = [singleValue];
      }
    }

    // Remove duplicates
    resultValue = [...new Set(resultValue)];

    if (!multiple) {
      const currentValue = internalValue[0];
      const newSingleValue = resultValue[0];
      
      if (currentValue === newSingleValue) {
        return;
      }
    }

    setInternalValue(resultValue);
    onChange(resultValue);
  }, [onChange, isValidValue, multiple, internalValue]);

  // Transform value to TreeSelect format
  const transformedValue = useMemo(() => {
    if (!treeSelectData.length || internalValue.length === 0) {
      return multiple ? [] : undefined;
    }

    if (multiple) {
      return internalValue.map(id => ({
        value: id,
        label: findLabelById(treeSelectData, id)
      }));
    } else {
      return {
        value: internalValue[0],
        label: findLabelById(treeSelectData, internalValue[0])
      };
    }
  }, [internalValue, treeSelectData, multiple, findLabelById]);

  return (
    <TreeSelect
      {...restProps}
      multiple={multiple}
      treeData={treeSelectData}
      placeholder={placeholder || `${t('common.selectMsg')}${t('common.group')}`}
      treeCheckable={true}
      treeCheckStrictly={true}
      showCheckedStrategy={TreeSelect.SHOW_ALL}
      treeDefaultExpandAll={true}
      treeDefaultExpandedKeys={defaultExpandedKeys}
      style={style}
      maxTagCount={maxTagCount}
      disabled={disabled}
      allowClear={allowClear}
      value={transformedValue}
      onChange={handleChange}
    />
  );
};

export default GroupTreeSelect;