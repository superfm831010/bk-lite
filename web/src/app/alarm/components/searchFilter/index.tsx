import React, { useState, useEffect } from 'react';
import searchFilterStyle from './index.module.scss';
import { Select, Input } from 'antd';
import {
  SearchFilterProps,
  SearchFilterCondition,
} from '@/app/alarm/types/alarms';

const SearchFilter: React.FC<SearchFilterProps> = ({ onSearch, attrList }) => {
  const [searchAttr, setSearchAttr] = useState<string>('');
  const [searchValue, setSearchValue] = useState<any>('');

  useEffect(() => {
    if (attrList.length) {
      setSearchAttr(attrList[0].attr_id);
    }
  }, [attrList.length]);

  const onSearchValueChange = (value: any) => {
    setSearchValue(value);
    const selectedAttr: any = attrList.find((attr) => attr.attr_id === searchAttr);
    const condition: SearchFilterCondition = {
      field: searchAttr,
      type: selectedAttr?.attr_type,
      value,
    };
    onSearch(condition, value);
  };

  const onSearchAttrChange = (attr: string) => {
    setSearchAttr(attr);
    setSearchValue('');
  };

  const renderSearchInput = () => {
    const selectedAttr = attrList.find((attr) => attr.attr_id === searchAttr);
    switch (selectedAttr?.attr_type) {
      case 'enum':
        return (
          <Select
            allowClear
            className="value"
            style={{ width: 250 }}
            value={searchValue}
            onChange={(e) => onSearchValueChange(e)}
            onClear={() => onSearchValueChange('')}
          >
            {selectedAttr.option?.map((opt: any) => (
              <Select.Option key={opt.id} value={opt.id}>
                {opt.name}
              </Select.Option>
            ))}
          </Select>
        );
      default:
        return (
          <Input
            allowClear
            className="value"
            style={{ width: 250 }}
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            onClear={() => onSearchValueChange('')}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onSearchValueChange(searchValue);
              }
            }}
          />
        );
    }
  };

  return (
    <div className={searchFilterStyle.searchFilter + ' flex items-center'}>
      <Select
        className={searchFilterStyle.attrList}
        style={{ width: 120 }}
        value={searchAttr}
        onChange={onSearchAttrChange}
      >
        {attrList.map((attr) => (
          <Select.Option key={attr.attr_id} value={attr.attr_id}>
            {attr.attr_name}
          </Select.Option>
        ))}
      </Select>
      {renderSearchInput()}
    </div>
  );
};

export default SearchFilter;
