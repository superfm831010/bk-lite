'use client';
import CustomTable from "@/components/custom-table";
import Icon from "@/components/icon";
import { useTranslation } from "@/utils/i18n";
import { ColumnItem } from "@/types";
import SubLayout from '@/components/sub-layout';
import { Button } from "antd";
import { useState, useMemo } from "react";
import { Pagination } from "@/app/mlops/types";
// import type { TableProps } from "antd";

const ModelRelease = () => {
  const { t } = useTranslation();
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20
  });

  const Intro = useMemo(() => {
    return (
      <div className="flex h-[58px] flex-row items-center">
        <Icon
          type="yunquyu"
          className="h-16 w-16"
          style={{ height: '36px', width: '36px' }}
        ></Icon>
        <h1 className="ml-2 text-center truncate">{t(`traintask.traintask`)}</h1>
      </div>
    );
  }, []);

  const columns: ColumnItem[] = [
    {
      title: '模型名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '模型版本',
      dataIndex: 'version',
      key: 'version'
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      render: () => (
        <Button type="link" onClick={publish}>发布</Button>
      )
    }
  ];

  const Topsection = () => {
    return (
      <div className="flex flex-col h-[90px] p-4 overflow-hidden">
        <h1 className="text-lg truncate w-full mb-1">{t('model-release.title')}</h1>
        <p className="text-sm overflow-hidden w-full min-w-[1000px] mt-[8px]">
          {t('model-release.detail')}
        </p>
      </div>
    )
  };

  const mock = [
    { id: 1, name: '异常检测训练', version: 'v1' },
    { id: 2, name: '异常检测训练', version: 'v2' },
    { id: 3, name: '异常检测训练', version: 'v3' },
  ];

  



  const publish = () => {
    setPagination({
      current: 1,
      total: 0,
      pageSize: 20
    });
  }


  return (
    <div className="w-full relative">
      <SubLayout
        topSection={<Topsection />}
        intro={Intro}
      >
        <div className="flex-1 relative">
          <div className="absolute w-full">
            <CustomTable
              columns={columns}
              dataSource={mock}
              rowKey='id'
              pagination={pagination}
            />
          </div>
        </div>
      </SubLayout>
    </div>
  )
};

export default ModelRelease;