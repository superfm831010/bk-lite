"use client";
import { Segmented, Menu, Button } from 'antd';
import stlyes from '@/app/lab/styles/index.module.scss';
import { useState, useEffect } from 'react';
import EntityList from '@/components/entity-list';
import useLabManage from '@/app/lab/api/manage';

const MirrorManage = () => {
  const [activeTab, setActiveTab] = useState<string>('ide');
  const tabOptions = [
    { label: 'IDE 镜像', value: 'ide' },
    { label: '基础设施镜像', value: 'infra' }
  ];

  const { getIdeImages, getInfraImages } = useLabManage();
  const [tableData, setTableData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // tab切换时请求镜像列表
  const fetchImages = async (type: string) => {
    setLoading(true);
    try {
      let res;
      if (type === 'ide') {
        res = await getIdeImages();
      } else {
        res = await getInfraImages();
      }
      setTableData(res || []);
    } catch (e) {
      console.log(e);
      setTableData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages(activeTab);
  }, [activeTab]);

  // 菜单操作
  const menuActions = (item: any) => (
    <Menu>
      <Menu.Item onClick={() => {console.log(item)}}>
        <Button type="text">编辑</Button>
      </Menu.Item>
      <Menu.Item onClick={() => {/* 删除逻辑 */}}>
        <Button type="text" danger>删除</Button>
      </Menu.Item>
    </Menu>
  );

  // 描述区域
  const descSlot = (item: any) => (
    <p className="text-right font-mini text-[var(--color-text-3)]">
      {`创建人: ${item.created_by || '--'}`}
    </p>
  );

  // 卡片点击
  const handleCardClick = (item: any) => {
    console.log(item);
    // 可跳转详情或弹窗
  };

  // 新增
  const handleAdd = () => {
    // 新增逻辑
  };

  // 搜索
  const handleSearch = () => {
    // 搜索逻辑
  };

  return (
    <div className={`w-full h-full ${stlyes.segmented}`}>
      <Segmented options={tabOptions} value={activeTab} onChange={(value) => setActiveTab(value)} />
      <div className='flex h-full w-full mt-4'>
        <EntityList
          data={tableData}
          menuActions={menuActions}
          loading={loading}
          onCardClick={handleCardClick}
          openModal={handleAdd}
          onSearch={handleSearch}
          descSlot={descSlot}
        />
      </div>
    </div>
  )
};

export default MirrorManage;