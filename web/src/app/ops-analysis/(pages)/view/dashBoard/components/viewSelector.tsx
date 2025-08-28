import React, { useState } from 'react';
import Icon from '@/components/icon';
import { Modal, Menu, List, Input } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { ComponentSelectorProps } from '@/app/ops-analysis/types/dashBoard';
import { getWidgetsByCategory } from '../config/registry';

const ComponentSelector: React.FC<ComponentSelectorProps> = ({
  visible,
  onCancel,
  onOpenConfig,
}) => {
  const { t } = useTranslation();
  const componentCategories = getWidgetsByCategory();
  const categories = Object.keys(componentCategories);
  const [selected, setSelected] = useState(categories[0]);
  const [search, setSearch] = useState('');

  const items = componentCategories[selected].filter((item) =>
    item.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleConfig = (item: any) => {
    const layoutItem = {
      i: '',
      x: 0,
      y: 0,
      w: 4,
      h: 3,
      widget: item.key,
      title: item.name,
      config: {},
    };

    // 调用外部回调来打开配置
    onOpenConfig?.(layoutItem);
    // 关闭当前选择器
    onCancel();
  };

  return (
    <Modal
      title={t('dashboard.title')}
      open={visible}
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
            placeholder={t('common.search')}
            allowClear
            className="mb-4"
            onSearch={(value) => setSearch(value)}
            onClear={() => setSearch('')}
          />
          <List
            size="small"
            dataSource={items}
            renderItem={(item) => (
              <List.Item
                className="cursor-pointer hover:bg-blue-50 flex items-center gap-3 justify-between p-3 border border-gray-200 rounded mb-2 last:mb-0"
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
  );
};

export default ComponentSelector;
