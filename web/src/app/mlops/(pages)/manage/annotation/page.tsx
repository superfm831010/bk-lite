"use client";
import {
  useEffect,
  useState,
  useMemo,
  memo,
  useCallback
} from "react";
import { useSearchParams } from 'next/navigation';
import { cloneDeep } from "lodash";
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import { useTranslation } from "@/utils/i18n";
import { TYPE_CONTENT } from "@/app/mlops/constants";
import useMlopsManageApi from "@/app/mlops/api/manage";
import {
  Button,
  message,
  Spin,
  TablePaginationConfig,
  Tag
} from "antd";
import Aside from "./aside";
import Icon from '@/components/icon';
import LineChart from "@/app/mlops/components/charts/lineChart";
import CustomTable from "@/components/custom-table";
import { ColumnItem, TableDataItem, Pagination, } from '@/app/mlops/types';
import { AnomalyTrainData } from '@/app/mlops/types/manage';
import sideMenuStyle from './aside/index.module.scss';

interface AnnotationData {
  timestamp: number;
  value: number;
  label: number;
  index?: number;
  [key: string]: unknown;
}

const AnnotationIntro = memo(() => {
  const searchParams = useSearchParams();
  const folder_name = searchParams.get('folder_name');
  return (
    <div className="flex h-[58px] flex-row items-center">
      <Icon
        type="shiyongwendang"
        className="h-16 w-16"
        style={{ height: '36px', width: '36px', color: 'blue' }}
      ></Icon>
      <h1 className="ml-2 text-center truncate">{folder_name}</h1>
    </div>
  );
});
AnnotationIntro.displayName = 'AnnotationIntro';

const Topsection = memo(() => {
  const { t } = useTranslation();
  return (
    <div className="flex flex-col h-[90px] p-4 overflow-hidden">
      <h1 className="text-lg truncate w-full mb-1">{t('datasets.title')}</h1>
      <p className="text-xs truncate w-full min-w-[1000px] mt-[8px]">
        {t('datasets.detail')}
      </p>
    </div>
  );
});
Topsection.displayName = 'Topsection';

