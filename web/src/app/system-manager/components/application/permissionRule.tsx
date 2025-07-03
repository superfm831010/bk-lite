import React, { useState, useEffect, useCallback } from 'react';
import { Tabs, Skeleton } from 'antd';
import type { RadioChangeEvent } from 'antd';
import type { CheckboxChangeEvent } from 'antd/es/checkbox';
import { useSearchParams } from 'next/navigation';
import { useRoleApi } from '@/app/system-manager/api/application';
import { useTranslation } from '@/utils/i18n';

import {
  PermissionRuleProps,
  PermissionsState,
  ModulePermissionConfig,
  ProviderPermissionConfig,
  PermissionConfig,
  DataPermission,
  PaginationInfo
} from '@/app/system-manager/types/permission';
import {
  ModuleItem,
  buildSubModulesMap,
  buildEditableModules,
  buildModuleTree
} from '@/app/system-manager/constants/application';
import ModuleContent from './permission/moduleContent';
import SubModuleTabs from './permission/subModuleTabs';

const PermissionRule: React.FC<PermissionRuleProps> = ({
  value = {},
  modules = [],
  onChange,
  formGroupId
}) => {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const clientId = searchParams ? searchParams.get('clientId') : null;
  const { getAppData, getAppModules } = useRoleApi();

  // Dynamic module configuration state
  const [moduleConfig, setModuleConfig] = useState<ModuleItem[]>([]);
  const [subModuleMap, setSubModuleMap] = useState<{ [key: string]: string[] }>({});
  const [editableModules, setEditableModules] = useState<string[]>([]);
  const [moduleTree, setModuleTree] = useState<{ [key: string]: ModuleItem }>({});
  const [moduleConfigLoading, setModuleConfigLoading] = useState(false);

  // Fetch module configuration only when component mounts and has clientId
  const fetchModuleConfig = useCallback(async () => {
    if (!clientId || moduleConfigLoading) return;

    try {
      setModuleConfigLoading(true);
      const config = await getAppModules({ params: { app: clientId } });
      
      setModuleConfig(config);
      
      const subModules = buildSubModulesMap(config);
      const editable = buildEditableModules(config);
      const tree = buildModuleTree(config);
      
      setSubModuleMap(subModules);
      setEditableModules(editable);
      setModuleTree(tree);
    } catch (error) {
      console.error('Failed to fetch module config:', error);
      setModuleConfig([]);
      setSubModuleMap({});
      setEditableModules([]);
      setModuleTree({});
    } finally {
      setModuleConfigLoading(false);
    }
  }, [clientId]);

  // Only fetch module config once when modules are provided
  useEffect(() => {
    if (modules.length > 0 && moduleConfig.length === 0) {
      fetchModuleConfig();
    }
  }, [modules]);

  // Get permission config from nested structure - supports multi-level recursion
  const getPermissionConfig = useCallback((
    permissions: PermissionsState,
    module: string,
    subModule?: string
  ): PermissionConfig | undefined => {
    if (!subModule) {
      const modulePermission = permissions[module];
      return modulePermission?.__type === 'module' 
        ? modulePermission as ModulePermissionConfig
        : undefined;
    }
    
    const modulePermission = permissions[module];
    if (!modulePermission || modulePermission.__type !== 'provider') {
      return undefined;
    }
    
    const providerConfig = modulePermission as ProviderPermissionConfig;
    
    // Recursive search function - find matching targetSubModule in all levels
    const findInAllLevels = (config: any, target: string): PermissionConfig | undefined => {
      if (config[target] && typeof config[target] === 'object' && config[target].type !== undefined) {
        return config[target] as PermissionConfig;
      }
      
      for (const key in config) {
        if (key === '__type') continue;
        
        const value = config[key];
        if (value && typeof value === 'object' && value.type === undefined) {
          const found = findInAllLevels(value, target);
          if (found) return found;
        }
      }
      return undefined;
    };
    
    return findInAllLevels(providerConfig, subModule);
  }, []);

  // Build initial permission state - supports multi-level permission initialization
  const buildInitialPermissions = useCallback((moduleList: string[], hasValue: boolean) => {
    const initialPermissions: PermissionsState = {};

    moduleList.forEach(module => {
      const moduleConfig = moduleTree[module];
      if (!moduleConfig) {
        // Module without config, treat as regular module
        initialPermissions[module] = {
          __type: 'module',
          type: hasValue && value[module]?.type || 'all',
          allPermissions: {
            view: hasValue && value[module]?.allPermissions?.view !== undefined
              ? value[module]?.allPermissions?.view
              : true,
            operate: hasValue && value[module]?.allPermissions?.operate !== undefined
              ? value[module]?.allPermissions?.operate
              : true
          },
          specificData: hasValue && value[module]?.specificData
            ? value[module]?.specificData.map((item: DataPermission) => ({
              ...item,
              operate: item.operate === true
            })) : []
        };
        return;
      }

      // Module with sub-modules
      if (moduleConfig.children && moduleConfig.children.length > 0) {
        const providerConfig: ProviderPermissionConfig = { __type: 'provider' };

        // Recursively build multi-level permission structure
        const buildNestedPermissions = (
          children: ModuleItem[], 
          currentPath: string[] = [],
          parentConfig: any = providerConfig
        ) => {
          children.forEach(child => {
            const childPath = [...currentPath, child.name];
            
            if (!child.children || child.children.length === 0) {
              // Leaf node, create permission config
              const valueConfig = hasValue && getNestedValue(value, [module, ...childPath]);
              parentConfig[child.name] = {
                type: valueConfig?.type || 'all',
                allPermissions: {
                  view: valueConfig?.allPermissions?.view !== undefined
                    ? valueConfig?.allPermissions?.view
                    : true,
                  operate: valueConfig?.allPermissions?.operate !== undefined
                    ? valueConfig?.allPermissions?.operate
                    : true
                },
                specificData: valueConfig?.specificData
                  ? valueConfig?.specificData.map((item: DataPermission) => ({
                    ...item,
                    operate: item.operate === true
                  })) : []
              };
            } else {
              // Intermediate node, create nested structure
              parentConfig[child.name] = {};
              buildNestedPermissions(child.children, childPath, parentConfig[child.name]);
            }
          });
        };

        buildNestedPermissions(moduleConfig.children);
        initialPermissions[module] = providerConfig;
      } else {
        // No sub-modules, treat as regular module
        initialPermissions[module] = {
          __type: 'module',
          type: hasValue && value[module]?.type || 'all',
          allPermissions: {
            view: hasValue && value[module]?.allPermissions?.view !== undefined
              ? value[module]?.allPermissions?.view
              : true,
            operate: hasValue && value[module]?.allPermissions?.operate !== undefined
              ? value[module]?.allPermissions?.operate
              : true
          },
          specificData: hasValue && value[module]?.specificData
            ? value[module]?.specificData.map((item: DataPermission) => ({
              ...item,
              operate: item.operate === true
            })) : []
        };
      }
    });

    return initialPermissions;
  }, [subModuleMap, value, moduleTree]);

  // Get nested value from object
  const getNestedValue = (obj: any, path: string[]): any => {
    return path.reduce((current, key) => {
      return current && current[key] ? current[key] : undefined;
    }, obj);
  };

  const [permissions, setPermissions] = useState<PermissionsState>(() => {
    const hasValue = value && Object.keys(value).length > 0;
    return buildInitialPermissions(modules, hasValue);
  });

  const [loading, setLoading] = useState<{ [key: string]: boolean }>({});
  const [moduleData, setModuleData] = useState<{ [key: string]: any[] }>({});
  const [pagination, setPagination] = useState<{ [key: string]: { current: number, pageSize: number, total: number } }>({});
  const [activeKey, setActiveKey] = useState<string>('');
  const [activeSubModule, setActiveSubModule] = useState<string>('');

  // Initialize activeKey and activeSubModule when modules and moduleTree are ready
  useEffect(() => {
    if (modules.length > 0 && Object.keys(moduleTree).length > 0 && !activeKey) {
      const firstModule = modules[0];
      setActiveKey(firstModule);
      
      // Check if first module has sub-modules and initialize activeSubModule
      const firstModuleConfig = moduleTree[firstModule];
      if (firstModuleConfig?.children && firstModuleConfig.children.length > 0) {
        // Find the first leaf node for sub-modules
        const getFirstLeafModule = (module: ModuleItem): string => {
          if (module.children && module.children.length > 0) {
            return getFirstLeafModule(module.children[0]);
          }
          return module.name;
        };
        
        const firstLeafModule = getFirstLeafModule(firstModuleConfig);
        setActiveSubModule(firstLeafModule);
      }
    }
  }, [modules, moduleTree, activeKey]);

  // Check and load specific data for the currently active tab when permissions are ready
  useEffect(() => {
    if (!activeKey || Object.keys(permissions).length === 0 || Object.keys(moduleTree).length === 0) {
      return;
    }

    const modulePermission = permissions[activeKey];
    if (!modulePermission) return;

    if (modulePermission.__type === 'module') {
      // Handle regular module
      const moduleConfig = modulePermission as ModulePermissionConfig;
      if (moduleConfig.type === 'specific') {
        loadSpecificData(activeKey);
      }
    } else if (modulePermission.__type === 'provider') {
      // Handle provider module with sub-modules
      if (activeSubModule) {
        const providerConfig = modulePermission as ProviderPermissionConfig;
        
        // Use recursive search to find the active sub-module config
        const findInAllLevels = (config: any, target: string): PermissionConfig | undefined => {
          if (config[target] && typeof config[target] === 'object' && config[target].type !== undefined) {
            return config[target] as PermissionConfig;
          }
          
          for (const key in config) {
            if (key === '__type') continue;
            const value = config[key];
            if (value && typeof value === 'object' && value.type === undefined) {
              const found = findInAllLevels(value, target);
              if (found) return found;
            }
          }
          return undefined;
        };
        
        const subModuleConfig = findInAllLevels(providerConfig, activeSubModule);
        if (subModuleConfig?.type === 'specific') {
          loadSpecificData(activeKey, activeSubModule);
        }
      }
    }
  }, [activeKey, activeSubModule, permissions, moduleTree]);

  // Rebuild permission state when module configuration updates
  useEffect(() => {
    if (moduleConfig.length > 0 && modules.length > 0) {
      const hasValue = value && Object.keys(value).length > 0;
      const newPermissions = buildInitialPermissions(modules, hasValue);
      setPermissions(newPermissions);
    }
  }, [moduleConfig, modules, buildInitialPermissions]);

  const loadSpecificData = useCallback(async (module: string, subModule?: string) => {
    console.log('loadSpecificData called with:', { module, subModule });
    const dataKey = subModule ? `${module}_${subModule}` : module;

    if (loading[dataKey]) {
      return;
    }

    try {
      setLoading(prev => ({ ...prev, [dataKey]: true }));

      const paginationInfo = pagination[dataKey] || { current: 1, pageSize: 10, total: 0 };

      const params: Record<string, any> = {
        app: clientId,
        module,
        child_module: subModule || '',
        page: paginationInfo.current,
        page_size: paginationInfo.pageSize,
        group_id: formGroupId
      };
      
      const data = await getAppData({ params });
      const currentPermissions = permissions;

      const formattedData = data.items.map((item: any) => {
        let currentPermission;
        
        // Use same recursive search logic as moduleContent
        if (subModule) {
          const modulePermission = currentPermissions[module];
          if (modulePermission && modulePermission.__type === 'provider') {
            const providerConfig = modulePermission as ProviderPermissionConfig;
            
            const findInAllLevels = (config: any, target: string): PermissionConfig | undefined => {
              if (config[target] && typeof config[target] === 'object' && config[target].type !== undefined) {
                return config[target] as PermissionConfig;
              }
              
              for (const key in config) {
                if (key === '__type') continue;
                const value = config[key];
                if (value && typeof value === 'object' && value.type === undefined) {
                  const found = findInAllLevels(value, target);
                  if (found) return found;
                }
              }
              return undefined;
            };
            
            const subModuleConfig = findInAllLevels(providerConfig, subModule);
            currentPermission = subModuleConfig?.specificData?.find(p => p.id === item.id);
          }
        } else {
          const moduleConfig = currentPermissions[module] as ModulePermissionConfig;
          currentPermission = moduleConfig.specificData?.find(p => p.id === item.id);
        }

        return {
          ...item,
          view: currentPermission?.view ?? false,
          operate: currentPermission?.operate ?? false
        };
      });

      setModuleData(prev => ({
        ...prev,
        [dataKey]: formattedData
      }));

      setPagination(prev => ({
        ...prev,
        [dataKey]: {
          ...paginationInfo,
          total: data.count
        }
      }));
    } catch (error) {
      console.error('Failed to load specific data:', error);
    } finally {
      setLoading(prev => ({ ...prev, [dataKey]: false }));
    }
  }, [clientId, permissions]);

  // Check if a subModule belongs to a module - supports multi-level nesting
  const isSubModuleOfModule = useCallback((module: string, subModule: string): boolean => {
    const moduleConfig = moduleTree[module];
    if (!moduleConfig?.children) return false;

    const findInChildren = (children: ModuleItem[]): boolean => {
      for (const child of children) {
        if (child.name === subModule) {
          return true;
        }
        if (child.children && findInChildren(child.children)) {
          return true;
        }
      }
      return false;
    };

    return findInChildren(moduleConfig.children);
  }, [moduleTree]);

  const handleTypeChange = useCallback((e: RadioChangeEvent, module: string, subModule?: string) => {
    console.log('handleTypeChange:', { module, subModule, value: e.target.value });
    const newPermissions = { ...permissions };

    const modulePermission = newPermissions[module];
    const hasSubModules = modulePermission && modulePermission.__type === 'provider';
    
    if (subModule && hasSubModules && isSubModuleOfModule(module, subModule)) {
      const providerConfig = { ...newPermissions[module] } as ProviderPermissionConfig;

      // Recursive function to set multi-level permission config
      const setNestedPermissionConfigDeep = (config: any, targetSubModule: string, newConfig: PermissionConfig): boolean => {
        if (config[targetSubModule] && typeof config[targetSubModule] === 'object' && config[targetSubModule].type !== undefined) {
          config[targetSubModule] = newConfig;
          return true;
        }
        
        for (const key in config) {
          if (key === '__type') continue;
          
          const value = config[key];
          if (value && typeof value === 'object' && value.type === undefined) {
            if (setNestedPermissionConfigDeep(value, targetSubModule, newConfig)) {
              return true;
            }
          }
        }
        
        return false;
      };

      const currentConfig = getPermissionConfig(newPermissions, module, subModule);
      const updatedConfig: PermissionConfig = {
        type: e.target.value,
        allPermissions: currentConfig?.allPermissions || { view: true, operate: true },
        specificData: currentConfig?.specificData || []
      };

      const updateSuccess = setNestedPermissionConfigDeep(providerConfig, subModule, updatedConfig);
      
      if (updateSuccess) {
        newPermissions[module] = providerConfig;

        if (e.target.value === 'specific') {
          loadSpecificData(module, subModule);
        }
      } else {
        console.error('Failed to update permissions for:', subModule);
      }
    } else {
      // Handle module without sub-modules
      const moduleConfig = { ...newPermissions[module] } as ModulePermissionConfig;
      moduleConfig.type = e.target.value;
      newPermissions[module] = moduleConfig;

      if (e.target.value === 'specific') {
        loadSpecificData(module);
      }
    }

    setPermissions(newPermissions);
    if (onChange) {
      onChange(newPermissions);
    }
  }, [permissions, isSubModuleOfModule]);

  const handleAllPermissionChange = useCallback((e: CheckboxChangeEvent, module: string, type: 'view' | 'operate', subModule?: string) => {
    const newPermissions = { ...permissions };

    const modulePermission = newPermissions[module];
    const hasSubModules = modulePermission && modulePermission.__type === 'provider';

    if (subModule && hasSubModules && isSubModuleOfModule(module, subModule)) {
      const providerConfig = { ...newPermissions[module] } as ProviderPermissionConfig;
      if (!providerConfig[subModule]) return;

      const subModuleConfig = {
        ...(providerConfig[subModule] as PermissionConfig),
        allPermissions: {
          ...(providerConfig[subModule] as PermissionConfig).allPermissions
        }
      };

      if (type === 'view') {
        subModuleConfig.allPermissions.view = e.target.checked;

        if (!e.target.checked) {
          subModuleConfig.allPermissions.operate = false;
        }
      } else if (type === 'operate') {
        if (subModuleConfig.allPermissions.view) {
          subModuleConfig.allPermissions.operate = e.target.checked;
        }
      }

      providerConfig[subModule] = subModuleConfig;
      newPermissions[module] = providerConfig;
    } else {
      const moduleConfig = {
        ...newPermissions[module],
        allPermissions: {
          ...(newPermissions[module] as ModulePermissionConfig).allPermissions
        }
      } as ModulePermissionConfig;

      if (type === 'view') {
        moduleConfig.allPermissions.view = e.target.checked;

        if (!e.target.checked) {
          moduleConfig.allPermissions.operate = false;
        }
      } else if (type === 'operate') {
        if (moduleConfig.allPermissions.view) {
          moduleConfig.allPermissions.operate = e.target.checked;
        }
      }

      newPermissions[module] = moduleConfig;
    }

    setPermissions(newPermissions);

    if (onChange) {
      onChange(newPermissions);
    }
  }, [permissions, isSubModuleOfModule]);

  const handleSpecificDataChange = useCallback((record: DataPermission, module: string, type: 'view' | 'operate', subModule?: string) => {
    const newPermissions = { ...permissions };
    const dataKey = subModule ? `${module}_${subModule}` : module;

    setModuleData(prev => {
      const newData = [...(prev[dataKey] || [])];
      const itemIndex = newData.findIndex(item => item.id === record.id);

      if (itemIndex > -1) {
        if (type === 'view') {
          newData[itemIndex] = {
            ...newData[itemIndex],
            view: record.view
          };

          if (!record.view) {
            newData[itemIndex].operate = false;
          }
        } else if (type === 'operate') {
          if (newData[itemIndex].view) {
            newData[itemIndex] = {
              ...newData[itemIndex],
              operate: record.operate
            };
          }
        }
      }

      return { ...prev, [dataKey]: newData };
    });

    const modulePermission = newPermissions[module];
    const hasSubModules = modulePermission && modulePermission.__type === 'provider';

    if (subModule && hasSubModules && isSubModuleOfModule(module, subModule)) {
      const providerConfig = { ...newPermissions[module] } as ProviderPermissionConfig;
      if (!providerConfig[subModule]) return;

      const subModuleConfig = {
        ...(providerConfig[subModule] as PermissionConfig),
        specificData: [...((providerConfig[subModule] as PermissionConfig).specificData || [])]
      };

      const dataIndex = subModuleConfig.specificData.findIndex(item => item.id === record.id);

      if (dataIndex === -1) {
        subModuleConfig.specificData.push(record);
      } else {
        const item = { ...subModuleConfig.specificData[dataIndex] };
        if (type === 'view') {
          item.view = record.view;
          if (!record.view) {
            item.operate = false;
          }
        } else if (type === 'operate') {
          if (item.view) {
            item.operate = record.operate;
          }
        }

        subModuleConfig.specificData[dataIndex] = item;
      }

      providerConfig[subModule] = subModuleConfig;
      newPermissions[module] = providerConfig;
    } else {
      const moduleConfig = {
        ...newPermissions[module],
        specificData: [...((newPermissions[module] as ModulePermissionConfig).specificData || [])]
      } as ModulePermissionConfig;

      const dataIndex = moduleConfig.specificData.findIndex(item => item.id === record.id);

      if (dataIndex === -1) {
        moduleConfig.specificData.push(record);
      } else {
        const item = { ...moduleConfig.specificData[dataIndex] };
        if (type === 'view') {
          item.view = record.view;
          if (!record.view) {
            item.operate = false;
          }
        } else if (type === 'operate') {
          if (item.view) {
            item.operate = record.operate;
          }
        }

        moduleConfig.specificData[dataIndex] = item;
      }

      newPermissions[module] = moduleConfig;
    }

    setPermissions(newPermissions);
    if (onChange) {
      onChange(newPermissions);
    }
  }, [permissions]);

  const handleTableChange = async (pagination: PaginationInfo, filters: any, sorter: any, module?: string, subModule?: string) => {
    if (!module) return;

    console.log('handleTableChange called with:', { module, subModule });
    const dataKey = subModule ? `${module}_${subModule}` : module;

    setPagination(prev => ({
      ...prev,
      [dataKey]: {
        current: pagination.current,
        pageSize: pagination.pageSize,
        total: prev[dataKey]?.total || 0
      }
    }));

    try {
      setLoading(prev => ({ ...prev, [dataKey]: true }));

      const params: Record<string, any> = {
        app: clientId,
        module,
        child_module: subModule || '',
        page: pagination.current,
        page_size: pagination.pageSize,
        group_id: formGroupId
      };

      const data = await getAppData({ params });

      const formattedData = data.items.map((item: any) => {
        let currentPermission;
        if (subModule) {
          const providerConfig = permissions[module] as ProviderPermissionConfig;
          const subModuleConfig = providerConfig[subModule] as PermissionConfig;
          currentPermission = subModuleConfig.specificData?.find(p => p.id === item.id);
        } else {
          const moduleConfig = permissions[module] as ModulePermissionConfig;
          currentPermission = moduleConfig.specificData?.find(p => p.id === item.id);
        }

        return {
          ...item,
          view: currentPermission?.view ?? false,
          operate: currentPermission?.operate ?? false
        };
      });

      setModuleData(prev => ({
        ...prev,
        [dataKey]: formattedData
      }));
    } catch (error) {
      console.error('Failed to load specific data:', error);
    } finally {
      setLoading(prev => ({ ...prev, [dataKey]: false }));
    }
  };

  // Show skeleton when module configuration is loading
  if (moduleConfigLoading) {
    return (
      <div className="permission-rule-skeleton">
        <Skeleton.Button active size="large" style={{ width: 120, marginRight: 16 }} />
        <Skeleton.Button active size="large" style={{ width: 100, marginRight: 16 }} />
        <Skeleton.Button active size="large" style={{ width: 140 }} />
        <div className="mt-6">
          <Skeleton active paragraph={{ rows: 8 }} />
        </div>
      </div>
    );
  }

  if (modules.length === 0) {
    return <div>{t('system.permission.noAvailableModules')}</div>;
  }

  const items = modules.map(module => {
    const moduleConfig = moduleTree[module];
    const hasSubModules = moduleConfig?.children && moduleConfig.children.length > 0;
    
    return {
      key: module,
      label: moduleTree[module]?.display_name,
      children: hasSubModules
        ? (
          <SubModuleTabs
            module={module}
            activeSubModule={activeSubModule}
            setActiveSubModule={setActiveSubModule}
            permissions={permissions}
            moduleData={moduleData}
            loadSpecificData={loadSpecificData}
            loading={loading}
            pagination={pagination}
            activeKey={activeKey}
            handleTypeChange={handleTypeChange}
            handleAllPermissionChange={handleAllPermissionChange}
            handleSpecificDataChange={handleSpecificDataChange}
            handleTableChange={handleTableChange}
            subModuleMap={subModuleMap}
            moduleTree={moduleTree}
          />
        )
        : (
          <ModuleContent
            module={module}
            permissions={permissions}
            loading={loading}
            moduleData={moduleData}
            pagination={pagination}
            activeKey={activeKey}
            activeSubModule={activeSubModule}
            handleTypeChange={handleTypeChange}
            handleAllPermissionChange={handleAllPermissionChange}
            handleSpecificDataChange={handleSpecificDataChange}
            handleTableChange={handleTableChange}
          />
        )
    };
  });

  return (
    <Tabs
      activeKey={activeKey}
      onChange={(key) => {
        if (key === activeKey) return;

        setActiveKey(key);

        const moduleConfig = moduleTree[key];
        const hasSubModules = moduleConfig?.children && moduleConfig.children.length > 0;
        
        if (hasSubModules) {
          const getFirstLeafModule = (module: ModuleItem): string => {
            if (module.children && module.children.length > 0) {
              return getFirstLeafModule(module.children[0]);
            }
            return module.name;
          };
          
          const firstLeafModule = getFirstLeafModule(moduleConfig);
          setActiveSubModule(firstLeafModule);

          if (!editableModules.includes(firstLeafModule)) {
            return;
          }

          const providerConfig = permissions[key] as ProviderPermissionConfig;
          const subModuleConfig = providerConfig[firstLeafModule] as PermissionConfig;

          if (subModuleConfig?.type === 'specific') {
            loadSpecificData(key, firstLeafModule);
          }
        } else {
          if (!editableModules.includes(key)) {
            return;
          }

          const moduleConfig = permissions[key] as ModulePermissionConfig;
          if (moduleConfig?.type === 'specific') {
            loadSpecificData(key);
          }
        }
      }}
      items={items}
      className="permission-rule-tabs"
    />
  );
};

export default React.memo(PermissionRule);

