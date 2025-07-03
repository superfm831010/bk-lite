'use client';
import CustomTable from "@/components/custom-table";
import { useTranslation } from "@/utils/i18n";
import { ColumnItem } from "@/types";
import SubLayout from '@/components/sub-layout';
import { Button } from "antd";
import { useState } from "react";
import { Pagination } from "../../../types";

const ModelRelease = () => {
  const { t } = useTranslation();
  const [pagination, setPagination] = useState<Pagination>({
    current: 1,
    total: 0,
    pageSize: 20
  });

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

  const mock = [
    { id: 1, name: '异常检测训练', version: 1.0 },
    { id: 2, name: '异常检测训练', version: 2.0 },
    { id: 3, name: '异常检测训练', version: 3.0 },
  ]

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
        intro={<></>}
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