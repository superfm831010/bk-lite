import React from 'react';
import { Form, Radio, Checkbox, Spin } from 'antd';
import { useTranslation } from '@/utils/i18n';
import CustomTable from '@/components/custom-table';
import {
  DataPermission,
  PermissionConfig,
  ModulePermissionConfig,
  ProviderPermissionConfig,
  ModuleContentProps,
  PermissionTypeSelectorProps,
  AllPermissionsSelectorProps,
  PermissionTableColumnsProps,
  SpecificDataTableProps
} from '@/app/system-manager/types/permission';

const PermissionTypeSelector: React.FC<PermissionTypeSelectorProps> = ({
  type,
  module,
  subModule,
  handleTypeChange,
  isEditable
}) => {
  const { t } = useTranslation();
  
  // 确保使用正确的子模块值 - 优先使用 activeSubModule（叶子节点）
  const actualSubModule = subModule;
  
  return (
    <Form.Item label={t('system.permission.type')} className="mb-2">
      <Radio.Group
        value={type}
        onChange={(e) => handleTypeChange(e, module, actualSubModule)}
        disabled={!isEditable}
      >
        <Radio value="all">{t('system.permission.allData')}</Radio>
        <Radio value="specific">{t('system.permission.specificData')}</Radio>
      </Radio.Group>
    </Form.Item>
  );
};

const AllPermissionsSelector: React.FC<AllPermissionsSelectorProps> = ({
  currentModule,
  module,
  subModule,
  handleAllPermissionChange,
  isEditable
}) => {
  const { t } = useTranslation();
  return (
    <Form.Item label={t('system.permission.permissions')} className="mt-4">
      <div className="flex space-x-4">
        <Checkbox
          checked={currentModule?.allPermissions?.view ?? true}
          onChange={(e) => handleAllPermissionChange(e, module, 'view', subModule)}
          disabled={!isEditable}
        >
          {t('system.permission.view')}
        </Checkbox>
        <Checkbox
          checked={currentModule?.allPermissions?.operate ?? true}
          disabled={!isEditable || !(currentModule?.allPermissions?.view ?? true)}
          onChange={(e) => handleAllPermissionChange(e, module, 'operate', subModule)}
        >
          {t('system.permission.operate')}
        </Checkbox>
      </div>
    </Form.Item>
  );
};

const PermissionTableColumns = ({
  handleSpecificDataChange,
  activeKey,
  activeSubModule,
  module,
  subModule
}: PermissionTableColumnsProps) => {
  const { t } = useTranslation();
  return [
    {
      title: t('system.permission.data'),
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: t('system.permission.actions'),
      key: 'actions',
      render: (_: unknown, record: DataPermission) => (
        <div className="flex space-x-4">
          <Checkbox
            checked={record.view}
            onChange={() => handleSpecificDataChange(
              { ...record, view: !record.view },
              module || activeKey,
              'view',
              subModule || (subModule ? activeSubModule : undefined)
            )}
          >
            {t('system.permission.view')}
          </Checkbox>
          <Checkbox
            checked={record.operate}
            disabled={!record.view}
            onChange={() => handleSpecificDataChange(
              { ...record, operate: !record.operate },
              module || activeKey,
              'operate',
              subModule || (subModule ? activeSubModule : undefined)
            )}
          >
            {t('system.permission.operate')}
          </Checkbox>
        </div>
      ),
    },
  ];
};

const SpecificDataTable: React.FC<SpecificDataTableProps> = ({
  isEditable,
  isModuleLoading,
  dataKey,
  moduleData,
  columns,
  pagination,
  handleTableChange,
  module,
  subModule,
  activeKey,
  activeSubModule,
  handleSpecificDataChange
}) => {
  const { t } = useTranslation();
  
  // 使用传入的 subModule 或 activeSubModule 作为实际的子模块参数
  const actualSubModule = subModule || activeSubModule;
  
  return (
    <Spin spinning={isModuleLoading}>
      {isEditable ? (
        <CustomTable
          rowKey="id"
          scroll={{ y: '300px' }}
          columns={columns}
          dataSource={moduleData[dataKey] || []}
          rowSelection={{
            type: 'checkbox',
            selectedRowKeys: (moduleData[dataKey] || [])
              .filter(item => item.view)
              .map(item => item.id),
            onSelect: (record: DataPermission, selected: boolean) => {
              const newRecord = {
                ...record,
                view: selected,
                operate: selected ? record.operate : false
              };

              handleSpecificDataChange(
                newRecord,
                activeKey,
                'view',
                activeKey === 'provider' ? actualSubModule : undefined
              );
            },
            onSelectAll: (selected: boolean, selectedRows: DataPermission[], changeRows: DataPermission[]) => {
              changeRows.forEach(record => {
                const newRecord = {
                  ...record,
                  view: selected,
                  operate: selected ? record.operate : false
                };

                handleSpecificDataChange(
                  newRecord,
                  activeKey,
                  'view',
                  activeKey === 'provider' ? actualSubModule : undefined
                );
              });
            }
          }}
          pagination={{
            current: pagination.current || 1,
            pageSize: pagination.pageSize || 10,
            total: pagination.total || 0,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `${t('system.permission.total')} ${total} ${t('system.permission.items')}`,
            onChange: (page: number, pageSize: number) => handleTableChange(
              { current: page, pageSize, total: pagination.total },
              {},
              {},
              module,
              actualSubModule // 确保传递正确的子模块参数
            )
          }}
          className="mt-4"
        />
      ) : (
        <div className="text-gray-500 mt-4">{t('system.permission.noSpecificDataSupport')}</div>
      )}
    </Spin>
  );
};

