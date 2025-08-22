'use client';
import React, { useState, useMemo } from 'react';
import { CloseOutlined, MoreOutlined, PlusOutlined } from '@ant-design/icons';
import { Input, Empty, Button } from 'antd';
import CustomPopover from './customPopover';
import { useTranslation } from '@/utils/i18n';
import searchStyle from './index.module.scss';
import { FieldListProps } from '@/app/log/types/search';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import { cloneDeep } from 'lodash';

const DEFAULT_FIELDS = ['timestamp', 'message'];
const DEFAULT_FIELDS_MAP: Record<string, string> = {
  timestamp: '_time',
  message: '_msg',
};

const FieldList: React.FC<FieldListProps> = ({
  fields,
  className = '',
  style = {},
  addToQuery,
  changeDisplayColumns,
}) => {
  const { t } = useTranslation();
  const [searchText, setSearchText] = useState<string>('');
  const [displayFields, setDisplayFields] = useState<string[]>(
    localStorage.getItem('logSearchFields')
      ? JSON.parse(localStorage.getItem('logSearchFields') || '[]')
      : DEFAULT_FIELDS
  );

  const hiddenFields = useMemo(() => {
    return fields.filter(
      (item) => ![...displayFields, '_msg', '_time', '*'].includes(item)
    );
  }, [fields, displayFields]);

  const filteredDisplayFields = useMemo(() => {
    if (!searchText) {
      return displayFields;
    }
    return displayFields.filter((item) =>
      item.toLowerCase().includes(searchText.toLowerCase())
    );
  }, [displayFields, searchText]);

  const filteredHiddenFields = useMemo(() => {
    if (!searchText) {
      return hiddenFields;
    }
    return hiddenFields.filter((item) =>
      item.toLowerCase().includes(searchText.toLowerCase())
    );
  }, [hiddenFields, searchText]);

  const operateFields = (type: string, field: string) => {
    let storageFileds = cloneDeep(displayFields);
    if (type === 'add') {
      storageFileds = [...storageFileds, field];
    } else {
      const index = storageFileds.findIndex((item) => item === field);
      if (index !== -1) {
        storageFileds.splice(index, 1);
      }
    }
    setDisplayFields(storageFileds);
    localStorage.setItem('logSearchFields', JSON.stringify(storageFileds));
    changeDisplayColumns(storageFileds);
  };

  return (
    <div className={`${searchStyle.fieldTree} ${className}`}>
      <Input
        allowClear
        placeholder={t('common.searchPlaceHolder')}
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      ></Input>
      <div className={searchStyle.fields} style={style}>
        <div className={`${searchStyle.displayFields} mb-[10px]`}>
          <div className={searchStyle.title}>
            {t('log.search.displayFields')}
          </div>
          {filteredDisplayFields.length ? (
            <ul className={searchStyle.fieldList}>
              {filteredDisplayFields.map((item: string, index: number) => (
                <li key={index} className={searchStyle.listItem}>
                  <CustomPopover
                    title={item}
                    content={(onClose) => (
                      <ul>
                        <li>
                          <Button
                            type="link"
                            size="small"
                            onClick={() => {
                              onClose();
                              addToQuery(
                                { label: DEFAULT_FIELDS_MAP[item] || item },
                                'field'
                              );
                            }}
                          >
                            {t('log.search.addToQuery')}
                          </Button>
                        </li>
                      </ul>
                    )}
                  >
                    <div className="flex">
                      <EllipsisWithTooltip
                        className={`w-[120px] overflow-hidden text-ellipsis whitespace-nowrap ${searchStyle.label}`}
                        text={item}
                      />
                      <MoreOutlined
                        className={`${searchStyle.operate} cursor-pointer`}
                      />
                    </div>
                  </CustomPopover>
                  {!DEFAULT_FIELDS.includes(item) && (
                    <CloseOutlined
                      className={`${searchStyle.operate} ml-[4px] cursor-pointer scale-[0.8]`}
                      onClick={() => {
                        operateFields('reduce', item);
                      }}
                    />
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
          )}
        </div>
        <div className={`${searchStyle.displayFields} mt-[20px]`}>
          <div className={searchStyle.title}>
            {t('log.search.hiddenFields')}
          </div>
          {filteredHiddenFields.length ? (
            <ul className={searchStyle.fieldList}>
              {filteredHiddenFields.map((item: string, index: number) => (
                <li key={index} className={searchStyle.listItem}>
                  <CustomPopover
                    title={item}
                    content={(onClose) => (
                      <ul>
                        <li>
                          <Button
                            type="link"
                            size="small"
                            onClick={() => {
                              onClose();
                              addToQuery({ label: item }, 'field');
                            }}
                          >
                            {t('log.search.addToQuery')}
                          </Button>
                        </li>
                      </ul>
                    )}
                  >
                    <div className="flex">
                      <EllipsisWithTooltip
                        className={`w-[120px] overflow-hidden text-ellipsis whitespace-nowrap ${searchStyle.label}`}
                        text={item}
                      />
                      <MoreOutlined
                        className={`${searchStyle.operate} cursor-pointer`}
                      />
                    </div>
                  </CustomPopover>
                  <PlusOutlined
                    className={`${searchStyle.operate} ml-[4px] cursor-pointer scale-[0.8]`}
                    onClick={() => {
                      operateFields('add', item);
                    }}
                  />
                </li>
              ))}
            </ul>
          ) : (
            <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
          )}
        </div>
      </div>
    </div>
  );
};

export default FieldList;
