import React, { useState, useEffect } from 'react';
import { Select, Input, InputNumber, Cascader, Checkbox, DatePicker } from 'antd';
import { UserItem } from '@/app/cmdb/types/assetManage';
import searchFilterStyle from './searchFilter.module.scss';
import { useTranslation } from '@/utils/i18n';
import type { CheckboxProps } from 'antd';
import { SearchFilterProps } from '@/app/cmdb/types/assetData';

const SearchFilter: React.FC<SearchFilterProps> = ({
  attrList,
  userList,
  organizationList,
  onSearch,
}) => {
  const [searchAttr, setSearchAttr] = useState<string>('');
  const [searchValue, setSearchValue] = useState<any>('');
  const [isExactSearch, setIsExactSearch] = useState<boolean>(false);
  const { t } = useTranslation();
  const { RangePicker } = DatePicker;

  useEffect(() => {
    if (attrList.length) {
      setSearchAttr(attrList[0].attr_id);
    }
  }, [attrList.length]);

  const onSearchValueChange = (value: any, isExact?: boolean) => {
    setSearchValue(value);
    const selectedAttr = attrList.find((attr) => attr.attr_id === searchAttr);
    let condition: any = {
      field: searchAttr,
      type: selectedAttr?.attr_type,
      value,
    };
    // 排除布尔类型的false || 多选框没选时的空数组
    if (
      (!value && value !== false && value !== 0) ||
      (Array.isArray(value) && !value.length) ||
      (selectedAttr?.attr_type === 'time' && !(value?.[0] && value?.[1]))
    ) {
      condition = null;
    } else {
      switch (selectedAttr?.attr_type) {
        case 'enum':
          condition.type = typeof value === 'number' ? 'int=' : 'str=';
          break;
        case 'str':
          condition.type = isExact ? 'str=' : 'str*';
          break;
        case 'user':
          condition.type = 'user[]';
          condition.value = [value];
          break;
        case 'int':
          condition.type = 'int=';
          condition.value = +condition.value;
          break;
        case 'organization':
          condition.type = 'list[]';
          break;
        case 'time':
          delete condition.value;
          condition.start = value.at(0);
          condition.end = value.at(-1);
          break;
      }
    }
    onSearch(condition, value);
  };

  const onSearchAttrChange = (attr: string) => {
    setSearchAttr(attr);
    setSearchValue('');
  };

  const onExactSearchChange: CheckboxProps['onChange'] = (e) => {
    setIsExactSearch(e.target.checked);
    onSearchValueChange(searchValue, e.target.checked);
  };

  const renderSearchInput = () => {
    const selectedAttr = attrList.find((attr) => attr.attr_id === searchAttr);
    switch (selectedAttr?.attr_type) {
      case 'user':
        return (
          <Select
            allowClear
            showSearch
            className="value"
            style={{ width: 200 }}
            value={searchValue}
            onChange={(e) => onSearchValueChange(e, isExactSearch)}
            onClear={() => onSearchValueChange('', isExactSearch)}
          >
            {userList.map((opt: UserItem) => (
              <Select.Option key={opt.id} value={opt.id}>
                {opt.username}
              </Select.Option>
            ))}
          </Select>
        );
      case 'enum':
        return (
          <Select
            allowClear
            className="value"
            style={{ width: 200 }}
            value={searchValue}
            onChange={(e) => onSearchValueChange(e, isExactSearch)}
            onClear={() => onSearchValueChange('', isExactSearch)}
          >
            {selectedAttr.option?.map((opt) => (
              <Select.Option key={opt.id} value={opt.id}>
                {opt.name}
              </Select.Option>
            ))}
          </Select>
        );
      case 'bool':
        return (
          <Select
            allowClear
            className="value"
            style={{ width: 200 }}
            value={searchValue}
            onChange={(e) => onSearchValueChange(e, isExactSearch)}
            onClear={() => onSearchValueChange('', isExactSearch)}
          >
            {[
              { id: 1, name: 'Yes' },
              { id: 0, name: 'No' },
            ].map((opt) => (
              <Select.Option key={opt.id} value={opt.id}>
                {opt.name}
              </Select.Option>
            ))}
          </Select>
        );
      case 'organization':
        return (
          <Cascader
            allowClear
            showSearch
            className="value"
            style={{ width: 200 }}
            options={organizationList}
            value={searchValue}
            onChange={(e) => onSearchValueChange(e, isExactSearch)}
            onClear={() => onSearchValueChange([], isExactSearch)}
          />
        );
      case 'time':
        return (
          <RangePicker
            allowClear
            style={{ width: 320 }}
            showTime={{ format: 'HH:mm' }}
            format="YYYY-MM-DD HH:mm"
            onChange={(value, dateString) => {
              onSearchValueChange(dateString, isExactSearch);
            }}
          />
        );
      case 'int':
        return (
          <InputNumber
            className="value"
            style={{ width: 200 }}
            value={searchValue}
            onChange={(val) => {
              setSearchValue(val);
              if (val === undefined || val === null) {
                onSearchValueChange('', isExactSearch);
              }
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onSearchValueChange(searchValue, isExactSearch);
              }
            }}
          />
        );
      default:
        return (
          <Input
            allowClear
            className="value"
            style={{ width: 200 }}
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            onClear={() => onSearchValueChange('', isExactSearch)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onSearchValueChange(searchValue, isExactSearch);
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
      <Checkbox onChange={onExactSearchChange} className='min-w-[103px]'>
        {t('Model.isExactSearch')}
      </Checkbox>
    </div>
  );
};

export default SearchFilter;
