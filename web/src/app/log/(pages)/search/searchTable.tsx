'use client';
import React, { useState } from 'react';
import { CopyTwoTone, CaretDownFilled } from '@ant-design/icons';
import { Button } from 'antd';
import CustomPopover from './customPopover';
import CustomTable from '@/components/custom-table';
import { useTranslation } from '@/utils/i18n';
import searchStyle from './index.module.scss';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import { TableDataItem } from '@/app/log/types';
import { SearchTableProps } from '@/app/log/types/search';
import { useHandleCopy } from '@/app/log/hooks';
import { useLocalizedTime } from '@/hooks/useLocalizedTime';

const SearchTable: React.FC<SearchTableProps> = ({
  dataSource,
  pagination,
  expand,
  loading = false,
  onChange,
  addToQuery,
}) => {
  const { t } = useTranslation();
  const { handleCopy } = useHandleCopy();
  const { convertToLocalizedTime } = useLocalizedTime();
  const [expandedRowKeys, setExpandedRowKeys] = useState<React.Key[]>([]);

  const columns = [
    {
      title: 'timestrap',
      dataIndex: '_time',
      key: '_time',
      width: 150,
      render: (val: string) => (
        <EllipsisWithTooltip
          text={convertToLocalizedTime(val, 'YYYY-MM-DD HH:mm:ss')}
          className="w-full overflow-hidden text-ellipsis whitespace-nowrap"
        ></EllipsisWithTooltip>
      ),
    },
    {
      title: 'source',
      dataIndex: '_msg',
      key: '_msg',
    },
  ];

  const getRowExpandRender = (record: TableDataItem) => {
    return (
      <div
        className={`w-[calc(100vw-90px)] min-w-[1180px] ${searchStyle.detail}`}
      >
        <div className={searchStyle.title}>
          <div className="mb-1">
            <CopyTwoTone
              className="cursor-pointer mr-[4px]"
              onClick={() => handleCopy(record._msg)}
            />
            <span className="font-[500] break-all">{record._msg}</span>
          </div>
          <div>
            <span className="mr-3">
              <span className="text-[var(--color-text-3)]">
                {t('common.time')}：
              </span>
              <span>
                {convertToLocalizedTime(
                  record._time,
                  'YYYY-MM-DD HH:mm:ss.SSS'
                )}
              </span>
            </span>
            <span className="mr-3">
              <span className="text-[var(--color-text-3)]">
                {t('log.integration.collectType')}：
              </span>
              <span>{record.collect_type || '--'}</span>
            </span>
          </div>
        </div>
        <ul>
          {Object.entries(record)
            .map(([key, value]) => ({
              label: key,
              value,
            }))
            .map((item: TableDataItem, index: number) => (
              <li className="flex items-start mt-[10px]" key={index}>
                <div className="flex items-center min-w-[250px] w-[250px] mr-[10px]">
                  <CustomPopover
                    title={`${item.label} = string`}
                    content={(onClose) => (
                      <ul>
                        <li>
                          <Button
                            type="link"
                            size="small"
                            onClick={() => {
                              onClose();
                              addToQuery(item, 'field');
                            }}
                          >
                            {t('log.search.addToQuery')}
                          </Button>
                        </li>
                      </ul>
                    )}
                  >
                    <div
                      className={`flex max-w-[100%] cursor-pointer ${searchStyle.field}`}
                    >
                      <EllipsisWithTooltip
                        text={item.label}
                        className="w-full overflow-hidden text-[var(--color-text-3)] text-ellipsis whitespace-nowrap"
                      ></EllipsisWithTooltip>
                      <span className="text-[var(--color-text-3)]">:</span>
                      <CaretDownFilled
                        className={`text-[12px] ${searchStyle.arrow}`}
                      />
                    </div>
                  </CustomPopover>
                </div>
                <span className={`${searchStyle.value}`}>
                  <CustomPopover
                    title={`${item.label} = ${item.value}`}
                    content={(onClose) => (
                      <ul>
                        <li>
                          <Button
                            type="link"
                            size="small"
                            onClick={() => {
                              onClose();
                              addToQuery(item, 'value');
                            }}
                          >
                            {t('log.search.addToQuery')}
                          </Button>
                        </li>
                      </ul>
                    )}
                  >
                    <span className="break-all">{item.value}</span>
                    <CaretDownFilled
                      className={`text-[12px] ${searchStyle.arrow}`}
                    />
                  </CustomPopover>
                </span>
              </li>
            ))}
        </ul>
      </div>
    );
  };

  return (
    <CustomTable
      columns={columns}
      dataSource={dataSource}
      loading={loading}
      rowKey="_time"
      scroll={{
        y: `calc(100vh - ${expand ? '568px' : '488px'})`,
      }}
      pagination={pagination}
      expandable={{
        columnWidth: 40,
        expandedRowRender: (record) => getRowExpandRender(record),
        expandedRowKeys: expandedRowKeys,
        onExpandedRowsChange: (keys) => setExpandedRowKeys(keys as React.Key[]),
      }}
      onChange={onChange}
    />
  );
};

export default SearchTable;
