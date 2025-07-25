import React, { useState } from 'react';
import Icon from '@/components/icon';
import ComponentConfigDrawer from './baseConfig';
import { Modal, Menu, List, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { ComponentSelectorProps } from '@/app/ops-analysis/types/dashBoard';
import { getWidgetsByCategory } from './registry';

const ComponentSelector: React.FC<ComponentSelectorProps> = ({
  visible,
  onAdd,
  onCancel,
}) => {
  const { t } = useTranslation();
  const componentCategories = getWidgetsByCategory();
  const categories = Object.keys(componentCategories);
  const [selected, setSelected] = useState(categories[0]);
  const [search, setSearch] = useState('');
  const [drawerVisible, setDrawerVisible] = useState(false);
  const [pendingItem, setPendingItem] = useState<any>(null);
  const [modalOpen, setModalOpen] = useState(visible);
  React.useEffect(() => {
    setModalOpen(visible);
  }, [visible]);
  const items = componentCategories[selected].filter((item) =>
    item.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleConfig = (item: any) => {
    const layoutItem = {
      i: 'temp',
      x: 0,
      y: 0,
      w: 4,
      h: 3,
      widget: item.key,
      title: item.name,
      config: {},
    };
    setPendingItem(layoutItem);
    setDrawerVisible(true);
    setModalOpen(false);
  };
  const handleDrawerConfirm = (values: any) => {
    if (pendingItem) {
      onAdd(pendingItem.widget, values);
    }
    setDrawerVisible(false);
    setPendingItem(null);
  };
  const handleDrawerClose = () => {
    setDrawerVisible(false);
    setPendingItem(null);
    setModalOpen(true);
  };

  return (
    <>
      <Modal
        title={t('dashboard.title')}
        open={modalOpen}
        onCancel={onCancel}
        footer={null}
        width={630}
        style={{ top: '20%' }}
        styles={{ body: { height: '40vh', overflowY: 'auto' } }}
      >
        <div className="flex h-full pt-2">
          <Menu
            mode="inline"
            selectedKeys={[selected]}
            className="w-1/4 h-full [&_.ant-menu-item]:px-2 [&_.ant-menu-item]:py-0 [&_.ant-menu-item]:m-0 [&_.ant-menu-item]:rounded [&_.ant-menu-item]:h-9  overflow-y-auto"
            onClick={({ key }) => setSelected(key)}
            items={categories.map((cat) => ({ key: cat, label: cat }))}
          />
          <div className="w-3/4 pl-2">
            <Input.Search
              placeholder={t('common.searchPlaceHolder')}
              allowClear
              className="mb-4"
              onSearch={(value) => setSearch(value)}
              onClear={() => setSearch('')}
            />
            <List
              size="small"
              bordered
              dataSource={items}
              renderItem={(item) => (
                <List.Item
                  className="cursor-pointer hover:bg-blue-50 flex items-center gap-3 justify-between"
                  onClick={() => handleConfig(item)}
                >
                  <div className="flex flex-col gap-1 leading-relaxed">
                    <span className="font-medium leading-5">{item.name}</span>
                    <span className="text-xs text-[var(--color-text-2)] leading-4">
                      {item.desc}
                    </span>
                  </div>
                  <Icon
                    type={item.icon}
                    className="text-[20px] text-[var(--color-primary)]"
                  />
                </List.Item>
              )}
            />
          </div>
        </div>
      </Modal>
      <ComponentConfigDrawer
        open={drawerVisible}
        item={pendingItem}
        onConfirm={handleDrawerConfirm}
        onClose={handleDrawerClose}
      />
    </>
  );
};

export default ComponentSelector;
