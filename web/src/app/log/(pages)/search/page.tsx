'use client';
import React, { useState, useRef, useEffect } from 'react';
import TimeSelector from '@/components/time-selector';
import { TimeSelectorRef } from '@/types';
import {
  SearchOutlined,
  BulbFilled,
  CopyTwoTone,
  CaretDownFilled,
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { Card, Input, Button, Select } from 'antd';
import CustomPopover from './custom-popover';
import CustomTable from '@/components/custom-table';
import { useTranslation } from '@/utils/i18n';
import searchStyle from './index.module.scss';
import Collapse from '@/components/collapse';
import CustomBarChart from '../../components/charts/barChart';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import { Pagination, TableDataItem } from '@/app/log/types';
import { useHandleCopy } from '@/app/log/hooks';

const { Option } = Select;
const dateFormat = 'YYYY-MM-DD HH:mm:ss';

const SearchView: React.FC = () => {
  const { t } = useTranslation();
  const { handleCopy } = useHandleCopy();
  const timeSelectorRef = useRef<TimeSelectorRef>(null);
  const [frequence, setFrequence] = useState<number>(0);
  const [searchText, setSearchText] = useState<string>('');
  const [tableData, setTableData] = useState<any[]>([]);
  const [groupList, setGroupList] = useState<any[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [expand, setExpand] = useState<boolean>(true);
  const [expandedRowKeys, setExpandedRowKeys] = useState<React.Key[]>([]);
  const [logData, setLogData] = useState<TableDataItem[]>([]);

  // 模拟数据加载
  useEffect(() => {
    loadData();
    setGroupList([]);
    setLogData([
      {
        label:
          'filebeat_filebeatfilebeat_filebeatfilebeat_filebeatfilebeat_filebeatfilebeat_',
        value:
          'ewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscsewqtwetuhgfsasadscse',
      },
      {
        label: 'type',
        value: 'filebeat',
      },
    ]);
  }, [frequence]);

  const loadData = () => {
    // 模拟API请求
    const mockData = Array.from({ length: 10 }, (_, i) => ({
      key: i,
      source: `项目 ${i}`,
      date: dayjs().subtract(i, 'day').format(dateFormat),
    }));
    setPagination((pre) => {
      return {
        ...pre,
        total: 10,
      };
    });
    setTableData(mockData);
  };

  const onFrequenceChange = (val: number) => {
    setFrequence(val);
  };

  const onRefresh = () => {
    const val = timeSelectorRef.current?.getValue();
    console.log(val, frequence);
    loadData();
  };

  const onTimeChange = () => {
    const val = timeSelectorRef.current?.getValue();
    console.log(val);
    loadData();
  };

  const handleSearch = () => {
    loadData();
  };

  const handleTableChange = (pagination: any) => {
    setPagination(pagination);
  };

  const columns = [
    { title: 'timestrap', dataIndex: 'date', key: 'date', width: 200 },
    { title: 'source', dataIndex: 'name', key: 'name' },
  ];

  const expandRow = async (expanded: boolean, row: TableDataItem) => {
    console.log(expanded, row);
  };

  const addToQuery = (row: TableDataItem, type: string) => {
    setSearchText((pre: string) => {
      if (type === 'field') {
        return pre ? `${pre} AND ${row.label}:string` : `${row.label}:string`;
      }
      return pre
        ? `${pre} AND ${row.label}:${row.value}`
        : `${row.label}:${row.value}`;
    });
  };

  const getRowExpandRender = (record: TableDataItem) => {
    return (
      <div
        className={`w-[calc(100vw-90px)] min-w-[1180px] ${searchStyle.detail}`}
      >
        <div className={searchStyle.title}>
          <div className="mb-1">
            <CopyTwoTone
              className="cursor-pointer mr-[4px]"
              onClick={() => handleCopy('Jun 26 16:43:08 control')}
            />
            <span className="font-[500] break-all">
              Jun 26 16:43:08 control
              11111111111111111111sxsavfv11111111111111111111sxsavfvfdvwddwqdddeqdccxcdsc2fdfwdc11111111111111111111sxsavfvfdvwddwqdddeqdccxcdsc2fdfwdcfdvwddwqdddeqdccxcdsc2fdfwdc11111111111111111111sxsavfvfdvwddwqdddeqdccxcdsc2fdfwdc
            </span>
          </div>
          <div>
            <span className="mr-2">
              <span className="text-[var(--color-text-3)]">
                {t('common.time')}：
              </span>
              <span>{record.date}</span>
            </span>
            <span className="mr-2">
              <span className="text-[var(--color-text-3)]">
                {t('log.search.receiver')}：
              </span>
              <span>yhd1</span>
            </span>
          </div>
        </div>
        <ul>
          {logData.map((item: TableDataItem, index: number) => (
            <li className="flex items-start mt-[10px]" key={index}>
              <div className="flex items-center w-[250px] mr-[10px]">
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
                    :
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
    <div className={`${searchStyle.search} w-full space-y-3`}>
      <div className="flex justify-end">
        <TimeSelector
          ref={timeSelectorRef}
          defaultValue={{
            selectValue: 15,
            rangePickerVaule: null,
          }}
          onChange={onTimeChange}
          onFrequenceChange={onFrequenceChange}
          onRefresh={onRefresh}
        />
      </div>
      <Card bordered={false} className={searchStyle.searchCondition}>
        <b className="flex mb-[10px]">{t('log.search.searchCriteria')}</b>
        <div className="flex">
          <Select
            style={{
              width: '250px',
            }}
            showSearch
            allowClear
            mode="tags"
            maxTagCount="responsive"
            placeholder={t('common.select')}
          >
            {groupList.map((item) => (
              <Option value={item.id} key={item.id}>
                {item.name}
              </Option>
            ))}
          </Select>
          <Input
            style={{ width: 200 }}
            className="flex-1 mx-[8px]"
            placeholder={t('log.search.searchPlaceHolder')}
            value={searchText}
            addonAfter={
              <BulbFilled style={{ color: 'var(--color-primary)' }} />
            }
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Button
            type="primary"
            icon={<SearchOutlined />}
            onClick={handleSearch}
          >
            {t('common.search')}
          </Button>
        </div>
      </Card>
      <Card bordered={false}>
        <Collapse
          title={t('log.search.histogram')}
          icon={
            <div>
              <span className="mr-2">
                <span className="text-[var(--color-text-3)]">
                  {t('log.search.total')}：
                </span>
                <span>5328</span>
              </span>
              <span className="mr-2">
                <span className="text-[var(--color-text-3)]">
                  {t('log.search.queryTime')}：
                </span>
                <span>2025-06-26 14:28:01</span>
              </span>
              <span className="mr-2">
                <span className="text-[var(--color-text-3)]">
                  {t('log.search.timeConsumption')}：
                </span>
                <span>582ms</span>
              </span>
            </div>
          }
          onToggle={(val) => setExpand(val)}
        >
          <CustomBarChart data={[]} />
        </Collapse>
      </Card>
      <Card bordered={false}>
        <CustomTable
          columns={columns}
          dataSource={tableData}
          scroll={{
            x: 'max-content',
            y: `calc(100vh - ${expand ? '610px' : '456px'})`,
          }}
          pagination={pagination}
          expandable={{
            expandedRowRender: (record) => getRowExpandRender(record),
            expandedRowKeys: expandedRowKeys,
            onExpand: (expanded, record) => {
              expandRow(expanded, record);
            },
            onExpandedRowsChange: (keys) => setExpandedRowKeys(keys as any),
          }}
          onChange={handleTableChange}
        />
      </Card>
    </div>
  );
};

export default SearchView;
