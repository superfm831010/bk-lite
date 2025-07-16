'use client';

import React, { useState } from 'react';
import ComponentSelector from './components/compSelector';
import ComponentConfig from './components/compConfig';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
// @ts-expect-error missing type declarations for react-grid-layout
import GridLayout, { WidthProvider } from 'react-grid-layout';
import { Button, Empty, Dropdown, Menu, Modal, Select } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { LayoutItem } from '@/app/ops-analysis/types/dashBoard';
import { DirItem } from '@/app/ops-analysis/types';
import { SaveOutlined, PlusOutlined, MoreOutlined } from '@ant-design/icons';
import TimeSelector from '@/components/time-selector';
import {
  getWidgetComponent,
  needsGlobalTimeSelector,
  needsGlobalInstanceSelector,
} from './components/registry';

interface DashboardProps {
  selectedDashboard?: DirItem | null;
}

const ResponsiveGridLayout = WidthProvider(GridLayout);

const Dashboard: React.FC<DashboardProps> = ({ selectedDashboard }) => {
  const { t } = useTranslation();
  const [addModalVisible, setAddModalVisible] = useState(false);
  const [layout, setLayout] = useState<LayoutItem[]>([]);
  const [configDrawerVisible, setConfigDrawerVisible] = useState(false);
  const [currentConfigItem, setCurrentConfigItem] = useState<any>(null);
  const [globalTimeRange, setGlobalTimeRange] = useState<any>(null);
  const [globalInstances, setGlobalInstances] = useState<string[]>([]);

  const timeDefaultValue = {
    selectValue: 0,
    rangePickerVaule: null,
  };

  const handleTimeChange = (timeData: any) => {
    setGlobalTimeRange(timeData);
    console.log('Global time range changed:', timeData);
  };

  const handleRefresh = () => {
    console.log('Dashboard refreshed');
  };

  const needGlobalTimeSelector = needsGlobalTimeSelector(layout);

  const needGlobalInstanceSelector = needsGlobalInstanceSelector(layout);

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

  const openAddModal = () => setAddModalVisible(true);

  const handleAddComponent = (widget: string, config?: any) => {
    const newId = (layout.length + 1).toString();
    const newWidget: LayoutItem = {
      i: newId,
      x: (layout.length % 3) * 4,
      y: Infinity,
      w: 4,
      h: 3,
      widget: widget,
      title: config?.name || `New ${widget}`,
      config: config,
    };
    setLayout((prev) => [...prev, newWidget]);
    setAddModalVisible(false);
  };
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
            <h2 className="text-xl font-semibold text-gray-800 mb-2">
              {selectedDashboard.name}
            </h2>
            {selectedDashboard.description && (
              <p className="text-sm text-gray-600">
                {selectedDashboard.description}
              </p>
            )}
          </div>
        )}
        <div className="flex items-center space-x-4 justify-between">
          {
            <div className="flex items-center space-x-2 py-2">
              {needGlobalTimeSelector && (
                <>
                  <span className="text-sm text-gray-600">
                    {t('dashboard.timeRange')}:
                  </span>
                  <TimeSelector
                    onlyTimeSelect
                    defaultValue={timeDefaultValue}
                    onChange={handleTimeChange}
                    onRefresh={handleRefresh}
                  />
                </>
              )}
              {needGlobalInstanceSelector && (
                <>
                  <span className="text-sm text-gray-600">
                    {t('dashboard.instanceList')}:
                  </span>
                  <Select
                    mode="multiple"
                    placeholder={t('dashboard.selectInstance')}
                    style={{ width: 200 }}
                    value={globalInstances}
                    onChange={handleInstancesChange}
                    options={[
                      { label: '实例-1', value: 'instance1' },
                      { label: '实例-2', value: 'instance2' },
                      { label: '实例-3', value: 'instance3' },
                    ]}
                  />
                </>
              )}
            </div>
          }
          <Button icon={<SaveOutlined />} onClick={handleSave}>
            {t('dashboard.save')}
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

      <div className="flex-1 bg-[#F0F2F5] rounded-lg overflow-auto">
        {(() => {
          if (layout.length === 0) {
            return (
              <div className="h-full flex flex-col items-center justify-center">
                <Empty
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                  description={
                    <span className="text-gray-500">
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

                let backgroundColor = '#fff';
                if ((item.config as any)?.bgColor) {
                  backgroundColor = (item.config as any).bgColor;
                }

                return (
                  <div
                    key={item.i}
                    className="widget bg-white rounded-lg shadow-sm overflow-hidden p-4 flex flex-col"
                    style={{ backgroundColor }}
                  >
                    <div className="widget-header pb-4 flex justify-between items-center">
                      <h4 className="text-md font-medium text-gray-800">
                        {item.title}
                      </h4>
                      <Dropdown overlay={menu} trigger={['click']}>
                        <button className="no-drag text-gray-500 hover:text-gray-800 transition-colors">
                          <MoreOutlined style={{ fontSize: '20px' }} />
                        </button>
                      </Dropdown>
                    </div>
                    <div className="widget-body flex-1 h-full rounded-b overflow-hidden">
                      <WidgetComponent
                        config={item.config}
                        globalTimeRange={globalTimeRange}
                        globalInstances={globalInstances}
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
