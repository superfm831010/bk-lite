'use client';
import { useState, useMemo, useRef } from "react";
import { useRouter } from "next/navigation";
import { useCopyToClipboard } from "@/app/mlops/hooks/useCopyToClipboard";
import CustomTable from "@/components/custom-table";
import Icon from "@/components/icon";
import { useTranslation } from "@/utils/i18n";
import { Button } from "antd";
import { PlusOutlined } from '@ant-design/icons';
import SubLayout from '@/components/sub-layout';
import ReleaseModal from "./releaseModal";
import { ModalRef, Pagination } from "@/app/mlops/types";
import { ColumnItem } from "@/types";


const ModelRelease = () => {
  const { t } = useTranslation();
  const router = useRouter();
  const modalRef = useRef<ModalRef>(null);
  const { copyToClipboard } = useCopyToClipboard();
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
      title: '模型介绍',
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: t(`common.action`),
      dataIndex: 'action',
      key: 'action',
      render: () => (
        <Button type="link" onClick={() => copyToClipboard('123')}>复制链接</Button>
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
    { id: 7, name: '异常检测训练', description: '1' },
    { id: 2, name: '异常检测训练', description: '2' },
    { id: 3, name: '异常检测训练', description: '3' },
  ];

  const publish = (record: any) => {
    modalRef.current?.showModal({ type: 'release', form: record })
    setPagination({
      current: 1,
      total: 0,
      pageSize: 20
    });
  };


  return (
    <div className="w-full relative">
      <SubLayout
        topSection={<Topsection />}
        intro={Intro}
        onBackButtonClick={() => router.back()}
      >
        <div className="flex justify-end mb-2">
          <Button type="primary" icon={<PlusOutlined />} onClick={() => publish({})}>模型发布</Button>
        </div>
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
      <ReleaseModal ref={modalRef} />
    </div>
  )
};

export default ModelRelease;