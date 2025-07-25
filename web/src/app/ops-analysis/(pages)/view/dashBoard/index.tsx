'use client';

import React, { useState, useEffect } from 'react';
import dayjs from 'dayjs';
import ComponentSelector from './components/compSelector';
import ComponentConfig from './components/baseConfig';
import TimeSelector from '@/components/time-selector';
// @ts-expect-error missing type declarations for react-grid-layout
import GridLayout, { WidthProvider } from 'react-grid-layout';
import { Button, Empty, Dropdown, Menu, Modal, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { LayoutItem } from '@/app/ops-analysis/types/dashBoard';
import { DirItem } from '@/app/ops-analysis/types';
import { SaveOutlined, PlusOutlined, MoreOutlined } from '@ant-design/icons';
import { useDashBoardApi } from '@/app/ops-analysis/api/dashBoard';
import { getWidgetComponent, getWidgetMeta } from './components/registry';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

interface DashboardProps {
  selectedDashboard?: DirItem | null;
}

const ResponsiveGridLayout = WidthProvider(GridLayout);

const Dashboard: React.FC<DashboardProps> = ({ selectedDashboard }) => {
  const { t } = useTranslation();
  const { getInstanceList } = useDashBoardApi();
  const [addModalVisible, setAddModalVisible] = useState(false);
  const [layout, setLayout] = useState<LayoutItem[]>([]);
  const [configDrawerVisible, setConfigDrawerVisible] = useState(false);
  const [currentConfigItem, setCurrentConfigItem] = useState<any>(null);
  const [globalInstances, setGlobalInstances] = useState<string[]>([]);
  const [instanceOptions, setInstanceOptions] = useState<any[]>([]);
  const [instancesLoading, setInstancesLoading] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [timeRefreshKey, setTimeRefreshKey] = useState(0);
  const timeDefaultValue = {
    selectValue: 10080,
    rangePickerVaule: null,
  };
  const getInitialTimeRange = () => {
    const endTime = dayjs().valueOf();
    const startTime = dayjs()
      .subtract(timeDefaultValue.selectValue, 'minute')
      .valueOf();
    return { start: startTime, end: endTime };
  };
  const [globalTimeRange, setGlobalTimeRange] = useState<any>(
    getInitialTimeRange()
  );

  // 直接从 layout 判断是否需要全局选择器
  const needGlobalTimeSelector = layout.some((item) => {
    const meta = getWidgetMeta(item.widget);
    const filterType =
      item.config?.filterType || meta.defaultConfig?.filterType;
    return filterType === 'selector';
  });

  const needGlobalInstanceSelector = false;

  const componentNeedsGlobalTime = (item: LayoutItem) => {
    const meta = getWidgetMeta(item.widget);
    const filterType =
      item.config?.filterType || meta.defaultConfig?.filterType;
    return filterType === 'selector';
  };

  // 获取实例列表
  useEffect(() => {
    const fetchInstanceList = async () => {
      try {
        setInstancesLoading(true);
        const response: any = await getInstanceList();
        setInstanceOptions(response.data || []);
      } catch (error) {
        console.error('获取实例列表失败:', error);
        setInstanceOptions([]);
      } finally {
        setInstancesLoading(false);
      }
    };

    fetchInstanceList();
  }, []);

  const openAddModal = () => setAddModalVisible(true);

  const handleTimeChange = (timeData: any) => {
    setGlobalTimeRange(timeData);
    setTimeRefreshKey((prev) => prev + 1);
  };

  const handleRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const handleInstancesChange = (instances: string[]) => {
    setGlobalInstances(instances);
    console.log('Global instances changed:', instances);
  };

  const onLayoutChange = (newLayout: any) => {
    setLayout((prevLayout) => {
      return prevLayout.map((item) => {
        const newItem = newLayout.find((l: any) => l.i === item.i);
        if (newItem) {
          return { ...item, ...newItem };
        }
        return item;
      });
    });
  };

  const handleAddComponent = (widget: string, config?: any) => {
    const newId = (layout.length + 1).toString();
    const widgetMeta = getWidgetMeta(widget);
    const newWidget: LayoutItem = {
      i: newId,
      x: (layout.length % 3) * 4,
      y: Infinity,
      w: 4,
      h: 3,
      widget: widget,
      title: config?.name || `New ${widget}`,
      description: widgetMeta?.description || '',
      config: {
        ...widgetMeta?.defaultConfig,
        ...config,
      },
    };
    setLayout((prev) => [...prev, newWidget]);
    setAddModalVisible(false);
  };

  // TODO
  const handleSave = () => {
    console.log('Save layout:', layout);
  };

  const removeWidget = (id: string) => {
    setLayout(layout.filter((item) => item.i !== id));
  };

  const handleEdit = (id: string) => {
    const item = layout.find((i) => i.i === id);
    setCurrentConfigItem(item);
    setConfigDrawerVisible(true);
  };

  const handleConfigConfirm = (values: any) => {
    setLayout((prevLayout) =>
      prevLayout.map((item) => {
        if (item.i === currentConfigItem?.i) {
          return {
            ...item,
            title: values.name,
            config: {
              ...item.config,
              ...values,
            },
          };
        }
        return item;
      })
    );
    setConfigDrawerVisible(false);
    setCurrentConfigItem(null);
  };

  const handleConfigClose = () => {
    setConfigDrawerVisible(false);
    setCurrentConfigItem(null);
  };

  const handleDelete = (id: string) => {
    Modal.confirm({
      title: t('deleteTitle'),
      content: t('deleteContent'),
      okText: t('confirm'),
      cancelText: t('cancel'),
      centered: true,
      onOk: async () => {
        try {
          removeWidget(id);
        } catch {
          console.error(t('common.operateFailed'));
        }
      },
    });
  };

  return (
    <div className="h-full flex-1 p-4 pb-0 overflow-auto flex flex-col ">
      <div className="w-full mb-4 flex items-center justify-between rounded-lg shadow-sm">
        {selectedDashboard && (
          <div className="p-2 pt-0">
            <h2 className="text-xl font-semibold mb-2 text-[var(--color-text-1)]">
              {selectedDashboard.name}
            </h2>
            {selectedDashboard.description && (
              <p className="text-sm text-[var(--color-text-2)]">
                {selectedDashboard.description}
              </p>
            )}
          </div>
        )}
        <div className="flex items-center space-x-4 justify-between">
          {
            <div className="flex items-center space-x-2 py-2">
              <TimeSelector
                onlyRefresh={!needGlobalTimeSelector}
                defaultValue={timeDefaultValue}
                onChange={handleTimeChange}
                onRefresh={handleRefresh}
              />
              {needGlobalInstanceSelector && (
                <>
                  <span className="text-sm text-[var(--color-text-2)]">
                    {t('dashboard.instanceList')}:
                  </span>
                  <Select
                    mode="multiple"
                    loading={instancesLoading}
                    placeholder={t('dashboard.selectInstance')}
                    style={{ width: 200 }}
                    value={globalInstances}
                    onChange={handleInstancesChange}
                    options={instanceOptions}
                  />
                </>
              )}
            </div>
          }
          <Button icon={<SaveOutlined />} onClick={handleSave}>
            {t('common.save')}
          </Button>
          <Button
            type="dashed"
            icon={<PlusOutlined />}
            onClick={openAddModal}
            style={{ borderColor: '#1677ff', color: '#1677ff' }}
          >
            {t('dashboard.addComponent')}
          </Button>
        </div>
      </div>

      <div className="flex-1 bg-[var(--color-fill-1)] rounded-lg overflow-auto">
        {(() => {
          if (!layout.length) {
            return (
              <div className="h-full flex flex-col items-center justify-center">
                <Empty
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                  description={
                    <span className="text-[var(--color-text-2)]">
                      {t('dashboard.addView')}
                    </span>
                  }
                >
                  <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={openAddModal}
                  >
                    {t('dashboard.addView')}
                  </Button>
                </Empty>
              </div>
            );
          }
          return (
            <ResponsiveGridLayout
              className="layout w-full flex-1"
              layout={layout}
              onLayoutChange={onLayoutChange}
              cols={12}
              rowHeight={100}
              margin={[12, 12]}
              containerPadding={[12, 12]}
              draggableCancel=".no-drag"
            >
              {layout.map((item) => {
                const WidgetComponent = getWidgetComponent(item.widget);
                const menu = (
                  <Menu>
                    <Menu.Item key="edit" onClick={() => handleEdit(item.i)}>
                      {t('common.edit')}
                    </Menu.Item>
                    <Menu.Item
                      key="delete"
                      onClick={() => handleDelete(item.i)}
                    >
                      {t('common.delete')}
                    </Menu.Item>
                  </Menu>
                );

                return (
                  <div
                    key={item.i}
                    className="widget bg-[var(--color-bg-1)] rounded-lg shadow-sm overflow-hidden p-4 flex flex-col"
                  >
                    <div className="widget-header pb-4 flex justify-between items-center">
                      <div className="flex-1">
                        <h4 className="text-md font-medium text-[var(--color-text-1)]">
                          {item.title}
                        </h4>
                        {item.description && (
                          <p className="text-sm text-[var(--color-text-2)] mt-1">
                            {item.description}
                          </p>
                        )}
                      </div>
                      <Dropdown overlay={menu} trigger={['click']}>
                        <button className="no-drag text-[var(--color-text-2)] hover:text-[var(--color-text-1)] transition-colors">
                          <MoreOutlined style={{ fontSize: '20px' }} />
                        </button>
                      </Dropdown>
                    </div>
                    <div className="widget-body flex-1 h-full rounded-b overflow-hidden">
                      <WidgetComponent
                        key={`${item.i}-${
                          componentNeedsGlobalTime(item)
                            ? `${refreshKey}-${timeRefreshKey}`
                            : refreshKey
                        }`}
                        config={item.config}
                        globalTimeRange={globalTimeRange}
                        globalInstances={globalInstances}
                        refreshKey={refreshKey}
                      />
                    </div>
                  </div>
                );
              })}
            </ResponsiveGridLayout>
          );
        })()}
      </div>

      <ComponentSelector
        visible={addModalVisible}
        onAdd={handleAddComponent}
        onCancel={() => setAddModalVisible(false)}
      />
      <ComponentConfig
        open={configDrawerVisible}
        item={currentConfigItem}
        onConfirm={handleConfigConfirm}
        onClose={handleConfigClose}
      />
    </div>
  );
};

export default Dashboard;
