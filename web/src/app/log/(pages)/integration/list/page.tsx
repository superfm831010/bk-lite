'use client';
import React, { useEffect, useState } from 'react';
import { Spin, Input, Button, Tag } from 'antd';
import useApiClient from '@/utils/request';
import useIntegrationApi from '@/app/log/api/integration';
import integrationStyle from './index.module.scss';
import { SettingOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import Icon from '@/components/icon';
import { useCollectTypeInfo } from '@/app/log/hooks/integration/common/getCollectTypeConfig';
import { useRouter } from 'next/navigation';
import { CollectTypeItem } from '@/app/log/types/integration';
import { TableDataItem } from '@/app/log/types';
import Permission from '@/components/permission';
const { Search } = Input;

const Integration = () => {
  const { isLoading } = useApiClient();
  const { getCollectTypes } = useIntegrationApi();
  const { t } = useTranslation();
  const router = useRouter();
  const { getIcon } = useCollectTypeInfo();
  const [pageLoading, setPageLoading] = useState<boolean>(false);
  const [searchText, setSearchText] = useState<string>('');
  const [collectTypeList, setCollectTypeList] = useState<CollectTypeItem[]>([]);

  useEffect(() => {
    if (isLoading) return;
    getCollectTypeList();
  }, [isLoading]);

  const getCollectTypeList = async (params = {}) => {
    setPageLoading(true);
    try {
      const data = await getCollectTypes(params);
      setCollectTypeList(data);
    } finally {
      setPageLoading(false);
    }
  };

  const onSearchTxtChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(e.target.value);
  };

  const onTxtPressEnter = (val: string) => {
    setSearchText(val);
    const params = {
      name: val,
    };
    getCollectTypeList(params);
  };

  const linkToDetial = (app: CollectTypeItem) => {
    const row: TableDataItem = {
      icon: getIcon(app.name, app.collector),
      name: app.name,
      collector: app.collector,
      id: app.id,
      display_name: app.name,
      description: app.description || '--',
    };
    const params = new URLSearchParams(row);
    const targetUrl = `/log/integration/list/detail/configure?${params.toString()}`;
    router.push(targetUrl);
  };

  return (
    <div className={integrationStyle.integration}>
      <div className={integrationStyle.cards}>
        <div className="flex justify-end">
          <Search
            className="mb-[20px] w-60"
            allowClear
            enterButton
            placeholder={`${t('common.search')}...`}
            value={searchText}
            onChange={onSearchTxtChange}
            onSearch={onTxtPressEnter}
          />
        </div>
        <Spin spinning={pageLoading}>
          <div
            className={`flex flex-wrap w-full ${integrationStyle.integrationList}`}
          >
            {collectTypeList.map((app) => (
              <div key={app.id} className="w-full sm:w-1/4 p-2">
                <div className="bg-[var(--color-bg-1)] shadow-sm hover:shadow-md transition-shadow duration-300 ease-in-out rounded-lg p-4 relative cursor-pointer group">
                  <div className="flex items-center space-x-4 my-2">
                    <Icon
                      type={getIcon(app.name, app.collector)}
                      className="text-[48px] min-w-[48px]"
                    />
                    <div
                      style={{
                        width: 'calc(100% - 60px)',
                      }}
                    >
                      <h2
                        title={app.name}
                        className="text-xl font-bold m-0 hide-text"
                      >
                        {app.name || '--'}
                      </h2>
                      <Tag className="mt-[4px]">{app.collector}</Tag>
                    </div>
                  </div>
                  <p
                    className={`mb-[15px] text-[var(--color-text-3)] text-[13px] ${integrationStyle.lineClamp3}`}
                    title={app.description || '--'}
                  >
                    {app.description || '--'}
                  </p>
                  <div className="w-full h-[32px] flex justify-center items-end">
                    <Permission
                      requiredPermissions={['Setting']}
                      className="w-full"
                    >
                      <Button
                        icon={<SettingOutlined />}
                        type="primary"
                        className="w-full rounded-md transition-opacity duration-300"
                        onClick={(e) => {
                          e.stopPropagation();
                          linkToDetial(app);
                        }}
                      >
                        {t('common.setting')}
                      </Button>
                    </Permission>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Spin>
      </div>
    </div>
  );
};

export default Integration;