const ModuleContent: React.FC<ModuleContentProps> = ({
  module,
  subModule,
  permissions,
  loading,
  moduleData,
  pagination,
  activeKey,
  activeSubModule,
  handleTypeChange,
  handleAllPermissionChange,
  handleSpecificDataChange,
  handleTableChange
}) => {
  let currentModule: PermissionConfig | undefined;

  // 递归查找多层级权限配置的辅助函数
  const findPermissionConfig = (
    permissionState: any,
    module: string,
    targetSubModule?: string
  ): PermissionConfig | undefined => {
    if (!targetSubModule) {
      // 没有子模块，直接返回模块配置
      const modulePermission = permissionState[module];
      return modulePermission?.__type === 'module' 
        ? modulePermission as ModulePermissionConfig
        : undefined;
    }
    
    const modulePermission = permissionState[module];
    if (!modulePermission || modulePermission.__type !== 'provider') {
      return undefined;
    }
    
    const providerConfig = modulePermission as ProviderPermissionConfig;
    
    // 递归查找函数 - 在所有层级中查找匹配的 targetSubModule
    const findInAllLevels = (config: any, target: string): PermissionConfig | undefined => {
      // 检查当前层级是否直接包含目标子模块
      if (config[target] && typeof config[target] === 'object' && config[target].type !== undefined) {
        return config[target] as PermissionConfig;
      }
      
      // 递归查找所有子级
      for (const key in config) {
        if (key === '__type') continue; // 跳过类型标识符
        
        const value = config[key];
        if (value && typeof value === 'object' && value.type === undefined) {
          // 这是一个中间层级，继续递归查找
          const found = findInAllLevels(value, target);
          if (found) return found;
        }
      }
      return undefined;
    };
    
    return findInAllLevels(providerConfig, targetSubModule);
  };

  // 检查当前模块是否有子模块（通过检查permissions结构判断）
  const modulePermission = permissions[module];
  const hasSubModules = modulePermission && modulePermission.__type === 'provider';

  if (subModule && hasSubModules) {
    // 有子模块的情况，使用递归查找函数来获取多层级权限配置
    currentModule = findPermissionConfig(permissions, module, subModule);
  } else {
    // 没有子模块的情况，直接使用模块配置
    currentModule = permissions[module] as ModulePermissionConfig;
  }

  const type = currentModule?.type || 'all';
  const dataKey = subModule ? `${module}_${subModule}` : module;
  const isModuleLoading = loading[dataKey] || false;
  const isEditable = true;

  const columns = PermissionTableColumns({
    handleSpecificDataChange,
    activeKey,
    activeSubModule,
    module,
    subModule
  });

  return (
    <div>
      <div className="mb-4">
        <PermissionTypeSelector
          type={type}
          module={module}
          subModule={subModule}
          handleTypeChange={handleTypeChange}
          isEditable={isEditable}
        />

        {type === 'all' ? (
          <AllPermissionsSelector
            currentModule={currentModule}
            module={module}
            subModule={subModule}
            handleAllPermissionChange={handleAllPermissionChange}
            isEditable={isEditable}
          />
        ) : (
          <SpecificDataTable
            isEditable={isEditable}
            isModuleLoading={isModuleLoading}
            dataKey={dataKey}
            moduleData={moduleData}
            columns={columns}
            pagination={pagination[dataKey] || { current: 1, pageSize: 10, total: 0 }}
            handleTableChange={handleTableChange}
            module={module}
            subModule={subModule}
            activeKey={activeKey}
            activeSubModule={activeSubModule}
            handleSpecificDataChange={handleSpecificDataChange}
          />
        )}
      </div>
    </div>
  );
};

export default ModuleContent;
export {
  PermissionTypeSelector,
  AllPermissionsSelector,
  PermissionTableColumns,
  SpecificDataTable
};