const AnnotationPage = () => {
  const searchParams = useSearchParams();
  const { t } = useTranslation();
  const { getAnomalyTrainDataInfo, getAnomalyTrainData, labelingData } = useMlopsManageApi();
  const { convertToLocalizedTime } = useLocalizedTime();
  const [menuItems, setMenuItems] = useState<AnomalyTrainData[]>([]);
  const [tableData, setTableData] = useState<TableDataItem[]>([]);
  const [currentFileData, setCurrentFileData] = useState<AnnotationData[]>([]);
  const [loadingState, setLoadingState] = useState({
    loading: false,
    chartLoading: false,
    saveLoading: false,
  });
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [isChange, setIsChange] = useState<boolean>(false);
  const [flag, setFlag] = useState<boolean>(true);
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20,
  });
  const [timeline, setTimeline] = useState<any>({
    startIndex: 0,
    endIndex: 0,
  });

  const tagsData = ['is_train_data', 'is_val_data', 'is_test_data'];

  const colmuns: ColumnItem[] = useMemo(() => {
    return [
      {
        title: t('common.time'),
        key: 'timestamp',
        dataIndex: 'timestamp',
        width: 80,
        align: 'center',
        render: (_, record) => {
          const time = new Date(record.timestamp * 1000).toISOString();
          return <p>{convertToLocalizedTime(time.toString(), 'YYYY-MM-DD HH:mm:ss')}</p>;
        },
      },
      {
        title: t('datasets.value'),
        key: 'value',
        dataIndex: 'value',
        align: 'center',
        width: 30,
        render: (_, record) => {
          const value = Number(record.value).toFixed(2);
          return <p>{value}</p>
        },
      },
      {
        title: t('datasets.labelResult'),
        key: 'label',
        dataIndex: 'label',
        width: 100,
        align: 'center',
        hidden: true
      },
      {
        title: t('common.action'),
        key: 'action',
        dataIndex: 'action',
        align: 'center',
        width: 30,
        render: (_, record) => {
          return (
            <Button color="danger" variant="link" onClick={() => handleDelete(record)}>
              {t('common.delete')}
            </Button>
          )
        }
      }
    ];
  }, [t, convertToLocalizedTime]);

  const pagedData = useMemo(() => {
    if (!tableData.length) return [];
    return tableData.slice(
      (pagination.current! - 1) * pagination.pageSize!,
      pagination.current! * pagination.pageSize!
    );
  }, [tableData, pagination.current, pagination.pageSize]);

  useEffect(() => {
    getCurrentFileData();
  }, [searchParams]);

  useEffect(() => {
    setPagination((prev) => {
      return {
        ...prev,
        total: tableData.length
      }
    });
  }, [tableData]);

  useEffect(() => {
    if (currentFileData.length && flag) {
      setTimeline({
        startIndex: 0,
        endIndex: currentFileData.length > 10 ? Math.floor(currentFileData.length / 10) : (currentFileData.length > 1 ? currentFileData.length - 1 : 0)
      });
      setFlag(false);
    }
  }, [currentFileData]);

  const handleLabelData = useCallback((data: any[], points: number[] | undefined) => {
    const _data = cloneDeep(data).map((item, index) => ({
      ...item,
      index
    }));
    if (!points) {
      setCurrentFileData(data);
      setTableData([]);
      return;
    }
    points.forEach(item => {
      _data[item] = {
        ..._data[item],
        label: 1
      }
    });
    setCurrentFileData(_data);
    setTableData(_data.filter((item) => item.label === 1))
  }, []);

  const getCurrentFileData = useCallback(async () => {
    setLoadingState(prev => ({ ...prev, loading: true, chartLoading: true }));
    const id = searchParams.get('id');
    const folder_id = searchParams.get('folder_id');

    try {
      const fileList = await getAnomalyTrainData({
        dataset: folder_id as string
      });
      const data = await getAnomalyTrainDataInfo(id as string, true, true);
      const { is_train_data, is_val_data, is_test_data } = data;
      const activeTypes = Object.entries({ is_train_data, is_val_data, is_test_data })
        .filter(([, value]) => value === true)
        .map(([key]) => key);
      handleLabelData(data?.train_data, data?.metadata?.anomaly_point);
      setSelectedTags(activeTypes);
      setMenuItems(fileList);
    } catch (e) {
      console.log(e);
    } finally {
      setLoadingState(prev => ({ ...prev, loading: false, chartLoading: false }));
    }
  }, [searchParams]);

  const onXRangeChange = useCallback((data: any[]) => {
    if (!isChange) setIsChange(true);
    setLoadingState(prev => ({ ...prev, chartLoading: true }));
    if (!currentFileData.length) {
      setLoadingState(prev => ({ ...prev, chartLoading: false }));
      return;
    }
    try {
      const minTime = data[0].unix();
      const maxTime = data[1].unix();
      let newData;
      if (minTime === maxTime) {
        newData = currentFileData.map((item: any) =>
          item.timestamp === minTime ? { ...item, label: 1 } : item
        );
        setCurrentFileData(newData);
      } else {
        newData = currentFileData.map((item: any, index) =>
          item.timestamp >= minTime && item.timestamp <= maxTime
            ? { ...item, label: 1, index }
            : item
        );
      }
      const _tableData = newData.filter((item: any) => item.label === 1);
      setTableData(_tableData);
      setCurrentFileData(newData);
    } finally {
      setLoadingState(prev => ({ ...prev, chartLoading: false }));
    }
  }, [currentFileData]);

  const onAnnotationClick = useCallback((value: any[]) => {
    if (!value) return;
    if (!isChange) setIsChange(true);
    setLoadingState(prev => ({ ...prev, chartLoading: true }));
    try {
      const _data: any[] = cloneDeep(currentFileData);
      value.map((item: any) => {
        const index = _data.findIndex((k) => k.timestamp === item.timestamp);
        _data.splice(index, 1, {
          ...item,
          label: item.label ? 0 : 1
        })
      });
      const _tableData = _data.filter((item: any) => item.label === 1);
      setTableData(_tableData);
      setCurrentFileData(_data);
    } finally {
      setLoadingState(prev => ({ ...prev, chartLoading: false }));
    }
  }, [currentFileData]);

  const handleChange = (value: TablePaginationConfig) => {
    setPagination((prev) => {
      return {
        current: value.current as number,
        pageSize: value.pageSize as number,
        total: prev.total as number,
      }
    })
  };

  const handleDelete = useCallback((record: ColumnItem) => {
    setIsChange(true);
    setLoadingState(prev => ({ ...prev, chartLoading: true }));
    try {
      const newData = currentFileData.map((item: any) =>
        item.timestamp === record.timestamp ? { ...item, label: 0 } : item
      );
      const _tableData = newData.filter((item: any) => item.label === 1);
      setCurrentFileData(newData);
      setTableData(_tableData);
    } finally {
      setLoadingState(prev => ({ ...prev, chartLoading: false }));
    }
  }, [currentFileData]);

  const handleSava = useCallback(async () => {
    setLoadingState(prev => ({ ...prev, saveLoading: true }));
    const id = searchParams.get('id');
    try {
      if (!selectedTags.length) {
        message.error(t(`datasets.selectWarn`));
        return;
      }
      const points = tableData.map(item => item.index);
      const params = {
        metadata: {
          anomaly_point: points
        },
        is_train_data: selectedTags.includes('is_train_data'),
        is_val_data: selectedTags.includes('is_val_data'),
        is_test_data: selectedTags.includes('is_test_data')
      }
      await labelingData(id as string, params);
      message.success(t('datasets.saveSuccess'));
      getCurrentFileData();
    } catch (e) {
      console.log(e);
      message.error(t('datasets.saveError'));
    } finally {
      setLoadingState(prev => ({ ...prev, saveLoading: false }));
      setIsChange(false);
    }
  }, [currentFileData, colmuns]);

  const handleCancel = () => {
    getCurrentFileData();
    setIsChange(false);
  };

  const onTimeLineChange = (value: any) => {
    setTimeline(value);
  };

  const handleTagChange = (tag: string, checked: boolean) => {
    if (!isChange) setIsChange(true);
    const nextSelectedTag = checked ? [...selectedTags, tag] : selectedTags.filter((t) => t !== tag);
    setSelectedTags(nextSelectedTag);
  };

  return (
    <div className={`flex w-full h-full text-sm ${sideMenuStyle.sideMenuLayout} grow`}>
      <div className="w-full flex grow flex-1 h-full">
        <Aside
          loading={loadingState.loading}
          menuItems={menuItems}
          isChange={isChange}
          onChange={(value: boolean) => setIsChange(value)}
          changeFlag={(value: boolean) => setFlag(value)}
        >
          <AnnotationIntro />
        </Aside>
        <section className="flex-1 flex flex-col overflow-hidden">
          <div className={`mb-4 w-full rounded-md ${sideMenuStyle.sectionContainer}`}>
            <Topsection />
          </div>
          <div className={`pt-4 pr-4 flex-1 rounded-md overflow-auto ${sideMenuStyle.sectionContainer} ${sideMenuStyle.sectionContext}`}>
            <Spin className="w-full" spinning={loadingState.chartLoading}>
              <div className="flex justify-end gap-2 mb-4">
                <div>
                  <span className="mr-2">文件类型: </span>
                  {tagsData.map((tag) => (
                    <Tag.CheckableTag
                      className={`h-full content-center`}
                      key={tag}
                      checked={selectedTags.includes(tag)}
                      style={{
                        backgroundColor: selectedTags.includes(tag) ? '#1890ff' : '',
                        color: selectedTags.includes(tag) ? `var(--color-secondary)` : `var(--color-text-1)`,
                      }}
                      onChange={(checked) => handleTagChange(tag, checked)}
                    >
                      {t(`datasets.${TYPE_CONTENT[tag]}`)}
                    </Tag.CheckableTag>
                  ))}
                </div>
                <Button className="mr-4" onClick={handleCancel}>{t('common.cancel')}</Button>
                <Button type="primary" loading={loadingState.saveLoading} onClick={handleSava}>{t('common.save')}</Button>
              </div>
              <div className="flex justify-between">
                <div className="w-[74%]" style={{ height: `calc(100vh - 270px)` }}>
                  <LineChart
                    data={currentFileData}
                    timeline={timeline}
                    showDimensionTable
                    showDimensionFilter
                    onXRangeChange={onXRangeChange}
                    onTimeLineChange={onTimeLineChange}
                    onAnnotationClick={onAnnotationClick}
                  />
                </div>
                <div className="w-[25%] anomaly-container" style={{ height: `calc(100vh - 240px)` }}>
                  <CustomTable
                    size="small"
                    rowKey="timestamp"
                    scroll={{ y: 'calc(100vh - 340px)' }}
                    columns={colmuns}
                    dataSource={pagedData}
                    pagination={pagination}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </Spin>
          </div>
        </section>
      </div>
    </div>
  )
};

export default AnnotationPage;